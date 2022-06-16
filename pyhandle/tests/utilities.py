import logging
import os
import collections
import operator
import copy
from functools import cmp_to_key
from future.utils import viewitems
class NullHandler(logging.Handler):
    """
    For backward-compatibility with Python 2.6, a local class definition
    is used instead of logging.NullHandler
    """

    def emit(self, record):
        pass

REQUESTLOGGER = logging.getLogger('log_all_requests_of_testcases_to_file')
REQUESTLOGGER.addHandler(NullHandler())

def failure_message(expected, passed, methodname):
    msg = 'The PUT request payload that the method "' + methodname + '" assembled differs from the expected. This does not necessarily mean that it is wrong, it might just be a different way to talking to the Handle Server. Please run an integration test to check this and update the exptected PUT request accordingly.\nCreated:  ' + str(passed) + '\nExpected: ' + str(expected)
    return msg

def replace_timestamps(jsonobject):
    ''' Replace timestamp values by "xxx" because their values do not matter.'''

    # Replace:
    if type(jsonobject) == type({}):
        if 'timestamp' in jsonobject:
            jsonobject['timestamp'] = 'xxx'

    # Recursion:
    if type(jsonobject) == type({'b':2}):
        for item in jsonobject.items():
            replace_timestamps(item)

    elif type(jsonobject) == type([2, 2]) or type(jsonobject) == type((2, 2)):
        for item in jsonobject:
            replace_timestamps(item)

def log_new_case(name):
    REQUESTLOGGER.info('\n' + 60 * '*' + '\n*** ' + name + '\n' + 60 * '*' + '\n')

def log_request_response_to_file(op, handle, url, head, veri, resp, payload=None):

    space = '\n   '
    message = ''
    message += op + ' ' + handle
    message += space + 'URL:          ' + url
    message += space + 'HEADERS:      ' + str(head)
    message += space + 'VERIFY:       ' + str(veri)
    if payload is not None:
        message += space + 'PAYLOAD:' + space + str(payload)
    message += space + 'RESPONSECODE: ' + str(resp.status_code)
    message += space + 'RESPONSE:' + space + str(resp.content)
    REQUESTLOGGER.info(message)

def log_start_test_code():
    REQUESTLOGGER.info('--->')

def log_end_test_code():
    REQUESTLOGGER.info('---<')

def sort_lists(jsonobject):
    '''
    Deprecated!
    '''
    # DEPRECATED!!!
    #
    # TODO: The whole function does not sort anything, as "sorted" returns
    # a new list instead of modifying the existing one. So the sorted version
    # vanishes in neverland... nowhereland. And the function returns None.
    # Which, when compared, is... None. Yay. All tests pass.
    msg = 'This sort function returns false positive when comparing sorted test results.'
    msg += 'Use flattensort() instead.'
    raise ValueError(msg)

    # Sort:
    if type(jsonobject) == type([]):
        sorted(jsonobject, key=lambda x:sorted(x.keys()))
        # Python 2.6.6:
        # sorted(iterable, cmp=None, key=None, reverse=False) --> new sorted list
        # Python 3.7.1:
        # Return a new list containing all items from the iterable in ascending order.
        # A custom key function can be supplied to customize the sort order, and the
        # reverse flag can be set to request the result in descending order.


    # Recursion:
    if type(jsonobject) == type({'b':2}):
        for item in jsonobject.items():
            sort_lists(item)

    elif type(jsonobject) == type([2, 2]) or type(jsonobject) == type((2, 2)):
        # TODO Isn't the first comparison bullshit, as lists are caught above?
        for item in jsonobject:
            sort_lists(item)

def flattensort(jsonobject):
    '''
    Take a complex object (JSON object: nested dicts and lists of
    any depth) and flatten and sort it.
    
    This is done recursively: The leaves are being sorted flattened
    first. Then we go up and sort and flatten each level.

    Purpose: Compare JSON objects in unit tests, where the order of
    the objects does not matter, and they can be quite deeply nested.

    Test using these:

# These are the same, just differently sorted:
x = {"values": [{"index": 100, "type": "HS_ADMIN", "data": {"value": {"permissions": "011111110011", "index": "200", "handle": "0.NA/my"}, "format": "admin"}}, {"index": 1, "type": "URL", "data": "http://foo.bar"}, {"index": 2, "type": "CHECKSUM", "data": "123456"}, {"index": 4, "type": "BAR", "data": "bar"}, {"index": 3, "type": "FOO", "data": "foo"}, {"index": 5, "type": "10320/LOC", "data": "<locations><location href=\"http://bar.bar\" id=\"0\" /><location href=\"http://foo.foo\" id=\"1\" /></locations>"}]}
y = {"values": [{"type": "HS_ADMIN", "index": 100, "data": {"value": {"index": "200", "handle": "0.NA/my", "permissions": "011111110011"}, "format": "admin"}}, {"index": 1, "type": "URL", "data": "http://foo.bar"}, {"index": 2, "type": "CHECKSUM", "data": "123456"}, {"index": 3, "type": "FOO", "data": "foo"}, {"index": 4, "type": "BAR", "data": "bar"}, {"index": 5, "type": "10320/LOC", "data": "<locations><location href=\"http://bar.bar\" id=\"0\" /><location href=\"http://foo.foo\" id=\"1\" /></locations>"}]}

# These are actually different:
x = {'values': [{'index': 100, 'type': 'HS_ADMIN', 'data': {'value': {'index': '200', 'handle': '0.NA/my', 'permissions': '011111110011'}, 'format': 'admin'}}, {'index': 2, 'type': 'FOO', 'data': 'foo'}, {'index': 3, 'type': 'BAR', 'data': 'bar'}, {'index': 1, 'type': 'URL', 'data': 'http://foo.bar'}, {'index': 4, 'type': 'CHECKSUM', 'data': '123456'}]}
y = {'values': [{'index': 100, 'type': 'HS_ADMIN', 'data': {'value': {'index': '200', 'handle': '0.NA/my', 'permissions': '011111110011'}, 'format': 'admin'}}, {'index': 1, 'type': 'URL', 'data': 'http://foo.bar'}, {'index': 2, 'type': 'CHECKSUM', 'data': '123456'}, {'index': 3, 'type': 'FOO', 'data': 'foo'}, {'index': 4, 'type': 'BAR', 'data': 'bar'}, {'index': 5, 'type': '10320/LOC', 'data': '<locations><location href="http://bar.bar" id="0" /><location href="http://foo.foo" id="1" /></locations>'}]}

print('x==x:   %s' % (x==x))
print('y==y:   %s' % (y==y))
print('x==y:   %s' % (x==y))
print('rx==ry: %s' % (flattensort(x)==flattensort(y)))

    '''

    # Sorting a leave (end of recursion):
    # If it is a shallow, simple list, we can use sort().

    if type(jsonobject) == type([]):


        res = copy.deepcopy(jsonobject)
        # Why? The sort() can alter the list before failing, so
        # we must operate on a deep-copy.

        try:
            res.sort()
            # We make it a string so that the deep lists become flat lists and
            # can be sorted eventually. Otherwise we'd sort all the leaves, but
            # still could not sort the higher levels.
            res = ','.join(res)
            res = '['+res+']'
            return res

        except TypeError as e:
            # Not a shallow list, or items have uncomparable types.
            pass

        # Shallow list of various types: Recursion
        res = []
        shallow = True
        for item in jsonobject:
            
            if isinstance(item, list) or isinstance(item, tuple) or isinstance(item, dict):
                shallow = False
                res = None
                break
            else:
                res.append(str(item))
        
        if shallow:
            res.sort()
            res = ','.join(res)
            res = '['+res+']'
            return res


        # Deep list: Recursion
        res = []
        for item in jsonobject:
            item = flattensort(item)
            res.append(item)
        # The deep list's entries were now all flattened, so we
        # can and must sort them (then flatten):
        res.sort()
        res = ','.join(res)
        res = '['+res+']'
        return res

    # Dictionary: Recursion
    if type(jsonobject) == type({'b':2}):
        res = []
        for item in jsonobject.items():
            item = flattensort(item)
            res.append(item)
        # The dictionary's entries were now all flattened, so we
        # can and must sort them (then flatten):
        res.sort()
        res = ','.join(res)
        res = '{'+res+'}'
        return res

    # Tuples: Recursion
    elif type(jsonobject) == type((2, 2)):
        
        if not len(jsonobject) == 2:
            raise ValueError('Tuple of length %s, expected 2!')
        
        # Here, tuples are dictionary entries, kv pairs, so we don't
        # need to sort them but just flatten them to string:
        tup1 = flattensort(jsonobject[0])
        tup2 = flattensort(jsonobject[1])
        res = tup1+':'+tup2
        return res

    # Simple types: Just return
    try:
        if isinstance(jsonobject, basestring):
            return '"'+jsonobject+'"'
    except NameError:
        if isinstance(jsonobject, str):
            return '"'+jsonobject+'"'

    return str(jsonobject)