#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""Find the prefix string common to a group of paths.
"""

__version__ = "$Id: ospath_commonprefix.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import os.path

paths = ['/one/two/three/four',
         '/one/two/threefold',
         '/one/two/three/',
         ]
print paths
print os.path.commonprefix(paths)