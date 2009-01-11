#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: base64_urlsafe.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import base64

for original in [ chr(251) + chr(239), chr(255) * 2 ]:
    print 'Original         :', repr(original)
    print 'Standard encoding:', base64.standard_b64encode(original)
    print 'URL-safe encoding:', base64.urlsafe_b64encode(original)
    print
