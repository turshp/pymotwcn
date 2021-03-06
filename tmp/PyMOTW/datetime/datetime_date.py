#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""Some basic date() methods and attributes.
"""

__version__ = "$Id: datetime_date.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import datetime

today = datetime.date.today()
print today
print 'ctime:', today.ctime()
print 'tuple:', today.timetuple()
print 'ordinal:', today.toordinal()
print 'Year:', today.year
print 'Mon :', today.month
print 'Day :', today.day
