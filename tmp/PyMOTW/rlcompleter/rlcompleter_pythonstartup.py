#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: rlcompleter_pythonstartup.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

try:
    import readline
except ImportError:
    # Silently ignore missing readline module
    pass
else:
    import rlcompleter
    readline.parse_and_bind("tab: complete")