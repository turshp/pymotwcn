#!/bin/sh
#
# $Id: with_os.sh 1882 2009-01-04 15:38:33Z dhellmann $
#
#end_pymotw_header

export PYTHONPATH=os_${1}
echo "PYTHONPATH=$PYTHONPATH"
echo

python pkgutil_os_specific.py
