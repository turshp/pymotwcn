#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: warnings_filterwarnings_module.py 1882 2009-01-04 15:38:33Z dhellmann $"

import warnings

warnings.filterwarnings('ignore', 
                        '.*', 
                        UserWarning,
                        'warnings_filtering',
                        )

import warnings_filtering
