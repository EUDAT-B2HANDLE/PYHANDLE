# PyHandle Testing

## Testing with plain unittest/unittest2

Simply run:

```bash
python setup.py test
```

## Testing with nose and/or coverage

If you have installed the PyHandle module running `python setup.py install`, [nose](https://pypi.python.org/pypi/nose/) should already be available. Otherwise you can install it using your distribution's package manager or `pip` (recommended) as follows:

    pip install nose

Then run:

    nosetests --with-xunit --xunit-testsuite-name=pyhandle --with-coverage --cover-erase --cover-package=pyhandle --cover-branches --cover-inclusive --cover-xml main_test_script.py

The above will generate test results in the standard XUnit XML format and also provide an XML-formatted coverage report using Ned Batchelder's [Coverage.py](https://pypi.python.org/pypi/coverage). The latter can be installed using `pip` (recommended) as follows:

    pip install coverage

To generate test coverage reports without `nose`, run:

    coverage erase
    coverage run --branch -m pyhandle.tests.main_test_script
    coverage xml -i

Alternatively you may run tests with nose and generate coverage reports as follows:

    python setup.py test

To configure the nosetests command see also nosetests section in setup.cfg.

