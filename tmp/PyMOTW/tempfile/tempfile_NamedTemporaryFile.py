#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: tempfile_NamedTemporaryFile.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import os
import tempfile

temp = tempfile.NamedTemporaryFile()
try:
    print 'temp:', temp
    print 'temp.name:', temp.name
finally:
    # Automatically cleans up the file
    temp.close()
print 'Exists after close:', os.path.exists(temp.name)