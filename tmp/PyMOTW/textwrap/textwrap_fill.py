#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: textwrap_fill.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import textwrap
from textwrap_example import sample_text

print 'No dedent:\n'
print textwrap.fill(sample_text)
