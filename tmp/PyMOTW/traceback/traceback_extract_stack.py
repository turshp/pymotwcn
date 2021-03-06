#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: traceback_extract_stack.py 1882 2009-01-04 15:38:33Z dhellmann $"

import traceback
import sys
from pprint import pprint

from traceback_example import call_function

def f():
    return traceback.extract_stack()

stack = call_function(f)
pprint(stack)
