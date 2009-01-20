PyMOTW: os(3)
===============

.. currentmodule:: os(3)

描述
----

前面讲述了如何来处理进程参数和输入/输出, 本周我将探讨一些操作文件和目录的函数.


文件描述符
-----------

os模块中包含了一些函数集用于处理底层的文件描述符(当前进程打开属主文件所使用的整型), 相比file()对象来说这些是更底层的API, 在本文中将不会解释什么是文件描述符, 它通常可以很好的和file()对象协同工作, 更多细节可以参考 `这里 <http://docs.python.org/lib/os-fd-ops.html>`_ 来了解如何使用文件描述符.


文件系统权限
-------------

os.access()可以测试一个进程对一个文件是否有可访问权限.

.. code-block:: python

    import os

    print 'Testing:', __file__
    print 'Exists:', os.access(__file__, os.F_OK)
    print 'Readable:', os.access(__file__, os.R_OK)
    print 'Writable:', os.access(__file__, os.W_OK)
    print 'Executable:', os.access(__file__, os.X_OK)

这个结果将取决于你如何来运行这个示例程序, 可能会显示如下:

::

   $ python os_access.py
   Testing: os_access.py
   Exists: True
   Readable: True
   Writable: True
   Executable: False

os.access()模块包含了2个特殊的含义, 首先, 在实际使用open()函数之前使用os.access()函数来判断一个文件是否可访问是没有意义的. 这里有个小事实, 在函数的两次调用之间可能会改变文件的权限. 另外一个含义是该函数适合于大部分扩展的POSIX许可语义的网络文件系统. 文件系统对于一个进程对文件有访问权限的POSIX调用会做出响应, 在调用open()时, 因为某些原因没有通过POSIX的调用测试, 那么会报告失败. 总之, 最好时在特定的模式中使用open(), 如果出现错误还可以捕获IOError异常. 

如果想获得更多关于文件的信息, 可以查阅stat()或者os.lstat(如果你查看的文件一个动态链接的话).

.. code-block:: python

    import os
    import sys
    import time

    if len(sys.argv) == 1:
      filename = __file__
      else:
        filename = sys.argv[1]

    stat_info = os.stat(filename)

    print 'os.stat(%s):' % filename
    print '\tSize:', stat_info.st_size
    print '\tPermissions:', oct(stat_info.st_mode)
    print '\tOwner:', stat_info.st_uid
    print '\tDevice:', stat_info.st_dev
    print '\tLast modified:', time.ctime(stat_info.st_mtime)

再次申明, 你得到的结果将取决于你运行的方式, 可以尝试向os_stat.py传递不同的文件名看看.

::

   $ python os_stat.py
   os.stat(os_stat.py):
       Size: 1547
       Permissions: 0100644
       Owner: 527
       Device: 234881026
       Last modified: Sun Jun 10 08:13:26 2007
 
在Unix类型系统上, 文件权限可以由chmod()来修改, 以整形形式传递. 形式值可以用stat模块的常量值来b表示. 以下示例了如何来触发用户的可执行权限位.

.. code-block:: python
    
    import os
    import stat

    # Determine what permissions are already set using stat
    existing_permissions = stat.S_IMODE(os.stat(__file__).st_mode)

    if not os.access(__file__, os.X_OK):
      print 'Adding execute permission'
      new_permissions = existing_permissions | stat.S_IXUSR
    else:
      print 'Removing execute permission'
      # use xor to remove the user execute permission
      new_permissions = existing_permissions ^ stat.S_IXUSR

    os.chmod(__file__, new_permissions)

运行该脚本前假设你有修改文件模式的权限.

::

   $ python os_stat_chmod.py
   Adding execute permission
   $ python os_stat_chmod.py
   Removing execute permission


目录
-----

同样提供了一些处理文件系统中目录的函数, 包括创建内容列表和删除它们.

.. code-block:: python

    import os

    dir_name = 'os_directories_example'

    print 'Creating', dir_name
    os.makedirs(dir_name)

    file_name = os.path.join(dir_name, 'example.txt')
    print 'Creating', file_name
    f = open(file_name, 'wt')
    try:
      f.write('example file')
    finally:
      f.close()

    print 'Listing', dir_name
    print os.listdir(dir_name)

    print 'Cleaning up'
    os.unlink(file_name)
    os.rmdir(dir_name)

::

   $ python os_directories.py
   Creating os_directories_example
   Creating os_directories_example/example.txt
   Listing os_directories_example
   ['example.txt']
   Cleaning up

有2个函数集用来创建和删除目录, 当使用os.mkdir()创建一个新的目录时, 其父目录必须存在. 当使用os.rmdir()来删除一个目录时候, 那么只有目录树的叶子节点(目录的最后一级)可以被删除. 相比下, os.makedirs()和os.removedirs()可以操作当前路径下的所有目录, os.makedirs()可以创建路径不存在的目录, os.removedirs()可以删除包含父目录的子目录(当然前提有这个权限). 

符号链接
---------

很多文件系统和平台都支持它, 同样有一些函数可以用来处理它们.

.. code-block:: python

    import os, tempfile

    link_name = tempfile.mktemp()

    print 'Creating link %s->%s' % (link_name, __file__)
    os.symlink(__file__, link_name)

    stat_info = os.lstat(link_name)
    print 'Permissions:', oct(stat_info.st_mode)

    print 'Points to:', os.readlink(link_name)

    # Cleanup
    os.unlink(link_name)

虽然os中包含了os.temparm()来创建临时文件, 当时相比tempfile模块还不够安全, 在使用中可能会产生RuntimeWarning信息, 更好的方法使用tempfile模块.

::

   $ python os_symlinks.py
   Creating link /tmp/tmpRxRiHn->os_symlinks.py
   Permissions: 0120755
   Points to: os_symlinks.py

访问目录树
-----------

os.walk()可以递归遍历一个目录, 对于每一个目录, 可以产生一个包含目录路径、当前路径的子目录列表, 以及在子目录中的文件. 以下示例展示了一个遍历目录的简单方法:

.. code-block:: python

    import os, sys

    # If we are not given a path to list, use /tmp
    if len(sys.argv) == 1:
      root = '/tmp'
    else:
      root = sys.argv[1]

    for dir_name, sub_dirs, files in os.walk(root):
      print '\n', dir_name
      # Make the subdirectory names stand out with /
      sub_dirs = [ '%s/' % n for n in sub_dirs ]
      # Mix the directory contents together
      contents = sub_dirs + files
      contents.sort()
      # Show the contents
      for c in contents:
        print '\t%s' % c

::

   $ python os_walk.py

   /tmp
      .KerberosLogin-0--1074266944 (inited,root,local)/
      .KerberosLogin-527-4839472 (inited,gui,tty,local)/
      527/
      cs_cache_lock_527
      cs_cache_lock_92
      emacs527/
      fry.log
      hsperfdata_dhellmann/
      objc_sharing_ppc_4294967294
      objc_sharing_ppc_527
      objc_sharing_ppc_92
      svn.arg.1835l59
      var_backups/
                                                                                 
   /tmp/.KerberosLogin-527-4839472 (inited,gui,tty,local)
      KLLCCache.lock

   /tmp/527
      /tmp/emacs527
      server
      /tmp/hsperfdata_dhellmann
      976
      
   /tmp/var_backups
      infodir.bak
      local.nidump


后续
---------

下次, 我们讨论os模块中创建和管理进程的函数.


参考
-----

* `Working with Files and Directories <http://docs.python.org/lib/os-file-dir.html>`_
* `tempfile module <http://docs.python.org/lib/module-tempfile.html>`_
