#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: datetime_timedelta.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import datetime

print "microseconds:", datetime.timedelta(microseconds=1)
print "milliseconds:", datetime.timedelta(milliseconds=1)
print "seconds     :", datetime.timedelta(seconds=1)
print "minutes     :", datetime.timedelta(minutes=1)
print "hours       :", datetime.timedelta(hours=1)
print "days        :", datetime.timedelta(days=1)
print "weeks       :", datetime.timedelta(weeks=1)
