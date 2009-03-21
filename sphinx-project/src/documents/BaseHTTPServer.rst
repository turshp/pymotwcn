PyMOTW: BaseHTTPServer
========================

.. currentmodule:: BaseHTTPServer

* 模块： BaseHTTPServer
* 目的： 提供实现web服务的基础类.
* python版本： 1.4+

BaseHTTPServer模块包括了能够构成基本的web服务器的类.


描述
----

BaseHTTPServer使用 `SocketServer <http://docs.python.org/lib/module-SocketServer.html>`_ 中的类来创建HTTP服务基本类, HTTPServer可以被直接使用, 但是其中的BaseHTTPRequestHandler需要被扩展去处理各种协议方法(如GET, POST等).

简单的GET请求例子
--------------------

实现 ``do_METHOD()`` 方法可以让你的请求类支持HTTP方法, 这里的METHOD用具体的HTTP方法名字代替. 例如, ``do_GET()``, ``do_POST()`` 等. 为了保持一致, 这些方法不含参数. 用于请求的所有的参数被BaseHTTPRequestHandler解析, 然后被存储在一个实例属性集合中, 这样你可以很方便地检索它们.

下面的例子中, 请求处理对象说明了如何返回一个响应对象给客户端, 一些本地属性在构造响应对象中很有用的.

.. code-block:: python

    from BaseHTTPServer import BaseHTTPRequestHandler
    import urlparse

    class GetHandler(BaseHTTPRequestHandler):
     
        def do_GET(self):
            parsed_path = urlparse.urlparse(self.path)
            message = '\n'.join([
              'CLIENT VALUES:',
              'client_address=%s (%s)' % (self.client_address, self.address_string()),
              'command=%s' % self.command,
              'path=%s' % self.path,
              'real path=%s' % parsed_path.path,
              'query=%s' % parsed_path.query,
              'request_version=%s' % self.request_version,
              '',
              'SERVER VALUES:',
              'server_version=%s' % self.server_version,
              'sys_version=%s' % self.sys_version,
              'protocol_version=%s' % self.protocol_version,
              '',
            ]) 
            self.send_response(200)
            self.end_headers()
        
            self.wfile.write(message)
        
            return


消息正文被组装好后就写入到self.wfile中, 这个文件处理对象封装了整个响应socket. 每个响应对象需要一个响应代码, 它可以通过self.send_response()来设置. 如果使用了一个错误代码(如404, 501等), 那么对应的默认错误信息会被包含在消息头中, 或者, 你能使用错误码来传递信息.


在服务器中运行请求处理对象, 将这个请求处理对象传递给HTTPServer构造器.

.. code-block:: python

    if __name__ == '__main__':
        from BaseHTTPServer import HTTPServer
        server = HTTPServer(('localhost', 8080), GetHandler)
        print 'Starting server, use <Ctrl-C> to stop'
        server.serve_forever()

接下来启动服务器:

::

   $ python BaseHTTPServer_GET.py 
   Starting server, use <Ctrl-C> to stop

在另外一终端中, 使用curl访问:

::

   $ curl -i http://localhost:8080/?foo=barHTTP/1.0 200 OK
   Server: BaseHTTP/0.3 Python/2.5.1
   Date: Sun, 09 Dec 2007 16:00:34 GMT

   CLIENT VALUES:
   client_address=('127.0.0.1', 51275) (localhost)
   command=GET
   path=/?foo=bar
   real path=/
   query=foo=bar
   request_version=HTTP/1.1

   SERVER VALUES:
   server_version=BaseHTTP/0.3
   sys_version=Python/2.5.1
   protocol_version=HTTP/1.0

线程和进程
-----------

HTTPServer是SocketServer.TCPServer的一个简单子类. 它不使用多线程或多进程来处理请求. 要增加多线程和多进程, 可以使用SocketServer中的合适的混用类来创建一个新的类.

.. code-block:: python

    from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
    from SocketServer import ThreadingMixIn
    import threading

    class Handler(BaseHTTPRequestHandler):
     
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            message = threading.currentThread().getName() ## 这里threading就可以自己处理
            self.wfile.write(message)
            self.wfile.write('\n')
            return

    class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
        """Handle requests in a separate thread."""

    if __name__ == '__main__':
        server = ThreadedHTTPServer(('localhost', 8080), Handler)
        print 'Starting server, use <Ctrl-C> to stop'
        server.serve_forever()

每次当一个请求过来的时候, 一个新的线程或进程会被创建来处理它:

::

   $ curl http://localhost:8080/
   Thread-1
   $ curl http://localhost:8080/
   Thread-2
   $ curl http://localhost:8080/
   Thread-3

如果把上面的ThreadingMixIn换成ForkingMixIn, 也可以获得类似的结果, 但是后者是使用了独立的进程而不是线程.

POST
-----

支持POST请求需要多一点的工作, 因为基本类不会为我们解析表单数据. `cgi <http://docs.python.org/lib/module-cgi.html>`_ 模块提供了用于解析表单的FieldStorage类,只要我们提供正确的输入格式.

.. code-block:: python

    from BaseHTTPServer import BaseHTTPRequestHandler
    import cgi

    class PostHandler(BaseHTTPRequestHandler):
     
        def do_POST(self):
            # Parse the form data posted
            form = cgi.FieldStorage(
            fp=self.rfile, 
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
              'CONTENT_TYPE':self.headers['Content-Type'],
            })

            # Begin the response
            self.send_response(200)
            self.end_headers()
            self.wfile.write('Client: %s\n' % str(self.client_address))
            self.wfile.write('Path: %s\n' % self.path)
            self.wfile.write('Form data:\n')

            
            # Echo back information about what was posted in the form
            for field in form.keys():
                field_item = form[field]
                if field_item.filename:
                    # The field contains an uploaded file
                    file_data = field_item.file.read()
                    file_len = len(file_data)
                    del file_data
                    self.wfile.write('\tUploaded %s (%d bytes)\n' % (field, file_len))
                else:
                    # Regular form value
                    self.wfile.write('\t%s=%s\n' % (field, form[field].value))
            return

    if __name__ == '__main__':
        from BaseHTTPServer import HTTPServer
        server = HTTPServer(('localhost', 8080), PostHandler)
        print 'Starting server, use <Ctrl-C> to stop'
        server.serve_forever()

再次使用curl, 我们可以包含表单数据, 它自动以POST方式发送. 最后的参数, -F datafile=@BaseHTTPServer_GET.py, 将文件BaseHTTPServer_GET.py的内容发送, 从而表示已从表单中读取了文件数据.

::

    $ curl http://localhost:8080/ -F name=dhellmann -F foo=bar -F datafile=@BaseHTTPServer_GET.py
    Client: ('127.0.0.1', 51128)
    Path: /
    Form data:
             name=dhellmann
             foo=bar
             Uploaded datafile (2222 bytes)

Errors
--------

错误处理可以使用 ``send_error()`` 方法. 简单的传递给它合适的错误代码以及一个可选的错误信息, 那么就会为你生成整个响应对象(包括头, 状态码, 消息体).

.. code-block:: python

    from BaseHTTPServer import BaseHTTPRequestHandler

    class ErrorHandler(BaseHTTPRequestHandler):
     
        def do_GET(self):
            self.send_error(404)
            return

    if __name__ == '__main__':
        from BaseHTTPServer import HTTPServer
        server = HTTPServer(('localhost', 8080), ErrorHandler)
        print 'Starting server, use <Ctrl-C> to stop'
        server.serve_forever()

在这种情况下, 一直返回404错误.

::

   $ curl -i http://localhost:8080/
   HTTP/1.0 404 Not Found
   Server: BaseHTTP/0.3 Python/2.5.1
   Date: Sun, 09 Dec 2007 15:49:44 GMT
   Content-Type: text/html
   Connection: close

   <head>
   <title>Error response</title>
   </head>
   <body>
   <h1>Error response</h1>
   <p>Error code 404.
   <p>Message: Not Found.
   <p>Error code explanation: 404 = Nothing matches the given URI.
   </body>


