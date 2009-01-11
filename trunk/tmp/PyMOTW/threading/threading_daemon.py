#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""Daemon vs. non-daemon threads.
"""

__version__ = "$Id: threading_daemon.py 1882 2009-01-04 15:38:33Z dhellmann $"

import threading
import time

def daemon():
    print 'Starting:', threading.currentThread().getName()
    time.sleep(2)
    print 'Exiting :', threading.currentThread().getName()

d = threading.Thread(name='daemon', target=daemon)
d.setDaemon(True)

def non_daemon():
    print 'Starting:', threading.currentThread().getName()
    print 'Exiting :', threading.currentThread().getName()

t = threading.Thread(name='non-daemon', target=non_daemon)

d.start()
t.start()
