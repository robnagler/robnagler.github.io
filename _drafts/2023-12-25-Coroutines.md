---
layout: post
title: "Coroutines"
date: 2023-12-25T12:00:00Z
---


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
