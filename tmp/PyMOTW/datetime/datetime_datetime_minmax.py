#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""The range of valid datetime values.
"""

__version__ = "$Id: datetime_datetime_minmax.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import datetime

print 'Earliest  :', datetime.datetime.min
print 'Latest    :', datetime.datetime.max
print 'Resolution:', datetime.datetime.resolution
