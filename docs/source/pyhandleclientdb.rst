================
DB Handle Client
================

The DB Handle client provides methods to create, update and delete Handles directly via the (SQL) database of the
Handle System server.

.. note::
   The current version of the library supports MySQL database.

.. important::
   For the Db client there is no read-only mode. All operations require authentication.

Instantiation
=============

As described in the :doc:`pyhandleclient`, credentials and information about the database server are required in
order to
instantiate the DB client.

.. code:: python

   client = PyHandleClient('db', credentials)

The credentials can loaded from a file or passed as a dictionary to the PyHandleClient

.. code:: python

   credentials = {'db_host':'', 'db_user':'', 'db_pass':'', 'db_name':''}

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
  This can be done either through :meth:`~pyhandle.client.dbhandleclient.DBHandleClient.retrieve_handle_record`.

Retrieving a single value
  Use :meth:`~pyhandle.client.dbhandleclient.DBHandleClient.get_value_from_handle` to retrieve a single Handle record
  value.

Modifying a Handle record
  Use :meth:`~pyhandle.client.dbhandleclient.DBHandleClient.modify_handle_value` to modify any number of values in a
  specific Handle record. To remove individual values, use :meth:`~pyhandle.client.dbhandleclient.DBHandleClient.delete_handle_value`.

Searching for a Handle
  Use :meth:`~pyhandle.client.dbhandleclient.DBHandleClient.search_handle` to search for Handles with a specific key and
  value.
  Please note that searching requires access to a search servlet whose access information, if it differs from the handle server,
  has to be specified at client instantiation.


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

Helper methods
--------------

.. automethod:: pyhandle.client.dbhandleclient.DBHandleClient.get_list_of_idx

.. automethod:: pyhandle.client.dbhandleclient.DBHandleClient.connection_status

.. automethod:: pyhandle.client.dbhandleclient.DBHandleClient.create_list_of_queries


Exceptions
==========

.. automodule:: pyhandle.dbhsexceptions
  :members:

