#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""Removing items from a deque.
"""

__version__ = "$Id: collections_deque_consuming.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import collections

print 'From the right:'
d = collections.deque('abcdefg')
while True:
    try:
        print d.pop()
    except IndexError:
        break

print 'From the left:'
d = collections.deque('abcdefg')
while True:
    try:
        print d.popleft()
    except IndexError:
        break
