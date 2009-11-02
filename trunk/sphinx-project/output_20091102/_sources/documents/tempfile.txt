PyMOTW: tempfile
========================

.. currentmodule:: tempfile

使用tempfile模块可以安全的生成临时文件和目录.

* 模块: tempfile
* 目的: 创建临时的文件系统资源.
* Python 版本: 1.4 + (主安全修订版本2.3)

描述
------

许多程序需要将产生的中间数据保存在文件中. 安全地创建一些具有唯一名字的文件,  使得想要中断应用的人无法猜测到这些文件的名字，这是具有挑战性的.  tempfile模块提供一些用于安全处理文件系统资源的函数. TemporaryFile()打开并返回一个未命名文件. NamedTemporaryFile() 打开并返回一个已命名文件, mktemp()可以创建一个临时目录并返回它的名字.

临时文件
--------------------

如果你的应用需要用一临时文件来存储数据, 但不想和其他程序共享数据的话, 创建文件的最好方式是使用TemporaryFile()函数. 它在任意一个可能的平台上创建文件，并且能够随时断开链接. 这让其他程序不可能找到或访问这个文件,因为在文件系统表中没有它的引用.这个由TemporaryFile()创建的文件在关闭的时候自动删除.

.. code-block:: python

    import os
    import tempfile

    print 'Building a file name yourself:'
    filename = '/tmp/guess_my_name.%s.txt' % os.getpid()
    temp = open(filename, 'w+b')
    try:
        print 'temp:', temp
        print 'temp.name:', temp.name
    finally:
        temp.close()
        # Clean up the temporary file yourself
        os.remove(filename)

    print
    print 'TemporaryFile:'
    temp = tempfile.TemporaryFile()
    try:
        print 'temp:', temp
        print 'temp.name:', temp.name
    finally:
        # Automatically cleans up the file
        temp.close()

这个例子说明了使用一个普通模式作为名字的文件和使用TemporaryFile()创建的文件的区别. 注意: TemporaryFile()返回的文件不含有名字. 

::

    $ python tempfile_TemporaryFile.py
    Building a file name yourself:
    temp: <open file '/tmp/guess_my_name.7297.txt', mode 'w+b' at 0x5c338>
    temp.name: /tmp/guess_my_name.7297.txt

    TemporaryFile:
    temp: <open file '<fdopen>', mode 'w+b' at 0x5c410>
    temp.name: <fdopen>


默认情况下, 文件以模式'w+b'方式被创建, 所以在所有平台上都是一致的, 你的程序都能写入和读取它.

.. code-block:: python

    import os
    import tempfile

    temp = tempfile.TemporaryFile()
    try:
        temp.write('Some data')
        temp.seek(0)
     
        print temp.read()
    finally:
        temp.close()

在写入之后, 你需使用seek()将当前文件指针指向之前的位置以便能够读取刚才的写入的数据.

::

    $ python tempfile_TemporaryFile_binary.py
    Some data

如果你想要的是文本模式的临时文件, 可以传递mode='w+t':

.. code-block:: python

    import tempfile

    f = tempfile.TemporaryFile(mode='w+t')
    try:
        f.writelines(['first\n', 'second\n'])
        f.seek(0)

        for line in f:
            print line.rstrip()
    finally:
        f.close()


这个文件把数据看成是文本字符串:

::

    $ python tempfile_TemporaryFile_text.py
    first
    second

命名临时文件
--------------

在一些情况下, 也需要命名临时文件. 如果你的程序跨越多个进程, 或者甚至是主机, 命名文件是一种最简单的在程序各部分间传递数据的方式. NamedTemporaryFile()函数创建了一个有名字的, 即可以按名访问的文件.

.. code-block:: python

    import os
    import tempfile

    temp = tempfile.NamedTemporaryFile()
    try:
        print 'temp:', temp
        print 'temp.name:', temp.name
    finally:
        # Automatically cleans up the file
        temp.close()
        print 'Exists after close:', os.path.exists(temp.name)

即使文件被命名了, 他仍然可以在处理结束后删除.

::

    $ python tempfile_NamedTemporaryFile.py
    temp: <open file '<fdopen>', mode 'w+b' at 0x5c338>
    temp.name: /var/folders/9R/9R1t+tR02Raxzk+F71Q50U+++Uw/-Tmp-/tmplBKZMv
    Exists after close: False


mkdtemp
----------

如果你需要多个临时文件, 可以创建一个临时目录然后把所有文件放在这个目录中. 使用mkdtemp()函数来创建一个临时目录.

.. code-block:: python

    import os
    import tempfile

    directory_name = tempfile.mkdtemp()
    print directory_name
    # Clean up the directory yourself
    os.removedirs(directory_name)


由于目录不是"opened", 你需要手动将它删除.

:: 

    $ python tempfile_mkdtemp.py
    /var/folders/9R/9R1t+tR02Raxzk+F71Q50U+++Uw/-Tmp-/tmp0OsHPg


预测文件名
--------------

为了便于调试, 需要将原始临时文件的一些信息保留. 当然这样明显地比匿名临时文件不安全很多, 包括名字中的一部分信息能够让你检测这个文件是否正在被你的程序使用. 到目前为止描述的所有函数需要3个参数来在一定程度上控制你的文件名. 命名规则如下:

::

    dir + prefix + random + suffix


除了random之外的所有参数值都被传递给TemporaryFile(), NamedTemporaryFile(), 和 mkdtemp(). 例如:

.. code-block:: python

    import tempfile

    temp = tempfile.NamedTemporaryFile(suffix='_suffix', 
                                       prefix='prefix_', 
                                       dir='/tmp',
                                       )
    try:
        print 'temp:', temp
        print 'temp.name:', temp.name
    finally:
        temp.close()


prefix 和suffix参数再联合一个随机字符串生成一个文件名, dir参数指定新文件所在的位置.

::

    $ python tempfile_NamedTemporaryFile_args.py
    temp: <open file '<fdopen>', mode 'w+b' at 0x5c338>
    temp.name: /tmp/prefix_zy-7H3_suffix



临时文件的位置
--------------------

如果你没有使用dir参数来指定一个目标目录, 那么, 临时文件所在的真实路径会根据你平台和设置来确定. tempfile模块包含2个用于查询运行时间相关设置的函数:

.. code-block:: python

    import tempfile

    print 'gettempdir():', tempfile.gettempdir()
    print 'gettempprefix():', tempfile.gettempprefix()


gettempdir()返回放所有临时文件的默认目录. gettempprefix()返回新文件和目录名字的字符串前缀.

::

    $ python tempfile_settings.py
    gettempdir(): /var/folders/9R/9R1t+tR02Raxzk+F71Q50U+++Uw/-Tmp-
    gettempprefix(): tmp

gettempdir() 返回值的确定是基于一个直接查找算法, 它从一个位置列表中找到第一个可以创建文件的目录. 库文档中说明:

Python查找一个标准目录列表, 将第一个用户有权限在其中创建文件的目录来设置tempdir . 这个列表是:

1. 环境变量TMPDIR中的目录名.

2. 环境变量TEMP中的目录.

3. 环境变量TMP中的目录.

4. 平台指定的位置:

    * 在RiscOS上, 由Wimp$ScrapDir指定目录名字.

    * 在Windows上, 以C:$\backslash$TEMP, C:$\backslash$TMP, $\backslash$TEMP, 和 $\backslash$TMP按序查找目录.

    * 在其他平台上, 以/tmp, /var/tmp, 和/usr/tmp按序查找目录.

5. 最后一个是当前工作目录.



如果你的程序需要一个在全局位置下存放所有的临时文件, 你需要明确设置这个位置但又不想通过环境变量来设置, 这样的话, 你可以直接设置tempfile.tempdir来指定.

.. code-block:: python

    import tempfile

    tempfile.tempdir = '/I/changed/this/path'
    print 'gettempdir():', tempfile.gettempdir()

::

    $ python tempfile_tempdir.py
    gettempdir(): /I/changed/this/path


参考
-------

* `Python Module of the Week Home <http://www.doughellmann.com/projects/PyMOTW/>`_
* `Download Sample Code <http://www.doughellmann.com/downloads/PyMOTW-1.40.tar.gz>`_
