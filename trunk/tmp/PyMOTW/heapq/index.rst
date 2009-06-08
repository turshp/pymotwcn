=====================================
heapq -- In-place heap sort algorithm就地堆排序算法
=====================================

.. module:: heapq
    :synopsis: In-place heap sort algorithm就地堆排序算法

:Purpose:
    The heapq implements a min-heap sort algorithm suitable for use with
    Python's lists. heapq模块实现了小顶堆排序算法, 适合于Python的列表.
:Python Version: New in 2.3 with additions in 2.5   2.3+, 2.5中有所增加

A heap is a tree-like data structure where the child nodes have a sort-order
relationship with the parents. Binary heaps can be represented using a list or
array organized so that the children of element N are at positions 2*N+1 and
2*N+2 (for zero-based indexes). This feature makes it possible to rearrange
heaps in place, so it is not necessary to reallocate as much memory when
adding or removing items.
堆是一种树型数据结构, 其父子节点间具有顺序关系. 二进制堆可以使用一个列表或数组来表示, 其中元素N的孩子所在位置为2*N+1 和 2*N+2(以0开始计算位置). 这种特征让就地重排成为可能, 这样在增加或删除元素时就不需要重新分配内存空间.

A max-heap ensures that the parent is larger than or equal to both of its
children. A min-heap requires that the parent be less than or equal to its
children. Python's heapq module implements a min-heap.
大顶堆确保每个父元素都大于或等于他的任一个孩子元素. 而小顶堆则需要每个父元素都要小于或等于他的任一个孩子元素. Python的heapq模块实现的是小顶堆.

Example Data 示例数据
============

The examples below use this sample data: 本文的例子中使用的是如下的示例数据: 

.. include:: heapq_heapdata.py
    :literal:
    :start-after: #end_pymotw_header


Creating a Heap创建一个堆:
===============

There are 2 basic ways to create a heap, heappush() and heapify().
有两个基本的堆创建方式, 分别是heappush()和heapify().

Using heappush(), the heap sort order of the elements is maintained as new
items are added from a data source.
使用heappush(), 堆中元素排序顺序是随着新元素的不断增加而不断更新的.

.. include:: heapq_heappush.py
    :literal:
    :start-after: #end_pymotw_header

::

    $ python heapq_heappush.py
    random : [19, 9, 4, 10, 11, 8, 2]

    add  19:

                     19                 
    ------------------------------------

    add   9:

                     9                  
            19        
    ------------------------------------

    add   4:

                     4                  
            19                9         
    ------------------------------------

    add  10:

                     4                  
            10                9         
        19   
    ------------------------------------

    add  11:

                     4                  
            10                9         
        19       11   
    ------------------------------------

    add   8:

                     4                  
            10                8         
        19       11       9    
    ------------------------------------

    add   2:

                     2                  
            10                4         
        19       11       9        8    
    ------------------------------------


If the data is already in memory, it is more efficient to use heapify() to
rearrange the items of the list in place.
如果数据已经在内存中了, 使用heapify()进行就地排序会更有效.

.. include:: heapq_heapify.py
    :literal:
    :start-after: #end_pymotw_header

::

    $ python heapq_heapify.py
    random    : [19, 9, 4, 10, 11, 8, 2]
    heapified :

                     2                  
            9                 4         
        10       11       8        19   
    ------------------------------------


Accessing Contents of a Heap访问堆:
============================

Once the heap is organized correctly, use heappop() to remove the element with
the lowest value. In this example, adapted from the stdlib documentation,
heapify() and heappop() are used to sort a list of numbers.
成功建立堆之后, 可以使用heappop()删除堆中最小的元素. 下面的例子改编自标准库文档中的例子, heapify()和heappop()用于对一个列表进行排序.

.. include:: heapq_heappop.py
    :literal:
    :start-after: #end_pymotw_header

::

    $ python heapq_heappop.py
    random    : [19, 9, 4, 10, 11, 8, 2]
    heapified :

                     2                  
            9                 4         
        10       11       8        19   
    ------------------------------------


    pop      2:

                     4                  
            9                 8         
        10       11       19   
    ------------------------------------

    pop      4:

                     8                  
            9                 19        
        10       11   
    ------------------------------------

    pop      8:

                     9                  
            10                19        
        11   
    ------------------------------------

    pop      9:

                     10                 
            11                19        
    ------------------------------------

    pop     10:

                     11                 
            19        
    ------------------------------------

    pop     11:

                     19                 
    ------------------------------------

    pop     19:

    ------------------------------------

    inorder   : [2, 4, 8, 9, 10, 11, 19]


To remove existing elements and replace them with new values in a single
operation, use heapreplace().
使用heapreplace()可以删除现有元素和用新的值替换已存元素.

.. include:: heapq_heapreplace.py
    :literal:
    :start-after: #end_pymotw_header

This technique lets you maintain a fixed size heap, such as a queue of jobs
ordered by priority.
这个功能让你维持了一个固定大小的堆, 这在具有优先级任务队列中是很用的.

::

    $ python heapq_heapreplace.py
    start:

                     2                  
            9                 4         
        10       11       8        19   
    ------------------------------------

    replace  2 with  0:

                     0                  
            9                 4         
        10       11       8        19   
    ------------------------------------

    replace  0 with  7:

                     4                  
            9                 7         
        10       11       8        19   
    ------------------------------------

    replace  4 with 13:

                     7                  
            9                 8         
        10       11       13       19   
    ------------------------------------

    replace  7 with  9:

                     8                  
            9                 9         
        10       11       13       19   
    ------------------------------------

    replace  8 with  5:

                     5                  
            9                 9         
        10       11       13       19   
    ------------------------------------


Data Extremes数据极值:
=============

heapq also includes 2 functions to examine an iterable to find a range of the
largest or smallest values it contains. Using nlargest() and nsmallest() are
really only efficient for relatively small values of n > 1, but can still come
in handy in a few cases.
heapq也包含了2个用于检查迭代对象中最大或最小的值范围. 使用nlargest()和nsmallest()可以获得相对最小或最大的n个数, n一般大于1, 但在有些情况下不能获得正确的值.

.. include:: heapq_extremes.py
    :literal:
    :start-after: #end_pymotw_header

::

    $ python heapq_extremes.py
    all       : [19, 9, 4, 10, 11, 8, 2]
    3 largest : [19, 11, 10]
    from sort : [19, 11, 10]
    3 smallest: [2, 4, 8]
    from sort : [2, 4, 8]

.. seealso参考::

    `heapq <http://docs.python.org/library/heapq.html>`_
        The standard library documentation for this module.

    `WikiPedia: Heap (data structure) <http://en.wikipedia.org/wiki/Heap_(data_structure)>`_
        A general description of heap data structures.
