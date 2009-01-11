#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: EasyDialogs_AskFileForOpen.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import EasyDialogs
import os

filename = EasyDialogs.AskFileForOpen(
    message='Select a Python source file',
    defaultLocation=os.getcwd(),
    wanted=unicode,
    )

print 'Selected:', filename