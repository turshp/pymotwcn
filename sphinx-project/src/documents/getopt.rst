PyMOTW: getopt
=======================

.. currentmodule:: getopt

* 模块: getopt
* 目的: 命令行选项解析 
* Python 版本: 1.4

描述:
--------

getopt模块是老派的命令行选项解析器, 兼容Unix函数getopt(). 它解析一个参数序列, 如sys.argv, 返回(option, argument)对和其他非选项的参数序列.

支持的选项语法包括:

::

    -a
    -bval
    -b val
    --noarg
    --witharg=val
    --witharg val


函数参数
-----------

getopt函数可带三个参数:

* 第一个参数是待解析的参数序列, 它通常来自sys.argv[1:](忽略sys.arg[0], 因为它是程序名字).

* 第二个参数是选项定义字符串用于指示单个字符选项. 如果一个选项需要一个参数, 那么选项字符之后会跟着个冒号.

* 第三个参数, 如果使用的话, 应该是一个长类型选项名字序列. 长类型选项包含多个字符, 如--noarg或--witharg. 序列中的选项名字不应该包含前缀符'-'. 如果任何一个长选项需要一个参数, 那么它需要后缀符"=".

短形式和长形式选项可以在一个调用中结合起来定义.

短形式选项
---------------

如果一个程序需要带2个选项, -a和-b, b选项需要一个参数, 那么值应为"ab:".

.. code-block:: python

    print getopt.getopt(['-a', '-bval', '-c', 'val'], 'ab:c:')

::

    $ python getopt_short.py 
    ([('-a', ''), ('-b', 'val'), ('-c', 'val')], [])


长形式选项
----------------

如果程序带2个选项, -noarg和-witharg, 其参数序列应为[ 'noarg', 'witharg=' ].

.. code-block:: python

    print getopt.getopt([ '--noarg', '--witharg', 'val', '--witharg2=another' ],
                        '',
                        [ 'noarg', 'witharg=', 'witharg2=' ])

::

    $ python getopt_long.py 
    ([('--noarg', ''), ('--witharg', 'val'), ('--witharg2', 'another')], [])


例子
---------

接下来一个复杂点的例子, 它带5个选项: -o, -v, --output, --verbose, 和 --version. 选项-o, --output和--version需要携带参数.

.. code-block:: python

    import getopt
    import sys

    version = '1.0'
    verbose = False
    output_filename = 'default.out'

    print 'ARGV      :', sys.argv[1:]

    options, remainder = getopt.getopt(sys.argv[1:], 'o:v', ['output=', 
                                                             'verbose',
                                                             'version=',
                                                             ])
    print 'OPTIONS   :', options

    for opt, arg in options:
        if opt in ('-o', '--output'):
            output_filename = arg
        elif opt in ('-v', '--verbose'):
            verbose = True
        elif opt == '--version':
            version = arg

    print 'VERSION   :', version
    print 'VERBOSE   :', verbose
    print 'OUTPUT    :', output_filename
    print 'REMAINING :', remainder

程序可以多种方式调用.

::

    $ python ./getopt_example.py
    ARGV      : []
    OPTIONS   : []
    VERSION   : 1.0
    VERBOSE   : False
    OUTPUT    : default.out
    REMAINING : []

可以将单个字符选项和参数分隔开:

::

    $ python ./getopt_example.py -o foo
    ARGV      : ['-o', 'foo']
    OPTIONS   : [('-o', 'foo')]
    VERSION   : 1.0
    VERBOSE   : False
    OUTPUT    : foo
    REMAINING : []

或者结合起来:

::

    $ python ./getopt_example.py -ofoo
    ARGV      : ['-ofoo']
    OPTIONS   : [('-o', 'foo')]
    VERSION   : 1.0
    VERBOSE   : False
    OUTPUT    : foo
    REMAINING : []

长形式选项可以被简单的分离:

::

    $ python ./getopt_example.py --output foo    
    ARGV      : ['--output', 'foo']
    OPTIONS   : [('--output', 'foo')]
    VERSION   : 1.0
    VERBOSE   : False
    OUTPUT    : foo
    REMAINING : []

或者使用'='结合:

::

    $ python ./getopt_example.py --output=foo
    ARGV      : ['--output=foo']
    OPTIONS   : [('--output', 'foo')]
    VERSION   : 1.0
    VERBOSE   : False
    OUTPUT    : foo
    REMAINING : []


长形式选项的缩写
-----------------------

对于长形式的选项, 我们可以不必全部拼写出来, 而只要提供一个唯一的前缀以确定到底是哪个选项即可:

::

    $ python ./getopt_example.py --o foo
    ARGV      : ['--o', 'foo']
    OPTIONS   : [('--output', 'foo')]
    VERSION   : 1.0
    VERBOSE   : False
    OUTPUT    : foo
    REMAINING : []

如果唯一前缀不存在, 则会有抛出异常.

::

    $ python ./getopt_example.py --ver 2.0
    ARGV      : ['--ver', '2.0']
    Traceback (most recent call last):
      File "./getopt_example.py", line 43, in 
        'version=',
      File "/Library/Frameworks/Python.framework/Versions/2.5/lib/python2.5/getopt.py", line 89, in getopt
        opts, args = do_longs(opts, args[0][2:], longopts, args[1:])
      File "/Library/Frameworks/Python.framework/Versions/2.5/lib/python2.5/getopt.py", line 153, in do_longs
        has_arg, opt = long_has_args(opt, longopts)
      File "/Library/Frameworks/Python.framework/Versions/2.5/lib/python2.5/getopt.py", line 180, in long_has_args
        raise GetoptError('option --%s not a unique prefix' % opt, opt)
    getopt.GetoptError: option --ver not a unique prefix

选项解析过程会在遇到第一个非选项参数之后马上停止.

::

    $ python ./getopt_example.py -v not_an_option --output foo
    ARGV      : ['-v', 'not_an_option', '--output', 'foo']
    OPTIONS   : [('-v', '')]
    VERSION   : 1.0
    VERBOSE   : True
    OUTPUT    : default.out
    REMAINING : ['not_an_option', '--output', 'foo']


GNU风格的选项解析
-------------------------

这是Python 2.3中的新特性, 它提供了一个函数, 叫做gnu_getopt(). 该函数允许选项和非选项参数以任意顺序混合在命令行中. 我们改变了先前的那个例子, 可以很明显的看出差别所在: 
## cjj: 两边的差别是,getopt中遇到不能解析的参数时立刻停止, 而gnu_getopt遇到不能解析的参数时, 会放入未解析部分并返回 

.. code-block:: python

    import getopt
    import sys

    version = '1.0'
    verbose = False
    output_filename = 'default.out'

    print 'ARGV      :', sys.argv[1:]

    options, remainder = getopt.gnu_getopt(sys.argv[1:], 'o:v', ['output=', 
                                                                 'verbose',
                                                                 'version=',
                                                                 ])
    print 'OPTIONS   :', options

    for opt, arg in options:
        if opt in ('-o', '--output'):
            output_filename = arg
        elif opt in ('-v', '--verbose'):
            verbose = True
        elif opt == '--version':
            version = arg

    print 'VERSION   :', version
    print 'VERBOSE   :', verbose
    print 'OUTPUT    :', output_filename
    print 'REMAINING :', remainder

After changing the call in the previous example, the difference becomes clear:
修改了先前的例子, 可以看到差别是很明显的:

::

    $ python ./getopt_gnu.py -v not_an_option --output foo
    ARGV      : ['-v', 'not_an_option', '--output', 'foo']
    OPTIONS   : [('-v', ''), ('--output', 'foo')]
    VERSION   : 1.0
    VERBOSE   : True
    OUTPUT    : foo
    REMAINING : ['not_an_option']


特殊的例子: --
--------------------

如果getopt在输入参数序列中遇到--, 它就会马上停止剩余参数的解析.

::

    $ python ./getopt_example.py -v -- --output foo
    ARGV      : ['-v', '--', '--output', 'foo']
    OPTIONS   : [('-v', '')]
    VERSION   : 1.0
    VERBOSE   : True
    OUTPUT    : default.out
    REMAINING : ['--output', 'foo']

参考
-----

    `getopt <http://docs.python.org/library/getopt.html>`_
        The standard library documentation for this module.

    :mod:`optparse`
        The :mod:`optparse` module.
