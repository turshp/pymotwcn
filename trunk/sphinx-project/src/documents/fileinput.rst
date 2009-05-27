PyMOTW: fileinput
================
.. currentmodule:: fileinput

* 模块: fileinput
* 目的: 创建命令行过滤程序.
* Python 版本: ?

描述:
---------

让我们从 fileinput 模块开始这个系列的学习吧. 这是一个非常有用的模块, 用于创建处理文本文件中过滤信息的命令行程序. 例如, 最近为我的朋友 `Patrick <http://events.mediumloud.com/>`_ 写了个应用 m3utorss , 用于将一些小demo转成podcastable格式便于记录.


程序的输入是一个或多个m3u文件, 列出了所有的mp3文件. 输出是一个XML文件, 看起来有点像RSS feed(简单起见, 输出到stdout). 为了处理输入, 我需要对一个文件名列表一次处理:

* 打开每个文件.
* 读取一个文件的每一行.
* 标记出指向一个mp3文件的行.
* 如果有, 提出取mp3文件的信息用于生成RSS feed.
* 输出.

我本应该手工写所有文件的处理代码. 但没有非常复杂, 在一些测试之后, 我确信, 连错误处理都可以正确处理. 但是使用fileinput模块, 我可以不用这么麻烦的考虑很多东西, 主需要写如下:

.. code-block::python

    import fileinput
    import sys


    def generate_item(filename):
    	"""Process the named file go generate an RSS item.
    	"""
	print filename
    
    for line in fileinput.input(sys.argv[1:]):
    	mp3filename = line.strip()
    	if not mp3filename or mp3filename.startswith('#'):
    		continue
    	generate_item(mp3filename)
	


这段代码中相关的代码是for循环中的. fileinput.input()函数将参数看成是要检测是文件名列表. 如果这个列表是空的, 那么模块会从标准输入中获取. 它返回的是一个迭代器, 依次返回正在处理的文本文件中的每一行. 因此, 我所要做的就是循环处理每行, 跳过空白和注释, 寻找mp3文件.

在这个例子中, 我不需要关心正在处理哪个文件和具体的哪个行. 可能还是其他工具(例如, 类grep搜索工具). fileinput模块也包含了访问这些信息的函数(filename(), filelineno(), lineno(), 等等). 具体使用可参考fileinput的标准库文档.

参考:
-------

* `fileinput <http://docs.python.org/library/fileinput.html>`_ 该模块的标准库文档.

* `Patrick Bryant <http://events.mediumloud.com/>`_  一位歌曲/歌词作家.
