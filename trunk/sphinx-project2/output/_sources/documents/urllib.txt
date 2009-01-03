PyMOTW: urllib
================

.. currentmodule:: urllib

urllib模块提供了一个访问网络资源的简单接口。

* 模块：urllib
* 目的：访问不需要认证的远程资源 
* python版本：1.4+

虽然urllib可以与gopher和ftp协议一起使用, 但下面的例子都是用了http协议。

HTTP GET:
----------

这些例子的测试服务器是在BaseHTTPServer_GET.py中, 这个脚本在PyMOTW例子的BaseHTTPServer模块中.在一个终端窗口中启动服务器, 然后在另一个窗口中运行以下这些例子.

HTTP GET 是urllib最简单的操作。简单把URL传递给urlopen()来获取一个用于操作远程数据的类文件句柄。

.. code-block:: python

    import urllib

    response = urllib.urlopen('http://localhost:8080/')
    print 'RESPONSE:', response
    print 'URL :', response.geturl()

    headers = response.info()
    print 'DATE :', headers['date']
    print 'HEADERS :'
    print '---------'
    print headers

    data = response.read()
    print 'LENGTH :', len(data)
    print 'DATA :'
    print '---------'
    print data

该示例服务器取得传入的值，并且返回格式化的纯文本response。从urlopen()返回的值通过info()方法给出HTTP服务器的headers的入口，并且通过read()和readlines()等方法获得远程资源的数据。

::

   $ python urllib_urlopen.py
   RESPONSE: <addinfourl at 10180248 whose fp = <socket._fileobject object at 0x935c30>>
   URL : http://localhost:8080/
   DATE : Sun, 30 Mar 2008 16:27:10 GMT
   HEADERS :
   ---------
   Server: BaseHTTP/0.3 Python/2.5.1
   Date: Sun, 30 Mar 2008 16:27:10 GMT

   LENGTH : 221
   DATA :
   ---------
   CLIENT VALUES:
   client_address=('127.0.0.1', 54354) (localhost)
   command=GET
   path=/
   real path=/
   query=
   request_version=HTTP/1.0

   SERVER VALUES:
   server_version=BaseHTTP/0.3
   sys_version=Python/2.5.1
   protocol_version=HTTP/1.0

类文件对象也是可以迭代的:

.. code-block:: python

    import urllib

    response = urllib.urlopen('http://localhost:8080/')
    for line in response:
        print line.rstrip()

因为返回的每一行都有换行符和完整的框架回车符 -艳 盛 11/21/08 1:31 PM ，所以在输出之前先去掉他们。

::

   $ python urllib_urlopen_iterator.py
   CLIENT VALUES:
   client_address=('127.0.0.1', 54380) (localhost)
   command=GET
   path=/
   real path=/
   query=
   request_version=HTTP/1.0

   SERVER VALUES:
   server_version=BaseHTTP/0.3
   sys_version=Python/2.5.1
   protocol_version=HTTP/1.0

编码参数：
----------

将参数编码并且追加在URL之后，传给服务器。

.. code-block:: python
        
    import urllib
    query_args = { 'q':'query string', 'foo':'bar' }
    encoded_args = urllib.urlencode(query_args) ##这个编码, 是将其转换为a=aa&b=bb的形式
    print 'Encoded:', encoded_args

    url = 'http://localhost:8080/?' + encoded_args
    print urllib.urlopen(url).read()


注意query，在客户端的值的列表中包含了已编码的参数query。

::

   $ python urllib_urlencode.py
   Encoded: q=query+string&foo=bar
   CLIENT VALUES:
   client_address=('127.0.0.1', 54415) (localhost)
   command=GET
   path=/?q=query+string&foo=bar
   real path=/
   query=q=query+string&foo=bar
   request_version=HTTP/1.0

   SERVER VALUES:
   server_version=BaseHTTP/0.3
   sys_version=Python/2.5.1
   protocol_version=HTTP/1.0

在查询字符串中使用单独的变量来传递值序列时, 需传递doseq=True给urlencode()。

.. code-block:: python

    import urllib
    query_args = { 'foo':['foo1', 'foo2'] }
    print 'Single :', urllib.urlencode(query_args)
    print 'Sequence:', urllib.urlencode(query_args, doseq=True)

::

   $ python urllib_urlencode_doseq.py
   Single : foo=%5B%27foo1%27%2C+%27foo2%27%5D
   Sequence: foo=foo1&foo=foo2

为了解码查询字符串，可查看cgi模块中的FieldStorage类。

在查询参数里的一些特别字符，在传递给urlencode()后，在服务器端可能和URL一起引起解析错误。可以直接使用quote()或者quote_plus()函数在本地引用他们以生成安全的字符串。

.. code-block:: python

    import urllib

    url = 'http://localhost:8080/~dhellmann/'
    print 'urlencode() :', urllib.urlencode({'url':url})
    print 'quote() :', urllib.quote(url)
    print 'quote_plus():', urllib.quote_plus(url)

.. note::

    quote_plus()能够替换更多的特殊字符。

::

   $ python urllib_quote.py
   urlencode() : url=http%3A%2F%2Flocalhost%3A8080%2F%7Edhellmann%2F
   quote() : http%3A//localhost%3A8080/%7Edhellmann/
   quote_plus(): http%3A%2F%2Flocalhost%3A8080%2F%7Edhellmann%2F

视情况而定，用unquote()或者unquote_plus()来还原quote操作。

.. code-block:: python

    import urllib

    print urllib.unquote('http%3A//localhost%3A8080/%7Edhellmann/')
    print urllib.unquote_plus('http%3A%2F%2Flocalhost%3A8080%2F%7Edhellmann%2F')

::

   $ python urllib_unquote.py
   http://localhost:8080/~dhellmann/
   http://localhost:8080/~dhellmann/

HTTP POST:
-----------

这些例子的测试服务器是在BaseHTTPServer_POST.py中, 这个脚本在PyMOTW例子的BaseHTTPServer模块中.在一个终端窗口中启动服务器, 然后在另一个窗口中运行以下这些例子.

通过POST代替GET方式传递数据给远程服务器，仅仅是把已编码的查询参数当作数据传递给urlopen().

.. code-block:: python

    import urllib
    query_args = { 'q':'query string', 'foo':'bar' }
    encoded_args = urllib.urlencode(query_args)
    url = 'http://localhost:8080/'
    print urllib.urlopen(url, encoded_args).read()

::

   $ python urllib_urlopen_post.py
   Client: ('127.0.0.1', 54545)
   Path: /
   Form data:
        q=query string
        foo=bar
   
如果服务器需要的不是已编码url形式的参数，你可以传递任一字节字符串作为发送的数据。

Paths vs. URLs:
----------------

一些操作系统使用不同的方法分离本地文件路径和URL。为了使代码简捷，你应该反复地使用函数pathname2url() 和 url2pathname()。因为我在Mac上工作，我必须明确引入Windows上的函数版本。使用由urllib导出的函数版本可以让你默认在正确平台下，因此就不用自己做了。

.. code-block:: python

    import os

    from urllib import pathname2url, url2pathname

    print '== Default =='
    path = '/a/b/c'
    print 'Original:', path
    print 'URL :', pathname2url(path)
    print 'Path :', url2pathname('/d/e/f')
    print

    from nturl2path import pathname2url, url2pathname

    print '== Windows, without drive letter =='
    path = path.replace('/', '\\')
    print 'Original:', path
    print 'URL :', pathname2url(path)
    print 'Path :', url2pathname('/d/e/f')
    print

    print '== Windows, with drive letter =='
    path = 'C:\\' + path.replace('/', '\\')
    print 'Original:', path
    print 'URL :', pathname2url(path)
    print 'Path :', url2pathname('/d/e/f')

有两个Windows例子，分别是路径的前缀中有和没有驱动器名。

::

   $ python urllib_pathnames.py
   == Default ==
   Original: /a/b/c
   URL : /a/b/c
   Path : /d/e/f

   == Windows, without drive letter ==
   Original: \a\b\c
   URL : /a/b/c
   Path : \d\e\f

   == Windows, with drive letter ==
   Original: C:\\a\b\c
   URL : ///C|/a/b/c
   Path : \d\e\f


带Cache简单检索：
------------------

检索数据是常见的操作，urllib包括urlretrieve()函数，因此你不用自己写它。urlretrieve()带有URL中的参数, 一个用于存储数据的临时文件, 一个用于报告下载进度的函数, 和URL中要POST数据。如果没有给定文件名，urlretrieve()就建立一个临时文件。你自己能删除它，或者把它看作一个cache，可以用urlcleanup()移除它。

这个例子使用GET从web服务器中检索数据。

.. code-block:: python

    import urllib
    import os

    def reporthook(blocks_read, block_size, total_size):
        if not blocks_read:
            print 'Connection opened'
            return    
        if total_size < 0:
            # Unknown size 未知大小
            print 'Read %d blocks' % blocks_read
        else:
            amount_read = blocks_read * block_size
            print 'Read %d blocks, or %d/%d' % (blocks_read, amount_read, total_size)
            return

             
     try:
         filename, msg = urllib.urlretrieve('http://blog.doughellmann.com/', reporthook=reporthook)
         print
         print 'File:', filename
         print 'Headers:'
         print msg
         print 'File exists before cleanup:', os.path.exists(filename)
     finally:
         urllib.urlcleanup()
         print 'File still exists:', os.path.exists(filename)
   
由于服务器没有返回header中的Content-length，urlretrieve()不知道数据应该有多大，所以将-1传给reporthook()中的参数total_size。

::

   $ python urllib_urlretrieve.py
   Connection opened
   Read 1 blocks
   Read 2 blocks
   Read 3 blocks
   Read 4 blocks
   Read 5 blocks
   Read 6 blocks
   Read 7 blocks
   Read 8 blocks
   Read 9 blocks
   Read 10 blocks
   Read 11 blocks
   Read 12 blocks
   Read 13 blocks
   Read 14 blocks
   Read 15 blocks
   Read 16 blocks
   Read 17 blocks
   Read 18 blocks
   Read 19 blocks

   File: /var/folders/9R/9R1t+tR02Raxzk+F71Q50U+++Uw/-Tmp-/tmp3HRpZP
   Headers:
   Content-Type: text/html; charset=UTF-8
   Last-Modified: Tue, 25 Mar 2008 23:09:10 GMT
   Cache-Control: max-age=0 private
   ETag: "904b02e0-c7ff-47f6-9f35-cc6de5d2a2e5"
   Server: GFE/1.3
   Date: Sun, 30 Mar 2008 17:36:48 GMT
   Connection: Close

   File exists before cleanup: True
   File still exists: False

URLopener:
-----------

urllib提供了一个URLopener基类，并且默认使用FancyURLopener处理支持的协议。如果你想要改变其行为，你可能需要查看Python2.1中新加的urllib2模块（PyMOTW将会阐述）。

参考
----

* `RFC 2616 - HTTP Specification <http://www.faqs.org/rfcs/rfc2616.html>`_
* `cgi - For decoding query arguments <http://docs.python.org/lib/module-cgi.html>`_
* `PyMOTW: BaseHTTPServer <http://blog.doughellmann.com/2007/12/pymotw-basehttpserver.html>`_
* `urllib2 - For more complex URL access needs <http://docs.python.org/lib/module-urllib2.html>`_
* `Python Module of the Week Home <http://www.doughellmann.com/projects/PyMOTW/>`_

