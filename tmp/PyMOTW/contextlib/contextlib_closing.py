#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
$Id: contextlib_closing.py 1882 2009-01-04 15:38:33Z dhellmann $
"""
#end_pymotw_header

from __future__ import with_statement

import contextlib

class Door(object):
    def __init__(self):
        print '  __init__()'
    def close(self):
        print '  close()'

print 'Normal Example:'
with contextlib.closing(Door()) as door:
    print '  inside with statement'

print
print 'Error handling example:'
try:
    with contextlib.closing(Door()) as door:
        print '  raising from inside with statement'
        raise RuntimeError('error message')
except Exception, err:
    print '  Had an error:', err

