PyMOTW: glob
===================

.. currentmodule:: glob

* 模块：glob
* 目的：使用Unix Shell规则来寻找文件名匹配某一模式的文件。
* python版本：1.4+


描述
----

即使glob API非常简单，但这个模块具有强大的力量。在很多情况下，尤其是你的程序需要寻找出文件系统中，文件名匹配特定模式的文件时，是非常有用的。如果你需要包含一个特定扩展名，或前缀，或含有任何普通字符串的文件列表，可以直接使用glob代替手工编程扫描目录内容。

glob中模式规则不是正则表达式，而是，符合标准Uinx路径扩展规则。但是Shell变量名和符号(~)是不被扩充的，只有一些特殊的字符：两个不同的通配符和字母范围被支持。模块规则适合于文件名的片段(以/为分隔)，但模式中的路径可以是相对或者绝对路径。


示例数据
---------

假设当前工作目录下包含有以下一些文件。

::

   dir/
   dir/file.txt
   dir/file1.txt
   dir/file2.txt
   dir/filea.txt
   dir/fileb.txt
   dir/subdir/
   dir/subdir/subfile.txt

使用glob_maketestdata.py脚本可以创建这些文件。

通配符
--------

``*`` 匹配名字片段中的0个或多个字符，例如，dir/``*`` 。

.. code-block:: python

    import glob
    print glob.glob('dir/*')

这个模式匹配在目录dir中的任何文件或子目录，但没有进一步递归匹配子目录。

::

   $ python glob_asterisk.py
   ['dir/file.txt', 'dir/file1.txt', 'dir/file2.txt',
   'dir/filea.txt', 'dir/fileb.txt', 'dir/subdir']

如果要列出子目录中的文件，你应该在模式中包含相应子目录：

.. code-block:: python

    print 'Named explicitly:'
    print glob.glob('dir/subdir/*')

    print 'Named with wildcard:'
    print glob.glob('dir/*/*')

上面的第一个例子直接列出了指定子目录名的文件，而第二个例子则依赖于通配符来寻找子目录。

::

   $ python glob_subdir.py
   Named explicitly:
   ['dir/subdir/subfile.txt']
   Named with wildcard:
   ['dir/subdir/subfile.txt']

在这个例子中，结果是一样的。如果还有其他的子目录，那么，通配符匹配所有子目录及其他们中包含的文件。

单一字符通配符
----------------

其他的被支持的通配符是问号(?)。它匹配在对应位置的任一单个字符。例如：

.. code-block:: python

    print glob.glob('dir/file?.txt')

匹配所有以"file"开头，之后包含一个任何字符并以".txt"结尾的文件。

::

   $ python glob_question.py
   ['dir/file1.txt', 'dir/file2.txt',
   'dir/filea.txt', 'dir/fileb.txt']

字符范围
----------

当你需要匹配一个特定字符时，可以使用一个字符范围来替代问号。例如，为了找到所有文件名中在扩展名之前包含数字的文件时：

.. code-block:: python

    print glob.glob('dir/*[0-9].*')

字符范围[0-9]匹配任何单一数字。这个范围是基于每个字符/数字的字符编码顺序，破折号(-)表示一个范围。上面的范围也可直接用[0123456789]来表示。

::

   $ python glob_charrange.py
   ['dir/file1.txt', 'dir/file2.txt']

参考
-------

* `Pattern Matching Notation <http://www.opengroup.org/onlinepubs/000095399/utilities/xcu_chap02.html#tag_02_13>`_


