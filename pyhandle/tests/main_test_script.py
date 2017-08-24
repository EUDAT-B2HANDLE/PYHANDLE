from __future__ import print_function, absolute_import

import argparse
import logging
import time
import unittest

from .testcases.clientcredentials_unit_test import PIDClientCredentialsTestCase
from .testcases.handleclient_2_read_patched_unit_test import RESTHandleClientReadaccessPatchedTestCase
from .testcases.handleclient_read_patched_unit_test import RESTHandleClientReadaccessFakedTestCase
from .testcases.handleclient_search_unit_test import RESTHandleClientSearchNoAccessTestCase
from .testcases.handleclient_unit_test import RESTHandleClientNoaccessTestCase
from .testcases.handleclient_write_patched_unit_test import RESTHandleClientWriteaccessPatchedTestCase
from .testcases.handleconnector_patched_unit_test import RESTHandleConnectorAccessPatchedTestCase
from .testcases.handleconnector_unit_test import RESTHandleConnectorNoaccessTestCase
from .testcases.utilconfig_unit_test import UtilConfigTestCase

# Integration tests:
# Imports below!

# Logging:
log_pyhandle = False
if log_pyhandle == True:
    LOGGER = logging.getLogger()
    LOGGER.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler('logs_pyhandle' + time.strftime("%Y-%m-%d_%H-%M") + '.txt', mode='a+')
    file_handler.setFormatter(logging.Formatter('%(levelname)s:%(module)s:%(message)s'))
    LOGGER.addHandler(file_handler)

if __name__ == '__main__':
    desc = 'Test script for pyhandle library, including unit tests and integration ' + \
           'tests. The integration tests need either read access to a handle server ' + \
           'containing some specific test handle record (read), write access to a ' + \
           ' handle server (write) or read access to a search servlet (search).'

    parser = argparse.ArgumentParser(description=desc)

    # Reading test types from args:
    parser.add_argument('testtype', metavar='testtype', nargs='*',
                        help='a test type to run (unit, read, write, and/or search)',
                        default=["unit"], action="store")
    param = parser.parse_args()
    print("Specified test types: " + str(param.testtype))

    write_access = False
    search_access = False
    no_access = False
    mocked_access = False
    read_access = False

    if 'unit' in param.testtype:
        no_access = True
        mocked_access = True
    if 'read' in param.testtype:
        read_access = True
        from .testcases.handleclient_read_integration_test import RESTHandleClientReadaccessTestCase
    if 'write' in param.testtype:
        write_access = True
        import logging
        import time

        REQUESTLOGGER = logging.getLogger('log_all_requests_of_testcases_to_file')
        REQUESTLOGGER.setLevel("INFO")
        REQUESTLOGGER.addHandler(
            logging.FileHandler(
                'logged_http_requests_' + time.strftime("%Y-%m-%d_%H-%M") + '.txt', mode='a+'
            )
        )
        from .testcases.handleclient_write_integration_test import RESTHandleClientWriteaccessTestCase
    if 'search' in param.testtype:
        search_access = True
        from .testcases.handleclient_search_integration_test import RESTHandleClientSearchTestCase


    # Collection tests:
    verbosity = 5
    descriptions = 0

    print('\nCollecting tests:')
    tests_to_run = []
    numtests = 0

    if no_access:
        utilconfig_testcase = unittest.TestLoader().loadTestsFromTestCase(UtilConfigTestCase)
        tests_to_run.append(utilconfig_testcase)
        n = utilconfig_testcase.countTestCases()
        numtests += utilconfig_testcase.countTestCases()
        print('Number of tests for utilconfig (no access required):\t\t\t\t' + str(n))

        noaccess = unittest.TestLoader().loadTestsFromTestCase(RESTHandleClientNoaccessTestCase)
        tests_to_run.append(noaccess)
        n = noaccess.countTestCases()
        numtests += n
        print('Number of tests for client (no access required):\t\t\t\t' + str(n))

        noaccess_connector = unittest.TestLoader().loadTestsFromTestCase(RESTHandleConnectorNoaccessTestCase)
        tests_to_run.append(noaccess_connector)
        n = noaccess_connector.countTestCases()
        numtests += n
        print('Number of tests for handle system connector (no access required):\t\t\t\t' + str(n))

        credentials = unittest.TestLoader().loadTestsFromTestCase(PIDClientCredentialsTestCase)
        tests_to_run.append(credentials)
        n = credentials.countTestCases()
        numtests += n
        print('Number of tests for PIDClientCredentials:\t\t\t\t\t' + str(n))

        search_noaccess = unittest.TestLoader().loadTestsFromTestCase(RESTHandleClientSearchNoAccessTestCase)
        tests_to_run.append(search_noaccess)
        n = search_noaccess.countTestCases()
        numtests += n
        print('Number of tests for searching (without server access):\t\t\t\t' + str(n))

    if mocked_access:
        mocked_read = unittest.TestLoader().loadTestsFromTestCase(RESTHandleClientReadaccessFakedTestCase)
        tests_to_run.append(mocked_read)
        n = mocked_read.countTestCases()
        numtests += n
        print('Number of tests for client (faked read access):\t\t\t\t\t' + str(n))

        patched_read = unittest.TestLoader().loadTestsFromTestCase(RESTHandleClientReadaccessPatchedTestCase)
        tests_to_run.append(patched_read)
        n = patched_read.countTestCases()
        numtests += n
        print('Number of tests for patched read access:\t\t\t\t\t' + str(n))

        patched_write = unittest.TestLoader().loadTestsFromTestCase(RESTHandleClientWriteaccessPatchedTestCase)
        tests_to_run.append(patched_write)
        n = patched_write.countTestCases()
        numtests += n
        print('Number of tests for patched write access:\t\t\t\t\t' + str(n))

        patched_conn = unittest.TestLoader().loadTestsFromTestCase(RESTHandleConnectorAccessPatchedTestCase)
        tests_to_run.append(patched_conn)
        n = patched_conn.countTestCases()
        numtests += n
        print('Number of tests for patched access (connector):\t\t\t\t\t' + str(n))

    if read_access:
        read = unittest.TestLoader().loadTestsFromTestCase(RESTHandleClientReadaccessTestCase)
        tests_to_run.append(read)
        n = read.countTestCases()
        numtests += n
        print('Number of integration tests for client (read access required):\t\t\t' + str(n))

    if write_access:
        write = unittest.TestLoader().loadTestsFromTestCase(RESTHandleClientWriteaccessTestCase)
        tests_to_run.append(write)
        n = write.countTestCases()
        numtests += n
        print('Number of integration tests for client (write access required):\t\t\t' + str(n))

    if search_access:
        search = unittest.TestLoader().loadTestsFromTestCase(RESTHandleClientSearchTestCase)
        tests_to_run.append(search)
        n = search.countTestCases()
        numtests += n
        print('Number of integration tests for searching (search servlet access required):\t' + str(n))


    # Run them
    print('Run ' + str(numtests) + ' tests.')
    test_suites = unittest.TestSuite(tests_to_run)
    print('\nStarting tests:')
    unittest.TextTestRunner(descriptions=descriptions, verbosity=verbosity).run(test_suites)

    # Run with:
    # python main_test_script.py
