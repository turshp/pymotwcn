PyMOTW: os(2)
===============

.. currentmodule:: os(2)

描述
----

上一部分, 我们讨论了进程参数, 现在我们讨论一下os模块提供的输入/输出特性.


管道
-----

os模块提供了一些函数, 这些函数利用管道来管理子进程的IO操作. 这些函数的工作方式基本相同, 但根据输入/输出的需求类型返回不同的文件句柄. 相对于2.4版本中的 `subprocess <http://docs.python.org/lib/module-subprocess.html>`_ 模块这些函数是过时了, 但这是一个很好的机会, 你可以在已有的代码中看到它们.

管道中经常使用的是popen()函数, 它创建一个新的进程用于运行给定的命令并且根据模式选项附加给这个进程一个单一的输入输出数据流. 虽然在Windows中可以使用popen(), 但以下例子假设以Unix shell方式运行, 其中流的概念也是unix技术.

stdin: 进程(文件描述符0)的标准输入流, 对于这个进程来说是可读的, 通常指终端输入.

stdout: 进程(文件描述符1)的标准输出流, 对于这个进程来说是可写的, 通常用于给用户显示非错误信息. 

stderr: 进程(文件描述符2)的标准错误流, 对于这个进程来说是可写的, 通常用于传递错误信息.

.. code-block:: python

    import os

    print '\npopen, read:'
    pipe_stdout = os.popen('echo "to stdout"', 'r')
    try:
        stdout_value = pipe_stdout.read()
    finally:
        pipe_stdout.close()
    print '\tstdout:', repr(stdout_value)

    print '\npopen, write:'
    pipe_stdin = os.popen('cat -', 'w')
    try:
        pipe_stdin.write('\tstdin: to stdin\n')
    finally:
        pipe_stdin.close()

::

   popen, read:
        stdout: 'to stdout\n'

   popen, write:
        stdin: to stdin
        
从子进程的流中读取或者写入的方法是比较受限的, popen提供了额外的流, 如stdin、stdout、stderr来以便使用. 

比如, popen2()函数返回一个与子进程标准输入绑定的只写流和一个与子进程标准输出绑定的只读流.

.. code-block:: python

    print '\npopen2:'
    pipe_stdin, pipe_stdout = os.popen2('cat -')
    try:
        pipe_stdin.write('through stdin to stdout')
    finally:
        pipe_stdin.close()
    
    try:
        stdout_value = pipe_stdout.read()
    finally:
        pipe_stdout.close()
    print '\tpass through:', repr(stdout_value)

这个简单例子解释了双向通信方式, 从stdin写入的值被cat命令读取('-'参数的作用), 然后由stdout输出. 显然, 一个复杂的进程通过管道可以来回传递其它类型的信息, 甚至是序列化对象.


::

   popen2:
        pass through: 'through stdin to stdout'

有些情况下, 希望同时访问stdout和stderr, stdout常用于输出信息, stderr常用于抛出错误. 因此分别读取他们可以减少解析错误消息的复杂度, 而popen3函数返回一个新进程的3个流stdin、stdout、stderr.

.. code-block:: python

    print '\npopen3:'
    pipe_stdin, pipe_stdout, pipe_stderr = os.popen3('cat -; echo ";to stderr" 1>&2')
    try:
        pipe_stdin.write('through stdin to stdout')
    finally:
        pipe_stdin.close()
    try:
        stdout_value = pipe_stdout.read()
    finally:
        pipe_stdout.close()
    print '\tpass through:', repr(stdout_value)
    try:
        stderr_value = pipe_stderr.read()
    finally:
        pipe_stderr.close()
    print '\tstderr:', repr(stderr_value)

注意, 我们需要分别读取和关闭这些流, 在处理多进程的IO中, 还涉及到流程控制和排序, I/O即为缓冲器, 如果想读取流中的所有数据, 那么子进程必须关闭这个流来表示文件的结束, 更多信息可以参考Python库文档 `Flow Control Issues <http://docs.python.org/lib/popen2-flow-control.html>`_ .

::
   
   popen3:
        pass through: 'through stdin to stdout'
        stderr: ';to stderr\n'

最后, popen4()返回两个流, stdin和stdout/stderr的组合, 这对于命令的结果需要被记录, 但不需要解析是很有用的.

.. code-block:: python

    print '\npopen4:'
    pipe_stdin, pipe_stdout_and_stderr = os.popen4('cat -; echo ";to stderr" 1>&2')
    try:
        pipe_stdin.write('through stdin to stdout')
    finally:
        pipe_stdin.close()
    try:
        stdout_value = pipe_stdout_and_stderr.read()
    finally:
        pipe_stdout.close()
    print '\tcombined output:', repr(stdout_value)

::

   popen4:
        combined output: 'through stdin to stdout;to stderr\n'

另外, 除了接收简单的字符串命令来传递给shell解析, popen2()、popen3()、popen4()函数同样接收字符串序列(命令, 加参数). 这种情况中, 参数不是传递给shell的.

.. code-block:: python

    print '\npopen2, cmd as sequence:'
    pipe_stdin, pipe_stdout = os.popen2(['cat', '-'])
    try:
        pipe_stdin.write('through stdin to stdout')
    finally:
        pipe_stdin.close()
    try:
        stdout_value = pipe_stdout.read()
    finally:
        pipe_stdout.close()
    print '\tpass through:', repr(stdout_value)

::

   popen2, cmd as sequence:
        pass through: 'through stdin to stdout'

        
后续
---------

下次, 我们将讨论如何来控制文件描述符.


参考
-----

* `Unix Concepts <http://www.linuxhq.com/guides/LUG/node67.html>`_ for more discussion of stdin, stdout, and stderr
* `File Object Creation <http://docs.python.org/lib/os-newstreams.html>`_ with the os module
* `subprocess <http://docs.python.org/lib/module-subprocess.html>`_
* `Flow Control Issues <http://docs.python.org/lib/popen2-flow-control.html>`_
