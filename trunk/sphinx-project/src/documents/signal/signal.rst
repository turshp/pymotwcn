============================================================
signal -- 通过signal模块接收异步系统的事件通知.
============================================================

.. module:: signal
    :synopsis: 通过signal模块接收异步系统的事件通知.

:目的: 异步事件处理.
:Python 版本: 1.4+

.. 注意::

    对Unix信号进行编程需要程序员付出较多的努力。本文仅是一个介绍，可能不包含你在各个平台上, 成功使用信号的所有细节。在各个Unix版本上有规定一些标准化，但是仍然存在不一致的地方, 所以在当你碰到麻烦时最好去查看系统文档.

信号是通知你的程序发生某个事件的一种方法, 并异步的进行处理. 信号可以由系统自己生成, 或者由一进程发送到另一进程. 由于信号打断了你程序的正常执行流程, 所以当在处理一些操作(尤其I/O)的过程中, 收到一个信号的话, 可能会发生错误.

信号由一个整数唯一标识, 被定义在操作系统的C头文件中(译者注: linux/sem.h文件)Python把适合于各平台的信号定义为Python信号模块中的符号链接. 在下面的例子中, 我使用了SIGINT和SIGUSR1, 它们通常在所有Unix和类Unix系统上都有定义.


接收信号
=================

和其他基于事件的编程的形式类似, 在使用信号时需建立一个回调函数, 被称为信号处理函数, 它会在信号发生时被调用. 信号处理函数的参数为对应的信号标识号和从程序断点开始的栈状态

.. include:: signal_signal.py
    :literal:
    :start-after: #end_pymotw_header

这个相对简单的程序无限循环, 每次循环暂停一小段时间. 当一个信号到来时, sleep函数会被打断, 转而去执行信号处理函数``receive_signal()``, 打印信号标识号. 当执行完信号处理函数, 循环体继续. 我使用了命令行程序kill来给正在运行的程序发送信号, 为了产生下面的输出, 我首先在一个窗口中运行signal_signal.py, 然后在另一个窗口中使用命令``kill -USR1 $pid, kill -USR2 $pid``, 和 ``kill -INT $pid``.

::

    $ python signal_signal.py 
    My PID is: 71387
    Waiting...
    Waiting...
    Waiting...
    Received: 30
    Waiting...
    Waiting...
    Received: 31
    Waiting...
    Waiting...
    Traceback (most recent call last):
      File "signal_signal.py", line 25, in <module>
        time.sleep(3)
    KeyboardInterrupt


getsignal()
===========

使用getsignal()函数可以查看一个信号的信号处理函数是哪个. 传递信号标识号给getsignal(), 会返回对应的信号处理函数. 其中一些比较特殊的信号signal.SIG_IGN(信号会被忽略), signal.SIG_DFL(会使用默认的信号处理函数), None(从C中, 而不是Python中注册现有的信号处理函数)

.. include:: signal_getsignal.py
    :literal:
    :start-after: #end_pymotw_header

因为每个操作系统可能具有不同的信号定义, 所以你看到的输出会有所不同, 下面的结果是在OS X系统上运行得到的: 

::

    $ python signal_getsignal.py
    SIGHUP     ( 1): SIG_DFL
    SIGINT     ( 2): &lt;built-in function default_int_handler&gt;
    SIGQUIT    ( 3): SIG_DFL
    SIGILL     ( 4): SIG_DFL
    SIGTRAP    ( 5): SIG_DFL
    SIGIOT     ( 6): SIG_DFL
    SIGEMT     ( 7): SIG_DFL
    SIGFPE     ( 8): SIG_DFL
    SIGKILL    ( 9): None
    SIGBUS     (10): SIG_DFL
    SIGSEGV    (11): SIG_DFL
    SIGSYS     (12): SIG_DFL
    SIGPIPE    (13): SIG_IGN
    SIGALRM    (14): &lt;function alarm_received at 0x7c3f0&gt;
    SIGTERM    (15): SIG_DFL
    SIGURG     (16): SIG_DFL
    SIGSTOP    (17): None
    SIGTSTP    (18): SIG_DFL
    SIGCONT    (19): SIG_DFL
    SIGCHLD    (20): SIG_DFL
    SIGTTIN    (21): SIG_DFL
    SIGTTOU    (22): SIG_DFL
    SIGIO      (23): SIG_DFL
    SIGXCPU    (24): SIG_DFL
    SIGXFSZ    (25): SIG_IGN
    SIGVTALRM  (26): SIG_DFL
    SIGPROF    (27): SIG_DFL
    SIGWINCH   (28): SIG_DFL
    SIGINFO    (29): SIG_DFL
    SIGUSR1    (30): SIG_DFL
    SIGUSR2    (31): SIG_DFL


发送信号
===============

发送信号的函数是``os.kill()``, 它的使用在 PyMOTW的os模块中 有详细叙述  :ref:`creating-processes-with-os-fork` .

Alarms
======

Alarms是一种特殊类型的信号, 如果你的程序想让OS在一段时间后通知它, 则可以使用这种类型的信号. `标准模块文档 <http://docs.python.org/lib/node545.html>`_ 指出, 这有利于避免在进行I/O操作或者其他系统调用时引起的无限阻塞.

.. include:: signal_alarm.py
    :literal:
    :start-after: #end_pymotw_header

在这个例子中, ``sleep()``不会持续完整的4秒钟.

::

    $ python signal_alarm.py
    Before: Sun Aug 17 10:51:09 2008
    Alarm : Sun Aug 17 10:51:11 2008
    After : Sun Aug 17 10:51:11 2008


忽略信号
================

使用SIG_IGN作为信号处理函数来忽略一个信号. 下面的代码中让SIGINT使用了默认的信号处理函数SIG_IGN, 为信号SIGUSR1注册了处理函数 . 使用signal.pause()等待一个信号的到来.

.. include:: signal_ignore.py
    :literal:
    :start-after: #end_pymotw_header

正常情况下, SIGINT(在shell中按Ctrl-C产生的信号)引发键盘中断. 所以在这个例子中, 我们忽略了SIGINT, 而在接收到SIGUSR1时引起SystemExit异常才退出程序. 输出结果中的``^C``代表了从终端中使用Ctrl-C 来尝试中断程序. 在另一终端中使用``kill -USR1 72598``命令来退出我们的程序.

::

    $ python signal_ignore.py 
    My PID: 72598
    ^C^C^C^CExiting


信号和线程
===================

信号和线程一般情况下不宜混合使用. 但只有一个进程的主线程才会接收信号, 所以在线程中使用信号一般是没有什么用的. 接下来的例子设置了一个信号处理函数, 在一个线程中等待信号, 而在另一线程中发送信号.

.. include:: signal_threads.py
    :literal:
    :start-after: #end_pymotw_header

注意这里的信号处理函数是在主线程中注册. 这是使用Python信号模块的必需, 尽管底层的系统是支持线程和信号混用. 虽然接收线程调用了signal.pause(), 但它是不会接收到信号的. 后面的signal.alarm(2)调用防止程序无限期的阻塞下去, 因为接收线程一直不会退出. 

::

    $ python signal_threads.py 
    Waiting for signal in <Thread(receiver, started)>
    Sending signal in <Thread(sender, started)>
    Received signal 30 in <_MainThread(MainThread, started)>
    Waiting for <Thread(receiver, started)>
    Alarm clock

虽然alarms可以设置在线程中, 但它们也只能在主线程中接收.

.. include:: signal_threads_alarm.py
    :literal:
    :start-after: #end_pymotw_header

注意这里alarm不会在use_alarm()中终止sleep()的调用.

::

    $ python signal_threads_alarm.py
    Sun Aug 17 12:06:00 2008 Setting alarm in <Thread(alarm_thread, started)>
    Sun Aug 17 12:06:00 2008 Sleeping in <Thread(alarm_thread, started)>
    Sun Aug 17 12:06:00 2008 Waiting for <Thread(alarm_thread, started)>;
    Sun Aug 17 12:06:03 2008 Done with sleep
    Sun Aug 17 12:06:03 2008 Alarm in <_MainThread(MainThread, started)>
    Sun Aug 17 12:06:03 2008 Exiting normally

.. 参考::

    `signal <http://docs.python.org/lib/module-signal.html>`_
        Standard library documentation for this module.

    :ref:`creating-processes-with-os-fork`
        The kill() function can be used to send signals between processes.
