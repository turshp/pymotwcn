PyMOTW: sched
========================

.. currentmodule:: sched

sched模块实现了一般事件调度功能, 能在指定时间执行某个任务.

* 模块: sched
* 目的: 一般事件调度.
* Python 版本: 1.4 + 

描述:
------

scheduler类使用一般的事件调度接口. 它使用time函数来获得当前时间, delay函数用于等待一段特定时间. 这里, 真正使用什么样的时间单位不是很重要, 因为这能让接口更具灵活性, 可用于多种用途.

time函数调用时不需要给定任何参数, 应返回当前时间的字符串表示. 而delay函数需要一个整型参数, 和time函数使用相同的时间刻度, 该函数在返回前需要等待特定个时间单元. 例如, time.time()和time.sleep()这两个函数符合这些要求.

为了支持多线程应用, 在生成每个线程之后, 调用参数为0的delay函数, 这样来保证其他线程有机会运行.


延迟后运行事件:
--------------------

事件可以在延迟一段时间后, 或在指定时间点上调度执行.  enter()方法使这些事件在延迟一段时间后被调度, 它需要4个参数:

 * A number representing the delay 代表延迟多长时间的数字
 * A priority value 优先级值
 * The function to call 需要被调用的函数
 * A tuple of arguments for the function 函数的参数元组


下面这个例子中, 分别在2和3秒之后调度2个不同的事件. 当到达某事件的调度时刻, print_event()被调用, 显示出目前时间和传递给事件的参数名字.

.. code-block:: python

    import sched
    import time

    scheduler = sched.scheduler(time.time, time.sleep)

    def print_event(name):
        print 'EVENT:', time.time(), name

    print 'START:', time.time()
    scheduler.enter(2, 1, print_event, ('first',))
    scheduler.enter(3, 1, print_event, ('second',))

    scheduler.run()

输出如下:

::

    $ python sched_basic.py
    START: 1190727943.36
    EVENT: 1190727945.36 first
    EVENT: 1190727946.36 second

第一个事件的时间信息是调度开始2秒后, 第二个事件的时间信息是调度开始3秒后.

事件重叠:
-------------

run()一直被阻塞, 直到所有事件被全部执行完. 每个事件在同一线程中运行, 所以如果一个事件的执行时间大于其他事件的延迟时间, 那么, 就会产生重叠. 重叠的解决方法是推迟后来事件的执行时间. 这样保证没有丢失任何事件, 但这些事件的调用时刻会比原先设定的迟. 在下面的例子中, long_event()中通过睡眠2秒钟来延迟调度, 同样延迟调度很容易通过运行长时间计算或阻塞I/O来实现.

.. code-block:: python

    import sched
    import time

    scheduler = sched.scheduler(time.time, time.sleep)

    def long_event(name):
        print 'BEGIN EVENT :', time.time(), name
        time.sleep(2)
        print 'FINISH EVENT:', time.time(), name

    print 'START:', time.time()
    scheduler.enter(2, 1, long_event, ('first',))
    scheduler.enter(3, 1, long_event, ('second',))

    scheduler.run()

第二个事件在第一个事件运行结束后立即运行, 因为第一个事件的执行时间足够长, 已经超过第二个事件的预期开始时刻.

::

    $ python sched_overlap.py 
    START: 1190728573.16
    BEGIN EVENT : 1190728575.16 first
    FINISH EVENT: 1190728577.16 first
    BEGIN EVENT : 1190728577.16 second
    FINISH EVENT: 1190728579.16 second


事件优先级:
---------------

如果在相同的时刻点上有多个事件需要被执行, 那么它们的优先级参数决定他们的执行顺序.

.. code-block:: python

    now = time.time()
    print 'START:', now
    scheduler.enterabs(now+2, 2, print_event, ('first',))
    scheduler.enterabs(now+2, 1, print_event, ('second',))
    scheduler.run()

为了保证事件准确的在同一时刻执行, 使用了enterabs()方法而不是enter()方法. enterabs()的第一个参数是运行事件的确切时间, 而不是延迟时间量.

::

    $ python sched_priority.py 
    START: 1190728789.4
    EVENT: 1190728791.4 second
    EVENT: 1190728791.4 first


取消事件:
--------------

enter()和enterabs()返回一事件的引用, 该引用可被用于事件的取消. 由于run()阻塞, 所以事件的取消操作需要在另外一个线程中进行. 如下例子, 在一个子线程开始执行调度, 而主处理线程用于取消某个事件.

.. code-block:: python

    import sched
    import threading
    import time

    scheduler = sched.scheduler(time.time, time.sleep)

    # Set up a global to be modified by the threads
    counter = 0

    def increment_counter(name):

        global counter
        print 'EVENT:', time.time(), name
        counter += 1
        print 'NOW:', counter


    print 'START:', time.time()
    e1 = scheduler.enter(2, 1, increment_counter, ('E1',))
    e2 = scheduler.enter(3, 1, increment_counter, ('E2',))

    # Start a thread to run the events
    t = threading.Thread(target=scheduler.run)
    t.start()

    # Back in the main thread, cancel the first scheduled event.
    scheduler.cancel(e1)

    # Wait for the scheduler to finish running in the thread
    t.join()

    print 'FINAL:', counter


两个事件被安排调度, 但之后取消了第一个事件. 只有第二个事件执行了, 所以我们看到计数器仅累加了一次.

::
    $ python sched_cancel.py
    START: 1190729094.13
    EVENT: 1190729097.13 E2
    NOW: 1
    FINAL: 1


参考:
-------

* `Python Module of the Week Home <http://www.doughellmann.com/projects/PyMOTW/>`_
* `Download Sample Code <http://www.doughellmann.com/downloads/PyMOTW-1.19.tar.gz>`_
