# PYHANDLE
PyHandle is a python library for interaction with HANDLE system. 

PyHandle was first developed in the [EUDAT project](https://eudat.eu) under the name B2Handle.
As [B2Handle](https://github.com/EUDAT-B2SAFE/B2HANDLE) was developed with a specific scope - Handle operations in the EUDAT project - in mind, it has been improved and made more generic to cater to a broader audience.
PyHandle will soon be available on PyPi.


# Installation

You can install the PyHandle library as follows:
 1. host$ git clone https://github.com/EUDAT-B2SAFE/PYHANDLE.git 
 1. host$ cd PYHANDLE/
 1. host$ python setup.py install
 
As soon as the library is available on PyPi, you can install it via pip:
* host$ pip install _pyhandle_
 
# Basic Usage

## Using the REST interface

1. from pyhandle.handleclient import 
1. client = HandleClientFactory('rest')
1. handle = 'prefix/suffix'
1. record = client.retrieve_handle_record(handle)

## Using the DB interface (MySQL)

1. from pyhandle.handleclient import HandleClientFactory
1. credentials = {'db_host':'xxx', 'db_user':'xxx', 'db_pass':'xxx', 'db_name':'xxx'}
1. client = HandleClientFactory('db', credentials)
1. handle = 'prefix/suffix'
1. record = client.retrieve_handle_record(handle)

# Full Documentation (REST)

See the [technical documentation](http://eudat-b2safe.github.io/B2HANDLE/) for more information on the features provided by the library.

# License

Copyright 2015-2017, Deutsches Klimarechenzentrum GmbH, GRNET S.A., SURFsara

   The PyHandle library is licensed under the Apache License,
   Version 2.0 (the "License"); you may not use this product except in 
   compliance with the License.
   You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.







