#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: string_capwords.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import string

s = 'The quick brown fox jumped over the lazy dog.'

print s
print string.capwords(s)