PyMOTW: itertools
===================

.. currentmodule:: itertools

* 模块： itertools
* 目的： 用于高效循环的迭代函数
* python版本： 2.3+


描述
----

这个模块中提供的函数具有和"lazy functional programming language" `Haskell <http://www.haskell.org/>`_ 和 `SML <http://en.wikipedia.org/wiki/Standard_ML>`_ 相似的特点. 他们都是为了跑得更快和更有效的使用内存. 但他们也被牵扯在一起以表示更为复杂的迭代算法.

由于某些原因, 基于迭代的代码可能更优于使用列表的代码. 由于数据只有在需要它的时候才产生, 所以所有的数据不会同时被存储在内存中.节省内存使用可以减少数据的交换次数和其他大数据集操作的副作用, 从而提高性能.

以下所有的例子都是使用from itertools import * 来导入itertools的.

合并和切分迭代器
-----------------

``chain()`` 函数将多个迭代器作为参数, 但只返回单个迭代器, 它产生所有参数迭代器的内容, 就好像他们是来自于一个单一的序列.

.. code-block:: python

    for i in chain([1, 2, 3], ['a', 'b', 'c']):
        print i

::

   $ python itertools_chain.py 
   1
   2
   3
   a
   b
   c

``izip()`` 函数返回一个合并了多个迭代器为一个元组的迭代器. 它类似于内置函数zip(), 只是它返回的是一个迭代器而不是一个列表.

.. code-block:: python

    for i in izip([1, 2, 3], ['a', 'b', 'c']):
        print i

::
 
   $ python itertools_izip.py 
   (1, 'a')
   (2, 'b')
   (3, 'c')

``islice()`` 函数返回的迭代器是返回了输入迭代器根据索引来选取的项.

.. code-block:: python

    print 'Stop at 5:'
    for i in islice(count(), 5):
        print i

::

   class count(__builtin__.object)
     |  count([firstval]) --> count object
     |  
     |  Return a count object whose .next() method returns consecutive
     |  integers starting from zero or, if specified, from firstval.

::

   Stop at 5:
   0
   1
   2
   3
   4

它可以使用和列表的slice操作相同的参数: start, stop和step. start和step参数是可选的.

.. code-block:: python

    print 'Start at 5, Stop at 10:'
    for i in islice(count(), 5, 10):
        print i


::

   Start at 5, Stop at 10:
   5
   6
   7
   8
   9

.. code-block:: python

    print 'By tens to 100:'
    for i in islice(count(), 0, 100, 10):
        print i

::

   By tens to 100:
   0
   10
   20
   30
   40
   50
   60
   70
   80
   90

``tee()`` 函数返回一些基于单个原始输入的独立迭代器(默认为2). 它和Unix上的tee工具有点语义相似, 也就是说它们都重复读取输入设备中的值并将值写入到一个命名文件和标准输出中.

.. code-block:: python

    r = islice(count(), 5)
    i1, i2 = tee(r)

    for i in i1:
        print 'i1:', i
    for i in i2:
        print 'i2:', i

::

   $ python itertools_tee.py
   i1: 0
   i1: 1
   i1: 2
   i1: 3
   i1: 4
   i2: 0
   i2: 1
   i2: 2
   i2: 3
   i2: 4

因为 ``tee()`` 新建的迭代器共享了输入, 所以你就不需要使用原始的迭代器. 如果你使用了原始输入中的值, 新的迭代器就不会产生对应的值:

.. code-block:: python

    r = islice(count(), 5)
    i1, i2 = tee(r)

    for i in r:
        print 'r:', i
        if i > 1:
            break

    for i in i1:
        print 'i1:', i
    for i in i2:
        print 'i2:', i

::

   $ python itertools_tee_error.py
   r: 0
   r: 1
   r: 2 
   i1: 3
   i1: 4
   i2: 3
   i2: 4

转换输入
---------

``imap()`` 函数返回一个迭代器, 它是调用了一个其值在输入迭代器上的函数, 返回结果. 它类似于内置函数 ``map()`` , 只是前者在任意输入迭代器结束后就停止(而不是插入None值来补全所有的输入).

在下面的第一个例子中, lambda函数将输入的值乘上2:

.. code-block:: python
  
    print 'Doubles:'
    for i in imap(lambda x:2*x, xrange(5)):
        print i

::

   $ python itertools_imap.py
   Doubles:
   0
   2
   4
   6
   8

在第二个例子中, lambda函数将2个参数相乘, 这两个参数各自取自两个独立的迭代器并返回一个原始参数和计算结果的元组.

.. code-block:: python

    print 'Multiples:'
    for i in imap(lambda x,y:(x, y, x*y), xrange(5), xrange(5,10)):
        print '%d * %d = %d' % i

::

   Multiples: 
   0 * 5 = 0
   1 * 6 = 6
   2 * 7 = 14
   3 * 8 = 24
   4 * 9 = 36

``starmap()`` 函数类似于 ``imap()`` , 但是在从多个迭代器中构造元组时, 它先将各个项切分成单个迭代器并将它作为参数以*语法传递给映射函数. ``imap()`` 的映射函数被称为f(i1, i2), ``startmap()`` 的映射函数被称为f(*i).

.. code-block:; python

    values = [(0, 5), (1, 6), (2, 7), (3, 8), (4, 9)]
    for i in starmap(lambda x,y:(x, y, x*y), values):
        print '%d * %d = %d' % i

::
 
   $ python itertools_starmap.py 
   0 * 5 = 0
   1 * 6 = 6
   2 * 7 = 14
   3 * 8 = 24
   4 * 9 = 36

产生新值
---------

``count()`` 函数返回一个不断产生连续整数的迭代器. 第一个数可以由参数指定, 默认为0. 它没有上届参数(可参见内置函数 ``xrange()`` , 它更好的控制结果集). 在下面的例子中, 迭代器由于参数列表结束而停止.

.. code-block:: python

    for i in izip(count(1), ['a', 'b', 'c']):
         print i

:: 

   $ python itertools_count.py 
   (1, 'a')
   (2, 'b')
   (3, 'c')

``cycle()`` 函数返回一个不断重复参数内容的迭代器. 由于它必须记住整个输入迭代器的内容, 所以如果输入迭代器很长的话, 它可能会消耗大量的内存. 在下面的例子中, 一个计数变量用于在一定数量的循环后, 跳出循环.

.. code-block:: python

    i = 0
    for item in cycle(['a', 'b', 'c']):
        i += 1
        if i == 10:
            break
        print (i, item)

::

   $ python itertools_cycle.py
   (1, 'a')
   (2, 'b')
   (3, 'c')
   (4, 'a')
   (5, 'b')
   (6, 'c')
   (7, 'a')
   (8, 'b')
   (9, 'c')

``repeat()`` 函数返回一个每次都产生相同值的迭代器. 它也是永远继续的, 除非你设置了times参数来限制.

.. code-block:: python

    for i in repeat('over-and-over', 5):
        print i

::

   $ python itertools_repeat.py 
   over-and-over
   over-and-over
   over-and-over
   over-and-over
   over-and-over

当其他迭代器使用的是一个固定值时, 将 ``repeat()`` 和 ``izip()`` 或 ``imap()`` 联合起来使用是非常有用的.

.. code-block:: python

    for i, s in izip(count(), repeat('over-and-over', 5)):
         print i, s

::

   $ python itertools_repeat_izip.py 
   0 over-and-over
   1 over-and-over
   2 over-and-over
   3 over-and-over
   4 over-and-over

.. code-block:; python

    for i in imap(lambda x,y:(x, y, x*y), repeat(2), xrange(5)):
         print '%d * %d = %d' % i

::

   $ python itertools_repeat_imap.py 
   2 * 0 = 0
   2 * 1 = 2
   2 * 2 = 4
   2 * 3 = 6
   2 * 4 = 8

过滤
-----

``dropwhile()`` 函数返回一个当条件为false之后的输入迭代器中剩余元素的迭代器. 它不过滤输入迭代器中的每一个项; 在条件为false之后的第一次, 返回迭代器中剩下来的项.

.. code-block:: python

    def should_drop(x):
        print 'Testing:', x
        return (x<1)

    for i in dropwhile(should_drop, [ -1, 0, 1, 2, 3, 4, 1, -2 ]): 
        print 'Yielding:', i

::

   $ python itertools_dropwhile.py 
   Testing: -1
   Testing: 0
   Testing: 1
   Yielding: 1
   Yielding: 2
   Yielding: 3
   Yielding: 4
   Yielding: 1
   Yielding: -2

和 ``dropwhile()`` 相反的是, ``tabkewhile()`` , 它返回的是一个产生输入迭代器中只要测试函数返回true的项的迭代器.

.. code-block:: python

    def should_take(x):
        print 'Testing:', x
        return (x<2)

    for i in takewhile(should_take, [ -1, 0, 1, 2, 3, 4, 1, -2 ]): 
        print 'Yielding:', i

::

   $ python itertools_takewhile.py
   Testing: -1
   Yielding: -1
   Testing: 0
   Yielding: 0
   Testing: 1
   Yielding: 1
   Testing: 2

``ifilter()`` 返回的是迭代器类似于针对列表的内置函数 ``filter()`` , 它只包括当测试函数返回true时的项. 它不同于 ``dropwhile()`` 的是每个项是在被返回之前进行测试的. 

.. code-block:: python

    def check_item(x):
        print 'Testing:', x
        return (x<1)

    for i in ifilter(check_item, [ -1, 0, 1, 2, 3, 4, 1, -2 ]):
        print 'Yielding:', i

::

   $ python itertools_ifilter.py 
   Testing: -1
   Yielding: -1
   Testing: 0
   Yielding: 0
   Testing: 1
   Testing: 2
   Testing: 3
   Testing: 4
   Testing: 1
   Testing: -2
   Yielding: -2

和 ``ifilter()`` 函数相反的是, ``ifilterfalse()`` 返回一个包含那些测试函数返回false的项的迭代器.

.. code-block:: python

    def check_item(x):
        print 'Testing:', x
        return (x<1)

    for i in ifilterfalse(check_item, [ -1, 0, 1, 2, 3, 4, 1, -2 ]):
        print 'Yielding:', i

::

   $ python itertools_ifilterfalse.py Testing: -1
   Testing: 0
   Testing: 1
   Yielding: 1
   Testing: 2
   Yielding: 2
   Testing: 3
   Yielding: 3
   Testing: 4
   Yielding: 4
   Testing: 1
   Yielding: 1
   Testing: -2

分组数据
--------

``groupby()`` 函数返回一个产生按照key进行分组后的值集合的迭代器.

下面的例子来自于标准库文档, 它表明怎样将一个字典根据值将关键字分组.

.. code-block:: python

    from itertools import *
    from operator import itemgetter

    d = dict(a=1, b=2, c=1, d=2, e=1, f=2, g=3)
    di = sorted(d.iteritems(), key=itemgetter(1))
    for k, g in groupby(di, key=itemgetter(1)):
        print k, map(itemgetter(0), g)

::

   $ python itertools_groupby.py
   1 ['a', 'c', 'e']
   2 ['b', 'd', 'f']
   3 ['g']

下面一个更复杂的例子说明了如何基于一些属性来对值进行分组的. 注意了, 输入的序列需要按照关键字进行排序, 这样就可以得到预期的分组结果了:

.. code-block:: python

    class Point:
        def __init__(self, x, y):
            self.x = x
            self.y = y
        
        def __repr__(self):
            return 'Point(%s, %s)' % (self.x, self.y)
 
        def __cmp__(self, other):
            return cmp((self.x, self.y), (other.x, other.y)) ## 比较

    # Create a dataset of Point instances
    data = list(imap(Point, cycle(islice(count(), 3)), islice(count(), 10),))
    print 'Data:', data
    print

    # Try to group the unsorted data based on X values
    print 'Grouped, unsorted:'
    for k, g in groupby(data, lambda o:o.x):
        print k, list(g)
    print

    # Sort the data
    data.sort()
    print 'Sorted:', data
    print

    # Group the sorted data based on X values
    print 'Grouped, sorted:'
    for k, g in groupby(data, lambda o:o.x):
        print k, list(g)
    print

::

   $ python itertools_groupby_seq.py
   Data: [Point(0, 0), Point(1, 1), Point(2, 2), Point(0, 3), 
     Point(1, 4), Point(2, 5), Point(0, 6), Point(1, 7), 
     Point(2, 8), Point(0, 9)]

   Grouped, unsorted:
   0 [Point(0, 0)]
   1 [Point(1, 1)]
   2 [Point(2, 2)]
   0 [Point(0, 3)]
   1 [Point(1, 4)]
   2 [Point(2, 5)]
   0 [Point(0, 6)]
   1 [Point(1, 7)]
   2 [Point(2, 8)]
   0 [Point(0, 9)]

   Sorted: [Point(0, 0), Point(0, 3), Point(0, 6), Point(0, 9), 
     Point(1, 1), Point(1, 4), Point(1, 7), Point(2, 2), 
     Point(2, 5), Point(2, 8)]

   Grouped, sorted:
   0 [Point(0, 0), Point(0, 3), Point(0, 6), Point(0, 9)]
   1 [Point(1, 1), Point(1, 4), Point(1, 7)]
   2 [Point(2, 2), Point(2, 5), Point(2, 8)]

参考
-----

* `The Standard ML Basis Library <http://www.standardml.org/Basis/>`_
* `Definition of Haskell and the Standard Libraries <http://www.haskell.org/definition/>`_
