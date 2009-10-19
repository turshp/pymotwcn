============================================================================
platform -- 访问系统硬件,操作系统和解释器版本信息. 
============================================================================

.. module:: platform
    :synopsis: 访问系统硬件,操作系统和解释器版本信息. 

:目的: 使用platform模块访问系统平台的结构和版本信息的. 
:Python 版本: 2.3+

尽管Python是一种跨平台的语言, 它仍然需要了解当前系统信息. 制作系统工具时常会需要这些信息, 正如你所知道的, 有些库或外部命令在不同的操作系统中是完全不同的. 例如, 如果你正编写一个程序来管理操作系统的网络配置, 你可以得到网络接口,别名,IP地址等的配置. 但一旦当你开始编辑配置文件, 你需要更详细地了解你的主机以及如何配置. platform模块为你提供了一些工具, 让你可以了解程序运行时所使用的解释器,操作系统和硬件平台. 

.. 注意::

    下面实例所显示的输出结果是在安装OS X 10.5.2系统的MacBook Pro机子上测试得到的, 对于Linux系统中的结果是使用VMware虚拟机运行CentOS 4.6所得到的结果. 我没实际在Windows上测试, 但这些代码在测试环境下运行良好. (如果有人将下面的脚本在Windows测试, 请将输出结果发布到评论当中, 我将不胜感激！)

解释器
===========

模块提供了4个方法来获取当前的Python解释器的信息. python_version()和python_version_tuple()以不同的形式返回解释器的版本信息, 包括：主版本号, 次版本号和补丁级别组件.  python_compiler()返回用于创建解释器所使用的编译器信息. python_build()返回字符串版本的创建信息. 

.. include:: platform_python.py
    :literal:
    :start-after: #end_pymotw_header


OS X::

    $ python platform_python.py
    Version      : 2.5.1
    Version tuple: ['2', '5', '1']
    Compiler     : GCC 4.0.1 (Apple Computer, Inc. build 5367)
    Build        : ('r251:54869', 'Apr 18 2007 22:08:04')


Linux::

    $ python platform_python.py 
    Version      : 2.4.4
    Version tuple: ['2', '4', '4']
    Compiler     : GCC 3.4.6 20060404 (Red Hat 3.4.6-9)
    Build        : (1, 'Mar 12 2008 15:09:04')

(看来我需要升级系统...)

Windows::

    C:> python.exe platform_python.py
    Version : 2.5.4
    Version tuple: ['2', '5', '4']
    Compiler : MSC v.1310 32 bit (Intel)
    Build : ('r254:67916', 'Dec 23 2008 15:10:54')

操作系统
========

操作系统的版本信息可通过platform()函数获取. platform()接受两个可选布尔值类型的参数. 如果aliased为True, 返回值所返回的将是普通的版本值. 当terse是True, 返回值为省略部分信息的简化后的版本值. 操作系统的版本信息可通过platform()函数获取. platform()接受两个可选布尔值类型的参数. 如果aliased为True, 返回值所返回的将是普通的版本值. 当terse是True, 返回值为省略部分信息的简化后的版本值. 

.. include:: platform_platform.py
    :literal:
    :start-after: #end_pymotw_header

OS X::

    $ python platform_platform.py
    Normal : Darwin-9.2.2-i386-32bit
    Aliased: Darwin-9.2.2-i386-32bit
    Terse  : Darwin-9.2.2

Linux::

    $ python platform_platform.py 
    Normal : Linux-2.6.9-67.0.4.ELsmp-i686-with-redhat-4.6-Final
    Aliased: Linux-2.6.9-67.0.4.ELsmp-i686-with-redhat-4.6-Final
    Terse  : Linux-2.6.9-67.0.4.ELsmp-i686-with-glibc2.3

Windows::

    C:> python.exe platform_platform.py
    Normal : Windows-XP-5.1.2600
    Aliased: Windows-XP-5.1.2600
    Terse : Windows-XP
    

操作系统和硬件信息
==================================

也可获得解释器运行时所在操作系统和硬件的详细信息. uname()返回一个包含系统信息,主机名称,发布,版本,机器和处理器信息的元组. 各个值可通过同名函数来得到：
system() returns the operating system name. node() returns the hostname of the server, not fully qualified. release() returns the operating system release number. version() returns the more detailed system version. machine() gives a hardware-type identifier such as 'i386'. processor() returns a real identifier for the processor, or the same value as machine() in many cases.
system()返回的操作系统名称. node()返回的服务器主机名称, 不是完全格式. release()返回的操作系统发布编号. version()返回详细的系统版本信息. machine()提供了硬件类型标识符, 如'i386' . processor()返回一个实际处理器标识符, 或返回与machine()相同的值.  system()返回的操作系统名称. node()返回的服务器主机名称, 不是完全格式. release()返回的操作系统发布编号. version()返回详细的系统版本信息. machine()提供了硬件类型标识符, 如'i386' . processor()返回一个实际处理器标识符, 或返回与machine()相同的值. 


.. include:: platform_os_info.py
    :literal:
    :start-after: #end_pymotw_header


OS X::

    $ python platform_os_info.py
    uname: ('Darwin', 'farnsworth.local', '9.2.2', 'Darwin Kernel Version 9.2.2: Tue Mar  4 21:17:34 PST 2008; root:xnu-1228.4.31~1/RELEASE_I386', 'i386', 'i386')

    system   : Darwin
    node     : farnsworth.local
    release  : 9.2.2
    version  : Darwin Kernel Version 9.2.2: Tue Mar  4 21:17:34 PST 2008; root:xnu-1228.4.31~1/RELEASE_I386
    machine  : i386
    processor: i386

Linux::

    $ python platform_os_info.py 
    uname: ('Linux', 'zoidberg', '2.6.9-67.0.4.ELsmp', '#1 SMP Sun Feb 3 07:08:57 EST 2008', 'i686', 'i686')

    system   : Linux
    node     : zoidberg
    release  : 2.6.9-67.0.4.ELsmp
    version  : #1 SMP Sun Feb 3 07:08:57 EST 2008
    machine  : i686
    processor: i686

Windows::

    C:> python.exe platform_os_info.py
    uname: ('Windows', 'argent', 'XP', '5.1.2600', '', '')

    system : Windows
    node : argent
    release : XP
    version : 5.1.2600
    machine :
    processor:
    

可执行程序架构
=======================

各个程序的系统架构信息可以利用architecture()函数来得到. 第一个参数必须为一个可执行程序的路径(默认为sys.executable , 指向Python解释器). 返回值是一个包含程序指令结构和所用链接格式的元组. 各个程序的系统架构信息可以利用architecture()函数来得到. 第一个参数必须为一个可执行程序的路径(默认为sys.executable , 指向Python解释器). 返回值是一个包含程序指令结构和所用链接格式的元组. 

.. include:: platform_architecture.py
    :literal:
    :start-after: #end_pymotw_header


OS X::

    $ python platform_architecture.py
    interpreter: ('32bit', '')
    /bin/ls    : ('32bit', '')

Linux::

    $ python platform_architecture.py 
    interpreter: ('32bit', 'ELF')
    /bin/ls    : ('32bit', 'ELF')

Windows::

    C:> python.exe platform_architecture.py
    interpreter: ('32bit', 'WindowsPE')
    explorer.exe : ('32bit', '')

.. 参见::

    `platform <http://docs.python.org/lib/module-platform.html>`_
        此模块的标准库文档. 
