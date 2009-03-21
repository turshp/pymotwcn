PyMOTW: pprint
=================

.. currentmodule:: pprint

* 模块： pprint
* 目的： 用于更加好看的显示数据
* python版本： 1.4+

pprint模块让你的数据的显示结构更加美观.

描述
----

pprint模块中使用的格式化可以按照一种格式正确的显示数据, 这种格式即可被解析器解析, 又很易读. 输出保存在一个单行内, 但如果有必要, 在分割多行数据时也可使用缩进表示.

这里的例子全部依赖于pprint_data.py这个脚本, 它包含:

::

   data = [ (i, { 'a':'A',
    'b':'B',
    'c':'C',
    'd':'D',
    'e':'E',
    'f':'F',
    'g':'G',
    'h':'H',
    })
    for i in xrange(3)
    ]

输出
-----

使用这个模块的最简单方式是使用 ``pprint()`` 函数. 它格式化你的对象并作为参数写入到数据流中(默认为sys.stdout)中.

.. code-block:: python

    from pprint import pprint
    from pprint_data import data

    print 'PRINT:'
    print data
    print
    print 'PPRINT:'
    pprint(data)

::

   $ python pprint_pprint.py
   PRINT:
   [(0, {'a': 'A', 'c': 'C', 'b': 'B', 'e': 'E', 'd': 'D', 'g': 'G', 'f': 'F', 'h': 'H'}), (1, {'a': 'A', 'c': 'C', 'b': 'B', 'e': 'E', 'd': 'D', 'g': 'G', 'f': 'F', 'h': 'H'}), (2, {'a': 'A', 'c': 'C', 'b': 'B', 'e': 'E', 'd': 'D', 'g': 'G', 'f': 'F', 'h': 'H'})]


   PPRINT:
   [(0,
    {'a': 'A',
    'b': 'B',
    'c': 'C',
    'd': 'D',
    'e': 'E',
    'f': 'F',
    'g': 'G',
    'h': 'H'}),
    (1,
    {'a': 'A',
    'b': 'B',
    'c': 'C',
    'd': 'D',
    'e': 'E',
    'f': 'F',
    'g': 'G',
    'h': 'H'}),
    (2,
    {'a': 'A',
    'b': 'B',
    'c': 'C',
    'd': 'D',
    'e': 'E',
    'f': 'F',
    'g': 'G',
    'h': 'H'})]

格式化
--------

如果你需要格式化一个数据结构, 但不想直接写入到流中(比如, 为了记录日志), 你可以使用 ``pformat()`` 来构建一个字符串传递给其他函数.

.. code-block:: python

    import logging
    from pprint import pformat
    from pprint_data import data

    logging.basicConfig(level=logging.DEBUG,
     format='%(asctime)s %(levelname)-8s %(message)s',
    )

    logging.debug('Logging pformatted data')
    logging.debug(pformat(data))

::

   $ python pprint_pformat.py
   2007-10-21 18:10:32,881 DEBUG Logging pformatted data
   2007-10-21 18:10:32,884 DEBUG [(0,
   {'a': 'A',
    'b': 'B',
    'c': 'C',
    'd': 'D',
    'e': 'E',
    'f': 'F',
    'g': 'G',
    'h': 'H'}),
    (1,
    {'a': 'A',
    'b': 'B',
    'c': 'C',
    'd': 'D',
    'e': 'E',
    'f': 'F',
    'g': 'G',
    'h': 'H'}),
    (2,
    {'a': 'A',
    'b': 'B',
    'c': 'C',
    'd': 'D',
    'e': 'E',
    'f': 'F',
    'g': 'G',
    'h': 'H'})]

其他类
--------

``pprint()`` 中使用到的PrettyPrinter类也支持自定义类, 前提是在自定义类中, 定义了 ``__repr__`` 方法.

.. code-block:: python

    from pprint import pprint

    class node(object):
        def __init__(self, name, contents=[]):
            self.name = name
            self.contents = contents[:]
        
        def __repr__(self):
            return 'node(' + repr(self.name) + ', ' + repr(self.contents) + ')'

    trees = [ node('node-1'),
        node('node-2', [ node('node-2-1')]),
        node('node-3', [ node('node-3-1')]),
    ]
    pprint(trees)

::

    $ python pprint_arbitrary_object.py
    [node('node-1', []),
     node('node-2', [node('node-2-1', [])]),
     node('node-3', [node('node-3-1', [])])]

递归
------

递归的数据可用一个指向原始数据的引用来表示, 具体的形式为 *<Recursion on typename with id=number>*. 例如:

.. code-block:: python

    local_data = [ 'a', 'b', 1, 2 ]
    local_data.append(local_data)

    print 'id(local_data) =>', id(local_data)
    pprint(local_data)

::

   $ python pprint_recursion.py
   id(local_data) => 486936
   ['a', 'b', 1, 2, <Recursion on list with id=486936>]

限制嵌套输出
---------------

对于每一个深层次的数据结构, 你可能不想输出所有的细节. 也可能无法适当的格式化数据, 或者要格式化的文本很大而难控制, 或者你可能需要全部使用. 在这种情况下, 指定depth参数可控制嵌套数据结构显示的深度.

.. code-block:: python

    from pprint import pprint
    from pprint_data import data

    pprint(data, depth=1)

::

    $ python pprint_depth.py 
    [(0, {...}), (1, {...}), (2, {...})]

控制输出宽度
-------------

默认的格式化文本输出宽度是80列. 指定 ``pprint()`` 中的width参数可以调整文本输出宽度.

.. code-block:: python

    from pprint import pprint
    from pprint_data import data

    for d in data:
        for c in 'defgh':
            del d[1][c]

    for width in [ 80, 20, 5 ]:
        print 'WIDTH =', width
        pprint(data, width=width)
        print

注意: 当width被定义的太小而不能容纳所有的格式化数据时, 行是不会被截断. 如果有出现无效的语法时, 也不会被包裹起来.

::

   $ python pprint_width.py 
   WIDTH = 80
   [(0, {'a': 'A', 'b': 'B', 'c': 'C'}),
    (1, {'a': 'A', 'b': 'B', 'c': 'C'}),
    (2, {'a': 'A', 'b': 'B', 'c': 'C'})]

   WIDTH = 20
   [(0,
    {'a': 'A',
    'b': 'B',
    'c': 'C'}),
    (1,
    {'a': 'A',
    'b': 'B',
    'c': 'C'}),
    (2,
    {'a': 'A',
    'b': 'B',
    'c': 'C'})]
    
   WIDTH = 5
   [(0,
    {'a': 'A',
    'b': 'B',
    'c': 'C'}),
    (1,
    {'a': 'A',
    'b': 'B',
    'c': 'C'}),
    (2,
    {'a': 'A',
    'b': 'B',
    'c': 'C'})]

