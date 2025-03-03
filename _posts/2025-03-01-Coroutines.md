---
layout: post
title: "Python Coroutines: Words of Advice"
date: 2025-03-01T23:00:00Z
---

### The Initial Project

Around 2018 [Sirepo](https://sirepo.com) had outgrown
[Celery](https://docs.celeryq.dev) as a job management system. We
decided to implement a tailored solution to our problem, which
involves jobs running from a few seconds to a few days. We also
had a requirement to integrate with job managers on 3rd party
supercomputers with independent authentication.

To manage the events in a job manager, we would need to manage
asynchrony.
Python supports several mechanisms for asynchrony: coroutines,
threads, and multiprocessing. We had used
[Flask](https://flask.palletsprojects.com), which relies
on threads (and multiple processes) for asynchrony. Our
[experience with Flask](https://github.com/radiasoft/sirepo/issues?q=is%3Aissue+flask+NOT+release)
was not great.

We also reasoned that multi-threading is hard to implement
correctly.
With
Python, the
[global interpreter lock](https://en.wikipedia.org/wiki/Global_interpreter_lock)
always looms large in threading
discussions, anyway. We thought fully separate memory spaces
(processes) or cooperative multi-tasking (coroutines) would be more
reliable.

We had good experience in
[BOP](https://github.com/biviosoftware/perl-Bivio) relying on
[PostgreSQL](https://www.postgresql.org) for locking and inter-process
communication for jobs. However, Sirepo is different. It's all about
the jobs whereas BOP applications are mostly about the database.

We considered a publish-subscribe database like Redis to solve the
queuing/locking problem with multiple processes. Even with pub-sub, we
realized we would need a process manager so that jobs
could be started, awaited on, cancelled, and timed out. An important
part of this change was being able to
[charge](https://www.sirepo.com/plans) for different levels of CPU
resources.

Cancellation and timeouts led me to Nathaniel J Smith's
[Timeouts and cancellation for humans](https://vorpus.org/blog/timeouts-and-cancellation-for-humans/).
It's
well-written and worth a read. Nathaniel and I struck up a
conversation about coroutines. This further convinced me that
coroutines were the way to go, especially because they were
cancellable. I did not have experience with modern day coroutines so
we hired Nathaniel who helped us get started on the project. This was a
good call. I am very grateful for Nathaniel for helping me (in
particular) understand the ins and outs of
[Python's asyncio](https://docs.python.org/3/library/asyncio.html).

Fast forward six years, the
[Sirepo job system](https://github.com/radiasoft/sirepo/wiki/Job-system-architecture-overview)
has been in production for several years. Suffice it to say, we
have learned a thing or two about job management, coroutines,
cancellations, timeouts, locking, etc. This article collects our
experience.

### Job Supervisor and Coroutines

Sirepo jobs run on our cluster and at [NERSC](https://nersc.gov),
which uses [Slurm](https://slurm.schedmd.com) for job management. On
our cluster, we control CPU and memory utlization with containers.
We have paying customers with few complaints about the job system. The
"one-click" 3rd party supercomputer integration is a godsend to many
of our users. It is very nice to have happy customers.

And, we have had
[many issues](https://github.com/radiasoft/sirepo/issues?q=is%3Aissue+label%3Asupervisor)
with the job supervisor. Many are the natural outcome of emergent design,
and others are intrinsic to coroutines in combination with Python's
[easier to ask forgiveness than permission](https://docs.python.org/3/glossary.html#term-EAFP)
approach to cancellation, timeouts, errors, and other exceptional
conditions.

We have expanded our use of coroutines to other
projects.  All new projects, which require asynchrony, use [Tornado](https://www.tornadoweb.org). We
[replaced Flask with Tornado](https://github.com/radiasoft/sirepo/commit/6bfd0696fb09ef33b9af938f987c5c38a1c4e9c5)
for the API server so now all services rely on Tornado. Coroutines
work well. We have not encountered many bugs with Tornado or
asyncio. We think at this point we also know a bit better how to write
reliable services based on coroutines.

### Cooperative vs Preemptive Multitasking

In order to understand coroutines, we need to separate
[concurrency](https://en.wikipedia.org/wiki/Concurrency_(computer_science))
[from parallelism](https://en.wikipedia.org/wiki/Parallel_computing),
and
[cooperative multitasking](https://en.wikipedia.org/wiki/Cooperative_multitasking)
[preemptive multitasking](https://en.wikipedia.org/wiki/Preemption_(computing)#Preemptive_multitasking).

For most programmers, concurrency implies preemptive
multitasking. Threads and multiprocessing are the most common form of
concurrent programming we encounter.  Coroutines while being an old
invention in programming, only recently started to become
popular. They weren't added (formally) to Python
until 2015. Programming language courses do not emphasize them.  This
is why they are tricksy, and why we can easily confuse concurrency with
parallelism.

I think the confusion starts with the word concurrent, which
[Merriam-Webster](https://www.merriam-webster.com/dictionary/concurrent)
defines as "operating or occurring at the same time." Python
coroutines execute concurrently, but they do not execute "at the same
time".

A better definition is found on the
[Wikipedia Concurrency page](https://en.wikipedia.org/wiki/Concurrency_(computer_science)):

> In computer science, concurrency is the ability of different parts or
> units of a program, algorithm, or problem to be executed out-of-order
> or in partial order, without affecting the outcome. This allows for
> parallel execution of the concurrent units.

The word *allows* is key. Concurrency allows for out of order
execution. Coroutines can execute out of order, but their execution
does not happen *simultaneously* as with (preemptible) threads.

Parallelism is overlapping execution. Coroutines do not run in
parallel. They execute in a single Python thread.

Coroutine execution order is controlled by the
[asyncio event loop](https://docs.python.org/3/library/asyncio-eventloop.html)
Coroutines are cooperative, not preemptive multitasking.  That's their
main attraction: there can be no
[race conditions](https://en.wikipedia.org/wiki/Race_condition#In_software).

Rob Pike's talk
[Concurrency is not parallelism](https://go.dev/blog/waza-talk) is
worth a watch. The caveat here is that Goroutines are not coroutines,
because they are *allowed* to execute in parallel, which Python
coroutines cannot. Still, the talk explains concurrency and
parallelism clearly and with some good examples.

### Concurrency Requires Logging

Let's move on to something practical: Debugging concurrent code is
hard, precisely because execution is out of order.  Good logging is
essential in order to make it easy to debug, especially in production.

We have had numerous failures due to concurrency, most of which are
easily explainable in hindsight. Debugging consists of staring at logs
for hours on end, because the difficult to find defects only occur in
production, in real-time. They are difficult to reproduce.

[Over](https://github.com/radiasoft/sirepo/issues/6779)
[the](https://github.com/radiasoft/sirepo/issues/6572)
[years](https://github.com/radiasoft/sirepo/issues/6250),
[we](https://github.com/radiasoft/sirepo/issues/3658)
[have](https://github.com/radiasoft/sirepo/issues/2169)
[had](https://github.com/radiasoft/sirepo/issues/2135)
[to](https://github.com/radiasoft/sirepo/issues/2055)
improve logging in the job system. Here are some
guidelines we use:

- Always catch and log exceptions in coroutines with sufficient
  context. Sufficient will become apparent over time.
- Use something like
  [`__repr__`](https://docs.python.org/3/reference/datamodel.html#object.__repr__)
  or the more robust [pkdebug_str](https://github.com/radiasoft/pykern/blob/f5da92a963ef5e58f896eff236bcaf5762bef806/pykern/pkdebug.py#L125)
  to create consistent context for objects in log message.
- Include detailed logs with timestamps in issues (bug reports). In
  public repos, like Sirepo, use a
  [log trimmer](https://github.com/biviosoftware/home-env/blob/55605e8dad11f5a949a9724bb79059e8498cfda8/bin/journal_trim)
  to avoid exposing
  [personally identifiable information (PII)](https://www.gsa.gov/reference/gsa-privacy-program/rules-and-policies-protecting-pii-privacy-act).

Here's how `job_supervisor._Op` [logs its context](https://github.com/radiasoft/sirepo/blob/06ae456eca538aaa577e6cf9abe83e17518aefa1/sirepo/job_supervisor.py#L1306):

```py
def pkdebug_str(self):
    def _internal_error():
        if not self.get("internal_error"):
            return ""
        return ", internal_error={self.internal_error}"

    return pkdformat(
        "_Op({}{}, {:.4}{})",
        "DESTROYED, " if self.get("is_destroyed") else "",
        self.get("op_name"),
        self.get("op_id"),
        _internal_error(),
    )
```

### Track Object Life Cycle

Note the `is_destroyed` flag in the previous code snippet. In
shared-memory, asynchronous code, an object can be destroyed by one
coroutine while it still is being used by another. This is the
cause of numerous failures: using state when it is no longer
valid.

For example, in the supervisor, a job might be canceled asynchronously
by an API call triggered by a user pressing a cancel button. The
coroutine handling the request that cancels the job is not the
coroutine which is monitoring the job. The coroutine monitoring the
job holds a copy of the job object, which is destroyed by the
coroutine canceling the job.

That's why in Sirepo asynchronous code, objects that are referenced
concurrently by two coroutines are destroyed explicitly. Coroutines
are obligated to check object's `is_destroyed` flag to determine the
object's validity after an `await`. This means state management can
get complicated.


In `_send`,
[`is_destroyed` is checked](https://github.com/radiasoft/sirepo/blob/06ae456eca538aaa577e6cf9abe83e17518aefa1/sirepo/job_supervisor.py#L1103):

```py
async def _send(op):
    if not await op.prepare_send() or op.is_destroyed:
        return None, False
    if not op.send():
        return None, False
    if (r := await op.reply_get()) is None:
        return None, False

```

This check ensures that `op` has not been canceled. Once checked, we
know that `op` can't be destroyed until after the `await
op.reply_get`.

### asyncio.Task.cancel

That's a lot of code and logic just to send and get a reply. Why not
just
[Task.cancel](https://docs.python.org/3/library/asyncio-task.html#task-cancellation)
the `_send` coroutine?
After all, as the documentation says, "Tasks can easily and safely be cancelled."
[We](https://github.com/radiasoft/sirepo/issues/2346)
[did](https://github.com/radiasoft/sirepo/issues/2570)
[not](https://github.com/radiasoft/sirepo/issues/3753)
[find](https://github.com/radiasoft/sirepo/issues/2712)
[Task.cancel](https://github.com/radiasoft/sirepo/issues/2664)
[to](https://github.com/radiasoft/sirepo/issues/2375)
be easy to manage.  It
is very hard to write correct cancellation code.
We found [one defect](https://github.com/radiasoft/sirepo/issues/2375)
related to cancel in Tornado itself. Admittedly, Tornado was written
well before asyncio, and before tasks could be canceled.

Cancelling is hard. For example,
you can only cancel a
[concurrent.futures.Future](https://docs.python.org/3/library/concurrent.futures.html#future-objects)
when it is pending. Already executing futures cannot be canceled,
even when they are waiting on another coroutine.

Another example is
[threading.Timer.cancel](https://docs.python.org/3/library/threading.html#threading.Timer.cancel),
which "will only work if the timer is still in its waiting stage."

You cannot cancel a
[`threading.Thread`](https://docs.python.org/3/library/threading.html):
"threads cannot be destroyed, stopped, suspended, resumed, or interrupted."

And, you guessed it, you can't kill a Goroutine, a Rust thread, a Java
thread, etc. Indeed, Java had `Thread.stop`,
and it was removed for
[good reasons](https://docs.oracle.com/javase/1.5.0/docs/guide/misc/threadPrimitiveDeprecation.html).

That's why canceling a Python coroutine is problematic,
too. Cancelling coroutines is hard. In Python 3.11,
[Task.uncancel](https://docs.python.org/3/library/asyncio-task.html#asyncio.Task.uncancel)
and
[Task.cancelling](https://docs.python.org/3/library/asyncio-task.html#asyncio.Task.cancelling)
were added, which to me is yet another clue that it is hard to implement
cancelling. Piling on more methods, doesn't fix the fundamental issue.

### Use asyncio.Queue

We have settled on
[`asyncio.Queue`](https://docs.python.org/3/library/asyncio-queue.html)
as the sole means of communication and synchronization in
coroutines. The advantage of Queues over
[Locks](https://docs.python.org/3/library/asyncio-sync.html#asyncio.Lock)
and
[Events](https://docs.python.org/3/library/asyncio-sync.html#asyncio.Event)
is that a Queue allows you to pass values. As you saw in the example
above,
[`reply_get` returns None](https://github.com/radiasoft/sirepo/blob/06ae456eca538aaa577e6cf9abe83e17518aefa1/sirepo/job_supervisor.py#L1343)
when there is no reply, and that only happens when the send was
canceled. This is a clean way to communicate out-of-band state. With
Events and Locks, there's no value -- just one state change. This
means you have to have some other value to release a Lock or Event in
a way that clearly communicates this alternative state.

Python 3.13 added
[Queue.shutdown](https://docs.python.org/3/library/asyncio-queue.html#asyncio.Queue.shutdown),
which makes this communication even clearer. Here's the code in
[pykern.api.client](https://github.com/radiasoft/pykern/blob/79511e45c374c25d6971cef834a316769bd29427/pykern/api/client.py#L254),
to destroy and API call:

```py
if x := getattr(self._reply_q, "shutdown", None):
    x.shutdown(immediate=True)
else:
    # Inferior to shutdown, but necessary pre-Python 3.13
   self._reply_q.put_nowait(None)
```

And, the corresponding code in:
[result_get](https://github.com/radiasoft/pykern/blob/79511e45c374c25d6971cef834a316769bd29427/pykern/api/client.py#L267):

```py
try:
    rv = await self._reply_q.get()
except Exception as e:
    if (x := getattr(asyncio, "QueueShutDown", None)) and isinstance(e, x):
        raise util.APIDisconnected()
    raise
```

This code allows for clean communication that the
`APIDisconnected`, and the API call did not complete.

### Coroutines Block on I/O

Calls to `open`, `read`, etc. are blocking, that is, they block *all*
coroutines until the operating system fulfills the I/O
operation(s). You need parallelism in order to implement asynchronous
I/O in Python. (I have no idea why they call the coroutine module
`asyncio`, since it does not support I/O.)

A Tornado specific problem is that reply functions block and
[are not thread safe](https://www.tornadoweb.org/en/stable/web.html#thread-safety-notes).
This means a single response blocks the entire server.
Sirepo has an
[outstanding issue](https://github.com/radiasoft/sirepo/issues/5326)
with sending data without blocking. With websockets, we will
eventually chunk messages to avoid this issue.

We use [`aiohttp`](https://github.com/aio-libs/aiohttp) and
[`aiofiles`](https://github.com/Tinche/aiofiles) to avoid
blocking on other types of I/O. The implementation uses
[ThreadPoolExecutor](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor)
to parallelize the I/O operations.

To achieve true parallelism in production, we run
[Tornado in multiple processes](https://www.tornadoweb.org/en/stable/guide/running.html#processes-and-ports)
behind a proxy. This is true for any `asyncio`-based web server.

### Backfitting is Hard

When an existing function is converted into a coroutine, all callers
have to be modified. This makes updating exiting code very
difficult. This is by design. It also is annoying, let's face it.

One way to fix this problem is to create a new function that calls the
async function with
[asyncio.run](https://docs.python.org/3/library/asyncio-runner.html#asyncio.run),
which allows non-async functions to call coroutines. This allows you
to deprecate the usage and migrate your code slowly. Here's a simple
example
[from Sirepo](https://github.com/radiasoft/sirepo/blob/06ae456eca538aaa577e6cf9abe83e17518aefa1/sirepo/quest.py#L94):

```py
def call_api_sync(self, *args, **kwargs):
    import asyncio

    return asyncio.run(self.call_api(*args, **kwargs))
```

This allows non-async code to use `call_api`, which is async.

### Programmers Infer Parallelism

The way coroutines work is more than semantics. It directly affects
what is going on in programs that use them. I think programmers infer
parallelism from the asyncio objects, e.g. Lock and Semaphore. These
are words we learn in operating system courses. Coroutines execute
in a single thread.

When you write some asyncio code that reads from a file in an
asyncio-based web server such as Tornado, no other coroutine can
preempt the read loop unless there is a call to `await`.

This may seem
obvious in the context of this article, but the language of preemption
is implied in the
[asyncio documentation](https://docs.python.org/3/library/asyncio-sync.html):

> asyncio synchronization primitives are designed to be similar to those
> of the threading module with two important caveats:
>
> - asyncio primitives are not thread-safe, therefore they should not be
>   used for OS thread synchronization (use threading for that);
> - methods of these synchronization primitives do not accept the timeout
>   argument; use the asyncio.wait_for() function to perform operations
>   with timeouts.

To me, the most important caveat is that coroutines are not
parallel. The language implies an equivalence to threads, which are
totally unrelated. All asyncio operations are not thread safe except
[call_soon_threadsafe](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.loop.call_soon_threadsafe).

### Yield to the Event Loop

You have to pay attention when coding coroutines. Cooperative
multitasking requires yielding to the event loop whenever real work is
being done. By real work, this could be blocking I/O or
computation. Blocking I/O is solved by `aiofiles` (discussed
above).

If a coroutine has a loop, it needs yield to the event loop in its
loop unless the loop is "fast" or calls `await` in the loop. The
meaning of "fast" is obviously in the eye of the beholder.

In the `job_supervisor` we yield to the event loop [when garbage
collecting old jobs](https://github.com/radiasoft/sirepo/blob/06ae456eca538aaa577e6cf9abe83e17518aefa1/sirepo/job_supervisor.py#L595):

```py
for u, jids in (await _uids_to_jids(too_old, qcall)).items():
    with qcall.auth.logged_in_user_set(u):
        for j in jids:
            _purge_job(jid=j, too_old=too_old, qcall=qcall)
    await sirepo.util.yield_to_event_loop()
```

[`sirepo.util.yield_to_event_loop`](https://github.com/radiasoft/sirepo/blob/06ae456eca538aaa577e6cf9abe83e17518aefa1/sirepo/util.py#L511)
is wrapper, which allows us to document this magic:

```py
async def yield_to_event_loop():
    await asyncio.sleep(0)
```

[`asyncio.sleep(0)` has special semantics](https://docs.python.org/3/library/asyncio-task.html#asyncio.sleep):

> Setting the delay to 0 provides an optimized path to allow other
> tasks to run. This can be used by long-running functions to avoid
> blocking the event loop for the full duration of the function call.

(Nit: I hate tricks like this. They should just have provided
`asyncio.yield_to_event_loop`.)

### `await` does not Always Yield

The use of `await` does mean "yield to the event loop". In the
following code `await some_func()` executes completely synchronously:

```py
async def some_func():
    for i in range(1000):
        await sync_func()

async def sync_func():
    pass
```

This code would execute the same in the event loop if we removed
`async` and `await` keywords. This may seem obvious in this simple
example, it's not obvious in any non-trivial coroutine.

This is important, because unless you know exactly what the coroutine
being awaited on does, there's no guarantee that a loop which contains
an `await` actually releases the processor. This means you have to
break the abstraction of any coroutines you call, or you have to
always call `yield_to_event_loop`. This would be annoying, and it's a
real problem in asyncio-based code. This is a Python specific issue,
and is a design flaw in my opinion.

### Tornado.on_message

When we first wrote the supervisor, we assumed that
[`WebSocketHandler.on_message`](https://www.tornadoweb.org/en/stable/websocket.html#tornado.websocket.WebSocketHandler.on_message)
is a coroutine, because it can be defined that way. This is another
example of inferring something the behavior of coroutines, which I
believe would true for thread-based web server.
There's an
[open issue](https://github.com/tornadoweb/tornado/issues/2941) about
this in Tornado so we aren't the only ones who made this assumption.

The fix is to simply create a task in `on_message` as is
[done in `pykern.api.server`](https://github.com/radiasoft/pykern/blob/79511e45c374c25d6971cef834a316769bd29427/pykern/api/server.py#L239):

```py
async def on_message(self, msg):
    try:
        # WebSocketHandler only allows one on_message at a time
        pykern.pkasyncio.create_task(
            self.pykern_api_connection.handle_on_message(msg)
        )
    except Exception as e:
        pkdlog("exception={} stack={}", e, pkdexc())
```

I want to emphasize again the importance of logging at this level. If
there is an exception in `handle_on_message`, a stack trace will be
logged. The exception is not raised, because there's no value in
having Tornado process the exception. WebSocket messages are
simple. There are no replies so there's nothing for Tornado to do, and
it has no useful context for this problem (in our code).

### Debugging

In our experience, debugging coroutines is just as hard as threads,
and possibly harder. A coroutine is not visible to the operating
system. If a thread is an infinite loop, for example, you can easily
see that with a operating system thread monitoring tool like
[`top`](https://man7.org/linux/man-pages/man1/top.1.html). Coroutines
can't be monitored externally. All you see is the whole process is
busy computing.

Coroutines do not have race conditions, which eliminates one very
difficult class of defect. However, they can deadlock.  When two or
more coroutines are deadlocked, there's no insight with normal
operating system tools. There are tools to see threads which are
blocked, which greatly helps debugging.

The way we debug is to have very good logging. Every new hard to debug
defect usually results in improved log messages either to include more
context or messages in places that were missing.

Sirepo uses
[`pykern.pkdebug`](https://github.com/radiasoft/pykern/blob/79511e45c374c25d6971cef834a316769bd29427/pykern/pkdebug.py)
which allows (real-time) control of logging on a per line, function,
or module basis. A regular expression controls the output. If the
controlling regular expression is not set (normal case), the log
function does nothing, which is efficient. This type of logging can be
useful in particularly difficult defects, where you don't want to
flood the production logs when the system is running normally.

`asyncio` has a static environment variable
[`PYTHONASYNCIODEBUG`](https://docs.python.org/3/library/asyncio-dev.html),
which logs interesting information about coroutines, e.g. long running
coroutines, not awaited coroutines (common problem), and exceptions
raised when calling asyncio APIs from the wrong thread.

### Summary

`asyncio` is part of Python now, and more and more code will use
it. Hopefully this article helps you write more effective
coroutines. It's not as easy as it looks, but as you develop your own
coroutine coding patterns, it becomes manageable.

Other people have written extensively about coroutines. Here are some
useful references in alphabetical order:

- [Asyncio, twisted, tornado, gevent walk into a bar...](https://www.bitecode.dev/p/asyncio-twisted-tornado-gevent-walk)
- [Serving large files with Tornado safely without blocking](https://bhch.github.io/posts/2017/12/serving-large-files-with-tornado-safely-without-blocking/)
- [Stack Overflow: Does `await` in Python yield to the event loop?](https://stackoverflow.com/a/59780868)
- [Unity Forum: Why do people hate Coroutines?](https://forum.unity.com/threads/why-do-people-hate-coroutines.260160/page-3#post-1722915)
- [Why I stopped using Coroutines in Kotlin](https://dev.to/martinhaeusler/why-i-stopped-using-coroutines-in-kotlin-kg0)
