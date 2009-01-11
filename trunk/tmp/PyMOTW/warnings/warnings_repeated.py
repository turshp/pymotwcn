#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: warnings_repeated.py 1882 2009-01-04 15:38:33Z dhellmann $"

import warnings

def function_with_warning():
    warnings.warn('This is a warning!')
    
function_with_warning()
function_with_warning()
function_with_warning()
