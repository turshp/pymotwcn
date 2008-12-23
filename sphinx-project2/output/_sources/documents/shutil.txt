PyMOTW: shutil
=================

.. currentmodule:: shutil

* 模块：shutil
* 目的: 高层次的文件操作.
* python版本：1.4+

shutil模块提供了一些高层次的文件操作,比如复制,设置权限等等.

描述:
------

shutil模块提供了一些用于复制和删除整个文件的函数.

复制文件:
-----------

copyfile() 将源文件内容完全复制给目标文件.如果没有写入目标文件的权限,会引起IOError.由于该函数是为了读取文件内容而打开此输入文件,而不管它的类型是什么,特殊类型的文件使用copyfile()是不能拷贝的，比如管道文件。

.. code-block:: python

    import os
    from shutil import *

    print 'BEFORE:', os.listdir(os.getcwd())
    copyfile('shutil_copyfile.py', 'shutil_copyfile.py.copy')
    print 'AFTER:', os.listdir(os.getcwd())

::

   $ python shutil_copyfile.py 
   BEFORE: ['__init__.py', 'shutil_copyfile.py']
   AFTER: ['__init__.py', 'shutil_copyfile.py', 'shutil_copyfile.py.copy']

copyfile()底层调用了copyfileobj()函数.文件名参数传递给copyfile()后,进而将此文件句柄传递给copyfileobj().第三个可选参数是一个缓冲区长度,以块读入(默认情况下,一次性读取整个文件).

.. code-block:: python

    import os
    from StringIO import StringIO
    import sys
    from shutil import *

    class VerboseStringIO(StringIO):
        def read(self, n=-1):
           next = StringIO.read(self, n)
           print 'read(%d) =>' % n, next
           return next

    lorem_ipsum = '''Lorem ipsum dolor sit amet, consectetuer adipiscing elit. 
                  Vestibulum aliquam mollis dolor. Donec vulputate nunc ut diam. 
                  Ut rutrum mi vel sem. Vestibulum ante ipsum.'''

    print 'Default:'
    input = VerboseStringIO(lorem_ipsum)
    output = StringIO()
    copyfileobj(input, output)

    print

    print 'All at once:'
    input = VerboseStringIO(lorem_ipsum)
    output = StringIO()
    copyfileobj(input, output, -1)

    print

    print 'Blocks of 20:'
    input = VerboseStringIO(lorem_ipsum)
    output = StringIO()
    copyfileobj(input, output, 20)

默认的行为是以大块读取:

::

   $ python shutil_copyfileobj.py
   Default:
   read(16384) => Lorem ipsum dolor sit amet, consectetuer adipiscing elit. 
   Vestibulum aliquam mollis dolor. Donec vulputate nunc ut diam. 
   Ut rutrum mi vel sem. Vestibulum ante ipsum.
   read(16384) => 

使用-1表示一次性读取所有输入:

::

   All at once:
   read(-1) => Lorem ipsum dolor sit amet, consectetuer adipiscing elit. 
   Vestibulum aliquam mollis dolor. Donec vulputate nunc ut diam. 
   Ut rutrum mi vel sem. Vestibulum ante ipsum.
   read(-1) => 

使用一个正整数设置块大小:

::

   Blocks of 20:
   read(20) => Lorem ipsum dolor si
   read(20) => t amet, consectetuer
   read(20) =>  adipiscing elit. 
   V
   read(20) => estibulum aliquam mo
   read(20) => llis dolor. Donec vu
   read(20) => lputate nunc ut diam
   read(20) => . 
   Ut rutrum mi vel 
   read(20) => sem. Vestibulum ante
   read(20) =>  ipsum.
   read(20) => 

copy()函数类似于Unix命令cp.如果目标参数是一个目录而不是一个文件,那么在这个目录中复制一个源文件副本(它与源文件同名).文件的权限也随之复制.

.. code-block:: python

    import os
    from shutil import *

    os.mkdir('example')
    print 'BEFORE:', os.listdir('example')
    copy('shutil_copy.py', 'example')
    print 'AFTER:', os.listdir('example')

::

   $ python shutil_copy.py
   BEFORE: []
   AFTER: ['shutil_copy.py']

copy2()函数类似于copy(),但是它将一些元信息,如文件最后一次被读取时间和修改时间等,也复制至新文件中.

.. code-block:: python

    import os
    from shutil import *

    def show_file_info(filename):
        stat_info = os.stat(filename)
        print '\tMode    :', stat_info.st_mode
        print '\tCreated :', time.ctime(stat_info.st_ctime)
        print '\tAccessed:', time.ctime(stat_info.st_atime)
        print '\tModified:', time.ctime(stat_info.st_mtime)

    os.mkdir('example')
    print 'SOURCE:'
    show_file_info('shutil_copy2.py')
    copy2('shutil_copy2.py', 'example')
    print 'DEST:'
    show_file_info('example/shutil_copy2.py')

::

   $ python shutil_copy2.py

   SOURCE:
           Mode    : 33188
           Created : Sun Oct 21 15:16:07 2007
           Accessed: Sun Oct 21 15:16:11 2007
           Modified: Sun Oct 21 15:16:07 2007
           DEST:
           Mode    : 33188
           Created : Sun Oct 21 15:16:11 2007
           Accessed: Sun Oct 21 15:16:11 2007
           Modified: Sun Oct 21 15:16:07 2007

复制文件元信息:
------------------
    
默认情况下,在Unix下,一个新创建的文件的权限会根据当前用户的umask值来设置.把一个文件的权限复制给另一个文件，可以使用copymode()函数.

.. code-block:: python

    from commands import *
    from shutil import *

    print 'BEFORE:', getstatus('file_to_change.txt')
    copymode('shutil_copymode.py', 'file_to_change.txt')
    print 'AFTER :', getstatus('file_to_change.txt')

首先,需要创建一个文件.然后对权限做些修改:

::

   $ touch file_to_change.txt
   $ chmod ugo+w file_to_change.txt

然后,运行刚才的示例脚本会改变之前的权限:

::

   $ python shutil_copymode.py
   BEFORE: -rw-rw-rw-   1 dhellman  dhellman  0 Oct 21 14:43 file_to_change.txt
   AFTER : -rw-r--r--   1 dhellman  dhellman  0 Oct 21 14:43 file_to_change.txt

复制文件的其他元信息(权限,最后读取时间,最后修改时间)可以使用copystat().

.. code-block:: python

    import os
    from shutil import *
    import time

    def show_file_info(filename):
        stat_info = os.stat(filename)
        print '\tMode    :', stat_info.st_mode
        print '\tCreated :', time.ctime(stat_info.st_ctime)
        print '\tAccessed:', time.ctime(stat_info.st_atime)
        print '\tModified:', time.ctime(stat_info.st_mtime)

    print 'BEFORE:'
    show_file_info('file_to_change.txt')
    copystat('shutil_copystat.py', 'file_to_change.txt')
    print 'AFTER :'
    show_file_info('file_to_change.txt')

::

   $ python shutil_copystat.py
   BEFORE:
           Mode    : 33206
           Created : Sun Oct 21 15:01:23 2007
           Accessed: Sun Oct 21 14:43:26 2007
           Modified: Sun Oct 21 14:43:26 2007
           AFTER :
           Mode    : 33188
           Created : Sun Oct 21 15:01:44 2007
           Accessed: Sun Oct 21 15:01:43 2007
           Modified: Sun Oct 21 15:01:39 2007

目录树:
-----------

shutil模块包含3个操作目录树的函数.使用copytree()来复制目录,它会递归复制整个目录结构.目标目录必须不存在.其中, symlinks参数控制符号链接是否作为链接或文件被复制,默认是将其内容复制成一个新文件.如果此选项为true,新的链接会在目标目录树中创建.

.. note::

    注意:copytree()文档中说,它一般作为一个样本实现,而不是一个工具.你可以修改其源码,让它变得更稳定,或者增加一些功能,比如说进度条.

.. code-block:: python

    from commands import *
    from shutil import *

    print 'BEFORE:'
    print getoutput('ls -rlast /tmp/example')
    copytree('example', '/tmp/example')
    print 'AFTER:'
    print getoutput('ls -rlast /tmp/example')

::

   $ python shutil_copytree.py
   BEFORE:
   ls: /tmp/example: No such file or directory
   AFTER:
   total 8
   8 -rw-r--r--    1 dhellman  wheel  1627 Oct 21 15:16 shutil_copy2.py
   0 drwxr-xr-x    3 dhellman  wheel   102 Oct 21 15:16 .
   0 drwxrwxrwt   18 root      wheel   612 Oct 21 15:26 ..

使用rmtree()可以删除整个目录树.里面若产生错误会作为异常抛出.但是如果它的第二个参数是目录树,那么错误会被忽略,第三个参数可以指定为一个特殊出错处理函数句柄.

.. code-block:: python

    from commands import *
    from shutil import *

    print 'BEFORE:'
    print getoutput('ls -rlast /tmp/example')
    rmtree('example', '/tmp/example')
    print 'AFTER:'
    print getoutput('ls -rlast /tmp/example')

::

   $ python shutil_rmtree.py

   BEFORE:
   total 8
   8 -rw-r--r--    1 dhellman  wheel  1627 Oct 21 15:16 shutil_copy2.py
   0 drwxr-xr-x    3 dhellman  wheel   102 Oct 21 15:16 .
   0 drwxrwxrwt   18 root      wheel   612 Oct 21 15:26 ..
   AFTER:
   ls: /tmp/example: No such file or directory

移动文件或目录可以使用move(),这很类似于Unix命令mv.如果源文件或目录和目标文件或目录在同一个文件系统下,那么源文件或目录会直接重命名.否则源文件或目录会复制到目标文件或目录,接着删除源文件或目录.

.. code-block:: python

    import os
    from shutil import *

    print 'BEFORE: example : ', os.listdir('example')
    move('example', 'example2')
    print 'AFTER : example2: ', os.listdir('example2')

::

   $ python shutil_move.py
   BEFORE: example :  ['shutil_copy.py']
   AFTER : example2:  ['shutil_copy.py']

参考
-----

* `PyMOTW <http://tc-nsop-test2.tc.baidu.com:3129/documents>`_
