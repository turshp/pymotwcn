#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""Combine path components to create a single path.
"""

__version__ = "$Id: ospath_join.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import os.path

for parts in [ ('one', 'two', 'three'),
               ('/', 'one', 'two', 'three'),
               ('/one', '/two', '/three'),
               ]:
    print parts, ':', os.path.join(*parts)
