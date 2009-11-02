PyMOTW: asyncore
=================

.. currentmodule:: asyncore

* 模块： asyncore
* 目的： 异步I/O操作
* python版本： 1.5.2+

asyncore模块包含了使用I/O对象如sockets以方便我们异步的进行操作(可以代替例如线程). 他提供的主要类是dispatcher, 是一个封装了一个socket并提供了处理如连接, 读取, 写入等的事件钩子, 这些会在主循环函数loop()中被调用.

客户端
-------

创建一个异步客户端，继承dispatcher并提供了创建, 读取和写入socket的实现. 让我们拿HTTP客户端来做示例, 它基于一个来自标准库文档的例子.

.. code-block:: python

    import asyncore
    import logging
    import socket
    from cStringIO import StringIO
    import urlparse

    class HttpClient(asyncore.dispatcher):

        def __init__(self, url):
            self.url = url
            self.logger = logging.getLogger(self.url)
            self.parsed_url = urlparse.urlparse(url)
            asyncore.dispatcher.__init__(self)
            self.write_buffer = 'GET %s HTTP/1.0\r\n\r\n' % self.url 
            self.read_buffer = StringIO() 
            self.create_socket(socket.AF_INET, socket.SOCK_STREAM) 
            address = (self.parsed_url.netloc, 80)
            self.logger.debug('connecting to %s', address)
            self.connect(address) 

        def handle_connect(self):
            self.logger.debug('handle_connect()')

        def handle_close(self):
            self.logger.debug('handle_close()')
            self.close()

        def writable(self):
            is_writable = (len(self.write_buffer) > 0)
            if is_writable:
                self.logger.debug('writable() -> %s', is_writable)
            return is_writable
                          
        def readable(self):
            self.logger.debug('readable() -> True')
            return True
    
        def handle_write(self):
            sent = self.send(self.write_buffer) 
            self.logger.debug('handle_write() -> "%s"', self.write_buffer[:sent])
            self.write_buffer = self.write_buffer[sent:]
    
        def handle_read(self):
            data = self.recv(8192) 
            self.logger.debug('handle_read() -> %d bytes', len(data))
            self.read_buffer.write(data)

            
    if __name__ == '__main__':
        logging.basicConfig(level=logging.DEBUG,
          format='%(name)s: %(message)s',
        )

        clients = [
          HttpClient('http://www.python.org/'),
          HttpClient('http://www.doughellmann.com/PyMOTW/contents.html'),
        ]
        
        logging.debug('LOOP STARTING')
        asyncore.loop()
        logging.debug('LOOP DONE')
        for c in clients:
            response_body = c.read_buffer.getvalue()
            print c.url, 'got', len(response_body), 'bytes' 

首先，通过在 ``__init__()`` 中使用基类的 ``create_socket()`` 方法创建socket. 当然还有其他的方法, 但在这个例子中. 我们创建的是一个TCP/IP socket. 因此使用基类已经可以满足需要了.

handle_connect()钩子简单的显示了被调用的信息. 其他客户端还可以在 ``handle_connect()`` 中进行一些握手或者协议交涉等类似的处理.

handle_close()同样的显示了被调用的信息. 基类可以正确的关闭socket, 如果你不想作额外的工作可以交给函数来处理.

asyncore循环中, 使用 ``writeable()`` 和同属方法 ``readable()`` 决定什么样的操作来处理每个dispatcher. 实际上, sockets的 ``poll()`` 和 ``select()`` 方法或由每个dispatcher操作的文件描述符会在asyncore代码内部处理. 因此你不必自己来实现这些. 只需简单的指出某dispatcher是否是对读和写都要处理. 在这个HTTP client的例子中, 只要存在请求发送到服务器的数据, ``writable()`` 会返回True, 而 ``readable()`` 一直返回True, 因为我们想读取所有到来的数据.

在每次循环中, 当 ``writable()`` 正确响应, ``handle_write()`` 会被调用. 在这个例子中, 在 ``__init__()`` 中创建的HTTP请求字符串会被发送到服务器, 写缓冲区会清除成功发送的数据.

类似地, 当 ``readable()`` 正确响应, 也就是有数据要读取了. 那么, ``handle_read()`` 会被调用.

例子中__main__之后的代码首先配置一个日志记录以便调试, 然后创建了两个客户端分别下载网页. 创建客户端需要在一个由asyncore内部保存的 *map* 中注册. 随着主循环的开始, 客户端的下载也开始, 当一个客户端从可读socket中读取0个字节, 这会被解释成关闭连接然后.

下面是这个例子中客户端app运行出的可能结果:

::

   $ python asyncore_http_client.py
   http://www.python.org/: connecting to ('www.python.org', 80)
   http://www.doughellmann.com/PyMOTW/contents.html: connecting to ('www.doughellmann.com', 80)
   root: LOOP STARTING
   http://www.python.org/: readable() -> True
   http://www.python.org/: writable() -> True
   http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
   http://www.doughellmann.com/PyMOTW/contents.html: writable() -> True
   http://www.doughellmann.com/PyMOTW/contents.html: handle_connect()
   http://www.doughellmann.com/PyMOTW/contents.html: handle_write() -> "GET http://www.doughellmann.com/PyMOTW/contents.html HTTP/1.0

   "
   http://www.python.org/: readable() -> True
   http://www.python.org/: writable() -> True
   http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
   http://www.doughellmann.com/PyMOTW/contents.html: handle_read() -> 3163 bytes
   http://www.python.org/: readable() -> True
   http://www.python.org/: writable() -> True
   http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
   http://www.doughellmann.com/PyMOTW/contents.html: handle_read() -> 1448 bytes
   http://www.python.org/: readable() -> True
   http://www.python.org/: writable() -> True
   http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
   http://www.doughellmann.com/PyMOTW/contents.html: handle_read() -> 2896 bytes
   http://www.python.org/: readable() -> True
   http://www.python.org/: writable() -> True
   http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
   http://www.doughellmann.com/PyMOTW/contents.html: handle_read() -> 2896 bytes
   http://www.python.org/: readable() -> True
   http://www.python.org/: writable() -> True
   http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
   http://www.doughellmann.com/PyMOTW/contents.html: handle_read() -> 2896 bytes
   http://www.python.org/: readable() -> True
   http://www.python.org/: writable() -> True
   http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
   http://www.doughellmann.com/PyMOTW/contents.html: handle_read() -> 2896 bytes
   http://www.python.org/: readable() -> True
   http://www.python.org/: writable() -> True
   http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
   http://www.doughellmann.com/PyMOTW/contents.html: handle_read() -> 1448 bytes
   http://www.python.org/: readable() -> True
   http://www.python.org/: writable() -> True
   http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
   http://www.doughellmann.com/PyMOTW/contents.html: handle_read() -> 1448 bytes
   http://www.python.org/: readable() -> True
   http://www.python.org/: writable() -> True
   http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
   http://www.doughellmann.com/PyMOTW/contents.html: handle_read() -> 1448 bytes
   http://www.python.org/: readable() -> True
   http://www.python.org/: writable() -> True
   http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
   http://www.doughellmann.com/PyMOTW/contents.html: handle_read() -> 1448 bytes
   http://www.python.org/: readable() -> True
   http://www.python.org/: writable() -> True
   http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
   http://www.doughellmann.com/PyMOTW/contents.html: handle_read() -> 895 bytes
   http://www.python.org/: readable() -> True
   http://www.python.org/: writable() -> True
   http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
   http://www.doughellmann.com/PyMOTW/contents.html: handle_close()
   http://www.doughellmann.com/PyMOTW/contents.html: handle_read() -> 0 bytes
   http://www.python.org/: readable() -> True
   http://www.python.org/: writable() -> True
   http://www.python.org/: handle_connect()
   http://www.python.org/: handle_write() -> "GET http://www.python.org/ HTTP/1.0

   "
   http://www.python.org/: readable() -> True
   http://www.python.org/: handle_read() -> 1396 bytes
   http://www.python.org/: readable() -> True
   http://www.python.org/: handle_read() -> 1396 bytes
   http://www.python.org/: readable() -> True
   http://www.python.org/: handle_read() -> 1396 bytes
   http://www.python.org/: readable() -> True
   http://www.python.org/: handle_read() -> 1396 bytes
   http://www.python.org/: readable() -> True
   http://www.python.org/: handle_read() -> 1396 bytes
   http://www.python.org/: readable() -> True
   http://www.python.org/: handle_read() -> 1396 bytes
   http://www.python.org/: readable() -> True
   http://www.python.org/: handle_read() -> 1396 bytes
   http://www.python.org/: readable() -> True
   http://www.python.org/: handle_read() -> 1396 bytes
   http://www.python.org/: readable() -> True
   http://www.python.org/: handle_read() -> 1396 bytes
   http://www.python.org/: readable() -> True
   http://www.python.org/: handle_read() -> 1396 bytes
   http://www.python.org/: readable() -> True
   http://www.python.org/: handle_read() -> 1396 bytes
   http://www.python.org/: readable() -> True
   http://www.python.org/: handle_read() -> 1396 bytes
   http://www.python.org/: readable() -> True
   http://www.python.org/: handle_read() -> 1257 bytes
   http://www.python.org/: readable() -> True
   http://www.python.org/: handle_close()
   http://www.python.org/: handle_read() -> 0 bytes
   root: LOOP DONE
   http://www.python.org/ got 18009 bytes
   http://www.doughellmann.com/PyMOTW/contents.html got 22882 bytes

服务器
--------

下面的例子, 通过重新实现SocketServe中的EchoServer例子来说明如何在服务器上使用异步. 这里主要有3个类: EchoServer用于接收来自客户端的连接并创建各自的EchoHandler实例, EchoClient是类似于HTTPClient的异步dispatche.

.. code-block:: python

    import asyncore
    import logging

    class EchoServer(asyncore.dispatcher):
        """Receives connections and establishes handlers for each client.
        """
       
        def __init__(self, address):
            self.logger = logging.getLogger('EchoServer')
            asyncore.dispatcher.__init__(self)
            self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
            self.bind(address) 
            self.address = self.socket.getsockname()
            self.logger.debug('binding to %s', self.address)
            self.listen(1) 
            return

        def handle_accept(self):
            # Called when a client connects to our socket 
            client_info = self.accept()
            self.logger.debug('handle_accept() -> %s', client_info[1])
            EchoHandler(sock=client_info[0])
            # We only want to deal with one client at a time,
            # so close as soon as we set up the handler.
            # Normally you would not do this and the server
            # would run forever or until it received instructions
            # to stop.
            self.handle_close()
            return
         
        def handle_close(self):
            self.logger.debug('handle_close()')
            self.close()
            return

    class EchoHandler(asyncore.dispatcher):
        """Handles echoing messages from a single client.
        """
                                  
        def __init__(self, sock, chunk_size=256):
            self.chunk_size = chunk_size
            self.logger = logging.getLogger('EchoHandler%s' % str(sock.getsockname()))
            asyncore.dispatcher.__init__(self, sock=sock)  
            self.data_to_write = []
            return
                                        
        def writable(self):
            """We want to write if we have received data."""
            response = bool(self.data_to_write)
            self.logger.debug('writable() -> %s', response)
            return response
                                             
        
        def handle_write(self):
            """Write as much as possible of the most recent message we have received."""
            data = self.data_to_write.pop()
            sent = self.send(data[:self.chunk_size])
            if sent < len(data):
                remaining = data[sent:]
                self.data_to_write.append(remaining)
            self.logger.debug('handle_write() -> (%d) "%s"', sent, data[:sent])
            if not self.writable():
                self.handle_close()
         
        def handle_read(self):
            """Read an incoming message from the client and put it into our outgoing queue."""
            data = self.recv(self.chunk_size)
            self.logger.debug('handle_read() -> (%d) "%s"', len(data), data)
            self.data_to_write.insert(0, data)
        
        def handle_close(self):
            self.logger.debug('handle_close()')
            self.close()


        
    class EchoClient(asyncore.dispatcher):
        """Sends messages to the server and receives responses.
        """
        
        def __init__(self, host, port, message, chunk_size=512):
            self.message = message
            self.to_send = message
            self.received_data = []
            self.chunk_size = chunk_size
            self.logger = logging.getLogger('EchoClient')
            asyncore.dispatcher.__init__(self)
            self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
            self.logger.debug('connecting to %s', (host, port))
            self.connect((host, port))
            return
            
        def handle_connect(self):
            self.logger.debug('handle_connect()')
            
        def handle_close(self):
            self.logger.debug('handle_close()')
            self.close()
            received_message = ''.join(self.received_data)
            if received_message == self.message:
                self.logger.debug('RECEIVED COPY OF MESSAGE')
            else:
                self.logger.debug('ERROR IN TRANSMISSION')
                self.logger.debug('EXPECTED "%s"', self.message)
                self.logger.debug('RECEIVED "%s"', received_message)
            return
                                                                                         
        def writable(self):
            self.logger.debug('writable() -> %s', bool(self.to_send))
            return bool(self.to_send)
            
        def handle_write(self):
            sent = self.send(self.to_send[:self.chunk_size])
            self.logger.debug('handle_write() -> (%d) "%s"', sent, self.to_send[:sent])
            self.to_send = self.to_send[sent:]
            
        def handle_read(self):
            data = self.recv(self.chunk_size)
            self.logger.debug('handle_read() -> (%d) "%s"', len(data), data)
            self.received_data.append(data)
            
    if __name__ == '__main__':
        import socket
        import threading
        
        logging.basicConfig(level=logging.DEBUG,
          format='%(name)s: %(message)s',
        )

        address = ('localhost', 0) # let the kernel give us a port
        server = EchoServer(address)
        ip, port = server.address # find out what port we were given
        client = EchoClient(ip, port, message=open('lorem.txt', 'r').read())
        asyncore.loop()

EchoServer和EchoHandler被定义在独立的类中因为他们各自处理不同的事情. 当EchoServer接收一个连接, 一个新的socket被建立. 一个利用socket map(这是由asyncore内部维护的)的EchoHandler被创建, 而不是在EchoServer内部进行各个客户端请求的分配.

::

   $ python asyncore_echo_server.py
   EchoServer: binding to ('127.0.0.1', 52235)
   EchoClient: connecting to ('127.0.0.1', 52235)
   EchoClient: writable() -> True
   EchoServer: handle_accept() -> ('127.0.0.1', 52236)
   EchoServer: handle_close()
   EchoClient: handle_connect()
   EchoClient: handle_write() -> (512) "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Donec
   egestas, enim et consectetuer ullamcorper, lectus ligula rutrum leo, a
   elementum elit tortor eu quam. Duis tincidunt nisi ut ante. Nulla
   facilisi. Sed tristique eros eu libero. Pellentesque vel arcu. Vivamus
   purus orci, iaculis ac, suscipit sit amet, pulvinar eu,
   lacus. Praesent placerat tortor sed nisl. Nunc blandit diam egestas
   dui. Pellentesque habitant morbi tristique senectus et netus et
   malesuada fames ac turpis egestas. Aliquam viverra f"
   EchoClient: writable() -> True
   EchoHandler('127.0.0.1', 52235): writable() -> False
   EchoHandler('127.0.0.1', 52235): handle_read() -> (256) "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Donec
   egestas, enim et consectetuer ullamcorper, lectus ligula rutrum leo, a
   elementum elit tortor eu quam. Duis tincidunt nisi ut ante. Nulla
   facilisi. Sed tristique eros eu libero. Pellentesque ve"
   EchoClient: handle_write() -> (225) "ringilla
   leo. Nulla feugiat augue eleifend nulla. Vivamus mauris. Vivamus sed
   mauris in nibh placerat egestas. Suspendisse potenti. Mauris massa. Ut
   eget velit auctor tortor blandit sollicitudin. Suspendisse imperdiet
   justo.
   "
   EchoClient: writable() -> False
   EchoHandler('127.0.0.1', 52235): writable() -> True
   EchoHandler('127.0.0.1', 52235): handle_read() -> (256) "l arcu. Vivamus
   purus orci, iaculis ac, suscipit sit amet, pulvinar eu,
   lacus. Praesent placerat tortor sed nisl. Nunc blandit diam egestas
   dui. Pellentesque habitant morbi tristique senectus et netus et
   malesuada fames ac turpis egestas. Aliquam viverra f"
   EchoHandler('127.0.0.1', 52235): handle_write() -> (256) "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Donec
   egestas, enim et consectetuer ullamcorper, lectus ligula rutrum leo, a
   elementum elit tortor eu quam. Duis tincidunt nisi ut ante. Nulla
   facilisi. Sed tristique eros eu libero. Pellentesque ve"
   EchoHandler('127.0.0.1', 52235): writable() -> True
   EchoClient: writable() -> False
   EchoHandler('127.0.0.1', 52235): writable() -> True
   EchoClient: handle_read() -> (256) "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Donec
   egestas, enim et consectetuer ullamcorper, lectus ligula rutrum leo, a
   elementum elit tortor eu quam. Duis tincidunt nisi ut ante. Nulla
   facilisi. Sed tristique eros eu libero. Pellentesque ve"
   EchoHandler('127.0.0.1', 52235): handle_read() -> (225) "ringilla
   leo. Nulla feugiat augue eleifend nulla. Vivamus mauris. Vivamus sed
   mauris in nibh placerat egestas. Suspendisse potenti. Mauris massa. Ut
   eget velit auctor tortor blandit sollicitudin. Suspendisse imperdiet
   justo.
   "
   EchoHandler('127.0.0.1', 52235): handle_write() -> (256) "l arcu. Vivamus
   purus orci, iaculis ac, suscipit sit amet, pulvinar eu,
   lacus. Praesent placerat tortor sed nisl. Nunc blandit diam egestas
   dui. Pellentesque habitant morbi tristique senectus et netus et
   malesuada fames ac turpis egestas. Aliquam viverra f"
   EchoHandler('127.0.0.1', 52235): writable() -> True
   EchoClient: writable() -> False
   EchoHandler('127.0.0.1', 52235): writable() -> True
   EchoClient: handle_read() -> (256) "l arcu. Vivamus
   purus orci, iaculis ac, suscipit sit amet, pulvinar eu,
   lacus. Praesent placerat tortor sed nisl. Nunc blandit diam egestas
   dui. Pellentesque habitant morbi tristique senectus et netus et
   malesuada fames ac turpis egestas. Aliquam viverra f"
   EchoHandler('127.0.0.1', 52235): handle_write() -> (225) "ringilla
   leo. Nulla feugiat augue eleifend nulla. Vivamus mauris. Vivamus sed
   mauris in nibh placerat egestas. Suspendisse potenti. Mauris massa. Ut
   eget velit auctor tortor blandit sollicitudin. Suspendisse imperdiet
   justo.
   "
   EchoHandler('127.0.0.1', 52235): writable() -> False
   EchoHandler('127.0.0.1', 52235): handle_close()
   EchoClient: writable() -> False
   EchoClient: handle_read() -> (225) "ringilla
   leo. Nulla feugiat augue eleifend nulla. Vivamus mauris. Vivamus sed
   mauris in nibh placerat egestas. Suspendisse potenti. Mauris massa. Ut
   eget velit auctor tortor blandit sollicitudin. Suspendisse imperdiet
   justo.
   "
   EchoClient: writable() -> False
   EchoClient: handle_close()
   EchoClient: RECEIVED COPY OF MESSAGE
   EchoClient: handle_read() -> (0) ""

在这个例子中, 服务器, 处理者, 客户端对象都被asyncore在一个单独进程中使用一相同的socket map维护. 将服务器和客户端分开, 简单的将相关代码分开, 并且在各自程序中运行 ``asyncore.loop()``. 当一个dispatcher被关闭了, 会从map中删掉, 整个循环会在map为空时停下来.

其他循环事件的处理
-------------------

有时候需必须在已有的应用事件中加入异步事件. 例如, 一个GUI应用不想在所有异步操作处理时阻断UI-这是违背了异步的目的. 为了使这种集成更方便, ``asycore.loop()`` 接收一个用于设置超时的参数和一个用于限制循环次数的参数, 重新使用第一个例子中的HttpClient, 我们可以看到他们各自的效果.

.. code-block:: python

    import asyncore
    import logging

    from asyncore_http_client import HttpClient

    logging.basicConfig(level=logging.DEBUG,
      format='%(name)s: %(message)s',
    )

    clients = [
      HttpClient('http://www.doughellmann.com/PyMOTW/contents.html'),
      HttpClient('http://www.python.org/'),
    ]

    loop_counter = 0
    while asyncore.socket_map:
        loop_counter += 1
        logging.debug('loop_counter=%s', loop_counter)
        asyncore.loop(timeout=1, count=1)

我们可以看到, 在 ``asyncore.loop()`` 中调用时, 客户端仅读或写数据一次, 替代我们自己的while循环. 我们可以在GUI工具包活其他需要这种功能机制的地方类似的调用 ``asyncore.loop()`` (ui不会忙于处理其他事件).

::

   $ python asyncore_loop.py

   http://www.doughellmann.com/PyMOTW/contents.html: connecting to ('www.doughellmann.com', 80)
   http://www.python.org/: connecting to ('www.python.org', 80)
   root: loop_counter=1
   http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
   http://www.doughellmann.com/PyMOTW/contents.html: writable() -> True
   http://www.python.org/: readable() -> True
   http://www.python.org/: writable() -> True
   http://www.doughellmann.com/PyMOTW/contents.html: handle_connect()
   http://www.doughellmann.com/PyMOTW/contents.html: handle_write() -> "GET http://www.doughellmann.com/PyMOTW/contents.html HTTP/1.0

   "
   root: loop_counter=2
   http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
   http://www.python.org/: readable() -> True
   http://www.python.org/: writable() -> True
   http://www.doughellmann.com/PyMOTW/contents.html: handle_read() -> 267 bytes
   root: loop_counter=3
   http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
   http://www.python.org/: readable() -> True
   http://www.python.org/: writable() -> True
   http://www.doughellmann.com/PyMOTW/contents.html: handle_read() -> 8192 bytes
   root: loop_counter=4
   http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
   http://www.python.org/: readable() -> True
   http://www.python.org/: writable() -> True
   http://www.doughellmann.com/PyMOTW/contents.html: handle_read() -> 6288 bytes
   root: loop_counter=5
   http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
   http://www.python.org/: readable() -> True
   http://www.python.org/: writable() -> True
   http://www.doughellmann.com/PyMOTW/contents.html: handle_read() -> 1448 bytes
   root: loop_counter=6
   http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
   http://www.python.org/: readable() -> True
   http://www.python.org/: writable() -> True
   http://www.doughellmann.com/PyMOTW/contents.html: handle_read() -> 1448 bytes
   root: loop_counter=7
   http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
   http://www.python.org/: readable() -> True
   http://www.python.org/: writable() -> True
   http://www.doughellmann.com/PyMOTW/contents.html: handle_read() -> 2896 bytes
   root: loop_counter=8
   http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
   http://www.python.org/: readable() -> True
   http://www.python.org/: writable() -> True
   http://www.doughellmann.com/PyMOTW/contents.html: handle_read() -> 2343 bytes
   root: loop_counter=9
   http://www.doughellmann.com/PyMOTW/contents.html: readable() -> True
   http://www.python.org/: readable() -> True
   http://www.python.org/: writable() -> True
   http://www.doughellmann.com/PyMOTW/contents.html: handle_close()
   http://www.doughellmann.com/PyMOTW/contents.html: handle_read() -> 0 bytes
   root: loop_counter=10
   http://www.python.org/: readable() -> True
   http://www.python.org/: writable() -> True
   http://www.python.org/: handle_connect()
   http://www.python.org/: handle_write() -> "GET http://www.python.org/ HTTP/1.0

   "
   root: loop_counter=11
   http://www.python.org/: readable() -> True
   http://www.python.org/: handle_read() -> 1396 bytes
   root: loop_counter=12
   http://www.python.org/: readable() -> True
   http://www.python.org/: handle_read() -> 1396 bytes
   root: loop_counter=13
   http://www.python.org/: readable() -> True
   http://www.python.org/: handle_read() -> 1396 bytes
   root: loop_counter=14
   http://www.python.org/: readable() -> True
   http://www.python.org/: handle_read() -> 1396 bytes
   root: loop_counter=15
   http://www.python.org/: readable() -> True
   http://www.python.org/: handle_read() -> 1396 bytes
   root: loop_counter=16
   http://www.python.org/: readable() -> True
   http://www.python.org/: handle_read() -> 1396 bytes
   root: loop_counter=17
   http://www.python.org/: readable() -> True
   http://www.python.org/: handle_read() -> 1396 bytes
   root: loop_counter=18
   http://www.python.org/: readable() -> True
   http://www.python.org/: handle_read() -> 1396 bytes
   root: loop_counter=19
   http://www.python.org/: readable() -> True
   http://www.python.org/: handle_read() -> 1396 bytes
   root: loop_counter=20
   http://www.python.org/: readable() -> True
   http://www.python.org/: handle_read() -> 1396 bytes
   root: loop_counter=21
   http://www.python.org/: readable() -> True
   http://www.python.org/: handle_read() -> 1396 bytes
   root: loop_counter=22
   http://www.python.org/: readable() -> True
   http://www.python.org/: handle_read() -> 1396 bytes
   root: loop_counter=23
   http://www.python.org/: readable() -> True
   http://www.python.org/: handle_read() -> 1257 bytes
   root: loop_counter=24
   http://www.python.org/: readable() -> True
   http://www.python.org/: handle_close()
   http://www.python.org/: handle_read() -> 0 bytes

文件处理
----------

一般情况下, 你可能只想在sockets中使用asyncore, 但有时异步的读取文件也是有用的(当测试网络服务器而不需要网络设置使用文件，或者是部分读取, 写入大数据文件）在这些情况下, asyncore提供了file_dispatcher和file_wrapper类.

.. code-block:: python

    import asyncore
    import os

    class FileReader(asyncore.file_dispatcher):
     
        def writable(self):
            return False
       
        def handle_read(self):
            data = self.recv(256)
            print 'READ: (%d) "%s"' % (len(data), data)
          
        def handle_expt(self):
            # Ignore events that look like out of band data
            pass
             
        def handle_close(self):
            self.close()

    lorem_fd = os.open('lorem.txt', os.O_RDONLY)
    reader = FileReader(lorem_fd)
    asyncore.loop()

这个例子在Python2.5.2下进行测试, 我使用了 ``os.open()`` 获得文件描述符. 对于Python2.6之后, file_dispatcher自动将所有具有 ``fileno()`` 方法的东西转换成一个文件描述符.

::

   $ python asyncore_file_dispatcher.py
   READ: (256) "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Donec
   egestas, enim et consectetuer ullamcorper, lectus ligula rutrum leo, a
   elementum elit tortor eu quam. Duis tincidunt nisi ut ante. Nulla
   facilisi. Sed tristique eros eu libero. Pellentesque ve"
   READ: (256) "l arcu. Vivamus
   purus orci, iaculis ac, suscipit sit amet, pulvinar eu,
   lacus. Praesent placerat tortor sed nisl. Nunc blandit diam egestas
   dui. Pellentesque habitant morbi tristique senectus et netus et
   malesuada fames ac turpis egestas. Aliquam viverra f"
   READ: (225) "ringilla
   leo. Nulla feugiat augue eleifend nulla. Vivamus mauris. Vivamus sed
   mauris in nibh placerat egestas. Suspendisse potenti. Mauris massa. Ut
   eget velit auctor tortor blandit sollicitudin. Suspendisse imperdiet
   justo.
   "
   READ: (0) ""

参考
-----

* `asyncore: 该模块的标准库文档 <http://docs.python.org/library/asyncore.html>`_
