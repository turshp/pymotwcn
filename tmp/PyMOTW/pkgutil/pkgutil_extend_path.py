#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: pkgutil_extend_path.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import demopkg1
print 'demopkg1:', demopkg1.__file__

try:
    import demopkg1.shared
except Exception, err:
    print 'demopkg1.shared: Not found (%s)' % err
else:
    print 'demopkg1.shared:', demopkg1.shared.__file__

try:
    import demopkg1.not_shared
except Exception, err:
    print 'demopkg1.not_shared: Not found (%s)' % err
else:
    print 'demopkg1.not_shared:', demopkg1.not_shared.__file__
