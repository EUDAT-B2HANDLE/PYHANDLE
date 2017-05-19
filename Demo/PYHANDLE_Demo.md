# PID Demonstration

In this training we are going to use the PyHandle pre-release.
The library offers methods to create, update and delete Handles as well as advanced functionality such as searching over Handles using an additional search servlet and managing multiple location entries per Handle.

## Setup
ipython


## Import

First, we have to import the PyHandle library. 
The library is used by creating a client object and using its methods to interact with the Global Handle System.


```py
from pyhandle.handleclient import PyHandleClient
```

## Resolving Handles
It is easy to resolve a handle and read its handle record using the Pyhandle library. For this, we instantiate the client in read-mode and use its reading methods.

### Instantiation of the client

```py
client = PyHandleClient('rest').instantiate_for_read_access()
```

Now we can use its various reading methods, for example get_value_from_handle(handle) or retrieve_handle_record(handle).

For example, retrieve_handle_record(handle) returns a dictionary of the record's entries:

```py
handle = '21.T14998/TESTHANDLE'
record = client.retrieve_handle_record(handle)
print(record)
```
{'URL': 'http://example.com/', 'HS_ADMIN': "{'index': 200, 'permissions': '011111110011', 'handle': '21.T14998/USER1'}"}


We can access individual values using:

```py 
value1 = client.get_value_from_handle(handle, 'URL')
value2 = client.get_value_from_handle(handle, 'CREATION_DATE')
print(value1)
print(value2)
```

## Creating Handle records

For modifying/creating handle records, we first need to authenticate. In this tutorial, we will use a username and a password. (There is other methods, e.g. using client certificates.)

```py
user = '300:21.T14998/USER_TRAINING'
password = 'K_rTb39UsG+M'
handle_server_url = 'https://handle.dkrz.de:8004'
```

Now we create a client that has write access to the server.

```py
client.instantiate_with_username_and _password(handle_server_url, user, password, HTTPS_verify=False)
```

In their most simple form, PIDs are simple redirection to a URL. In this case, all they have is an entry that stores the URL. You can simply create such a handle using the method register_handle():

```py 
prefix = '21.T14998'
newhandle = prefix+'/myhandle'
url = 'www.dkrz.de'
client.register_handle(newhandle, url)
```

We can check the contents of this newly created handle record:

```py 
record = client.retrieve_handle(newhandle)
```

## Updating Handle records

After the creation of the client with write access we can try to modify a Handle record value:

### Modifying Handle records

```py 
client.modify_handle_value(handle, CREATION_DATE='2017-05-20'
```

To verify if it works:

```py 
print(client.get_value_from_handle(handle, 'CREATION_DATE'))
```

### Adding new values
With the same method, we can add new values to a handle record:

```py 
client.modify_handle_value(handle, ADDED_VALUE='added value')
print(client.retrieve_handle_record(handle))
```

### Deleting values

In case we wrote a wrong entry or we simply want to delete a value from the Handle record, the delete_handle_value() 
method allows to delete that entry:

```py 
client.delete_handle_value(handle, 'CREATION_DATE')
```

```py 
print client.get_value_from_handle(handle, 'CREATION_DATE')
```

None