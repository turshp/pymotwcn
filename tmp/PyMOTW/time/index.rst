====
time
====
.. module:: time
    :synopsis: Functions for manipulating times.

:Module: time
:Purpose: Functions for manipulating times.
:Python Version: 1.4 or earlier
:Abstract:

    The time module provides functions for working with dates and times.

Description
===========

The time module exposes C library functions for manipulating dates and times.
Since it is tied to the underlying C implementation, some details (such as the
start of the epoch and maximum date value supported) are platform-specific.
Refer to the library documentation for complete details.

Wall Clock Time
===============

One of the core functions of the time module is time.time(), which returns the
number of seconds since the start of the epoch as a floating point value. 

::

    import time

    print 'The time is:', time.time()

Although the value is always a float, actual precision is platform-dependent.

::

    $ python time_time.py
    The time is: 1205079300.54

The float representation is useful when storing or comparing dates, but not as
useful for producing human readable representations. For logging or printing
time time.ctime() can be more useful.

::

    import time

    print 'The time is      :', time.ctime()
    later = time.time() + 15
    print '15 secs from now :', time.ctime(later)

Here the second output line shows how to use ctime() to format a time value
other than the current time.

::

    $ python time_ctime.py
    The time is      : Sun Mar  9 12:18:02 2008
    15 secs from now : Sun Mar  9 12:18:17 2008

Processor Clock Time
====================

While time() returns a wall clock time, clock() returns processor clock time.
The values returned from clock() should be used for performance testing,
benchmarking, etc. since they reflect the actual time used by the program, and
can be more precise than the values from time().

::

    import hashlib
    import time

    # Data to use to calculate md5 checksums
    data = open(__file__, 'rt').read()

    for i in range(5):
        h = hashlib.sha1()
        print time.ctime(), ': %0.3f %0.3f' % (time.time(), time.clock())
        for i in range(100000):
            h.update(data)
        cksum = h.digest()


In this example, the formatted ctime() is printed along with the floating
point values from time(), and clock() for each iteration through the loop. If
you want to run the example on your system, you may have to add more cycles to
the inner loop or work with a larger amount of data to actually see a
difference.

::

    $ python time_clock.py
    Sun Mar  9 12:41:53 2008 : 1205080913.260 0.030
    Sun Mar  9 12:41:53 2008 : 1205080913.682 0.440
    Sun Mar  9 12:41:54 2008 : 1205080914.103 0.860
    Sun Mar  9 12:41:54 2008 : 1205080914.518 1.270
    Sun Mar  9 12:41:54 2008 : 1205080914.932 1.680

Typically, the processor clock doesn't tick if your program isn't doing
anything.

::

    import time

    for i in range(6, 1, -1):
        print '%s %0.2f %0.2f' % (time.ctime(), time.time(), time.clock())
        print 'Sleeping', i
        time.sleep(i)


In this example, the loop does very little work by going to sleep after each
iteration. The time.time() value increases even while the app is asleep, but
the time.clock() value does not.

::

    $ python time_clock_sleep.py
    Sun Mar  9 12:46:36 2008 1205081196.20 0.02
    Sleeping 6
    Sun Mar  9 12:46:42 2008 1205081202.20 0.02
    Sleeping 5
    Sun Mar  9 12:46:47 2008 1205081207.20 0.02
    Sleeping 4
    Sun Mar  9 12:46:51 2008 1205081211.20 0.02
    Sleeping 3
    Sun Mar  9 12:46:54 2008 1205081214.21 0.02
    Sleeping 2

Calling time.sleep() yields control from the current thread and asks it to
wait for the system to wake it back up. If your program has only one thread,
this effectively blocks the app and it does no work.

struct_time
===========

Storing times as elapsed seconds is useful in some situations, but there are
times when you need to have access to the individual fields of a date (year,
month, etc.). The time module defines struct_time for holding date and time
values with components broken out so they are easy to access. There are
several functions that work with struct_time values instead of floats.

::

    import time

    print 'gmtime   :', time.gmtime()
    print 'localtime:', time.localtime()
    print 'mktime   :', time.mktime(time.localtime())

    print
    t = time.localtime()
    print 'Day of month:', t.tm_mday
    print ' Day of week:', t.tm_wday
    print ' Day of year:', t.tm_yday

gmtime() returns the current time in UTC. localtime() returns the current time
with the current time zone applied. mktime() takes a struct_time and converts
it to the floating point representation.

::

    $ python time_struct.py
    gmtime   : (2008, 3, 9, 16, 58, 19, 6, 69, 0)
    localtime: (2008, 3, 9, 12, 58, 19, 6, 69, 1)
    mktime   : 1205081899.0

    Day of month: 9
     Day of week: 6
     Day of year: 69


Parsing and Formatting Times
============================

The two functions strptime() and strftime() convert between struct_time and
string representations of time values. There is a long list of formatting
instructions available to support input and output in different styles. The
complete list is documented in the library documentation for the time module.

This example converts the current time from a string, to a struct_time
instance, and back to a string.

::

    import time

    now = time.ctime()
    print now
    parsed = time.strptime(now)
    print parsed
    print time.strftime("%a %b %d %H:%M:%S %Y", parsed)

The output string is not exactly like the input, since the day of the month is
prefixed with a zero.

::

    $ python time_strptime.py
    Sun Mar  9 13:01:19 2008
    (2008, 3, 9, 13, 1, 19, 6, 69, -1)
    Sun Mar 09 13:01:19 2008

Working with Time Zones
=======================

The functions for determining the current time depend on having the time zone
set, either by your program or by using a default time zone set for the
system. Changing the time zone does not change the actual time, just the way
it is represented.

To change the time zone, set the environment variable TZ, then call tzset().
Using TZ, you can specify the time zone with a lot of detail, right down to
the start and stop times for daylight savings time. It is usually easier to
use the time zone name and let the underlying libraries derive the other
information, though.

This example program changes the time zone to a few different values and shows
how the changes affect other settings in the time module.

::

    import time
    import os

    def show_zone_info():
        print '\tTZ    :', os.environ.get('TZ', '(not set)')
        print '\ttzname:', time.tzname
        print '\tZone  : %d (%d)' % (time.timezone, (time.timezone / 3600))
        print '\tDST   :', time.daylight
        print '\tTime  :', time.ctime()
        print

    print 'Default :'
    show_zone_info()

    for zone in [ 'US/Eastern', 'US/Pacific', 'GMT', 'Europe/Amsterdam' ]:
        os.environ['TZ'] = zone
        time.tzset()
        print zone, ':'
        show_zone_info()

My default time zone is US/Eastern, so setting TZ to that has no effect. The
other zones used change the tzname, daylight flag, and timezone offset value.

::

    $ python time_timezone.py
    Default :
        TZ    : (not set)
        tzname: ('EST', 'EDT')
        Zone  : 18000 (5)
        DST   : 1
        Time  : Sun Mar  9 13:06:53 2008

    US/Eastern :
        TZ    : US/Eastern
        tzname: ('EST', 'EDT')
        Zone  : 18000 (5)
        DST   : 1
        Time  : Sun Mar  9 13:06:53 2008

    US/Pacific :
        TZ    : US/Pacific
        tzname: ('PST', 'PDT')
        Zone  : 28800 (8)
        DST   : 1
        Time  : Sun Mar  9 10:06:53 2008

    GMT :
        TZ    : GMT
        tzname: ('GMT', 'GMT')
        Zone  : 0 (0)
        DST   : 0
        Time  : Sun Mar  9 17:06:53 2008

    Europe/Amsterdam :
        TZ    : Europe/Amsterdam
        tzname: ('CET', 'CEST')
        Zone  : -3600 (-1)
        DST   : 1
        Time  : Sun Mar  9 18:06:53 2008


