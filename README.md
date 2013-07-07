json_parser
===========

A pure python JSON parser using generators/coroutines.

***Please note that this is not complete.***

Requirements
-----------

The latest Python 2.7, might work in Python 3...

Usage
-----

Usage is identical to the standard simplejson parsing:

>>> from parse import loads
>>> loads('{"key":"value"}')
{"key":"value"}

Running tests
-------------

>>> python test.py