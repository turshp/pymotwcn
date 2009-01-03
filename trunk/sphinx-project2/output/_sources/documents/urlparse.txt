PyMOTW: urlparse
==================

.. currentmodule:: urlparse

urlparse模块提供了切分统一资源定位符(URL)的接口。

* 模块： urlparse
* 目的： 将URL切分为几个组成部分。
* python版本： 1.4+


描述
----

urlparse模块提供了一些将URL切分成对应与RFC中定义的组成部分的函数。

Parsing:分解
--------------

urlparse函数返回的值是一个包含6个元素的类似于元组的对象。

.. code-block:: python

    from urlparse import urlparse
    parsed = urlparse('http://netloc/path;parameters?query=argument#fragment')
    print parsed

通过借口可以获得URL的各部分组成，网络位置，路径，参数，查询变量和剩余的部分。在下面的例子中，使用http语法来代替"scheme"。

::

   $ python urlparse_urlparse.py 
   ('http', 'netloc', '/path', 'parameters', 'query=argument', 'fragment')

虽然返回的值是类似于元组，但它不是元组的子类，它支持通过属性名字而不是索引来获取URL对应的部分。这在当你不记得索引顺序时是非常有用的。除了让程序员更容易的使用外，这些属性API还可以获得一些在元组API中不可用的值。

.. code-block:: python

    from urlparse import urlparse
    parsed = urlparse('http://user:pass@NetLoc:80/path;parameters?query=argument#fragment')
    print 'scheme :', parsed.scheme
    print 'netloc :', parsed.netloc
    print 'path :', parsed.path
    print 'params :', parsed.params
    print 'query :', parsed.query
    print 'fragment:', parsed.fragment
    print 'username:', parsed.username
    print 'password:', parsed.password
    print 'hostname:', parsed.hostname, '(netloc in lower case)'
    print 'port :', parsed.port

当URL中有包含用户名和密码时username和password就会有对应值，如果没有出现则为空。hostname和netloc的值是一样的，但所有字符被强制转换为小写字母。如果出现端口的话，port值被转换成一个对应的整数值，如果没有出现则为None。

::

   $ python urlparse_urlparseattrs.py 
   scheme : http
   netloc : user:pass@NetLoc:80
   path : /path
   params : parameters
   query : query=argument
   fragment: fragment
   username: user
   password: pass
   hostname: netloc (netloc in lower case)
   port : 80

``urlsplit()`` 函数是 ``urlparse()`` 的一种替代函数。它不将参数从URL中切分出来。这对于遵循RFC 2396标准的URL, 即支持每段路径中包含参数时，是很有用的。

.. code-block:: python

    from urlparse import urlsplit
    parsed = urlsplit('http://user:pass@NetLoc:80/path;parameters/path2;parameters2?query=argument#fragment')
    print parsed
    print 'scheme :', parsed.scheme
    print 'netloc :', parsed.netloc
    print 'path :', parsed.path
    print 'query :', parsed.query
    print 'fragment:', parsed.fragment
    print 'username:', parsed.username
    print 'password:', parsed.password
    print 'hostname:', parsed.hostname, '(netloc in lower case)'
    print 'port :', parsed.port

因为参数没有被切分出来，所以返回的元组只有5个元素而不是6个，因此也没有params属性。

::

   $ python urlparse_urlsplit.py
   ('http', 'user:pass@NetLoc:80', '/path;parameters/path2;parameters2', 'query=argument', 'fragment')
   scheme : http
   netloc : user:pass@NetLoc:80
   path : /path;parameters/path2;parameters2
   query : query=argument
   fragment: fragment
   username: user
   password: pass
   hostname: netloc (netloc in lower case)
   port : 80


为了简单的从URL中获得fragment标识符，因为你有可能需要寻找URL指向的页面中特定的位置名称，可以使用urldefrag。

.. code-block:: python

    from urlparse import urldefrag
    original = 'http://netloc/path;parameters?query=argument#fragment'
    print original
    url, fragment = urldefrag(original)
    print url
    print fragment

返回的是包含基本URL和片段的元组。

::

   $ python urlparse_urldefrag.py
   http://netloc/path;parameters?query=argument#fragment
   http://netloc/path;parameters?query=argument
   fragment

组装
------

有很多方法可以将URL的各个部分组合回原来的单个字符串。被解析后的URL对象有一个叫做 ``geturl()`` 的方法。

.. code-block:: python

    from urlparse import urlparse
    original = 'http://netloc/path;parameters?query=argument#fragment'
    print 'ORIG :', original
    parsed = urlparse(original)
    print 'PARSED:', parsed.geturl()

当然，只有urlparse或者urlsplit返回的对象才起作用。

::

   $ python urlparse_geturl.py 
   ORIG : http://netloc/path;parameters?query=argument#fragment
   PARSED: http://netloc/path;parameters?query=argument#fragment

如果你有一个元组，可以使用 ``urlunparse()`` 将它组装成URL。

.. code-block:: python

    from urlparse import urlparse, urlunparse
    original = 'http://netloc/path;parameters?query=argument#fragment'
    print 'ORIG :', original
    parsed = urlparse(original)
    print 'PARSED:', type(parsed), parsed
    t = parsed[:]
    print 'TUPLE :', type(t), t
    print 'NEW :', urlunparse(t)

urlparse返回的ParseResult可以当元组用，如上面的例子中，创建了一个新的元组，并且urlunparse也可以处理一般的元组。

::

   $ python urlparse_urlunparse.py
   ORIG : http://netloc/path;parameters?query=argument#fragment
   PARSED: <class 'urlparse.ParseResult'> ('http', 'netloc', '/path', 'parameters', 'query=argument', 'fragment')
   TUPLE : <type 'tuple'> ('http', 'netloc', '/path', 'parameters', 'query=argument', 'fragment')
   NEW : http://netloc/path;parameters?query=argument#fragment

如果输入的URL包含多余的部分，那么，这些部分可能会被丢弃。

.. code-block:: python

    from urlparse import urlparse, urlunparse
    original = 'http://netloc/path;?#'
    print 'ORIG :', original
    parsed = urlparse(original)
    print 'PARSED:', type(parsed), parsed
    t = parsed[:]
    print 'TUPLE :', type(t), t
    print 'NEW :', urlunparse(t)

在这个例子中，原始的URL中缺少参数，查询，片段。之后产生新的URL可能和原来的不一样，但是两者是等价的。

::

   $ python urlparse_urlunparseextra.py 
   ORIG : http://netloc/path;?#
   PARSED: <class 'urlparse.ParseResult'> ('http', 'netloc', '/path', '', '', '')
   TUPLE : <type 'tuple'> ('http', 'netloc', '/path', '', '', '')
   NEW : http://netloc/path

连接
------

除了解析URL之外，urlparse模块包含 ``urljoin()`` 函数。用来从关联片段中构造绝对URL。

.. code-block:: python

    from urlparse import urljoin
    print urljoin('http://www.example.com/path/file.html', 'anotherfile.html')
    print urljoin('http://www.example.com/path/file.html', '../anotherfile.html')


.. note::

    相对路径("../")被作为第二URL来计算。

::

   $ python urlparse_urljoin.py
   http://www.example.com/path/anotherfile.html
   http://www.example.com/anotherfile.html

参考
-----

* `RFC 1378 <http://www.faqs.org/rfcs/rfc1738.html>`_
* `RFC 2396 <http://www.faqs.org/rfcs/rfc2396.html>`_
