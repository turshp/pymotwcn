#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: SimpleXMLRPCServer_instance_with_prefix_client.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import xmlrpclib

proxy = xmlrpclib.ServerProxy('http://localhost:9000')
print 'public():', proxy.prefix.public()
try:
    print 'private():', proxy.prefix.private()
except Exception, err:
    print 'ERROR:', err
try:
    print 'public() without prefix:', proxy.public()
except Exception, err:
    print 'ERROR:', err

