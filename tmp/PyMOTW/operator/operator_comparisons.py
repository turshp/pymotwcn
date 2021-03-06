#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: operator_comparisons.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

from operator import *

a = 1
b = 5.0

print 'a =', a
print 'b =', b
for func in (lt, le, eq, ne, ge, gt):
    print '%s(a, b):' % func.__name__, func(a, b)
