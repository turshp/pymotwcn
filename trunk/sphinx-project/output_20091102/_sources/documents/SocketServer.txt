PyMOTW: SocketServer
======================

.. currentmodule:: SocketServer

* 模块： SocketServer
* 目的： 创建网络服务器.
* python版本： 1.4+


SocketServer模块是一个用于创建网络服务器的框架. 他提供了处理TCP, UDP, Unix流和Unix数据报的基本类和支持线程和进程服务器, 这依赖于具体的应用情况.

描述
----

SocketServer模块定义了处理同步网络请求(服务器请求处理时会阻塞直到请求完成)的类. 它也提供了一个接口类, 可以方便地将服务器转换使其对于每个请求使用独立线程或进程.

处理一个请求需要先将server(服务器)类和request handler(请求处理)类分开来. 服务器处理通信事宜(如列出一个socket, 接受连接等等), 而请求处理类处理"协议"事宜(解释来到的数据并处理他, 返回数据给客户端). 这种任务的划分意味着，在许多情况下，你可以简单地并且可以不加修改的使用一个现有的服务器类，并为之提供一个符合用户特定需要的请求处理类.

服务器类型
-----------

在SocketServer模块中定义了5种不同的服务器类. BaseServer仅定义了API, 但没有实例化很多方法所以不能直接使用. TCPServer使用TCP/IP sockets来通信. UDPServer使用数据报sockets. UnixStreamServer和UnixDatagramServer使用Unix-domain sockets，这仅在Unix平台上可用.

服务器对象
-----------

构造一个服务器对象，需要传递给它一个监听请求的地址和一个请求处理类(不是实例). 地址格式根据服务器的类型和所使用的socket族. 细节可以参考 `socket模块文档 <http://docs.python.org/lib/module-socket.html>`_.

一旦一个服务器对象被实例化, 使用 ``handle_request()`` 或者 ``serve_forever()`` 来处理请求. ``serve_forever()`` 方法简单的在一个无穷循环中调用 ``handle_request()``, 所以如果你需要在服务器中集成其他事件循环, 或者使用 ``select()`` 监视多个不同服务器的sockets, 你可以独立调用 ``handle_request()``. 可以看下面的例子.

实现一个服务器
---------------

如果你要创建一个服务器, 它通常是复用现有的类并简单提供自定义的请求处理类. 如果这不能满足你的需求, 还可以使用BaseServer并在其子类中重载一些方法:

verify_request(request, client_address) - 返回True来处理请求, 或者False表示忽略这个请求. 比如, 你也可以拒绝从一个IP范围来的请求, 假如你想要阻断某些客户端访问服务器.

process_request(request, client_address) - 它通常是调用finish_request()来完成实际工作. 但它也看创建一个独立的线程或进程, 作为混合类来使用(如下).

finish_request(request, client_address) - 使用在服务器构造时指定的类来创建一个请求处理实例. 她调用请求处理类的 ``handle()`` 来处理请求.

请求处理者
-----------

请求处理者做了大部分的接受到达的请求和决定如何处理. 处理者应该实现socket层面的 *protocol* (例如, HTTP或XML-RPC). 请求处理者从到达的数据通道中读取请求, 处理它, 并写回一个response. 有下面的3个方法可以被重载.

setup() - 准备一个请求处理者. 在StreamRequestHandler中, 例如, ``setup()`` 方法创建一个类文件对象用于读取和写入socket.

handle() - 做实际处理请求的工作. 解析到来的请求, 处理数据并发送一个response.

finish() - 清除在setup()中创建的所有东西.

在很多情况下, 你可以简单提供handle()方法就可.

Echo例子
----------

在这个例子中, 让我们看下一对简单的server/request处理对象, 它们接受TCP连接, 并将接收的数据返回给客户端. 例子代码中, 唯一实际需要的方法是 ``EchoRequestHandler.handle()``, 但我已经重载上述描述的所有方法并插入了日志功能调用以便输出示例程序调用时的执行顺序.

.. code-block:: python
    
    import logging
    import sys
    import SocketServer

    logging.basicConfig(level=logging.DEBUG,
      format='%(name)s: %(message)s',
    )

    class EchoRequestHandler(SocketServer.BaseRequestHandler):
       
        def __init__(self, request, client_address, server):
            self.logger = logging.getLogger('EchoRequestHandler')
            self.logger.debug('__init__')
            SocketServer.BaseRequestHandler.__init__(self, request, client_address, server)
            return

        def setup(self):
            self.logger.debug('setup')
            return SocketServer.BaseRequestHandler.setup(self)

        def handle(self):
            self.logger.debug('handle')

            # Echo the back to the client
            data = self.request.recv(1024)
            self.logger.debug('recv()->"%s"', data)
            self.request.send(data)
            return

        def finish(self):
            self.logger.debug('finish')
            return SocketServer.BaseRequestHandler.finish(self)

    class EchoServer(SocketServer.TCPServer):
                         
        def __init__(self, server_address, handler_class=EchoRequestHandler):
            self.logger = logging.getLogger('EchoServer')
            self.logger.debug('__init__')
            SocketServer.TCPServer.__init__(self, server_address, handler_class)
            return

        def server_activate(self):
            self.logger.debug('server_activate')
            SocketServer.TCPServer.server_activate(self)
            return

        def serve_forever(self):
            self.logger.debug('waiting for request')
            self.logger.info('Handling requests, press <Ctrl-C> to quit')
            while True:
                self.handle_request()
            return

        def handle_request(self):
            self.logger.debug('handle_request')
            return SocketServer.TCPServer.handle_request(self)

        def verify_request(self, request, client_address):
            self.logger.debug('verify_request(%s, %s)', request, client_address)
            return SocketServer.TCPServer.verify_request(self, request, client_address)
            
        def process_request(self, request, client_address):
            self.logger.debug('process_request(%s, %s)', request, client_address)
            return SocketServer.TCPServer.process_request(self, request, client_address)

        def server_close(self):
            self.logger.debug('server_close')
            return SocketServer.TCPServer.server_close(self)
            
        def finish_request(self, request, client_address):
            self.logger.debug('finish_request(%s, %s)', request, client_address)
            return SocketServer.TCPServer.finish_request(self, request, client_address)
            
        def close_request(self, request_address):
            self.logger.debug('close_request(%s)', request_address)
            return SocketServer.TCPServer.close_request(self, request_address)

这是一个简单的程序, 他创建了服务器, 在一个线程中运行, 连接它能返回哪些方法被调用的信息.

.. code-block:: python

    if __name__ == '__main__':
        import socket
        import threading

        address = ('localhost', 0) # let the kernel give us a port
        server = EchoServer(address, EchoRequestHandler)
        ip, port = server.server_address # find out what port we were given

        t = threading.Thread(target=server.serve_forever)
        t.setDaemon(True) # don't hang on exit
        t.start()

        logger = logging.getLogger('client')
        logger.info('Server on %s:%s', ip, port)
        
        # Connect to the server
        logger.debug('creating socket')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logger.debug('connecting to server')
        s.connect((ip, port))
        
        # Send the data
        message = 'Hello, world'
        logger.debug('sending data: "%s"', message)
        len_sent = s.send(message)
        
        # Receive a response
        logger.debug('waiting for response')
        response = s.recv(len_sent)
        logger.debug('response from server: "%s"', response)

        # Clean up
        logger.debug('closing socket')
        s.close()
        logger.debug('done')
        server.socket.close()

程序输出的结果如下:

::

   $ python SocketServer_echo.py
   EchoServer: __init__
   EchoServer: server_activate
   EchoServer: waiting for request
   EchoServer: Handling requests, press to quit
   EchoServer: handle_request
   client: Server on 127.0.0.1:53477
   client: creating socket
   client: connecting to server
   EchoServer: verify_request(, ('127.0.0.1', 53478))
   EchoServer: process_request(, ('127.0.0.1', 53478))
   EchoServer: finish_request(, ('127.0.0.1', 53478))
   EchoRequestHandler: __init__
   EchoRequestHandler: setup
   EchoRequestHandler: handle
   client: sending data: "Hello, world"
   EchoRequestHandler: recv()->"Hello, world"
   EchoRequestHandler: finish
   EchoServer: close_request()
   EchoServer: handle_request
   client: waiting for response
   client: response from server: "Hello, world"
   client: closing socket
   client: done

程序使用的端口号会在你每次运行时改变, 因为内核自动分配给他可用的端口. 如果你想让服务器每次运行时都监听固定的端口, 可以为地址元组提供一个数字而不是0.

上述例子的简单版本, 没有日志记录, 如下:

.. code-block:: python

    import SocketServer

    class EchoRequestHandler(SocketServer.BaseRequestHandler):

        def handle(self):
            # Echo the back to the client
            data = self.request.recv(1024)
            self.request.send(data)
            return

    if __name__ == '__main__':
        import socket
        import threading
        address = ('localhost', 0) # let the kernel give us a port
        server = SocketServer.TCPServer(address, EchoRequestHandler)
        ip, port = server.server_address # find out what port we were given
        
        t = threading.Thread(target=server.serve_forever)
        t.setDaemon(True) # don't hang on exit
        t.start()

        # Connect to the server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))

        # Send the data
        message = 'Hello, world'
        print 'Sending : "%s"' % message
        len_sent = s.send(message)
        
        # Receive a response
        response = s.recv(len_sent)
        print 'Received: "%s"' % response
        
        # Clean up
        s.close()
        server.socket.close()

.. note::

    这种情况下, 不需要特殊的服务器类, 因为TCPServer已经符合我们的需要了.

::

   $ python SocketServer_echo_simple.py
   Sending : "Hello, world"
   Received: "Hello, world"

线程和进程
------------

为服务器增加线程或forking支持, 只需要简单的在类层次结构中增加包含合适的混合类. 这个混合类重载 ``process_request()``, 当要处理一个请求时开始一个新的线程或进程, 并且会在一个新的孩子线程或进程中完成工作.

对于线程, 使用ThreadingMixIn:

.. code-block:: python

    import threading
    import SocketServer

    class ThreadedEchoRequestHandler(SocketServer.BaseRequestHandler):

        def handle(self):
            # Echo the back to the client
            data = self.request.recv(1024)
            cur_thread = threading.currentThread()
            response = '%s: %s' % (cur_thread.getName(), data)
            self.request.send(response)
            return

    class ThreadedEchoServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
        pass

    if __name__ == '__main__':
        import socket
        import threading
        
        address = ('localhost', 0) # let the kernel give us a port
        server = ThreadedEchoServer(address, ThreadedEchoRequestHandler)
        ip, port = server.server_address # find out what port we were given
        
        t = threading.Thread(target=server.serve_forever)
        t.setDaemon(True) # don't hang on exit
        t.start()
        print 'Server loop running in thread:', t.getName()
        
        # Connect to the server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))

        # Send the data
        message = 'Hello, world'
        print 'Sending : "%s"' % message
        len_sent = s.send(message)
        
        # Receive a response
        response = s.recv(1024)
        print 'Received: "%s"' % response
        
        # Clean up
        s.close()
        server.socket.close()

从服务器返回的response包括了处理请求的线程id:

::

    $ python SocketServer_threaded.py
    Server loop running in thread: Thread-1
    Sending : "Hello, world"
    Received: "Thread-2: Hello, world"

使用独立的进程, 可以使用ForkingMixIn:

.. code-block:: python

    import os
    import SocketServer

    class ForkingEchoRequestHandler(SocketServer.BaseRequestHandler):

        def handle(self):
            # Echo the back to the client
            data = self.request.recv(1024)
            cur_pid = os.getpid()
            response = '%s: %s' % (cur_pid, data)
            self.request.send(response)
            return

    class ForkingEchoServer(SocketServer.ForkingMixIn, SocketServer.TCPServer):
        pass

    if __name__ == '__main__':
        import socket
        import threading
        
        address = ('localhost', 0) # let the kernel give us a port
        server = ForkingEchoServer(address, ForkingEchoRequestHandler)
        ip, port = server.server_address # find out what port we were given
        
        t = threading.Thread(target=server.serve_forever)
        t.setDaemon(True) # don't hang on exit
        t.start()
        
        print 'Server loop running in process:', os.getpid()
        # Connect to the server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        
        # Send the data
        message = 'Hello, world'
        print 'Sending : "%s"' % message
        len_sent = s.send(message)
        
        # Receive a response
        response = s.recv(1024)
        print 'Received: "%s"' % response
        
        # Clean up
        s.close()
        
        server.socket.close()

在这种情况下, 从服务器返回的response包含了一个子进程的id:

::

   $ python SocketServer_forking.py
   Server loop running in process: 20173
   Sending : "Hello, world"
   Received: "20175: Hello, world"

参考
------

* `effbot.org: Sockets <http://effbot.org/zone/socket-intro.htm>`_
