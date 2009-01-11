#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: imaplib_status.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import imaplib
import re

from imaplib_connect import open_connection
from imaplib_list_parse import parse_list_response

if __name__ == '__main__':
    c = open_connection()
    try:
        typ, data = c.list()
        for line in data:
            flags, delimiter, mailbox_name = parse_list_response(line)
            print c.status(mailbox_name, '(MESSAGES RECENT UIDNEXT UIDVALIDITY UNSEEN)')
    finally:
        c.logout()
        
