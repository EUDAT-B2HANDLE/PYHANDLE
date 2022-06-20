#!/bin/bash
set -e

if [ "$1" = 'coverage' ]; then
  nosetests --with-xunit --xunit-testsuite-name=pyhandle --with-coverage --cover-erase --cover-package=pyhandle --cover-branches --cover-inclusive --cover-xml main_test_script.py
else
  exec "$@"
fi
