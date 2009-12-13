#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: dircache_reset.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import dircache

path = '/tmp'
first = dircache.listdir(path)
dircache.reset()
second = dircache.listdir(path)

print 'Identical :', first is second
print 'Equal     :', first == second
print 'Difference:', list(set(second) - set(first))
