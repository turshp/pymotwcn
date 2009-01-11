#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: EasyDialogs_ProgressBar_set.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import EasyDialogs
import time

meter = EasyDialogs.ProgressBar('Making progress...',
                                maxval=1000,
                                label='Starting',
                                )
for i in xrange(1, 1001, 123):
    msg = 'Bytes: %d' % i
    meter.label(msg)
    meter.set(i)
    time.sleep(1)
