PyMOTW: Struct
=================

.. currentmodule:: struct

* 模块：Struct
* 目的: 实现字符串和二进制数据之间的相互转换
* python版本：1.4 +

struct模块包含了实现字符串字节和Python本地数据类型(如数字和字符串)间的相互转换的函数.

函数 vs Struct类
-----------------

这里有一系列用来处理结构化数值的模块级函数, 同样存在Struct类(Python 2.5中新加入的). 格式化描述即将字符串格式转化为可编译形式,类似于正则式的方式. 这种转换需要消耗一些资源, 所以一旦创建Struct实例后并调用Struct实例的方法而不使用模块级的方法, 这样是更有效的. 下面举些使用Struct类的例子.


封装和解封
-----------

Structs支持将数据封装成字符串, 也能够通过格式化描述(它是由一些代表特定数据类型的字符, 可选的个数和字节序指示符组成的)从字符串中解封数据. 进一步的细节, 可以参考 `标准库文档 <http://docs.python.org/library/struct.html>`_

在下面的这个例子中, 格式化描述调用了一个整型或者长整型数, 一个2个字符组成的字符串和一个浮点数. 为了清晰描述，在格式化描述中包含了空格，但格式被编译后将忽略这个空格.

.. code-block:: python

    import struct
    import binascii

    values = (1, 'ab', 2.7)
    s = struct.Struct('I 2s f')
    packed_data = s.pack(*values)

    print 'Original values:', values
    print 'Format string  :', s.format
    print 'Uses           :', s.size, 'bytes'
    print 'Packed Value   :', binascii.hexlify(packed_data)


封装后的值被转换成16进制字节流输出, 所以有些字符显示为空.

::

   $ python struct_pack.py
   Original values: (1, 'ab', 2.7000000000000002)
   Format string  : I 2s f
   Uses           : 12 bytes
   Packed Value   : 0100000061620000cdcc2c40

如果我们将封装后的值传递给unpack(), 可以基本上得到原来的数值(注意其中浮点数的差异).

.. code-block:: python

    import struct
    import binascii

    packed_data = binascii.unhexlify('0100000061620000cdcc2c40')

    s = struct.Struct('I 2s f')
    unpacked_data = s.unpack(packed_data)
    print 'Unpacked Values:', unpacked_data

::
   
   $ python struct_unpack.py
   Unpacked Values: (1, 'ab', 2.7000000476837158)

字节序
-------

默认情况下, 使用标准C库中"字节序"的概念将数值编码. 通过在字符串格式中直接指定一个明确的字节序可以简单的覆盖这个选项.

.. code-block:: python

    import struct
    import binascii

    values = (1, 'ab', 2.7)
    print 'Original values:', values

    endianness = [
        ('@', 'native, native'),
        ('=', 'native, standard'),
        ('<', 'little-endian'),
        ('>', 'big-endian'),
        ('!', 'network'),
    ]

    
    for code, name in endianness:
        s = struct.Struct(code + ' I 2s f')
        packed_data = s.pack(*values)
        print
        print 'Format string  :', s.format, 'for', name
        print 'Uses           :', s.size, 'bytes'
        print 'Packed Value   :', binascii.hexlify(packed_data)
        print 'Unpacked Value :', s.unpack(packed_data)

::

   $ python struct_endianness.py
   Original values: (1, 'ab', 2.7000000000000002)

   Format string  : @ I 2s f for native, native
   Uses           : 12 bytes
   Packed Value   : 0100000061620000cdcc2c40
   Unpacked Value : (1, 'ab', 2.7000000476837158)

   Format string  : = I 2s f for native, standard
   Uses           : 10 bytes
   Packed Value   : 010000006162cdcc2c40
   Unpacked Value : (1, 'ab', 2.7000000476837158)

   Format string  : < I 2s f for little-endian
   Uses           : 10 bytes
   Packed Value   : 010000006162cdcc2c40
   Unpacked Value : (1, 'ab', 2.7000000476837158)

   Format string  : > I 2s f for big-endian
   Uses           : 10 bytes
   Packed Value   : 000000016162402ccccd
   Unpacked Value : (1, 'ab', 2.7000000476837158)

   Format string  : ! I 2s f for network
   Uses           : 10 bytes
   Packed Value   : 000000016162402ccccd
   Unpacked Value : (1, 'ab', 2.7000000476837158)

缓冲
------

在高性能的敏感情况或者通过通过第三方模块来传递数据经常会要求对二进制数据进行封装. 一种优化的方式是避免为每一个封装结构分配新的缓冲区. 函数pack_into()和unpack_from()支持直接写入到预分配的缓冲区中.

.. code-block:: python

    import struct
    import binascii

    s = struct.Struct('I 2s f')
    values = (1, 'ab', 2.7)
    print 'Original:', values

    print
    print 'ctypes string buffer'

    import ctypes
    b = ctypes.create_string_buffer(s.size)
    print 'Before  :', binascii.hexlify(b.raw)
    s.pack_into(b, 0, *values)
    print 'After   :', binascii.hexlify(b.raw)
    print 'Unpacked:', s.unpack_from(b, 0)

    print
    print 'array'

    import array
    a = array.array('c', '\0' *s.size)
    print 'Before  :', binascii.hexlify(a)
    s.pack_into(a, 0, *values)
    print 'After   :', binascii.hexlify(a)
    print 'Unpacked:', s.unpack_from(a, 0)

::

   $ python struct_buffers.py

   Original: (1, 'ab', 2.7000000000000002)

   ctypes string buffer
   Before  : 000000000000000000000000
   After   : 0100000061620000cdcc2c40
   Unpacked: (1, 'ab', 2.7000000476837158)

   array
   Before  : 000000000000000000000000
   After   : 0100000061620000cdcc2c40
   Unpacked: (1, 'ab', 2.7000000476837158)

参考
-------

* `struct <http://docs.python.org/library/struct.html>`_
* array：用于处理固定类型的序列.
* binascii：用于产生二进制数据的ASCII表示.
* `WikiPedia: Endianness <http://en.wikipedia.org/wiki/Endianness>`_

字节序, 其实是数据的二进制形式的排列顺序, 在内存存贮顺序, 或者是传输时的顺序, 或者还有其他特殊的规定.

