PyMOTW: shelve
===================

.. currentmodule:: shelve

* 模块：shelve
* 目的：shelve模块实现了对任意可被pickle的Python对象进行持久性存储, 也提供类字典API给我们使用.
* python版本：1.4+


描述
----

当使用关系数据库是一种浪费的时候, shelve模块可以为Python对象提供一个简单的持久性存储选择. 就像使用字典一样, 通过关键字访问shelf对象. 其值经过pickle, 写入到由anydbm创建和管理的数据库.


创建一Shelf对象
----------------

最简单的使用shelve模块的方式是通过DbfilenameShelf类.  使用函数 ``shelve.open()`` (使用的是 `anydbm <http://docs.python.org/lib/module-anydbm.html>`_ )来存储数据. 你可以直接使用类, 或者简单的调用:

.. code-block:: python

    import shelve

    s = shelve.open('test_shelf.db')
    try:
        s['key1'] = { 'int': 10, 'float':9.5, 'string':'Sample data' }
    finally:
        s.close()

为了再次访问数据, 打开shelf并且像字典一样使用它.

.. code-block:: python

    s = shelve.open('test_shelf.db')
    try:
        existing = s['key1']
    finally:
        s.close()

    print existing

如果你运行了上面两个脚本, 你应该看到:

::

   $ python shelve_create.py
   $ python shelve_existing.py
   {'int': 10, 'float': 9.5, 'string': 'Sample data'}

dbm模块不支持多个应用同时写入同一数据库. 如果你确定客户端不会修改shelf, 请指定shelve以只读方式打开数据库.

.. code-block:: python

    s = shelve.open('test_shelf.db', flag='r')
    try:
        existing = s['key1']
    finally:
        s.close()

    print existing

当数据库以只读方式打开时, 你又尝试着更改数据库, 这将引起一个访问出错异常. 这一异常类型依赖于在创建数据库时被anydbm选择的数据库模块.

写回
------

默认情况下, Shelves不去追踪可变对象的修改. 意思就是, 如果你改变了已存储在shelf中的一个项目的内容, 就必须重新存储该项目来更新shelf.

.. code-block:: python

    s = shelve.open('test_shelf.db')
    try:
        print s['key1']
        s['key1']['new_value'] = 'this was not here before'
    finally:
        s.close()

    s = shelve.open('test_shelf.db', writeback=True)
    try:
        print s['key1']
    finally:
        s.close()

在这个例子中, 没有对字典里的关键字"key1"的内容进行存储, 因此, 重新打开shelf的时候, 还没保存所做的改变.

::

   $ python shelve_create.py
   $ python shelve_withoutwriteback.py
   {'int': 10, 'float': 9.5, 'string': 'Sample data'}
   {'int': 10, 'float': 9.5, 'string': 'Sample data'}

为了自动捕捉储存在shelf中的可变对象所发生的改变, 置writeback功能可用. writeback标志导致shelf使用一缓存来记住从数据库中调出的所有对象. 当shelf关闭的时候, 每一个缓存中的对象也重新写入数据库.

.. code-block:: python

    s = shelve.open('test_shelf.db', writeback=True)
    try:
        print s['key1']
        s['key1']['new_value'] = 'this was not here before'
        print s['key1']
    finally:
        s.close()

    s = shelve.open('test_shelf.db', writeback=True)
    try:
        print s['key1']
    finally:
        s.close()

虽然使用writeback模式可以减少程序员出错机率, 也能更加透明化对象持久性, 但是, 不是每种情况都要使用writeback模式的. 当shelf打开的时候, 缓存就要占据额外的空间, 并且, 当shelf关闭的时候, 也会花费额外的时间去将所有缓存中的对象写入到数据库中. 即使不知道缓存中的对象有没有改变, 都要写回数据库. 如果你的应用程序读取数据多于写入数据, 那么writeback模式将增大开销.

::
  
   $ python shelve_create.py
   $ python shelve_writeback.py
   {'int': 10, 'float': 9.5, 'string': 'Sample data'}
   {'int': 10, 'new_value': 'this was not here before', 'float': 9.5, 'string': 'Sample data'}
   {'int': 10, 'new_value': 'this was not here before', 'float': 9.5, 'string': 'Sample data'}

指定Shelf类型
---------------

上面的例子全都使用了默认的shelf实现. 使用 ``shelve.open()`` 直接代替一种shelf实现, 是常见用法, 尤其是在不关心用哪种数据库存储数据的时候. 然而, 有时常会关心它. 如果是在这种情况下, 通常就会直接使用DbfilenameShelf或者BsdDbShelf, 更或者是通过Shelf的子类来解决问题.

参考
-----

* `feedcache uses shelve as a default storage option <http://www.doughellmann.com/projects/feedcache/>`_
