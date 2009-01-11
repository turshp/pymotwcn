#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: string_template_defaultpattern.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import string

t = string.Template('$var')
print t.pattern.pattern
