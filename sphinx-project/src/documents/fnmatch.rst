PyMOTW: fnmatch
===================

.. currentmodule:: fnmatch

使用fnmatch模块处理Unix风格的文件名的比较.

* 模块： fnmatch
* 目的： 对文件名和Unix风格模式进行比较.
* python版本：1.4+


描述
----

fnmatch模块用来全局模式上比较文件名(比如在Unix Shell中的模式).

简单匹配
---------

``fnmatch()`` 比较一个简单的文件名和一个模式并且返回一个布尔类型, 即匹配返回True, 不匹配返回Fasle. 如果操作系统使用了一个大小写不敏感的文件系统, 那么这种比较也是大小写不敏感的, 否则是大小写敏感的.

.. code-block:: python

    import fnmatch
    import os

    pattern = 'fnmatch_*.py'
    print 'Pattern :', pattern
    print

    files = os.listdir('.')
    for name in files:
        print 'Filename: %-25s %s' % (name, fnmatch.fnmatch(name, pattern))

这个例子中, 模式匹配所有以fnmatch_开头, 以 ``.py`` 结尾的文件名.

::

   $ python fnmatch_fnmatch.py

   Pattern : fnmatch_*.py

   Filename: .svn False
   Filename: __init__.py False
   Filename: fnmatch_filter.py True
   Filename: fnmatch_fnmatch.py True
   Filename: fnmatch_fnmatchcase.py True
   Filename: fnmatch_translate.py True

为了在各个不同文件系统或操作系统设置也能强制匹配大小写, 可以使用 ``fnmatchcase()`` .

.. code-block:: python

    import fnmatch
    import os

    pattern = 'FNMATCH_*.PY'
    print 'Pattern :', pattern
    print

    files = os.listdir('.')

    for name in files:
        print 'Filename: %-25s %s' % (name, fnmatch.fnmatchcase(name, pattern))

由于我的笔记本使用大小写敏感的文件系统, 所以修改后的模式不匹配任何一个文件.

::

   $ python fnmatch_fnmatchcase.py
   Pattern : FNMATCH_*.PY

   Filename: .svn False
   Filename: __init__.py False
   Filename: fnmatch_filter.py False
   Filename: fnmatch_fnmatch.py False
   Filename: fnmatch_fnmatchcase.py False
   Filename: fnmatch_translate.py False

过滤
------

你可以使用 ``filter()`` 来测试一系列的文件名. 它返回匹配模式参数的名字列表.

.. code-block:: python

    import fnmatch
    import os

    pattern = 'fnmatch_*.py'
    print 'Pattern :', pattern

    files = os.listdir('.')
    print 'Files :', files

    print 'Matches :', fnmatch.filter(files, pattern)

在这个例子中, ``filter()`` 返回这篇文章中所有示例源文件的名字. #即他们都以fnmatch_开头.

::

   $ python fnmatch_filter.py

   Pattern : fnmatch_*.py
   Files : ['.svn', '__init__.py', 'fnmatch_filter.py', 'fnmatch_fnmatch.py', 'fnmatch_fnmatchcase.py', 'fnmatch_translate.py']
   Matches : ['fnmatch_filter.py', 'fnmatch_fnmatch.py', 'fnmatch_fnmatchcase.py', 'fnmatch_translate.py']

翻译模式
----------

在内部, fnmatch将这种全局模式转换成一个正则式, 然后使用re模块来比较名字和模式.  ``translate()`` 函数是一个公共API用于将全局模式转换成正则式.

.. code-block:: python

    import fnmatch

    pattern = 'fnmatch_*.py'
    print 'Pattern :', pattern
    print 'Regex :', fnmatch.translate(pattern)

.. note::

    为了得到一个有效的表达式，有些特殊字符被转义。

::

   $ python fnmatch_translate.py
   Pattern : fnmatch_*.py
   Regex : fnmatch\_.*\.py$

参考
------

* `glob module documentation <http://docs.python.org/lib/module-glob.html>`_

