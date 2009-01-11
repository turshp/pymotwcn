#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""Expand tilde in filenames.
"""

__version__ = "$Id: ospath_expanduser.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import os.path

for user in [ '', 'dhellmann', 'postgres' ]:
    lookup = '~' + user
    print lookup, ':', os.path.expanduser(lookup)
