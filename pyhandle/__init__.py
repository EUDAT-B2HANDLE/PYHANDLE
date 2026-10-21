from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("pyhandle")
except PackageNotFoundError:
    __version__ = "0+unknown"

# IMPORTANT
# Please put no comment above the __version__ variable,
# as they would be printed in the help(pyhandle) output!
# (The first comment - empty or not - would be appended to
# the package name, the next non-empty comment would be
# printed as description).

from . import clientcredentials, handleclient
from .handleexceptions import (
    BrokenHandleRecordException,
    CredentialsFormatError,
    GenericHandleError,
    HandleAlreadyExistsException,
    HandleAuthenticationError,
    HandleNotFoundException,
    HandleSyntaxError,
    IllegalOperationException,
    PyhandleBaseException,
    ReverseLookupException,
)

__all__ = [
    "clientcredentials",
    "handleclient",
    "BrokenHandleRecordException",
    "CredentialsFormatError",
    "GenericHandleError",
    "HandleAlreadyExistsException",
    "HandleAuthenticationError",
    "HandleNotFoundException",
    "HandleSyntaxError",
    "IllegalOperationException",
    "PyhandleBaseException",
    "ReverseLookupException",
]

# Make sure that a single "import pyhandle" allows the use of
# relevant submodules!
# See
# https://github.com/psf/requests/blob/master/requests/__init__.py#L120
