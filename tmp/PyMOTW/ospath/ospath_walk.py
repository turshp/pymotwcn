#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""Traverse a directory tree.
"""

__version__ = "$Id: ospath_walk.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import os.path
import pprint

def visit(arg, dirname, names):
    print dirname, arg
    for name in names:
        subname = os.path.join(dirname, name)
        if os.path.isdir(subname):
            print '  %s/' % name
        else:
            print '  %s' % name
    # Do not recurse into .svn directory
    if '.svn' in names:
        names.remove('.svn')
    print

os.path.walk('..', visit, '(User data)')