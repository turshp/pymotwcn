PyMOTW: csv
====================

.. currentmodule:: csv

* 模块: csv
* 目的: 对以分号分隔的数值文件进行读写
* Python 版本: 2.3+

描述:
---------

csv 模块在处理那些从电子数据表格或数据库中导入到文本文件的数据时, 是很有用的. 这里并没有很好的定义标准, 因此csv模块使用了"dialects", 通过使用不同的参数来解析csv文件. 对于一般的读和写, 这个模块也能处理Microsoft Excel格式数据.

局限性:
----------

Python 2.5 版本的csv不支持unicode数据, 而对于ASCII的NUL字符处理也有点问题, 所以推荐使用UTF-8或可打印ASCII字符.

读取:
----------

从csv文件中读取数据, 可以使用reader()函数来创建一个读取对象. 这个读取对象顺序处理文件的每一行, 可以把它当成迭代器使用, 例如:

.. code-block::python

    import csv
    import sys

    f = open(sys.argv[1], 'rt')
    try:

        reader = csv.reader(f)
        for row in reader:
        print row

    finally:

        f.close()


reader()的第一个参数指示源文本行, 在这个例子中, 是一个文件, 但它可以是任何可转换的对象(StringIO对象, lists等). 指定其他可选的参数可用于控制输入的数据如何被解析.

例子文件"testdata.csv"是从NeoOffice中导入的, 其内容如下.

::

    $ cat testdata.csv 
    "Title 1","Title 2","Title 3"
    1,"a",08/18/07
    2,"b",08/19/07
    3,"c",08/20/07
    4,"d",08/21/07
    5,"e",08/22/07
    6,"f",08/23/07
    7,"g",08/24/07
    8,"h",08/25/07
    9,"i",08/26/07

它被读取时, 输入数据的每一行被转换为一个字符串列表.

::

    $ python csv_reader.py testdata.csv
    ['Title 1', 'Title 2', 'Title 3']
    ['1', 'a', '08/18/07']
    ['2', 'b', '08/19/07']
    ['3', 'c', '08/20/07']
    ['4', 'd', '08/21/07']
    ['5', 'e', '08/22/07']
    ['6', 'f', '08/23/07']
    ['7', 'g', '08/24/07']
    ['8', 'h', '08/25/07']
    ['9', 'i', '08/26/07']


如果你知道特定的列具有特定的类型, 你就可以自行转换, 但csv不会自动转换. 它会自动处理嵌入在一行字符串中(这个行和输入源文件的"行"意思是不同的)的换行符.

::

    $ cat testlinebreak.csv 
    "Title 1","Title 2","Title 3"
    1,"first line ## 这是源文件的一个line
    second line",08/18/07

    $ python csv_reader.py testlinebreak.csv 
    ['Title 1', 'Title 2', 'Title 3']
    ['1', 'first line\nsecond line', '08/18/07'] ## 这是csv的一个row


写入:
---------

当你想把数据导入到其他应用程序中, 对CSV文件的写入也是非常方便的. 使用writer()函数来创建一个写入对象, 对于每一行, 使用writerow()来输出一行.

.. code-block::python

    import csv
    import sys

    f = open(sys.argv[1], 'wt')
    try:

        writer = csv.writer(f)
        writer.writerow( ('Title 1', 'Title 2', 'Title 3') )
        for i in range(10):
        writer.writerow( (i+1, chr(ord('a') + i), '08/%02d/07' % (i+1)) )

    finally:

        f.close()

这个例子的输出和上述读取例子的导出数据看起来不怎么一样.

::
    $ python csv_writer.py testout.csv 
    $ cat testout.csv 
    Title 1,Title 2,Title 3
    1,a,08/01/07
    2,b,08/02/07
    3,c,08/03/07
    4,d,08/04/07
    5,e,08/05/07
    6,f,08/06/07
    7,g,08/07/07
    8,h,08/08/07
    9,i,08/09/07
    10,j,08/10/07

写入对象没有使用默认的引号, 所以每列字符串没有用引号引起来. 但如果增加额外的引用参数即可将非数值数据用引号引起来.

.. code-block::python

    writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)


现在每个字符串都被引起来了:

::

    $ python csv_writer_quoted.py testout_quoted.csv 
    $ cat testout_quoted.csv 
    "Title 1","Title 2","Title 3"
    1,"a","08/01/07"
    2,"b","08/02/07"
    3,"c","08/03/07"
    4,"d","08/04/07"
    5,"e","08/05/07"
    6,"f","08/06/07"
    7,"g","08/07/07"
    8,"h","08/08/07"
    9,"i","08/09/07"
    10,"j","08/10/07"


引用:
--------

还有4种不同的引用选项, 它们作为常量定义在csv模块中.

QUOTE_ALL
    不管是什么类型, 任何内容都加上引号

QUOTE_MINIMAL
    这是默认的, 使用指定的字符引用各个域(如果解析器被配置为相同的dialect和选项时, 可能会让解析器在解析时产生混淆)

QUOTE_NONNUMERIC
    引用那些不是整数或浮点数的域. 当使用读取对象时, 如果输入的域是没有引号, 那么它们会被转换成浮点数.

QUOTE_NONE
    对所有的输出内容都不加引用, 当使用读取对象时, 引用字符看作是包含在每个域的值里(但在正常情况下, 他们被当成定界符而被去掉)


Dialects:
------------

有很多参数可以控制csv模块如何解析或读取数据. 但这不是通过各自传递给读取对象和写入对象相关参数, 而是统一起来, 使用一个"dialect"对象. Dialect类可以通过名字注册, 因此csv模块调用它时可以不必预先知道相关的参数设置. 标准库包含两种dialects: excel和excel-tabs. "excel" dialect是用于处理默认来自 Microsoft Excel格式的数据的, 同样, 也可以处理 OpenOffice 或 NeoOffice的数据. 更多详细的dialect参数及其使用在csv模块的 `节9.1.2 <http://docs.python.org/lib/csv-fmt-params.html>`_ 中有说明.      ## dialect就是一些参数(定界符, 换行符等等)设置, 预先设置好的, 但同样我们也可以自己设定,

DictReader 和DictWriter:
---------------------------

另外, 在处理数据序列时, csv模块包含了一些将行作为字典进行处理的类. 类DictReader和类DictWriter将每一行转成字典对象, 可以传递字典键值, 或者从输入文件的第一行中推断出键值.

.. code-block:: python

    import csv
    import sys

    f = open(sys.argv[1], 'rt')
    try:

        reader = csv.DictReader(f)
        for row in reader:
        print row

    finally:
         f.close()


基于字典的读取和写入对象可以当作是基于序列对象的进一步实现, 它们使用相同的参数和API. 唯一的差别就是前者把每一行当成是字典而不是列表或元组.

::

    $ python csv_dictreader.py testdata.csv 
    {'Title 1': '1', 'Title 3': '08/18/07', 'Title 2': 'a'}
    {'Title 1': '2', 'Title 3': '08/19/07', 'Title 2': 'b'}
    {'Title 1': '3', 'Title 3': '08/20/07', 'Title 2': 'c'}
    {'Title 1': '4', 'Title 3': '08/21/07', 'Title 2': 'd'}
    {'Title 1': '5', 'Title 3': '08/22/07', 'Title 2': 'e'}
    {'Title 1': '6', 'Title 3': '08/23/07', 'Title 2': 'f'}
    {'Title 1': '7', 'Title 3': '08/24/07', 'Title 2': 'g'}
    {'Title 1': '8', 'Title 3': '08/25/07', 'Title 2': 'h'}
    {'Title 1': '9', 'Title 3': '08/26/07', 'Title 2': 'i'}



DictWriter必须指定一个域名字的列表, 因为这样它才在输出时知道每个列的顺序.

.. code-block:: python

    import csv
    import sys

    f = open(sys.argv[1], 'wt')
    try:

        fieldnames = ('Title 1', 'Title 2', 'Title 3')
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        headers = {}
        for n in fieldnames:
            headers[n] = n
        writer.writerow(headers)
        for i in range(10):
            writer.writerow({ 'Title 1':i+1,
                            'Title 2':chr(ord('a') + i),
                            'Title 3':'08/%02d/07' % (i+1),
                            })

    finally:

        f.close()

::

    $ python csv_dictwriter.py testout.csv 
    $ cat testout.csv 
    Title 1,Title 2,Title 3
    1,a,08/01/07
    2,b,08/02/07
    3,c,08/03/07
    4,d,08/04/07
    5,e,08/05/07
    6,f,08/06/07
    7,g,08/07/07
    8,h,08/08/07
    9,i,08/09/07
    10,j,08/10/07


参考:
-------
* `Python Module of the Week Home <http://www.doughellmann.com/projects/PyMOTW/>`_
* `Download Sample Code <http://www.doughellmann.com/downloads/PyMOTW-1.14.tar.gz>`_
* `PEP 305, CSV File API <http://www.python.org/peps/pep-0305.html>`_
