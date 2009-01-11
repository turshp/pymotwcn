#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""Initializing a defaultdict.
"""

__version__ = "$Id: collections_defaultdict.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import collections

def default_factory():
    return 'default value'

d = collections.defaultdict(default_factory, foo='bar')
print d
print d['foo']
print d['bar']
