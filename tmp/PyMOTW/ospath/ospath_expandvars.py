#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""Expand shell variables in filenames.
"""

__version__ = "$Id: ospath_expandvars.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import os.path
import os

os.environ['MYVAR'] = 'VALUE'

print os.path.expandvars('/path/to/$MYVAR')
