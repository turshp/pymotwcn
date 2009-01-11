#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: mailbox_mbox_remove.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import mailbox

mbox = mailbox.mbox('example.mbox')
to_remove = []
for key, msg in mbox.iteritems():
    if '2' in msg['subject']:
        print 'Removing:', key
        to_remove.append(key)
mbox.lock()
try:
    for key in to_remove:
        mbox.remove(key)
finally:
    mbox.flush()
    mbox.close()

print open('example.mbox', 'r').read()