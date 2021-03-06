#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: Cookie_coded_value.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import Cookie

c = Cookie.SimpleCookie()
c['integer'] = 5
c['string_with_quotes'] = 'He said, "Hello, World!"'

for name in ['integer', 'string_with_quotes']:
    print c[name].key
    print '  %s' % c[name]
    print '  value=%s' % c[name].value, type(c[name].value)
    print '  coded_value=%s' % c[name].coded_value
    print
