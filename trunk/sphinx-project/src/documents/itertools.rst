PyMOTW: anydbm
=================

.. currentmodule:: anydbm

* 模块： anydbm
* 目的： anydbm提供了针对DBM-style, String-keyed数据库的字典接口.
* python版本： 1.4+


描述
----

anydbm面向DBM数据库, 利用简单的字符串值作为key来访问包含字符串的记录. 它利用whichdb模块来识别dbhash, gdbm和dbm数据库, 并使用appropriate模块来打开它们, 常常在shelve中作为后端使用, 比如我们知道如何利用pickle来存储对象. 她常被用作为shelve的后端, 就像我们知道如何利用pickle来存储对象. 

创建一个新的数据库 
--------------------

新数据库的存储格式是可以通过查询如下模块来选择:

* dbhash
* gdbm
* dbm
* dumbdbm

open函数通过flags标志来控制如何处理数据库文件, 当在必要时创建一个新的数据库时候, 使用"c", 当经常要创建一个新数据库时, 使用"n".

c和n的区别:
也就是说用c, 如果不存在则创建, 如果存在就不创建新的了, 用n的话, 不管存不存在都是创建新的空数据库.

开始, 我们加载一些有用的模块:

.. code-block:: python
    
    import anydbm

    db = anydbm.open('/tmp/example.db', 'n')
    db['key'] = 'value'
    db['today'] = 'Sunday'
    db['author'] = 'Doug'
    db.close()

在这个例子中, 这个文件会总是被重新初始化, 如果想知道被创建的数据库类型, 可以使用whichdb. 

.. code-block:: python

    import whichdb

    print whichdb.whichdb('/tmp/example.db')

你得到的结果可能会不同, 它取决于你安装在系统中的模块.

::

   $ python anydbm_whichdb.py
   dbhash

打开一个存在的数据库
----------------------
   
要打开一个存在的数据库, 使用标记"r"(只读)或者"w"(读写). 你不需要担心格式问题, 因为数据库格式会自动由whichdb来识别, 如果一个文件可以被识别, 那么对应的模块会打开它.

.. code-block:: python

    import anydbm

    db = anydbm.open('/tmp/example.db', 'r')
    try:
        print 'keys():', db.keys()
        for k, v in db.iteritems():
            print 'iterating:', k, v
        print 'db["author"] =', db['author']
     finally:
        db.close()

一旦打开, db就是一个字典对象, 支持一些常规方法:

::

  $ python anydbm_existing.py
  keys(): ['key', 'today', 'author']
  iterating: key value
  iterating: today Sunday
  iterating: author Doug
  db["author"] = Doug

错误案例
----------

数据库关键词必须是字符串.

.. code-block:: python

    import anydbm

    db = anydbm.open('/tmp/example.db', 'w')
    try:
        db[1] = 'one'
    finally:
        db.close()

传递其它类型结果将导致TypeError异常.

::

   $ python anydbm_intkeys.py
   Traceback (most recent call last):
   File "/Users/dhellmann/Documents/PyMOTW/in_progress/anydbm/PyMOTW/anydbm/anydbm_intkeys.py", line 16, in <module>
   db[1] = 'one'
   File "/Library/Frameworks/Python.framework/Versions/2.5/lib/python2.5/bsddb/__init__.py", line 230, in __setitem__
   _DeadlockWrap(wrapF) # self.db[key] = value
   File "/Library/Frameworks/Python.framework/Versions/2.5/lib/python2.5/bsddb/dbutils.py", line 62, in DeadlockWrap
   return function(*_args, **_kwargs)
   File "/Library/Frameworks/Python.framework/Versions/2.5/lib/python2.5/bsddb/__init__.py", line 229, in wrapF
   self.db[key] = value
   TypeError: Integer keys only allowed for Recno and Queue DB's

值必须是字符串或者是空.

.. code-block:: python

    import anydbm

    db = anydbm.open('/tmp/example.db', 'w')
    try:
        db['one'] = 1
    finally:
        db.close()

如果值是非字符串, 那么同样会抛出TypeError异常.

::

   $ python anydbm_intvalue.py
   Traceback (most recent call last):
   File "/Users/dhellmann/Documents/PyMOTW/in_progress/anydbm/PyMOTW/anydbm/anydbm_intvalue.py", line 16, in <module>
   db['one'] = 1
   File "/Library/Frameworks/Python.framework/Versions/2.5/lib/python2.5/bsddb/__init__.py", line 230, in __setitem__
   _DeadlockWrap(wrapF) # self.db[key] = value
   File "/Library/Frameworks/Python.framework/Versions/2.5/lib/python2.5/bsddb/dbutils.py", line 62, in DeadlockWrap
   return function(*_args, **_kwargs)
   File "/Library/Frameworks/Python.framework/Versions/2.5/lib/python2.5/bsddb/__init__.py", line 229, in wrapF
   self.db[key] = value
   TypeError: Data values must be of type string or None.

参考
-----

* `标准库文件：anydbm <http://docs.python.org/lib/module-anydbm.html>`_
