#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: warnings_formatwarning.py 1882 2009-01-04 15:38:33Z dhellmann $"

import warnings

def warning_on_one_line(message, category, filename, lineno):
    return '%s:%s: %s:%s' % (filename, lineno, category.__name__, message)

warnings.warn('This is a warning message, before')
warnings.formatwarning = warning_on_one_line
warnings.warn('This is a warning message, after')
