"""
This module provides some helper functions to ease porting the codebase
     to supported Python 3 versions.

"""


def check_response_content_type(response):
    if isinstance(response.content, str):
        return True


def decoded_response(response):
    if check_response_content_type(response):
        return response.content
    return response.content.decode("utf-8")


def set_encoding_variable():
    return "unicode"
