#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""Force a case-sensitive test of a filename with a pattern.
"""

__version__ = "$Id: fnmatch_fnmatchcase.py 1882 2009-01-04 15:38:33Z dhellmann $"

import fnmatch
import os

pattern = 'FNMATCH_*.PY'
print 'Pattern :', pattern
print

files = os.listdir('.')

for name in files:
    print 'Filename: %-25s %s' % (name, fnmatch.fnmatchcase(name, pattern))
