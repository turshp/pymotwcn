#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""Manipulating the order of items in a deque.
"""

__version__ = "$Id: collections_deque_rotate.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import collections

d = collections.deque(xrange(10))
print 'Normal        :', d

d = collections.deque(xrange(10))
d.rotate(2)
print 'Right rotation:', d

d = collections.deque(xrange(10))
d.rotate(-2)
print 'Left rotation :', d
