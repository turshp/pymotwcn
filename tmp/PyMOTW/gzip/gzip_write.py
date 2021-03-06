#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: gzip_write.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import gzip
import os

output = gzip.open('example.txt.gz', 'wb')
try:
    output.write('Contents of the example file go here.\n')
finally:
    output.close()

os.system('ls -l example.txt.gz')
os.system('file example.txt.gz')
