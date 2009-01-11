#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: warnings_warn_stacklevel.py 1882 2009-01-04 15:38:33Z dhellmann $"

import warnings

def old_function():
    warnings.warn(
        'old_function() is deprecated, use new_function() instead', 
        stacklevel=2)

def caller_of_old_function():
    old_function()
    
caller_of_old_function()
