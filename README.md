# PYHANDLE

PyHandle is a Python client library for interaction with a [Handle System](https://handle.net) server, providing basic create, read, update and delete capabilities for Handles. The library offers a client for the HTTP REST interface. It also includes a client that interacts directly with a Handle server SQL back-end and a client that creates customized Batch files (containing Batch operations that can be performed using the GenericBatch command utility provided by the Handle System), but those two are no longer maintained.

PyHandle currently supports Python >=3.5 (tested up to 3.10), and requires at least a Handle System server 9. The library requires OpenSSL v1.0.1 or higher. Python 2.7 and 3.10 are supported. 

PyHandle is based on a prior development of the [EUDAT project](https://eudat.eu) under the name B2Handle.
As [B2Handle](https://github.com/EUDAT-B2SAFE/B2HANDLE) was developed with a specific scope - Handle operations in the EUDAT project - in mind, it has been improved and made more generic to cater to a broader audience.

We advice you to use PyHandle isteard of B2HADNLE. 


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

For more information on the methods offered by the library, please consult the [technical documentation](http://eudat-b2handle.github.io/PYHANDLE/).

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


# Link to documentation

Check out the technical documentation [here](https://eudat-b2handle.github.io/PYHANDLE/).

Check out the overall documentation [here](https://eudat-b2handle.github.io/).


# License

Copyright 2015-2022, Deutsches Klimarechenzentrum GmbH, GRNET S.A., SURFsara

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



