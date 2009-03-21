PyMOTW: Trace
=================

* 模块：Trace
* 目的: 监控程序语句和函数运行情况,并且产生报告信息.
* python版本：2.3+

trace - 跟踪正在执行的Python语句

trace模块帮助你明白程序的运行过程. 你可以跟踪执行的语句, 产生报表, 也能获取函数间的调用关系.

命令行接口
--------------

可以很简单的直接从命令行使用trace. 给定以下的Python脚本:

.. code-block:: python

    from recurse import recurse

    def main():
         print 'This is the main program.'
         recurse(2)
         return
           
    if __name__ == '__main__':
         main()
                    
    def recurse(level):
         print 'recurse(%s)' % level
         if level:
             recurse(level-1)
         return

    def not_called():        
         print 'This function is never called.'


跟踪时的异常
--------------

我们可以使用--trace选项来查看程序运行时哪条语句正在被执行.

::

   $ python -m trace --trace trace_example/main.py
   --- modulename: threading, funcname: settrace
   threading.py(70): _trace_hook = func
   --- modulename: trace, funcname: <module>
   <string>(1): --- modulename: trace, funcname: <module>
   main.py(7): """
   main.py(12): from recurse import recurse
   --- modulename: recurse, funcname: <module>
   recurse.py(7): """
   recurse.py(12): def recurse(level):
   main.py(14): def main():
   main.py(19): if __name__ == '__main__':
   main.py(20): main()
   --- modulename: trace, funcname: main
   main.py(15): print 'This is the main program.'
   This is the main program.
   main.py(16): recurse(2)
   --- modulename: recurse, funcname: recurse
   recurse.py(13): print 'recurse(%s)' % level
   recurse(2)
   recurse.py(14): if level:
   recurse.py(15): recurse(level-1)
   --- modulename: recurse, funcname: recurse
   recurse.py(13): print 'recurse(%s)' % level
   recurse(1)
   recurse.py(14): if level:
   recurse.py(15): recurse(level-1)
   --- modulename: recurse, funcname: recurse
   recurse.py(13): print 'recurse(%s)' % level
   recurse(0)
   recurse.py(14): if level:
   recurse.py(16): return
   recurse.py(16): return
   recurse.py(16): return
   main.py(17): return

输出结构的第一部分表明了trace的一个安装操作. 剩下来的输出显示了每个函数的入口信息, 包括函数位于哪个模块, 然后是原脚本文件中的语句行. 你可以看到函数recurse()被进入了3次, 正如你在main()中调用的那样.

代码报告
------------

从命令行中运行trace并使用--count选项可以产生代码信息报告, 因此可以看到哪些行是被执行的, 哪些被跳过了. 因为你的程序通常是多个文件组成, 那就会为每个文件产生独立的报表. 默认下, 报表文件在和模块的同一目录下被创建, 并以模块名命名, 而且使用 ``.cover`` 后缀名替换 ``.py`` .

::

   $ python -m trace --count trace_example/main.py
   This is the main program.
   recurse(2)
   recurse(1)
   recurse(0)

两个输出文件, trace_example/main.cover: 

::

   1: from recurse import recurse

   1: def main():
   1:     print 'This is the main program.'
   1:     recurse(2)
   1:     return

   1: if __name__ == '__main__':
   1:     main()

trace_example/recurse.cover:

::

   1: def recurse(level):
   3:     print 'recurse(%s)' % level
   3:     if level:
   2:         recurse(level-1)
   3:     return

.. note::

     虽然代码行def recurse(level):有一个1数值, 这不意味着这个函数仅运行一次, 而是意味着这个函数definition仅被执行一次.
     使用不同的选项来多次运行程序是有可能的, 并且保存报告数据, 产生一个联合报告. 

::
  
   $ python -m trace --coverdir coverdir1 --count --file coverdir1/coverage_report.dat trace_example/main.py
   This is the main program.
   recurse(2)
   recurse(1)
   recurse(0)
   Skipping counts file 'coverdir1/coverage_report.dat': [Errno 2] No such file or directory: 'coverdir1/coverage_report.dat'

::

   $ python -m trace --coverdir coverdir1 --count --file coverdir1/coverage_report.dat trace_example/main.py
   This is the main program.
   recurse(2)
   recurse(1)
   recurse(0)

::

   $ python -m trace --coverdir coverdir1 --count --file coverdir1/coverage_report.dat trace_example/main.py
   This is the main program.
   recurse(2)
   recurse(1)
   recurse(0)

::
 
   $ find coverdir1
   coverdir1
   coverdir1/coverage_report.dat

一旦报告信息被记录到 ``.cover`` 文件中, 你可以使用--report选项产生报告.

::

   $ python -m trace --coverdir coverdir1 --report --summary --missing --file coverdir1/coverage_report.dat trace_example/main.py
   lines cov% module (path)
   533 0% threading (/Library/Frameworks/Python.framework/Versions/2.5/lib/python2.5/threading.py)
   8 100% trace_example.main (trace_example/main.py)
   8 87% trace_example.recurse (trace_example/recurse.py)
   $ find coverdir1
   coverdir1
   coverdir1/coverage_report.dat
   coverdir1/threading.cover
   coverdir1/trace_example.main.cover
   coverdir1/trace_example.recurse.cover

程序一共运行了3次, 因此在报告中显示的值要比第一份报告中的值高3倍. --summary选项在输出信息中增加了百分比信息. 模块recurse只有87%被报告. 从这个报告中还可看到not_called()这个函数从未被运行, 这个是由前缀>>>>>>表示.

::

   3: def recurse(level):
   9:     print 'recurse(%s)' % level
   9:     if level:
   6:         recurse(level-1)
   9:     return

   3: def not_called():
   >>>>>> print 'This function is never called.'

调用关系
----------

除了以上覆盖信息, trace还可以收集函数间调用关系. 使用--listfuncs可以在结果中输出简单的函数调用关系: 

::

   $ python -m trace --listfuncs trace_example/main.py
   This is the main program.
   recurse(2)
   recurse(1)
   recurse(0)

   functions called:
   filename: /Library/Frameworks/Python.framework/Versions/2.5/lib/python2.5/threading.py, modulename: threading, funcname: settrace
   filename: <string>, modulename: <string>, funcname: <module>
   filename: trace_example/main.py, modulename: main, funcname: <module>
   filename: trace_example/main.py, modulename: main, funcname: main
   filename: trace_example/recurse.py, modulename: recurse, funcname: <module>
   filename: trace_example/recurse.py, modulename: recurse, funcname: recurse

可以使用--trackcalls获得更多信息, 比如说谁调用了函数.

::

   $ python -m trace --listfuncs --trackcalls trace_example/main.py
   This is the main program.
   recurse(2)
   recurse(1)
   recurse(0)

   calling relationships:

   *** /Library/Frameworks/Python.framework/Versions/2.5/lib/python2.5/trace.py ***
   --> /Library/Frameworks/Python.framework/Versions/2.5/lib/python2.5/threading.py
   trace.Trace.run -> threading.settrace
   --> <string>
   trace.Trace.run -> <string>.<module>

   *** <string> ***
   --> trace_example/main.py
   <string>.<module> -> main.<module>

   *** trace_example/main.py ***
   main.<module> -> main.main
   --> trace_example/recurse.py
   main.<module> -> recurse.<module>
   main.main -> recurse.recurse

   *** trace_example/recurse.py ***
   recurse.recurse -> recurse.recurse

编程接口
---------

通过trace接口增加更多的控制, 你可以在你的程序中使用Trace对象. Trace可以让你设置fixtures和其他依赖关系在运行单个函数前或执行一个用于跟踪的Python命令.

.. code-block:: python

    import trace
    from trace_example.recurse import recurse

    tracer = trace.Trace(count=False, trace=True)
    tracer.run('recurse(2)')

由于例子只跟踪到recurse()函数, 所以结果中没有把main.py的信息包含进来.

::

   $ python trace_run.py
   --- modulename: threading, funcname: settrace
   threading.py(70): _trace_hook = func
   --- modulename: trace_run, funcname: <module>
   <string>(1): --- modulename: recurse, funcname: recurse
   recurse.py(13): print 'recurse(%s)' % level
   recurse(2)
   recurse.py(14): if level:
   recurse.py(15): recurse(level-1)
   --- modulename: recurse, funcname: recurse
   recurse.py(13): print 'recurse(%s)' % level
   recurse(1)
   recurse.py(14): if level:
   recurse.py(15): recurse(level-1)
   --- modulename: recurse, funcname: recurse
   recurse.py(13): print 'recurse(%s)' % level
   recurse(0)
   recurse.py(14): if level:
   recurse.py(16): return
   recurse.py(16): return
   recurse.py(16): return

使用runfunc()也可以得到上述同样的输出. runfunc()接收任意位置和关键字参数, 他们在函数被tracer调用时都被传递给函数.

.. code-block:: python

    import trace
    from trace_example.recurse import recurse

    tracer = trace.Trace(count=False, trace=True)
    tracer.runfunc(recurse, 2)

::

   $ python trace_runfunc.py
   --- modulename: recurse, funcname: recurse
   recurse.py(13): print 'recurse(%s)' % level
   recurse(2)
   recurse.py(14): if level:
   recurse.py(15): recurse(level-1)
   --- modulename: recurse, funcname: recurse
   recurse.py(13): print 'recurse(%s)' % level
   recurse(1)
   recurse.py(14): if level:
   recurse.py(15): recurse(level-1)
   --- modulename: recurse, funcname: recurse
   recurse.py(13): print 'recurse(%s)' % level
   recurse(0)
   recurse.py(14): if level:
   recurse.py(16): return
   recurse.py(16): return
   recurse.py(16): return

保存结果数据
--------------

就像在命令行中使用一样, 计算和报告信息也可以被记录下来. 使用Trace对象的CoverageResults可以将这些数据明确的保存下来.

.. code-block:: python

    import trace
    from trace_example.recurse import recurse

    tracer = trace.Trace(count=True, trace=False)
    tracer.runfunc(recurse, 2)

    results = tracer.results()
    results.write_results(coverdir='coverdir2')

::

   $ python trace_CoverageResults.py
   recurse(2)
   recurse(1)
   recurse(0)

   $ find coverdir2
   coverdir2/
   coverdir2//trace_example.recurse.cover

   $ cat coverdir2/trace_example.recurse.cover
   #!/usr/bin/env python
   # encoding: utf-8
   #
   # Copyright (c) 2008 Doug Hellmann All rights reserved.
   #
   """
   """

   #__version__ = "$Id: recurse.py 1732 2008-10-12 14:50:28Z dhellmann $"
   #end_pymotw_header

   >>>>>> def recurse(level):
   3: print 'recurse(%s)' % level
   3: if level:
   2: recurse(level-1)
   3: return

   >>>>>> def not_called():
   >>>>>> print 'This function is never called.'

为了在生成报告时也保存计算数据, 可以使用参数infile和outfile.

.. code-block:: python

    mport trace
    from trace_example.recurse import recurse

    tracer = trace.Trace(count=True, trace=False, outfile='trace_report.dat')
    tracer.runfunc(recurse, 2)

    report_tracer = trace.Trace(count=False, trace=False, infile='trace_report.dat')
    results = tracer.results()
    results.write_results(summary=True, coverdir='/tmp')

传递给参数infile一个文件名来余弦读取存储的数据, 参数outfile指定在跟踪之后需要新建的一个结果文件名. 如果infile和outfile是相同的, 那么, 就相当于在原有文件中增加新的数据.

::

   $ python trace_report.py
   recurse(2)
   recurse(1)
   recurse(0)
   lines cov% module (path)
   7 57% trace_example.recurse (trace_example/recurse.py)

Trace选项
-----------

Trace构造器可以带多个可选参数以便更好的控制运行行为.

* count:        布尔型.打开行号计数.默认是True.
* countfuncs:   布尔型.打开运行中函数调用列表.默认是False
* countcallers: 布尔型.打开跟踪时的调用者和被调用者信息.默认是False.
* ignoremods:   序列.在跟踪报告中需要忽略的模块或包列表.默认是一个空元祖.
* ignoredirs:   序列.在跟踪报告中需要忽略的目录(其中包含模块或包)列表.默认是一个空元祖.
* infile:       包含缓存信息的文件名,作为输入.默认是None.
* outfile:      用于存储缓存信息的文件名,作为输入.默认是None,也就是数据不被存储.
  

参考
-----

* `标准库文档: trace <http://docs.python.org/library/trace.html>`_
