#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: imp_find_module_error.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import imp

try:
    imp.find_module('no_such_module')
except ImportError, err:
    print 'ImportError:', err

