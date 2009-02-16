PyMOTW: string
================

.. currentmodule:: string


* 模块：string
* 目的：包括文本处理中的常量和类.
* python版本：2.5

string模块始于Python的最早版本. 2.0版本中, 许多之前只在模块中实现的函数被转移为string对象的方法. 之后的版本中, 虽然这些函数仍然可用, 但是不推荐使用, 并且在Python 3.0中将被去掉. string模块也包含了一些有用的常量和类来处理字符串和unicode对象, 后面的讨论会集中在这个方面.

常量
-----

string模块中的常量, 例如ascii_letters和digits等, 用来指定字符的种类. 有些常量是依赖于系统的, 比如lowercase, 因此会受用户语言设置的影响而改变. 而其它的常量, 如hexdigits, 不会因本地设置的改变而改变.

.. code-block:: python

    import string

    for n in dir(string):
        if n.startswith('_'):
        continue
        v = getattr(string, n)c
        if isinstance(v, basestring):
        print '%s=%s' % (n, repr(v))
        print

大部分常量的名字是很直观的.

::

   $ python string_constants.py
   ascii_letters='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
   ascii_lowercase='abcdefghijklmnopqrstuvwxyz'
   ascii_uppercase='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
   digits='0123456789'
   hexdigits='0123456789abcdefABCDEF'
   letters='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
   lowercase='abcdefghijklmnopqrstuvwxyz'
   octdigits='01234567'
   printable='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'
   punctuation='!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
   uppercase='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
   whitespace='\t\n\x0b\x0c\r '

函数
-----

有两个函数没有从string模块中移除. capwords()将一个字符串所有单词首字母大写.

.. code-block:: python

    import string

    s = 'The quick brown fox jumped over the lazy dog.'

    print s
    print string.capwords(s)

得到的结果和调用split(), 将结果列表中的每个单词首字母大写, 然后调用join()连接这些单词这一系列动作的结果相同.

::

   $ python string_capwords.py
   The quick brown fox jumped over the lazy dog.
   The Quick Brown Fox Jumped Over The Lazy Dog.

另一个函数创建了一个翻译表. 这个翻译表作为translate()方法的参数, 用来将某一集合中的字符改成另一个集合中的字符.

.. code-block:: python

    import string

    leet = string.maketrans('abegiloprstz', '463611092572')

    s = 'The quick brown fox jumped over the lazy dog.'

    print s
    print s.translate(leet)

在这个例子中, 一些字符被替换为其 `133t <http://en.wikipedia.org/wiki/Leet>`_ 数字.

::

   $ python string_maketrans.py
   The quick brown fox jumped over the lazy dog.
   Th3 qu1ck 620wn f0x jum93d 0v32 7h3 142y d06.

模板
-----

字符串模板是在Python 2.4中增加的, 作为 `PEP 292 <http://www.python.org/peps/pep-0292.html>`_ 的一部分, 以及用作内置的占位符表达式的另一种实现形式. 若使用了 ``string.Template`` 的占位符, 前缀为$的单词就被认为是变量(如$var), 如果需要将其在上下文中区别出来的话, 也可以将变量名包括在大括号中(如${var}).

.. code-block:: python

    import string
    
    values = { 'var':'foo' }
    t = string.Template("""
    $var
    $$
    ${var}iable
    """)
    
    print 'TEMPLATE:', t.substitute(values)

    s = """
    %(var)s
    %%
    %(var)siable
    """

    print 'INTERPLOATION:', s % values

如您所见, 两种形式中, 触发字符($或%)若重复两次则被转义为普通字符.

::

   $ python string_template.py
   TEMPLATE:
   foo
   $
   fooiable

   INTERPLOATION:
   foo
   %
   fooiable

模板和标准字符串占位符的一个关键区别就是模板不会考虑参数类型. 参数的值将被转为字符串并插入到模板中. 模板中没有格式选项. 比如, 模板中无法控制显示一个浮点数时数字的个数.

而使用模板的一个好处是调用 ``safe_substitute()`` 方法, 当模板需要的参数值没有全部提供时, 可以避免了异常的产生.

.. code-block:: python

    import string

    values = { 'var':'foo' }

    t = string.Template("$var is here but $missing is not provided")

    try:
        print 'TEMPLATE:', t.substitute(values)
    except KeyError, err:
        print 'ERROR:', str(err)
       
    print 'TEMPLATE:', t.safe_substitute(values)

因为missing这个变量的值没有出现在参数字典里, 所以 ``substitue()`` 会引发一个KeyError异常. 而 ``safe_substitute()`` 则捕获了这个异常并将这个变量表达式保留在文本中.

::

   $ python string_template_missing.py
   TEMPLATE: ERROR: 'missing'
   TEMPLATE: foo is here but $missing is not provided

模板的高级应用
----------------

如果string.Template的默认表达式无法满足你的要求, 你可以通过调整用于匹配模板正文中变量名的正则表达式来达到你的目的. 一种简单的方法就是改变delimiter和idpattern这两个类属性.

.. code-block:: python

    import string

    class MyTemplate(string.Template):
        delimiter = '%'
        idpattern = '[a-z]+_[a-z]+'

    t = MyTemplate('%% %with_underscore %notunderscored')
    d = { 'with_underscore':'replaced', 
              'notunderscored':'not replaced',
    }

    print t.safe_substitute(d)

在这个例子中, 变量名必须在中间的某个位置包含一个下划线, 因此%notunderscored不会被替换为任何东西.

::

   $ python string_template_advanced.py
   % replaced %notunderscored

如果需要更复杂的变化, 你可以重载pattern属性, 定义一个全新的正则表达式. 新的pattern属性必须包含4个命名的组来分别匹配定界符, 已命名的变量, 区分变量的括号类型, 和无效界定符模式.

让我们看一下默认的模式:

.. code-block:: python

    import string

    t = string.Template('$var')
    print t.pattern.pattern

因为t.pattern是已经被编译的正则表达式, 我们只能通过它的pattern属性来看真实的字符串.

::

   $ python string_template_defaultpattern.py

   \$(?:
   (?P<escaped>\$) | # Escape sequence of two delimiters
   (?P<named>[_a-z][_a-z0-9]*) | # delimiter and a Python identifier
   {(?P<braced>[_a-z][_a-z0-9]*)} | # delimiter and a braced identifier
   (?P<invalid>) # Other ill-formed delimiter exprs
   )

如果希望创建一个新的模板, 如, 以{{var}}作为变量表达式, 可以使用这样的一个pattern:

.. code-block:: python

    import re
    import string

    class MyTemplate(string.Template):
        delimiter = '{{'
        pattern = re.compile(r'''
                  \{\{(?:
                  (?P<escaped>\{\{)|
                  (?P<named>[_a-z][_a-z0-9]*)\}\}|
                  (?P<braced>[_a-z][_a-z0-9]*)\}\}|
                  (?P<invalid>)
                  )
        ''', re.VERBOSE | re.DOTALL)
          
    t = MyTemplate('''
        {{{{
        {{var}}
    ''')

    print 'MATCHES:', t.pattern.findall(t.template)
    print 'SUBSTITUTED:', t.safe_substitute(var='replacement')

即使named和braced是一样的, 仍然需要将它们都描述出来. 下面是输出:

::

   $ python string_template_newsyntax.py
   MATCHES: [('{{', '', '', ''), ('', 'var', '', '')]
   SUBSTITUTED:
   {{
   replacement

不推荐使用的函数
------------------

那些不推荐使用的函数已经被转移到string和unicode类中, 可参考手册中的 `String Methods <http://docs.python.org/library/stdtypes.html#string-methods>`_.

参考
-----

* `string <http://docs.python.org/library/string.html>`_
* `PEP 292 <http://www.python.org/peps/pep-0292.html>`_
