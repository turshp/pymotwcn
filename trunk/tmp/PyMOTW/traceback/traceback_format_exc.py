#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: traceback_format_exc.py 1882 2009-01-04 15:38:33Z dhellmann $"

import traceback
import sys

from traceback_example import produce_exception

try:
    produce_exception()
except Exception, err:
    print 'format_exc():'
    print traceback.format_exc()