#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: exceptions_AttributeError_assignment.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

class MyClass(object):
    
    @property
    def attribute(self):
        return 'This is the attribute value'

o = MyClass()
print o.attribute
o.attribute = 'New value'
