PyMOTW: heapq
=================

.. currentmodule:: heapq

* 模块： heapq
* 目的： 就地堆排序算法
* python版本：New in 2.3 with additions in 2.5 2.3+, 2.5中有所增加

heapq实现了适用于Python列表的小顶堆排序算法.

描述
----

堆是一种树型数据结构, 其父子节点间具有顺序关系. 二进制堆可以使用一个列表或数组来表示, 其中元素N的孩子所在位置为2*N+1 和 2*N+2(以0开始计算位置). 这种特征让就地重排成为可能, 这样在增加或删除元素时就不需要重新分配内存空间.

大顶堆确保每个父元素都大于或等于他的任一个孩子元素. 而小顶堆则需要每个父元素都要小于或等于他的任一个孩子元素. Python的heapq模块实现的是小顶堆.


示例数据
----------

本文的例子中使用的是如下的示例数据:

.. code-block:: python

    data = [19, 9, 4, 10, 11, 8, 2]

创建一个堆
------------

有两个基本的堆创建方式, 分别是heappush()和heapify().

使用heappush(), 堆中元素排序顺序是随着新元素的不断增加而不断更新的.

.. code-block:: python

    import heapq
    from heapq_showtree import show_tree
    from heapq_heapdata import data

    heap = []
    print 'random :', data
    print

    for n in data:
        print 'add %3d:' % n
	heapq.heappush(heap, n)
	show_tree(heap)

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

如果数据已经在内存中了, 使用heapify()进行就地排序会更有效.

.. code-block:: python

    import heapq
    from heapq_showtree import show_tree
    from heapq_heapdata import data

    print 'random :', data
    heapq.heapify(data)
    print 'heapified :'
    show_tree(data)

::

   $ python heapq_heapify.py
   random : [19, 9, 4, 10, 11, 8, 2]
   heapified :

                    2                  
           9                 4         
       10       11       8        19   
   ------------------------------------

访问堆
-------

成功建立堆之后, 可以使用heappop()删除堆中最小的元素. 下面的例子改编自标准库文档中的例子, heapify()和heappop()用于对一个列表进行排序.

.. code-block:: python

    import heapq
    from heapq_showtree import show_tree
    from heapq_heapdata import data

    print 'random :', data
    heapq.heapify(data)
    print 'heapified :'
    show_tree(data)
    print

    inorder = []
    while data:
        smallest = heapq.heappop(data)
	print 'pop %3d:' % smallest
	show_tree(data)
	inorder.append(smallest)
    print 'inorder :', inorder

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

使用heapreplace()可以删除现有元素和用新的值替换已存元素.

.. code-block:: python

    import heapq
    from heapq_showtree import show_tree
    from heapq_heapdata import data

    heapq.heapify(data)
    print 'start:'
    show_tree(data)

    for n in [0, 7, 13, 9, 5]:
        smallest = heapq.heapreplace(data, n)
        print 'replace %2d with %2d:' % (smallest, n)
        show_tree(data)

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

数据极值
----------

heapq也包含了2个用于检查迭代对象中最大或最小的值范围. 使用nlargest()和nsmallest()可以获得相对最小或最大的n个数, n一般大于1, 但在有些情况下不能获得正确的值.

.. code-block:: python

    import heapq
    from heapq_heapdata import data

    print 'all :', data
    print '3 largest :', heapq.nlargest(3, data)
    print 'from sort :', list(reversed(sorted(data)[-3:]))
    print '3 smallest:', heapq.nsmallest(3, data)
    print 'from sort :', sorted(data)[:3]

::

   $ python heapq_extremes.py
   all : [19, 9, 4, 10, 11, 8, 2]
   3 largest : [19, 11, 10]
   from sort : [19, 11, 10]
   3 smallest: [2, 4, 8]
   from sort : [2, 4, 8]

参考
-----

* `heapq Theory <http://docs.python.org/lib/node92.html>`_
* `WikiPedia - Heap Data Structure <http://en.wikipedia.org/wiki/Heap_%28data_structure%29>`_
