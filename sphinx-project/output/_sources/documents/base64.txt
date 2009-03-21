PyMOTW: base64
===============

.. currentmodule:: base64

* 模块： base64
* 目的： 编码二进制数据转化为ASCII码
* python版本： 1.4+

base64模块提供一些函数l来把二进制数据转换为ASCII集, 通常在明文协议的传输中使用.

描述
----

base64、base32、base16可以分别编码转化8位字节为6位、5位、4位, 允许非ASCII字节以编码为ASCII码的协议中传输, 例如SMTP, "base"值对应是在每一个编码中字母表的长度. 有一些原始编码的url类型会使用略有不同的结果.


Base64 编码
---------------

简单的文本编码示例如下:

.. code-block:: python

    import base64

    initial_data = open(__file__, 'rt').read()

    encoded_data = base64.b64encode(initial_data)

    num_initial = len(initial_data)
    padding = { 0:0, 1:2, 2:1 }[num_initial % 3]

    print '%d bytes before encoding' % num_initial
    print 'Expect %d padding bytes' % padding
    print '%d bytes after encoding' % len(encoded_data)
    print
    print encoded_data
        
输出显示原来529字节的文本在编码之后被扩展到了708个字节, 从编码过程来看, 每一个24位序列(3个字节)作为输入, 输出时候则增加了4个字节, 最后2个字符"==", 则是简单的追加, 因为原始字符串的位数不能被24整除.

在标准输出中时没有很多回车府, 但是为了在文档中有好的可读性, 在如下显示中稍作了变化.

::

   $ python base64_b64encode.py
   529 bytes before encoding
       Expect 2 padding bytes
       708 bytes after encoding

   IyEvdXNyL2Jpbi9lbnYgcHl0aG9uCiMgZW5jb2Rpbmc
   6IHV0Zi04CiMKIyBDb3B5cmlnaHQgKGMpIDIwMDggRG
   91ZyBIZWxsbWFubiBBbGwgcmlnaHRzIHJlc2VydmVkL
   gojCiIiIgoiIiIKCl9fdmVyc2lvbl9fID0gIiRJZDog
   cHltb3R3LnB5IDEyMzkgMjAwOC0wMS0xNiAxMDo1NTo
   xOVogZGhlbGxtYW5uICQiCgppbXBvcnQgYmFzZTY0Cg
   ppbml0aWFsX2RhdGEgPSBvcGVuKF9fZmlsZV9fLCAnc
   nQnKS5yZWFkKCkKCmVuY29kZWRfZGF0YSA9IGJhc2U2
   NC5iNjRlbmNvZGUoaW5pdGlhbF9kYXRhKQoKbnVtX2l
   uaXRpYWwgPSBsZW4oaW5pdGlhbF9kYXRhKQpwYWRkaW
   5nID0geyAwOjAsIDE6MiwgMjoxIH1bbnVtX2luaXRpY
   WwgJSAzXQoKcHJpbnQgJyVkIGJ5dGVzIGJlZm9yZSBl
   bmNvZGluZycgJSBudW1faW5pdGlhbApwcmludCAnRXh
   wZWN0ICVkIHBhZGRpbmcgYnl0ZXMnICUgcGFkZGluZw
   pwcmludCAnJWQgYnl0ZXMgYWZ0ZXIgZW5jb2RpbmcnI
   CUgbGVuKGVuY29kZWRfZGF0YSkKcHJpbnQKcHJpbnQg
   ZW5jb2RlZF9kYXRhCg==

Base64 解码
--------------

编码的字符串可以转换为原来的格式, 利用反向查询, 把4个字节转换为3个字节. b64decode()函数可以帮助你. 

.. code-block:: python

    import base64

    original_string = 'This is the data, in the clear.'
    print 'Original:', original_string

    encoded_string = base64.b64encode(original_string)
    print 'Encoded :', encoded_string

    decoded_string = base64.b64decode(encoded_string)
    print 'Decoded :', decoded_string


::

   $ python base64_b64decode.py
   Original: This is the data, in the clear.
   Encoded : VGhpcyBpcyB0aGUgZGF0YSwgaW4gdGhlIGNsZWFyLg==
   Decoded : This is the data, in the clear.


URL-Safe变化
--------------

默认的base64字母表可能会使用+和/, 而这些字符可能出现在url中, 因此必须为这些字符指定可选择的编码情况, +由a-来代替, (_)来代替/, 其他字母表还是相同.

.. code-block:: python

    import base64

    for original in [ '\xfb\xef', '\xff\xff' ]:
        print 'Original         :', repr(original)
        print 'Standard encoding:', base64.standard_b64encode(original)
        print 'URL-safe encoding:', base64.urlsafe_b64encode(original)
        print

::

   $ python base64_urlsafe.py
   Original         : '\xfb\xef'
   Standard encoding: ++8=
   URL-safe encoding: --8=

   Original         : '\xff\xff'
   Standard encoding: //8=
   URL-safe encoding: __8=

其他编码
------------

除了base 64以外, 还有base 32和base 16(16进制)提供函数用于编码数据.

.. code-block:: python
    
    import base64

    original_string = 'This is the data, in the clear.'
    print 'Original:', original_string

    encoded_string = base64.b32encode(original_string)
    print 'Encoded :', encoded_string

    decoded_string = base64.b32decode(encoded_string)
    print 'Decoded :', decoded_string

::

   $ python base64_base32.py
   Original: This is the data, in the clear.
   Encoded : KRUGS4ZANFZSA5DIMUQGIYLUMEWCA2LOEB2GQZJAMNWGKYLSFY======
   Decoded : This is the data, in the clear.

base 16中的函数是以16进制方式工作.

.. code-block:: python

    import base64

    original_string = 'This is the data, in the clear.'
    print 'Original:', original_string

    encoded_string = base64.b16encode(original_string)
    print 'Encoded :', encoded_string

    decoded_string = base64.b16decode(encoded_string)
    print 'Decoded :', decoded_string

::

   $ python base64_base16.py
   Original: This is the data, in the clear.
   Encoded : 546869732069732074686520646174612C20696E2074686520636C6561722E
   Decoded : This is the data, in the clear.

参考
-----

* `RFC 3548 - The Base16, Base32, and Base64 Data Encodings <http://www.faqs.org/rfcs/rfc3548.html>`_
