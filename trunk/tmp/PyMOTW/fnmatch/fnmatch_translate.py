#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""Translate a glob-style pattern to a regular expression.
"""

__version__ = "$Id: fnmatch_translate.py 1882 2009-01-04 15:38:33Z dhellmann $"

import fnmatch

pattern = 'fnmatch_*.py'
print 'Pattern :', pattern
print 'Regex   :', fnmatch.translate(pattern)