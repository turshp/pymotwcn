PyMOTW: datetime
===================

.. currentmodule:: datetime

datetime 模块包含了一些用于时间解析、格式化、计算的函数。

* 模块： datetime
* 目的： 日期/时间处理
* python版本： 2.3+

时间
----

时间值由time类来表示，Times有小时，分，秒和微秒属性，以及包含时区信息。初始化time实例的参数是可选的，但这样的话，你将获得初始值0（也许不是你所想要的）。

.. code-block:: python

    import datetime

    t = datetime.time(1, 2, 3)
    print t
    print 'hour :', t.hour
    print 'minute:', t.minute
    print 'second:', t.second
    print 'microsecond:', t.microsecond
    print 'tzinfo:', t.tzinfo

::

   $ python datetime_time.py
   01:02:03
   hour  : 1
   minute: 2
   second: 3
   microsecond: 0
   tzinfo: None

一个time实例只包含时间值，不包含日期值。

.. code-block:: python

    import datetime

    print 'Earliest  :', datetime.time.min
    print 'Latest    :', datetime.time.max
    print 'Resolution:', datetime.time.resolution


类属性中的最大最小值反应了一天中的时间范围。

::

   $ python datetime_time_minmax.py
   Earliest  : 00:00:00
   Latest    : 23:59:59.999999
   Resolution: 0:00:00.000001

时间的最小取值是微秒，更精确的位数就被截断了。

.. code-block:: python

    import datetime

    for m in [ 1, 0, 0.1, 0.6 ]:
        print '%02.1f :' % m, datetime.time(0, 0, 0, microsecond=m)

实际中，如果使用浮点型作为微秒参数，那么将产生一些警告信息。

::

   $ python datetime_time_resolution.py
   /home/cjj/python/pymotw/datetime_time_resolution.py:14: DeprecationWarning: integer argument expected, got float

.. code-block:: python

    print '%02.1f :' % m, datetime.time(0, 0, 0, microsecond=m)

::

   1.0 : 00:00:00.000001
   0.0 : 00:00:00
   0.1 : 00:00:00
   0.6 : 00:00:00

日期
------

日期值可以由date类来表示，实例有年、月、日属性，使用data类的 ``today()`` 方法可以方便的表示出今天的日期。

.. code-block:: python

    import datetime

    today = datetime.date.today()
    print today
    print 'ctime:', today.ctime()
    print 'tuple:', today.timetuple()
    print 'ordinal:', today.toordinal()
    print 'Year:', today.year
    print 'Mon :', today.month
    print 'Day :', today.day

示例演示了今天日期的多种表示方法：

::

   $ python datetime_date.py
   2008-03-13
   ctime: Thu Mar 13 00:00:00 2008
   tuple: (2008, 3, 13, 0, 0, 0, 3, 73, -1)
   ordinal: 733114
   Year: 2008
   Mon : 3
   Day : 13

使用整数（从阳历的第1年1月1号开始）或者POSIX标准时间戳可以类实例。

.. code-block:: python

    import datetime
    import time

    o = 733114
    print 'o:', o
    print 'fromordinal(o):', datetime.date.fromordinal(o)
    t = time.time()
    print 't:', t
    print 'fromtimestamp(t):', datetime.date.fromtimestamp(t)

示例显示了函数 ``fromordinal()`` 和 ``fromtimestamp()`` 返回了不同的结果。

::

   $ python datetime_date_fromordinal.py
   o: 733114
   fromordinal(o): 2008-03-13
   t: 1205436039.53
   fromtimestamp(t): 2008-03-13

日期的最大和最小范围可以使用属性max和min来表示。

.. code-block:: python

    import datetime

    print 'Earliest :', datetime.date.min
    print 'Latest :', datetime.date.max
    print 'Resolution:', datetime.date.resolution

一个日期的单位就是1天。

::

   $ python datetime_date_minmax.py
   Earliest  : 0001-01-01
   Latest    : 9999-12-31
   Resolution: 1 day, 0:00:00

对于一个存在的日期，可使用replace函数可以创建出一个新的日期实例。比如你可以改变年数，只保留月份和日。

.. code-block:: python

    import datetime

    d1 = datetime.date(2008, 3, 12)
    print 'd1:', d1

    d2 = d1.replace(year=2009)
    print 'd2:', d2

::

   $ python datetime_date_replace.py
   d1: 2008-03-12
   d2: 2009-03-12

timedelta
-----------

除了 ``replace()`` 函数可以计算过去或者未来的时间，还可以使用timedelta类对日期值进行基本运算。通过timedelta可以加减一个日期来产生另外一个日期。timedelta中的内部值可以用天、秒和微秒来表示。

.. code-block:: python

    import datetime

    print "microseconds:", datetime.timedelta(microseconds=1)
    print "milliseconds:", datetime.timedelta(milliseconds=1)
    print "seconds :", datetime.timedelta(seconds=1)
    print "minutes :", datetime.timedelta(minutes=1)
    print "hours :", datetime.timedelta(hours=1)
    print "days :", datetime.timedelta(days=1)
    print "weeks :", datetime.timedelta(weeks=1)

传递给构造器的中间值被转换为天、秒和微秒。

::

   $ python datetime_timedelta.py

   microseconds: 0:00:00.000001
   milliseconds: 0:00:00.001000
   seconds : 0:00:01
   minutes : 0:01:00
   hours : 1:00:00
   days : 1 day, 0:00:00
   weeks : 7 days, 0:00:00

比较
------

时间和日期值都可以通过标准的操作符来进行比较。

.. code-block:: python

    import datetime
    import time

    print 'Times:'
    t1 = datetime.time(12, 55, 0)
    print '\tt1:', t1
    t2 = datetime.time(13, 5, 0)
    print '\tt2:', t2
    print '\tt1 < t2:', t1 < t2

    print 'Dates:'
    d1 = datetime.date.today()
    print '\td1:', d1
    d2 = datetime.date.today() + datetime.timedelta(days=1)
    print '\td2:', d2
    print '\td1 > d2:', d1 > d2

::

   $ python datetime_comparing.py
   Times:
        t1: 12:55:00
        t2: 13:05:00
        t1 < t2: True
                    
   Dates:
        d1: 2008-03-13 
        d2: 2008-03-14              
        d1 > d2: False

日期和时间组合
----------------

使用datetime类可以存储日期和时间的组合部分，类似于使用date。有多种方法可以创建datetime。

.. code-block:: python

    import datetime

    print 'Now :', datetime.datetime.now()
    print 'Today :', datetime.datetime.today()
    print 'UTC Now:', datetime.datetime.utcnow()

    d = datetime.datetime.now()
    for attr in [ 'year', 'month', 'day', 'hour', 'minute', 'second', 'microsecond']:
        print attr, ':', getattr(d, attr)

同时，datetime实例拥有date和time对象的所有属性。

::

   $ python datetime_datetime.py
   Now : 2008-03-15 22:58:14.770074
   Today : 2008-03-15 22:58:14.779804
   UTC Now: 2008-03-16 03:58:14.779858
   year : 2008
   month : 3
   day : 15
   hour : 22
   minute : 58
   second : 14
   microsecond : 780399

datetime类提供了一些类方法来创建新的实例，当然它也包含 ``fromordinal()`` 和 ``fromtimestamp()`` ，如果你已经有一个日期实例和时间实例，并需要创建datetime的话，combine()方法比较有用。

.. code-block:: python

    import datetime

    t = datetime.time(1, 2, 3)
    print 't :', t
    d = datetime.date.today()
    print 'd :', d
    dt = datetime.datetime.combine(d, t)
    print 'dt:', dt

::

   $ python datetime_datetime_combine.py
   t : 01:02:03
   d : 2008-03-16
   dt: 2008-03-16 01:02:03

格式化和解析
--------------

datetime对象的字符串表示方法默认使用的是ISO 8601格式（YYYY-MM-DDTHH:MM:SS.mmmmmm），使用 ``strftime()`` 可以产生其他格式，同样，如果你的输入值是用 ``time.strptime()`` 解析的时间戳，那么 ``strptime()`` 是一个合适的方法来把它转换为datetime实例。

.. code-block:: python

    import datetime

    format = "%a %b %d %H:%M:%S %Y"

    today = datetime.datetime.today()
    print 'ISO :', today

    s = today.strftime(format)
    print 'strftime:', s

    d = datetime.datetime.strptime(s, format)
    print 'strptime:', d.strftime(format)

::
   
   $ python datetime_datetime_strptime.py
   ISO     : 2008-03-16 08:08:16.275134
   strftime: Sun Mar 16 08:08:16 2008
   strptime: Sun Mar 16 08:08:16 2008

时区
------

时区是由子类datetime.tzinfo来表示的，tzinfo是一个抽象的基类，你需要定义子类，并提供相应的方法去实现一些方法。很可惜，dateime不包含任何实际可用的实现，可以参考 `文档 <http://docs.python.org/lib/datetime-tzinfo.html>`_ 来获取一些示例。

参考
-------

* `PLEAC - Dates and Times <http://pleac.sourceforge.net/pleac_python/datesandtimes.html>`_
* `WikiPedia: Proleptic Gregorian calendar <http://en.wikipedia.org/wiki/Proleptic_Gregorian_calendar>`_
