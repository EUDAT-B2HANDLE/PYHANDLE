================
DB Handle Client
================

The DB Handle client provides methods to create, update and delete Handles directly via the (SQL) database of the
Handle System server.

.. note::
   The current version of the library supports MySQL database.

.. important::
   The DB client does not provide a read-only mode. All operations require authentication.

Instantiation
=============

As described in the :doc:`pyhandleclient`, credentials and information about the database server are required in
order to instantiate the DB client.

.. code:: python

   from pyhandle.handleclient import PyHandleClient
   client = PyHandleClient('db', credentials)

The credentials can loaded from a file or passed as a dictionary to the PyHandleClient

.. code:: python

   credentials = {'db_host':'', 'db_user':'', 'db_pass':'', 'db_name':''}

Credentials can be also loaded from a json file using the PIDClientCredentials class as follows:

.. code:: python

    cred = PIDClientCredentials.load_from_JSON('my_credentials.json')
    client = PyHandleClient('db', cred)

The JSON file should look like this:

  .. code:: json

    {
      "client":"",
      "db_host": "https://handle.server",
      "db_user": "db_user",
      "db_password": "db_password",
      "db_name": "db_name"
    }

Then the client's methods can be used to read, create, modify or delete Handles

.. code:: python

   value = client.some_methods(...)


Basic Handle interaction
========================

Creating a Handle
  Use :meth:`~pyhandle.client.dbhandleclient.DBHandleClient.register_handle` to create a Handle with a custom name
   or :meth:`~pyhandle.client.dbhandleclient.DBHandleClient.generate_and_register_handle` to create a Handle with a random UUID-based name.

Deleting a Handle
  Use :meth:`~pyhandle.client.dbhandleclient.DBHandleClient.delete_handle`.

Retrieving a full Handle record
  This can be done by :meth:`~pyhandle.client.dbhandleclient.DBHandleClient.retrieve_handle_record`.

Retrieving a single value
  Use :meth:`~pyhandle.client.dbhandleclient.DBHandleClient.get_value_from_handle` to retrieve a single Handle record
  value.

Modifying a Handle record
  Use :meth:`~pyhandle.client.dbhandleclient.DBHandleClient.modify_handle_value` to modify any number of values in a
  specific Handle record. To remove individual values, use :meth:`~pyhandle.client.dbhandleclient.DBHandleClient.delete_handle_value`.

Searching for a Handle
  Use :meth:`~pyhandle.client.dbhandleclient.DBHandleClient.search_handle` to search for Handles with a specific key and
  value. For multiple key-value search use :meth:`~pyhandle.client.dbhandleclient.DBHandleClient.search_handle_multiple_keys`

Registering new Handles (HS_ADMIN)
==================================

An administrator Handle (HS_ADMIN entry) is automatically added to the created Handle.
It contains the name of the admin Handle, the index and the permissions.
These values must be passed as parameters to :meth:`~pyhandle.client.dbhandleclient.DBHandleClient.register_handle`

Example
-------

To create the Handle 123/NEW_HANDLE, which has 123/admin as admin Handle, the following parameters need to be provided:

.. code:: python

   'HS_ADMIN': "{'index': 200, 'handle': '123/admin', 'permissions': '011111110011'}"

Then the method :meth:`~pyhandle.client.dbhandleclient.DBHandleClient.register_handle` is called as follows

.. code:: python

   register_handle(handle, url, admin_handle='123/admin', admin_handle_index=200, permissions='011111110011')

.. note::
 The sequence of the permissions should be respected and is in form: **(create hdl, delete hdl, create derived prefix, delete derived prefix, read val, modify val, del val, add val,
 moodify admin, del, admin, add admin, list)**

Full method documentation
=========================

Constructors
------------

.. automethod:: pyhandle.client.dbhandleclient.DBHandleClient.__init__

Handle record methods
---------------------

.. automethod:: pyhandle.client.dbhandleclient.DBHandleClient.register_handle

.. automethod:: pyhandle.client.dbhandleclient.DBHandleClient.generate_and_register_handle

.. automethod:: pyhandle.client.dbhandleclient.DBHandleClient.delete_handle

.. automethod:: pyhandle.client.dbhandleclient.DBHandleClient.retrieve_handle_record

.. automethod:: pyhandle.client.dbhandleclient.DBHandleClient.get_value_from_handle

.. automethod:: pyhandle.client.dbhandleclient.DBHandleClient.modify_handle_value

.. automethod:: pyhandle.client.dbhandleclient.DBHandleClient.delete_handle_value

.. automethod:: pyhandle.client.dbhandleclient.DBHandleClient.search_handle

.. automethod:: pyhandle.client.dbhandleclient.DBHandleClient.list_all_handles

.. automethod:: pyhandle.client.dbhandleclient.DBHandleClient.search_handle_multiple_keys

Helper methods
--------------

.. automethod:: pyhandle.client.dbhandleclient.DBHandleClient.get_list_of_idx

.. automethod:: pyhandle.client.dbhandleclient.DBHandleClient.connection_status

.. automethod:: pyhandle.client.dbhandleclient.DBHandleClient.create_list_of_queries


Exceptions
==========

.. automodule:: pyhandle.dbhsexceptions
  :members:

