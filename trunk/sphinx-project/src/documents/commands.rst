PyMOTW: commands
=====================

.. currentmodule:: commands

commands模块包含一些用于处理Unix下shell命令及其输出的函数.

* 模块: commands
* 目的: 运行外部shell命令并能捕获退出状态码和输出结果.
* Python版本: 1.4+

描述:
-------

注意: 这个模块相对于 `subprocess <http://blog.doughellmann.com/2007/07/pymotw-subprocess.html>`_ 来说是已经过时了.

commands模块主要有3个用于处理外部命令的函数.这些函数具有shell感知并且能返回被执行命令的输出和状态码.

getstatusoutput():
---------------------

getstatusoutput() 函数通过shell运行一个命令, 之后返回退出状态码和文本输出(包含stdout和stderr的信息). 退出状态码是和C函数的wait()或os.wait()一样的, 是一个16位整数. 低字节包含杀死该进程的信号标识符. 当信号标识符为0时, 高字节表示了程序的退出状态. 如果产生了一个核心文件, 低字节的最高比特位会被设置1.

.. code-block::python

    from commands import *

    def run_command(cmd):

        print 'Running: "%s"' % cmd
        status, text = getstatusoutput(cmd)
        exit_code = status >> 8
        signal_num = status % 256
        print 'Signal: %d' % signal_num
        print 'Exit : %d' % exit_code
        print 'Core? : %s' % bool(exit_code / 256)
        print 'Output:'
        print text
        print


    run_command('ls -l *.py')
    run_command('ls -l *.notthere')
    run_command('echo "WAITING TO BE KILLED"; read input')



这个例子中, 运行的前2个命令正常退出, 而第三个会一直阻塞(等待输入)直到从另一个shell中将它杀死. 不要简单的使用Ctrl-C来中断程序, 而是在另一终端中, 使用ps和grep获得相关进程的标识, 并使用kill发送信号给它.

::

    $ python commands_getstatusoutput.py
    Running: "ls -l *.py"
    Signal: 0
    Exit : 0
    Core? : False
    Output:
    -rw-r--r-- 1 dhellman dhellman 1191 Oct 21 09:41 __init__.py
    -rw-r--r-- 1 dhellman dhellman 1321 Oct 21 09:48 commands_getoutput.py
    -rw-r--r-- 1 dhellman dhellman 1265 Oct 21 09:50 commands_getstatus.py
    -rw-r--r-- 1 dhellman dhellman 1626 Oct 21 10:10 commands_getstatusoutput.py

    Running: "ls -l *.notthere"
    Signal: 0
    Exit : 1
    Core? : False
    Output:
    ls: *.notthere: No such file or directory

    Running: "echo "WAITING TO BE KILLED"; read input"
    Signal: 1
    Exit : 0
    Core? : False
    Output:
    WAITING TO BE KILLED



我使用了"kill -HUP $PID"来杀死这个读进程.

getoutput():
-------------------

如果退出状态码对于你的应用来说是没有用的, 你使用getoutput()可以仅仅获得文本输出.

.. code-block::python

    from commands import *

    text = getoutput('ls -l *.py')
    print 'ls -l *.py:'
    print text

    print

    text = getoutput('ls -l *.notthere')
    print 'ls -l *.py:'
    print text

::

    $ python commands_getoutput.py 
    ls -l *.py:
    -rw-r--r-- 1 dhellman dhellman 1191 Oct 21 09:41 __init__.py
    -rw-r--r-- 1 dhellman dhellman 1321 Oct 21 09:48 commands_getoutput.py
    -rw-r--r-- 1 dhellman dhellman 1265 Oct 21 09:50 commands_getstatus.py
    -rw-r--r-- 1 dhellman dhellman 1626 Oct 21 10:10 commands_getstatusoutput.py

    ls -l *.py:
    ls: *.notthere: No such file or directory



getstatus():
----------------

和你期望的可能不一样, getstatus()函数在运行一个命令之后不是返回状态码. 而是, 传递一个参数给它, 这个参数是一个文件名, 被合并到"ls -ld"中, 运行该命令之后返回相应文本输出, 即获得该文件的相关信息.

.. code-block::python

    from commands import *

    status = getstatus('commands_getstatus.py')
    print 'commands_getstatus.py:', status
    status = getstatus('notthere.py')
    print 'notthere.py:', status
    status = getstatus('$filename')
    print '$filename:', status


从输出可以看到, 参数中的字符$不会被转义, 所以相关环境变量也不会被扩展.

::
    $ python commands_getstatus.py
    commands_getstatus.py: -rw-r--r-- 1 dhellman dhellman 1387 Oct 21 10:19 commands_getstatus.py
    notthere.py: ls: notthere.py: No such file or directory
    $filename: ls: $filename: No such file or directory



参考:
--------

* `Python Module of the Week Home <http://www.doughellmann.com/projects/PyMOTW/>`_
* `Download Sample Code <http://www.doughellmann.com/downloads/PyMOTW-1.25.tar.gz>`_

