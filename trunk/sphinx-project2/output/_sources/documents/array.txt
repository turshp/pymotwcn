PyMOTW: array
===============

.. currentmodule:: array

time模块提供了操作日期和时间的函数

* 模块： array
* 目的： 有效管理固定数值序列。
* python版本：1.4+

数组模块定义了一个序列型的数据结构，非常像一个列表，只是其中元素的类型是相同的。支持的数据类型在 `标准库文档 <http://docs.python.org/library/array.html>`_ 中列出了。他们是所有数值型或其他固定大小的基本数据类型，如bytes。


数组的初始化
--------------

一个数组实例化时需要一个描述数据类型的参数，还可能需要一个初始化序列。

.. code-block:: python

    import array
    import binascii

    s = 'This is the array.'
    a = array.array('c', s)

    print 'As string:', s
    print 'As array :', a
    print 'As hex :', binascii.hexlify(a)

    
在这个例子中，数组保存的是一字节序列并且用一个简单的字符串来初始化。

::

   $ python array_string.py
   As string: This is the array.
   As array : array('c', [84, 104, 105, 115, 32, 105, 115,
   32, 116, 104, 101, 32, 97, 114, 114, 97, 121, 46])
   As hex : 54686973206973207468652061727261792e

处理数组
----------

一个数组可以被扩展，否则也可以与其他Python序列的相同的方式处理。

.. code-block:: python

    import array

    a = array.array('i', xrange(5))
    print 'Initial :', a

    a.extend(xrange(5))
    print 'Extended:', a

    print 'Slice :', a[3:6]

    print 'Iterator:', list(enumerate(a))


::

   $ python array_sequence.py
   Initial : array('i', [0, 1, 2, 3, 4])
   Extended: array('i', [0, 1, 2, 3, 4, 0, 1, 2, 3, 4])
   Slice : array('i', [3, 4, 0])
   Iterator: [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4),
   (5, 0), (6, 1), (7, 2), (8, 3), (9, 4)]


数组和文件
------------

使用一些编码高效的内置方法可以从文件中读入一个数组的内容，或者将数组内容写入文件中。

.. code-block:: python

    import array
    import binascii
    import tempfile

    a = array.array('i', xrange(5))
    print 'A1:', a

    # Write the array of numbers to the file
    output = tempfile.NamedTemporaryFile()
    a.tofile(output.file) # must pass an *actual* file
    output.flush()

    # Read the raw data
    input = open(output.name, 'rb')
    raw_data = input.read()
    print 'Raw Contents:', binascii.hexlify(raw_data)

    # Read the data into an array
    input.seek(0)
    a2 = array.array('i')
    a2.fromfile(input, len(a))
    print 'A2:', a2

这个例子中，直接从二进制文件中读取原数据，并将它读入一个新的数组并将其转换为合适的类型。

::

   $ python array_file.py
   A1: array('i', [0, 1, 2, 3, 4])
   Raw Contents: 0000000001000000020000000300000004000000 ## ?
   A2: array('i', [0, 1, 2, 3, 4])

交替字节排序
--------------

如果数组中的数据不是按照本地字节序排列，或者在写入到文件之前需要进行交换来适合不同系统的不同字节序，很容易对整个数组进行这种转换。

.. code-block:: python

    import array

    import binascii

    def to_hex(a):
        chars_per_item = a.itemsize * 2 # 2 hex digits
        hex_version = binascii.hexlify(a)
        num_chunks = len(hex_version) / chars_per_item
        for i in xrange(num_chunks):
            start = i*chars_per_item
            end = start + chars_per_item
            yield hex_version[start:end]

    a1 = array.array('i', xrange(5))
    a2 = array.array('i', xrange(5))
    a2.byteswap()

    fmt = '%10s %10s %10s %10s'
    print fmt % ('A1 hex', 'A1', 'A2 hex', 'A2')
    print fmt % (('-' * 10,) * 4)
    for values in zip(to_hex(a1), a1, to_hex(a2), a2):
        print fmt % values

::

   $ python array_byteswap.py
      A1 hex      A1        A2 hex       A2
    ---------- ---------- ---------- ----------
     00000000     0        00000000       0
     01000000     1        00000001    16777216
     02000000     2        00000002    33554432
     03000000     3        00000003    50331648
     04000000     4        00000004    67108864


参考
------

* `array <http://docs.python.org/library/array.html>`_
* `Numerical Python <http://www.scipy.org/>`_ NumPy是Python针对大数据集的有效处理模块。

