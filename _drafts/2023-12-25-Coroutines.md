---
layout: post
title: "Python Coroutines: Words of Advice"
date: 2023-12-25T12:00:00Z
---

### The Initial Project

Around 2018 [Sirepo](https://sirepo.com) had outgrown
[Celery](https://docs.celeryq.dev) as a job management system. We
decided to implement a tailored solution to our problem, which
involves jobs running for a few seconds seconds to a few days. We also
had a requirement to integrate with job managers on 3rd party
supercomputers with independent authentication.

Python supports many mechanisms for managing asynchrony: coroutines,
threads, and multiprocessing. Our
[experience with threads](https://github.com/radiasoft/sirepo/issues?q=is%3Aissue+flask+NOT+release)
was not great with [Flask](https://flask.palletsprojects.com). We
reasoned that multi-threading is hard to implement correctly. With
Python, the global interpreter lock always looms large in threading
discussions, anyway. We thought fully separate memory spaces
(processes) or cooperative multi-tasking (coroutines) would be more
reliable.

We had had good experience in
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
[Timeouts and cancellation for humans](https://vorpus.org/blog/timeouts-and-cancellation-for-humans/). It's
well-written and worth a read. Nathaniel and I struck up a
conversation about coroutines. This further convinced me that
coroutines were the way to go, especially because they were
cancellable. I did not have experience with modern day coroutines so
we hired Nathaniel helped us get started on the project. This was a
good call. I am very grateful for Nathaniel for helping me (in
particular) understand the insides and out of
[Python's asyncio](https://docs.python.org/3/library/asyncio.html).

Fast forward six years, the
[Sirepo job system](https://github.com/radiasoft/sirepo/wiki/Job-system-architecture-overview)
has been in production for several years. Suffice it to say, we
have learned a thing or two about job management, coroutines,
cancellations, timeouts, locking, etc. This article collects our
experience.

### xxx

Sirepo Jobs run on our cluster and on [NERSC](https://nersc.gov). CPU
utilization is monitored, and we have paying customers with few
complaints about the job system. The "one-click" 3rd party
supercomputer integration is a godsend to many of our users. It is
very nice to have happy customers.

And, we have had
[many issues](https://github.com/radiasoft/sirepo/issues?q=is%3Aissue+label%3Asupervisor)
with the job manager. Many are the natural outcome of emergent design,
and others are intrinsic to coroutines in combination with Python's
[easier to ask forgiveness than permission](https://docs.python.org/3/glossary.html#term-EAFP)
approach to cancellation, timeouts, errors, and other exceptional
conditions. Cooperative multitasking has not been easier than
multi-threading in our experience.

Despite that, we have expanded our use of coroutines to other
projects.  [Tornado](https://www.tornadoweb.org) serves as the central
dispatcher. We finally
[replaced Flask with Tornado](https://github.com/radiasoft/sirepo/commit/6bfd0696fb09ef33b9af938f987c5c38a1c4e9c5)
for the API server so all services are based on Tornado. Coroutines
work well. We have not encountered many bugs with Tornado or
asyncio. We think at this point we also know how to write reliable
services based on coroutines.


### Work Less I/O, etc.?

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
