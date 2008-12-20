PyMOTW: textwrap
=================

.. currentmodule:: textwrap

* 模块：textwrap
* 目的: 通过调整段落中的换行符位置来格式化文本
* python版本：2.5


描述
------

textwrap模块可以用来格式化文本，使其在某些场合输出更美观。他提供了一些类似于在很多文本编辑器中都有的段落包装或填充特性的程序功能.

例子
-----

.. code-block:: python

    import textwrap

    # Provide some sample text 提供样本文本
    sample_text = '''

     The textwrap module can be used to format text for output in situations
     where pretty-printing is desired.  It offers programmatic functionality similar
     to the paragraph wrapping or filling features found in many text editors.
       
    '''

fill()将文本作为输入，格式化文本作为输出。让我们看下面是如何对样本文本进行格式化的

.. code-block:: python

    print 'No dedent:\n'
    print textwrap.fill(sample_text)

结果比我们想要的结果要少：

::

   No dedent:

           The textwrap module can be used to format text for output in
           situations         where pretty-printing is desired.  It offers
           programmatic functionality similar         to the paragraph wrapping
           or filling features found in many text editors.

.. note::

    注意嵌入的tab符号和多余的空格被混合在输出文本中。这个看起来是很粗糙的。当然，我们可以做的更好。我们想在样本文本中的每一行的开始处删掉所有普通空格前缀。这个允许我们在去除代码本身的格式化时直接从Python代码中使用文档字符串或者嵌入式多行字符串。下面的样本字符串引入了一个人工的缩进层次以便更好的说明这个特征。

删除样本行中的普通空格前缀

.. code-block:: python

    dedented_text = textwrap.dedent(sample_text).strip()
    print 'Dedented:\n'
    print dedented_text

结果看上去似乎好点：

::
 
   Dedented:

   The textwrap module can be used to format text for output in situations
   where pretty-printing is desired.  It offers programmatic functionality similar
   to the paragraph wrapping or filling features found in many text editors.

由于“dedent”是“indent”的相反，结果就是将每行开始的普通空白符删除了。如果某行已经比另一行多了个缩进层次，那么对应的空格不会被去掉。

::

   >>> a="""
   ...     one tab
   ...             two tab
   ...     one tab
   ... """
   >>> import textwrap
   >>> dedented_text = textwrap.dedent(a).strip()
   >>> print dedented_text
   one tab
       two tab
   one tab
   >>> print a
       one tab
           two tab
       one tab
   >>> 

接下来，让我们看下如果我们传递非缩进格式的文本给fill()，并使用一些不同的宽度值，会发生什么。

使用不同行宽值进行格式化输出:

.. code-block:: python

    for width in [ 20, 60, 80 ]:
        print
        print '%d Columns:\n' % width
        print textwrap.fill(dedented_text, width=width)

在指定不同宽度时会有以下不同的输出结果：

20 Columns: 

::

   The textwrap module
   can be used to
   format text for
   output in situations
   where pretty-
   printing is desired.
   It offers
   programmatic
   functionality
   similar to the
   paragraph wrapping
   or filling features
   found in many text
   editors.

60 Columns:

::

   The textwrap module can be used to format text for output in
   situations where pretty-printing is desired.  It offers
   programmatic functionality similar to the paragraph wrapping
   or filling features found in many text editors.

80 Columns:

::

   The textwrap module can be used to format text for output in situations where
   pretty-printing is desired.  It offers programmatic functionality similar to the
   paragraph wrapping or filling features found in many text editors.

除了制定输出中的宽度，你可以控制首行缩进，他独立于接下来的行。

.. code-block:: python

    # 演示怎样去产生悬挂缩进
    print '\nHanging indent:\n'
    print textwrap.fill(dedented_text, initial_indent='', subsequent_indent='    ')

这个看起来很容易就能实现文本的悬挂缩进，也就是首行要比后继行有少的缩进。

::

   Hanging indent:

   The textwrap module can be used to format text for output in
      situations where pretty-printing is desired.  It offers
      programmatic functionality similar to the paragraph wrapping or
      filling features found in many text editors.

缩进值也可以是非空格字符，因此，可以用*作为前缀产生bullet点，等等。在我转换老的zwiki内容以便将其导入到trac中是很灵活的。我使用Zope中的StructuredText包来解析zwiki数据，然后创建一个格式化器产生一个trac的wiki标记作为输出。使用textwrap就可以格式化输出页，因此转换后就几乎不需要再进行手工操作整个转换过程几乎没有手工进行。


参考
-------

* `textwrap_example.py <http://www.doughellmann.com/PyMOTW/textwrap_example.py>`_
