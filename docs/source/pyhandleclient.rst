==============
PyHandleClient
==============


PyHandleClient is the main class of the PyHandle library and provides methods to:

 * select a client (REST or DB)
 * authenticate to the Handle System server
 * invoke methods to create, retrieve, update and delete Handles

Select a client
===============

PyHandleClient acts as a factory that takes arguments to determine what type of client to instantiate.
There are two interfaces to interact with the Handle System server: REST and DB.
User selects the client by passing the client as String to the PyHandleClient class

.. code:: python

   from pyhandle.handleclient import PyHandleClient

and then:

* REST

.. code:: python

   client = PyHandleClient('rest')

* DB

  .. code:: python

   client = PyHandleClient('db', credentials)

The *credentials* parameter is not required when creating a REST client. It has instantiation methods that are
presented in `Instantiation`_
The credentials are mandatory when creating a DB client. In that case, information about the database have to be
passed to the client (see :doc:`pyhandleclientdb`).


Instantiation
=============

When creating a REST client instance there are several constructors with differences in
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

    cred = PIDClientCredentials.load_from_JSON('my_credentials.json')
    client = PyHandleClient('rest').instantiate_with_credentials(cred)

The JSON file should look like this:

  .. code:: json

    {
      "baseuri": "https://my.handle.server",
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


Full method documentation
=========================

Constructors
------------

.. automethod:: pyhandle.client.resthandleclient.RESTHandleClient.__init__

.. automethod:: pyhandle.client.resthandleclient.RESTHandleClient.instantiate_for_read_access

.. automethod:: pyhandle.client.resthandleclient.RESTHandleClient.instantiate_for_read_and_search

.. automethod:: pyhandle.client.resthandleclient.RESTHandleClient.instantiate_with_username_and_password

.. automethod:: pyhandle.client.resthandleclient.RESTHandleClient.instantiate_with_credentials

