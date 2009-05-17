PyMOTW: collections
======================

.. currentmodule:: collections

collections模块包含了一些除了内置类型, 如列表, 字典外的容器数据类型.

* 模块: collections
* 目的: 数据类型的包含容器.
* Python 版本: 2.4 +

双端队列:
------------

A double-ended queue, or "deque", supports adding and removing elements from either end. The more commonly used stacks and queues are degenerate forms of deques, where the inputs and outputs are restricted to a single end.
一个双头队列, 或者"双端队列", 支持从每一端上增加和删除元素. 更常用的像栈和队列, 它们可看成是双端队列的特殊情况, 即被限制为输入和输出只能从一端进行.

Since deques are a type of sequence container, they support some of the same operations that lists support, such as examining the contents with __getitem__(), determining length, and removing elements from the middle by matching identity.
因为双端队列是一种序列容器, 所以它们支持一些列表也支持的相同操作, 如利用__getitem__()检查内部元素, 计算长度, 根据标识符的匹配与否来移除某个元素.

import collections

d = collections.deque('abcdefg')

print 'Deque:', d
print 'Length:', len(d)
print 'Left end:', d[0]
print 'Right end:', d[-1]


d.remove('c')

print 'remove(c):', d


$ python collections_deque.py
Deque: deque(['a', 'b', 'c', 'd', 'e', 'f', 'g'])
Length: 7
Left end: a
Right end: g
remove(c): deque(['a', 'b', 'd', 'e', 'f', 'g'])



A deque can be populated from either end, termed "left" and "right" in the Python implementation.
一个双端队列可以从每一端填入元素, 在Python实现中使用词语 "left" 和 "right".

import collections

# Add to the right ## 增加到右边, 使用extend和append
d = collections.deque()
d.extend('abcdefg')
print 'extend :', d
d.append('h')
print 'append :', d

# Add to the left ## 增加到左边, 使用extendleft和appendleft
d = collections.deque()
d.extendleft('abcdefg')
print 'extendleft:', d
d.appendleft('h')
print 'appendleft:', d



Notice that extendleft() iterates over its input and performs the equivalent of an appendleft() for each item. The end result is the deque contains the input sequence in reverse order.
注意: extendleft()将对所有的输入进行, 其执行效果等价于对每一个元素进行appendleft(). 最终的结果是这个双端队列包含了一个逆序的输入元素序列.


$ python collections_deque_populating.py
extend : deque(['a', 'b', 'c', 'd', 'e', 'f', 'g'])
append : deque(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
extendleft: deque(['g', 'f', 'e', 'd', 'c', 'b', 'a'])
appendleft: deque(['h', 'g', 'f', 'e', 'd', 'c', 'b', 'a'])



Similarly, the elements of the deque can be consumed from both or either end, depending on the algorithm you're applying.
类似的, 双端队列可以同时从两端或只从一端获取元素, 具体得看你在算法中是如何写的.

import collections

print 'From the right:'
d = collections.deque('abcdefg')
while True:

try:
print d.pop() ## 从右
except IndexError:
break


print 'From the left:'
d = collections.deque('abcdefg')
while True:

try:
print d.popleft() ## 从左
except IndexError:
break




$ python collections_deque_consuming.py
From the right:
g
f
e
d
c
b
a
From the left:
a
b
c
d
e
f
g



Since deques are thread-safe, you can even consume the contents from both ends at the same time in separate threads.
因为双端队列是线程安全的, 所以你甚至可以在独立线程中从它的两端同时获取元素.

import collections
import threading
import time

candle = collections.deque(xrange(11))

def burn(direction, nextSource):

while True:
try:
next = nextSource()
except IndexError:
break
else:
print '%8s: %s' % (direction, next)
time.sleep(0.1)
print '%8s done' % direction
return


left = threading.Thread(target=burn, args=('Left', candle.popleft))
right = threading.Thread(target=burn, args=('Right', candle.pop))

left.start()
right.start()

left.join()
right.join()



$ python collections_deque_both_ends.py
 Left: 0
 Right: 10
 Left: 1
 Right: 9
 Left: 2
 Right: 8
 Left: 3
 Right: 7
 Left: 4
 Right: 6
 Left: 5
 Right done
 Left done



Another useful capability of the deque is to rotate it in either direction, to skip over some item(s).
另外一个双端队列有用的功能是在每一个方向上转动一些项, 以跳过某些项 .

import collections

d = collections.deque(xrange(10))
print 'Normal :', d

d = collections.deque(xrange(10))
d.rotate(2) ## 向右旋转两个元素
print 'Right rotation:', d

d = collections.deque(xrange(10))
d.rotate(-2) ## 向左旋转两个元素
print 'Left rotation :', d



Rotating the deque to the right (using a positive rotation) takes items from the right end and moves them to the left end. Rotating to the left (with a negative value) takes items from the left end and moves them to the right end. It may help to visualize the items in the deque as being engraved along the edge of a dial.
从右边旋转(使用一个正数)双端队列, 将项向右移动至右端末尾, 对于超过右边界的项又被移动到双端队列的左边. 从左边旋转(使用一个负数)双端队列, 将项向左边移至左端末尾, 对于超过左边界的项又被移动到双端队列的右边.


$ python collections_deque_rotate.py
Normal : deque([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
Right rotation: deque([8, 9, 0, 1, 2, 3, 4, 5, 6, 7])
Left rotation : deque([2, 3, 4, 5, 6, 7, 8, 9, 0, 1])



defaultdict:

The standard dictionary includes the method setdefault() for retrieving a value and establishing a default if the value does not exist. By contrast, defaultdict lets you specify the default up front when it is initialized.
标准的字典包含了setdefault(), 用于设置一个默认值, 即当查找一个不存在的键值时用这个默认值来代替. 同样的, defaultdict能够让你在初始化时指定默认值.

import collections

def default_factory():

return 'default value'


d = collections.defaultdict(default_factory, foo='bar')
print d
print d['foo']
print d['bar']




$ python collections_defaultdict.py
defaultdict(<function default_factory at 0x7ca70>, {'foo': 'bar'})
bar
default value



This works well as long as it is appropriate for all keys to use that same default. It can be especially useful if the default is a type used for aggregating or accumulating values, such as a list, set, or even integer. The standard library documentation includes several examples of using defaultdict this way.
这个例子中, 所有键都使用相同的默认值.  当默认的是一个用于集成或累计值的类型, 如一个列表, 集合, 甚至是整型时会更有用处. 标准库文档包含了许多使用defaultdict的例子.

##更多的defaultdict例子

defaultdict的第一个参数default_factory, 提供了初始值, 默认为None, 余下的参数被看作是字典的键值对.

例子1: 字典值默认是一个空列表
>>> s = [('yellow', 1), ('blue', 2), ('yellow', 3), ('blue', 4), ('red', 1)]
>>> d = defaultdict(list)
>>> for k, v in s:
 d[k].append(v)

>>> d.items()
[('blue', [2, 4]), ('red', [1]), ('yellow', [1, 3])]
例子2: 和上同样的效果, 只是使用了dict
>>> d = {}
>>> for k, v in s:
	d.setdefault(k, []).append(v)

>>> d.items()
[('blue', [2, 4]), ('red', [1]), ('yellow', [1, 3])]
例子3: 值默认为整型, 其整型值默认为0
>>> s = 'mississippi'
>>> d = defaultdict(int)
>>> for k in s:
 d[k] += 1

>>> d.items()
[('i', 4), ('p', 2), ('s', 4), ('m', 1)]
例子4:
>>> def constant_factory(value):
... return itertools.repeat(value).next
>>> d = defaultdict(constant_factory('<missing>'))
>>> d.update(name='John', action='ran')
>>> '%(name)s %(action)s to %(object)s' % d ## 字符串格式化中, 还可以利用字典的key
'John ran to <missing>'
例子5:
>>> s = [('red', 1), ('blue', 2), ('red', 3), ('blue', 4), ('red', 1), ('blue', 4)]
>>> d = defaultdict(set)
>>> for k, v in s:
 d[k].add(v)

>>> d.items()
[('blue', set([2, 4])), ('red', set([1, 3]))]


参考:

Wikipedia: Deque
Deque Recipes
defaultdict examples
James Tauber: Evolution of Default Dictionaries in Python
Python Module of the Week Home
Download Sample Code
