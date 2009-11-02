PyMOTW: ConfigParser
======================

.. currentmodule:: ConfigParser

* 模块： ConfigParser
* 目的： 读取/写入配置文件,类似于Windows的INI文件
* python版本： 1.5+


描述
----

ConfigParser模块可以为你的应用程序创建用户可编辑的配置文件. 这个配置文件由一个个节组成, 每个节可以包含配置数据的名字-值对. 支持通过使用Python的格式化字符串进行值的插入, 以此来构建那些依赖于其他值的数据值(这对路径或URL来说是尤其方便的).

在工作中,当我们把东西移动到svn和 `trac <http://trac.edgewall.org/>`_ 之前, 我们开发推出了自己的用于进行分布式代码复查的工具. 为了准备好需要复查的代码, 一个开发者常常需要写完一个"approach"摘要文件, 然后附上被修改后的代码(即和原代码有区别的地方). 这个approach文档支持通过Web页面添加注释, 因此开发者不在我们的主要办公室里也可以复查代码. 但是唯一的麻烦之处是, 发表代码的不同之处让人感到有点痛苦. 想要让部分处理过程变得简单些, 我写了一个命令行工具, 运行他可以针对CVS沙盒, 自动的寻找出并发表代码的不同之处.

为了能够让这个工具即时更新approach文档中的区别, 需要知道怎样到达存放approach文档的网络服务器. 由于我们开发者不总是在办公室, 从任意给定主机到达服务器的URL可能是通过SSH端口转发过来的. 为了不强迫每个开发者都使用同样的端口转发协议?这个工具应使用一个简单的配置文件来记住这个URL.

一个开发者的配置文件可能会是这个样子:

::

   [portal]
   url = http://%(host)s:%(port)s/Portal
   username = dhellmann
   host = localhost
   password = SECRET
   port = 8080

portal小节表示approach文件的网址. 一旦代码的区别被发送到这个网址, 我们的工具应该下载这个配置文件, 通过ConfigParser模块来访问URL. 这可能看起来像这样:

.. code-block:: python

    from ConfigParser import ConfigParser
    import os

    filename = os.path.join(os.environ['HOME'], '.approachrc')

    config = ConfigParser()
    config.read([filename])

    url = config.get('portal', 'url')

上述的例子中, 变量url的值为"http://localhost:8080/Portal". 配置文件中的变量url中包含两个格式化字符串:"%(host)s"和"%(port)s". 通过 ``get()`` 方法, 自动地将变量host和port的值替换到格式化字符串中.

当然, 这是基于Python2.1的旧代码. 在近来的版本中,ConfigParser模块已经被改进了很多. SafeConfigParser类是a drop? 用来取代ConfigParser, 以改善插值处理.

对于这个工具, 我只需要字符串选项. ConfigParser支持其他的选项类型:整型, 浮点型和布尔型. 由于可选文件格式不提供直接使用一个值来关联一种类型的方式, 所以调用者需要知道何时需要使用一种不同的函数来查询那些其他类型的选项. 例如, 为了查找一个布尔选项, 使用 ``getboolean()`` 函数而不是 ``get()`` 函数. 函数的参数是一样的, 但是选项的值在返回之前被转换为一个布尔类型. 类似地, 还有独立的 ``getint()`` 和 ``getfloat()`` 函数.

ConfigParser类也支持增加和删除小节到指定文件并保存结果. 这使得创建一个用于编辑程序的配置的用户界面,或是利用配置文件格式存放简单数据文件成为可能. 例如, 一个应用需要存储小量的类似于数据库格式的数据, 可以利用ConfigParser类, 这样一来生成的文件也是人类可读的.

