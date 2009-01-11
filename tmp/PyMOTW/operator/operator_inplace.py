#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: operator_inplace.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

from operator import *

a = -1
b = 5.0
c = [ 1, 2, 3 ]
d = [ 'a', 'b', 'c']
print 'a =', a
print 'b =', b
print 'c =', c
print 'd =', d

print 'iadd(a, b):', iadd(a, b)
a = iadd(a, b)
print 'a = iadd(a, b) =>', a

print 'iconcat(c, d):', iconcat(c, d)
c = iconcat(c, d)
print 'c = iconcat(c, d) =>', c