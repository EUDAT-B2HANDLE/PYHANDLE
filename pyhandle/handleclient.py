'''
This module provides the main client for the PYHANDLE
    library.
'''

import logging
import pyhandle
import requests

from . import util
from pyhandle.client.dbhandleclient import DBHandleClient
from pyhandle.client.resthandleclient import RESTHandleClient

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(util.NullHandler())
REQUESTLOGGER = logging.getLogger('log_all_requests_of_testcases_to_file')
REQUESTLOGGER.propagate = False
REQUESTLOGGER.addHandler(util.NullHandler())

class PyHandleClient(object):
    ''' PYHANDLE main client class '''

    HANDLE_CLIENTS = [DBHandleClient, RESTHandleClient]

    def __init__(self, client, credentials=None):
        allowed_args = ['rest', 'db', 'batch']
        if client in allowed_args:
            self.client = client
            self.credentials = credentials
            self.handle_client = self.select_handle_client()
        else:
            raise ValueError("Allowed clients: 'rest', 'db' or 'batch'")

    def select_handle_client(self):
        for client in self.HANDLE_CLIENTS:
            if client.check_client(self.client):
                return client(self.credentials)

    # Instantiate methods for REST

    def instantiate_for_read_access(self, **config):
        return self.handle_client.instantiate_for_read_access()

    def instantiate_with_credentials(self, credentials, **config):
        return self.handle_client.instantiate_with_credentials(credentials, **config)

    def instantiate_with_username_and_password(self, handle_server_url, username, password, **config):
        return self.handle_client.instantiate_with_username_and_password(handle_server_url, username, password,
                                                                         **config)

    def instantiate_for_read_and_search(self, handle_server_url, reverselookup_username, reverselookup_password,
                                        **config):
        return self.handle_client.instantiate_for_read_and_search(handle_server_url, reverselookup_username,
                                                                      reverselookup_password, **config)
    # Methods for REST and DB

    def retrieve_handle(self, handle):
        return self.handle_client.retrieve_handle_record(handle)

    def get_value_from_handle(self, handle, key):
        return self.handle_client.get_value_from_handle(handle, key)

    def modify_handle_value(self, handle, **kvpairs):
        self.handle_client.modify_handle_value(handle, **kvpairs)

    def delete_handle_value(self, handle, key):
            self.handle_client.delete_handle_value(handle, key)

    def delete_handle(self, handle):
        self.handle_client.delete_handle(handle)

    def generate_and_register_handle(self, prefix, location, checksum=None, **extratypes):
        return self.handle_client.generate_and_register_handle(prefix, location, checksum, **extratypes)

    def register_handle(self, handle, location, checksum=None, overwrite=False, **extratypes):
        self.handle_client.register_handle(handle, location, checksum=None, overwrite=False, **extratypes)

    # Methods for DB
    def list_handles(self):
        return self.handle_client.list_all_handles()

    def check_if_handle_exists(self, handle):
        return self.handle_client.check_if_handle_exists(handle)
