#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: SimpleXMLRPCServer_dotted_name_client.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import xmlrpclib

proxy = xmlrpclib.ServerProxy('http://localhost:9000')
print 'BEFORE       :', 'EXAMPLE' in proxy.dir.list('/tmp')
print 'CREATE       :', proxy.dir.create('/tmp/EXAMPLE')
print 'SHOULD EXIST :', 'EXAMPLE' in proxy.dir.list('/tmp')
print 'REMOVE       :', proxy.dir.remove('/tmp/EXAMPLE')
print 'AFTER        :', 'EXAMPLE' in proxy.dir.list('/tmp')