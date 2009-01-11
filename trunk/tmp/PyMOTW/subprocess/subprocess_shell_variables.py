#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: subprocess_shell_variables.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import subprocess

# Command with shell expansion
subprocess.call('ls -l $HOME', shell=True)
