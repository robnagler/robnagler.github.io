---
layout: post
title: "Python Coroutines: Words of Advice"
date: 2023-12-25T12:00:00Z
---

### The Initial Project

Around 2018 [Sirepo](https://sirepo.com) had outgrown
[Celery](https://docs.celeryq.dev) as a job management system. We
decided to implement a tailored solution to our problem, which
involves jobs running from a few seconds seconds to a few days. We also
had a requirement to integrate with job managers on 3rd party
supercomputers with independent authentication.

Python supports many mechanisms for managing asynchrony: coroutines,
threads, and multiprocessing. Our
[experience with threads](https://github.com/radiasoft/sirepo/issues?q=is%3Aissue+flask+NOT+release)
was not great with [Flask](https://flask.palletsprojects.com). We
reasoned that multi-threading is hard to implement correctly. With
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
realized we would need some process managing the queueing so that jobs
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
we hired Nathaniel helped us get started on the project. This was a
good call. I am very grateful for Nathaniel for helping me (in
particular) understand the ins and outs of
[Python's asyncio](https://docs.python.org/3/library/asyncio.html).

Fast forward six years, the
[Sirepo job system](https://github.com/radiasoft/sirepo/wiki/Job-system-architecture-overview)
has been in production for several years. Suffice it to say, we
have learned a thing or two about job management, coroutines,
cancellations, timeouts, locking, etc. This article collects our
experience.

### xx

Sirepo Jobs run on our cluster and on [NERSC](https://nersc.gov). CPU
utilization is monitored and controlled (in containers), and we have
paying customers with few complaints about the job system. The
"one-click" 3rd party supercomputer integration is a godsend to many
of our users. It is very nice to have happy customers.

And, we have had
[many issues](https://github.com/radiasoft/sirepo/issues?q=is%3Aissue+label%3Asupervisor)
with the job manager. Many are the natural outcome of emergent design,
and others are intrinsic to coroutines in combination with Python's
[easier to ask forgiveness than permission](https://docs.python.org/3/glossary.html#term-EAFP)
approach to cancellation, timeouts, errors, and other exceptional
conditions.
[Cooperative multitasking](https://en.wikipedia.org/wiki/Cooperative_multitasking)
(coroutines)
has not been easier than
[preemptive multitasking](https://en.wikipedia.org/wiki/Preemption_(computing)#Preemptive_multitasking)
(threads) in our experience.

Despite that, we have expanded our use of coroutines to other
projects.  [Tornado](https://www.tornadoweb.org) serves as the central
dispatcher. We finally
[replaced Flask with Tornado](https://github.com/radiasoft/sirepo/commit/6bfd0696fb09ef33b9af938f987c5c38a1c4e9c5)
for the API server so all services are based on Tornado. Coroutines
work well. We have not encountered many bugs with Tornado or
asyncio. We think at this point we also know a bit better how to write
reliable services based on coroutines.

### Preemptable vs Cooperative Multitasking

In order to understand many of the issues with coroutines, we need to
compare them to threads, briefly.

For most programmers,
[Concurrent programming](https://en.wikipedia.org/wiki/Concurrent_computing)
implies preemptive multitasking. In modern programming, we confuse
concurrency with parallelism. Rob Pike's talk
[Concurrency is not parallelism](https://go.dev/blog/waza-talk)
is worth a watch.

Concurrency in Python is confusing. Consider Python's
[Concurrent Execution documentation](https://docs.python.org/3/library/concurrency.html),
which fails to discuss
[generators](https://wiki.python.org/moin/Generators) or
callbacks, which are both forms of concurrent execution.
Even MIT's course 6.005 Software Construction states:
"[*Concurrency* means multiple computations are happening at the same time](https://web.mit.edu/6.005/www/fa14/classes/17-concurrency/)."

This is more than semantics. People confuse cooperative and preemptive
multitasking. Consider
[this stackoverflow post](https://stackoverflow.com/a/37345564):

> According to python docs for
> [asyncio.Task](https://docs.python.org/3/library/asyncio-task.html#asyncio.Task)
> it is possible to start some coroutine to
> **execute "in the background"**. The task created by
> [asyncio.ensure_future](https://docs.python.org/3/library/asyncio-future.html#asyncio.ensure_future)
> won't block the execution (therefore the function will return immediately!). This
> looks like a way to "fire and forget" as you requested.

The emphasis in the original creates the confusion. The quotes are
"correct" and also imply something that's not true: Coroutines and futures do not
[execute in the background](https://en.wikipedia.org/wiki/Background_process).
They simply hand off control -- just like passing a callback does --
to another part of the same thread.

When you write some asyncio code that reads from a file in an
asyncio-based web server such as Tornado, no other coroutine can
preempt the read loop unless there is a call to `await`. This may seem
obvious in one sense, but the language of preemption is implied in the
[asyncio documentation](https://docs.python.org/3/library/asyncio-sync.html):

> asyncio synchronization primitives are designed to be similar to those
> of the threading module with two important caveats:
>
> - asyncio primitives are not thread-safe, therefore they should not be
>   used for OS thread synchronization (use threading for that);
> - methods of these synchronization primitives do not accept the timeout
>   argument; use the asyncio.wait_for() function to perform operations
>   with timeouts.
>
> asyncio has the following basic synchronization primitives:
>
> - Lock
> - Event
> - Condition
> - Semaphore
> - BoundedSemaphore
> - Barrier

All of this smells like parallism, and therein lies the problem

### Too Many Primitives

The list of synchronization primitives is confusing due to their
variety. Add to that
[Tornado's coroutine primitives](https://www.tornadoweb.org/en/stable/coroutine.html),
and you might thing all these different primitives are necessary.
Also, [the stack overflow post (above)](https://stackoverflow.com/a/37345564),
gives the advice "**Kill tasks instead of awaiting them**", which is
yet another coroutine primitive, not listed above.

In my experience, fewer coroutines primitives are better. This is also
Rob Pike's experience, and why
[Go channels](https://go.dev/doc/effective_go#channels) are the
primary way to communicate between goroutines. There is no way for one
goroutine to cancel another goroutine. Also, Go eschews exceptions in
farvor of explicit returns, because exceptions are confusing to
manage in concurrent execution.

When we started writing the supervisor, there were many locks and
queues. We relied on cancel. However, we found ther


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

### Logging

Debugging asynchronous code is hard, and in a distributed system, it's
even harder. We have had numerous failures, most of which are easily
explainable in hindsight. Debugging consists of staring at logs for
hours on end, because the difficult to find defects only occur in
prodution, in real-time. They are difficult to reproduce.

[Over](https://github.com/radiasoft/sirepo/issues/6779)
[the](https://github.com/radiasoft/sirepo/issues/6572)
[years](https://github.com/radiasoft/sirepo/issues/6250),
[we](https://github.com/radiasoft/sirepo/issues/3658)
[have](https://github.com/radiasoft/sirepo/issues/2169)
[had](https://github.com/radiasoft/sirepo/issues/2135)
[to](https://github.com/radiasoft/sirepo/issues/2055)
improve logging in the job system. I think we have come up with some
guidelines:

- Always catch and log exceptions in coroutines with sufficient
  context. Sufficient will become apparent over time.
- Use something like
  [pkdebug_str](https://github.com/radiasoft/pykern/blob/f5da92a963ef5e58f896eff236bcaf5762bef806/pykern/pkdebug.py#L125)
  to create consistent context for logs.
- Include detailed logs with timestamps in issues. In public repos, like Sirepo, use a
  [log trimmer](https://github.com/biviosoftware/home-env/blob/55605e8dad11f5a949a9724bb79059e8498cfda8/bin/journal_trim)
  to ensure issues avoid exposing [personally identifiable
  information (PII)](https://www.gsa.gov/reference/gsa-privacy-program/rules-and-policies-protecting-pii-privacy-act).
- Documenting flow can be helpful. In the supervisor, we have a
  context manager called
  [set_job_situation](https://github.com/radiasoft/sirepo/blob/c12aedc0d2d6b60186015dc88091baafb2698503/sirepo/job_supervisor.py#L1154)
  to make it easy to document important state transitions.

**FIXME**: restore link and changed code
[Example](https://github.com/radiasoft/sirepo/blob/734b7195c3b0032ba32dd4451885f32da60e162f/sirepo/job_supervisor.py#L1200):
```py
@contextlib.asynccontextmanager
**FIXME** not async
async def set_job_situation(self, situation):
    await self._supervisor.set_situation(self, situation)
    try:
        yield
        await self._supervisor.set_situation(self, None)
    except Exception as e:
        pkdlog("{} situation={} stack={}", self, situation, pkdexc())
        await self._supervisor.set_situation(self, None, exception=e)
        raise
```

**FIXME** change to master commit
`self` is logged [with this context](https://github.com/radiasoft/sirepo/blob/734b7195c3b0032ba32dd4451885f32da60e162f/sirepo/job_supervisor.py#L1137):

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

In the previous code snippet, note the `is_destroyed` flag. In
shared-memory, asynchronous code, an object can be destroyed by one
coroutine while it still is being used by another. This is the
cause of numerous failures: using state when it is no longer
valid. For example, in the supervisor, a job might be canceled by the
user. The request that cancels the job is not the same running in the
same coroutine as the coroutine which is monitoring the job.

In Sirepo asynchronous code, object that cross coroutines are
destroyed explicitly. Coroutines check object's `is_destroyed` flag to
determine the object's validity after an `await`. This also means
coroutines need to cascade the state on completion.

This can get complicated especially on inter-coroutine communication,
e.g. queues. If an object gets destroyed, it's queues are no longer
valid so we have a proxy object for queues that handles the management
of the queue values when an object is
**FIXME** change to master commit
[destroyed during allocation](https://github.com/radiasoft/sirepo/blob/ff2def11788e757ec5c6a89057debe50d9069648/sirepo/job_supervisor.py#L112):

```py
class SlotProxy(PKDict):
    async def alloc(self, situation):
        if self._value is not None:
            return SlotAllocStatus.DID_NOT_AWAIT
        try:
            self._value = self._q.get_nowait()
            return SlotAllocStatus.DID_NOT_AWAIT
        except tornado.queues.QueueEmpty:
            pkdlog("{} situation={}", self._op, situation)
**FIXME** not async
            async with self._op.set_job_situation(situatioen):
                if not self._op.is_destroyed:
                    self._value = await self._q.get()
                    if not self._op.is_destroyed:
                        return SlotAllocStatus.HAD_TO_AWAIT
                self.free()
                return SlotAllocStatus.OP_IS_DESTROYED
```

A `SlotProxy` is used to access shared resources via a queue
(`self._q`). When `SlotProxy` owner (`self._op`) is destroyed, the
coroutine needs to check `is_destroyed` after every `await` and free
the slot. Otherwise, the `SlotProxy` value would get lost. Finally,
`alloc` returns a state that is used by higher levels of code.

### asyncio.CancelledError

Why not just use
[CancelledError](https://docs.python.org/3/library/asyncio-exceptions.html#asyncio.CancelledError)?
[The Python documentation states](https://docs.python.org/3/library/asyncio-task.html#task-cancellation),
"Tasks can easily and safely be cancelled.".
[We](https://github.com/radiasoft/sirepo/issues/2346)
[did](https://github.com/radiasoft/sirepo/issues/2570)
[not](https://github.com/radiasoft/sirepo/issues/3753)
[find](https://github.com/radiasoft/sirepo/issues/2712)
[this](https://github.com/radiasoft/sirepo/issues/2664)
[to](https://github.com/radiasoft/sirepo/issues/2375)
be the case.
It is very hard to write correct cancellation code. (Let
alone
[decide whether its canceled or cancelled](https://www.merriam-webster.com/grammar/canceled-or-cancelled). :-)
We found
[one defect](https://github.com/radiasoft/sirepo/issues/2375) related
to cancel in Tornado itself.

When we started the job system, `CancelledError` was a subclass of
`Exception`, and that changed in Python 3.8, to be a subclass of
`BaseException`. This
[required complicated code changes](https://github.com/radiasoft/sirepo/issues/2447).

, of the following in the
[Python 3 tutorial](https://docs.python.org/3/tutorial/errors.html#exceptions):

> Exceptions which are not subclasses of Exception are not typically
> handled, because they are used to indicate that the program should
> terminate. They include SystemExit which is raised by sys.exit() and
> KeyboardInterrupt which is raised when a user wishes to interrupt the program.






### END

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
