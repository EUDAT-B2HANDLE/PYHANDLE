'''
This module contains the exceptions that may occur in
libraries interacting with the Handle System (Database).

Author: Sofiane Bendoukha, DKRZ, 2016-2017

'''

from __future__ import absolute_import


class DBHandleNotFoundException(Exception):
    ''' Raises when handle not found in database'''

    def __init__(self, **args):
        self.msg = 'Handle not found on Server'
        self.handle = args['handle']

        if self.handle is not None:
            self.msg = self.msg.replace('andle', 'andle ' + self.handle)

        if self.msg is None:
            self.msg = "Handle not found in DB"

        super(self.__class__, self).__init__(self.msg)


class DBHandleKeyNotSpecifiedException(Exception):
    """ Raises when no search items has been provided """

    def __init__(self, **args):
        # Default message:
        self.msg = 'Error during searching'
        self.custom_message = args['msg']

        if self.custom_message is not None:
            self.msg += '.'

        super(self.__class__, self).__init__(self.msg)


class DBHandleAlreadyExistsException(Exception):
    '''
    To be raised if self.handle already exists.
    '''

    def __init__(self, **args):

        # Default message:
        self.msg = 'Handle already exists'

        # Possible arguments:
        optional_args = ['msg', 'handle']
        self.handle = args['handle']
        self.custom_message = args['msg']

        if self.handle is not None:
            self.msg = self.msg.replace('andle', 'andle ' + self.handle)

        if self.custom_message is not None:
            self.msg += ': ' + self.custom_message
        self.msg += '.'

        super(self.__class__, self).__init__(self.msg)


class DBHandleNoCredentialsError(Exception):
    ''' Raises when insufficient credentials are given'''

    def __init__(self, msg=None):
        if msg is None:
            msg = "Insufficient credentials"
        super(self.__class__, self).__init__(msg)


class DBHandleKeyNotFoundException(Exception):
    ''' Raises when handle key not found'''

    def __init__(self, **args):
        self.msg = 'Key not found in Handle'
        self.handle = args['handle']
        self.key = args['key']

        if self.handle is not None:
            if self.key is not None:
                self.msg = self.msg.replace('andle', 'andle ' + self.handle)
                self.msg = self.msg.replace('ey', 'ey ' + self.key)

        if self.msg is None:
            self.msg = 'Handle key not found'

        super(self.__class__, self).__init__(self.msg)
