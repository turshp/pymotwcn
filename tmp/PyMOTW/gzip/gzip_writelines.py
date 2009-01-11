#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: gzip_writelines.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import gzip
import itertools
import os

output = gzip.open('example_lines.txt.gz', 'wb')
try:
    output.writelines(itertools.repeat('The same line, over and over.\n', 10))
finally:
    output.close()

os.system('gzcat example_lines.txt.gz')
