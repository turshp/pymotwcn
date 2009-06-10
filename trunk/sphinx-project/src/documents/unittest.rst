PyMOTW: unittest
==================

.. currentmodule:: unittest

* 模块： unittest
* 目的： 自动测试框架
* python版本： 2.1+


描述
----

Python的unittest模块, 有时被称为PyUnit, 它是基于由Kent Beck 和Erich Gamma设计的XUnit框架的. 这种模型被重复使用在其他很多语言(如C, perl, Java和Smalltalk)中. 这个由unittest实现的框架支持fixtures, test suites, 和a test runner, 以便能自动测试你的代码.


基本测试结构
-------------------

unittest模块中定义的测试包含两个部分: 管理测试“fixtures”的代码, 和本身的测试代码. 每个测试继承unittest.TestCase并被创建, 并且它可以被重载或增加相关方法. 例如:

.. code-block:: python

    import unittest

    class SimplisticTest(unittest.TestCase):
        def test(self):
            self.failUnless(True)

    if __name__ == '__main__':
        unittest.main()

在这个例子中, SimplisticTest仅包含一个test()方法, 如果不是True而是false时即会失败.

测试运行
----------

最简单的运行unitest测试的方式是在每个测试文件的底部包含下面的语句:

.. code-block:: python

    if __name__ == '__main__':
        unittest.main()

然后, 直接从命令行中运行这个脚本:

::

   $ python unittest_simple.py
   .
   ----------------------------------------------------------------------
   Ran 1 test in 0.000s

   OK
   
简短的输出中包含了测试所需的时间信息, 也包含每项测试的状态指标(第一行的"."表示通过一个测试项). 使用-v选项可以在测试结果中显示更详细的信息.

::

   $ python unittest_simple.py -v
   test (__main__.SimplisticTest) ... ok

   ----------------------------------------------------------------------
   Ran 1 test in 0.001s

   OK

测试结果输出
---------------

测试包含3个可能的结果输出:

ok: 测试通过.
FAIL: 测试没有通过, 并且引发一个AssertionError异常.
ERROR: 测试过程中引发一个不是AssertionError的异常.

这里不能直接让一个测试"pass", 所以测试的状态由是否存在某个异常决定.

.. code-block:: python

    class OutcomesTest(unittest.TestCase):

        def testPass(self):
            return

        def testFail(self):
            self.failIf(True)

	def testError(self):
 	    raise RuntimeError('Test error!')

当测试失败或产生一个错误, 那么在输出中会包含相关回溯信息.

::

   $ python unittest_outcomes.py
   EF.
   ======================================================================
   ERROR: testError (__main__.OutcomesTest)
   ----------------------------------------------------------------------
   Traceback (most recent call last):
     File "unittest_outcomes.py", line 43, in testError
     raise RuntimeError('Test error!')
   RuntimeError: Test error!

   ======================================================================
   FAIL: testFail (__main__.OutcomesTest)
   ----------------------------------------------------------------------
   Traceback (most recent call last):
     File "unittest_outcomes.py", line 40, in testFail
     self.failIf(True)
   AssertionError

   ----------------------------------------------------------------------
   Ran 3 tests in 0.002s

   FAILED (failures=1, errors=1)

在上面的例子中, testFail()失败, 回溯信息显示了引起失败的代码行. 大部分人可以阅读代码的测试输出来找出引起测试失败的语义. 为了能更容易的理解测试失败的本质原因, 可以使用 fail*() 和 assert*()方法, 并让它们接收msg参数, 指示在输出中显示更详细的错误信息.

.. code-block:: python

    class FailureMessageTest(unittest.TestCase):
        def testFail(self):
 	    self.failIf(True, 'failure message goes here')

::

   $ python unittest_failwithmessage.py -vtestFail (__main__.FailureMessageTest) ... FAIL

   ======================================================================
   FAIL: testFail (__main__.FailureMessageTest)
   ----------------------------------------------------------------------
   Traceback (most recent call last):
     File "unittest_failwithmessage.py", line 37, in testFail
     self.failIf(True, 'failure message goes here')
   AssertionError: failure message goes here

   ----------------------------------------------------------------------
   Ran 1 test in 0.002s

   FAILED (failures=1)

断言的本质
------------

大多数的测试在特定条件下进行断言测试. 编写truth-checking测试的方法也有很多, 采用哪个方法主要由测试者的个人习惯和想获得什么样的测试结果来决定. 如果由代码产生的值可视为真, 那么可以使用 failUnless() 和 assertTrue()方法, 如果该值可被评价为假, 那么, 使用failIf() 和 assertFalse()方法会更有意义.

.. code-block:: python

    class TruthTest(unittest.TestCase):
        def testFailUnless(self):
	    self.failUnless(True)

	def testAssertTrue(self):
	    self.assertTrue(True)

	def testFailIf(self):
	    self.failIf(False)

	def testAssertFalse(self):
 	    self.assertFalse(False)

等价测试
---------

这是一个特殊的测试类型, unittest包含了测试俩个值是否相等的方法.

.. code-block:: python

    class EqualityTest(unittest.TestCase):
        def testEqual(self):
	    self.failUnlessEqual(1, 3-2)

	def testNotEqual(self):
 	    self.failIfEqual(2, 3-2)

这些特殊的测试使用比较方便, 因为当测试失败时, 被比较的两个值会显示在失败信息中.

.. code-block:: python

    class InequalityTest(unittest.TestCase): 
        def testEqual(self):
	    self.failIfEqual(1, 3-2)

	def testNotEqual(self):
 	    self.failUnlessEqual(2, 3-2)

当运行这些测试, 可以看到:

::

   $ python unittest_notequal.py -v
   testEqual (__main__.EqualityTest) ... FAIL
   testNotEqual (__main__.EqualityTest) ... FAIL

   ======================================================================
   FAIL: testEqual (__main__.EqualityTest)
   ----------------------------------------------------------------------
   Traceback (most recent call last):
     File "unittest_notequal.py", line 37, in testEqual
     self.failIfEqual(1, 3-2)
   AssertionError: 1 == 1

   ======================================================================
   FAIL: testNotEqual (__main__.EqualityTest)
   ----------------------------------------------------------------------
   Traceback (most recent call last):
     File "unittest_notequal.py", line 40, in testNotEqual
     self.failUnlessEqual(2, 3-2)
   AssertionError: 2 != 1

   ----------------------------------------------------------------------
   Ran 2 tests in 0.002s

   FAILED (failures=2)

近似相等?
----------

除了严格的相等外, 对于浮点数来说, 可以测试两个数是否近似相等, 这种情况下, 可以使用failIfAlmostEqual() 和 failUnlessAlmostEqual().

.. code-block:: python

    class AlmostEqualTest(unittest.TestCase):
        def testNotAlmostEqual(self):
	    self.failIfAlmostEqual(1.1, 3.3-2.0, places=1)

	def testAlmostEqual(self):
 	    self.failUnlessAlmostEqual(1.1, 3.3-2.0, places=0)

它们的参数为2个待比较的数值, places表示小数位数, 指示测试时要考虑的小数位数.

::

   $ python unittest_almostequal.py 
   ..
   ----------------------------------------------------------------------
   Ran 2 tests in 0.001s

   OK

测试中的异常
-------------

之前也提到过, 如果一个测试引发了一个异常, 这会在测试过程中会被看成是一个错误. 这有利于显示在你修改了现有的测试代码后会出现的错误. 然而有时, 当你想在测试时确认是哪些代码产生了异常, 如一个对象的某个属性被赋于一无效值, 这些情况下, 使用TestCase.fallUnlessRaises()比直接捕获异常更容易简洁代码. 比较下面的两个测试:

.. code-block:: python

    def raises_error(*args, **kwds):
        print args, kwds
	raise ValueError('Invalid value: ' + str(args) + str(kwds))

    class ExceptionTest(unittest.TestCase):
	def testTrapLocally(self):
	    try:
	        raises_error('a', b='c')
	    except ValueError:
		pass
	    else:
		self.fail('Did not see ValueError')

	def testFailUnlessRaises(self):
	    self.failUnlessRaises(ValueError, raises_error, 'a', b='c')

两个测试的结果是一样的, 但第二个测试使用了failUnlessRaises(), 显得更加简洁.

::

   $ python unittest_exception.py -v
   testFailUnlessRaises (__main__.ExceptionTest) ... ('a',) {'b': 'c'}
   ok
   testTrapLocally (__main__.ExceptionTest) ... ('a',) {'b': 'c'}
   ok

   ----------------------------------------------------------------------
   Ran 2 tests in 0.001s

   OK

Test Fixtures
---------------

Fixtures是一个测试过程中所有需要的资源. 例如, 如果你正在写多个针对同一个类的测试用例, 这些测试用例都需要这个类的一个实例来作测试, 其他测试要用到的fixtures包括数据库连接和临时文件(许多人争论使用外部资源来让这些测试不像是"单元"测试, 但是他们仍然使用它们来测试, 结果也仍然是可用的). TestCase包括一些特殊的钩子用于配置和清理这些fixtures. 重载setUp()用于配置fixtures. 重载tearDown()用于清理fixtures.

.. code-block:: python

    class FixturesTest(unittest.TestCase):
        def setUp(self):
	    print 'In setUp()'
	    self.fixture = range(1, 10)

	def tearDown(self):
	    print 'In tearDown()'
	    del self.fixture

	def test(self):
	    print 'in test()'
	    self.failUnlessEqual(self.fixture, range(1, 10))

上面的测试运行之后, 你可以看到fixtures和测试方法的执行顺序:

::

   $ python unittest_fixtures.py 
   In setUp()
   in test()
   In tearDown()
   .
   ----------------------------------------------------------------------
   Ran 1 test in 0.001s

   OK

Test Suites(测试整合)
-----------------------

标准库文档讲述了怎样去手工组织test suites, 我一般也不直接使用test suites, 因为我更喜欢自动建立suites(它们是自动生成的测试集). 自动构建test suites对于大型工程来说尤其有用, 因为相关的测试不是全部都在一个地方. 使用像nose 和 Proctor 的这些工具, 对于遍布多个文件和目录的测试来说, 更加容易操作.

