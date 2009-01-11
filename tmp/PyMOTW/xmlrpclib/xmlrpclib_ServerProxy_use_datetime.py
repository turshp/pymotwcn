#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: xmlrpclib_ServerProxy_use_datetime.py 1882 2009-01-04 15:38:33Z dhellmann $"

import xmlrpclib

server = xmlrpclib.ServerProxy('http://localhost:9000', use_datetime=True)
now = server.now()
print 'With:', now, type(now), now.__class__.__name__

server = xmlrpclib.ServerProxy('http://localhost:9000', use_datetime=False)
now = server.now()
print 'Without:', now, type(now), now.__class__.__name__
