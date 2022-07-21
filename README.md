# PYHANDLE

PyHandle is a Python client library for interaction with a [Handle System](https://handle.net) server, providing basic create, read, update and delete capabilities for Handles. The library offers a client for the HTTP REST interface. It also includes a client that interacts directly with a Handle server SQL back-end and a client that creates customized Batch files (containing Batch operations that can be performed using the GenericBatch command utility provided by the Handle System), but those two are no longer maintained.

PyHandle currently supports Python >=3.5 (tested up to 3.8), and requires at least a Handle System server 8.1. The library requires OpenSSL v1.0.1 or higher. Python 2.7 and 3.5 used to be supported, but now the PyMysql dependencies fails (02/2021).

PyHandle is based on a prior development of the [EUDAT project](https://eudat.eu) under the name B2Handle.
As [B2Handle](https://github.com/EUDAT-B2SAFE/B2HANDLE) was developed with a specific scope - Handle operations in the EUDAT project - in mind, it has been improved and made more generic to cater to a broader audience.




# Installation

You can install the PyHandle library as follows:

```bash
git clone https://github.com/EUDAT-B2SAFE/PYHANDLE.git
cd PYHANDLE/
python setup.py install
```
 
The library is also available on PyPi and can be installed via pip:

```bash
 pip install pyhandle
```

For more information on the methods offered by the library, please consult the [technical documentation](http://eudat-b2safe.github.io/PYHANDLE/).

## Instantiate:

One of the core steps is to instantiate the file with the needed credentials. 
A guide on how to use them is the following: 

```
credentials_file = './credentials/creds.json'
# Path must be relative to current working dir
# JSON file must contain absolute paths, or paths relative to the creds.json file!!
creds = pyhandle.clientcredentials.PIDClientCredentials.load_from_JSON(credentials_file)
client = pyhandle.handleclient.PyHandleClient('rest').instantiate_with_credentials(
        creds, HTTPS_verify=https_verify)
```

# Building the documentation

For more details about the library you can build the documention using [Sphinx](http://www.sphinx-doc.org), requiring at least version 1.3. Sphinx and can be installed via pip. To build HTML documentation locally, then run:

```bash
python setup.py build_sphinx
```


# Link to documentation


Check out the documentation [here](https://eudat-b2safe.github.io/PYHANDLE/).

(You can find the source in the GitHub repository at [/docs/source/index.rst](./docs/source/index.rst)!)

# License

Copyright 2015-2021, Deutsches Klimarechenzentrum GmbH, GRNET S.A., SURFsara

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


# Some usage notes

(to be migrated to documentation)


* `register_handle_kv(handle, **kv-pairs)` allows to pass (additionally to the handle name) key-value pairs.

* `register_handle_json(handle, list_of_entries, ...)` allow to pass JSON snippets instead of key-value pairs, so you can specify the indices. An entry looks like this: `{'index':index, 'type':entrytype, 'data':data}`. This is the format in which the changes are communicated to the handle server via its REST interface. An entry of type `HS_ADMIN` will be added if you do not provide one.

* `register_handle(...)` allows to pass (additionally to the handle name) a mandatory URL, and optionally a CHECKSUM, and more types as key-value pairs. Old method, made for legacy reasons, as this library was created to replace an earlier library that had a method with specifically this signature.

* `generate_and_register_handle(prefix, ...)` is a similar legacy method. Instead, just use `generate_PID_name(prefix)` to create a handle name and use one of the above. 


# How to run the unit tests

The simplest way (tested with python 3.7.1):

```bash
python setup.py test
```

(More info in the GitHub repository at [./pyhandle/tests/README.md](./pyhandle/tests/README.md)!)

To quickly test different versions using docker (see [./pyhandle/tests/testdockers](./pyhandle/tests/testdockers)):

```
today=`date +%m%d%Y`
version="1.x.x" # pyhandle version, e.g. 1.0.4

docker build -t temp_pyhandle:36_$version_$today -f pyhandle/tests/testdockers/Dockerfile36 . 
docker run  -it temp_pyhandle:36_$version_$today python setup.py test

docker build -t temp_pyhandle:37_$version_$today -f pyhandle/tests/testdockers/Dockerfile37 . 
docker run  -it temp_pyhandle:37_$version_$today python setup.py test

docker build -t temp_pyhandle:38_$version_$today -f pyhandle/tests/testdockers/Dockerfile38 . 
docker run  -it temp_pyhandle:38_$version_$today python setup.py test
```

There are also Dockerfiles in [./pyhandle/tests/testdockers](./pyhandle/tests/testdockers), but they are not documented and fail.

# TODO Fix these Dockerfiles eventually, or update to functioning versions.

```
# build successful, but fails to run:
docker build -t eudat-pyhandle:py3.5 -f Dockerfile-py3.5 .
cd ./pyhandle/tests
docker build -t temp:temp -f Dockerfile-py3.5 .
docker run -it temp:temp

# build fails:
docker build -t eudat-pyhandle:py2.6 -f Dockerfile-python2.6 .



# Github contributions

Devs:

* Please make contributions based on the devel branch, then issue a PR to the devel branch.
* Small contributions (e.g. typos, README, ...) can be pushed directly to devel if you have permissions.

Owners:

* Run unit tests on PR
* Merged PR into devel
* If/when changes are ready for a next release, bump the version number (no PR, but push directly to the repo)
* Run unit tests again on this devel branch.
* Merge devel into master (no PR, directly merge them **with --no-ff to keep history** and push to master)
* Add "-dev" to the incremented version number on devel
* Send release to pypi: 

```
virtualenv venv 
source venv/bin/activate
pip install pypandoc
python setup.py sdist upload -r pypi


# TODO: Deprecated, move to twine!
```


