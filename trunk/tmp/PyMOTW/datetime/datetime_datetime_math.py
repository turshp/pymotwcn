#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""Calculations with datetime values.
"""

__version__ = "$Id: datetime_datetime_math.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import datetime

today = datetime.datetime.today()
print 'Today    :', today

yesterday = today - datetime.timedelta(days=1)
print 'Yesterday:', yesterday

tomorrow = today + datetime.timedelta(days=1)
print 'Tomorrow :', tomorrow

print 'tomorrow - yesterday:', tomorrow - yesterday
print 'yesterday - tomorrow:', yesterday - tomorrow

print 'tomorrow > yesterday:', tomorrow > yesterday