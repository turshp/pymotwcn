#使用reportlab生成PDF过程记录 liz的过程

# 使用Reportlab生成PDF文件 #

## 下载 ##
可以从[这里](http://www.reportlab.org/ftp/ReportLab_2_2.tgz)下载, 或者直接新立得安装python-reportlab

## 安装 ##
使用源码安装时出现:
```
$ sudo python setup.py tests-preinstall
[sudo] password for shengyan: 
...............................Failed to import renderPM.
..................................................
----------------------------------------------------
Ran 166 tests in 263.699s

OK
```
出现错误, 后来直接用新立得中安装python-reportlab, 之后import reportlab没问题

## 使用 ##
使用现成的rst2pdf.py尝试运行出现:
```
$ python rst2pdf.py whatnow.rst 
Traceback (most recent call last):
  File "rst2pdf.py", line 4, in <module>
    import docutils.core,docutils.nodes,sys,re
ImportError: No module named docutils.core
```
后来又装python-docutils, 再运行, 没有导入问题了, 但是出现一大堆:
```
No support for hyphenation, install wordaxe
No hyphenation support install wordaxe #断字不支持
No support for hyphenation, install wordaxe
<string>:14: (ERROR/3) Unknown interpreted text role "ref".
<string>:24: (ERROR/3) Unknown interpreted text role "ref".
<string>:27: (ERROR/3) Unknown interpreted text role "ref".
<string>:56: (ERROR/3) Unknown interpreted text role "newsgroup".
<string>:56: (ERROR/3) Unknown interpreted text role "file".
:ref:`library-index`
<string>:14: (INFO/1) No role entry for "ref" in module "docutils.parsers.rst.languages.en".
Trying "ref" as canonical role name.
<string>:14: (ERROR/3) Unknown interpreted text role "ref".
:ref:`install-index`
<string>:24: (INFO/1) No role entry for "ref" in module "docutils.parsers.rst.languages.en".
Trying "ref" as canonical role name.
<string>:24: (ERROR/3) Unknown interpreted text role "ref".
:ref:`reference-index`
<string>:27: (INFO/1) No role entry for "ref" in module "docutils.parsers.rst.languages.en".
Trying "ref" as canonical role name.
<string>:27: (ERROR/3) Unknown interpreted text role "ref".
:newsgroup:`comp.lang.python`
:file:`Misc/`
<string>:56: (INFO/1) No role entry for "newsgroup" in module "docutils.parsers.rst.languages.en".
Trying "newsgroup" as canonical role name.
<string>:56: (ERROR/3) Unknown interpreted text role "newsgroup".
<string>:56: (INFO/1) No role entry for "file" in module "docutils.parsers.rst.languages.en".
Trying "file" as canonical role name.
<string>:56: (ERROR/3) Unknown interpreted text role "file".
```
有些标记不识别,不过不管他, 因为已经生成了pdf文件,对中文支持也ok.


除了上述一些问题, 算是ok.具体reportlab提供的各种方法还没有看完....


## 另外 ##
有个c扩展的一个东西, 在README:
```
The C extension are optional but anyone able to do so should
use _rl_accel as it helps achieve acceptable speeds.  The
_renderPM extension allows graphics (such as charts) to be saved
as bitmap images for the web, as well as inside PDFs.
```
就是里面的renderPM, 需要安装python-reportlab-accel-dbg, 这是可选的.

# 相关资源 #
  * [reportlab官网](http://www.reportlab.org/)
  * [用 python-reportlab 将 rst 转换为中文 PDF](http://wiki.woodpecker.org.cn/moin/UsageRstReportlabExPdf)
  * [用 Reportlab 生成中文 PDF](http://wiki.woodpecker.org.cn/moin/MiscItems/2008-08-08)