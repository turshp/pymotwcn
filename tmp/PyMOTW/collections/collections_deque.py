#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""Double-ended queue.
"""

__version__ = "$Id: collections_deque.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import collections

d = collections.deque('abcdefg')
print 'Deque:', d
print 'Length:', len(d)
print 'Left end:', d[0]
print 'Right end:', d[-1]

d.remove('c')
print 'remove(c):', d