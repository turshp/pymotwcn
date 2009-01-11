#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""Configuration file for Sphinx-generated documentation.
"""

import glob
import os

__version__ = "$Id: conf.py 1882 2009-01-04 15:38:33Z dhellmann $"

source_suffix = '.rst'

project = 'Python Module of the Week'
copyright = 'Doug Hellmann'

# Version information comes from the Makefile that calls sphinx-build.
version = '1.0'
release = version

html_title = 'Python Module of the Week'
html_short_title = 'PyMOTW'
html_additional_pages = {
    'index':'index.html',
    }
html_use_modindex = True

# The TEMPLATES variable is set by the Makefile before sphinx-build is called.
templates_path = ['../sphinx/mytemplates/',
                  ]

latex_documents = [
    ('pdf_contents', 'PyMOTW-%s.tex' % version, 
     'Python Module of the Week', 'Doug Hellmann', 'manual', False),
    ]

#latex_preamble = r'''
#'''
