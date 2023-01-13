__version__ = "1.2.1"
# The version as used in setup.py and docs/source/conf.py.

# IMPORTANT
# Please put no comment above the __version__ variable,
# as they would be printed in the help(pyhandle) output!
# (The first comment - empty or not - would be appended to
# the package name, the next non-empty comment would be
# printed as description).

from . import clientcredentials
from . import handleclient

# Make sure that a single "import pyhandle" allows the use of
# relevant submodules!
# See 
# https://github.com/psf/requests/blob/master/requests/__init__.py#L120
