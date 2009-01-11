#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""Simple MD5 generation.
"""

__version__ = "$Id: hashlib_md5.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import hashlib

from hashlib_data import lorem

h = hashlib.md5()
h.update(lorem)
print h.hexdigest()
