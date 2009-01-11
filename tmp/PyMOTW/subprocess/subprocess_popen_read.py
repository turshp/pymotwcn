#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: subprocess_popen_read.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import subprocess

print '\nread:'
proc = subprocess.Popen('echo "to stdout"', 
                        shell=True, 
                        stdout=subprocess.PIPE,
                        )
stdout_value = proc.communicate()[0]
print '\tstdout:', repr(stdout_value)
