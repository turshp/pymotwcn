#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: textwrap_fill_width.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import textwrap
from textwrap_example import sample_text

dedented_text = textwrap.dedent(sample_text).strip()
for width in [ 20, 60, 80 ]:
	print
	print '%d Columns:\n' % width
	print textwrap.fill(dedented_text, width=width)
