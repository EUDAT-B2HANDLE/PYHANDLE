from __future__ import absolute_import

import logging
import pymysql


from past.builtins import basestring 
from .. import util
from pyhandle.dbhsexceptions import DBHandleNotFoundException, DBHandleKeyNotFoundException, DBHandleAlreadyExistsException, DBHandleKeyNotSpecifiedException

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(util.NullHandler())
REQUESTLOGGER = logging.getLogger('log_all_requests_of_testcases_to_file')
REQUESTLOGGER.propagate = False



class DBHandleClient(object):
          
    _handle_db_connection = None
    _handle_db_cur = None

    def __init__(self, credentials, **args):
        '''
        Initialize the DB client. Instantiate a connection object and connect to the HS database

        :param db_host: host where the handle server database is located
        :param db_user: username to log in as
        :param db_password: password for db_user
        :param db_name: database name
        '''
        
        LOGGER.debug('\n' + 60 * '*' + '\nInstantiation of DBHandleClient\n' + 60 * '*')
                
        super(DBHandleClient, self).__init__()

        if credentials is not None:
            self.db_host = credentials['db_host']
            self.db_user = credentials['db_user']
            self.db_password = credentials['db_password']
            self.db_name = credentials['db_name']
        else:
            raise ValueError('No credentials given')
            
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
               
    def search_handle(self, **args):
        '''
        Search for handles containing the specified key with the specified
        value.         
        :param key_value_pairs: Optional. Several search fields and values can
            be specified as key-value-pairs,
            e.g. CHECKSUM=123456, URL=www.foo.com
        :return: A list of all Handles (list of strings) that bear the given key with
            given value of given prefix or server. The list may be empty and
            may also contain more than one element.
        ''' 
                 
        # Check if there is any key-value pairs to be searched.
        if len(args) == 0:
            LOGGER.debug('search_handle: No key value pair was specified.')
            msg = 'No search terms have been specified. Please specify' + \
                ' at least one key-value-pair.'
            raise DBHandleKeyNotSpecifiedException(msg=msg)
                  
        for key in args.keys():
            key = key
            value = args[key]
            query = "SELECT handle from handles WHERE type='%s' AND data='%s'" % (key, value)   
            query_result = self.execute_query(query)
                
        list_handles = []
        
        for key in range(len(query_result)):
            list_handles.append(query_result[key]['handle'])
        
        return list_handles
        
    def execute_query_customized(self, handle, key=None, query=None):
        '''
        Execute the SQL query
        :param query: the sql query to be performed
        :return: result: query result as list of dictionaries
        '''
        
        LOGGER.debug('Get handle, key and execute query')
        
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
        :return: query_as_dict
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
            temp_dict = {query_result[key]['type'].decode('utf-8'):query_result[key]['data'].decode('utf-8')}
            result_as_dict.update(temp_dict)
            LOGGER.debug('Query result %s', result_as_dict)
            
        return result_as_dict

    def check_if_handle_exists(self, handle):
        '''
        This statement is used to query whether or not a given handle exists in the database
        :param handle: The handle being queried
        :return True if handle exists
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
        
    def register_handle(self, handle, url, overwrite=False, **args):
        '''
        Register a new Handle with given name. If the handle already exists
        and overwrite is not set to True, the method will throw an
        exception.

        :param handle: The full name of the handle to be registered (prefix
            and suffix)
        :param url; The URL of the data entity to be referenced
        :param overwrite: Optional. If set to True, an existing handle record
            will be overwritten. Defaults to False.
        :raises: :exc:`~pyhandle.handleexceptions.HandleAlreadyExistsException` Only if overwrite is not set or
            set to False.
        
        '''
        LOGGER.debug('register_handle...')
        
        # default idx for url
        idx = 1
        # If already exists and can't be overwritten:
        if overwrite == False:
            handle_exists = self.check_if_handle_exists(handle)
            if handle_exists:
                msg = 'Could not register handle'
                LOGGER.error(msg + ', as it already exists.')
                raise DBHandleAlreadyExistsException(handle=handle, msg=msg)
               
        query = "INSERT INTO handles (handle, idx, type, data) values ('%s', '%s', '%s', '%s')" % (handle, idx, 'URL', url)
        self.execute_query(query)        
        
    def add_handle_value(self, handle, key):
        '''
        Add a key-value pair from a handle record.
        :param handle: Handle from whose record they entry should be deleted.
        :param key: Key to be deleted.
        '''
        
        LOGGER.debug('Add handle value')
        
        if handle_exist(handle):
           query = "INSERT INTO handles WHERE handle= '%s' AND type='%s'" % (handle, key)
           self.execute_query_customized(handle, key, query)

    def get_value_from_handle(self, handle, key):
        ''' 
        Retrieve a single value from a single handle.
        :param handle: The handle to take the value from.
        :param key: The key.
        :raises::exc:'~pyhandle.handleexceptions.DBHandleNotFoundException'
        :raises::exc:'~pyhandle.handleexceptions.DBHandleKeyNotFoundException'
        :return: string containing the value.
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
        Delete handle and its handle record
        :param handle: Handle being deleted
        :raises::exc:'~pyhandle.handleexceptions.DBHandleNotFoundException'
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
        :param handle
        :return list_idx: list of indices 
        '''
        list_idx = []
        query = "SELECT idx FROM handles WHERE handle='%s'" % handle
        query_result = self.execute_query(query)
        
        for key in range(len(query_result)):
            list_idx.append(query_result[key]['idx'])
        return list_idx            
            
    def list_all_handles(self):
        ''' Get a list of all of the handles in the database. '''
        
        list_all_handles = []
        query = 'SELECT DISTINCT handle FROM handles'
        result_query = self.execute_query(query)
        for key in range(len(result_query)):
            list_all_handles.append(str(result_query[key]['handle']))
        return list_all_handles

    def list_handles_by_prefix(self, prefix):
        ''' Get a list of handles in the database that have a given prefix.
        :param prefix: The prefix, including the slash ('/') character.
        :raises::exc:'~pyhandle.handleexceptions.HandleNotFoundOnDBException'
        :return handle_records: list of handles
        '''

        query = "SELECT DISTINCT handle FROM handles WHERE handle LIKE '%s'" % prefix
        handle_records = self.execute_query(query)
        return handle_records

    def retrieve_handle_record(self, handle):
        '''
        Retrieve a handle record from the Handle server database as a dict.
        :param handle
        :return handle_records_as_dict: 
        '''
        
        LOGGER.info("Retrieving handle record (db)")
        query = "SELECT type, data FROM handles WHERE handle= '%s'" % handle
        
        handle_records = self.execute_query(query)
        handle_records_as_dict = self.convert_query_result_to_dict(handle_records)
        return handle_records_as_dict
        
    def modify_handle_value(self, handle, ttl= None, add_if_not_exists=True, **kvpairs):
        ''' 
        This statement is used to update a single handle value with new values. The value to
        update is identified by the handle and index.
        Modify entries (key-value pairs).
        :param handle: Handle whose record is to be modified
        :param key: The key to be added/modified 
        :param ttl: Optional. Integer value. If ttl should be set to a
            non-default value.
        :param all other args: The user can specify several key-value-pairs.
            These will be the handle value types and values that will be
            modified. The keys are the names or the handle value types (e.g.
            "URL"). The values are the new values to store in "data".
        :raises::exc:`~pyhandle.dbhsexceptions.DBHandleNotFoundException`    
        '''
        
        LOGGER.info("Modify handle value (db)")
                
        handle_key = list(kvpairs.keys())
        handle_value = list(kvpairs.values())
               
        # check if handle and the key already exist
        handle_record_exists = self.check_if_handle_exists(handle)
        key_exists = self.check_if_key_exists(handle, handle_key[0])
        
        if handle_record_exists:
            if  key_exists:
                # update the value of the key
                idx_key = self.get_idx_existing_key(handle, handle_key[0])
                query = "UPDATE handles set data = '%s' WHERE handle = '%s' and idx = '%s'" % (handle_value[0], handle, idx_key)
                self.execute_query(query)
            elif add_if_not_exists:
                LOGGER.debug('modify_handle_value: Adding entry "' + str(handle_key) + '"' + \
                        ' to handle ' + handle)
                self.create_new_value(handle, handle_key = handle_key[0], handle_value = handle_value[0])
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
                
        if kvpairs is not None:
            self.handle_key = str(kvpairs['handle_key'])
            self.handle_value = str(kvpairs['handle_value'])

        newidx = self.create_new_index(handle)
        
        query = "INSERT INTO handles (idx, handle, type, data, ttl_type, ttl) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (newidx, handle, self.handle_key, self.handle_value, '0', '86400')
        result = self.execute_query(query)
         
    def create_new_index(self, handle, url=False, hs_admin=False):
        '''
        Find an index not yet used in the handle record and not reserved for
            any (other) special type.

        :param: handle: The handle in which indices will be allocated
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
        handle_record = self.retrieve_handle_record(self.handle)
        handle_key = kvpairs['handle_key']

        value_exists = False
        
        if handle_key[0] in handle_record.keys():
           return True
        else:
            return False       
     
    def check_if_key_exists(self, handle, key):
        '''
        Check if a given key exists in a handle record
        :param handle: The handle in which the key is searched
        :param key: The key
        :return True if key exists
        '''
        
        query_result = self.retrieve_handle_record(handle)
        handle_keys = list(query_result.keys())
        
        if key in handle_keys:
            return True
        return False
                  
    def retrieve_handle_record_all(self, handle):
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
        query = "SELECT idx, type, data, ttl_type, ttl, timestamp, refs, admin_read, admin_write, pub_read, pub_write FROM handles \
                WHERE handle = '%s'" % handle
               
        handle_records = self.execute_query(query)
        
        handle_records = self.convert_query_result_to_dict(handle_records)
        
        return handle_records

    def get_query_from_user(self, query):
        ''' 
        Execute the SQL query formulated by user
        :param query: the sql query to be performed
        :return handle_record: 
        '''
        
        handle_records = self.execute_query(query)
        LOGGER.debug('Get query from user %s', handle_records)
        return handle_records

    def create_list_of_queries(query):
        ''' 
        Create a list of queries, which will be executed in a specific order
        :param query: The query to be added to the list.
        :return query_list: A list of queries
        '''

        list_queries = []
        listqueries.append(query)
        return list_queries

    @staticmethod
    def connection_status(self, handle_db_connection):
        if self.handle_db_connection:
            return True
        return False

    def _db_disconnect(self):
        ''' Close the connection to the database. '''
        self._handle_db_connection.close()
    
    def convert(data):
        if isinstance(data, basestring):
            return str(data)
        elif isinstance(data, collections.Mapping):
            return dict(map(convert, data.iteritems()))
        elif isinstance(data, collections.Iterable):
            return type(data)(map(convert, data))
        else:
            return data
