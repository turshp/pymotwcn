PyMOTW: pickle & cPickle
=============================

.. currentmodule:: pickle

* 模块：pickle 和 cPickle
* 目的: Python对象序列化
* python版本：pickle至少1.4, cPickle 至少1.5

Python对象序列化

描述
----

pickle模块可以实现任意的Python对象转换为一系列字节(即序列化对象)的算法. 这些字节流可以被传输或存储, 接着也可以重构为一个和原先对象具有相同特征的新对象.

cPickle模块实现了同样的算法, 但它是用c而不是python. 因此, 它比python实现的快上好几倍, 但是不允许使用者去继承Pickle. 如果继承对于你的使用不是很重要, 那么你大可以使用cPickle.

.. note::

    pickle的文档清晰的表明它不提供安全保证. 所以慎用pickle来作为内部进程通信或者数据存储, 也不要相信那些你不能验证安全性的数据.


例子
-----

第一个pickle示例是将一个数据结构编码为一个字符串, 然后将其输出到控制台.

.. code-block:: python

    try:
        import cPickle as pickle
    except:
        import pickle
    import pprint

我们首先尝试导入cPickle, 并指定别名为"pickle". 如果因为某种原因导入pickle失败, 我们则导入由Python实现的pickle模块. 如果cPickle是可用的, 会给我们带来更快的实现, 但如果不可用, 也会有正确的实现.

接下来, 我们定义一个完全由基本类型组成的数据结构. 任何类的实例都可被pickle, 这会在下一个例子中表述. 我选择基本数据类型以便更简单的示范.

.. code-block:: python

    data = [ { 'a':'A', 'b':2, 'c':3.0 } ]
    print 'DATA:',
    pprint.pprint(data)

现在我们就可以使用pickle.dumps()来创建数据值的字符串表示.

.. code-block:: python

    data_string = pickle.dumps(data)
    print 'PICKLE:', data_string

默认情况下, pickle仅使用ASCII字符. 也可以使用高效的二进制格式. 但这些示例依然使用了ASCII格式. 

::

   $ python pickle_string.py
   DATA:[{'a': 'A', 'b': 2, 'c': 3.0}]
   PICKLE: (lp1
   (dp2
   S'a'
   S'A'
   sS'c'
   F3
   sS'b'
   I2
   sa.

一旦数据被序列化, 你就可以把他写入到文件、socket、管道等等中. 之后你可以读取这个文件, unpickle这些数据来构造具有相同值的新对象.

.. code-block:: python

    data1 = [ { 'a':'A', 'b':2, 'c':3.0 } ]
    print 'BEFORE:',
    pprint.pprint(data1)

    data1_string = pickle.dumps(data1)

    data2 = pickle.loads(data1_string)
    print 'AFTER:',
    pprint.pprint(data2)

    print 'SAME?:', (data1 is data2)
    print 'EQUAL?:', (data1 == data2)

正像你看到的那样, 新构造的对象等于原来的对象, 但他们又不是相同的对象. 这里不足为奇.

::

   $ python pickle_unpickle.py
   BEFORE:[{'a': 'A', 'b': 2, 'c': 3.0}]
   AFTER:[{'a': 'A', 'b': 2, 'c': 3.0}]
   SAME?: False
   EQUAL?: True

pickle除了提供dumps()和loads(), 还提供非常方便的函数用于操作类文件流. 支持同时写多个对象到同一个流中, 然后在不知道有多少个对象或不知道它们有多大时, 能够从这个流中读取多个对象也是可能的.

.. code-block:: python

    try:
        import cPickle as pickle
    except:
        import pickle
    import pprint
    from StringIO import StringIO

    class SimpleObject(object):
        def __init__(self, name):
            self.name = name
            l = list(name)
            l.reverse()
            self.name_backwards = ''.join(l)
            return
    
    data = []
    data.append(SimpleObject('pickle'))
    data.append(SimpleObject('cPickle'))
    data.append(SimpleObject('last'))
        
    # Simulate a file with StringIO
    out_s = StringIO()

    # Write to the stream
    for o in data:
        print 'WRITING: %s (%s)' % (o.name, o.name_backwards)
        pickle.dump(o, out_s)
        out_s.flush()

    # Set up a read-able stream
    in_s = StringIO(out_s.getvalue())

    # Read the data
    while True:
        try:
            o = pickle.load(in_s)
        except EOFError:
            break
        else:
            print 'READ: %s (%s)' % (o.name, o.name_backwards)

这个例子使用StringIO缓冲区来模拟流, 因此我们在建立可读流时得玩点小花样. 一个简单数据库格式也可以使用pickle来存储对象, 虽然使用shelve模块可能会更简单.

::

   $ python pickle_stream.py
   WRITING: pickle (elkcip)
   WRITING: cPickle (elkciPc)
   WRITING: last (tsal)
   READ: pickle (elkcip)
   READ: cPickle (elkciPc)
   READ: last (tsal)

除了用于存储数据, pickle在用于内部进程通信时是非常灵活的. 比如, 使用os.fork()和os.pipe(), 可以建立一些工作进程, 它们从一个管道中读取任务说明并把结果输出到另一个管道. 操作这些工作池、发送任务和接受反应的核心代码可以重复利用, 因为任务和反应对象不是一个特殊的类. 如果你使用管道或者sockets, 就不要忘记在dump每个对象后刷新它们并通过其间的连接将数据推送到另外一个进程.

在处理自定义类时, 你应该保证这些被pickled的类会在进程名空间出现. 只有数据实例才能被pickle, 而不能是定义的类. 在unpickle时, 类的名字被用于寻找构造器以便创建新对象. 接下来这个例子, 是将一个类实例写入到文件中:

.. code-block:: python

    try:
        import cPickle as pickle
    except:
        import pickle
        import sys

    class SimpleObject(object):
        def __init__(self, name):
            self.name = name
            l = list(name)
            l.reverse()
            self.name_backwards = ''.join(l)
            return
        
    if __name__ == '__main__':
        data = []
        data.append(SimpleObject('pickle'))
        data.append(SimpleObject('cPickle'))
        data.append(SimpleObject('last'))
        try:
            filename = sys.argv[1]
            except IndexError:
            raise RuntimeError('Please specify a filename as an argument to %s' % sys.argv[0])
        out_s = open(filename, 'wb')
        try:
            # Write to the stream
            for o in data:
                print 'WRITING: %s (%s)' % (o.name, o.name_backwards)
                pickle.dump(o, out_s)
        finally:
            out_s.close()
        
当我运行这个脚本时, 它会创建名为我在命令行中输入的参数的文件:

::

   $ python pickle_dump_to_file_1.py test.dat
   WRITING: pickle (elkcip)
   WRITING: cPickle (elkciPc)
   WRITING: last (tsal)

一个简单的尝试将刚才的pickle结果对象装载进来可以是如下的样子:

.. code-block:: python

    try:
        import cPickle as pickle
    except:
        import pickle
    import pprint
    from StringIO import StringIO
    import sys

    try:
        filename = sys.argv[1]
    except IndexError:
        raise RuntimeError('Please specify a filename as an argument to %s' % sys.argv[0])

    in_s = open(filename, 'rb')
    try:
        # Read the data
        while True:
            try:
                o = pickle.load(in_s)
            except EOFError:
                break
            else:
                print 'READ: %s (%s)' % (o.name, o.name_backwards)
    finally:
        in_s.close()

这个版本失败了, 因为这里没有可用的SimpleObject类.

::

   $ python pickle_load_from_file_1.py test.dat
   Traceback (most recent call last):
   File "pickle_load_from_file_1.py", line 52, in 
      o = pickle.load(in_s)
   AttributeError: 'module' object has no attribute 'SimpleObject'

一个正确版本, 它从pickle_dump_to_file_1导入了SimpleObject类, 可以成功运行.
增加:

.. code-block:: python

    from pickle_dump_to_file_1 import SimpleObject

到导入列表的最后, 然后运行这个脚本:

::

   $ python pickle_load_from_file_2.py test.dat
   READ: pickle (elkcip)
   READ: cPickle (elkciPc)
   READ: last (tsal)

在pickle那些不能被pickle的数据(如sockets、文件句柄、数据库连接等等)时, 需要考虑一些特殊之处. 那些不能被pickle的类可以定义__getstate__()和__setstate__()来返回实例在被pickle时的状态. 新风格的类也可以定义__getnewargs__(), 它返回传递给类内存分配者(C.__new__())的参数. 关于这些特征的更详细的使用描述可以在标准库文档中找到.

参考
-----

* `Pickle: An interesting stack language by Alexandre Vassalotti <http://peadrop.com/blog/2007/06/18/pickle-an-interesting-stack-language/>`_
