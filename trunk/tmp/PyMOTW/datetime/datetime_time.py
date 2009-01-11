#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""Basic features of time objects.
"""

__version__ = "$Id: datetime_time.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import datetime

t = datetime.time(1, 2, 3)
print t
print 'hour  :', t.hour
print 'minute:', t.minute
print 'second:', t.second
print 'microsecond:', t.microsecond
print 'tzinfo:', t.tzinfo