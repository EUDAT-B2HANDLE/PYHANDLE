==================
REST Handle Client
==================

.. note:: The REST client documentation is based mainly on the `B2Handle <http://eudat-b2safe.github.io/B2HANDLE/index.html>`_ documentation.
          Here we describe only the main functionalities of the REST client.

.. important:: If you encounter security warnings when using the library, contact your Handle server administrators and ask them to set up the server certificates correctly! (see :doc:`handleserverconfig`)

The RESTHandleClient class provides a Python-level interface for interactions with a Handle server through its native REST interface. The class provides common methods for working with Handles and their records:

* Create and modify Handles
* Search across Handles (using an additional servlet)
..  Manage multiple URLs through special 10320/loc entries


General usage
=============

First, you create an instance of the client. It holds all necessary information, such as from which handle server to read, which
user credentials to use etc. Several different instantiation methods are available for different usages (see
:doc:`pyhandleclient`).

  .. code:: python

    client = PyHandleClient('rest').instantiate_...(...)


Then, use the client's methods to read, create and modify handles.

  .. code:: python

    value = client.some_method(...)

Search functionality is not offered by the Handle System. For searching, you need access to a customized search servlet.



Basic Handle interaction
========================

Creating a Handle
  Use :meth:`~pyhandle.handleclient.RESTHandleClient.register_handle` to create a Handle with a custom name or :meth:`~pyhandle.handleclient.RESTHandleClient.generate_and_register_handle` to create a Handle with a random UUID-based name.

Deleting a Handle
  Use :meth:`~pyhandle.handleclient.RESTHandleClient.delete_handle`.

Retrieving a full Handle record
  This can be done either through :meth:`~pyhandle.handleclient.RESTHandleClient.retrieve_handle_record` or :meth:`~pyhandle.handleclient.RESTHandleClient.retrieve_handle_record_json`.

Retrieving a single value
  Use :meth:`~pyhandle.handleclient.RESTHandleClient.get_value_from_handle` to retrieve a single Handle record value.

Modifying a Handle record
  Use :meth:`~pyhandle.handleclient.RESTHandleClient.modify_handle_value` to modify any number of values in a specific Handle record. To remove individual values, use :meth:`~pyhandle.handleclient.RESTHandleClient.delete_handle_value`.

Searching for a Handle
  Use :meth:`~pyhandle.handleclient.RESTHandleClient.search_handle` to search for Handles with a specific key and value.
  Please note that searching requires access to a search servlet whose access information, if it differs from the handle server,
  has to be specified at client instantiation.




Full method documentation
=========================

Constructors
------------

.. automethod:: pyhandle.handleclient.RESTHandleClient.__init__

.. automethod:: pyhandle.handleclient.RESTHandleClient.instantiate_for_read_access

.. automethod:: pyhandle.handleclient.RESTHandleClient.instantiate_for_read_and_search

.. automethod:: pyhandle.handleclient.RESTHandleClient.instantiate_with_username_and_password

.. automethod:: pyhandle.handleclient.RESTHandleClient.instantiate_with_credentials

Handle record methods
---------------------

.. automethod:: pyhandle.handleclient.RESTHandleClient.register_handle

.. automethod:: pyhandle.handleclient.RESTHandleClient.generate_and_register_handle

.. automethod:: pyhandle.handleclient.RESTHandleClient.delete_handle

.. automethod:: pyhandle.handleclient.RESTHandleClient.retrieve_handle_record

.. automethod:: pyhandle.handleclient.RESTHandleClient.retrieve_handle_record_json

.. automethod:: pyhandle.handleclient.RESTHandleClient.get_value_from_handle

.. automethod:: pyhandle.handleclient.RESTHandleClient.modify_handle_value

.. automethod:: pyhandle.handleclient.RESTHandleClient.delete_handle_value

.. automethod:: pyhandle.handleclient.RESTHandleClient.search_handle



Helper methods
--------------

.. automethod:: pyhandle.handleclient.RESTHandleClient.generate_PID_name
.. automethod:: pyhandle.handleclient.RESTHandleClient.get_handlerecord_indices_for_key


Utilities
==========

.. automodule:: pyhandle.utilhandle
  :members:


Client credentials
==================

.. automodule:: pyhandle.clientcredentials

.. automethod:: pyhandle.clientcredentials.PIDClientCredentials.load_from_JSON
.. automethod:: pyhandle.clientcredentials.PIDClientCredentials.__init__



Exceptions
==========

.. automodule:: pyhandle.handleexceptions
  :members:

