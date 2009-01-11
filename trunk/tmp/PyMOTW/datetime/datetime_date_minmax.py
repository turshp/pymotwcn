#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""Minimum and maximum values for dates.
"""

__version__ = "$Id: datetime_date_minmax.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import datetime

print 'Earliest  :', datetime.date.min
print 'Latest    :', datetime.date.max
print 'Resolution:', datetime.date.resolution