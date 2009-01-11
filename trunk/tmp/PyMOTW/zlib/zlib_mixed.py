#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: zlib_mixed.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import zlib

lorem = open('lorem.txt', 'rt').read()
compressed = zlib.compress(lorem)
combined = compressed + lorem

decompressor = zlib.decompressobj()
decompressed = decompressor.decompress(combined)

print 'Decompressed matches lorem:', decompressed == lorem
print 'Unused data matches lorem :', decompressor.unused_data == lorem
