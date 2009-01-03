PyMOTW: os.path
===================

.. currentmodule:: os.path

* 模块：os.path
* 目的：对文件名和路径进行解析, 创建, 测试和其他操作.
* python版本：1.4+


描述
----

我们可以利用os.path模块提供的函数更容易地在跨平台上处理文件。即使我们的程序不是用于夸平台，也应该使用os.path来让路径名字更加可靠。

解析路径
----------

os.path中的第一个函数集可以用于解析文件名字符串为不同部分。要注意到这些函数的解析不依赖于被解析的路径是否真正存在，他们只处理字符串。

路径解析依赖于一些os实现定义好的变量，如：

* ``os.sep`` ：表示路径的分隔符(如, "/")。
* ``os.extsep`` ：表示文件名和文件扩展名的分隔符(如, ".")。
* ``os.pardir`` ：表示上一层目录, 即父目录(如, "..")。
* ``os.curdir`` ：表示当前目录(如, ".")。

``split()`` 函数将路径切分成两个两部分并返回一个元组，它的第二个元素是路径的最后一部份, 第一个元素是路径的前面部分。

.. code-block:: python

    import os.path

    for path in [ '/one/two/three','/one/two/three/','/',.','']:
        print '"%s" : "%s"' % (path, os.path.split(path))

::
    
   $ python ospath_split.py
   "/one/two/three" : "('/one/two', 'three')"
   "/one/two/three/" : "('/one/two/three', '')"
   "/" : "('/', '')"
   "." : "('', '.')"
   "" : "('', '')"

**basename()** 返回的值和 ``split()`` 返回的第二个值相同。

.. code-block:: python

    import os.path

    for path in [ '/one/two/three','/one/two/three/','/','.','']:
        print '"%s" : "%s"' % (path, os.path.basename(path))


::

   $ python ospath_basename.py
   "/one/two/three" : "three"
   "/one/two/three/" : ""
   "/" : ""
   "." : "."
   "" : ""

**dirname()** 返回的值是和 ``split()`` 返回的第一个值相同。

.. code-block:: python

    import os.path

    for path in [ '/one/two/three', '/one/two/three/','/','.','']:
        print '"%s" : "%s"' % (path, os.path.dirname(path))

::

   $ python ospath_dirname.py

   "/one/two/three" : "/one/two"
   "/one/two/three/" : "/one/two/three"
   "/" : "/"
   "." : ""
   "" : ""

**splitext()** 和 ``split()`` 类似但是分隔路径的扩展名，而不是目录名。

.. code-block:: python

    import os.path

    for path in [ 'filename.txt', 'filename', '/path/to/filename.txt', '/', '' ]:
        print '"%s" :' % path, os.path.splitext(path)

::

   $ python ospath_splitext.py
   "filename.txt" : ('filename', '.txt')
   "filename" : ('filename', '')
   "/path/to/filename.txt" : ('/path/to/filename', '.txt')
   "/" : ('/', '')
   "" : ('', '')

**commonprefix()** 取一个路径列表作为参数，返回一个单一的字符串表示这些路径公共的前缀。这个值可能是一个实际上不存在的路径。路径分割符是被忽略的，所以前缀可能在在分割处被截断。

.. code-block:: python

    import os.path

    paths = ['/one/two/three/four','/one/two/threefold','/one/two/three/',]
    print paths
    print os.path.commonprefix(paths)


::

   $ python ospath_commonprefix.py
   ['/one/two/three/four', '/one/two/threefold', '/one/two/three/']
   /one/two/three


创建路径
--------

除了将现有的路径分隔外，你可能经常会将多个字符串组合成一个路径。

可以使用 ``join()`` 将多个路径部分组合成一个单个值：

.. code-block:: python

    import os.path

    for parts in [ ('one', 'two', 'three'),('/', 'one', 'two', 'three'),('/one', '/two', '/three'),]:
        print parts, ':', os.path.join(*parts)


::

   $ python ospath_join.py
   ('one', 'two', 'three') : one/two/three
   ('/', 'one', 'two', 'three') : /one/two/three
   ('/one', '/two', '/three') : /three


如果路径中包含变量部分，也能自动将她扩展出来. 例如， ``expanduser()`` 可以将波浪线(~)扩展成用户的主目录。


.. code-block:: python

    import os.path

    for user in [ '', 'dhellmann', 'postgres' ]:
        lookup = '~' + user
        print lookup, ':', os.path.expanduser(lookup)


::

   $ python ospath_expanduser.py
   ~ : /Users/dhellmann
   ~dhellmann : /Users/dhellmann
   ~postgres : /var/empty


**expandvars()** 是能更一般的扩展出现在路径中的环境变量。

.. code-block:: python

    import os.path
    import os

    os.environ['MYVAR'] = 'VALUE'

    print os.path.expandvars('/path/to/$MYVAR')

::

   $ python ospath_expandvars.py
   /path/to/VALUE


标准化路径
-------------

使用 ``join()`` 组装成的，或嵌入了变量的Paths路径可能会以多余的分隔符结束或含有相对路径部份。使用 ``normpath()`` 将这些清除：

.. code-block:: python

    import os.path

    for path in [ 'one//two//three', 'one/./two/./three', 'one/../one/two/three',]:
        print path, ':', os.path.normpath(path)


::

   $ python ospath_normpath.py
   one//two//three : one/two/three
   one/./two/./three : one/two/three
   one/../one/two/three : one/two/three


使用 **abspath()** 将一个相对路径转换成绝对路径。

.. code-block:: python

    import os.path

    for path in [ '.', '..', './one/two/three', '../one/two/three']:
        print '"%s" : "%s"' % (path, os.path.abspath(path))


::

   $ python ospath_abspath.py
   "." : "/Users/dhellmann/Documents/PyMOTW/in_progress/ospath"
   ".." : "/Users/dhellmann/Documents/PyMOTW/in_progress"
   "./one/two/three" : "/Users/dhellmann/Documents/PyMOTW/in_progress/ospath/one/two/three"
   "../one/two/three" : "/Users/dhellmann/Documents/PyMOTW/in_progress/one/two/three"


文件时间
----------

除了处理路径外， ``os.path`` 还可以包含一些用于检索文件属性的函数，他们比 ``os.stat()`` 更方便：

.. code-block:: python

    import os.path
    import time

    print 'File :', __file__
    print 'Access time :', time.ctime(os.path.getatime(__file__))
    print 'Modified time:', time.ctime(os.path.getmtime(__file__))
    print 'Change time :', time.ctime(os.path.getctime(__file__))
    print 'Size :', os.path.getsize(__file__)


::

   $ python ospath_properties.py
   File : /Users/dhellmann/Documents/PyMOTW/in_progress/ospath/ospath_properties.py
   Access time : Sun Jan 27 15:40:20 2008
   Modified time: Sun Jan 27 15:39:06 2008
   Change time : Sun Jan 27 15:39:06 2008
   Size : 478


测试文件
-----------

当你的程序含一个路径名时，他通常需要知道这个路径是否是文件还是目录。如果你的平台支持它，你需要知道这个路径是指向一个符号链接还是是一个挂载点。你也可能想测试路径是否存在。 ``os.path`` 提供测试这些条件的函数。


.. code-block:: python

    import os.path

    for file in [ __file__, os.path.dirname(__file__), '/', './broken_link']:
        print 'File :', file
        print 'Absolute :', os.path.isabs(file)
        print 'Is File? :', os.path.isfile(file)
        print 'Is Dir? :', os.path.isdir(file)
        print 'Is Link? :', os.path.islink(file)
        print 'Mountpoint? :', os.path.ismount(file)
        print 'Exists? :', os.path.exists(file)
        print 'Link Exists?:', os.path.lexists(file)
        print


::

   $ ln -s /does/not/exist broken_link
   $ python ospath_tests.py
   File : /Users/dhellmann/Documents/PyMOTW/in_progress/ospath/ospath_tests.py
   Absolute : True
   Is File? : True
   Is Dir? : False
   Is Link? : False
   Mountpoint? : False
   Exists? : True
   Link Exists?: True

   File : /Users/dhellmann/Documents/PyMOTW/in_progress/ospath
   Absolute : True
   Is File? : False
   Is Dir? : True
   Is Link? : False
   Mountpoint? : False
   Exists? : True
   Link Exists?: True

   File : /
   Absolute : True
   Is File? : False
   Is Dir? : True
   Is Link? : False
   Mountpoint? : True
   Exists? : True
   Link Exists?: True

   File : ./broken_link
   Absolute : False
   Is File? : False
   Is Dir? : False
   Is Link? : True
   Mountpoint? : False
   Exists? : False
   Link Exists?: True


遍历目录树
-------------

``os.path.walk()`` 遍历树中的所有目录，并调用一个你提供的函数，同时将目录名和目录中包含内容的名字传递给这个函数。下面的例子将递归的列出目录，但忽略.svn目录。

.. code-block:: python

    import os.path
    import pprint

    def visit(arg, dirname, names):
        print dirname, arg
        for name in names:
            subname = os.path.join(dirname, name)
            if os.path.isdir(subname):
                print ' %s/' % name
            else:
                print ' %s' % name
        # Do not recurse into .svn directory
        if '.svn' in names:
            names.remove('.svn') 
        print

    os.path.walk('..', visit, '(User data)')

::

   $ python ospath_walk.py
   .. (User data)
      .svn/
      ospath/

   ../ospath (User data)
      .svn/
      __init__.py
      ospath_abspath.py
      ospath_basename.py
      ospath_commonprefix.py
      ospath_dirname.py
      ospath_expanduser.py
      ospath_expandvars.py
      ospath_join.py
      ospath_normpath.py
      ospath_properties.py
      ospath_split.py
      ospath_splitext.py
      ospath_tests.py
      ospath_walk.py


