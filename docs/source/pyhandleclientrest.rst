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

    from pyhandle.handleclient import PyHandleClient
    client = PyHandleClient('rest').instantiate_...(...)


Then, use the client's methods to read, create and modify handles.

  .. code:: python

    value = client.some_method(...)

Search functionality is not offered by the Handle System. For searching, you need access to a customized search servlet.

Instantiation
=============

When instantiating the REST client there are several constructors with differences in
the permissions and thus possible actions on the Handle server.
Aside from the default constructor :meth:`~pyhandle.client.resthandleclient.RESTHandleClient.__init__`, there are
several shorthand constructors:

:meth:`~pyhandle.client.resthandleclient.RESTHandleClient.instantiate_for_read_access`
  Anonymous read-only access, no credentials needed, no search capabilities. Handles are read from the global Handle Registry.
:meth:`~pyhandle.client.resthandleclient.RESTHandleClient.instantiate_for_read_and_search`
  Read-only access, credentials for search functions required.
:meth:`~pyhandle.client.resthandleclient.RESTHandleClient.instantiate_with_username_and_password`
  Full read and write access, credentials required (username and password).
:meth:`~pyhandle.client.resthandleclient.RESTHandleClient.instantiate_with_credentials`
  Full read and write access, credentials required (username and password or client certificates). Credentials can
  conveniently be loaded from a JSON file. For this, please see documentation of :mod:`~pyhandle.clientcredentials`.

On top of the required arguments, more arguments can be passed to the constructors as key-value pairs. Please see the documentation of
the default constructor to find out which values are understood.

Instantiation can be performed when specifying the client as follows:

.. code:: python

   from pyhandle.handleclient import PyHandleClient
   client = PyHandleClient('rest').instantiate_...()

.. note::

   The instantiation methods mentioned above concern only the REST client. Concerning the DB client there is for now no
   restriction for creating or modifying Handles in the database.

Authentication
==============

For creating and modifying handles* you need to authenticate at the Handle Server you'd like to write to. Authentication using pyhandle is straightforward. There are two possibilities:

* Authenticating using username and password
* Authenticating using client certificates

.. important:: Here we assume that you know your username and password or have your private key file and your certificate file ready. If you need to set these up, please see :doc:`authentication`.

Authentication using client certificates
----------------------------------------

Using client certificates, you need to provide paths to the file containing your private key and to the certificate in a JSON file. The class :class:`~pyhandle.cliencredentials.PIDClientCredentials` provides a method :meth:`~pyhandle.cliencredentials.PIDClientCredentials.load_from_JSON`. This can be read as follows:

  .. code:: python

    from pyhandle.clientcredentials import PIDClientCredentials
    cred = PIDClientCredentials.load_from_JSON('my_credentials.json')
    client = PyHandleClient('rest').instantiate_with_credentials(cred)

The JSON file should look like this:

  .. code:: json

    {
      "client":"rest",
      "handle_server_url": "https://my.handle.server",
      "private_key": "my_private_key.pem",
      "certificate_only": "my_certificate.pem"
    }

Authentication using username and password
------------------------------------------

If you have a username (something that looks like **300:foo/bar**) and a password, we recommend using this constructor: :meth:`~pyhandle.handleclient.RESTHandleClient.instantiate_with_username_and_password`:

  .. code:: python

    client = PyHandleClient('rest').instantiate_with_username_and_password(
      'https://my.handle.server',
      '300:foo/bar',
      'mypassword123'
    )

Alternatively, you can store your username and password in a JSON file, instead of paths to certificate and key::
  {
  "baseuri": "https://my.handle.server",
  "username": "300:foo/bar",
  "password": "mypassword123"
  }

Like above, you can read the JSON like as shown above:

  .. code:: python

    cred = PIDClientCredentials.load_from_JSON('my_credentials.json')
    client = PyHandleClient('rest').instantiate_with_credentials(cred)


Credentials JSON file
---------------------

The JSON file can contain more information. All items it contains are passed to the client constructor as config. Please see :meth:`~pyhandle.handleclient.RESTHandleClient.__init__` to find out which configuration items the client constructor understands.



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

