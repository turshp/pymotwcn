=======
zipfile
=======
.. module:: zipfile
    :synopsis: Read and write ZIP archive files.

:Module: zipfile
:Purpose: Read and write ZIP archive files.
:Python Version: 1.6 and later
:Abstract:

    The zipfile module can be used to manipulate ZIP archive files. 

Limitations
===========

The zipfile module does not support ZIP files with appended comments, or
multi-disk ZIP files. It does support ZIP files larger than 4 GB that use the
ZIP64 extensions.

Testing ZIP Files
=================

The is_zipfile() function returns a boolean indicating whether or not the
filename passed as an argument refers to a valid ZIP file.

::

    import zipfile

    for filename in [ 'README.txt', 'example.zip', 
                      'bad_example.zip', 'notthere.zip' ]:
        print '%20s  %s' % (filename, zipfile.is_zipfile(filename))

Notice that if the file does not exist, is_zipfile() returns False.

::

    $ python zipfile_is_zipfile.py 
              README.txt  False
             example.zip  True
         bad_example.zip  False
            notthere.zip  False

Reading Meta-data from a ZIP Archive
====================================

Use the ZipFile class to work directly with a ZIP archive. It supports methods
for reading data about existing archives as well as modifying the archives by
adding additional files.

To read the names of the files in an existing archive, use namelist():

::

    import zipfile

    zf = zipfile.ZipFile('example.zip', 'r')
    print zf.namelist()

The return value is a list of strings with the names of the archive contents:

::

    $ python zipfile_namelist.py 
    ['README.txt']

The list of names is only part of the information available from the archive,
though. To access all of the meta-data about the ZIP contents, use the
infolist() or getinfo() methods.

::

    import datetime
    import zipfile

    def print_info(archive_name):
        zf = zipfile.ZipFile(archive_name)
        for info in zf.infolist():
            print info.filename
            print '\tComment:\t', info.comment
            print '\tModified:\t', datetime.datetime(*info.date_time)
            print '\tSystem:\t\t', info.create_system, '(0 = Windows, 3 = Unix)'
            print '\tZIP version:\t', info.create_version
            print '\tCompressed:\t', info.compress_size, 'bytes'
            print '\tUncompressed:\t', info.file_size, 'bytes'
            print

    if __name__ == '__main__':
        print_info('example.zip')

There are additional fields other than those printed here, but deciphering the
values into anything useful requires careful reading of the PKZIP Application
Note with the ZIP file specification.

::

    $ python zipfile_infolist.py 
    README.txt
            Comment:
            Modified:       2007-12-16 10:08:52
            System:         3 (0 = Windows, 3 = Unix)
            ZIP version:    23
            Compressed:     63 bytes
            Uncompressed:   75 bytes

If you know in advance the name of the archive member, you can retrieve its
ZipInfo object with getinfo().

::

    import zipfile

    zf = zipfile.ZipFile('example.zip')
    for filename in [ 'README.txt', 'notthere.txt' ]:
        try:
            info = zf.getinfo(filename)
        except KeyError:
            print 'ERROR: Did not find %s in zip file' % filename
        else:
            print '%s is %d bytes' % (info.filename, info.file_size)

If the archive member is not present, getinfo() raises a KeyError.

::

    $ python zipfile_getinfo.py 
    README.txt is 75 bytes
    ERROR: Did not find notthere.txt in zip file

Extracting Archived Files From a ZIP Archive
============================================

To access the data from an archive member, use the read() method, passing the
member's name.

::

    import zipfile

    zf = zipfile.ZipFile('example.zip')
    for filename in [ 'README.txt', 'notthere.txt' ]:
        try:
            data = zf.read(filename)
        except KeyError:
            print 'ERROR: Did not find %s in zip file' % filename
        else:
            print filename, ':'
            print repr(data)
        print

The data is automatically decompressed for you, if necessary.

::

    $ python zipfile_read.py 
    README.txt :
    'The examples for the zipfile module use this file and example.zip as data.\n'

    ERROR: Did not find notthere.txt in zip file

Creating New Archives
=====================

To create a new archive, simple instantiate the ZipFile with a mode of 'w'.
Any existing file is truncated and a new archive is started. To add files, use
the write() method.

::

    __version__ = "$Id: index.rst 1882 2009-01-04 15:38:33Z dhellmann $"

    from zipfile_infolist import print_info
    import zipfile

    print 'creating archive'
    zf = zipfile.ZipFile('zipfile_write.zip', mode='w')
    try:
        print 'adding README.txt'
        zf.write('README.txt')
    finally:
        print 'closing'
        zf.close()

    print
    print_info('zipfile_write.zip')

By default, the contents of the archive are not compressed:

::

    $ python zipfile_write.py
    creating archive
    adding README.txt
    closing

    README.txt
            Comment:
            Modified:       2007-12-16 10:08:50
            System:         3 (0 = Windows, 3 = Unix)
            ZIP version:    20
            Compressed:     75 bytes
            Uncompressed:   75 bytes

To add compression, the zlib module is required. If zlib is available, you can
set the compression mode for individual files or for the archive as a whole
using zipfile.ZIP_DEFLATED. The default compression mode is
zipfile.ZIP_STORED.

::

    from zipfile_infolist import print_info
    import zipfile
    try:
        import zlib
        compression = zipfile.ZIP_DEFLATED
    except:
        compression = zipfile.ZIP_STORED

    modes = { zipfile.ZIP_DEFLATED: 'deflated',
              zipfile.ZIP_STORED:   'stored',
              }

    print 'creating archive'
    zf = zipfile.ZipFile('zipfile_write_compression.zip', mode='w')
    try:
        print 'adding README.txt with compression mode', modes[compression]
        zf.write('README.txt', compress_type=compression)
    finally:
        print 'closing'
        zf.close()

    print
    print_info('zipfile_write_compression.zip')

This time the archive member is compressed:

::

    $ python zipfile_write_compression.py creating archive
    adding README.txt with compression mode deflated
    closing

    README.txt
            Comment:
            Modified:       2007-12-16 10:08:50
            System:         3 (0 = Windows, 3 = Unix)
            ZIP version:    20
            Compressed:     63 bytes
            Uncompressed:   75 bytes


Using Alternate Archive Member Names
====================================

It is easy to add a file to an archive using a name other than the original
file name, by passing the arcname argument to write().

::

    from zipfile_infolist import print_info
    import zipfile

    zf = zipfile.ZipFile('zipfile_write_arcname.zip', mode='w')
    try:
        zf.write('README.txt', arcname='NOT_README.txt')
    finally:
        zf.close()
    print_info('zipfile_write_arcname.zip')

There is no sign of the original filename in the archive:

::

    $ python zipfile_write_arcname.py 
    NOT_README.txt
            Comment:
            Modified:       2007-12-16 10:08:50
            System:         3 (0 = Windows, 3 = Unix)
            ZIP version:    20
            Compressed:     75 bytes
            Uncompressed:   75 bytes

Writing Data from Sources Other Than Files
==========================================

Sometimes it is necessary to write to a ZIP archive using data that did not
come from an existing file. Rather than writing the data to a file, then
adding that file to the ZIP archive, you can use the writestr() method to add
a string of bytes to the archive directly.

::

    from zipfile_infolist import print_info
    import zipfile

    msg = 'This data did not exist in a file before being added to the ZIP file'
    zf = zipfile.ZipFile('zipfile_writestr.zip', 
                         mode='w',
                         compression=zipfile.ZIP_DEFLATED, 
                         )
    try:
        zf.writestr('from_string.txt', msg)
    finally:
        zf.close()

    print_info('zipfile_writestr.zip')

    zf = zipfile.ZipFile('zipfile_writestr.zip', 'r')
    print zf.read('from_string.txt')


In this case, I used the compress argument to ZipFile to compress the data,
since writestr() does not take compress as an argument.

::

    $ python zipfile_writestr.py
    from_string.txt
            Comment:
            Modified:       2007-12-16 11:38:14
            System:         3 (0 = Windows, 3 = Unix)
            ZIP version:    20
            Compressed:     62 bytes
            Uncompressed:   68 bytes

This data did not exist in a file before being added to the ZIP file

Writing with a ZipInfo Instance
===============================

By default, the modification date is computed for you when you add a file or
string to the archive. When using writestr(), it is also possible to pass a
ZipInfo instance to define that and other meta-data yourself.

::

    import time
    import zipfile
    from zipfile_infolist import print_info

    msg = 'This data did not exist in a file before being added to the ZIP file'
    zf = zipfile.ZipFile('zipfile_writestr_zipinfo.zip', 
                         mode='w',
                         )
    try:
        info = zipfile.ZipInfo('from_string.txt', 
                               date_time=time.localtime(time.time()),
                               )
        info.compress_type=zipfile.ZIP_DEFLATED
        info.comment='Remarks go here'
        info.create_system=0
        zf.writestr(info, msg)
    finally:
        zf.close()

    print_info('zipfile_writestr_zipinfo.zip')

In this example, I set the modified time to the current time, compress the
data, provide a false value for create_system, and add a comment.

::

    $ python zipfile_writestr_zipinfo.pyfrom_string.txt
            Comment:        Remarks go here
            Modified:       2007-12-16 11:44:14
            System:         0 (0 = Windows, 3 = Unix)
            ZIP version:    20
            Compressed:     62 bytes
            Uncompressed:   68 bytes

Appending to Files
==================

In addition to creating new archives, it is possible to append to an existing
archive or add an archive at the end of an existing file (such as a .exe file
for a self-extracting archive). To open a file to append to it, use mode 'a'.

::

    from zipfile_infolist import print_info
    import zipfile

    print 'creating archive'
    zf = zipfile.ZipFile('zipfile_append.zip', mode='w')
    try:
        zf.write('README.txt')
    finally:
        zf.close()

    print
    print_info('zipfile_append.zip')

    print 'appending to the archive'
    zf = zipfile.ZipFile('zipfile_append.zip', mode='a')
    try:
        zf.write('README.txt', arcname='README2.txt')
    finally:
        zf.close()

    print
    print_info('zipfile_append.zip')

The resulting archive ends up with 2 members:

::

    $ python zipfile_append.py 
    creating archive

    README.txt
            Comment:
            Modified:       2007-12-16 10:08:50
            System:         3 (0 = Windows, 3 = Unix)
            ZIP version:    20
            Compressed:     75 bytes
            Uncompressed:   75 bytes

    appending to the archive

    README.txt
            Comment:
            Modified:       2007-12-16 10:08:50
            System:         3 (0 = Windows, 3 = Unix)
            ZIP version:    20
            Compressed:     75 bytes
            Uncompressed:   75 bytes

    README2.txt
            Comment:
            Modified:       2007-12-16 10:08:50
            System:         3 (0 = Windows, 3 = Unix)
            ZIP version:    20
            Compressed:     75 bytes
            Uncompressed:   75 bytes

Python ZIP Archives
===================

Since version 2.3 Python has had the ability to import modules from inside ZIP
archives if those archives appear in sys.path. The zipfile.PyZipFile class can
be used to construct a module suitable for use in this way. When you use the
extra method writepy(), PyZipFile scans a directory for .py files and adds the
corresponding .pyo or .pyc file to the archive. If neither compiled form
exists, a .pyc file is created and added.

::

    import sys
    import zipfile

    if __name__ == '__main__':
        zf = zipfile.PyZipFile('zipfile_pyzipfile.zip', mode='w')
        try:
            zf.debug = 3
            print 'Adding python files'
            zf.writepy('.')
        finally:
            zf.close()
        for name in zf.namelist():
            print name

        print
        sys.path.insert(0, 'zipfile_pyzipfile.zip')
        import zipfile_pyzipfile
        print 'Imported from:', zipfile_pyzipfile.__file__

When I set the debug attribute of the PyZipFile to 3, verbose debugging is
enabled and you can observe as it compiles each .py file it finds.

::

    $ python zipfile_pyzipfile.py
    Adding python files
    Adding package in . as .
    Compiling ./__init__.py
    Adding ./__init__.pyc
    Compiling ./zipfile_append.py
    Adding ./zipfile_append.pyc
    Compiling ./zipfile_getinfo.py
    Adding ./zipfile_getinfo.pyc
    Compiling ./zipfile_infolist.py
    Adding ./zipfile_infolist.pyc
    Compiling ./zipfile_is_zipfile.py
    Adding ./zipfile_is_zipfile.pyc
    Compiling ./zipfile_namelist.py
    Adding ./zipfile_namelist.pyc
    Compiling ./zipfile_printdir.py
    Adding ./zipfile_printdir.pyc
    Compiling ./zipfile_pyzipfile.py
    Adding ./zipfile_pyzipfile.pyc
    Compiling ./zipfile_read.py
    Adding ./zipfile_read.pyc
    Compiling ./zipfile_write.py
    Adding ./zipfile_write.pyc
    Compiling ./zipfile_write_arcname.py
    Adding ./zipfile_write_arcname.pyc
    Compiling ./zipfile_write_compression.py
    Adding ./zipfile_write_compression.pyc
    Compiling ./zipfile_writestr.py
    Adding ./zipfile_writestr.pyc
    Compiling ./zipfile_writestr_zipinfo.py
    Adding ./zipfile_writestr_zipinfo.pyc
    __init__.pyc
    zipfile_append.pyc
    zipfile_getinfo.pyc
    zipfile_infolist.pyc
    zipfile_is_zipfile.pyc
    zipfile_namelist.pyc
    zipfile_printdir.pyc
    zipfile_pyzipfile.pyc
    zipfile_read.pyc
    zipfile_write.pyc
    zipfile_write_arcname.pyc
    zipfile_write_compression.pyc
    zipfile_writestr.pyc
    zipfile_writestr_zipinfo.pyc
    
    Imported from: zipfile_pyzipfile.zip/zipfile_pyzipfile.pyc



