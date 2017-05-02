"""Testing methods that normally need Handle server read access,
by providing a handle record to replace read access."""

import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

import json
import pyhandle
from pyhandle.client.resthandleclient import RESTHandleClient
from pyhandle.utilhandle import check_handle_syntax
from past.builtins import long
# Load some data that is needed for testing
PATH_RES = pyhandle.util.get_neighbour_directory(__file__, 'resources')
RECORD = json.load(open(PATH_RES+'/handlerecord_for_reading_PUBLIC.json'))
RECORD_WITH = json.load(open(PATH_RES+'/handlerecord_with_10320LOC_PUBLIC.json'))
RECORD_WITHOUT = json.load(open(PATH_RES+'/handlerecord_without_10320LOC_PUBLIC.json'))
RECORD_WITH_EMPTY = json.load(open(PATH_RES+'/handlerecord_with_empty_10320LOC_PUBLIC.json'))

class RESTHandleClientReadaccessFakedTestCase(unittest.TestCase):
    '''Testing methods for retrieving values and indices.'''

    def setUp(self):
        self.inst = RESTHandleClient()

    def tearDown(self):
        pass

    # get_value_from_handle

    def test_get_value_from_handle_normal(self):
        """Test retrieving a specific value from a handle record."""

        handlerecord = RECORD
        handle = RECORD['handle']

        val = self.inst.get_value_from_handle(handle,
                                              'TEST1',
                                              handlerecord)
        self.assertEquals(val, 'val1',
            'The value of "TEST1" should be "val1".')

    def test_get_value_from_handle_inexistentvalue(self):
        """Test retrieving an inexistent value from a handle record."""

        handlerecord = RECORD
        handle = handlerecord['handle']

        val = self.inst.get_value_from_handle(handle,
                                              'TEST100',
                                              handlerecord)
        self.assertIsNone(val,
            'The value of "TEST100" should be None.')

    def test_get_value_from_handle_HS_ADMIN(self):
        """Test retrieving an HS_ADMIN value from a handle record."""

        handlerecord = RECORD
        handle = handlerecord['handle']

        val = self.inst.get_value_from_handle(handle,
                                              'HS_ADMIN',
                                              handlerecord)
        self.assertIn('handle', val,
            'The HS_ADMIN has no entry "handle".')
        self.assertIn('index', val,
            'The HS_ADMIN has no entry "index".')
        self.assertIn('permissions', val,
            'The HS_ADMIN has no entry "permissions".')
        syntax_ok = check_handle_syntax(val['handle'])
        self.assertTrue(syntax_ok,
            'The handle in HS_ADMIN is not well-formatted.')
        self.assertIsInstance(val['index'], (int, long),
            'The index of the HS_ADMIN is not an integer.')
        self.assertEqual(str(val['permissions']).replace('0','').replace('1',''), '',
            'The permission value in the HS_ADMIN contains not just 0 and 1.')

    def test_get_value_from_handle_duplicatekey(self):
        """Test retrieving a value of a duplicate key."""

        handlerecord = RECORD
        handle = handlerecord['handle']

        val = self.inst.get_value_from_handle(handle,
                                              'TESTDUP',
                                              handlerecord)
        self.assertIn(val, ("dup1", "dup2"),
            'The value of the duplicate key "TESTDUP" should be "dup1" or "dup2".')

    # retrieve_handle_record

    def test_retrieve_handle_record_normal(self):

        handlerecord = RECORD
        handle = handlerecord['handle']

        dict_record = self.inst.retrieve_handle_record(handle, handlerecord)

        self.assertIn('TEST1', dict_record,
            'Key "test1" not in handlerecord dictionary!')
        self.assertIn('TEST2', dict_record,
            'Key "test2" not in handlerecord dictionary!')
        self.assertIn('TESTDUP', dict_record,
            'Key "testdup" not in handlerecord dictionary!')
        self.assertIn('HS_ADMIN', dict_record,
            'Key "HS_ADMIN" not in handlerecord dictionary!')

        self.assertEqual(dict_record['TEST1'], 'val1',
            'The value of "TEST1" is not "val1.')
        self.assertEqual(dict_record['TEST2'], 'val2',
            'The value of "TEST2" is not "val2.')
        self.assertIn(dict_record['TESTDUP'], ("dup1", "dup2"),
            'The value of the duplicate key "TESTDUP" should be "dup1" or "dup2".')
        self.assertIn('permissions', dict_record['HS_ADMIN'],
            'The HS_ADMIN has no permissions: '+dict_record['HS_ADMIN'])

        self.assertEqual(len(dict_record), 4,
            'The record should have a length of 5 (as the duplicate is ignored.')


    # get_handlerecord_indices_for_key

    def test_get_indices_for_key_normal(self):
        """Test getting the indices for a specific key."""

        handlerecord = RECORD
        handle = handlerecord['handle']

        indices = self.inst.get_handlerecord_indices_for_key('TEST1', handlerecord['values'])
        self.assertEqual(len(indices),1,
            'There is more or less than 1 index!')
        self.assertEqual(indices[0], 3,
            'The index of "test1" is not 3.')

    def test_get_indices_for_key_duplicatekey(self):
        """Test getting the indices for a duplicate key."""

        handlerecord = RECORD
        handle = handlerecord['handle']

        indices = self.inst.get_handlerecord_indices_for_key('TESTDUP', handlerecord['values'])
        self.assertEqual(len(indices),2,
            'There is more or less than 2 indices!')
        self.assertIn(5, indices,
            '5 is not in indices for key "testdup".')
        self.assertIn(6, indices,
            '6 is not in indices for key "testdup".')

    def test_get_indices_for_key_inexistentkey(self):
        """Test getting the indices for an inexistent key."""

        handlerecord = RECORD
        handle = handlerecord['handle'] 

        indices = self.inst.get_handlerecord_indices_for_key('test100', handlerecord['values'])
        self.assertEqual(len(indices),0,
            'There is more than 0 index!')
        self.assertEqual(indices,[],
            'Indices should be an empty list!')

