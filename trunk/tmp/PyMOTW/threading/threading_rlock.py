#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""Re-entrant locks
"""

__version__ = "$Id: threading_rlock.py 1882 2009-01-04 15:38:33Z dhellmann $"

import threading

lock = threading.RLock()

def first():
    print 'First try:', lock.acquire()
    second()
    
def second():
    print 'Second try:', lock.acquire(0)

first()
