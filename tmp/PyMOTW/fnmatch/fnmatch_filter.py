#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""Filter a list of filenames against a pattern.
"""

__version__ = "$Id: fnmatch_filter.py 1882 2009-01-04 15:38:33Z dhellmann $"

import fnmatch
import os

pattern = 'fnmatch_*.py'
print 'Pattern :', pattern

files = os.listdir('.')
print 'Files   :', files

print 'Matches :', fnmatch.filter(files, pattern)
