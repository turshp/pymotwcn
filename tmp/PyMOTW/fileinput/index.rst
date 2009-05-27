================
fileinput
================
.. module:: fileinput
    :synopsis: Create command-line filter programs.创建命令行过滤程序.


To start this series, let's take a look at the fileinput module, a very useful
module for creating command line programs for processing text files in a
filter-ish manner. For example, the m3utorss app I recently wrote for my
friend `Patrick <http://events.mediumloud.com/>`_ to convert some of his 
demo recordings into a podcastable format.
让我们从 fileinput 模块开始这个系列的学习吧. 这是一个非常有用的模块, 用于创建处理文本文件中过滤信息的命令行程序. 例如, 最近为我的朋友 `Patrick <http://events.mediumloud.com/>`_ 写了个应用 m3utorss , 用于将一些小demo转成podcastable格式便于记录.

The inputs to the program are one or more m3u file listing the mp3 files to be
distributed. The output is a single blob of XML that looks like an RSS feed
(output is written to stdout, for simplicity). To process the input, I need to
iterate over the list of filenames and:
程序的输入是一个或多个m3u文件, 列出了所有的mp3文件. 输出是一个XML文件, 看起来有点像RSS feed(简单起见, 输出到stdout). 为了处理输入, 我需要对一个文件名列表一次处理:

* Open each file.打开每个文件.
* Read each line of the file.读取一个文件的每一行.
* Figure out if the line refers to an mp3 file.标记出指向一个mp3文件的行.
* If it does, extract the information from the mp3 file needed for the RSS feed.如果有, 提出取mp3文件的信息用于生成RSS feed.
* Print the output.输出.

I could have written all of that file handling out by hand. It isn't that
complicated, and with some testing I'm sure I could even get the error
handling right. But with the fileinput module, I don't need to worry about
that. I just write something like:
我本应该手工写所有文件的处理代码. 但没有非常复杂, 在一些测试之后, 我确信, 连错误处理都可以正确处理. 但是使用fileinput模块, 我可以不用这么麻烦的考虑很多东西, 主需要写如下:

.. include:: fileinput_example.py
    :literal:
    :start-after: #end_pymotw_header

The relevant bit in that snippet is the for loop. The fileinput.input()
function takes as argument a list of filenames to examine. If the list is
empty, the module reads data from standard input. The function returns an
iterator which returns individual lines from the text files being processed.
So, all I have to do is loop over each line, skipping blanks and comments, to
find the references to mp3 files.
这段代码中相关的代码是for循环中的. fileinput.input()函数将参数看成是要检测是文件名列表. 如果这个列表是空的, 那么模块会从标准输入中获取. 它返回的是一个迭代器, 依次返回正在处理的文本文件中的每一行. 因此, 我所要做的就是循环处理每行, 跳过空白和注释, 寻找mp3文件.

In this example, I don't care what file or line number we are processing in
the input. For other tools (grep-like searching, for example) you might. The
fileinput module includes functions for accessing that information
(filename(), filelineno(), lineno(), etc.). Check out the standard library
documentation for fileinput for more details.
在这个例子中, 我不需要关心正在处理哪个文件和具体的哪个行. 可能还是其他工具(例如, 类grep搜索工具). fileinput模块也包含了访问这些信息的函数(filename(), filelineno(), lineno(), 等等). 具体使用可参考fileinput的标准库文档.

.. seealso::

    `fileinput <http://docs.python.org/library/fileinput.html>`_
        该模块的标准库文档.

    `Patrick Bryant <http://events.mediumloud.com/>`_
        Atlanta-based singer/song-writer.
