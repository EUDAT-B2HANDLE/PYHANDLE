'''
This class provides methods to create batch file that contains different operations on Handle.
The batch file is executed by the hdl-genericbatch (hdl-genericbatch <batchfile>).

Author Sofiane Bendoukha (DKRZ), 2017.
'''
from __future__ import absolute_import

import logging
import os
from os.path import expanduser

from pyhandle.batchhsexceptions import BatchFileExistsException
from pyhandle.pyhandleclient import HandleClient
from pyhandle.clientcredentials import PIDClientCredentials

from .. import util

logging.basicConfig(level=logging.INFO)

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(util.NullHandler())

class BatchHandleClient(HandleClient):
    '''The BatchHandleClient class'''

    HANDLE_CLIENT = 'batch'
    HOME_DIRECTORY = expanduser("~")
    _default_batch_file_path = HOME_DIRECTORY + '/handle_batch'

    def __init__(self, **args):
        '''
        Initialize the batch client and set the path for the batch file.

        :param credentials: Optional. As json file in form {"user":"user", "password":"password"}
        :param args: Optional. This includes different parameters concerning the batch file, such as the PATH.
        '''

        LOGGER.debug('\n' + 60 * '*' + '\nInstantiation of BatchHandleClient\n' + 60 * '*')




        super(BatchHandleClient, self).__init__()

        self.__all_args = args
        self.__batch_file_path = args['batch_file_path']

        if self.__batch_file_path is None:
            self.__batch_file_path = self._default_batch_file_path

    def create_batch_file(self, overwrite=False):
        '''
        Creates a batch file in a directory specified by the user or in the default directory
              (./pyhandle/batch/handle_batch).

        :param overwrite: Optional. If set to True, the existing batch file
            will be overwritten. Defaults to False.
        :raises: :exc:`~pyhandle.batchhsexceptions.BatchFileExistsException` Only if overwrite is not set or
            set to False.
        '''

        LOGGER.debug('BatchHandleClient')

        batch_file_path = self.get_batch_file_path()

        if overwrite:
            batch_file = os.fdopen(os.open(batch_file_path, os.O_CREAT | os.O_WRONLY), "w")
            batch_file.seek(0)
            batch_file.truncate()

        else:
            try:
                batch_file = os.fdopen(os.open(batch_file_path, os.O_CREAT | os.O_WRONLY | os.O_EXCL), "w")
                batch_file.close()

            except Exception as exc:
                if exc.args[0] == 17:
                    msg = 'Could not create batch file, already exists'
                    LOGGER.error(msg + ', as it already exists.')
                    raise BatchFileExistsException(file=self.get_batch_file_path(), msg=msg)

    def register_handle_batch(self, handle, location, hdl_admin_index, admin_handle, perm):
        '''
        This method creates a simple Handle record including a Handle value to define the administrator of the Handle
        and the value for the location (URL)..
        Operation name is 'CREATE'. The first line is composed of the following:
               CREATE + space + handle_name.

        :param handle: The full name of the handle to be registered (prefix
            and suffix)
        :param location: The URL of the data entity to be referenced
        :param hdl_admin_index: Unique index number
        :param admin_handle: Administrator of the Handle
        :param perm: permissions
        :raises: :exc:`~pyhandle.batchhsexceptions.BatchFileExistsException`.
        '''

        LOGGER.debug("Creating a handle (batch)")

        if self.check_if_file_exists(self.get_batch_file_path()):
            with open(self.get_batch_file_path(), 'a') as bfile:
                bfile.write('\nCREATE ' + handle + '\n100 HS_ADMIN 86400 1110 ADMIN ' + str(hdl_admin_index)
                            + ':' + perm + ':' + admin_handle)

            with open(self.get_batch_file_path(), 'a') as bfile:
                bfile.write('\n\nADD ' + handle + '\n1 URL 86400 1110 UTF8 ' + location)

        else:
            msg = 'does not exists'
            raise BatchFileExistsException(file=self.get_batch_file_path(), msg=msg)

    def delete_handle(self, handle):
        '''
        This method deletes an existing Handle and its records.
        Operation name 'DELETE'.

        :param handle: Handle name to be deleted
        :raises: :exc:`~pyhandle.batchhsexceptions.BatchFileExistsException`.
        '''

        LOGGER.debug("Deleting a handle (batch)")

        if self.check_if_file_exists(self.get_batch_file_path()):
            with open(self.get_batch_file_path(), 'a') as bfile:
                bfile.write('\nDELETE ' + handle)
        else:
            msg = 'does not exists'
            raise BatchFileExistsException(file=self.get_batch_file_path(), msg=msg)

    def modify_handle_value(self, handle, **kvpairs):
        '''
        This method changes Handle values for an existing Handle.
        Operation name 'MODIFY'

        :param handle: Handle whose record is to be modified
        :param kvpairs: Contains the unique index number, Handle value type and the value data
        :raises: :exc:`~pyhandle.batchhsexceptions.BatchFileExistsException`.

        '''

        LOGGER.debug("Modifying a value of handle (batch)")

        if kvpairs:
            self.type = kvpairs['type']
            self.index = kvpairs['index']
            self.data = kvpairs['data']

            if self.check_if_file_exists(self.get_batch_file_path()):
                with open(self.get_batch_file_path(), 'a') as bfile:
                    bfile.write('\nMODIFY ' + handle + '\n' + str(self.index) + ' ' + self.type + ' 86400 1110 UTF8 ' +
                                self.data)
            else:
                msg = 'does not exists'
                raise BatchFileExistsException(file=self.get_batch_file_path(), msg=msg)

    def add_handle_value(self, handle, **kvpairs):
        '''
        The method adds new handle values to an existing handle.
        Operation name 'ADD'.

        :param handle: The handle where the new value will be added
        :param kvpairs: Contains the unique index number, Handle value type and the value data
        :raises: :exc:`~pyhandle.batchhsexceptions.BatchFileExistsException`.

        '''

        LOGGER.debug("Add handle value")

        if kvpairs:
            self.type = kvpairs['type']
            self.index = kvpairs['index']
            self.data = kvpairs['data']

        if self.check_if_file_exists(self.get_batch_file_path()):
            with open(self.get_batch_file_path(), 'a') as  bfile:
                bfile.write('\nADD ' + handle + '\n' + str(self.index) + ' ' + self.type + ' 86400 1110 UTF8 ' +
                            self.data)
        else:
            msg = 'does not exists'
            raise BatchFileExistsException(file=self.get_batch_file_path(), msg=msg)

    def delete_handle_value(self, handle, value_index):
        '''
        This method removes one or more handle values from an existing handle.
        Operation name 'REMOVE'.

        :param handle: Handle from whose record the entry should be deleted.
        :param value_index: The index of the value
        :raises: :exc:`~pyhandle.batchhsexceptions.BatchFileExistsException`.

        '''

        LOGGER.debug("Delete handle value")

        if self.check_if_file_exists(self.get_batch_file_path()):
            if len(value_index) == 1:
                with open(self.get_batch_file_path(), 'a') as bfile:
                    bfile.write('\nREMOVE ' + str(value_index[0]) + ':' + handle)

            else:
                with open(self.get_batch_file_path(), 'a') as bfile:
                    for key in range(len(value_index)):
                        bfile.write('\nREMOVE ' + str(value_index[key]) + ':' + handle)

        else:
            msg = 'does not exists'
            raise BatchFileExistsException(file=self.get_batch_file_path(), msg=msg)

    def authenticate_seckey(self, user, password):
        '''
        Secret key authentication. Operation name 'AUTHENTICATE'.

        :param user: This must be a handle value reference in the format
            "index:prefix/suffix".
        :param password: This is the password stored as secret key in the
            actual Handle value the username points to.
        :param credentials: Optional. When credentials are
        :raises: :exc:`~pyhandle.batchhsexceptions.BatchFileExistsException`.

        '''

        LOGGER.debug("Authenticate with SECKEY")

        if self.check_if_file_exists(self.get_batch_file_path()):
            with open(self.get_batch_file_path(), 'a') as bfile:
                bfile.write('\nAUTHENTICATE SECKEY:' + user + '\n' + password)
        else:
            msg = 'does not exists'
            raise BatchFileExistsException(file=self.get_batch_file_path(), msg=msg)

    def authenticate_pubkey(self, user, priv_key_path, passphrase=None):
        '''
        Private key authentication. Operation name 'AUTHENTICATE'.

        :param user: admin_index:admin_handle
        :param pubkey_path: private_key_file_path
        :param passphrase: If your private key was created and encrypted by passphrase
        :raises: :exc:`~pyhandle.batchhsexceptions.BatchFileExistsException`.
        '''

        LOGGER.debug("Authenticate with PUBKEY")

        if self.check_if_file_exists(self.get_batch_file_path()):
            if passphrase:
                with open(self.get_batch_file_path(), 'w+') as bfile:
                    bfile.write('AUTHENTICATE PUBKEY:' + user + '\n' + priv_key_path + '|' + passphrase)

            else:
                with open(self.get_batch_file_path(), 'w+') as bfile:
                    bfile.write('AUTHENTICATE PUBKEY:' + user + '\n' + priv_key_path)

        else:
            msg = 'does not exists'
            raise BatchFileExistsException(file=self.get_batch_file_path(), msg=msg)


    def authenticate_with_credentials(self, credentials, auth_type):
        '''
        Set the credentials for seckey and pubkey authentication.

        :param credentials: A credentials object, see separate class
            PIDClientCredentials.
        :param auth_type: Set authentication type to 'seckey' (username:password)
            or to pubkey (privatekey | passphrase).
        '''

        if isinstance(credentials, PIDClientCredentials):
            self.credentials = credentials.get_all_args()
        else:
            self.credentials = credentials

        self.username = credentials.get_username()
        self.password = credentials.get_password()
        self.private_key = credentials.get_path_to_private_key()
        self.passphrase = credentials.get_key_passphrase()


        if auth_type == "seckey":
            self.authenticate_seckey(self.username, self.password)

        if auth_type == "pubkey":
            self.authenticate_pubkey(self.username, self.private_key, passphrase=self.passphrase)

    def get_all_args(self):
        return self.__all_args

    def get_batch_file_path(self):
        return self.__batch_file_path

    def check_if_file_exists(self, file_path):
        if os.path.isfile(file_path):
            return True
        return False
