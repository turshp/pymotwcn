#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: anydbm_intkeys.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import anydbm

db = anydbm.open('/tmp/example.db', 'w')
try:
    db[1] = 'one'
finally:
    db.close()