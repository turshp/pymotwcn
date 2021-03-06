#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: signal_signal.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import signal
import os
import time

def receive_signal(signum, stack):
    print 'Received:', signum

signal.signal(signal.SIGUSR1, receive_signal)
signal.signal(signal.SIGUSR2, receive_signal)

print 'My PID is:', os.getpid()

while True:
    print 'Waiting...'
    time.sleep(3)
