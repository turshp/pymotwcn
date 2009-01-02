PyMOTW: Cookie
================

.. currentmodule:: Cookie

* 模块： Cookie
* 目的： 处理来自服务器端的HTTP cookies
* python版本： 2.1+


描述
----

很久以前，Cookies就已成为HTTP协议的一部分。现有的web开发框架提供了简单的访问cookies的接口。因此，程序员几乎不用担心怎样去格式化cookies数据或者确保头的正确发送。明白cookies是怎样工作以及有哪些工作模式是很让人受启发的事情。

Cookie模块实现了对cookies的解析，其大多是兼容RFC 2109的。它没有严重按照标准是因为MSIE 3.0x不支持整个标准。

创建和设置Cookie
-------------------

Cookies可以用作状态管理, 通常被服务器存储并由客户端返回。最普通的创建cookies的用法可以如下的样子：

.. code-block:: python

    import Cookie

    c = Cookie.SimpleCookie()
    c['mycookie'] = 'cookie_value'
    print c

输出是一个有效的Set-Cookie头，之后会作为HTTP响应传递给客户端。

::

   $ python Cookie_setheaders.py
   Set-Cookie: mycookie=cookie_value

Morsels
---------

控制cookie的其他方面也是有必要的，比如说期限、路径、域。事实上，RFC对应的所有的cookies属性可以通过代表cookie值的Morsel对象来操作。

.. code-block:: python

    import Cookie
    import datetime

    def show_cookie(c):
        print c
        for key, morsel in c.iteritems():
        print
        print 'key =', morsel.key
        print ' value =', morsel.value
        print ' coded_value =', morsel.coded_value
        for name in morsel.keys():
            if morsel[name]:
                print ' %s = %s' % (name, morsel[name])

    c = Cookie.SimpleCookie()

    # 一个cookie, 其值必须经过编码以符合头的标准.
    c['encoded_value_cookie'] = '"cookie_value"'
    c['encoded_value_cookie']['comment'] = 'Notice that this cookie value has escaped quotes'

    # 一个cookie, 仅适用于部分网站
    c['restricted_cookie'] = 'cookie_value'
    c['restricted_cookie']['path'] = '/sub/path'
    c['restricted_cookie']['domain'] = 'PyMOTW'
    c['restricted_cookie']['secure'] = True

    # 一个cookie, 期限为5分钟
    c['with_max_age'] = 'expires in 5 minutes'
    c['with_max_age']['max-age'] = 300 # seconds 以秒为单位

    # 一个cookie, 期限为某个指定的时间
    c['expires_at_time'] = 'cookie_value'
    expires = datetime.datetime.now() + datetime.timedelta(hours=1)
    c['expires_at_time']['expires'] = expires.strftime('%a, %d %b %Y %H:%M:%S')
    
    show_cookie(c)

以上的例子包括了两个不同的设置cookies期限的方法。你可以设置max-age为一些秒数，或者指定一个cookie失效的时间和日期。

::

   $ python Cookie_Morsel.py
   Set-Cookie: encoded_value_cookie="\"cookie_value\""; Comment=Notice that this cookie value has escaped quotes
   Set-Cookie: expires_at_time=cookie_value; expires=Sun, 01 Jun 2008 11:37:00
   Set-Cookie: restricted_cookie=cookie_value; Domain=PyMOTW; Path=/sub/path; secure
   Set-Cookie: with_max_age="expires in 5 minutes"; Max-Age=300

   key = restricted_cookie
   value = cookie_value
   coded_value = cookie_value
   domain = PyMOTW
   secure = True
   path = /sub/path

   key = with_max_age
   value = expires in 5 minutes
   coded_value = "expires in 5 minutes"
   max-age = 300

   key = encoded_value_cookie
   value = "cookie_value"
   coded_value = "\"cookie_value\""
   comment = Notice that this cookie value has escaped quotes

   key = expires_at_time
   value = cookie_value
   coded_value = cookie_value
   expires = Sun, 01 Jun 2008 11:37:00

Cookie和Morsel对象都像是一个字典。Morsel对应以下固定的键值：

- expires 期限
- path 路径
- comment 注释
- domain 域
- max-age 最大时间
- secure 安全性
- version 版本

一个Cookie对象的键是一些独立的会被cookie存储的名字。来自于Morsel的键属性的信息也是可用的。

编码后的值
-----------

cookie头可能会需要编码后的值以便它们被正确的解析。

.. code-block:: python

    import Cookie

    c = Cookie.SimpleCookie()
    c['integer'] = 5
    c['string_with_quotes'] = 'He said, "Hello, World!"'

    for name in ['integer', 'string_with_quotes']:
        print c[name].key
        print ' %s' % c[name]
        print ' value=%s' % c[name].value, type(c[name].value)
        print ' coded_value=%s' % c[name].coded_value
        print

Morsel.value常常是cookie中已经被解码的值，而 ``Morsel.coded_value`` 的值是以一种符合传递给客户端要求的形式来表示的。

::

   $ python Cookie_coded_value.py
   integer
     Set-Cookie: integer=5
     value=5 <type 'str'>
     coded_value=5

   string_with_quotes
     Set-Cookie: string_with_quotes="He said, \"Hello, World!\""
     value=He said, "Hello, World!" <type 'str'>
     coded_value="He said, \"Hello, World!\""

接收和解析Cookie头
--------------------

一旦客户端收到Set-Cookie头，它会将这些cookies在接下来的请求中作为新的Cookie头返回给服务器。那么传入的头看起来是：

::

   Cookie: integer=5; string_with_quotes="He said, \"Hello, World!\""


cookies既可以直接从HTTP响应头，或环境变量HTTP_COOKIE，这依赖于你的web服务器/框架。实例化时，将经过解码的没有头前缀的字符串传递给SimpleCookie，或者使用 ``load()`` 。

.. code-block:: python

    import Cookie

    HTTP_COOKIE = r'integer=5; string_with_quotes="He said, \"Hello, World!\""'

    print 'From constructor:'
    c = Cookie.SimpleCookie(HTTP_COOKIE)
    print c

    print
    print 'From load():'
    c = Cookie.SimpleCookie()
    c.load(HTTP_COOKIE)
    print c


::

   $ python Cookie_parse.py
   From constructor:
   Set-Cookie: integer=5
   Set-Cookie: string_with_quotes="He said, \"Hello, World!\""

   From load():
   Set-Cookie: integer=5
   Set-Cookie: string_with_quotes="He said, \"Hello, World!\""


选择输出格式
--------------

除了使用Set-Cookie头外，使用JavaScript给客户端增加cookies也是可以的。SimpleCookie和Morsel提供一种JavaScript输出格式，通过使用 ``js_output()`` 方法：

.. code-block:: python

    import Cookie

    c = Cookie.SimpleCookie()
    c['mycookie'] = 'cookie_value'
    c['another_cookie'] = 'second value'
    print c.js_output()


::

   $ python Cookie_js_output.py

    <script type="text/javascript">
    <!-- begin hiding
    document.cookie = "another_cookie="second value"";
    // end hiding -->
    </script>
         
    <script type="text/javascript">
    <!-- begin hiding
    document.cookie = "mycookie=cookie_value";
    // end hiding -->
    </script> 

不推荐使用的类
-----------------

上面所有的例子中都是使用的SimpleCookie类。Cookie模块也提供2个其他的类，SerialCookie和SmartCookie。SerialCookie可以处理任何可以被pickle的值。SmartCookie指明了一个值是否需要被unpickle或者是否是一个简单的值。由于他们两者都使用了pickle，他们是你应用中的潜在安全漏洞，所以你最好不要使用他们。在服务器上存贮cookie状态。然后传递给客户端一个会话key，这是更安全的。


参考
-----

* `cookielib <http://docs.python.org/lib/module-cookielib.html>`_
* `RFC 2109, HTTP State Management Mechanism <http://www.ietf.org/rfc/rfc2109.txt>`_
