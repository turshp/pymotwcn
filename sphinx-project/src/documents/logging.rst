PyMOTW: logging
===================

.. currentmodule:: logging

* 模块：logging
* 目的：为python模块提供状态、错误、信息输出的标准接口
* python版本：2.3


描述
----

logging模块定义了一个标准API, 用于报告所有你使用的模块的错误和状态信息.标准库模块中提供logging API的最重要意义是所有python模块可以参与到日志记录中, 因此你的应用程序日志可以包含来自第三方模块的信息.

当然, 在不同层次上或因不同目的来记录日志信息是有必要的. 将日志信息写入到文件, 如，HTTP GET/POST的地理信息, 通过SMTP发送的邮件, 一般的sockets, 或者特定OS的日志机制都是被标准模块支持的. 如果你有特殊需求, 任何内置模块都不能满足的话, 你也可以创建你自己的日志目标类.

例子
-----

大多数应用程序可能会将日志写入到文件中, 所以让我从这个例子开始讲述. 我们使用basicConfig()函数来设置默认的处理用于将调试信息写入到文件.

.. code-block:: python

    import logging
    LOG_FILENAME = '/tmp/logging_example.out'
    logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,)
        
    logging.debug('This message should go to the log file')


现在如果我们打开这个文件, 看看里面是什么, 我们应该可以找到以下的日志信息:

.. code-block:: python

    f = open(LOG_FILENAME, 'rt')
    try:
        body = f.read()
    finally:
        f.close()
        print 'FILE:'
        print body
        print

::

   FILE:
   DEBUG:root:This message should go to the log file

如果我们重复运行之前的脚本, 那么另外的日志信息会附加到文件末尾. 为了每次能够创建一个新的文件, 你可以传递一个filemode参数值为 ``'w'`` 给basicConfig().尽管你自己不能控制这个日志文件大小, 但, 可以使用RotatingFileHandler, 这更方便:

.. code-block:: python

    import glob
    import logging
    import logging.handlers

    LOG_FILENAME = '/tmp/logging_rotatingfile_example.out'

    # Set up a specific logger with our desired output level
    my_logger = logging.getLogger('MyLogger')
    my_logger.setLevel(logging.DEBUG)

    # Add the log message handler to the logger
    handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=20, backupCount=5)
    my_logger.addHandler(handler)

    for i in range(20):
        my_logger.debug('i = %d' % i)

    # See what files are created
    logfiles = glob.glob('%s*' % LOG_FILENAME) 
    
    for filename in logfiles:
        print filename

结果应该是6个独立的文件, 每个都含有应用程序的日志历史:

::

   /tmp/logging_rotatingfile_example.out
   /tmp/logging_rotatingfile_example.out.1
   /tmp/logging_rotatingfile_example.out.2
   /tmp/logging_rotatingfile_example.out.3
   /tmp/logging_rotatingfile_example.out.4
   /tmp/logging_rotatingfile_example.out.5 ##生成5个备份是由于之前设置了backupCount=5

当前日志文件总是为/tmp/logging_rotatingfile_example.out, 每次当文件大小达到限制时, 就以后缀.1来重命名. 每个已存的备份文件也依次重命名为原先后缀增一(如, .1成为.2), .5文件会被擦除.

显然的, 这个例子中设置了日志的长度太太太小了. 所以在实际程序下, 你可以为maxBytes设置一个合适的值.

使用日志API的另外一个有用的地方是能够在不同日志层次上产生不同的信息. 这能够让你书写的代码中带有调试信息, 例如, 降低日志层次以便这些调试信息不输出到你的生产系统中.

::

   CRITICAL 50
   ERROR 40
   WARNING 30
   INFO 20
   DEBUG 10
   UNSET 0

日志记录器, handler, 日志信息可以分别调用不同的层次. 一条日志信息, 只有当处理和日志记录器被设置为和它一样的层次或比它低层次时, 才被输出. 例如, 如果一个信息是CRITICAL, 记录器被设置为ERROR, 那么这个消息会输出来. 如果一个信息是WARNING, 记录器被设置为ERROR, 那么这个信息不被输出.

.. code-block:: python

    import logging
    import sys

    LEVELS = { 'debug':logging.DEBUG,
               'info':logging.INFO,
               'warning':logging.WARNING,
               'error':logging.ERROR,
               'critical':logging.CRITICAL,
    }

    if len(sys.argv) > 1:
        level_name = sys.argv[1]
        level = LEVELS.get(level_name, logging.NOTSET)
        logging.basicConfig(level=level)

    logging.debug('This is a debug message')
    logging.info('This is an info message')
    logging.warning('This is a warning message')
    logging.error('This is an error message')
    logging.critical('This is a critical error message')

运行这个脚本时指定参数, 如 ``'debug'`` 或 ``'warning'``, 看看在不同层次上, 哪些信息会显示出来:

::

   $ python logging_level_example.py debug
   DEBUG:root:This is a debug message
   INFO:root:This is an info message
   WARNING:root:This is a warning message
   ERROR:root:This is an error message
   CRITICAL:root:This is a critical error message

   $ python logging_level_example.py info
   INFO:root:This is an info message
   WARNING:root:This is a warning message
   ERROR:root:This is an error message
   CRITICAL:root:This is a critical error message

你可能不会注意到这些日志信息中都含有 ``'root'``. 这个日志模块支持一个不同名字日志记录器的层次结构. 一个告知某条日志信息来自于哪个日志器的简单方式是对每个模块使用独立的日志器对象. 每个新的日志器从它的父亲中"继承"一些配置, 日志信息发送到一个包含父日志器名字的日志器. 可选的, 每个日志器可以配置不同, 以便让来自不同模块的信息按不同的方式处理. 让我们看个简单的例子看怎样记录来自不同模块的信息, 这也便于追踪信息的对应源代码:

.. code-block:: python

    import logging

    logging.basicConfig(level=logging.WARNING)

    logger1 = logging.getLogger('package1.module1')
    logger2 = logging.getLogger('package2.module2')

    logger1.warning('This message comes from one module')
    logger2.warning('And this message comes from another module')

输出为:

::

   $ python logging_modules_example.py
   WARNING:package1.module1:This message comes from one module
   WARNING:package2.module2:And this message comes from another module

还有许多许多许多配置日志记录的选项, 包括不同日志信息格式化选项, 将信息发送到多个记录器, 使用socket接口改变一个正在运行的长时间程序的配置. 所有这些选项进一步在 `库模块文档 <http://docs.python.org/lib/module-logging.html>`_ 中深入.

参考
-----

* `PEP 282 <http://www.python.org/dev/peps/pep-0282/>`_
* `Python Standard Logging <http://www.onlamp.com/pub/a/python/2005/06/02/>`_

