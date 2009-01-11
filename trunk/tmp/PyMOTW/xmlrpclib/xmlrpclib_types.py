#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: xmlrpclib_types.py 1882 2009-01-04 15:38:33Z dhellmann $"

import xmlrpclib
import datetime

server = xmlrpclib.ServerProxy('http://localhost:9000')

for t, v in [ ('boolean', True), 
              ('integer', 1),
              ('floating-point number', 2.5),
              ('string', 'some text'), 
              ('datetime', datetime.datetime.now()),
              ('array', ['a', 'list']),
              ('array', ('a', 'tuple')),
              ('structure', {'a':'dictionary'}),
            ]:
    print '%-22s:' % t, server.show_type(v)
