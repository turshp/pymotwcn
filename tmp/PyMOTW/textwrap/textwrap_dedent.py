#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: textwrap_dedent.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import textwrap
from textwrap_example import sample_text

dedented_text = textwrap.dedent(sample_text).strip()
print 'Dedented:\n'
print dedented_text
