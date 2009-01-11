#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: webbrowser_get.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import webbrowser

b = webbrowser.get('lynx')
b.open('http://docs.python.org/lib/module-webbrowser.html')