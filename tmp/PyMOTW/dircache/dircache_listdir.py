#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: dircache_listdir.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import dircache

path = '.'
first = dircache.listdir(path)
second = dircache.listdir(path)

print 'Contents :', first
print 'Identical:', first is second
print 'Equal    :', first == second