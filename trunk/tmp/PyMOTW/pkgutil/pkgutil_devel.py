#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: pkgutil_devel.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import demopkg2
print 'demopkg2:', demopkg2.__file__

import demopkg2.overloaded
print 'demopkg2.overloaded:', demopkg2.overloaded.__file__

print
demopkg2.overloaded.func()