PyMOTW: webbrowser
===================

.. currentmodule:: webbrowser

* 模块：webbrowser
* 目的：在浏览器中打开web页面
* python版本：python2.1.3+

利用webbrowser模块可以向用户显示web页面.

描述
----

在一个交互式的浏览程序中, webbrowser模块提供了一些用于打开URL链接的函数. 在系统中安装的浏览器, 通过模块的许多选项可以来获取利用他们. 也可通过环境变量BROWSER来控制.


简单示例
---------

在浏览器中打开一个页面, 可以使用open()函数.

.. code-block:: python

    import webbrowser
    
    webbrowser.open('http://docs.python.org/lib/module-webbrowser.html')


这个url会在一个新窗口中打开, 当然如果当前已经有一个浏览器窗口, 那么会做为一个新标签打开.

窗口 Vs 标签
-------------

如果你只想在新窗口中打开页面, 那么可以使用 ``open_new()`` .

.. code-block:: python

    import webbrowser

    webbrowser.open_new('http://docs.python.org/lib/module-webbrowser.html')

如果你想在新的标签中打开, 那么可以使用 ``open_new_tab()`` .

使用特定的浏览器
-----------------

因为某些原因, 你的应用程序可能需要使用特定的浏览器, 可以利用get()函数来取得浏览器访问对象, 该对象提供了open()、open_new()和open_new_tab()函数, 下面示例演示了如何利用lynx浏览器.

.. code-block:: python

    import webbrowser

    b = webbrowser.get('lynx')
    b.open('http://docs.python.org/lib/module-webbrowser.html')

可以参考模块文档来了解浏览器类型列表.

BROWSER 变量
--------------

用户可以在你的应用程序之外为BROWSER变量设置浏览器名字或者命令来控制webbrowser模块, 值可以由一系列的浏览器名字组成, 中间由系统分割符os.pathsep来分割. 如果名字中包含%s, 那么将被解释成命令, 并且在URL中%s将被直接替换执行. 否则, 值将被传递给get()来获取控制对象.

举个例子, 如下示例是打开一个lynx浏览器, 假设它是可以获取的, 不管是否还存在其它的浏览器.

::

   BROWSER=lynx python webbrowser_open.py 

如果BROWSER中的名字中没有一个可以正确工作, 那么webbrowse会返回执行它的默认行为.


命令行接口
------------

webbrowser模块的所有特性可以通过命令行获取,类似运行一个python程序.

::

   $ python -m webbrowser   
   Usage: /Library/Frameworks/Python.framework/Versions/2.5/lib/python2.5/webbrowser.py [-n | -t] url
      -n: open new window
      -t: open new tab

