####################################################
Communication between processes with multiprocessing
####################################################

.. _multiprocessing-queues:

Passing Messages to Processes
=============================

As with threads, a common use pattern for multiple processes is to divide a job up among several workers to run in parallel.  A simple way to do that with :mod:`multiprocessing` is to use Queues to pass messages back and forth.  Any pickle-able object can pass through a :mod:`multiprocessing` Queue.

.. include:: multiprocessing_queue.py
    :literal:
    :start-after: #end_pymotw_header

This short example only passes a single message to a single worker, then the main process waits for the worker to finish.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'multiprocessing_queue.py'))
.. }}}

::

	$ python multiprocessing_queue.py
	Doing something fancy in Process-1 for Fancy Dan!

.. {{{end}}}

A more complex example shows how to manage several workers consuming data from the queue and passing results back to the parent process.  The *poison pill* technique is used to stop the workers.  After setting up the real tasks, the main program adds one "stop" value per worker to the job queue.  When a worker encounters the special value, it breaks out of its processing loop.

.. include:: multiprocessing_producer_consumer.py
    :literal:
    :start-after: #end_pymotw_header

Although the jobs enter the queue in order, since their execution is parallelized there is no guarantee about the order they will be completed.  

.. {{{cog
.. cog.out(run_script(cog.inFile, 'multiprocessing_producer_consumer.py'))
.. }}}

::

	$ python multiprocessing_producer_consumer.py
	Creating 4 consumers
	Consumer-4: 2 * 2
	Consumer-4: 6 * 6
	Consumer-4: Exiting
	Consumer-1: 0 * 0
	Consumer-1: 7 * 7
	Consumer-1: Exiting
	Consumer-3: 3 * 3
	Consumer-3: 5 * 5
	Consumer-3: 9 * 9
	Consumer-3: Exiting
	Consumer-2: 1 * 1
	Consumer-2: 4 * 4
	Consumer-2: 8 * 8
	Consumer-2: Exiting
	Result: 1 * 1 = 1
	Result: 3 * 3 = 9
	Result: 2 * 2 = 4
	Result: 0 * 0 = 0
	Result: 4 * 4 = 16
	Result: 5 * 5 = 25
	Result: 6 * 6 = 36
	Result: 7 * 7 = 49
	Result: 8 * 8 = 64
	Result: 9 * 9 = 81

.. {{{end}}}



Signaling between Processes with Event objects
==============================================

Events provide a simple way to communicate state information between processes.  An event can be toggled between set and unset states.  Users of the event object can wait for it to change from unset to set, using an optional timeout value.

.. include:: multiprocessing_event.py
    :literal:
    :start-after: #end_pymotw_header

When ``wait()`` times out it returns without an error.  The caller is responsible for checking the state of the event using ``is_set()``.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'multiprocessing_event.py'))
.. }}}

::

	$ python multiprocessing_event.py
	wait_for_event_timeout: starting
	wait_for_event_timeout: e.is_set()-> False
	wait_for_event: starting
	wait_for_event: e.is_set()-> True
	main: waiting before calling Event.set()
	main: event is set

.. {{{end}}}

Controlling access to resources with Lock
=========================================

In situations when a single resource needs to be shared between multiple processes, a Lock can be used to avoid conflicting accesses.  

.. include:: multiprocessing_lock.py
    :literal:
    :start-after: #end_pymotw_header

In this example, the messages printed to stdout may be jumbled together if the two processes do not synchronize their access of the output stream with the lock.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'multiprocessing_lock.py'))
.. }}}

::

	$ python multiprocessing_lock.py
	Lock acquired via with
	Lock acquired directly

.. {{{end}}}


Synchronizing threads with a Condition object
=============================================

Condition objects let you synchronize parts of a workflow so that some run in parallel but others run sequentially, even if they are in separate processes.  

.. include:: multiprocessing_condition.py
    :literal:
    :start-after: #end_pymotw_header

In this example, two process run stage two of a job in parallel once the first stage is done.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'multiprocessing_condition.py'))
.. }}}

::

	$ python multiprocessing_condition.py
	Starting s1
	s1 done and ready for stage 2
	Starting stage_2[1]
	stage_2[1] running
	Starting stage_2[2]
	stage_2[2] running

.. {{{end}}}


Controlling concurrent access to resources with a Semaphore
===========================================================

Sometimes it is useful to allow more than one worker access to a resource at a time,
while still limiting the overall number. For example, a connection pool might
support a fixed number of simultaneous connections, or a network application
might support a fixed number of concurrent downloads. A Semaphore is one way
to manage those connections.

.. include:: multiprocessing_semaphore.py
    :literal:
    :start-after: #end_pymotw_header

In this example, the ActivePool class simply serves as a convenient way to
track which process are running at a given moment. A real resource pool
would probably allocate a connection or some other value to the newly active
process, and reclaim the value when the task is done. Here, it is just used to
hold the names of the active processes to show that only 3 are running
concurrently.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'multiprocessing_semaphore.py'))
.. }}}

::

	$ python multiprocessing_semaphore.py
	Now running: ['0', '1', '2']
	Now running: ['0']
	Now running: ['2', '3', '4']
	Now running: ['2', '3', '5']
	Now running: ['0', '2', '3']
	Now running: ['2', '3', '6']
	Now running: ['0', '1', '2']
	Now running: ['2', '7', '8']
	Now running: ['2', '6', '7']
	Now running: ['7', '8', '9']
	Now running: ['2', '3', '4']
	Now running: ['2', '3', '4']
	Now running: ['7', '8', '9']
	Now running: ['7', '8', '9']
	Now running: ['7', '8', '9']
	Now running: ['7', '8', '9']
	Now running: ['7', '8', '9']
	Now running: ['9']
	Now running: ['9']
	Now running: []

.. {{{end}}}

Managers
========

In the previous example, the list of active processes is maintained centrally in the ActivePool instance via a special type of list object created by a Manager.  The Manager is responsible for coordinating shared information state between all of its users.  By creating the list through the manager, the list is updated in all processes when anyone modifies it.  In addition to lists, dictionaries are also supported.

.. include:: multiprocessing_manager_dict.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'multiprocessing_manager_dict.py'))
.. }}}

::

	$ python multiprocessing_manager_dict.py
	Results: {0: 0, 1: 2, 2: 4, 3: 6, 4: 8, 5: 10, 6: 12, 7: 14, 8: 16, 9: 18}

.. {{{end}}}

Namespaces
==========

In addition to dictionaries and lists, a Manager can create a shared Namespace.  Any named value added to the Namespace is visible across all of the clients.

.. include:: multiprocessing_namespaces.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'multiprocessing_namespaces.py'))
.. }}}

::

	$ python multiprocessing_namespaces.py
	Before event, consumer got: 'Namespace' object has no attribute 'value'
	After event, consumer got: This is the value

.. {{{end}}}

It is important to know that *updates* to mutable values in the namespace are *not* propagated.

.. include:: multiprocessing_namespaces_mutable.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'multiprocessing_namespaces_mutable.py'))
.. }}}

::

	$ python multiprocessing_namespaces_mutable.py
	Before event, consumer got: []
	After event, consumer got: []

.. {{{end}}}


Pool.map
========

For simple cases where the work to be done can be broken up and distributed between workers, you do not have to manage the queue and worker processes yourself.  The Pool class maintains a fixed number of workers and passes them jobs.  The return values are collected and returned as a list.  The result is functionally equivalent to the built-in ``map()``, except that individual tasks run in parallel.

.. include:: multiprocessing_pool.py
    :literal:
    :start-after: #end_pymotw_header

.. {{{cog
.. cog.out(run_script(cog.inFile, 'multiprocessing_pool.py'))
.. }}}

::

	$ python multiprocessing_pool.py
	Input   : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
	Built-in: [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
	Pool    : [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

.. {{{end}}}
