import logging
import os
import collections
import operator
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
    # TODO: The whole function does not sort anything, as "sorted" returns
    # a new list instead of modifying the existing one. So the sorted version
    # vanishes in neverland... nowhereland. And the function returns None.
    # Which, when compared, is... None. Yay. All tests pass.
    msg = 'This sort function returns false positive when comparing sorted test results.'
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
