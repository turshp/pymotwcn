PyMOTW: locale
===================

.. currentmodule:: locale

* 模块：locale
* 目的：POSIX标准的本地化API
* python版本：1.5,在2.5版本中有所扩展


描述
----

locale模块是Python国际化和本地化支持库的一部分. 他提供一种用于处理那些可能依赖于你用户语言或位置的操作的标准方式. 例如, 货币格式化, 比较字符串以便排序, 处理时间日期. 他没有包含翻译(可参见gettext模块)或Unicode编码.

由于可以在应用程序范围内改变本地化设置, 所以推荐用户避免在库中改变值而是让应用程序一次性设置. 在下面的例子中, 我会改变本地的一些时间以便说明目的.这更像是一旦你的应用程序启动就去设置本地化参数.

例子
----

让用户改变一个应用程序的本地设置的最一般的方式是通过一个环境变量（LC__ALL, LC__CTYPE, LANG, 或LANGUAGE, 这依赖于你的平台). 然后程序会调用locale.setlocale(), 没有使用硬编码值, 而是使用环境变量.

.. code-block:: python

    import locale
    import os
    import pprint

    print 'Environment settings:'
    for env_name in [ 'LC_ALL', 'LC_CTYPE', 'LANG', 'LANGUAGE' ]:
        print '\t%s = %s' % (env_name, os.environ.get(env_name, ''))

    # What is the default locale?默认的本地设置是什么?
    print
    print 'Default locale:', locale.getdefaultlocale()

    # Default settings based on the user's environment.根据用户的环境做些默认设置
    locale.setlocale(locale.LC_ALL, '')

    # If we do not have a locale, assume US English.如果没有本地设置, 假设为US English
    print 'From environment:', locale.getlocale()

    pprint.pprint(locale.localeconv())

在我的Mac上, 这个程序输出类似如下:

:: 

   $ python locale_env_example.py
   Environment settings:
    LC_ALL =
    LC_CTYPE =
    LANG =
    LANGUAGE =

   Default locale: (None, 'mac-roman')
   From environment: (None, None)
   {'currency_symbol': '',
    'decimal_point': '.',
    'frac_digits': 127,
    'grouping': [127],
    'int_curr_symbol': '',
    'int_frac_digits': 127,
    'mon_decimal_point': '',
    'mon_grouping': [127],
    'mon_thousands_sep': '',
    'n_cs_precedes': 127,
    'n_sep_by_space': 127,
    'n_sign_posn': 127,
    'negative_sign': '',
    'p_cs_precedes': 127,
    'p_sep_by_space': 127,
    'p_sign_posn': 127,
    'positive_sign': '',
    'thousands_sep': ''}

现在如果我们设置好LANG值后再运行同样的脚本, 可以看到本地设置和默认编码因此改变:

法国:

::

   $ LANG=fr_FR python locale_env_example.py
   Environment settings:
    LC_ALL =
    LC_CTYPE =
    LANG = fr_FR
    LANGUAGE =

   Default locale: (None, 'mac-roman')
   From environment: ('fr_FR', 'ISO8859-1')
   {'currency_symbol': 'Eu',
    'decimal_point': ',',
    'frac_digits': 2,
    'grouping': [127],
    'int_curr_symbol': 'EUR ',
    'int_frac_digits': 2,
    'mon_decimal_point': ',',
    'mon_grouping': [3, 3, 0],
    'mon_thousands_sep': ' ',
    'n_cs_precedes': 0,
    'n_sep_by_space': 1,
    'n_sign_posn': 2,
    'negative_sign': '-',
    'p_cs_precedes': 0,
    'p_sep_by_space': 1,
    'p_sign_posn': 1,
    'positive_sign': '',
    'thousands_sep': ''}

西班牙:

::

   $ LANG=es_ES python locale_env_example.py
   Environment settings:
    LC_ALL =
    LC_CTYPE =
    LANG = es_ES
    LANGUAGE =

   Default locale: (None, 'mac-roman')
   From environment: ('es_ES', 'ISO8859-1')
   {'currency_symbol': 'Eu',
    'decimal_point': ',',
    'frac_digits': 2,
    'grouping': [127],
    'int_curr_symbol': 'EUR ',
    'int_frac_digits': 2,
    'mon_decimal_point': ',',
    'mon_grouping': [3, 3, 0],
    'mon_thousands_sep': '.',
    'n_cs_precedes': 1,
    'n_sep_by_space': 1,
    'n_sign_posn': 1,
    'negative_sign': '-',
    'p_cs_precedes': 1,
    'p_sep_by_space': 1,
    'p_sign_posn': 1,
    'positive_sign': '',
    'thousands_sep': ''}

葡萄牙:

:: 

   $ LANG=pt_PT python locale_env_example.py
   Environment settings:
    LC_ALL =
    LC_CTYPE =
    LANG = pt_PT
    LANGUAGE =

   Default locale: (None, 'mac-roman')
   From environment: ('pt_PT', 'ISO8859-1')
   {'currency_symbol': 'Eu',
    'decimal_point': ',',
    'frac_digits': 2,
    'grouping': [127],
    'int_curr_symbol': 'EUR ',
    'int_frac_digits': 2,
    'mon_decimal_point': '.',
    'mon_grouping': [3, 3, 0],
    'mon_thousands_sep': '.',
    'n_cs_precedes': 0,
    'n_sep_by_space': 1,
    'n_sign_posn': 1,
    'negative_sign': '-',
    'p_cs_precedes': 0,
    'p_sep_by_space': 1,
    'p_sign_posn': 1,
    'positive_sign': '',
    'thousands_sep': ' '}

波兰:

::

   $ LANG=pl_PL python locale_env_example.py
   Environment settings:
    LC_ALL =
    LC_CTYPE =
    LANG = pl_PL
    LANGUAGE =

   Default locale: (None, 'mac-roman')
   From environment: ('pl_PL', 'ISO8859-2')
   {'currency_symbol': 'z?\x82',
    'decimal_point': ',',
    'frac_digits': 2,
    'grouping': [3, 3, 0],
    'int_curr_symbol': 'PLN ',
    'int_frac_digits': 2,
    'mon_decimal_point': ',',
    'mon_grouping': [3, 3, 0],
    'mon_thousands_sep': ' ',
    'n_cs_precedes': 1,
    'n_sep_by_space': 2,
    'n_sign_posn': 4,
    'negative_sign': '-',
    'p_cs_precedes': 1,
    'p_sep_by_space': 2,
    'p_sign_posn': 4,
    'positive_sign': '',
    'thousands_sep': ' '}

所以你可以看到货币符号(currency_symbol)设置改变了, 从小数中分离出整个数字的分割字符(decimal_point)也改变了, 等等. 现在以不同的地区设置(US 美元, 欧元, 和Polish złoty)格式输出同样的信息:

.. code-block:: python

    sample_locales = [ ('USA', 'en_US'),
                       ('France', 'fr_FR'),
                       ('Spain', 'es_ES'),
                       ('Portugal', 'pt_PT'),
                       ('Poland', 'pl_PL'),
                     ]

    for name, loc in sample_locales:
        locale.setlocale(locale.LC_ALL, loc)
        print '%20s: %s' % (name, locale.currency(1234.56))

输出一个小的表格:

:: 

   $ python locale_currency_example.py
   USA: $1234.56
   France: 1234,56 Eu
   Spain: Eu 1234,56
   Portugal: 1234.56 Eu
   Poland: zł 1234,56

除了以不同的格式输出外, 本地化模块还可以帮助解析输入. 不同的文化对数字格式化使用不同的转换(上面已列出). 本地化模块提供atoi()和atof()函数分别用来进行字符串与整数和浮点数之间的转换.

.. code-block:: python

    sample_data = [ ('USA', 'en_US', '1234.56'),
                    ('France', 'fr_FR', '1234,56'),
                    ('Spain', 'es_ES', '1234,56'),
                    ('Portugal', 'pt_PT', '1234.56'),
                    ('Poland', 'pl_PL', '1234,56'),
                  ]

    for name, loc, a in sample_data:
        locale.setlocale(locale.LC_ALL, loc)
        f = locale.atof(a)
        locale.setlocale(locale.LC_ALL, 'en_US')
        print '%20s: %7s => %f' % (name, a, f)

::

   $ python locale_atof_example.py
   USA: 1234.56 => 1234.560000
   France: 1234,56 => 1234.560000
   Spain: 1234,56 => 1234.560000
   Portugal: 1234.56 => 1234.560000
   Poland: 1234,56 => 1234.560000

另一个本地化的重要方面是时间和日期的格式化:

.. code-block:: python

    import locale
    import time

    sample_locales = [ ('USA', 'en_US'),
                       ('France', 'fr_FR'),
                       ('Spain', 'es_ES'),
                       ('Portugal', 'pt_PT'),
                       ('Poland', 'pl_PL'),
                     ]

    for name, loc in sample_locales:
        locale.setlocale(locale.LC_ALL, loc)
        print '%20s: %s' % (name, time.strftime(locale.nl_langinfo(locale.D_T_FMT)))

::

   $ python locale_date_example.py

   USA: Sun May 20 10:19:54 2007
   France: Dim 20 mai 10:19:54 2007
   Spain: dom 20 may 10:19:54 2007
   Portugal: Dom 20 Mai 10:19:54 2007
   Poland: ndz 20 maj 10:19:54 2007

这个星期我只阐述了本地化模块中的一些高层函数. 还有其他低层(格式化字符串)或那些管理你应用程序本地化的函数(resetlocale). 和往常一样, 你可以参考Python库文档来查看些细节.


参考
-----

* `Locale - Wikipedia <http://en.wikipedia.org/wiki/Locale>`_
* `Internationalization and localization - Wikipedia <http://en.wikipedia.org/wiki/Internationalization_and_localization>`_
* `OpenI18N.org - The Free standards Group Open Internationalisation Initiative <http://www.openi18n.org/>`_
* `MSDN - National Language Support Constants <http://msdn.microsoft.com/library/default.asp?url=/library/en-us/intl/nls_238z.asp>`_
* `Internationalizing Python <http://www.python.org/workshops/1997-10/proceedings/loewis.html>`_

