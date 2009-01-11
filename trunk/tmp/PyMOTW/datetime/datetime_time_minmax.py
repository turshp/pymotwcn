#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""Valid range of time values.
"""

__version__ = "$Id: datetime_time_minmax.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import datetime

print 'Earliest  :', datetime.time.min
print 'Latest    :', datetime.time.max
print 'Resolution:', datetime.time.resolution