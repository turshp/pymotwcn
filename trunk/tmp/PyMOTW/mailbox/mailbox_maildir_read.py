#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: mailbox_maildir_read.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import mailbox

mbox = mailbox.Maildir('Example')
for message in mbox:
    print message['subject']
