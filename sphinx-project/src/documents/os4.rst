PyMOTW: os(4)
===============

.. currentmodule:: os(4)

描述
----

这周,我总结整个os模块(但保留os.path的内容作为将来独立的一篇)并讨论一些有利于处理多进程的函数.我在part2中已经介绍了管道的使用, 这周我们来看下system(),fork(),exec()这3个函数和他们之间的关系.

申明
-----

这里的许多函数都有可移植性限制.可以查看subprocess模块以获得一种更一致的平台独立的处理进程方式.

运行外部命令
--------------

最简单的运行一条单独命令,没有一点交互的方式是使用os.system(). 他获取一个字符串,这个字符串就是一将被命令行执行的命令,通过一个shell中的子进程来执行.

.. code-block:: python

    import os

    # Simple command
    os.system('ls -l')

::

   $ python os_system_example.py
   total 168
   -rw-r--r-- 1 dhellman dhellman 0 May 27 06:58 __init__.py
   -rw-r--r-- 1 dhellman dhellman 1391 Jun 10 09:36 os_access.py
   -rw-r--r-- 1 dhellman dhellman 1383 May 27 09:23 os_cwd_example.py
   -rw-r--r-- 1 dhellman dhellman 1535 Jun 10 09:36 os_directories.py
   -rw-r--r-- 1 dhellman dhellman 1613 May 27 09:23 os_environ_example.py
   -rw-r--r-- 1 dhellman dhellman 2816 Jun 3 08:34 os_popen_examples.py
   -rw-r--r-- 1 dhellman dhellman 1438 May 27 09:23 os_process_id_example.py
   -rw-r--r-- 1 dhellman dhellman 1887 May 27 09:23 os_process_user_example.py
   -rw-r--r-- 1 dhellman dhellman 1545 Jun 10 09:36 os_stat.py
   -rw-r--r-- 1 dhellman dhellman 1638 Jun 10 09:36 os_stat_chmod.py
   -rw-r--r-- 1 dhellman dhellman 1452 Jun 10 09:36 os_symlinks.py
   -rw-r--r-- 1 dhellman dhellman 1279 Jun 17 12:17 os_system_example.py
   -rw-r--r-- 1 dhellman dhellman 1672 Jun 10 09:36 os_walk.py

由于命令是直接被传递到处理shell中,所以它可以包含shell语法,比如通配符或环境变量:

.. code-block:: python

    # Command with shell expansion
    os.system('ls -l $HOME')

::

   total 40
   -rwx------ 1 dhellman dhellman 1328 Dec 13 2005 %backup%~
   drwx------ 11 dhellman dhellman 374 Jun 17 12:11 Desktop
   drwxr-xr-x 15 dhellman dhellman 510 May 27 07:50 Devel
   drwx------ 29 dhellman dhellman 986 May 31 17:01 Documents
   drwxr-xr-x 45 dhellman dhellman 1530 Jun 17 12:12 DownloadedApps
   drwx------ 55 dhellman dhellman 1870 May 22 14:53 Library
   drwx------ 8 dhellman dhellman 272 Mar 4 2006 Movies
   drwx------ 10 dhellman dhellman 340 Feb 14 10:54 Music
   drwx------ 12 dhellman dhellman 408 Jun 17 01:00 Pictures
   drwxr-xr-x 5 dhellman dhellman 170 Oct 1 2006 Public
   drwxr-xr-x 15 dhellman dhellman 510 May 12 15:19 Sites
   drwxr-xr-x 4 dhellman dhellman 136 Jan 23 2006 iPod
   -rw-r--r-- 1 dhellman dhellman 105 Mar 7 11:48 pgadmin.log
   drwxr-xr-x 3 dhellman dhellman 102 Apr 29 16:32 tmp

除非你是直接在后台中运行这命令, 不然的话,直到命令执行完毕,调用 ``os.system()`` 的程序都会处于阻断状态. 子进程中的标准输入,输出,和错误输出默认被绑定到调用者的合适的流中. 但是也可以通过shell语法重定向到其他地方.

.. code-block:: python

    import os
    import time

    print 'Calling...'
    os.system('date; (sleep 3; date) &')

    print 'Sleeping...'
    time.sleep(5)

这就是shell的魔力,尽管还有更好的实现方式.

::

   $ python os_system_background.py
   Calling...
   Sun Jun 17 12:27:20 EDT 2007
   Sleeping...
   Sun Jun 17 12:27:23 EDT 2007

使用os.fork()创建进程
-----------------------

符合POSIX标准的函数 ``fork()`` 和 ``exec*()`` (在Mac OS X, Linux和其他类UNIX系统上可用)通过os模块都是可用的. 很多书已经很全面可靠的描述了这些函数的使用,所以检查你的库手册,或者去书店寻找进一步细节.

创建一个新进程作为当前进程的一个复本,可以使用 ``os.fork()`` :

.. code-block:: python

    pid = os.fork()

    if pid:
        print 'Child process id:', pid
    else:
        print 'I am the child'

每次运行这个事例代码时,你的输出变化给予你系统的当前状态, 但是它应该看起来像如下:

::

   $ python os_fork_example.py
   Child process id: 5883
   I am the child

当fork之后, 你结束这两个运行着相同代码的进程. 可以检查返回值来直到你在哪个进程中. 如果它是0, 表示你在子进程中,如果不是0, 则表示你在父进程中,它返回的值是其子进程的进程id.

对于父进程来说,发送给子进程信号是有必要的. 这个的设置有点复杂, 使用signal模块, 让我们通过具体代码来描述其使用吧. 首先我们定义一个信号处理句柄, 以便在收到相应信号时调用.

.. code-block:: python

    import os
    import signal
    import time

    def signal_usr1(signum, frame):
        pid = os.getpid()
        print 'Received USR1 in process %s' % pid

然后我们创建子进程, 并在父进程中,通过 ``os.kill()`` 发送一个USR1信号之前暂停一段时间.这短的暂停让子进程有时间去设置信号处理句柄.

.. code-block:: python

    print 'Forking...'
    child_pid = os.fork()
    if child_pid: ## 这个是父进程执行的代码
        print 'PARENT: Pausing before sending signal...'
        time.sleep(1)
        print 'PARENT: Signaling %s' % child_pid
        os.kill(child_pid, signal.SIGUSR1)

在子进程中,我们设置信号处理句柄后睡眠一段时间来让父进程有时间去发送信号给我们:

.. code-block:: python

    else:
        print 'CHILD: Setting up signal handler'
        signal.signal(signal.SIGUSR1, signal_usr1)
        print 'CHILD: Pausing to wait for signal'
        time.sleep(5)

当然，在实际的程序中,你也可能不需要(不想)调用sleep。

::

   $ python os_kill_example.py
   Forking...
   PARENT: Pausing before sending signal...
   CHILD: Setting up signal handler
   CHILD: Pausing to wait for signal
   PARENT: Signaling 6053
   Received USR1 in process 6053


正如你所看到的, 一个简单的处理子进程各自行为的方式是简单 ``fork()`` 函数的返回值并使用if分支实现. 对于更复杂的行为, 就需要更多的分离(独立)的代码,而不是简单的分支. 在其他的例子中,你可以使用一个已经封装好的程序. 对于这两种情况,你可以使用 ``os.exec*()`` 系列函数来运行其他程序. 当你"exec"一个程序, 程序中的代码会代替你进程中已存在的那些代码.

.. code-block:: python

    child_pid = os.fork()
    if child_pid:
        os.waitpid(child_pid, 0)
    else:
        os.execlp('ls', 'ls', '-l', '/tmp/') ## 执行多个子进程

::

   $ python os_exec_example.py

   total 40
   drwxr-xr-x 2 dhellman wheel 68 Jun 17 14:35 527
   prw------- 1 root wheel 0 Jun 15 19:24 afpserver_PIPE
   drwx------ 3 dhellman wheel 102 Jun 17 12:13 emacs527
   drwxr-xr-x 2 dhellman wheel 68 Jun 16 05:01 hsperfdata_dhellmann
   -rw------- 1 nobody wheel 12 Jun 17 13:55 objc_sharing_ppc_4294967294
   -rw------- 1 dhellman wheel 144 Jun 17 14:32 objc_sharing_ppc_527
   -rw------- 1 security wheel 24 Jun 17 07:09 objc_sharing_ppc_92
   drwxr-xr-x 4 dhellman dhellman 136 Jun 8 03:16 var_backups

有很多 ``exec*()`` 的变种, 它们依赖于你可能使用的参数, 如,你是否想要路径和父进程的环境变量都被复制到子进程中,等等. 细节可参见库文档.

对于所有变种, 它们的第一个参数是一个路径或者文件名, 剩下的参数控制如何运行相应程序. 它们要么作为命令行参数被传递, 要么覆盖进程"环境"(可查看 ``os.environ`` 和 ``os.getenv`` ).

等待一个子进程
---------------

假设说你使用了多个进程来突破Python的线程限制和 ``GIL``.如果你开始了多个进程来运行各自的任务, 你希望在开始新的进程之前等待其中一个或多个的结束, 以此来避免服务器的超载. 这里有一些使用 ``wait()`` 和相关函数来实现它的不同方法.

如果你不关心, 或者你已经知道, 哪个可能会首先退出 ``os.wait()`` 的子进程,并且这个子进程会尽快的返回任何存在:

.. code-block:: python

    import os
    import sys
    import time

    for i in range(3):
        print 'PARENT: Forking %s' % i
        worker_pid = os.fork()
        if not worker_pid:
            print 'WORKER %s: Starting' % i
            time.sleep(2 + i)
            print 'WORKER %s: Finishing' % i
            sys.exit(i)

     for i in range(3):
         print 'PARENT: Waiting for %s' % i
         done = os.wait()
         print 'PARENT:', done

.. note::

    ``os.wait()`` 的返回值是包含进程号和退出状态(一个16位的数字, 它的低字节是一个杀死该进程的信号数字, 它的高字节是退出状态)的一个元组.

::

   $ python os_wait_example.py

   PARENT: Forking 0
   PARENT: Forking 1
   PARENT: Forking 2
   PARENT: Waiting for 0
   WORKER 0: Starting
   WORKER 1: Starting
   WORKER 2: Starting
   WORKER 0: Finishing
   PARENT: (6501, 0)
   PARENT: Waiting for 1
   WORKER 1: Finishing
   PARENT: (6502, 256)
   PARENT: Waiting for 2
   WORKER 2: Finishing
   PARENT: (6503, 512)

如果你想等待一个特定的进程, 可以使用 ``os.waitpid()`` .

.. code-block:: python

    import os
    import sys
    import time

    workers = []
    for i in range(3):
        print 'PARENT: Forking %s' % i
        worker_pid = os.fork()
        if not worker_pid:
            print 'WORKER %s: Starting' % i
            time.sleep(2 + i)
            print 'WORKER %s: Finishing' % i
            sys.exit(i)
        workers.append(worker_pid)

    for pid in workers:
        print 'PARENT: Waiting for %s' % pid
        done = os.waitpid(pid, 0)
        print 'PARENT:', done

::

   $ python os_waitpid_example.py
   PARENT: Forking 0
   WORKER 0: Starting
   PARENT: Forking 1
   WORKER 1: Starting
   PARENT: Forking 2
   WORKER 2: Starting
   PARENT: Waiting for 6547
   WORKER 0: Finishing
   PARENT: (6547, 0)
   PARENT: Waiting for 6548
   WORKER 1: Finishing
   PARENT: (6548, 256)
   PARENT: Waiting for 6549
   WORKER 2: Finishing
   PARENT: (6549, 512)

``wait3()`` 和 ``wait4()`` 函数也是类似的方式, 但它们返回更多关于子进程的细节信息,如进程号, 退出状态, 资源使用情况等.

Spawn（孵化）
--------------

方便起见, ``os.spawn*()`` 系列函数将 ``fork()`` 和 ``exec*()`` 调用写在一条语句中:

.. code-block:: python

    os.spawnlp(os.P_WAIT, 'ls', 'ls', '-l', '/tmp/')

::

   $ python os_exec_example.py 
   total 40
   drwxr-xr-x 2 dhellman wheel 68 Jun 17 14:35 527
   prw------- 1 root wheel 0 Jun 15 19:24 afpserver_PIPE
   drwx------ 3 dhellman wheel 102 Jun 17 12:13 emacs527
   drwxr-xr-x 2 dhellman wheel 68 Jun 16 05:01 hsperfdata_dhellmann
   -rw------- 1 nobody wheel 12 Jun 17 13:55 objc_sharing_ppc_4294967294
   -rw------- 1 dhellman wheel 144 Jun 17 14:32 objc_sharing_ppc_527
   -rw------- 1 security wheel 24 Jun 17 07:09 objc_sharing_ppc_92
   drwxr-xr-x 4 dhellman dhellman 136 Jun 8 03:16 var_backups

结论
-----

还有其他很多在处理多进程时需要考虑的东西,比如,信号处理, 多进程文件读写等.所有这些话题都在参考书目(如 `Advanced Programming in the UNIX(R) Environment <http://www.amazon.com/Programming-Environment-Addison-Wesley-Professional-Computing/dp/0201433079/ref=pd_bbs_3/002-2842372-4768037?ie=UTF8&s=books&amp;qid=1182098757&sr=8-3>`_ )中有讲述.

参考
-----

* `Delve into UNIX process creation <http://www.ibm.com/developerworks/aix/library/au-unixprocess.html>`_
