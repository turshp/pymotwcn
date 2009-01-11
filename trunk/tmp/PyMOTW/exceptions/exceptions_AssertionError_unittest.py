#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: exceptions_AssertionError_unittest.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import unittest

class AssertionExample(unittest.TestCase):
    
    def test(self):
        self.failUnless(False)

unittest.main()
