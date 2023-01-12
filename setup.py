import codecs
import os
import re
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class NoseTestCommand(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)

        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import nose

        test_script = os.path.join('pyhandle', 'tests', 'main_test_script.py')
        # See also nosetests section in setup.cfg
        nose.run_exit(argv=['nosetests', test_script])

# Set common test dependencies
test_dependencies = [
    'mock',
    'nose',
]


if sys.version_info < (2, 7):
    test_dependencies.append('argparse')
    test_dependencies.append('unittest2')
    # Workaround for atexit._run_exitfuncs error when invoking `test` with
    # older versions of Python
    try:
        import multiprocessing
    except ImportError:
        pass
    
here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    # Intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    return codecs.open(os.path.join(here, *parts), 'r').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

long_description=open('README.md').read()

setup(name='pyhandle',
      version=find_version("pyhandle", "__init__.py"),
      description=('Library for management of handles '),
      long_description=long_description,
      long_description_content_type='text/markdown',
      classifiers=[
          'Development Status :: 1 - Planning',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'License :: OSI Approved :: Apache Software License',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      keywords=['handles', 'PIDs'],   
      download_url='https://github.com/EUDAT-B2SAFE/PYHANDLE',
      license='Apache License 2.0',
      packages=find_packages(),
      zip_safe=False,
      install_requires=[
          'requests==2.27.1; python_version=="3.5.0"',
          'requests==2.28.1; python_version>="3.6.0"',
          'datetime',
          'future',
          'six',
          'pymysql==0.8.0 ; python_version < "2.8.0"',
          'pymysql==0.8.0 ; python_version < "3.11.0"'       
      ],
      tests_require=test_dependencies,
      python_requires='>=3.6, <3.11',
      cmdclass={'test': NoseTestCommand},
      include_package_data=True
)

