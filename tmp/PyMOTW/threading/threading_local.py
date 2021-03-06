#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""Keeping thread-local values
"""

__version__ = "$Id: threading_local.py 1882 2009-01-04 15:38:33Z dhellmann $"

import random
import threading

def show_value(data):
    print threading.currentThread().getName(), ': value=',
    try:
        print data.value
    except AttributeError:
        print 'No value yet'

def worker(data):
    show_value(data)
    data.value = random.randint(1, 100)
    show_value(data)

local_data = threading.local()
show_value(local_data)
local_data.value = 1000
show_value(local_data)

for i in range(2):
    t = threading.Thread(target=worker, args=(local_data,))
    t.start()
