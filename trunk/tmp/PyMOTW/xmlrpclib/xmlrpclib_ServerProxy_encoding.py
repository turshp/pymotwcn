#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: xmlrpclib_ServerProxy_encoding.py 1882 2009-01-04 15:38:33Z dhellmann $"

import xmlrpclib

server = xmlrpclib.ServerProxy('http://localhost:9000', encoding='ISO-8859-1')
print 'Ping:', server.ping()
