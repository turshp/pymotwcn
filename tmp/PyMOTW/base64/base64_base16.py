#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: base64_base16.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import base64

original_string = 'This is the data, in the clear.'
print 'Original:', original_string

encoded_string = base64.b16encode(original_string)
print 'Encoded :', encoded_string

decoded_string = base64.b16decode(encoded_string)
print 'Decoded :', decoded_string
