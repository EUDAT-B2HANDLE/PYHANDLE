"""Testing methods that normally need Handle server read access,
by patching the get request to replace read access."""

import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

import json
import mock
from pyhandle.client.resthandleclient import RESTHandleClient
from pyhandle.clientcredentials import PIDClientCredentials
from pyhandle.handleexceptions import *
from pyhandle.tests.mockresponses import MockResponse, MockSearchResponse
from pyhandle.tests.utilities import failure_message, replace_timestamps, flattensort
from pyhandle.utilhandle import check_handle_syntax

class RESTHandleClientWriteaccessPatchedTestCase(unittest.TestCase):
    '''Testing methods with write access (patched server access).

    The tests work by intercepting all HTTP put requests and comparing their payload to
    the payload of successful real put requests from previous integration tests.

    The payloads from previous tests were collected by a logger in the integration
    tests (look for REQUESTLOGGER in the write-integration test code). Of course,
    the names of the handles have to be adapted in there.

    Comparison it done by python dictionary comparison, which ignores
    the order of the record entries, whitespace, string separators and
    whether keys are unicode strings or normal strings.

    The timestamps should not be compared, so they should be removed. For this,
    there is a method "replace_timestamps".
    '''

    @mock.patch('pyhandle.handlesystemconnector.HandleSystemConnector.check_if_username_exists')
    def setUp(self, username_check_patch):
        self.maxDiff = None

        # Define replacement for the patched check for username existence:
        username_check_patch = mock.Mock()
        username_check_patch.response_value = True

        # Create a client instance for write access:
        self.inst = RESTHandleClient.instantiate_with_username_and_password('http://handle.server', '999:user/name', 'apassword')

    def tearDown(self):
        pass
        pass

    def get_payload_headers_from_mockresponse(self, putpatch):
        # For help, please see: http://www.voidspace.org.uk/python/mock/examples.html#checking-multiple-calls-with-mock
        kwargs_passed_to_put = putpatch.call_args_list[len(putpatch.call_args_list) - 1][1]
        passed_payload = json.loads(kwargs_passed_to_put['data'])
        replace_timestamps(passed_payload)
        passed_headers = kwargs_passed_to_put['headers']
        return passed_payload, passed_headers

    # register_handle

    @mock.patch('pyhandle.handlesystemconnector.requests.Session.put')
    @mock.patch('pyhandle.handlesystemconnector.requests.Session.get')
    def test_register_handle(self, getpatch, putpatch):
        """Test registering a new handle with various types of values."""

        # Define the replacement for the patched GET method:
        # The handle does not exist yet, so a response with 404
        mock_response_get = MockResponse(notfound=True)
        getpatch.return_value = mock_response_get

        # Define the replacement for the patched requests.put method:
        mock_response_put = MockResponse(wascreated=True)
        putpatch.return_value = mock_response_put

        # Run the code to be tested:
        testhandle = 'my/testhandle'
        testlocation = 'http://foo.bar'
        testchecksum = '123456'
        additional_URLs = None
        handle_returned = self.inst.register_handle(testhandle,
                                                    location=testlocation,
                                                    checksum=testchecksum,
                                                    additional_URLs=additional_URLs,
                                                    FOO='foo',
                                                    BAR='bar')


        # Check if the PUT request was sent exactly once:
        self.assertEqual(putpatch.call_count, 1,
            'The method "requests.put" was not called once, but ' + str(putpatch.call_count) + ' times.')

        # Get the payload+headers passed to "requests.put"
        passed_payload, _ = self.get_payload_headers_from_mockresponse(putpatch)
        
        # Compare with expected payload:
        #expected_payload = {"values": [{"index": 100, "type": "HS_ADMIN", "data": {"value": {"index": "200", "handle": "0.NA/my", "permissions": "011111110011"}, "format": "admin"}}, {"index": 1, "type": "URL", "data": "http://foo.bar"}, {"index": 2, "type": "CHECKSUM", "data": "123456"}, {"index": 3, "type": "FOO", "data": "foo"}, {"index": 4, "type": "BAR", "data": "bar"}, {"index": 5, "type": "10320/LOC", "data": "<locations><location href=\"http://bar.bar\" id=\"0\" /><location href=\"http://foo.foo\" id=\"1\" /></locations>"}]}
        
        #expected_payload = {"values": [{"index": 100, "type": "HS_ADMIN", "data": {"value": {"index": "200", "handle": "0.NA/my", "permissions": "011111110011"}, "format": "admin"}}, {"index": 1, "type": "URL", "data": "http://foo.bar"}, {"index": 4, "type": "CHECKSUM", "data": "123456"}, {"index": 2, "type": "FOO", "data": "foo"}, {"index": 3, "type": "BAR", "data": "bar"}]}
        
        if (sys.version_info.major == 3 and sys.version_info.minor > 5):
            expected_payload = {"values": [{"index": 100, "type": "HS_ADMIN", "data": {"value": {"index": "200", "handle": "0.NA/my", "permissions": "011111110011"}, "format": "admin"}}, {"index": 2, "type": "FOO", "data": "foo"}, {"index": 3, "type": "BAR", "data": "bar"}, {"index": 1, "type": "URL", "data": "http://foo.bar"}, {"index": 4, "type": "CHECKSUM", "data": "123456"}]}
            replace_timestamps(expected_payload)
            self.assertIsNotNone(flattensort(passed_payload))
            self.assertIsNotNone(flattensort(expected_payload))
            self.assertEqual(flattensort(passed_payload), flattensort(expected_payload),
                failure_message(expected=expected_payload, passed=passed_payload, methodname='register_handle'))
        elif (sys.version_info.major == 2 and sys.version_info.minor > 6):
            expected_payload = {"values": [{"index": 100, "type": "HS_ADMIN", "data": {"value": {"index": "200", "handle": "0.NA/my", "permissions": "011111110011"}, "format": "admin"}}, {"index": 1, "type": "URL", "data": "http://foo.bar"}, {"index": 2, "type": "CHECKSUM", "data": "123456"}, {"index": 3, "type": "FOO", "data": "foo"}, {"index": 4, "type": "BAR", "data": "bar"}]}
            replace_timestamps(expected_payload)
            self.assertIsNotNone(flattensort(passed_payload))
            self.assertIsNotNone(flattensort(expected_payload))
            self.assertEqual(flattensort(passed_payload), flattensort(expected_payload),
                failure_message(expected=expected_payload, passed=passed_payload, methodname='register_handle'))
    
    @mock.patch('pyhandle.handlesystemconnector.requests.Session.put')
    @mock.patch('pyhandle.handlesystemconnector.requests.Session.get')
    def test_register_handle_kv(self, getpatch, putpatch):
        """Test registering a new handle with various types of values."""

        # Define the replacement for the patched GET method:
        # The handle does not exist yet, so a response with 404
        mock_response_get = MockResponse(notfound=True)
        getpatch.return_value = mock_response_get

        # Define the replacement for the patched requests.put method:
        mock_response_put = MockResponse(wascreated=True)
        putpatch.return_value = mock_response_put

        # Run the code to be tested:
        testhandle = 'my/testhandle'
        handle_returned = self.inst.register_handle_kv(testhandle,
                                                    URL='http://foo.bar',
                                                    CHECKSUM='123456',
                                                    FOO='foo',
                                                    BAR='bar')


        # Check if the PUT request was sent exactly once:
        self.assertEqual(putpatch.call_count, 1,
            'The method "requests.put" was not called once, but ' + str(putpatch.call_count) + ' times.')

        # Get the payload+headers passed to "requests.put"
        passed_payload, _ = self.get_payload_headers_from_mockresponse(putpatch)
        
        # Compare with expected payload:
        if (sys.version_info.major == 3 and sys.version_info.minor != 5):
            expected_payload = {"values": [{"index": 100, "type": "HS_ADMIN", "data": {"value": {"index": "200", "handle": "0.NA/my", "permissions": "011111110011"}, "format": "admin"}}, {"index": 1, "type": "URL", "data": "http://foo.bar"}, {"index": 2, "type": "CHECKSUM", "data": "123456"}, {"index": 3, "type": "FOO", "data": "foo"}, {"index": 4, "type": "BAR", "data": "bar"}]}
            #expected_payload = {"values": [{"index": 100, "type": "HS_ADMIN", "data": {"value": {"index": "200", "handle": "0.NA/my", "permissions": "011111110011"}, "format": "admin"}}, {"index": 1, "type": "URL", "data": "http://foo.bar"}, {"index": 4, "type": "CHECKSUM", "data": "123456"}, {"index": 2, "type": "FOO", "data": "foo"}, {"index": 3, "type": "BAR", "data": "bar"}]}
            replace_timestamps(expected_payload)
            self.assertIsNotNone(flattensort(passed_payload))
            self.assertIsNotNone(flattensort(expected_payload))
            self.assertEqual(flattensort(passed_payload), flattensort(expected_payload),
                failure_message(expected=expected_payload, passed=passed_payload, methodname='register_handle'))
    
    @mock.patch('pyhandle.handlesystemconnector.requests.Session.put')
    @mock.patch('pyhandle.handlesystemconnector.requests.Session.get')
    def test_register_handle_json(self, getpatch, putpatch):
        """Test registering a new handle using JSON entries, where HS_ADMIN is not specified."""

        # Define the replacement for the patched GET method:
        # The handle does not exist yet, so a response with 404
        mock_response_get = MockResponse(notfound=True)
        getpatch.return_value = mock_response_get

        # Define the replacement for the patched requests.put method:
        mock_response_put = MockResponse(wascreated=True)
        putpatch.return_value = mock_response_put

        # Run the code to be tested:
        testhandle = 'my/testhandle'
        entries = [
            {'index':1, 'type':'URL', 'data':'http://foo.bar'},
            {'index':2, 'type':'CHECKSUM', 'data':'123456'},
            {'index':3, 'type':'FOO', 'data':'foo'},
            {'index':4, 'type':'BAR', 'data':'bar'}
        ]

        handle_returned = self.inst.register_handle_json(testhandle,
                                                    entries)


        # Check if the PUT request was sent exactly once:
        self.assertEqual(putpatch.call_count, 1,
            'The method "requests.put" was not called once, but ' + str(putpatch.call_count) + ' times.')

        # Get the payload+headers passed to "requests.put"
        passed_payload, _ = self.get_payload_headers_from_mockresponse(putpatch)
        
        # Compare with expected payload:
        expected_payload = {"values": entries}
        expected_payload["values"].append({
                'index':100,
                'type':'HS_ADMIN', 
                'data': {
                    'value':{
                        'index':'200', # TODO Why string and not int?
                        'handle':'0.NA/my',
                        'permissions':'011111110011'
                    },
                    'format':'admin'
                }
            })
        replace_timestamps(expected_payload)
        self.assertIsNotNone(flattensort(passed_payload))
        self.assertIsNotNone(flattensort(expected_payload))
        self.assertEqual(flattensort(passed_payload), flattensort(expected_payload),
            failure_message(expected=expected_payload, passed=passed_payload, methodname='register_handle'))

    @mock.patch('pyhandle.handlesystemconnector.requests.Session.put')
    @mock.patch('pyhandle.handlesystemconnector.requests.Session.get')
    def test_register_handle_json_admin_given(self, getpatch, putpatch):
        """Test registering a new handle using JSON entries, where HS_ADMIN is specified."""

        # Define the replacement for the patched GET method:
        # The handle does not exist yet, so a response with 404
        mock_response_get = MockResponse(notfound=True)
        getpatch.return_value = mock_response_get

        # Define the replacement for the patched requests.put method:
        mock_response_put = MockResponse(wascreated=True)
        putpatch.return_value = mock_response_put

        # Run the code to be tested:
        testhandle = 'my/testhandle'
        entries = [
            {'index':1, 'type':'URL', 'data':'http://foo.bar'},
            {'index':2, 'type':'CHECKSUM', 'data':'123456'},
            {'index':3, 'type':'FOO', 'data':'foo'},
            {'index':4, 'type':'BAR', 'data':'bar'},
            {
                'index':100,
                'type':'HS_ADMIN', 
                'data': {
                    'value':{
                        'index':222,
                        'handle':'0.NA/myprefix',
                        'permissions':'bluubb'
                    },
                    'format':'admin'
                }
            }
        ]

        handle_returned = self.inst.register_handle_json(testhandle,
                                                    entries)


        # Check if the PUT request was sent exactly once:
        self.assertEqual(putpatch.call_count, 1,
            'The method "requests.put" was not called once, but ' + str(putpatch.call_count) + ' times.')

        # Get the payload+headers passed to "requests.put"
        passed_payload, _ = self.get_payload_headers_from_mockresponse(putpatch)
        
        # Compare with expected payload:
        #expected_payload = {"values": [{"index": 100, "type": "HS_ADMIN", "data": {"value": {"index": "200", "handle": "0.NA/my", "permissions": "011111110011"}, "format": "admin"}}, {"index": 1, "type": "URL", "data": "http://foo.bar"}, {"index": 2, "type": "CHECKSUM", "data": "123456"}, {"index": 3, "type": "FOO", "data": "foo"}, {"index": 4, "type": "BAR", "data": "bar"}]}
        #expected_payload = {"values": [{"index": 100, "type": "HS_ADMIN", "data": {"value": {"index": "200", "handle": "0.NA/my", "permissions": "011111110011"}, "format": "admin"}}, {"index": 1, "type": "URL", "data": "http://foo.bar"}, {"index": 4, "type": "CHECKSUM", "data": "123456"}, {"index": 2, "type": "FOO", "data": "foo"}, {"index": 3, "type": "BAR", "data": "bar"}]}
        #expected_payload = entries
        expected_payload = {"values": entries}
        replace_timestamps(expected_payload)
        self.assertIsNotNone(flattensort(passed_payload))
        self.assertIsNotNone(flattensort(expected_payload))
        self.assertEqual(flattensort(passed_payload), flattensort(expected_payload),
            failure_message(expected=expected_payload, passed=passed_payload, methodname='register_handle'))

    @mock.patch('pyhandle.handlesystemconnector.requests.Session.put')
    @mock.patch('pyhandle.handlesystemconnector.requests.Session.get')
    def test_register_handle_additional_urls(self, getpatch, putpatch):
        """Test registering a new handle with additional URLs, which is
        not supported anymore."""

        # Define the replacement for the patched GET method:
        # The handle does not exist yet, so a response with 404
        mock_response_get = MockResponse(notfound=True)
        getpatch.return_value = mock_response_get

        # Define the replacement for the patched requests.put method:
        mock_response_put = MockResponse(wascreated=True)
        putpatch.return_value = mock_response_put

        # Run the code to be tested:
        testhandle = 'my/testhandle'
        testlocation = 'http://foo.bar'
        testchecksum = '123456'
        additional_URLs = ['http://bar.bar', 'http://foo.foo']
        # Run code to be tested + check exception:
        with self.assertRaises(NotImplementedError):
            handle_returned = self.inst.register_handle(testhandle,
                                                    location=testlocation,
                                                    checksum=testchecksum,
                                                    additional_URLs=additional_URLs,
                                                    FOO='foo',
                                                    BAR='bar')

    @mock.patch('pyhandle.handlesystemconnector.HandleSystemConnector.check_if_username_exists')
    @mock.patch('pyhandle.handlesystemconnector.requests.Session.put')
    @mock.patch('pyhandle.handlesystemconnector.requests.Session.get')
    def test_register_handle_different_owner(self, getpatch, putpatch, username_check_patch):
        """Test registering a new handle with various types of values."""

        # Define the replacement for the patched GET method:
        # The handle does not exist yet, so a response with 404
        mock_response_get = MockResponse(notfound=True)
        getpatch.return_value = mock_response_get

        # Define the replacement for the patched requests.put method:
        mock_response_put = MockResponse(wascreated=True)
        putpatch.return_value = mock_response_put

        # Define replacement for the patched check for username existence:
        username_check_patch = mock.Mock()
        username_check_patch.response_value = True

        # Make another connector, to add the handle owner:
        cred = PIDClientCredentials(client='client',
                                   handle_server_url='http://handle.server',
                                   username='999:user/name',
                                   password='apassword',
                                   prefix='myprefix',
                                   handleowner='300:handle/owner')
        newInst = RESTHandleClient.instantiate_with_credentials(cred)

        # Run the code to be tested:
        testhandle = 'my/testhandle'
        testlocation = 'http://foo.bar'
        testchecksum = '123456'
        #additional_URLs = ['http://bar.bar', 'http://foo.foo']
        additional_URLs = None
        handle_returned = newInst.register_handle(testhandle,
                                                  location=testlocation,
                                                  checksum=testchecksum,
                                                  additional_URLs=additional_URLs,
                                                  FOO='foo',
                                                  BAR='bar')


        # Check if the PUT request was sent exactly once:
        self.assertEqual(putpatch.call_count, 1,
            'The method "requests.put" was not called once, but ' + str(putpatch.call_count) + ' times.')

        # Get the payload+headers passed to "requests.put"
        passed_payload, _ = self.get_payload_headers_from_mockresponse(putpatch)

        # Compare with expected payload:
        # Previously contained 10320LOC field:
        #expected_payload = {"values": [{"index": 100, "type": "HS_ADMIN", "data": {"value": {"index": 300, "handle": "handle/owner", "permissions": "011111110011"}, "format": "admin"}}, {"index": 1, "type": "URL", "data": "http://foo.bar"}, {"index": 2, "type": "CHECKSUM", "data": "123456"}, {"index": 3, "type": "FOO", "data": "foo"}, {"index": 4, "type": "BAR", "data": "bar"}, {"index": 5, "type": "10320/LOC", "data": "<locations><location href=\"http://bar.bar\" id=\"0\" /><location href=\"http://foo.foo\" id=\"1\" /></locations>"}]}
        # Changed order/index: old one
        #expected_payload = {"values": [{"index": 100, "type": "HS_ADMIN", "data": {"value": {"index": 300, "handle": "handle/owner", "permissions": "011111110011"}, "format": "admin"}}, {"index": 1, "type": "URL", "data": "http://foo.bar"}, {"index": 4, "type": "CHECKSUM", "data": "123456"}, {"index": 2, "type": "FOO", "data": "foo"}, {"index": 3, "type": "BAR", "data": "bar"}]}
        
        if (sys.version_info.major == 3 and sys.version_info.minor > 5):
            expected_payload = {"values": [{"index": 100, "type": "HS_ADMIN", "data": {"value": {"index": 300, "handle": "handle/owner", "permissions": "011111110011"}, "format": "admin"}}, {"index": 2, "type": "FOO", "data": "foo"}, {"index": 3, "type": "BAR", "data": "bar"}, {"index": 1, "type": "URL", "data": "http://foo.bar"}, {"index": 4, "type": "CHECKSUM", "data": "123456"}]}
            replace_timestamps(expected_payload)
            self.assertIsNotNone(flattensort(passed_payload))
            self.assertIsNotNone(flattensort(expected_payload))
            self.assertEqual(flattensort(passed_payload), flattensort(expected_payload),
                failure_message(expected=expected_payload, passed=passed_payload, methodname='register_handle'))
        elif (sys.version_info.major == 2 and sys.version_info.minor >= 7):
            expected_payload = {"values": [{"index": 100, "type": "HS_ADMIN", "data": {"value": {"index": 300, "handle": "handle/owner", "permissions": "011111110011"}, "format": "admin"}}, {"index": 1, "type": "URL", "data": "http://foo.bar"}, {"index": 2, "type": "CHECKSUM", "data": "123456"}, {"index": 3, "type": "FOO", "data": "foo"}, {"index": 4, "type": "BAR", "data": "bar"}]}
            replace_timestamps(expected_payload)
            self.assertIsNotNone(flattensort(passed_payload))
            self.assertIsNotNone(flattensort(expected_payload))
            self.assertEqual(flattensort(passed_payload), flattensort(expected_payload),
                failure_message(expected=expected_payload, passed=passed_payload, methodname='register_handle'))
        
        
  
            

    @mock.patch('pyhandle.handlesystemconnector.requests.Session.put')
    @mock.patch('pyhandle.handlesystemconnector.requests.Session.get')
    def test_register_handle_already_exists(self, getpatch, putpatch):
        """Test if overwrite=False prevents handle overwriting."""

        # Define the replacement for the patched GET method:
        mock_response_get = MockResponse(success=True)
        getpatch.return_value = mock_response_get

        # Run code to be tested + check exception:
        with self.assertRaises(HandleAlreadyExistsException):
            self.inst.register_handle('my/testhandle',
                                      'http://foo.foo',
                                      test1='I am just an illusion.',
                                      overwrite=False)

        # Check if nothing was changed (PUT should not have been called):
        self.assertEqual(putpatch.call_count, 0,
            'The method "requests.put" was called! (' + str(putpatch.call_count) + ' times). It should NOT have been called.')

    @mock.patch('pyhandle.handlesystemconnector.requests.Session.put')
    @mock.patch('pyhandle.handlesystemconnector.requests.Session.get')
    def test_register_handle_already_exists_overwrite(self, getpatch, putpatch):
        """Test registering an existing handle with various types of values, with overwrite=True."""

        # Define the replacement for the patched GET method:
        mock_response_get = MockResponse(success=True)
        getpatch.return_value = mock_response_get

        # Define the replacement for the patched requests.put method:
        mock_response_put = MockResponse(wascreated=True)
        putpatch.return_value = mock_response_put

        # Run the method to be tested:
        testhandle = 'my/testhandle'
        testlocation = 'http://foo.bar'
        testchecksum = '123456'
        overwrite = True
        #additional_URLs = ['http://bar.bar', 'http://foo.foo']
        additional_URLs = None
        handle_returned = self.inst.register_handle(testhandle,
                                                    location=testlocation,
                                                    checksum=testchecksum,
                                                    additional_URLs=additional_URLs,
                                                    overwrite=overwrite,
                                                    FOO='foo',
                                                    BAR='bar')

        # Check if the PUT request was sent exactly once:
        self.assertEqual(putpatch.call_count, 1,
            'The method "requests.put" was not called once, but ' + str(putpatch.call_count) + ' times.')

        # Get the payload+headers passed to "requests.put"
        passed_payload, passed_headers = self.get_payload_headers_from_mockresponse(putpatch)

        # Compare with expected payload:
        # Previously contained 10320LOC:
        #expected_payload = {"values": [{"index": 100, "type": "HS_ADMIN", "data": {"value": {"index": "200", "handle": "0.NA/my", "permissions": "011111110011"}, "format": "admin"}}, {"index": 1, "type": "URL", "data": "http://foo.bar"}, {"index": 2, "type": "CHECKSUM", "data": "123456"}, {"index": 3, "type": "FOO", "data": "foo"}, {"index": 4, "type": "BAR", "data": "bar"}, {"index": 5, "type": "10320/LOC", "data": "<locations><location href=\"http://bar.bar\" id=\"0\" /><location href=\"http://foo.foo\" id=\"1\" /></locations>"}]}
       
        # Different indizes:
        #expected_payload = {"values": [{"index": 100, "type": "HS_ADMIN", "data": {"value": {"index": "200", "handle": "0.NA/my", "permissions": "011111110011"}, "format": "admin"}}, {"index": 1, "type": "URL", "data": "http://foo.bar"}, {"index": 4, "type": "CHECKSUM", "data": "123456"}, {"index": 2, "type": "FOO", "data": "foo"}, {"index": 3, "type": "BAR", "data": "bar"}]}

        if (sys.version_info.major == 3 and sys.version_info.minor > 5):
            expected_payload = {"values": [{"index": 100, "type": "HS_ADMIN", "data": {"value": {"index": "200", "handle": "0.NA/my", "permissions": "011111110011"}, "format": "admin"}}, {"index": 2, "type": "FOO", "data": "foo"}, {"index": 3, "type": "BAR", "data": "bar"}, {"index": 1, "type": "URL", "data": "http://foo.bar"}, {"index": 4, "type": "CHECKSUM", "data": "123456"}]}
            replace_timestamps(expected_payload)
            self.assertEqual(flattensort(passed_payload), flattensort(expected_payload),
                failure_message(expected=expected_payload, passed=passed_payload, methodname='register_handle'))
            self.assertIsNotNone(flattensort(passed_payload))
            self.assertIsNotNone(flattensort(expected_payload))
            # Check if requests.put received an authorization header:
            self.assertIn('Authorization', passed_headers,
                'Authorization header not passed: ' + str(passed_headers))
        elif (sys.version_info.major == 2 and sys.version_info.minor > 6):
            expected_payload = {"values": [{"index": 100, "type": "HS_ADMIN", "data": {"value": {"index": "200", "handle": "0.NA/my", "permissions": "011111110011"}, "format": "admin"}}, {"index": 1, "type": "URL", "data": "http://foo.bar"}, {"index": 2, "type": "CHECKSUM", "data": "123456"}, {"index": 3, "type": "FOO", "data": "foo"}, {"index": 4, "type": "BAR", "data": "bar"}]}
            replace_timestamps(expected_payload)
            self.assertEqual(flattensort(passed_payload), flattensort(expected_payload),
                failure_message(expected=expected_payload, passed=passed_payload, methodname='register_handle'))
            self.assertIsNotNone(flattensort(passed_payload))
            self.assertIsNotNone(flattensort(expected_payload))
            # Check if requests.put received an authorization header:
            self.assertIn('Authorization', passed_headers,
                'Authorization header not passed: ' + str(passed_headers))

    # generate_and_register_handle

    @mock.patch('pyhandle.handlesystemconnector.requests.Session.put')
    @mock.patch('pyhandle.handlesystemconnector.requests.Session.get')
    def test_generate_and_register_handle(self, getpatch, putpatch):
        """Test generating and registering a new handle."""

        # Define the replacement for the patched GET method:
        mock_response_get = MockResponse(notfound=True)
        getpatch.return_value = mock_response_get
        # Define the replacement for the patched requests.put method:
        mock_response_put = MockResponse(wascreated=True)
        putpatch.return_value = mock_response_put

        # Run the method to be tested:
        testlocation = 'http://foo.bar'
        testchecksum = '123456'
        handle_returned = self.inst.generate_and_register_handle(
            prefix='my',
            location=testlocation,
            checksum=testchecksum)

        # Check if the PUT request was sent exactly once:
        self.assertEqual(putpatch.call_count, 1,
            'The method "requests.put" was not called once, but ' + str(putpatch.call_count) + ' times.')

        # Get the payload+headers passed to "requests.put"
        passed_payload, _ = self.get_payload_headers_from_mockresponse(putpatch)

        # Compare with expected payload:
        expected_payload = {"values": [{"index": 100, "type": "HS_ADMIN", "data": {"value": {"index": "200", "handle": "0.NA/my", "permissions": "011111110011"}, "format": "admin"}}, {"index": 1, "type": "URL", "data": "http://foo.bar"}, {"index": 2, "type": "CHECKSUM", "data": "123456"}]}
        replace_timestamps(expected_payload)
        self.assertIsNotNone(flattensort(passed_payload))
        self.assertIsNotNone(flattensort(expected_payload))
        self.assertEqual(flattensort(passed_payload), flattensort(expected_payload),
            failure_message(expected=expected_payload, passed=passed_payload, methodname='generate_and_register_handle'))

    # modify_handle_value

    @mock.patch('pyhandle.handlesystemconnector.requests.Session.put')
    @mock.patch('pyhandle.handlesystemconnector.requests.Session.get')
    def test_modify_handle_value_one(self, getpatch, putpatch):
        """Test modifying one existing handle value."""

        # Define the replacement for the patched GET method:
        cont = {"responseCode":1, "handle":"my/testhandle", "values":[{"index":111, "type": "TEST1", "data":{"format":"string", "value":"val1"}, "ttl":86400, "timestamp":"2015-09-29T15:51:08Z"}, {"index":2222, "type": "TEST2", "data":{"format":"string", "value":"val2"}, "ttl":86400, "timestamp":"2015-09-29T15:51:08Z"}, {"index":333, "type": "TEST3", "data":{"format":"string", "value":"val3"}, "ttl":86400, "timestamp":"2015-09-29T15:51:08Z"}, {"index":4, "type": "TEST4", "data":{"format":"string", "value":"val4"}, "ttl":86400, "timestamp":"2015-09-29T15:51:08Z"}]}
        mock_response_get = MockResponse(status_code=200, content=json.dumps(cont))
        getpatch.return_value = mock_response_get

        # Define the replacement for the patched requests.put method:
        cont = {"responseCode":1, "handle":"my/testhandle"}
        mock_response_put = MockResponse(status_code=201, content=json.dumps(cont))
        putpatch.return_value = mock_response_put

        # Run the method to be tested:
        testhandle = 'my/testhandle'
        self.inst.modify_handle_value(testhandle, TEST4='newvalue')

        # Check if the PUT request was sent exactly once:
        self.assertEqual(putpatch.call_count, 1,
            'The method "requests.put" was not called once, but ' + str(putpatch.call_count) + ' times.')

        # Get the payload passed to "requests.put"
        passed_payload, _ = self.get_payload_headers_from_mockresponse(putpatch)

        # Compare with expected payload:
        expected_payload = {"values": [{"index": 4, "ttl": 86400, "type": "TEST4", "data": "newvalue"}]}
        replace_timestamps(expected_payload)
        self.assertEqual(passed_payload, expected_payload,
            failure_message(expected=expected_payload,
                                 passed=passed_payload,
                                 methodname='modify_handle_value'))

    @mock.patch('pyhandle.handlesystemconnector.requests.Session.put')
    @mock.patch('pyhandle.handlesystemconnector.requests.Session.get')
    def test_modify_handle_value_with_hdl(self, getpatch, putpatch):
        """Test whether a prepended "hdl:" gets removed before asking the server to modify existing handle value.
        Because the Handle Server won't accept REST API calls with hdl: prepended. It will respond with HTTP 400
        and Response: {"responseCode":301, "message":"That prefix doesn't live here","handle":"hdl:21.14106/TESTTESTTEST"}
        The problem is prevented by removing any hdl: or doi: right before making the request."""

        # Define the replacement for the patched GET method:
        cont = {"responseCode":1, "handle":"my/testhandle", "values":[{"index":111, "type": "TEST1", "data":{"format":"string", "value":"val1"}, "ttl":86400, "timestamp":"2015-09-29T15:51:08Z"}, {"index":2222, "type": "TEST2", "data":{"format":"string", "value":"val2"}, "ttl":86400, "timestamp":"2015-09-29T15:51:08Z"}, {"index":333, "type": "TEST3", "data":{"format":"string", "value":"val3"}, "ttl":86400, "timestamp":"2015-09-29T15:51:08Z"}, {"index":4, "type": "TEST4", "data":{"format":"string", "value":"val4"}, "ttl":86400, "timestamp":"2015-09-29T15:51:08Z"}]}
        mock_response_get = MockResponse(status_code=200, content=json.dumps(cont))
        getpatch.return_value = mock_response_get

        # Define the replacement for the patched requests.put method:
        testhandle = 'hdl:my/testhandle'
        cont = {"responseCode":1, "handle":"my/testhandle"}
        mock_response_put = MockResponse(handle=testhandle, status_code=201, content=json.dumps(cont))
        putpatch.return_value = mock_response_put

        # Run the method to be tested:
        self.inst.modify_handle_value(testhandle, TEST4='newvalue')

        # Check if the PUT request was sent exactly once:
        self.assertEqual(putpatch.call_count, 1,
            'The method "requests.put" was not called once, but ' + str(putpatch.call_count) + ' times.')

        # Check whether the API got called with a handle WITHOUT "hdl:":
        url = 'http://handle.server/api/handles/my/testhandle?index=4&overwrite=true'
        payload = '{"values": [{"index": 4, "type": "TEST4", "data": "newvalue", "ttl": 86400}]}'
        head = {'Authorization': 'Basic OTk5JTNBdXNlci9uYW1lOmFwYXNzd29yZA==', 'Content-Type': 'application/json'}
        if not (sys.version_info.major==3 and sys.version_info.minor==5):
            putpatch.assert_called_with(url, data=payload, headers=head, verify=True, allow_redirects=False)    
        else:
            # In Python 3.5 sorting dictionaries is a problem. But the only thing that matters is the url, so we
            # test only that:
            rec_args = putpatch.call_args
            self.assertTrue(rec_args[0][0] == 'http://handle.server/api/handles/my/testhandle?index=4&overwrite=true')
            #print(rec_args[0])    # positional args: ('http://handle.server/api/handles/my/testhandle?index=4&overwrite=true',)
            #print(rec_args[1])    # kwargs
            # specific:
            #print(rec_args[0][0])                 # http://handle.server/api/handles/my/testhandle?index=4&overwrite=true
            #print(rec_args[1]['allow_redirects']) # False
            #print(rec_args[1]['data'])            # {"values": [{"ttl": 86400, "data": "newvalue", "index": 4, "type": "TEST4"}]}
            #print(rec_args[1]['headers'])         # {'Authorization': 'Basic OTk5JTNBdXNlci9uYW1lOmFwYXNzd29yZA==', 'Content-Type': 'application/json'}
            #print(rec_args[1]['verify'])          # True

        # Get the payload passed to "requests.put"
        passed_payload, _ = self.get_payload_headers_from_mockresponse(putpatch)

        # Compare with expected payload:
        expected_payload = {"values": [{"type": "TEST4", "index": 4, "ttl": 86400, "data": "newvalue"}]}
        replace_timestamps(expected_payload)
        self.assertEqual(sorted(passed_payload['values'][0]), sorted(expected_payload['values'][0]))
        #self.assertEqual(passed_payload, expected_payload,
        #    failure_message(expected=expected_payload,
        #                         passed=passed_payload,
        #                         methodname='modify_handle_value'))


    @mock.patch('pyhandle.handlesystemconnector.requests.Session.put')
    @mock.patch('pyhandle.handlesystemconnector.requests.Session.get')
    def test_modify_handle_value_several(self, getpatch, putpatch):
        """Test modifying several existing handle values."""

        # Define the replacement for the patched GET method:
        cont = {
            "responseCode":1,
            "handle":"my/testhandle",
            "values":[
            {
                "index":111,
                "type": "TEST1",
                "data":{
                    "format":"string",
                    "value":"val1"
                },
                "ttl":86400,
                "timestamp":"2015-09-29T15:51:08Z"
            }, {
                "index":2222,
                "type": "TEST2",
                "data":{
                    "format":"string",
                    "value":"val2"
                },
                "ttl":86400,
                "timestamp":"2015-09-29T15:51:08Z"
            }, {
                "index":333,
                "type": "TEST3",
                "data":{
                    "format":"string",
                    "value":"val3"
                },
                "ttl":86400,
                "timestamp":"2015-09-29T15:51:08Z"
            }, {
                "index":4,
                "type": "TEST4",
                "data":{
                    "format":"string",
                    "value":"val4"
                },
                "ttl":86400,
                "timestamp":"2015-09-29T15:51:08Z"
            }]
        }
        mock_response_get = MockResponse(status_code=200, content=json.dumps(cont))
        getpatch.return_value = mock_response_get

        # Define the replacement for the patched requests.delete method:
        mock_response_put = MockResponse()
        putpatch.return_value = mock_response_put

        # Test variables
        testhandle = 'my/testhandle'

        # Run the method to be tested:
        self.inst.modify_handle_value(testhandle,
                                          TEST4='new4',
                                          TEST2='new2',
                                          TEST3='new3')

        # Check if the PUT request was sent exactly once:
        self.assertEqual(putpatch.call_count, 1,
            'The method "requests.put" was not called once, but ' + str(putpatch.call_count) + ' times.')

        # Get the payload passed to "requests.put"
        passed_payload, _ = self.get_payload_headers_from_mockresponse(putpatch)
        
        # Compare with expected payload:
        expected_payload = {
        "values":[
            {
              "index":333,
                "type": "TEST3",
                "data":"new3",
                "ttl":86400,


            }, {
               
                "index":2222,
                "type": "TEST2",
                "data":"new2",
                "ttl":86400,
            }, {
                "index":4,
                "type": "TEST4",
                "data":"new4",
                "ttl":86400,
            }]
        }
        replace_timestamps(expected_payload)
        self.assertEqual(flattensort(passed_payload), flattensort(expected_payload),
            failure_message(expected=expected_payload,
                                 passed=passed_payload,
                                 methodname='modify_handle_value'))

    @mock.patch('pyhandle.handlesystemconnector.requests.Session.put')
    @mock.patch('pyhandle.handlesystemconnector.requests.Session.get')
    def test_modify_handle_value_corrupted(self, getpatch, putpatch):
        """Test exception when trying to modify corrupted handle record."""

        # Define the replacement for the patched GET method (getting a corrupted record):
        cont = {"responseCode":1, "handle":"my/testhandle", "values":[{"index":111, "type": "TEST1", "data":{"format":"string", "value":"val1"}, "ttl":86400, "timestamp":"2015-09-30T15:08:49Z"}, {"index":2222, "type": "TEST2", "data":{"format":"string", "value":"val2"}, "ttl":86400, "timestamp":"2015-09-30T15:08:49Z"}, {"index":333, "type": "TEST2", "data":{"format":"string", "value":"val3"}, "ttl":86400, "timestamp":"2015-09-30T15:08:49Z"}, {"index":4, "type": "TEST4", "data":{"format":"string", "value":"val4"}, "ttl":86400, "timestamp":"2015-09-30T15:08:49Z"}]}
        mock_response_get = MockResponse(status_code=200, content=json.dumps(cont))
        getpatch.return_value = mock_response_get

        # Define the replacement for the patched requests.put method:
        cont = {"responseCode":1, "handle":"my/testhandle"}
        mock_response_put = MockResponse(status_code=201, content=json.dumps(cont))
        putpatch.return_value = mock_response_put

        # Call the method to be tested: Modifying corrupted raises exception:
        with self.assertRaises(BrokenHandleRecordException):
            self.inst.modify_handle_value('my/testhandle',
                                          TEST4='new4',
                                          TEST2='new2',
                                          TEST3='new3')

        # Check if PUT was called (PUT should not have been called):
        self.assertEqual(putpatch.call_count, 0,
            'The method "requests.put" was called! (' + str(putpatch.call_count) + ' times). It should NOT have been called.')

    @mock.patch('pyhandle.handlesystemconnector.requests.Session.delete')
    @mock.patch('pyhandle.handlesystemconnector.requests.Session.get')
    def test_modify_handle_value_without_authentication(self, getpatch, putpatch):
        """Test if exception when not authenticated."""

        # Define the replacement for the patched GET method:
        cont = {"responseCode":1, "handle":"my/testhandle", "values":[{"index":111, "type": "TEST1", "data":{"format":"string", "value":"val1"}, "ttl":86400, "timestamp":"2015-09-29T15:51:08Z"}, {"index":2222, "type": "TEST2", "data":{"format":"string", "value":"val2"}, "ttl":86400, "timestamp":"2015-09-29T15:51:08Z"}, {"index":333, "type": "TEST3", "data":{"format":"string", "value":"val3"}, "ttl":86400, "timestamp":"2015-09-29T15:51:08Z"}, {"index":4, "type": "TEST4", "data":{"format":"string", "value":"val4"}, "ttl":86400, "timestamp":"2015-09-29T15:51:08Z"}]}
        mock_response_get = MockResponse(status_code=200, content=json.dumps(cont))
        getpatch.return_value = mock_response_get

        # Define the replacement for the patched requests.delete method:
        mock_response_put = MockResponse()
        putpatch.return_value = mock_response_put

        # Test variables
        inst_readonly = RESTHandleClient('http://foo.com', HTTP_verify=True)
        testhandle = 'my/testhandle'

        # Run code to be tested and check exception:
        with self.assertRaises(HandleAuthenticationError):
            inst_readonly.modify_handle_value(testhandle, FOO='bar')

    @mock.patch('pyhandle.handlesystemconnector.requests.Session.put')
    @mock.patch('pyhandle.handlesystemconnector.requests.Session.get')
    def test_modify_handle_value_several_inexistent(self, getpatch, putpatch):
        """Test modifying several existing handle values, one of them inexistent."""

        # Define the replacement for the patched GET method:
        cont = {"responseCode":1, "handle":"my/testhandle", "values":[{"index":111, "type": "TEST1", "data":{"format":"string", "value":"val1"}, "ttl":86400, "timestamp":"2015-09-29T15:51:08Z"}, {"index":2222, "type": "TEST2", "data":{"format":"string", "value":"val2"}, "ttl":86400, "timestamp":"2015-09-29T15:51:08Z"}, {"index":333, "type": "TEST3", "data":{"format":"string", "value":"val3"}, "ttl":86400, "timestamp":"2015-09-29T15:51:08Z"}, {"index":4, "type": "TEST4", "data":{"format":"string", "value":"val4"}, "ttl":86400, "timestamp":"2015-09-29T15:51:08Z"}]}
        mock_response_get = MockResponse(status_code=200, content=json.dumps(cont))
        getpatch.return_value = mock_response_get

        # Define the replacement for the patched requests.delete method:
        mock_response_put = MockResponse()
        putpatch.return_value = mock_response_put

        # Test variables
        testhandle = 'my/testhandle'

        # Run the method to be tested:
        self.inst.modify_handle_value(testhandle,
                                          TEST4='new4',
                                          TEST2='new2',
                                          TEST100='new100')

        # Check if the PUT request was sent exactly once:
        self.assertEqual(putpatch.call_count, 1,
            'The method "requests.put" was not called once, but ' + str(putpatch.call_count) + ' times.')

        # Get the payload passed to "requests.put"
        passed_payload, _ = self.get_payload_headers_from_mockresponse(putpatch)
        passed_payload.get('values', {})
        # Compare with expected payload:
        expected_payload = {"values": [{"index": 2, "type": "TEST100", "data": "new100"}, {"index": 2222, "ttl": 86400, "type": "TEST2", "data": "new2"}, {"index": 4, "ttl": 86400, "type": "TEST4", "data": "new4"}]}
        expected_payload.get('values', {})
        replace_timestamps(expected_payload)
        self.assertEqual(flattensort(passed_payload), flattensort(expected_payload),
            failure_message(expected=expected_payload,
                                 passed=passed_payload,
                                 methodname='modify_handle_value'))


    @mock.patch('pyhandle.handlesystemconnector.requests.Session.put')
    @mock.patch('pyhandle.handlesystemconnector.requests.Session.get')
    def test_modify_handle_value_several_inexistent_2(self, getpatch, putpatch):
        """Test modifying several existing handle values, SEVERAL of them inexistent."""

        # Define the replacement for the patched GET method:
        cont = {"responseCode":1, "handle":"my/testhandle", "values":[{"index":111, "type": "TEST1", "data":{"format":"string", "value":"val1"}, "ttl":86400, "timestamp":"2015-09-29T15:51:08Z"}, {"index":2222, "type": "TEST2", "data":{"format":"string", "value":"val2"}, "ttl":86400, "timestamp":"2015-09-29T15:51:08Z"}, {"index":333, "type": "TEST3", "data":{"format":"string", "value":"val3"}, "ttl":86400, "timestamp":"2015-09-29T15:51:08Z"}, {"index":4, "type": "TEST4", "data":{"format":"string", "value":"val4"}, "ttl":86400, "timestamp":"2015-09-29T15:51:08Z"}]}
            
            
        mock_response_get = MockResponse(status_code=200, content=json.dumps(cont))
        getpatch.return_value = mock_response_get

        # Define the replacement for the patched requests.delete method:
        mock_response_put = MockResponse()
        putpatch.return_value = mock_response_put

        # Test variables
        testhandle = 'my/testhandle'

        # Run the method to be tested:
        self.inst.modify_handle_value(testhandle,
                                          TEST4='new4',
                                          TEST2='new2',
                                          TEST100='new100',
                                          TEST101='new101')

        # Check if the PUT request was sent exactly once:
        self.assertEqual(putpatch.call_count, 1,
            'The method "requests.put" was not called once, but ' + str(putpatch.call_count) + ' times.')

        # Get the payload passed to "requests.put"
        passed_payload, _ = self.get_payload_headers_from_mockresponse(putpatch)
        
        # Compare with expected payload:
        
        if (sys.version_info.major == 3 and sys.version_info.minor > 5):
            expected_payload = {'values': [{'data': 'new100', 'index': 2, 'type': 'TEST100' }, {'data': 'new2', 'ttl': 86400, 'index': 2222, 'type': 'TEST2'}, {'data': 'new4', 'ttl': 86400, 'index': 4, 'type': 'TEST4'}, {'data': 'new101', 'index': 3, 'type': 'TEST101'}]}
            expected_payload.get('values', {})
            replace_timestamps(expected_payload)
            self.assertEqual(flattensort(passed_payload), flattensort(expected_payload),
                failure_message(expected=expected_payload,
                                 passed=passed_payload,
                                 methodname='modify_handle_value'))
        elif (sys.version_info.major == 2 and sys.version_info.minor > 6):
            expected_payload = {'values': [{'index': 2, 'type': 'TEST100', 'data': 'new100'}, {'index': 2222, 'ttl': 86400, 'type': 'TEST2', 'data': 'new2'}, {'index': 4, 'ttl': 86400, 'type': 'TEST4', 'data': 'new4'}, {'index': 3, 'type': 'TEST101', 'data': 'new101'}]}
            expected_payload.get('values', {})
            replace_timestamps(expected_payload)
            self.assertEqual(flattensort(passed_payload), flattensort(expected_payload),
                failure_message(expected=expected_payload,
                                 passed=passed_payload,
                                 methodname='modify_handle_value'))

    @mock.patch('pyhandle.handlesystemconnector.requests.Session.put')
    @mock.patch('pyhandle.handlesystemconnector.requests.Session.get')
    def test_modify_handle_value_HS_ADMIN(self, getpatch, putpatch):
        """Test exception when trying to modify HS_ADMIN."""

        # Define the replacement for the patched GET method:
        cont = {"responseCode":1, "handle":"my/testhandle", "values":[{"index":111, "type": "TEST1", "data":{"format":"string", "value":"val1"}, "ttl":86400, "timestamp":"2015-09-29T15:51:08Z"}, {"index":2222, "type": "TEST2", "data":{"format":"string", "value":"val2"}, "ttl":86400, "timestamp":"2015-09-29T15:51:08Z"}, {"index":333, "type": "TEST3", "data":{"format":"string", "value":"val3"}, "ttl":86400, "timestamp":"2015-09-29T15:51:08Z"}, {"index":4, "type": "TEST4", "data":{"format":"string", "value":"val4"}, "ttl":86400, "timestamp":"2015-09-29T15:51:08Z"}]}
        mock_response_get = MockResponse(status_code=200, content=json.dumps(cont))
        getpatch.return_value = mock_response_get

        # Define the replacement for the patched requests.delete method:
        mock_response_put = MockResponse()
        putpatch.return_value = mock_response_put

        # Test variables
        testhandle = 'my/testhandle'

        # Run the method to be tested and check exception:
        with self.assertRaises(IllegalOperationException):
                self.inst.modify_handle_value(testhandle, HS_ADMIN='please let me in!')


    # delete_handle_value:

    @mock.patch('pyhandle.handlesystemconnector.requests.Session.delete')
    @mock.patch('pyhandle.handlesystemconnector.requests.Session.get')
    def test_delete_handle_value_one_entry(self, getpatch, deletepatch):
        """Test deleting one entry from a record."""

        # Define the replacement for the patched GET method:
        cont = {"responseCode":1, "handle":"my/testhandle", "values":[{"index":111, "type": "TEST1", "data":{"format":"string", "value":"val1"}, "ttl":86400, "timestamp":"2015-09-30T15:08:49Z"}, {"index":2222, "type": "TEST2", "data":{"format":"string", "value":"val2"}, "ttl":86400, "timestamp":"2015-09-30T15:08:49Z"}, {"index":333, "type": "TEST2", "data":{"format":"string", "value":"val3"}, "ttl":86400, "timestamp":"2015-09-30T15:08:49Z"}, {"index":4, "type": "TEST4", "data":{"format":"string", "value":"val4"}, "ttl":86400, "timestamp":"2015-09-30T15:08:49Z"}]}
        mock_response_get = MockResponse(status_code=200, content=json.dumps(cont))
        getpatch.return_value = mock_response_get

        # Define the replacement for the patched requests.delete method:
        mock_response_del = MockResponse()
        deletepatch.return_value = mock_response_del

        # Call the method to be tested:
        self.inst.delete_handle_value('my/testhandle', 'TEST1')

        # Get the args passed to "requests.delete"
        # For help, please see: http://www.voidspace.org.uk/python/mock/examples.html#checking-multiple-calls-with-mock
        positional_args_passed_to_delete = deletepatch.call_args_list[len(deletepatch.call_args_list) - 1][0]
        passed_url = positional_args_passed_to_delete[0]

        # Compare with expected URL:
        self.assertIn('?index=111', passed_url,
            'The index 111 is not specified in the URL ' + passed_url + '. This is serious!')

    @mock.patch('pyhandle.handlesystemconnector.requests.Session.delete')
    @mock.patch('pyhandle.handlesystemconnector.requests.Session.get')
    def test_delete_handle_value_several_entries(self, getpatch, deletepatch):
        """Test deleting several entries from a record."""

        # Test variables
        testhandle = 'my/testhandle'

        # Define the replacement for the patched GET method:
        cont = {"responseCode":1, "handle":testhandle, "values":[{"index":111, "type": "TEST1", "data":{"format":"string", "value":"val1"}, "ttl":86400, "timestamp":"2015-09-30T15:08:49Z"}, {"index":2222, "type": "TEST2", "data":{"format":"string", "value":"val2"}, "ttl":86400, "timestamp":"2015-09-30T15:08:49Z"}, {"index":333, "type": "TEST2", "data":{"format":"string", "value":"val3"}, "ttl":86400, "timestamp":"2015-09-30T15:08:49Z"}, {"index":4, "type": "TEST4", "data":{"format":"string", "value":"val4"}, "ttl":86400, "timestamp":"2015-09-30T15:08:49Z"}]}
        mock_response_get = MockResponse(status_code=200, content=json.dumps(cont))
        getpatch.return_value = mock_response_get

        # Define the replacement for the patched requests.delete method:
        mock_response_del = MockResponse()
        deletepatch.return_value = mock_response_del

        # Call the method to be tested:
        self.inst.delete_handle_value(testhandle, ['TEST1', 'TEST2'])

        # Get the args passed to "requests.delete"
        # For help, please see: http://www.voidspace.org.uk/python/mock/examples.html#checking-multiple-calls-with-mock
        positional_args_passed_to_delete = deletepatch.call_args_list[len(deletepatch.call_args_list) - 1][0]
        passed_url = positional_args_passed_to_delete[0]

        # Compare with expected URL:
        self.assertIn('index=111', passed_url,
            'The index 111 is not specified in the URL ' + passed_url + '. This may be serious!')
        self.assertIn('index=222', passed_url,
            'The index 2222 is not specified in the URL ' + passed_url + '. This may be serious!')

    @mock.patch('pyhandle.handlesystemconnector.requests.Session.delete')
    @mock.patch('pyhandle.handlesystemconnector.requests.Session.get')
    def test_delete_handle_value_inexistent_entry(self, getpatch, deletepatch):
        """Test deleting one inexistent entry from a record."""

        # Test variables
        testhandle = 'my/testhandle'

        # Define the replacement for the patched GET method:
        cont = {"responseCode":1, "handle":testhandle, "values":[{"index":111, "type": "TEST1", "data":{"format":"string", "value":"val1"}, "ttl":86400, "timestamp":"2015-09-30T15:08:49Z"}, {"index":2222, "type": "TEST2", "data":{"format":"string", "value":"val2"}, "ttl":86400, "timestamp":"2015-09-30T15:08:49Z"}, {"index":333, "type": "TEST2", "data":{"format":"string", "value":"val3"}, "ttl":86400, "timestamp":"2015-09-30T15:08:49Z"}, {"index":4, "type": "TEST4", "data":{"format":"string", "value":"val4"}, "ttl":86400, "timestamp":"2015-09-30T15:08:49Z"}]}
        mock_response_get = MockResponse(status_code=200, content=json.dumps(cont))
        getpatch.return_value = mock_response_get

        # Define the replacement for the patched requests.delete method:
        mock_response_del = MockResponse()
        deletepatch.return_value = mock_response_del

        # Call the method to be tested:
        self.inst.delete_handle_value(testhandle, 'test100')

        # Check if PUT was called (PUT should not have been called):
        self.assertEqual(deletepatch.call_count, 0,
            'The method "requests.put" was called! (' + str(deletepatch.call_count) + ' times). It should NOT have been called.')

    @mock.patch('pyhandle.handlesystemconnector.requests.Session.delete')
    @mock.patch('pyhandle.handlesystemconnector.requests.Session.get')
    def test_delete_handle_value_several_entries_one_nonexistent(self, getpatch, deletepatch):
        """Test deleting several entries from a record, one of them does not exist."""

        # Test variables
        testhandle = 'my/testhandle'

        # Define the replacement for the patched GET method:
        cont = {"responseCode":1, "handle":testhandle, "values":[{"index":111, "type": "TEST1", "data":{"format":"string", "value":"val1"}, "ttl":86400, "timestamp":"2015-09-30T15:08:49Z"}, {"index":2222, "type": "TEST2", "data":{"format":"string", "value":"val2"}, "ttl":86400, "timestamp":"2015-09-30T15:08:49Z"}, {"index":333, "type": "TEST2", "data":{"format":"string", "value":"val3"}, "ttl":86400, "timestamp":"2015-09-30T15:08:49Z"}, {"index":4, "type": "TEST4", "data":{"format":"string", "value":"val4"}, "ttl":86400, "timestamp":"2015-09-30T15:08:49Z"}]}
        mock_response_get = MockResponse(status_code=200, content=json.dumps(cont))
        getpatch.return_value = mock_response_get

        # Define the replacement for the patched requests.delete method:
        mock_response_del = MockResponse()
        deletepatch.return_value = mock_response_del

        # Call the method to be tested:
        self.inst.delete_handle_value(testhandle, ['TEST1', 'TEST100'])

        # Get the args passed to "requests.delete"
        # For help, please see: http://www.voidspace.org.uk/python/mock/examples.html#checking-multiple-calls-with-mock
        positional_args_passed_to_delete = deletepatch.call_args_list[len(deletepatch.call_args_list) - 1][0]
        passed_url = positional_args_passed_to_delete[0]

        # Compare with expected URL:
        self.assertIn('index=111', passed_url,
            'The index 111 is not specified in the URL ' + passed_url + '. This may be serious!')
        self.assertNotIn('&index=', passed_url,
            'A second index was specified in the URL ' + passed_url + '. This may be serious!')

    @mock.patch('pyhandle.handlesystemconnector.requests.Session.delete')
    @mock.patch('pyhandle.handlesystemconnector.requests.Session.get')
    def test_delete_handle_value_several_occurrences(self, getpatch, deletepatch):
        """Test trying to delete from a corrupted handle record."""

        # Define the replacement for the patched GET method (getting a corrupted record):
        cont = {"responseCode":1, "handle":"my/testhandle", "values":[{"index":111, "type": "TEST1", "data":{"format":"string", "value":"val1"}, "ttl":86400, "timestamp":"2015-09-30T15:08:49Z"}, {"index":2222, "type": "TEST2", "data":{"format":"string", "value":"val2"}, "ttl":86400, "timestamp":"2015-09-30T15:08:49Z"}, {"index":333, "type": "TEST2", "data":{"format":"string", "value":"val3"}, "ttl":86400, "timestamp":"2015-09-30T15:08:49Z"}, {"index":4, "type": "TEST4", "data":{"format":"string", "value":"val4"}, "ttl":86400, "timestamp":"2015-09-30T15:08:49Z"}]}
        mock_response_get = MockResponse(status_code=200, content=json.dumps(cont))
        getpatch.return_value = mock_response_get

        # Define the replacement for the patched requests.delete method:
        mock_response_del = MockResponse()
        deletepatch.return_value = mock_response_del

        # Call the method to be tested:
        self.inst.delete_handle_value('my/testhandle', 'TEST2')

        # Get the args passed to "requests.delete"
        # For help, please see: http://www.voidspace.org.uk/python/mock/examples.html#checking-multiple-calls-with-mock
        positional_args_passed_to_delete = deletepatch.call_args_list[len(deletepatch.call_args_list) - 1][0]
        passed_url = positional_args_passed_to_delete[0]

        # Compare with expected URL:
        self.assertIn('index=2222', passed_url,
            'The index 2222 is not specified in the URL ' + passed_url + '. This may be serious!')
        self.assertIn('index=333', passed_url,
            'The index 333 is not specified in the URL ' + passed_url + '. This may be serious!')

        # Check if PUT was called once:
        self.assertEqual(deletepatch.call_count, 1,
            'The method "requests.put" was not called once, but ' + str(deletepatch.call_count) + ' times.')

    # delete_handle:

    @mock.patch('pyhandle.handlesystemconnector.requests.Session.delete')
    def test_delete_handle(self, deletepatch):

        # Define the replacement for the patched requests.delete method:
        mock_response_del = MockResponse(success=True)
        deletepatch.return_value = mock_response_del

        # Call method to be tested:
        self.inst.delete_handle('my/testhandle')

        # Get the args passed to "requests.delete"
        # For help, please see: http://www.voidspace.org.uk/python/mock/examples.html#checking-multiple-calls-with-mock
        positional_args_passed_to_delete = deletepatch.call_args_list[len(deletepatch.call_args_list) - 1][0]
        passed_url = positional_args_passed_to_delete[0]

        # Compare with expected URL:
        self.assertNotIn('index=', passed_url,
            'Indices were passed to the delete method.')

    @mock.patch('pyhandle.handlesystemconnector.requests.Session.delete')
    @mock.patch('pyhandle.handlesystemconnector.requests.Session.get')
    def test_delete_handle_inexistent(self, getpatch, deletepatch):

        # Define the replacement for the patched GET method:
        mock_response_get = MockResponse(notfound=True)
        getpatch.return_value = mock_response_get

        # Define the replacement for the patched requests.delete method:
        mock_response_del = MockResponse(notfound=True)
        deletepatch.return_value = mock_response_del

        # Call method to be tested, assert exception
        with self.assertRaises(HandleNotFoundException):
            resp = self.inst.delete_handle('my/testhandle')
            
    def test_delete_handle_too_many_args(self):

        # Call method to be tested:
        with self.assertRaises(TypeError):
            self.inst.delete_handle('my/testhandle', 'TEST1')


    @mock.patch('pyhandle.handlesystemconnector.requests.Session.put')
    @mock.patch('pyhandle.handlesystemconnector.requests.Session.get')
    def test_GenericHandleError(self, getpatch, putpatch):
        """Test causing a Generic Handle Exception.

        This should never happen, but this exception was designed for the
        really unexpected things, so to make sure it works, I invent a
        ver broken illegal action here.
        """

        # Define the replacement for the patched GET method:
        #cont = {"responseCode":1, "handle":"not/me", "values":[{"index":1, "type":"URL", "data":{"format":"string", "value":"www.url.foo"}, "ttl":86400, "timestamp":"2015-09-30T15:54:30Z"}, {"index":2, "type":"10320/LOC", "data":{"format":"string", "value":"<locations><location href = 'http://first.foo' /><location href = 'http://second.foo' /></locations> "}, "ttl":86400, "timestamp":"2015-09-30T15:54:30Z"}]}
        cont = {"responseCode":1, "handle":"not/me", "values":[{"index":1, "type":"URL", "data":{"format":"string", "value":"www.url.foo"}, "ttl":86400, "timestamp":"2015-09-30T15:54:30Z"}]}
        mock_response_get = MockResponse(status_code=200, content=json.dumps(cont))
        getpatch.return_value = mock_response_get

        # Define the replacement for the patched requests.put method:
        mock_response_put = MockResponse()
        putpatch.return_value = mock_response_put

        # Run the method to be tested:
        with self.assertRaises(GenericHandleError):
            self.inst.retrieve_handle_record_json('my/testhandle')

        # Check if the PUT request was sent exactly once:
        self.assertEqual(putpatch.call_count, 0,
            'The method "requests.put" was called ' + str(putpatch.call_count) + ' times. It should not have been called at all.')


        # search_handle

    @mock.patch('pyhandle.handlesystemconnector.requests.Session.get')
    @mock.patch('pyhandle.handlesystemconnector.HandleSystemConnector.check_if_username_exists')
    def test_search_handle_wrong_url(self, usernamepatch, getpatch):
        """Test exception when wrong search servlet URL is given."""

        # Define the replacement for the patched check_if_username_exists method:
        mock_response_user = MockResponse(success=True)
        usernamepatch.return_value = mock_response_user

        # Define the replacement for the patched GET method:
        mock_response_get = MockSearchResponse(wrong_url=True)
        getpatch.return_value = mock_response_get
        
        # Setup client for searching with existent but wrong url (google.com):
        inst = RESTHandleClient.instantiate_with_username_and_password(
            "url_https",
            "100:user/name",
            "password",
            reverselookup_baseuri='http://www.google.com',
            HTTP_verify=True)

        # Run code to be tested + check exception:
        with self.assertRaises(ReverseLookupException):
            self.inst.search_handle(URL='*')

    @mock.patch('pyhandle.handlesystemconnector.requests.Session.get')
    @mock.patch('pyhandle.handlesystemconnector.HandleSystemConnector.check_if_username_exists')
    def test_search_handle_handleurl(self, usernamepatch, getpatch):
        """Test exception when wrong search servlet URL (Handle Server REST API URL) is given."""

        # Define the replacement for the patched check_if_username_exists method:
        mock_response_user = MockResponse(success=True)
        usernamepatch.return_value = mock_response_user

        # Define the replacement for the patched GET method:
        mock_response_search = MockSearchResponse(handle_url=True)
        getpatch.return_value = mock_response_search

        # Setup client for searching with Handle Server url:
        inst = RESTHandleClient.instantiate_with_username_and_password(
            "url_https",
            "100:user/name",
            "password",
            reverselookup_url_extension='/api/handles/',
            HTTP_verify=True)

        # Run code to be tested + check exception:
        with self.assertRaises(ReverseLookupException):
            self.inst.search_handle(URL='*')

    @mock.patch('pyhandle.handlesystemconnector.requests.Session.get')
    def test_search_handle(self, getpatch):
        """Test searching for handles with any url (server should return list of handles)."""

        # Define the replacement for the patched GET method:
        mock_response_get = MockSearchResponse(success=True)
        getpatch.return_value = mock_response_get

        # Run code to be tested:
        val = self.inst.search_handle(URL='*')

        # Check desired outcome:
        self.assertEqual(type(val), type([]),
            '')
        self.assertTrue(len(val) > 0,
            '')
        self.assertTrue(check_handle_syntax(val[0]),
            '')

    @mock.patch('pyhandle.handlesystemconnector.requests.Session.get')
    def test_search_handle_emptylist(self, getpatch):
        """Test empty search result."""

        # Define the replacement for the patched GET method:
        mock_response_get = MockSearchResponse(empty=True)
        getpatch.return_value = mock_response_get

        # Run code to be tested:
        val = self.inst.search_handle(URL='noturldoesnotexist')

        # Check desired outcome:
        self.assertEqual(type(val), type([]),
            '')
        self.assertEqual(len(val), 0,
            '')

    @mock.patch('pyhandle.handlesystemconnector.requests.Session.get')
    def test_search_handle_for_url(self, getpatch):
        """Test searching for url with wildcards."""

        # Define the replacement for the patched GET method:
        mock_response_get = MockSearchResponse(success=True)
        getpatch.return_value = mock_response_get

        # Run code to be tested:
        val = self.inst.search_handle(URL='*dkrz*')

        # Check desired outcome:
        self.assertEqual(type(val), type([]),
            '')

        # Run code to be tested:
        val = self.inst.search_handle('*dkrz*')

        # Check desired outcome:
        self.assertEqual(type(val), type([]),
            '')

    if False:
        # At the moment, two keywords can not be searched!
        @mock.patch('pyhandle.handlesystemconnector.requests.Session.get')
        def test_search_handle_for_url_and_checksum(self, getpatch):
            """Test searching for url and checksum with wildcards."""

            # Define the replacement for the patched GET method:
            mock_response_get = MockSearchResponse(success=True)
            getpatch.return_value = mock_response_get

            # Run code to be tested:
            val = self.inst.search_handle('*dkrz*', CHECKSUM='*123*')

            # Check desired outcome:
            self.assertEqual(type(val), type([]),
                '')

            # Run code to be tested:
            val = self.inst.search_handle(URL='*dkrz*', CHECKSUM='*123*')

            # Check desired outcome:
            self.assertEqual(type(val), type([]),
                '')

    @mock.patch('pyhandle.handlesystemconnector.requests.Session.get')
    def test_search_handle_prefixfilter(self, getpatch):
        """Test filtering for prefixes."""

        prefix = "11111"

        # Define the replacement for the patched GET method:
        mock_response_get = MockSearchResponse(prefix=prefix)
        getpatch.return_value = mock_response_get

        # Run code to be tested:
        val = self.inst.search_handle(URL='*dkrz*', prefix=prefix)

        # Check desired outcome:
        self.assertEqual(type(val), type([]),
            '')
        for item in val:
            self.assertEqual(item.split('/')[0], prefix)

    @mock.patch('pyhandle.handlesystemconnector.requests.Session.get')
    def test_search_handle_prefixfilter_realprefix(self, getpatch):
        """Test filtering for prefixes."""

        prefix = "10876.test"

        # Define the replacement for the patched GET method:
        mock_response_get = MockSearchResponse(prefix=prefix)
        getpatch.return_value = mock_response_get

        # Run code to be tested:
        val = self.inst.search_handle(URL='*dkrz*', prefix=prefix)

        # Check desired outcome:
        self.assertEqual(type(val), type([]),
            '')
        for item in val:
            self.assertEqual(item.split('/')[0], prefix)

    @mock.patch('pyhandle.handlesystemconnector.requests.Session.get')
    def test_search_handle_fulltext(self, getpatch):
        """Test filtering for prefixes."""

        prefix = "10876.test"

        # Define the replacement for the patched GET method:
        mock_response_get = MockSearchResponse(prefix=prefix)
        getpatch.return_value = mock_response_get

        # Run code to be tested + check exception:
        with self.assertRaises(ReverseLookupException):
            self.inst.search_handle(URL='*dkrz*', searchterms=['foo', 'bar'])

