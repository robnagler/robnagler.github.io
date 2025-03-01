---
layout: post
title: "Python Coroutines: Words of Advice"
date: 2023-12-25T12:00:00Z
---

### make sure you wrap the coroutine to print a stack trace when
    an exception occurs in production
### python coroutine env var


**TODO** https://github.com/tornadoweb/tornado/issues/2532
on message is synchronous

- every async is a coroutine so you have to know
  that not only on entry is global state modified, but
  also when it returns. You have to write everything with
  locks so it becomes very complex code without any of the
  parallelism. Locks are costly.
- how to write a succesful coroutine:
  - check global state and do non-awaited ops first
  - on entry, verify global state
  - after an await, check any global state

- thread executors for expensive operations (aiohttp)
- running multiple event loops didn't seem like a good idea

- "with" is a coroutine so be aware of state changes

- narrow scope of exceptions (supervisor commit for key error)



# Example from email 12/11/2024 about sbatch_id
https://github.com/radiasoft/sirepo/issues/7385


I am starting to really hate asyncio. Here's a simple example:

        # Reply case yields, but does not modify global state
        if r := await _valid_or_reply(req.content.data.get("forceRun")):
            return r
        _update_db()

In normal threaded code, you don't have to write anything, because you don't prefix preemptable calls with "await". The same is true with callbacks. The "await" is actually a false sign. You need it, because inside the code it *may* call await. However, the whole method isn't async. This is a huge distinction between Java's "sync" prefix, which does perform a mutex on the entire call. I think this is a very subtle distinction which creates really hard to read code.

The routine does this:

        async def _valid_or_reply(force_run):
            if self._is_running_pending():
                if force_run or not self._req_is_valid(req):
                    return PKDict(
                        state=job.ERROR,
                        error="another browser is running the simulation",
                    )
                # Not _receive_api_runStatus, because runStatus should have been
                # called before this function is called.
                return self._status_reply(req)
            if (
                not force_run
                and self._req_is_valid(req)
                and self.db.status == job.COMPLETED
            ):
                # TODO(robnagler) simplify after https://github.com/radiasoft/sirepo/issues/7386

                # Valid, completed, sequential simulation
                # Read this first https://github.com/radiasoft/sirepo/issues/2007
                r = await self._receive_api_runStatus(req)
                if r.state == job.MISSING:
                    # happens when the run dir is deleted (ex purge_non_premium)
                    if recursing:
                        raise AssertionError(f"already called from self req={req}")
                    # Rerun the simulation, since there's no "button" in the UI for
                    # this case.
                    return await self._receive_api_runSimulation(req, recursing=True)
                return r
            return None

It is validating the args/state and takes actions based on the invalid paths. Those actions are tightly coupled with the invalidation. _status_reply is not async, because it just returns local state. The runStatus is async because it has to hit the agent to get the sequential result. The runSimulation is a bit goofy, but it is necessary. It doesn't matter, because those cases are explicitly coupled in the correct place in the code. I could return a status result from _validate and then call _reply with that result. It would decouple the logic and all the comments that are very difficult to explain, but are correct in the context of the validation.

So the "await" doesn't actually await. It is *really* confusing to read the await conditional in the main body, because _valid_or_reply() is not asynchronous in both cases. In the threaded case, you'd put a lock around the update_db, or better, you'd simply send a message to another thread to update the db. That's how you'd handle it in Go, I believe -- certainly in V, where there were no locks, only messages. The server would validate your request and reply failure if you were trying to update state based on invalid inputs.

I think this is a major thing for me why asyncio code is so hard to read and write. You need a completely different approach, and I'm not sure what that is. For most of this stuff, callbacks would be better, because you logically release when the function returns.

I think I need to see some real problems solved, like the supervisor/agent, with asyncio. I have only seen trivial problems or over-engineered solutions.

TODO: https://stackoverflow.com/questions/59586879/does-await-in-python-yield-to-the-event-loop
good reference on how await works

Working #6916 after a bit of a break. I realized that the `_run` task
is unnecessary, and overcomplicates the
process. [`_run`](https://github.com/radiasoft/sirepo/blob/60310d60eb862116bf4a80fada4bab19b437a06a/sirepo/job_supervisor.py#L951)
sends the op, and then loops on
[`reply_get`](https://github.com/radiasoft/sirepo/blob/60310d60eb862116bf4a80fada4bab19b437a06a/sirepo/job_supervisor.py#L1210). This
is how you would write a normal threaded application: receive a
message and then pass it off to a worker thread. However, that's not
how you should write an asyncio application: callbacks should handle
the operation immediately, because all other tasks block anyway. There
is not priority scheduling or multi-processing going on. This is very
hard to get your head around.


### TL;DR

TL;DR [Cooperative multitasking](https://en.wikipedia.org/wiki/Cooperative_multitasking)
(coroutines)
has not been easier than
[preemptive multitasking](https://en.wikipedia.org/wiki/Preemption_(computing)#Preemptive_multitasking)
(threads) in our experience.

TODO: give the hints at the top

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
is why they are tricksy, and whey we can easily confuse concurrency with
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
does not happen *simultaneously* as with (preemptable) threads.

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
prodution, in real-time. They are difficult to reproduce.

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

### Too Many Primitives

Furthermore, the list of synchronization primitives is confusing due
to their variety. And, throwing
[Tornado's coroutine primitives](https://www.tornadoweb.org/en/stable/coroutine.html),
into the mix, and you might think all these different primitives are
necessary.

In my experience, fewer coroutines primitives are better. This is also
Rob Pike's experience, and why
[Go channels](https://go.dev/doc/effective_go#channels) are the
primary way to communicate between goroutines. There is no way for one
goroutine to cancel another goroutine. Also, Go eschews exceptions in
favor of explicit returns, because exceptions are confusing with
concurrent execution.

As noted earlier, we are trying to limit all communication to
`asyncio.Queue`.

### The Cathedral and the Bazaar

The theory behind coroutines is that they are easier to reason about
than threads, since the programmer has "complete control". This
reminds me of the
[cathedral builder](http://www.catb.org/~esr/writings/cathedral-bazaar/cathedral-bazaar/index.html#catbmain)
approach to developing software. Threads are like the bazaar, because
the programmer has little control over scheduling. Bazaars are
non-deterministic, just like threads. The motto for threads is "be
prepared". With coroutines, a more relaxed approach can be taken. For
simple programs, this is fine. For complex programs, you need to be
prepared.

CONSIDER ending with this thought?. https://www.bitecode.dev/p/asyncio-twisted-tornado-gevent-walk

### END

- asyncio is misnamed, you can't do i/o
- every async is a coroutine so you have to know
  that not only on entry is global state modified, but
  also when it returns. You have to write everything with
  locks so it becomes very complex code without any of the
  parallelism. Locks are costly.
- how to write a succesful coroutine:
  - check global state and do non-awaited ops first
  - on entry, verify global state
  - after an await, check any global state

- thread executors for expensive operations (aiohttp)
- running multiple event loops didn't seem like a good idea

- "with" is a coroutine so be aware of state changes


computer.
in operating systems are two
things: memory and

There are many differences between coroutines and threads. There are
also many similarities.

Threads are preemptable

section on coroutines & concurrency threadexecutor

The Job Supervisor

At that point, I had not much experience with Go, which
solves the cancellation and timeout problem differently.

History:
- build job supervisor without db, as single thread, coroutines.
- redis added complexity, and we didn't need performance
- simple mechanism to manage resources and locking around them

Advice:
- Catch task exceptions always and log
- Collect locks in a single object and log "situation"
- Log, log, log
- No cancel task
- use go-routine style errors, avoiding exceptions so no jumps in
  control flow, catch exceptions and pass results.
- yield to event loop or async for is important
- tornado specific: async messages on websockets and I/O
- avoid any real work, farm that off to other processes
- good for "pub-sub" style service
- global locking a problem when multiple processes (use an acid db, we
  use file lock)
- async with isn't all that useful for our problem (long lived locks).
  transfer state to object, not lock, and then lock the object only
  when accessing (just like threads) so can avoid locking.
  check state before entering and then inside lock
- for short lived resources may be better to hold lock, but typically
  async only needed for complexity. avoid coros if possible

Structure:

- debugging just as many bugs
- Backfitting (aiohttp, aiofiles not out of the box)
- Two task switching methods: os kernel and event loop; more complicated
  than threads (vs processes) that use the same task switch method.
  python gilock adds another complexity to threads and coroutines.
  but with threads, at least, it's clear.
- If you want it to be fire-and-forget without blocking anything, you
  can just handle this today by spawning an async callback from your
  synchronous on_finish. [link](https://github.com/tornadoweb/tornado/issues/3038#issuecomment-885001031)
- the process world was designed already, coroutines are an add on.
  sending files is synchronous in tornado, because there's no
  asynchrony with coroutines. it blocks the process from running any
  other coroutines. same with databases unless adapted. threads do not
  have this problem. relates to the backfitting problem with aiohttp
- locking is more complex due to the need for concurrency in realworld
  apps.(https://www.tornadoweb.org/en/stable/guide/running.html#processes-and-ports)
  this means you need another sync method between these processes that
  is orthoginal to coroutine locking.
  nginx load balancer introduces another schduler that has no insight
  into the busyness of the process. with threads, the busyness is
  visible to the scheduler. coroutines, nobody knows. could be
  yielding to event loop
- tornado websocket handling: [ping timeouts](https://github.com/tornadoweb/tornado/issues/2941)
  without true concurrency, problems like this are insidious.
  accurate timing requires preemption
- need to yield to event loop - more complex programming when
  "work" needs to be done.
- time.sleep does the wrong thing. need to retrain all primitives
- catherdral and the bazzar: one is a carefully crafted process
  with contorlled switching, the other is natural, evolutionary.
  evolution is more robust than ivory tower in real world apps

### NOTES

[`asyncio`](https://docs.python.org/3/library/asyncio.html)
https://www.tornadoweb.org/en/stable/guide/coroutines.html

  - https://bhch.github.io/posts/2017/12/serving-large-files-with-tornado-safely-without-blocking/
  sending large files in tornado
  does not discuss upload problem

  - https://github.com/tornadoweb/tornado/issues/2532
  on message is synchronous

  - https://dev.to/martinhaeusler/why-i-stopped-using-coroutines-in-kotlin-kg0
    this is a long post with a lot of complexity, but basically:
    - debugging is hard (specific to kotlin?)
    - request context can't be global (this is a good thing)
    - synchronized keyword isn't the same
    - Throughput vs. Horizontal Scaling: "A big advantage of
      coroutines for the server-side is that a single thread can
      handle a lot more requests; while one request waits for a
      database response, the same thread can happily serve another
      request. In particular for I/O bound tasks, this can increase
      the throughput."
  - https://forum.unity.com/threads/why-do-people-hate-coroutines.260160/page-3#post-1722915
    Coroutines are all the bad things about working with threads, with
        none of the good points.

    It's just a way to add danger and uncertainty into your coding life
    when you didn't have any before, all without improving flow, execution
    speed, or concurrency.

    Yes I'm being flippant, but the point is simply that it's easy to do
    really nasty things to the stack (and heap) with a coroutine unless
    you know what you're doing.

    So

    Pros :
    - Allows you to pause execution of a function at any point and
      relinquish control to the caller.
    - Reduces visual branching in the code leaving it relatively compact
    - Unlike threads read/write is in series rather than concurrent
      parallel reads (safer)
    - Is easy and simple to understand and implement in C#
    - Allows you to easily place invocation/continuation on a timer or
      event e.g. continue executing this in 2 seconds (if nothing else is
      executing at this time)...
    - ...this also requires less overhead than most alternatives like
      checking on update against the difference in time before executing
      code.

    Cons :
    - Can cause stack memory issues if a coroutine is killed externally or
      never fully executed/closed
    - Makes program flow less obvious to read
    -Makes debugging more complex
    - Adds branching (which is slow, stack allocation and duplication etc
      if done too frequently)
    - While individual access is safe, code itself can still be vulnerable
      to state changes in the heap in the meantime, same as threads.
    - Doesn't operate concurrently, so event recall/timer usage is still
      dependent on light main thread execution.
    - Requires strict adherence to the design model once implemented.
    - New developers must be aware of what's required of their code to
      work in this environment, increasing the complexity and potential
      for error substantially on larger projects.

    To be fair to them, they're not an inherently awful thing, it's a
    single thread scheduler. The problems arise from poor memory
    management and when people make assumptions about the capabilities of
    the scheduler and the execution order that can arise from their
    use. i.e. it's really just PEBKAC. If it's easy to F*** up then people
    will (especially as you add more of them to a project), so why take
    the risk? Make your life easier, make your debugging life easier.

  - Randomness intereseting. like ML, stochastic processes are more
    robust. preemption is stochastic. ivory tower control (coroutines)
    doesn't win out. Bazarr and the cathedral.
  - Explicit await requires backfitting which does not scale.
    either everything preempts or nothing. you have to insert
    async await everywhere.
  - Two preemption methods like callbacks so very difficult to
    understand flow
  - kernel is the ultimate arbiter of processes, coroutines are
    are two schedulers so you have to navigate between them. python
    gil lock adds another scheduler/lock
  - mod_perl knows when the request is finished so a true process
    manager. tornado doesn't have that. you can't tell the proxy
    termination in nginx that a tornado process is busy with a request
  - coroutines have all the problems of asynchrony without the
    benefits of preemption. you still have async bugs that are hard to find
  - coroutine have implicit locks fool you so await needs as care or
    more care than anything else. every await can cause deadlock. with
    threads, ever line can cause deadlock so you have to think about
    it more clearly. the thread scheduler helps with this in that
    you switch out randomly.
  - the process world was designed already, coroutines are an add on.
    sending files is synchronous in tornado, because there's no
    asynchrony with coroutines. it blocks the process from running any
    other coroutines. same with databases. threads do not have this
    problem.
  - threads only have one problem: thread lock on shared memory and
    global lock (with db) on global resources. coroutines do not have
    good global locking. our file lock is a global lock that blocks
    all coroutines. this means it is hard to get a resource overview.
