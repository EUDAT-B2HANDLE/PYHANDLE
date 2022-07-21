==============
PyHandleClient
==============


This is the main class of the PYHANDLE Library. 
From Here you may understand the PyHandle library and the method it provides.
PyHandleClient is the main class of the PyHandle library and provides methods to:

 * select a client (REST, DB or Batch)
 * authenticate to the Handle System server
 * invoke methods to create, retrieve, update and delete Handles

Select a client
===============

PyHandleClient acts as a factory that takes arguments to determine what type of client to instantiate.
There are two interfaces to interact with the Handle System server: REST, DB or Batch.
User selects the client by passing the client as String to the PyHandleClient class and if required by the client more parameters.

.. code:: python

   from pyhandle.handleclient import PyHandleClient

and then:

* REST

.. code:: python

   client = PyHandleClient('rest')

* DB

.. code:: python

   client = PyHandleClient('db', credentials)

* Batch

.. code:: python

   client = PyHandleClient('batch')

Each client has its own methods and rules to authenticate to the Handle server. When some methods of REST client do not require authentication/authorization (see :doc:`pyhandleclientrest`), all methods related to DB or Batch need authorization.

Credentials are mandatory when creating a DB client. In that case, information about the database have to be
passed to the client (see :doc:`pyhandleclientdb`). Authentication within the Batch client is explained in :doc:`pyhandleclientbatch` and can be performed after instantiating the client.



.. Constructors
.. ------------

.. .. automethod:: pyhandle.client.resthandleclient.RESTHandleClient.__init__

.. .. automethod:: pyhandle.client.resthandleclient.RESTHandleClient.instantiate_for_read_access

.. .. automethod:: pyhandle.client.resthandleclient.RESTHandleClient.instantiate_for_read_and_search

.. .. automethod:: pyhandle.client.resthandleclient.RESTHandleClient.instantiate_with_username_and_password

.. .. automethod:: pyhandle.client.resthandleclient.RESTHandleClient.instantiate_with_credentials

