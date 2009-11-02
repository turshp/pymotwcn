PyMOTW: zipfile
===================

.. currentmodule:: zipfile

* 模块： zipfile
* 目的： 读写ZIP档案文件.
* python版本： 1.6+


zipfile模块能用来处理ZIP档案文件.

局限
-----

zipfile模块不支持附加评论的或者多磁盘ZIP文件, 支持大于4GB使用ZIP64扩展的ZIP文件.

测试ZIP文件
------------

``is_zipfile()`` 函数返回一个布尔值, 判断给定的文件是否是一个有效的ZIP文件.

.. code-block:: python

    import zipfile

    for filename in [ 'README.txt', 'example.zip', 'bad_example.zip', 'notthere.zip' ]:
        print '%20s %s' % (filename, zipfile.is_zipfile(filename))

注意：如果文件不存在, ``is_zipfile()`` 返回False.

::

   $ python zipfile_is_zipfile.py 
   README.txt False
   example.zip True
   bad_example.zip False
   notthere.zip False

从ZIP存档中读取元数据
----------------------

使用ZipFile类直接处理ZIP存档, 它支持从现有存档中读取数据也支持向存档中加入其它文件更改存档.

使用 ``namelist()`` 函数读取现有存档中所有文件的名字.

.. code-block:: python

    import zipfile

    zf = zipfile.ZipFile('example.zip', 'r')
    print zf.namelist()


返回的是存档内容名字的字符串列表.

::

   $ python zipfile_namelist.py 
   ['README.txt']

然而，名字列表只是存档中可用信息的一小部分, 使用 ``infolist()`` 或者 ``getinfo()`` 方法来访问存档内容的所有元数据.

.. code-block:: python

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

除了这儿输出的一些信息外, 还有别的东西, 但是需要仔细阅读ZIP文件说明书上的 `PKZIP应用注释 <http://www.pkware.com/business_and_developers/developer/appnote/>`_ 才能将其解密成有用的东西.

::

   $ python zipfile_infolist.py 
   README.txt
     Comment:
     Modified: 2007-12-16 10:08:52
     System: 3 (0 = Windows, 3 = Unix)
     ZIP version: 23
     Compressed: 63 bytes
     Uncompressed: 75 bytes

如果你已经知道了存档中各文件的名字, 你也可以通过 ``getinfo()`` 方法获得它的ZipInfo对象.

.. code-block:: python

    import zipfile

    zf = zipfile.ZipFile('example.zip')
    for filename in [ 'README.txt', 'notthere.txt' ]:
        try:
            info = zf.getinfo(filename)
        except KeyError:
            print 'ERROR: Did not find %s in zip file' % filename
        else:
            print '%s is %d bytes' % (info.filename, info.file_size)

如果存档中的某个文件不存在, ``getinfo()`` 方法会产生一个KeyError.

::

   $ python zipfile_getinfo.py 
   README.txt is 75 bytes
   ERROR: Did not find notthere.txt in zip file

从ZIP档案中提取文件
--------------------

为了访问存档文件的数据, 使用 ``read()`` 方法，并将该成员的名字传递给它.

.. code-block:: python

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

必要时, 数据会自动解压缩.

::

   $ python zipfile_read.py 
   README.txt :
   'The examples for the zipfile module use this file and example.zip as data.\n'

   ERROR: Did not find notthere.txt in zip file

创建一个新的档案
-----------------

为了创建一个新的档案, 以‘w’模式简单实例化ZipFile对象. 档案中任何现有文件会被清空, 开始新档案. 使用 ``write()`` 方法可以在档案中增加文件.

.. code-block:: python

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

默认情况下, 档案的文件不会被压缩:

::

   $ python zipfile_write.py
   creating archive
   adding README.txt
   closing

   README.txt
     Comment:
     Modified: 2007-12-16 10:08:50
     System: 3 (0 = Windows, 3 = Unix)
     ZIP version: 20
     Compressed: 75 bytes
     Uncompressed: 75 bytes

zlib模块提供压缩功能. 如果zlib是可用的, 你能使用zipfile.ZIP_DEFLATED对个人文件或者整个档案设置压缩模式. 默认压缩模式为zipfile.ZIP_STORED.

.. code-block:: python

    from zipfile_infolist import print_info
    import zipfile
    try:
        import zlib
        compression = zipfile.ZIP_DEFLATED
    except:
        compression = zipfile.ZIP_STORED

    modes = { zipfile.ZIP_DEFLATED: 'deflated',
        zipfile.ZIP_STORED: 'stored',
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

这次, 归档中的文件被压缩了:

::

   $ python zipfile_write_compression.py creating archive
   adding README.txt with compression mode deflated
   closing

   README.txt
     Comment:
     Modified: 2007-12-16 10:08:50
     System: 3 (0 = Windows, 3 = Unix)
     ZIP version: 20
     Compressed: 63 bytes
     Uncompressed: 75 bytes

使用备选的存档成员名
---------------------

传递arcname参数给 ``wirte()`` 可以很容易将一个文件添加到存档中, 但命名不能是原始文件名.

.. code-block:: python

    from zipfile_infolist import print_info
    import zipfile

    zf = zipfile.ZipFile('zipfile_write_arcname.zip', mode='w')
    try:
        zf.write('README.txt', arcname='NOT_README.txt')
    finally:
        zf.close()
    print_info('zipfile_write_arcname.zip')

在档案中, 新的文件没有使用原来的文件名.

::

   $ python zipfile_write_arcname.py 
   NOT_README.txt
     Comment:
     Modified: 2007-12-16 10:08:50
     System: 3 (0 = Windows, 3 = Unix)
     ZIP version: 20
     Compressed: 75 bytes
     Uncompressed: 75 bytes

从源而非文件上写数据
---------------------

有时候, 将那些不是来自现有文件的数据直接写入到ZIP档案中也是有必要的, 而不是通过先把这些数据写入到一个文件中, 再把这个文件添加到ZIP档案中, 你可以使用writestr()函数将字符串字节流直接写入到档案中.

.. code-block:: python

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

上述实例中, 我在ZipFile中使用compress参数来压缩数据, 但 ``writestr()`` 方法中不支持该参数.

::

   $ python zipfile_writestr.py
   from_string.txt
     Comment:
     Modified: 2007-12-16 11:38:14
     System: 3 (0 = Windows, 3 = Unix)
     ZIP version: 20
     Compressed: 62 bytes
     Uncompressed: 68 bytes

   This data did not exist in a file before being added to the ZIP file

通过ZipInfo实例写入
--------------------

默认情况下, 当你在档案中加入文件或者字符串时, 需要计算修改日期. 当使用 ``writestr()`` 方法时, 也需要传递一个ZipInfo实例给它, 该实例包含了修改日期和别的自定义元数据.

.. code-block:: python

    import time
    import zipfile
    from zipfile_infolist import print_info

    msg = 'This data did not exist in a file before being added to the ZIP file'
    zf = zipfile.ZipFile('zipfile_writestr_zipinfo.zip', mode='w',)
    try:
        info = zipfile.ZipInfo('from_string.txt', date_time=time.localtime(time.time()),)
        info.compress_type=zipfile.ZIP_DEFLATED
        info.comment='Remarks go here'
        info.create_system=0
        zf.writestr(info, msg)
    finally:
        zf.close()

    print_info('zipfile_writestr_zipinfo.zip')

在这个例子中, 我修改时间为当前时间. 压缩数据, 赋create_system值为0. 还增添了评论.

::

   $ python zipfile_writestr_zipinfo.pyfrom_string.txt
     Comment: Remarks go here
     Modified: 2007-12-16 11:44:14
     System: 0 (0 = Windows, 3 = Unix)
     ZIP version: 20
     Compressed: 62 bytes
         Uncompressed: 68 bytes

追加文件
----------

除了创建一个新档案之外, 还可以在现有档案上追加一个文件或在一个现有文件(如a.exe, 自解压档案文件)的末尾增加一个档案文件. 使用模式‘a‘打开文件以便追加.

.. code-block:: python

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

结果档案有2个文件：

::

   $ python zipfile_append.py 
   creating archive

   README.txt
     Comment:
     Modified: 2007-12-16 10:08:50
     System: 3 (0 = Windows, 3 = Unix)
     ZIP version: 20
     Compressed: 75 bytes
     Uncompressed: 75 bytes

   appending to the archive

   README.txt
     Comment:
     Modified: 2007-12-16 10:08:50
     System: 3 (0 = Windows, 3 = Unix)
     ZIP version: 20
     Compressed: 75 bytes
     Uncompressed: 75 bytes
               
   README2.txt
     Comment:
     Modified: 2007-12-16 10:08:50
     System: 3 (0 = Windows, 3 = Unix)
     ZIP version: 20
     Compressed: 75 bytes
     Uncompressed: 75 bytes

Python ZIP档案
---------------

如果存档出现在sys.path中, Python 2.3及以后版本都有能力从ZIP档案内部引入模块. 使用类zpfile.PyZipFile可以构造一个模块来适合这种用法. 当你使用其他方法 ``writepy()`` 时,PyZipFile浏览目录寻找.py文件, 并且将关联文件 ``.pyo`` 或 ``.pyc`` 加入到档案中. 如果两者都不存在, 则生成一个.pyc文件, 并将其加入到档案中.

.. code-block:: python

    import sys
    import zipfile

    if __name__ == '__main__':
        zf = zipfile.PyZipFile('zipfile_pyzipfile.zip', mode='w') ## 这段代码就可以直接将当前目录压缩打包，还能编译py脚本
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

当我设置PyZipFile的属性debug=3, 就激活了verbose debugging, 这在编译每一个.py文件时可以看到.

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


参考
-----

* `PKZIP Application Note <http://www.pkware.com/business_and_developers/developer/appnote/>`_
* `zipimport module <http://docs.python.org/lib/module-zipimport.html>`_
