#!/bin/bash
set -e

if [ "$1" = 'coverage' ]; then
  pytest -k 'not RESTHandleClientReadaccessTestCase and not  RESTHandleClientWriteaccessTestCase and not RESTTHandleClientSearchTestCase' --cov-report xml:coverage.xml --cov=pyhandle
else
  exec "$@"
fi
