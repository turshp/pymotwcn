#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""Subclassing Thread to create your own thread types.
"""

__version__ = "$Id: threading_subclass.py 1882 2009-01-04 15:38:33Z dhellmann $"

import threading

class MyThread(threading.Thread):

    def run(self):
        print 'MyThread:', self.getName()
        return

for i in range(5):
    t = MyThread()
    t.start()
