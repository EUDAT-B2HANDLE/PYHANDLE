# PYHANDLE

PyHandle is a Python client library for interaction with a [Handle System](https://handle.net) server, providing basic create, read, update and delete capabilities for Handles. The library offers a client for the HTTP REST interface, a client that interacts directly with a Handle server SQL back-end and a client that creates customized Batch files.
The latter contain Batch operations, that can be performed using the GenericBatch command utility provided by the Handle System.

PyHandle currently supports Python 2.6, 2.7 and 3.5, and requires at least a Handle System server 8.1. The library requires OpenSSL v1.0.1 or higher. 

PyHandle is based on a prior development of the [EUDAT project](https://eudat.eu) under the name B2Handle.
As [B2Handle](https://github.com/EUDAT-B2SAFE/B2HANDLE) was developed with a specific scope - Handle operations in the EUDAT project - in mind, it has been improved and made more generic to cater to a broader audience.



# Installation

You can install the PyHandle library as follows:
 1. git clone https://github.com/EUDAT-B2SAFE/PYHANDLE.git
 1. cd PYHANDLE/
 1. python setup.py install
 
The library is also available on PyPi and can be installed via pip:

```bash
 pip install pyhandle
```

# Building the documentation

For more details about the library you can build the documention using [Sphinx](http://www.sphinx-doc.org), requiring at least version 1.3. Sphinx and can be installed via pip. To build HTML documentation locally, then run:

```bash
python setup.py build_sphinx
```

# License

Copyright 2015-2017, Deutsches Klimarechenzentrum GmbH, GRNET S.A., SURFsara

   The PYHANDLE library is licensed under the Apache License,
   Version 2.0 (the "License"); you may not use this product except in 
   compliance with the License.
   You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.






