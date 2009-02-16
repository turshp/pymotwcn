PyMOTW: getpass
=================

.. currentmodule:: getpass

* 模块： getpass
* 目的： 提示用户输入一个值(通常为密码), 输入时不显示内容.
* python版本： 1.5.2


许多通过终端与用户交互的程序需要向用户询问密码而在用户输入时不将其内容显示出来, getpass这个模块提供了一种简单的方法来安全地处理这个密码输入问题.


例子
------

``getpass()`` 函数提示用户输入, 并获取用户回车之前的内容. 输入内容以字符串的形式回传给调用者.

.. code-block:: python

    import getpass

    p = getpass.getpass()
    print 'You entered:', p

如果调用者没有指定提示内容, 默认为"Password:".

::

   $ python getpass_defaults.py
   Password:
   You entered: sekret

当然提示可以是当然提示可以是程序所需要的任何内容.

.. code-block:: python

    import getpass

    p = getpass.getpass(prompt='What is your favorite color? ')
    if p.lower() == 'blue':
        print 'Right. Off you go.'
    else:
        print 'Auuuuugh!'

我不推荐使用这种不安全的认证方式, 但它仅仅只是为了说明这一点.

::

   $ python getpass_prompt.py
   What is your favorite color?
   Right. Off you go.
   $ python getpass_prompt.py
   What is your favorite color?
   Auuuuugh!

默认情况下, ``getpass()`` 在stdout中显示提示字符串. 程序可以产生有用的信息到sys.stdout, 那么也可以将提示发到另一个流中, 比如sys.stderr.

.. code-block:: python

    import getpass
    import sys

    p = getpass.getpass(stream=sys.stderr)
    print 'You entered:', p

这种方式将标准输出重定向到一个pipe或者文件, 这种方式将标准输出重定向到一个pipe或者文件, 因而不显示密码提示. 用户输入的值同样不会回显到屏幕上.

::

   $ python getpass_stream.py >/dev/null
   Password:

在非终端中使用getpass
-----------------------

在Unix环境中, ``getpass()`` 总是需要一个通过termios控制的tty, 因此可以控制密码不回显. 这也意味着无法从一个重定向到标准输入流的非终端流中获取输入.

::

   $ echo "sekret" | python getpass_defaults.py
   Traceback (most recent call last):
   File "getpass_defaults.py", line 34, in
     p = getpass.getpass()
     File "/Library/Frameworks/Python.framework/Versions/2.5/lib/python2.5/getpass.py", line 32, in unix_getpass
     old = termios.tcgetattr(fd) # a copy to save
   termios.error: (25, 'Inappropriate ioctl for device')

由调用者决定是否需要确定输入流是否为一个tty, 以及在非tty时使用备选方法.

.. code-block:: python

    import getpass
    import sys

    if sys.stdin.isatty():
        p = getpass.getpass('Using getpass: ')
    else:
        print 'Using readline'
        p = sys.stdin.readline().rstrip()

    print 'Read: ', p

在tty中:

::

   $ python ./getpass_noterminal.py
   Using getpass:
   Read: sekret

非tty环境:

::

   $ echo "sekret" | python ./getpass_noterminal.py
   Using readline
   Read: sekret


参考
-----

* `getpass <http://docs.python.org/library/getpass.html>`_
