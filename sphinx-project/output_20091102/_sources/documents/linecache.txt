PyMOTW: linecache
===================

.. currentmodule:: linecache

* 模块： linecache
* 目的： 从文件或者导入模块中检索文本行, 对结果采用缓冲来提高读文件的效率.
* python版本： 1.4+


描述
------

python标准库处理python源文件中linecache模块被广泛的使用. 缓冲的实现是读取文件的内容, 并解析成行, 保存在内存的字典中. API 根据索引返回列表中的请求行. 在读取文件和寻找需要的行信息上可以节省一定时间. 这对于从同一个文件中查询多行内容是非常有用的, 比如为一个error report产生trackback.

示例
-----

.. code-block:: python

    import linecache
    import os
    import tempfile

我们使用Lorem Ipsum generator产生的文本作为输入样例:

.. code-block:: python

    lorem = '''Lorem ipsum dolor sit amet, consectetuer adipiscing elit.
    Vivamus eget elit. In posuere mi non risus. Mauris id quam posuere

    lectus sollicitudin varius. Praesent at mi. Nunc eu velit. Sed augue
    massa, fermentum id, nonummy a, nonummy sit amet, ligula. Curabitur
    eros pede, egestas at, ultricies ac, pellentesque eu, tellus. 

    Sed sed odio sed mi luctus mollis. Integer et nulla ac augue convallis
    accumsan. Ut felis. Donec lectus sapien, elementum nec, condimentum ac,
    interdum non, tellus. Aenean viverra, mauris vehicula semper porttitor,
    ipsum odio consectetuer lorem, ac imperdiet eros odio a sapien. Nulla
    mauris tellus, aliquam non, egestas a, nonummy et, erat. Vivamus

    sagittis porttitor eros.'''

    # Create a temporary text file with some text in it
    fd, temp_file_name = tempfile.mkstemp()

    os.close(fd)
    f = open(temp_file_name, 'wt')

    try:
        f.write(lorem)
    finally:
        f.close()

现在我们有了一个可用的临时文件, 让我们更深入一步. 从文件中读取的第5行是单一行. 注意, 在linecache中的行号是从1开始的. 但是我们自己对字符串进行分割, 那么索引号是从0开始. 我们还需要从缓冲中返回的值进行过滤去除换行符.

.. code-block:: python

    # Pick out the same line from source and cache.
    # (Notice that linecache counts from 1)
    print 'SOURCE: ', lorem.split('\n')[4]
    print 'CACHE : ', linecache.getline(temp_file_name, 5).rstrip()

下一步看下, 如果我们需要的行为空将会发生什么.

.. code-block:: python
 
    # Blank lines include the newline
    print '\nBLANK : "%s"' % linecache.getline(temp_file_name, 6)

如果请求的行号超过了文件中有效行号的范围, 那么linecache会返回一个空字符串.

.. code-block:: python

    # The cache always returns a string, and uses
    # an empty string to indicate a line which does
    # not exist.
    not_there = linecache.getline(temp_file_name, 500)
    print '\nNOT THERE: "%s" includes %d characters' %  (not_there, len(not_there))

即使这个文件不存在, 模块也不会抛出任何异常.

.. code-block:: python

    # Errors are even hidden if linecache cannot find the file
    no_such_file = linecache.getline('this_file_does_not_exist.txt', 1)
    print '\nNO FILE: ', no_such_file

虽然linecache模块经常用在输出tracebacks上, 另一个重要特性是可以通过指定模块名在sys.path中寻找python模块源码. 如果在当前路径中无法找到文件, 那么linecache中的缓冲直接搜索sys.path中的模块.

.. code-block:: python

    # Look for the linecache module, using
    # the built in sys.path search.
    module_line = linecache.getline('linecache.py', 3)
    print '\nMODULE : ', module_line

示例输出
---------

::

   SOURCE:  eros pede, egestas at, ultricies ac, pellentesque eu, tellus.
   CACHE :  eros pede, egestas at, ultricies ac, pellentesque eu, tellus.

   BLANK : "
   "

   NOT THERE: "" includes 0 characters

   NO FILE: 

   MODULE :  This is intended to read lines from modules imported -- hence if a filename

参考
-------

* `PyMOTW <http://http://tc-nsop-test2.tc.baidu.com:3129/documents>`_

