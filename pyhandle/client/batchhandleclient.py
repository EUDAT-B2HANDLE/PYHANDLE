'''
This class provides methods to create batch file that contains different operations on Handle.
The batch file is executed by the hdl-genericbatch (hdl-genericbatch <batchfile>).

Author Sofiane Bendoukha (DKRZ), 2017.
'''
from __future__ import absolute_import

import logging
import os


from pyhandle.pyhandleclient import HandleClient
from .. import util

logging.basicConfig(level=logging.INFO)

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(util.NullHandler())
REQUESTLOGGER = logging.getLogger('log_all_requests_of_testcases_to_file')
REQUESTLOGGER.propagate = False


class BatchHandleClient(HandleClient):
    '''The BatchHandleClient class'''

    HANDLE_CLIENT = 'batch'
    __base_client_batch_path = './pyhandle/batch/'

    def __init__(self):

        LOGGER.debug('\n' + 60 * '*' + '\nInstantiation of BatchHandleClient\n' + 60 * '*')

    def create_batch_file(self, batch_file_name=None):
        '''

        :param batch_file_name: The name of the batch file as a String
        :return: __batch_file
        '''
        LOGGER.debug('BatchHandleClient')

        if batch_file_name is None:
            # Create a new empty batch file "handle_batch"
            temp_file = os.open(self.__base_client_batch_path + 'handle_batch', os.O_WRONLY | os.O_CREAT |
                                os.O_EXCL)
            __batch_file = os.fdopen(temp_file, "w")  # standard Python file object
        else:
            temp_file = os.open(batch_file_name, os.O_WRONLY | os.O_CREAT | os.O_EXCL)
            __batch_file = os.fdopen(temp_file, "w")  # standard Python file object

        return __batch_file

    def register_handle_batch(self, handle, url, hdl_admin_index, admin_handle, perm):
        '''
        This method creates a simple Handle record including a Handle value to define the administrator of the Handle
        and the value for the location (URL)..
        Operation name is 'CREATE'. The first line is composed of the following:
               CREATE + space + handle_name.

        :param handle: The handle name which will be created
        :param url: The location
        :param hdl_admin_index: Unique index number
        :param admin_handle: Administrator of the Handle
        :param perm: permissions
        '''
        LOGGER.debug("Creating a handle (batch)")

        batch_file = self.__base_client_batch_path + '/handle_batch'

        with open(batch_file, 'a') as bfile:
            bfile.write('\nCREATE ' + handle + '\n100 HS_ADMIN 86400 1110 ADMIN ' + str(hdl_admin_index)
                        + ':' + perm + ':' + admin_handle)

        with open(batch_file, 'a') as bfile:
            bfile.write('\n\nADD ' + handle + '\n1 URL 86400 1110 UTF8 ' + url)

    def delete_handle(self, handle):
        '''
        This method deletes an existing Handle completely.
        :param handle: Handle name to be deleted

        '''
        LOGGER.debug("Deleting a handle (batch)")

        batch_file = self.__base_client_batch_path + '/handle_batch'

        with open(batch_file, 'a') as bfile:
            bfile.write('\nDELETE ' + handle)

    def modify_handle_value(self, handle, **kvpairs):
        '''
        This method changes Handle values for an existing Handle.
        :param handle:
        :param kvpairs: Contains the unique index number, Handle value type and the value data

        '''
        LOGGER.debug("Modifying a value of handle (batch)")

        batch_file = self.__base_client_batch_path + '/handle_batch'

        if kvpairs:
            self.type = kvpairs['type']
            self.index = kvpairs['index']
            self.data = kvpairs['data']

            with open(batch_file, 'a') as bfile:
                bfile.write('\nMODIFY ' + handle + '\n' + str(self.index) + ' ' + self.type + ' 86400 1110 UTF8 ' +
                            self.data)

    def add_handle_value(self, handle, **kvpairs):
        '''
        The method adds new handle values to an existing handle
        :param handle: The handle where the new value will be added
        :param kvpairs: Contains the unique index number, Handle value type and the value data

        '''
        LOGGER.debug("Modifying a value of handle (batch)")

        batch_file = self.__base_client_batch_path + '/handle_batch'

        if kvpairs:
            self.type = kvpairs['type']
            self.index = kvpairs['index']
            self.data = kvpairs['data']

            with open(batch_file, 'a') as  bfile:
                bfile.write('\nADD ' + handle + '\n' + str(self.index) + ' ' + self.type + ' 86400 1110 UTF8 ' +
                            self.data)

    def delete_handle_value(self, handle, value_index):
        '''
        This method removes one or more handle values from an existing handle
        :param handle: The handle containing the value to be deleted
        :param value_index: The index of the value

        '''
        LOGGER.debug("Modifying a value of handle (batch)")

        batch_file = self.__base_client_batch_path + '/handle_batch'

        if len(value_index) == 1:
            with open(batch_file, 'a') as bfile:
                bfile.write('\nREMOVE ' + str(value_index[0]) + ':' + handle)

        else:
            with open(batch_file, 'a') as bfile:
                for key in range(len(value_index)):
                    bfile.write('\nREMOVE ' + str(value_index[key]) + ':' + handle)



    def authenticate_seckey(self, user, password):

        batch_file = self.__base_client_batch_path + '/handle_batch'

        with open(batch_file, 'w') as bfile:
            bfile.write('AUTHENTICATE SECKEY:' + user + '\n' + password)

        return batch_file

    def authenticate_pubkey(self, user, priv_key_path, passphrase=None):
        '''

        :param user: admin_index:admin_handle
        :param pubkey_path: private_key_file_path
        :param passphrase: If your private key was created and encrypted by passphrase

        '''

        batch_file = self.__base_client_batch_path + '/handle_batch'

        if passphrase is not None:
            with open(batch_file, 'w') as bfile:
                bfile.write('AUTHENTICATE PUBKEY:' + user + '\n' + priv_key_path + '|' + passphrase)

        else:
            with open(batch_file, 'w') as bfile:
                bfile.write('AUTHENTICATE PUBKEY:' + user + '\n' + priv_key_path)

