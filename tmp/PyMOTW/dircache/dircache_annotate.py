#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: dircache_annotate.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import dircache
from pprint import pprint

path = '../../trunk'

contents = dircache.listdir(path)

annotated = contents[:]
dircache.annotate(path, annotated)

fmt = '%20s\t%20s'

print fmt % ('ORIGINAL', 'ANNOTATED')
print fmt % (('-' * 20,)*2)

for o, a in zip(contents, annotated):
    print fmt % (o, a)
