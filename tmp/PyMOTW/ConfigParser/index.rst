=============================================
ConfigParser -- Work with configuration files
=============================================

.. module:: ConfigParser
    :synopsis: Read/write configuration files similar to Windows INI files

:Purpose: Read/write configuration files similar to Windows INI files
:Python Version: 1.5

The ConfigParser module is very useful for creating user-editable
configuration files for your applications. The configuration files are
broken up into sections, and each section can contain name-value pairs for
configuration data. Value interpolation using Python formatting strings
is also supported, to build values which depend on one another (this is
especially handy for paths or URLs).

Example
=======

At work, before we moved to svn and trac, we had rolled our own tool for
conducting distributed code reviews. To prepare the code for review, a
developer would write up a summary "approach" document, then attach code diffs
to it. The approach document supported comments through the web page, so
developers not located in our main office could also review code. The only
trouble was, posting the diffs could be a bit of a pain. To make that part of
the process easier, I wrote a command line tool to run against a CVS sandbox
to automatically find and post the diffs.

For the tool to update the diffs on an approach, it needed to know how to
reach the web server hosting the approach documents. Since our developers were
not always in the office, the URL to reach the server from any given host
might be port-forwarded through SSH. Rather than forcing each developer to use
the same port-forwarding scheme, the tool used a simple config file to
remember the URL.

A developer's configuration file might look like:

::

    [portal]
    url = http://%(host)s:%(port)s/Portal
    username = dhellmann
    host = localhost
    password = SECRET
    port = 8080


The "portal" section refers to the approach document web site. Once the diffs
were ready to be posted to the site, the tool would load the config file using
the ConfigParser module to access the URL. That might look something like
this:

.. include:: configparser_example.py
    :literal:
    :start-after: #end_pymotw_header


In the example above, the value of the url variable is
"``http://localhost:8080/Portal``". The "``url``" value from the config file
contains 2 formatting strings: "``%(host)s``" and "``%(port)s``". The values
of the host and port variables are automatically substituted in place of the
formatting strings by the ``get()`` method.

Of course, this is old code, written for Python 2.1. The ConfigParser module
has been improved in more recent versions. The ``SafeConfigParser`` class is a
drop in replacement for ``ConfigParser`` with improvements to the
interpolation processing.

For this tool, I only needed string options. The ConfigParser supports other
types of options as well: integer, floating point, and boolean. Since the
option file format does not offer a way to associate a "type" with a value,
the caller needs to know when to use a different method to retrieve options
with these other types. For example, to retrieve a boolean option, use the
``getboolean()`` method instead of ``get()``. The method arguments are the same, but
the option value is converted to a boolean before being returned. Similarly,
there are separate ``getint()`` and ``getfloat()`` methods.

The ConfigParser class also supports adding and removing sections to the file
programmaticaly, and saving the results. This makes it possible to create a
user interface for editing the configuration of your program, or to use the
config file format for simple data files. For example, an app which needed to
store a very small amount of data in a database-like format might take
advantage of ConfigParser so the files would be human-readable as well.

.. seealso::

    `ConfigParser <http://docs.python.org/library/configparser.html>`_
        The standard library documentation for this module.

