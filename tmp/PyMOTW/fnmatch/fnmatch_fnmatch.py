#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""Test an individual filename with a pattern.
"""

__version__ = "$Id: fnmatch_fnmatch.py 1882 2009-01-04 15:38:33Z dhellmann $"

import fnmatch
import os

pattern = 'fnmatch_*.py'
print 'Pattern :', pattern
print

files = os.listdir('.')
for name in files:
    print 'Filename: %-25s %s' % (name, fnmatch.fnmatch(name, pattern))