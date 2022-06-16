===================
BATCH Handle Client
===================

The Batch Handle client provides methods to create, update and delete Handles by creating customized batch files.
Batch files contain handle operations that can be submitted using the *GenericBatch* command line utility, which can be invoked using the following command:

 `bin/hdl-genericbatch <batchfile> [<LogFile>] [-verbose]`

.. note::
   The batch facilities are included with the Handle.net software distribution.

.. important::
   All batch operations require authentication to the Handle server. *Users* can authenticate by *SECKEY* or *PUBKEY* (see `Authententicating to Handle server`_)

Basic Handle interaction
========================

Creating a Handle
  Use :meth:`~pyhandle.client.batchhandleclient.BatchHandleClient.register_handle_batch` to create a Handle with a custom name

Deleting a Handle
  Use :meth:`~pyhandle.client.batchhandleclient.BatchHandleClient.delete_handle` to delete a Handle and its records.

Modifying a Handle
  Use :meth:`~pyhandle.client.batchhandleclient.BatchHandleClient.modify_handle_value` to modify a Handle value.

Adding a Handle value
  Use :meth:`~pyhandle.client.batchhandleclient.BatchHandleClient.add_handle_value` to add a new value to the existing Handle.

Instantiation
=============

The Batch client is instantiated as follows:

.. code:: python

   from pyhandle.handleclient import PyHandleClient
   client = PyHandleClient('batch')

If no additional parameters are passed to *PyHandleClient*, a default path for the batch file will be set */<homedirectory>/handle_batch*.
In order to specify your own path add it as parameter:

.. code:: python

   batch_file_path = '/abs/path'
   client = PyHandleClient('batch', batch_file_path)

Instantiation only selects the Handle client and set the path of the batch file. The latter is created by the method :meth:`~pyhandle.client.batchhandlient.BatchHandleClient.create_batch_file`.

.. important::
   The absolute path should be given: /abc/xyz/batch_file_name. This path will be used for all operations that come after the instantiation.


Creating batch files
====================

The next step after the instantiation is to create an empty batch file, which contains all the batch operations.
The latter are *appended* to the created file. To create a batch file use the following code:

.. code:: python

   client.create_batch_file()

This method takes the path specified during the instantiation and checks if the file exists.
If *overwrite* is set to True the batch file is overwritten, otherwise an exception is thrown.

.. code:: python

  client.create_batch_file(overwrite=True)

Default of overwrite is False.

Batch operations
================

The following operations are written on the batch file. For the execution see `Executing the batch file`_



Authententicating to Handle server
----------------------------------

In order to administer Handles, you must have administrative rights.
First line is the operation name: 'AUTHENTICATE'.
There are two possibilities to authenticate to Handle server:

* By SECKEY (:meth:`~pyhandle.client.batchhandleclient.BatchHandleClient.authenticate_seckey`): Users must provide {username}:{password} as parameters.
  The *username* is the usual Handle identity {index}:{handle}.

First line:

.. code:: bash

   AUTHENTICATE SECKEY:admin_index:admin_handle.

Second line:

.. code:: bash

  password

* By PUBKEY (:meth:`~pyhandle.client.batchhandleclient.BatchHandleClient.authenticate_pubkey`): Users must provide a private key.

First line:

.. code:: bash

   AUTHENTICATE PUBKEY: admin_index:admin_handle.

Second line: if your private key was created and encrypted by passphrase, then:

.. code:: bash

         private_key_file_path + '|' + passphrase

otherwise

.. code:: bash

   private_key_file_path

Example of authentication with user name and password:

.. code:: python

  username = 'index:prefix/suffix'
  password = 'passoword'
  client.authenticate_seckey(username, password)

* From a credential file: it is also possible to set authentication credentials from a json file. By using the method :meth:`~pyhandle.client.batchhandleclient.BatchHandleClient.authenticate_with_credentials`

Example:

.. code:: python

    from pyhandle.clientcredentials import PIDClientCredentials
    cred = PIDClientCredentials.load_from_JSON('my_credentials.json')
    client.authenticate_with_credentials(cred, auth_type='seckey')

This will call the method :meth:`~pyhandle.client.batchhandleclient.BatchHandleClient.authenticate_seckey`

The JSON file should look like this:

  .. code:: json

    {
      "client":"batch",
      "username": "username",
      "password": "password",
      "private_key": "path/to/private_key",
      "passphrase": "passphrase"
    }

This json file contains all mandatory and optional arguments. Depending on the authentication type, the required arguments should be added to json file.

.. important::
   When the private key is encrypted, the 'passphrase' must be added to json file.


Registering new Handles
-----------------------

In order to create a new Handle, the method :meth:`~pyhandle.client.batchhandleclient.BatchHandleClient.register_handle_batch`  is used with the the following parameters:

* handle: The full name of the handle to be registered (prefix and suffix)

* location: The URL of the data entity to be referenced

* hdl_admin_index: Unique index number. This concerns the administrator of the Handle not the Handle itself.

* admin_handle: The name of the administrator of the Handle

* perm: Permissions of the *admin_handle*

.. code:: python

   url = 'wwww.example.com'

   user = '300:123/abc'

   pw = 'password'

   handle = '123/xyz'

   hdl_admin_index = 300

   admin_handle = '123/admin'

   perm = '110011111110'

   client.register_handle_batch(handle, url, hdl_admin_index, admin_handle, perm)

.. note::

   The order of permissions MUST be respected and has the following sequence: (add handle, delete handle, no add naming authority, no delete naming authority, modify values, remove values, add values, read values, modify administrator, remove administrator, add administrator, list handles)

Deleting a Handle
-----------------

For deleting Handles, only the name of the Handle is required. The operation name is *DELETE*
These line will be written:

DELETE + space + handle_name

.. code:: python

   DELETE 123/abc

Modifying a Handle value
------------------------

To modify a Handle value, there must be a Handle value line to define the administrator of the handle.
Each Handle value line must start with a unique index number, followed by the handle value type, ttl, the permission set (admin read, admin write, public read, public write and the value data)
Permissions, ttl and encoding are set automatically, teh other parameters must be provided by the users (as key-value).

To modify more then a value, simply execute the method with different parameters. The modify operation will be appended to the file.

Example:
........

.. code:: python

   client.modify_handle_value(handle= '123/abc', index= 1, type= 'URL', data= 'www.example.com')

This changes the value of type 'URL', which has index 1 corresponding to Handle '123/abc'.

Adding Handle values
--------------------

Use the method :meth:`~pyhandle.client.batchhandleclient.BatchHandleClient.add_handle_value` to add a new value to existing Handle.
The first line is ADD + space + handle_name.

The next lines are Handle values lines. There must be a handle value line to define the administrator of the handle. Each handle value line must start with an index followed by the handle value type, ttl, permissions and the value data.
The method can be executed several times with different values to add more Handle values.

Example:
........

.. code:: python

   handle = '123/abc'
   client.add_handle_value(handle, index=1, type='URL', data='www.example.com')

Adds a value of type 'URL' at index 1 to Handle '123/abc'

Deleting Handle values
----------------------

With the method :meth:`~pyhandle.client.batchhandleclient.BatchHandleClient.delete_handle_value` it is possible to delete one or more Handle values from an existing Handle.
Required are: The Handle name and the indexes as a list.

Example:
........

.. code:: python

   handle = '123/abc'
   indexes = [1, 2]
   client.delete_handle_value(handle, indexes)

This deletes Handle values at the index 2 and 3 of Handle '123/abc'.

Executing the batch file
------------------------

After finishing writing batch operations, the *GenericBatch* command utility is used to perform the operations.

.. code:: bash

   bin/hdl-genericbatch <batchfile> [<LogFile>] [-verbose]

Full method documentation
=========================

Constructors
------------

.. automethod:: pyhandle.client.batchhandleclient.BatchHandleClient.__init__


Batch file methods
==================

.. automethod:: pyhandle.client.batchhandleclient.BatchHandleClient.create_batch_file
.. automethod:: pyhandle.client.batchhandleclient.BatchHandleClient.register_handle_batch
.. automethod:: pyhandle.client.batchhandleclient.BatchHandleClient.delete_handle
.. automethod:: pyhandle.client.batchhandleclient.BatchHandleClient.modify_handle_value
.. automethod:: pyhandle.client.batchhandleclient.BatchHandleClient.add_handle_value
.. automethod:: pyhandle.client.batchhandleclient.BatchHandleClient.delete_handle_value
.. automethod:: pyhandle.client.batchhandleclient.BatchHandleClient.authenticate_seckey
.. automethod:: pyhandle.client.batchhandleclient.BatchHandleClient.authenticate_pubkey
.. automethod:: pyhandle.client.batchhandleclient.BatchHandleClient.authenticate_with_credentials

Helper methods
==============

.. automethod:: pyhandle.client.batchhandleclient.BatchHandleClient.get_all_args
.. automethod:: pyhandle.client.batchhandleclient.BatchHandleClient.get_batch_file_path
.. automethod:: pyhandle.client.batchhandleclient.BatchHandleClient.check_if_file_exists


Exceptions
==========

.. automodule:: pyhandle.batchhsexceptions
  :members:



