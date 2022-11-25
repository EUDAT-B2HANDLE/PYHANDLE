# Instructions on uploading pyhandle releases to pypi

(Merret, 2022-07-21)

## Preparations:

1. Install twine: `pip install twine`
2. Create a pypirc file in your home dir: `vi ~/.pypirc` (see example below)
3. Login to pypi / test-pypi and create an API key to use for authentication,
  add that API key to the .pypirc file.


## To upload a release:

1. Make sure you are on master and master is up to date.

2. Go to the directory where the `setup.py` file is located.

3. Remove the previous builds: `rm dist/pyhandle-x.y.z.tar.gz`

4. Build the next build: `python setup.py sdist`

5. Check with twine: `twine check dist/*`

6. Upload with twine: `twine upload --repository pypi dist/*`


## Example .pypirc file:

```
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-Jhdsfjksdfk... (api key)

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-KsdkfKJHksjdhfkjsdf... (api key)

```
