"""
This class provides different methods to manage Handles using the database interface.

Author: Sofiane Bendoukha (DKRZ), 2017
"""
from __future__ import absolute_import

import binascii
import codecs
import logging
import sys
import uuid
import pymysql

from pyhandle.clientcredentials import PIDClientCredentials
from pyhandle.dbhsexceptions import DBHandleNotFoundException, DBHandleKeyNotFoundException, \
    DBHandleAlreadyExistsException, DBHandleKeyNotSpecifiedException
from pyhandle.pyhandleclient import HandleClient

from .. import util
from ..util import timeutil

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(util.NullHandler())


class DBHandleClient(HandleClient):
    _handle_db_connection = None
    _handle_db_cur = None
    HANDLE_CLIENT = 'db'

    def __init__(self, credentials, **args):
        '''
        Initialize the DB client. Instantiate a connection object and connect to the HS database

        :param db_host: host where the handle server database is located
        :param db_user: username to log in as
        :param db_password: password for db_user
        :param db_name: database name
        '''

        LOGGER.debug('\n' + 60 * '*' + '\nInstantiation of DBHandleClient\n' + 60 * '*')


        if credentials is None:
            raise ValueError('No credentials given')

        if isinstance(credentials, PIDClientCredentials):
            self.credentials = credentials.get_all_args()
        else:
            self.credentials = credentials

        self.db_host = self.credentials['db_host']
        self.db_user = self.credentials['db_user']
        self.db_password = self.credentials['db_password']
        self.db_name = self.credentials['db_name']

        try:
            self._handle_db_connection = pymysql.connect(self.db_host,
                                                         self.db_user,
                                                         self.db_password,
                                                         self.db_name,
                                                         cursorclass=pymysql.cursors.DictCursor)
            self._handle_db_cur = self._handle_db_connection.cursor()

        except pymysql.InternalError as error:
            code, message = error.args
            print(">>>>>>>>>>>>>", code, message)
            sys.exit(1)

    def execute_query(self, query):
        '''
        Execute the SQL query.

        :param query: the sql query to be performed

        :return: result_as_dict: the result of the sql query as dictionary
        '''

        LOGGER.debug('Execute query')

        result = None
        self.query = query

        try:
            with self._handle_db_cur as cursor:
                self_handle_db_cur = self._handle_db_connection.cursor()
                self_handle_db_cur.execute(self.query)
                result = self_handle_db_cur.fetchall()
            self._handle_db_connection.commit()
            LOGGER.debug('Query result %s', result)

        except pymysql.InternalError as error:
            code, message = error.args
            print(">>>>>>>>>>>>>", code, message)
        return result

    def search_handle(self, pattern=None, limit=None, offset=None, **args):
        '''
        Search for handles containing the specified key with the specified
        value (one key-value). The number of record can be controlled by limit and offset.

        :param pattern: Optional. This value can be set to do search depending on the handle name.
        :param limit: Optional. Limit the number of results returned in a SQL statement.
        :param offset: Optional. Page number, first row to return. Initial raw is 0.
        :param args: e.g URL='www.example.com'
        :return: A list of all Handles (list of strings) that bear the given key with
            given value of given prefix or server. The list may be empty and
            may also contain more than one element.
        '''

        query_result = []
        list_handles = []

        # Check if there is any key-value pairs to be searched.
        if len(args) == 0:
            LOGGER.debug('search_handle: No key value pair was specified.')
            msg = 'No search terms have been specified. Please specify' + \
                  ' at least one key-value-pair.'
            raise DBHandleKeyNotSpecifiedException(msg=msg)

        if limit:
            if offset is None:
                offset = 0
            list_handles= self.__search_handle_limit(
                pattern=pattern,
                limit=limit,
                offset=offset,
                **args
            )
        else:
           for key in args.keys():
                key = key
                value = args[key]
                if pattern:
                    query = "SELECT handle from handles WHERE handle LIKE '%s' AND type= '%s' AND data='%s'" % (pattern, key, value)
                else:
                    query = "SELECT handle from handles WHERE type= '%s' AND data LIKE '%s'" % (key, value)

                query_result = self.execute_query(query)

           for key in range(len(query_result)):
                list_handles.append(query_result[key]['handle'])

        return list_handles

    def __search_handle_limit(self, pattern, limit, offset, **args):
        '''
        Search handles with limit and offset.

        :param pattern: Optional. This value can be set to do search depending on the handle name.
        :param limit:  Optional. Number of records to return from the SQL statement.
        :param offset: Page number, first row to return. Initial raw is 0.
        :param args: search items as key-value e.g URL='www.example.com'
        :return: list_handles: A list of all Handles (list of strings) that bear the given key with
            given value of given prefix or server. The list may be empty and
            may also contain more than one element.
        '''
        query_result = []
        list_handles = []

        # Check if there is any key-value pairs to be searched.
        if len(args) == 0:
            LOGGER.debug('search_handle: No key value pair was specified.')
            msg = 'No search terms have been specified. Please specify' + \
                  ' at least one key-value-pair.'
            raise DBHandleKeyNotSpecifiedException(msg=msg)

        for key in args.keys():
            key = key
            value = args[key]
            if pattern:
                query = "SELECT handle from handles WHERE handle LIKE '%s' AND type= '%s' AND data='%s' LIMIT %s" \
                        " OFFSET %s" % (pattern, key, value, limit, offset)
            else:
                query = "SELECT handle from handles WHERE type= '%s' AND data LIKE '%s' LIMIT %s OFFSET %s" % (key,
                value, limit, offset)

            query_result = self.execute_query(query)

        for key in range(len(query_result)):
            list_handles.append(query_result[key]['handle'])

        return list_handles

    #TODO
    def search_handle_multiple_keys(self, **args):
        '''
        Search for handles containing the specified key(s) with the specified
        value(s).

        :param args: Several search fields and values can
            be specified as key-value-pairs,
            e.g. CHECKSUM=123456, URL=www.foo.com

        :return: A list of all Handles (list of strings) that bear the given key with
            given value of given prefix or server. The list may be empty and
            may also contain more than one element.
        '''

        list_handles = []
        temp_list = []

        # Check if there is any key-value pairs to be searched.
        if len(args) == 0:
               LOGGER.debug('search_handle: No key value pair was specified.')
               msg = 'No search terms have been specified. Please specify' + \
                 ' at least one key-value-pair.'
               raise DBHandleKeyNotSpecifiedException(msg=msg)


        for key, value in args.items():

            query = "SELECT handle from handles WHERE type LIKE '%s' AND data LIKE '%s'" % (key, value)
            query_result = self.get_query_from_user(query)
            if query_result is None:
               break
            for k in range(len(query_result)):
                 if query_result[k]['handle'] in list_handles:
                    temp_list.append(query_result[k]['handle'])

                 list_handles.append(query_result[k]['handle'])
        return temp_list


    def execute_query_customized(self, handle, key=None, query=None):
        '''
        Execute the customized SQL query.

        :param key: Optional.
        :param handle: Handle name
        :param query: the sql query to be performed
        :return: Query result as list of dictionaries
        '''

        LOGGER.debug('Get handle, key and execute query')

        result = None

        try:
            self_handle_db_cur = self._handle_db_connection.cursor()
            self_handle_db_cur.execute(query, (handle, key))
            result = self_handle_db_cur.fetchall()

            LOGGER.debug('Query result %s', result)
        except pymysql.InternalError as error:
            code, message = error.args
            print(">>>>>>>>>>>>>", code, message)
        return result

    def convert_query_result_to_dict(self, query_result):
        '''
        Convert the query result (list) to dictionary

        :param query_result: the result of the sql query (list)
        :return: The result of the query as a dictionary (No HS values)
        '''

        LOGGER.debug('Convert query result to dict')

        result_as_dict = {}
        hs_keys = ['HS_ADMIN', 'HS_SITE', 'HS_PUBKEY', 'HS_SECKEY', 'HS_ALIAS', 'HS_VLIST', 'HS_SERV']
        all_keys = list(set().union(*(d.keys() for d in query_result)))

        skip = False
        for key in range(len(query_result)):
            skiped_key = query_result[key]['type'].decode('utf-8')

            if skiped_key in hs_keys:
                skip = True
                continue
            if skip:
                skip = False
                continue
            temp_dict = {query_result[key]['type'].decode('utf-8'): query_result[key]['data'].decode('utf-8')}
            result_as_dict.update(temp_dict)
            LOGGER.debug('Query result %s', result_as_dict)

        return result_as_dict

    def check_if_handle_exists(self, handle):
        '''
        This statement is used to query whether or not a given handle exists in the database

        :param handle: The handle being queried.
        :return: True if handle exists.
        '''

        query_result_as_dict = {}
        query = "SELECT count(*) FROM handles WHERE handle= '%s'" % handle

        query_result = self.execute_query(query)
        query_result_as_dict = query_result[0]
        query_result_as_dict = query_result_as_dict['count(*)']
        LOGGER.debug('Query result %s', query_result_as_dict)

        if query_result_as_dict is not 0:
            return True
        else:
            return False

    def generate_PID_name(self, prefix=None):
        '''
        Generate a unique random Handle name (random UUID). The Handle is not
        registered. If a prefix is specified, the PID name has the syntax
        <prefix>/<generatedname>, otherwise it just returns the generated
        random name (suffix for the Handle).

        :param prefix: Optional. The prefix to be used for the Handle name.
        :return: The handle name in the form <prefix>/<generatedsuffix> or
            <generatedsuffix>.
        '''

        LOGGER.debug('generate_PID_name...')

        randomuuid = uuid.uuid4()
        if prefix is not None:
            return prefix + '/' + str(randomuuid)
        else:
            return str(randomuuid)

    def generate_and_register_handle(self, prefix, location, checksum=None, **extratypes):
        '''
        Register a new Handle with a unique random name (random UUID).

        :param prefix: The prefix of the handle to be registered. The method
            will generate a suffix.
        :param location: The URL of the data entity to be referenced.
        :param checksum: Optional. The checksum string.
        :param extratypes: Optional. Additional key value pairs as dict.

        :return: The new handle name.
        '''

        LOGGER.debug('generate_and_register_handle...')

        handle = self.generate_PID_name(prefix)
        handle = self.register_handle(
            handle,
            location,
            checksum,
            overwrite=True,
            **extratypes
        )

        return handle

    def register_handle(self, handle, url, overwrite=False, **args):
        '''
        Register a new Handle with given name. If the handle already exists
        and overwrite is not set to True, the method will throw an
        exception.

        :param handle: The full name of the handle to be registered (prefix
            and suffix)
        :param url: The URL of the data entity to be referenced
        :param overwrite: Optional. If set to True, an existing handle record
            will be overwritten. Defaults to False.
        :param args: Mandatory key_value parameters for the admin of the Handle being created.
               Example:

                        admin_handle = 'prefix/suffix'.

                        admin_handle_index = 200.

                        perm = '111111111111'
        :raises: :exc:`~pyhandle.handleexceptions.HandleAlreadyExistsException` Only if overwrite is not set or
            set to False.
        '''
        LOGGER.debug('register_handle...')

        # Get values for HS_ADMIN
        self.admin_handle = args['admin_handle']
        self.admin_handle_index = args['admin_handle_index']
        self.perm = args['permissions']

        # Set current UNIX time
        ts = timeutil.generate_timestamp()

        handle_exists = self.check_if_handle_exists(handle)

        # default idx for url
        idx = 1
        # If already exists and can't be overwritten:
        if not overwrite:

            if handle_exists:
                msg = 'Could not register handle'
                LOGGER.error(msg + ', as it already exists.')
                raise DBHandleAlreadyExistsException(handle=handle, msg=msg)

        if handle_exists:
            self.delete_handle(handle)

        # Create handle without HS_ADMIN
        query = "INSERT INTO handles (handle, idx, type, data, ttl_type, ttl, timestamp, refs, admin_read, " \
                "admin_write, pub_read, " \
                "pub_write) values (" \
                "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (handle, idx, 'URL', url,
                                                                                             '0', '86400', ts, '', '1',
                                                                                             '1', '1', '0')
        self.execute_query(query)

        # Add HS_ADMIN values (default values 0.NA/prefix)

        self.add_admin_entry(handle, self.admin_handle, self.admin_handle_index, self.perm)

    def add_handle_value(self, handle, key):
        '''
        Add a key-value pair from a handle record.

        :param handle: Handle from whose record they entry should be deleted.
        :param key: Key to be deleted.
        '''

        LOGGER.debug('Add handle value')

        if self.check_if_handle_exists(handle):
            query = "INSERT INTO handles WHERE handle= '%s' AND type='%s'" % (handle, key)
            self.execute_query_customized(handle, key, query)

    def get_value_from_handle(self, handle, key):
        '''
        Retrieve a single value from a single handle.

        :param handle: The handle to take the value from.
        :param key: The key.

        :raises: :exc:`~pyhandle.dbhsexceptions.DBHandleNotFoundException`
        :raises: :exc:`~pyhandle.dbhsexceptions.DBHandleKeyNotFoundException`
        :return: A string containing the value.
        '''

        LOGGER.debug('Get value from handle')

        query = "SELECT data FROM handles WHERE handle= '%s' AND type='%s'" % (handle, key)
        handle_records = self.execute_query(query)

        handle_record_exists = self.check_if_handle_exists(handle)
        key_exists = self.check_if_key_exists(handle, key)

        if handle_record_exists:
            if key_exists:
                result = handle_records[0]
                handle_value = result['data']
                return handle_value
            else:
                msg = 'Key not found in Handle'
                raise DBHandleKeyNotFoundException(handle=handle, key=key, msg=msg)
        else:
            msg = 'Cannot modify unexisting handle'
            raise DBHandleNotFoundException(handle=handle, msg=msg)

    def delete_handle(self, handle):
        '''
        Delete handle and its handle record.

        :param handle: Handle being deleted

        :raises: :exc:`~pyhandle.dbhsexceptions.DBHandleNotFoundException`

        '''

        LOGGER.debug('delete handle')
        handle_exists = self.check_if_handle_exists(handle)

        # delete query
        if handle_exists:
            query = "DELETE FROM handles WHERE handle= '%s'" % handle
            self.execute_query(query)
        else:
            msg = 'Handle does not exists'
            raise DBHandleNotFoundException(handle=handle)

    def delete_handle_value(self, handle, key):
        '''
        Delete a key-value pair from a handle record. If the key exists more
        than once, all key-value pairs with this key are deleted.

        :param handle: Handle from whose record the entry should be deleted.
        :param key: Key to be deleted. Also accepts a list of keys.
        '''
        LOGGER.debug('delete_handle_value...')

        key_exists = self.check_if_key_exists(handle, key)
        if key_exists:
            query = "DELETE FROM handles WHERE handle= '%s' AND type='%s'" % (handle, key)
            self.execute_query(query)
        else:
            msg = 'Key not found in Handle'
            raise DBHandleKeyNotFoundException(handle=handle, key=key, msg=msg)

    def get_list_of_idx(self, handle):
        '''
        Create a list of indices already used.

        :param handle: the handle to extract the indexes from.

        :return: list_idx: List of indices
        '''

        list_idx = []
        query = "SELECT idx FROM handles WHERE handle='%s'" % handle
        query_result = self.execute_query(query)

        for key in range(len(query_result)):
            list_idx.append(query_result[key]['idx'])
        return list_idx

    def list_all_handles(self):
        ''' Get a list of all of the handles in the database.

        :return: A list of all handles in the table
        '''

        list_all_handles = []
        query = 'SELECT DISTINCT handle FROM handles'
        result_query = self.execute_query(query)
        for key in range(len(result_query)):
            list_all_handles.append(str(result_query[key]['handle']))
        return list_all_handles

    def list_handles_by_prefix(self, prefix):
        ''' Get a list of handles in the database that have a given prefix.

        :param prefix: The prefix, including the slash ('/') character.

        :raises: :exc:`~pyhandle.handleexceptions.HandleNotFoundOnDBException`
        :return: List of handles
        '''

        query = "SELECT DISTINCT handle FROM handles WHERE handle LIKE '%s'" % prefix
        handle_records = self.execute_query(query)
        return handle_records

    def retrieve_handle_record_without_HS_values(self, handle):
        '''
        Retrieve a handle record from the Handle server database as a dict.

        :param handle: The handle whose record is to be retrieved.

        :raises: :exc:`~pyhandle.dbhsexceptions.DBHandleNotFoundException`
        :return: The handle record values as a list.
        '''

        LOGGER.info("Retrieving handle record (db)")
        handle_record_exists = self.check_if_handle_exists(handle)
        if handle_record_exists:
            query = "SELECT type, data FROM handles WHERE handle= '%s'" % handle
            handle_records = self.execute_query(query)
        else:
            msg = 'Handle not found'
            raise DBHandleNotFoundException(handle=handle)

        handle_records_as_dict = self.convert_query_result_to_dict(handle_records)
        return handle_records_as_dict

    def modify_handle_value(self, handle, ttl=None, add_if_not_exists=True, **kvpairs):
        '''
        This statement is used to update a single handle value with new values. The value to
        update is identified by the handle and index.
        Modify entries (key-value pairs).


        :param handle: Handle whose record is to be modified
        :param ttl: Optional. Integer value. If ttl should be set to a
            non-default value.
        :param kvpairs: The user can specify several key-value-pairs.
            These will be the handle value types and values that will be
            modified. The keys are the names or the handle value types (e.g.
            "URL"). The values are the new values to store in "data".
        :param add_if_not_exists: Optional.

        :raises: :exc:`~pyhandle.dbhsexceptions.DBHandleNotFoundException`
        '''

        LOGGER.info("Modify handle value (db)")

        handle_key = list(kvpairs.keys())
        handle_value = list(kvpairs.values())

        # check if handle and the key already exist
        handle_record_exists = self.check_if_handle_exists(handle)
        key_exists = self.check_if_key_exists(handle, handle_key[0])

        if handle_record_exists:
            if key_exists:
                # update the value of the key
                idx_key = self.get_idx_existing_key(handle, handle_key[0])
                query = "UPDATE handles set data = '%s' WHERE handle = '%s' and idx = '%s'" % (handle_value[0], handle,
                                                                                               idx_key)
                self.execute_query(query)
            elif add_if_not_exists:
                LOGGER.debug('modify_handle_value: Adding entry "' + str(handle_key) + '"' + \
                             ' to handle ' + handle)
                self.create_new_value(handle, handle_key=handle_key[0], handle_value=handle_value[0])
        else:
            msg = 'Cannot modify unexisting handle'
            raise DBHandleNotFoundException(handle=handle, msg=msg)

    def get_idx_existing_key(self, handle, key):

        query = "SELECT idx FROM handles WHERE handle='%s' AND type= '%s'" % (handle, key)
        query_result = self.execute_query(query)

        list_idx = query_result[0]['idx']

        return list_idx

    def create_new_value(self, handle, **kvpairs):
        '''
        Add new handle value.

        :param: handle: The handle in which the value will be added
        :param: **kvpairs: any other key-value pairs
        '''

        ts = timeutil.generate_timestamp()

        if kvpairs is not None:
            self.handle_key = str(kvpairs['handle_key'])
            self.handle_value = str(kvpairs['handle_value'])

        newidx = self.create_new_index(handle)

        query = "INSERT INTO handles (idx, handle, type, data, ttl_type, ttl, timestamp, refs, admin_read, " \
                "admin_write, pub_read, pub_write) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', " \
                "'%s', '%s', '%s')" % (
                    newidx, handle, self.handle_key, self.handle_value, '0', '86400', ts, '', '1', '1', '1', '0')
        self.execute_query(query)

    def add_admin_entry(self, handle, admin_handle, admin_handle_index, perm):
        '''
        Create an HS_ADMIN entry.
        The admin value is byte array constant, which means that all handle created use the same HS_ADMIN value.

        :param handle: The handle in which the HS-ADMIN value is added
        :param admin_handle: The administrator of the Handle (prefix/suffx)
        :param admin_handle_index: The index of the admin_handle
        :param perm: The permissions of the administrator of the handle in form '101001010100'
        '''

        index_length = 8
        hsadmin_index = hex(admin_handle_index)[2:]

        # Add missing values to index hex
        for k in range(index_length - len(hsadmin_index)):
            hsadmin_index = "0" + hsadmin_index

        admin_perm = hex(int(perm, 2))[2:]

        if sys.version_info[0] >= 3:
            admin_handle = codecs.encode(admin_handle.encode(), 'hex').decode('UTF-8')
        else:
            admin_handle = admin_handle.encode('hex')

        hsadmin_hex_value = '0' + admin_perm + "0000000f" + admin_handle + hsadmin_index

        admin_idx = '100'

        ts = timeutil.generate_timestamp()

        query = "INSERT INTO handles (idx, handle, type, data, ttl_type, ttl, timestamp, refs, admin_read, " \
                "admin_write, " \
                "pub_read, pub_write) VALUES ('%s', '%s', '%s', UNHEX('%s'), '%s', '%s', '%s', '%s', '%s', '%s', '%s', " \
                "'%s')" \
                % (admin_idx, handle, 'HS_ADMIN', hsadmin_hex_value, '0', '86400',
                   ts, '', '1', '1', '1', '0')
        self.execute_query(query)

    def create_new_index(self, handle, url=False, hs_admin=False):
        '''
        Find an index not yet used in the handle record and not reserved for
            any (other) special type.

        :param handle: The handle in which indices will be allocated
        :param url: If True, an index for an URL entry is returned (1, unless
            it is already in use).
        :param hs_admin: If True, an index for HS_ADMIN is returned (100 or one
            of the following).
        :return: An integer.
        '''

        start = 2

        # reserved indices:
        reserved_for_url = set([1])
        reserved_for_admin = set(range(100, 200))
        prohibited_indices = reserved_for_url | reserved_for_admin

        if url:
            prohibited_indices = prohibited_indices - reserved_for_url
            start = 1
        elif hs_admin:
            prohibited_indices = prohibited_indices - reserved_for_admin
            start = 100

        # existing indices
        list_of_indices_already_used = set(self.get_list_of_idx(handle))

        # find new index:
        all_prohibited_indices = list_of_indices_already_used | prohibited_indices

        searchmax = max(start, max(all_prohibited_indices)) + 2
        for index in range(start, searchmax):
            if index not in all_prohibited_indices:
                return index

    def check_if_value_exists(self, handle, **kvpairs):

        self.handle = handle
        handle_record = self.retrieve_handle_record_without_HS_values(self.handle)
        handle_key = kvpairs['handle_key']

        value_exists = False

        if handle_key[0] in handle_record.keys():
            return True
        else:
            return False

    def check_if_key_exists(self, handle, key):
        '''
        Check if a given key exists in a handle record.

        :param handle: The handle in which the key is searched
        :param key: The key
        :return: True if key exists
        '''

        query_result = self.retrieve_handle_record_without_HS_values(handle)
        handle_keys = list(query_result.keys())

        if key in handle_keys:
            return True
        return False

    def retrieve_handle_record_json(self, handle):
        '''
        This statement is used to retrieve the set of handle values associated with a handle
        from the database.

        :param handle: The name of the handle to be queried.
        :return: handle_records: This contains
                idx positive integer value: unique across all values for the handle
                type alphanumeric value: indicates the type of the data in each value
                                        data alphanumeric value; the data associated with
                                        the value ttl type byte/short; 0=relative, 1=absolute
                ttl numeric: cache timeout for this value in seconds (if ttl type is absolute, then this indicates
                             the date/time of expiration in seconds since Jan 1 0:00:00 1970.
                timestamp numeric: the date that this value was last modified, in seconds since Jan 1 0:00:00
                                   1970
                refs alphanumeric: list of tab delimited index:handle pairs. In each pair, tabs that occur in the
                                  handle part are escaped as \t.
                admin read boolean: indicates whether clients with administrative privileges have access to
                                   retrieve the handle value
                admin write boolean: indicates whether clients with administrative privileges have
                                   permission to modify the handle value
                pub read boolean: indicates whether all clients have permission to retrieve the handle value
                pub write boolean: indicates whether all clients have permission to modify the handle value
        '''

        # pylint: disable=missing-docstring
        query = "SELECT idx, type, data, ttl, timestamp FROM handles WHERE handle = '%s'" % handle

        handle_records = self.execute_query(query)

        return handle_records

    def get_query_from_user(self, query):
        '''
        Execute the SQL query formulated by user.

        :param query: the sql query to be performed
        :return: The handle record
        '''

        handle_records = self.execute_query(query)
        LOGGER.debug('Get query from user %s', handle_records)
        return handle_records

    @staticmethod
    def create_list_of_queries(query):
        '''
        Create a list of queries, which will be executed in a specific order.

        :param query: The query to be added to the list.
        :return: A list of queries
        '''

        list_queries = []
        list_queries.append(query)
        return list_queries

    @staticmethod
    def pretty_print(record):
        '''
        Print the query result as a table.
        :param record: The result of the query as dict.
        '''
        for key, value in record.items():
            print("----------------------------------------")
            print("{:<15} {:<25}".format(key, value))

    @staticmethod
    def connection_status(handle_db_connection):
        '''
        Check whether a connection to DB is open.

        :param handle_db_connection:
        :return: True if connection is open
        '''
        if handle_db_connection:
            return True
        return False

    def _db_disconnect(self):
        ''' Close the connection to the database. '''

        self._handle_db_connection.close()

    def retrieve_handle_record(self, handle):
        '''
        Retrieve all Handle record values including HS_ADMIN
        Extract HS_ADMIN value from the query result and converts it to Hex.

        :param handle: The handle from which the values are retrieved.
        :return: handle_records: All values of the Handle including HS_ADMIN.
        '''

        scale = 16

        num_of_bits = 12

        hsadmin = ''

        handle_records = self.retrieve_handle_record_without_HS_values(handle)

        handle_records_json = self.retrieve_handle_record_json(handle)

        # Get value of HS_ADMIN
        for k in range(len(handle_records_json)):
            if handle_records_json[k]['type'] == b'HS_ADMIN':
                hsadmin = handle_records_json[k]['data']

        hexhsadmin = binascii.hexlify(hsadmin)

        hs_admin_index = self.get_hs_admin_index(hexhsadmin)

        length_record = len(hexhsadmin)
        admin_handle = binascii.unhexlify(hexhsadmin[12:int(length_record - 8)]).decode('utf-8')

        # Get and convert permissions
        permissions = hexhsadmin[:4]

        perm_bin = bin(int(permissions, scale))[2:].zfill(num_of_bits)

        temp_dict = {'handle': admin_handle, 'index': hs_admin_index, 'permissions': perm_bin}

        handle_records.update({'HS_ADMIN': temp_dict})

        return handle_records

    @staticmethod
    def get_hs_admin_index(hexhsadmin):

        hexadmin_length = len(hexhsadmin)
        hs_admin_index = int(hexhsadmin[hexadmin_length - 8:hexadmin_length], 16)

        return hs_admin_index

    def get_permissions_from_hsadmin_hex(self, handle):
        '''

        :param handle: The handle for which the permissions are retrieved.
        :return: permission: Bit-like permissions
        '''

        handle_record_hex = self.convert_hs_admin_values_to_hex(handle)
        permissions = handle_record_hex[:4]

        return permissions

    def convert_permissions_to_binary(self, handle):
        '''
        Get permissions in HEX form and convert them to binary.

        :param handle: The Handle that contains the permissions
        :return: perm_bin
        '''

        scale = 16

        num_of_bits = 12

        perm = self.get_permissions_from_hsadmin_hex(handle)

        perm_bin = bin(int(perm, scale))[2:].zfill(num_of_bits)

        return perm_bin
