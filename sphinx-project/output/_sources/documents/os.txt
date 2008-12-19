PyMOTW: os
===============

:Author: vbarter <yzcaijunjie@gmail.com>,lizze <shengyan1985@gmail.com>


.. contents::
.. sectnum::

* 模块：os
* 目的：为访问操作系统的特定属性提供方便。
* python版本：1.4+


描述
----

os模块提供了对特定平台模块(如posix，nt，mac)的封装，函数提供的api在很多平台上都可以相同使用，所以使用os模块会变得很方便。但不是所有函数在所有平台上都可用，比如在本文中到的一些管理函数在windows上无法使用。

在Python文档中os模块的副标题是“操作系统混合接口”，模块包含的大部分函数用于创建和管理活动进程和文件系统（文件和目录），当然除此之外还有其它一些函数。本文中，我们对如何获取和设置进程参数来进行讨论。

.. note::

    以下示例代码有的只能在linux平台上工作。

属主处理
---------------

首先讨论用来检查和改变进程属主id的函数。在守护进程和特殊的系统程序需要改变执行权限而不使用root情况下这往往是非常有用的。这里我不会太过详细的解释linux的安全，进程属主等具体含义，这些可以见参考中的文章来获得更详细的介绍。

我们给出一段脚本来获取一个进程的有效用户和组信息，然后改变这些有效值。这类似于一个守护进程在系统启动时以root身份启动加载，然后降低权限并作为一个普通用户运行。如果你下载示例并试运行，你可以设置user相应的值为TEST_GID和TEST_UID。

.. code-block:: python

    import os

    TEST_GID=501
    TEST_UID=527

    def show_user_info():
         print 'Effective User  :', os.geteuid()
         print 'Effective Group :', os.getegid()
         print 'Actual User    :', os.getuid(), os.getlogin()
         print 'Actual Group  :', os.getgid()
         print 'Actual Groups   :', os.getgroups()
         return

    print 'BEFORE CHANGE:'
    show_user_info()
    print
    try:
         os.setegid(TEST_GID)
    except OSError:
         print 'ERROR: Could not change effective group.  Re-run as root.'
    else:
         print 'CHANGED GROUP:'
         show_user_info()
         print
    
    try:
         os.seteuid(TEST_UID)
    except OSError:
         print 'ERROR: Could not change effective user.  Re-run as root.'
    else:
         print 'CHANGE USER:'
         show_user_info()
         print
        
当我运行在DELL D630 Ubuntu上时，得到的结果如下： 

::

   ~ 16:51:33> ./a.py 
   BEFORE CHANGE:
   Effective User  : 1000
   Effective Group : 1000
   Actual User    : 1000 cjj
   Actual Group  : 1000
   Actual Groups   : [4, 20, 24, 25, 29, 30, 44, 46, 104, 108, 110, 115, 117, 1000]

   ERROR: Could not change effective group.  Re-run as root.
   ERROR: Could not change effective user.  Re-run as root.

注意，当我使用非root运行时，值未被改变，我所启动的进程不可以改变他们自身有效的属性。如果我试图设置其他的用户名和组id，那么会抛出OSError异常。

下面，我们以root权限来运行这段脚本:

::

   ~ 16:51:10> sudo ./a.py 
   [sudo] password for cjj:
   BEFORE CHANGE:
   Effective User  : 0
   Effective Group : 0
   Actual User    : 0 cjj
   Actual Group  : 0
   Actual Groups   : [0]

   CHANGED GROUP:
   Effective User  : 0
   Effective Group : 501
   Actual User    : 0 cjj
   Actual Group  : 0
   Actual Groups   : [0]

   CHANGE USER:
   Effective User  : 527
   Effective Group : 501
   Actual User    : 0 cjj
   Actual Group  : 0
   Actual Groups   : [0]

在这个例子中，如果我们以root权限运行，那么我们可以改变这个进程的用户和组属性。一旦我们改变了UID，那么进程将受这个用户的权限限制，非root用户是无法改变有效用户组，所以首先我们需要改变用户组，然后再改变用户名。 

除了查找和改变进程属主，还有其他函数可以获取当前进程和父进程的id，查找和改变其进程用户组和会话id，与控制终端id是一样的。在你编写复杂程序（如自己的终端命令行程序）中使用这些函数可以帮助你在进程之间传递信号。

环境处理
---------

通过os模块，你的程序可以访问的另一个操作系统特性是系统环境。通过os.environ和os.getenv()可以访问在环境中设置的变量字符串。环境变量常用来作为配置像搜索路径，文件路径、调试标志的值。下面的示例检索了一个环境变量，并且通过子进程改变了这个值。

.. code-block:: python

    print 'Initial value:', os.environ.get('TESTVAR', None)
    print 'Child process:'
    os.system('echo $TESTVAR')

    os.environ['TESTVAR'] = 'THIS VALUE WAS CHANGED'

    print
    print 'Changed value:', os.environ['TESTVAR']
    print 'Child process:'
    os.system('echo $TESTVAR')

    del os.environ['TESTVAR']

    print
    print 'Removed value:', os.environ.get('TESTVAR', None)
    print 'Child process:'
    os.system('echo $TESTVAR')

os.environ对象遵循标准的Python映射API以便检索和设置值。 os.environ值的改变将被输出到子进程中。

::

   $ python os_environ_example.py
   Initial value: None
   Child process:


   Changed value: THIS VALUE WAS CHANGED
   Child process:
   THIS VALUE WAS CHANGED

   Removed value: None
   Child process:

工作目录处理   
--------------

在操作系统的文件系统结构中有一个概念是“当前工作目录”。在文件系统中，当前进程在访问用相对路径表示的文件时，就把这个目录当作默认目录位置。 

.. code-block:: python

    print 'Starting:', os.getcwd()
    print os.listdir(os.curdir)

    print 'Moving up one:', os.pardir
    os.chdir(os.pardir)

    print 'After move:', os.getcwd()
    print os.listdir(os.curdir)

注意os.curdir()和os.pardir()是指向当前目录和父目录的一种快捷方式。结果很显然：

::

   Starting: /Users/dhellmann/Documents/PyMOTW/PyMOTW/os
   ['.svn', '__init__.py', 'os_cwd_example.py', 'os_environ_example.py',
   'os_process_id_example.py', 'os_process_user_example.py']
   Moving up one: ..
   After move: /Users/dhellmann/Documents/PyMOTW/PyMOTW
   ['.svn', '__init__.py', 'bisect', 'ConfigParser', 'fileinput', 'linecache',
   'locale', 'logging', 'os', 'Queue', 'StringIO', 'textwrap']

后续...
----------

这里我们仅介绍了os模块中查找和设置进程参数的一些函数。下一次，我们将介绍os模块来管理文件系统对象。

参考
-----

* `Python Reference Manual, Process Parameters <http://docs.python.org/lib/os-procinfo.html>`_
* `Speaking UNIX, Part 8: UNIX processes <http://www.ibm.com/developerworks/aix/library/au-speakingunix8/index.html>`_
* `geteuid <http://www.opengroup.org/onlinepubs/009695399/functions/geteuid.html>`_
* `getsid <http://opengroup.org/onlinepubs/007908799/xsh/getsid.html>`_
* `setpgrp <http://linux.about.com/library/cmd/blcmdl2_setpgrp.htm>`_
