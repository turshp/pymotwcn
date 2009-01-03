PyMOTW: smtplib
=================

.. currentmodule:: smtplib

* 模块：smtplib
* 目的: 与smtp服务器交互，提供邮件发送
* python版本：1.5.2+

smtplib包含了SMTP类，用于与邮件服务器进行邮件通信。


.. note::

    在以下示例中，邮件地址、主机名称、ip地址都是虚假的，但是举例说明的命令副本和响应的信息都是存在的。


发送一封邮件
---------------

SMTP最常用的方法是连接服务器并发送一封邮件，在构造器中指定邮件服务器名和端口名，或者你可以使用connect()方法来指定。一旦建立连接，就可以调用sendmail()函数，并附带信封体参数和消息内容，消息文本应该与RFC2822兼容。smtplib不会自动修改消息内容和头信息，这就意味着你需要自己添加From和To等头信息。

.. code-block:: python

    import smtplib
    import email.utils
    from email.mime.text import MIMEText

    # Create the message
    msg = MIMEText('This is the body of the message.')
    msg['To'] = email.utils.formataddr(('Recipient', 'recipient@example.com'))
    msg['From'] = email.utils.formataddr(('Author', 'author@example.com'))
    msg['Subject'] = 'Simple test message'

    server = smtplib.SMTP('mail')
    server.set_debuglevel(True) # show communication with the server显示与服务器的通信情况
    try:
        server.sendmail('author@example.com', ['recipient@example.com'], msg.as_string())
    finally:
        server.quit()

在这个示例中，调试开关被打开了，这样可以显示客户端和服务端之间的通讯信息，否则，示例不会显示任何信息。

::

   $ python smtplib_sendmail.py
   send: 'ehlo localhost.local\r\n'
   reply: '250-mail.example.com Hello [192.168.1.17], pleased to meet you\r\n'
   reply: '250-ENHANCEDSTATUSCODES\r\n'
   reply: '250-PIPELINING\r\n'
   reply: '250-8BITMIME\r\n'
   reply: '250-SIZE\r\n'
   reply: '250-DSN\r\n'
   reply: '250-ETRN\r\n'
   reply: '250-AUTH GSSAPI DIGEST-MD5 CRAM-MD5\r\n'
   reply: '250-DELIVERBY\r\n'
   reply: '250 HELP\r\n'
   reply: retcode (250); Msg: mail.example.com Hello [192.168.1.17], pleased to meet you
   ENHANCEDSTATUSCODES
   PIPELINING
   8BITMIME
   SIZE
   DSN
   ETRN
   AUTH GSSAPI DIGEST-MD5 CRAM-MD5
   DELIVERBY
   HELP
   send: 'mail FROM:<author@example.com> size=266\r\n'
   reply: '250 2.1.0 <author@example.com>... Sender ok\r\n'
   reply: retcode (250); Msg: 2.1.0 <author@example.com>... Sender ok
   send: 'rcpt TO:<recipient@example.com>\r\n'
   reply: '250 2.1.5 <recipient@example.com>... Recipient ok\r\n'
   reply: retcode (250); Msg: 2.1.5 <recipient@example.com>... Recipient ok
   send: 'data\r\n'
   reply: '354 Enter mail, end with "." on a line by itself\r\n'
   reply: retcode (354); Msg: Enter mail, end with "." on a line by itself
   data: (354, 'Enter mail, end with "." on a line by itself')
   send: 'From nobody Sun Sep 28 10:02:48 2008\r\nContent-Type: text/plain; charset="us-ascii"\r\nMIME-Version: 1.0\r\nContent-Transfer-Encoding: 7bit\r\nTo: Recipient <recipient@example.com>\r\nFrom: Author <author@example.com>\r\nSubject: Simple test message\r\n\r\nThis is the body of the message.\r\n.\r\n'
   reply: '250 2.0.0 m8SE2mpc015614 Message accepted for delivery\r\n'
   reply: retcode (250); Msg: 2.0.0 m8SE2mpc015614 Message accepted for delivery
   data: (250, '2.0.0 m8SE2mpc015614 Message accepted for delivery')
   send: 'quit\r\n'
   reply: '221 2.0.0 mail.example.com closing connection\r\n'
   reply: retcode (221); Msg: 2.0.0 mail.example.com closing connection

注意sendmail的第二个参数，收件人信息需要是一个list结构，你可以在list写上很多的邮件地址，message会依次把消息发送给他们. 由于信封信息和和邮件头是分开的，所以你可以通过一些方法参数来指定密送一些人，但不可以在邮件头中设置。 

认证和加密
------------

SMTP同样可以处理认证和TLS(一种底层通讯的安全协议)加密。如果服务器支持它们，你可以自己来检测服务器是否支持TLS，可以直接调用ehlo()来鉴定并询问服务器支持何种类型扩展 。然后通过调用has_extn()来检查结果。一旦启动TLS，你可以在认证之前再次调用ehlo()。

.. code-block:: python

    import smtplib
    import email.utils
    from email.mime.text import MIMEText
    import getpass

    # Prompt the user for connection info
    to_email = raw_input('Recipient: ')
    servername = raw_input('Mail server name: ')
    username = raw_input('Mail user name: ')
    password = getpass.getpass("%s's password: " % username)

    # Create the message
    msg = MIMEText('Test message from PyMOTW.')
    msg.set_unixfrom('author')
    msg['To'] = email.utils.formataddr(('Recipient', to_email))
    msg['From'] = email.utils.formataddr(('Author', 'author@example.com'))
    msg['Subject'] = 'Test from PyMOTW'

    server = smtplib.SMTP(servername)
    try:
        server.set_debuglevel(True)

        # identify ourselves, prompting server for supported features
        server.ehlo()

        # If we can encrypt this session, do it
        if server.has_extn('STARTTLS'):
             server.starttls()
             server.ehlo() # re-identify ourselves over TLS connection

        server.login(username, password)
        server.sendmail('author@example.com', [to_email], msg.as_string())
    finally:
        server.quit()

注意STARTTLS不会出现在扩展列表中，因为启动了TLS。

::

   $ python smtplib_authenticated.py
   Recipient: recipient@example.com
   Mail server name: smtpauth.isp.net
   Mail user name: user@isp.net
   user@isp.net's password:
   send: 'ehlo localhost.local\r\n'
   reply: '250-elasmtp-isp.net Hello localhost.local [<your IP here>]\r\n'
   reply: '250-SIZE 14680064\r\n'
   reply: '250-PIPELINING\r\n'
   reply: '250-AUTH PLAIN LOGIN CRAM-MD5\r\n'
   reply: '250-STARTTLS\r\n'
   reply: '250 HELP\r\n'
   reply: retcode (250); Msg: elasmtp-isp.net Hello localhost.local [<your IP here>]
   SIZE 14680064
   PIPELINING
   AUTH PLAIN LOGIN CRAM-MD5
   STARTTLS
   HELP
   send: 'STARTTLS\r\n'
   reply: '220 TLS go ahead\r\n'
   reply: retcode (220); Msg: TLS go ahead
   send: 'ehlo localhost.local\r\n'
   reply: '250-elasmtp-isp.net Hello localhost.local [<your IP here>]\r\n'
   reply: '250-SIZE 14680064\r\n'
   reply: '250-PIPELINING\r\n'
   reply: '250-AUTH PLAIN LOGIN CRAM-MD5\r\n'
   reply: '250 HELP\r\n'
   reply: retcode (250); Msg: elasmtp-isp.net Hello farnsworth.local [<your IP here>]
   SIZE 14680064
   PIPELINING
   AUTH PLAIN LOGIN CRAM-MD5
   HELP
   send: 'AUTH CRAM-MD5\r\n'
   reply: '334 PDExNjkyLjEyMjI2MTI1NzlAZWxhc210cC1tZWFseS5hdGwuc2EuZWFydGhsaW5rLm5ldD4=\r\n'
   reply: retcode (334); Msg: PDExNjkyLjEyMjI2MTI1NzlAZWxhc210cC1tZWFseS5hdGwuc2EuZWFydGhsaW5rLm5ldD4=
   send: 'ZGhlbGxtYW5uQGVhcnRobGluay5uZXQgN2Q1YjAyYTRmMGQ1YzZjM2NjOTNjZDc1MDQxN2ViYjg=\r\n'
   reply: '235 Authentication succeeded\r\n'
   reply: retcode (235); Msg: Authentication succeeded
   send: 'mail FROM:<author@example.com> size=221\r\n'
   reply: '250 OK\r\n'
   reply: retcode (250); Msg: OK
   send: 'rcpt TO:<recipient@example.com>\r\n'
   reply: '250 Accepted\r\n'
   reply: retcode (250); Msg: Accepted
   send: 'data\r\n'
   reply: '354 Enter message, ending with "." on a line by itself\r\n'
   reply: retcode (354); Msg: Enter message, ending with "." on a line by itself
   data: (354, 'Enter message, ending with "." on a line by itself')
   send: 'Content-Type: text/plain; charset="us-ascii"\r\nMIME-Version: 1.0\r\nContent-Transfer-Encoding: 7bit\r\nTo: Recipient <recipient@example.com>\r\nFrom: Author <author@example.com>\r\nSubject: Test from PyMOTW\r\n\r\nTest message from PyMOTW.\r\n.\r\n'
   reply: '250 OK id=1KjxNj-00032a-Ux\r\n'
   reply: retcode (250); Msg: OK id=1KjxNj-00032a-Ux
   data: (250, 'OK id=1KjxNj-00032a-Ux')
   send: 'quit\r\n'
   reply: '221 elasmtp-isp.net closing connection\r\n'
   reply: retcode (221); Msg: elasmtp-isp.net closing connection

验证一个邮件地址
-----------------

SMTP协议包含一个命令可以询问服务器一个邮件地址是否合法，通常VRFY是关闭的，以防止垃圾邮件发送者找到合法的邮件地址，但是，如果它打开，你可以向服务器询问这个邮件地址并接受一个状态码，如果是可用的，那么会返回一个可用的完整用户名。

.. code-block:: python

    import smtplib

    server = smtplib.SMTP('mail')
    server.set_debuglevel(True) # show communication with the server
    try:
        dhellmann_result = server.verify('dhellmann')
        notthere_result = server.verify('notthere')
    finally:
        server.quit()

    print 'dhellmann:', dhellmann_result
    print 'notthere :', notthere_result

最后二行输出中表示，地址 dhellmann是合法的，notthere是非法的。

::

   $ python smtplib_verify.py
   send: 'vrfy <dhellmann>\r\n'
   reply: '250 2.1.5 Doug Hellmann <dhellmann@mail.example.com>\r\n'
   reply: retcode (250); Msg: 2.1.5 Doug Hellmann <dhellmann@mail.example.com>
   send: 'vrfy <notthere>\r\n'
   reply: '550 5.1.1 <notthere>... User unknown\r\n'
   reply: retcode (550); Msg: 5.1.1 <notthere>... User unknown
   send: 'quit\r\n'
   reply: '221 2.0.0 mail.example.com closing connection\r\n'
   reply: retcode (221); Msg: 2.0.0 mail.example.com closing connection
   dhellmann: (250, '2.1.5 Doug Hellmann <dhellmann@mail.example.com>')
   notthere : (550, '5.1.1 <notthere>... User unknown')

参考
-----

* `RFC 821: Simple Mail Transfer Protocol <http://www.faqs.org/rfcs/rfc821.html>`_
* `RFC 822: Standard for the Format of ARPA Internet Text Messages <http://www.faqs.org/rfcs/rfc822.html>`_
* `RFC 1869: SMTP Service Extensions <http://www.faqs.org/rfcs/rfc1869.html>`_
* `RFC 2822: Internet Message Format <http://www.faqs.org/rfcs/rfc2822.html>`_
* `标准库文档: smtplib <http://docs.python.org/lib/module-smtplib.html>`_
