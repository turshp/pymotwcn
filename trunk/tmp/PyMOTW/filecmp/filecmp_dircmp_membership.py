#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: filecmp_dircmp_membership.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import filecmp

dc = filecmp.dircmp('example/dir1', 'example/dir2')
print 'Common:', dc.common
print 'Left  :', dc.left_only
print 'Right :', dc.right_only
