#!/bin/bash
set -e

if [ "$1" = 'coverage' ]; then
  pytest  --cov-report xml:coverage.xml --cov=pyhandle main_test_script.py
else
  exec "$@"
fi
