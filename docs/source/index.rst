.. PYHANDLE documentation master file, created by
   sphinx-quickstart on Wed May 24 15:25:24 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


Welcome to PYHANDLE's documentation!
====================================

PyHandle is a Python client library for interaction with a `Handle System <http://www.handle.net/>`_ server, providing basic create, read, update and delete capabilities for Handles.
The library offers both a client for the HTTP REST interface and a client that interacts directly with a Handle server SQL back-end.

.. important::
   In order to perform operations on Handles it is mandatory to select which client you want to work with.
   There are currently two interfaces to interact with Handle System server: The REST interface and the native (SQL)
   database (see :doc:`pyhandleclient`).



Contents:

.. toctree::
   :maxdepth: 2

   pyhandleclient
   pyhandleclientrest
   pyhandleclientdb

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
