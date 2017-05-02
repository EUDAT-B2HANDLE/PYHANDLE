'''
This module provides the main client for the PYHANDLE
    library.
'''

from __future__ import absolute_import

import logging 
import pyhandle
import requests

from . import util
from pyhandle.client import dbhandleclient, resthandleclient, batchhandleclient


class PyHandleClient(object):
    ''' PYHANDLE main client class '''
    
    def __new__(cls, client, credentials=None):
      '''
        Return an instance of a the client class depending on user input.
        :param client: a string to define the client class ('db', 'rest' or 'batch')
        :raises ValueError(msg)
        :returns client_instance: an instance of the client
      '''
      
      if client == 'db':
          client_instance = object.__new__(dbhandleclient.DBHandleClient, credentials)
          client_instance.__init__(credentials)   
      elif client == 'rest':
        client_instance = object.__new__(resthandleclient.RESTHandleClient)
        client_instance.__init__()
      elif client == 'batch':
        client_instance = object.__new__(batchhandleclient.BatchHandleClient)
        client_instance.__init__() 
      else:
        raise ValueError("Accepted arguments : 'rest', 'db' or 'batch'")    
      
      return client_instance  

    def __init__(self, client, credentials=None):
      if credentials is not None:
        self.credentials = credentials
        self.client = client

 
    


