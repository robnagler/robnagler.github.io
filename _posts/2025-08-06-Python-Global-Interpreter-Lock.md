---
layout: post
title: "Python Global Interpreter Lock"
date: 2025-08-06T20:00:00Z
---

### GIL Confusion

The Python Global Interpreter Lock (GIL) is the source of much
confusion. You will see
[code like this](https://github.com/pyepics/pyepics/blob/4a4caebd92b75ee21c774cfc33c05ae77f4d1f97/epics/ca.py#L260):

```py
# The following sleep is here only to allow other threads the
# opportunity to grab the Python GIL. (see pyepics/pyepics#171)
time.sleep(0)
```

Calling `time.sleep` releases the CPU the thread is running on at the
kernel level, but it does not release the GIL, per se.

That `time.sleep(0)` hands control back to the OS scheduler, but the
GIL remains held by the interpreter. The confusion stems from
[mixing up parallelism and concurrency](https://www.robnagler.com/2025/03/01/Coroutines.html#cooperative-vs-preemptive-multitasking):
the GIL prevents true parallel execution of Python bytecode, yet
allows threads to interleave execution cooperatively. A simple example
illustrates this.

### CPU Intense Example

```py
import threading, time

def _cpu_intense_function():
    def _is_prime(n):
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
            return True

    for n in range(3, 10000):
        _is_prime(n)

def _thread(inc):
    global shared_value

    for _ in range(500):
        _cpu_intense_function()
        shared_value += inc

shared_value = 0
ones = threading.Thread(target=_thread, args=(1,))
ones.start()
millions = threading.Thread(target=_thread, args=(1000000,))
millions.start()
while shared_value < 500000000:
    time.sleep(1)
    print(shared_value)
```

The following output demonstrates that the `shared_value` increases by
`ones` and `millions` simultaneously:

```sh
$ python cpu_intense.py
117000121
237000241
355000358
475000475
500000500
```

The GIL allows the two threads to interleave so `shared_value` changes
(almost) simultaneously in the ones and millions places. Neither
thread "releases" the CPU explicitly. The GIL allows the two threads
to run concurrently without corrupting the Python interpreter. The
GIL does *not guarantee atomicity* of operations like `shared_value
+= inc` or any other single Python statement.

Therefore, the program is not guaranteed to stop. There is a race
condition at the interpreter level from the time `shared_value` is
loaded to when it is stored after being incremented (three Python
opcodes, see below). Since the window is about 200 nanoseconds on
modern processors, the program terminates almost all of the time,
especially since the majority of the time is spent in
`_cpu_intense_function`.

You would need to use a synchronization primitive like
`threading.Lock` to update `shared_value` atomically and to guarantee
the program will always stop. Again, the GIL does about atomic
execution of Python statements.

### Parallel vs Concurrent

The GIL does guarantee that only one Python thread is executing Python
statements at any one time. To demonstrate this, we'll time the code
as written:

```sh
$ time python cpu_intense.py
<snip>
real    0m4.418s
```

Then, with the `ones.start()` commented out:

```sh
$ time python cpu_intense.py | grep real
<snip>
real    0m2.366s
```

The program runs in half the time, which means the two threads do not
run in parallel, even though they are running concurrently. On my
multicore machine, a similar C program would run in about the same
amount of time in both cases. In other words, the C program scales
linearly and the Python program does not scale.

### Interpreter is Shared State

In order to understand the GIL, we need to understand what the Python
interpreter is. The interpreter is not a thread; it's just code and
data. The code is the CPython program and all its libraries, and at
first, the Python program it reads in is its only data. The
interpreter compiles the Python program and its libraries into
opcodes to be executed on a vir

When you execute `python cpu_intense.py`, the kernel starts a process,
which is the code, data, and a thread, known as the main thread in
Python. In the example above, the main thread executes the Python code
which starts the other two threads (ones and millions, in this
example). In Linux, the code is read-only and the data is, of course,
writable. The GIL is what keeps this data from getting corrupted.

In other words, the GIL is an instance of a synchronization primitive,
which is
[rather complex](https://github.com/python/cpython/blob/main/Python/ceval_gil.c)
for
[efficiency reasons](https://github.com/zpoint/CPython-Internals/blob/master/Interpreter/gil/gil.md),
that is used to protect the shared state (your program and its data)
of the Python interpreter.

### Preemption vs Cooperation

I have tried
[to use coroutines](https://www.robnagler.com/2025/03/01/Coroutines.html),
and decided that threading is the way to go in Python. That's why I'm
writing this. I'm working of device control code right now, which uses
[EPICS](https://docs.epics-controls.org), and the first example code I
showed is from [PyEpics](https://pyepics.github.io).

By and large, device control code is not CPU intense. Rather, it's
asynchronous so it needs to be concurrent. There are three types of
concurrency in Python:
[multiprocessing](https://docs.python.org/3/library/multiprocessing.html),
[threading](https://docs.python.org/3/library/threading.html), and
[asyncio](https://docs.python.org/3/library/asyncio.html). The title
of the `threading` library is "Thread-based parallelism", which is
incorrect. The GIL as noted above, prevents that. Two Python threads
*cannot* execute in parallel. Furthermore, `asyncio` does not support
I/O in any sense -- concurrently or otherwise. `multiprocessing` is
correctly described as "Process-based parallelism", which is one way
get parallelism in Python.

`asyncio` supports coroutines which are *cooperative multitasking*. When
a coroutine calls `await`, it allows the `asyncio` loop to switch
to another coroutine. Without those calls to `await`, the coroutine
would hog the CPU, especially when it makes calls to C libraries. To
demonstrate to yourself, create two coroutines, start them running,
and have one call `time.sleep(5)`. The other coroutine will not run
for 5 seconds. However, change that to `await asyncio.sleep(5)`, and
the other coroutine will run.

`threading` supports kernel-level threads which are *preemptable
multitasking*. The kernel controls when threads run, *not* the Python
interpreter. That's what `cpu_intense.py` (above) example
demonstrates. The two threads run whenever the kernel
decides. However, the GIL prevents two threads from accessing their
Python interpreter at the same time, which means that any time. The
GIL is designed to release itself very frequently, not on every
[opcode](https://github.com/python/cpython/blob/main/Lib/opcode.py),
but close enough for our purposes.

Python opcodes are to `threading` as CPU level instructions are to
Python's `multiprocessing` module, that is, parallel execution of
[forked instances](https://en.wikipedia.org/wiki/Fork_(system_call))
of the Python interpreter. Just like the GIL, the kernel switch
processes (threads) at the CPU instruction level. On single core
computers (rare nowadays), this was just fine. Today, of course, we
want to take advantage of all the cores on a processor when we need
them. A Python opcode takes many CPU instructions to execute, which is
why `multiprocessing` is used to achive CPU-level parallelism,
allowing `multiprocessing` programs running faster than `threading`
programs.

### Asynchrony vs Polling

Our example program would run faster if we used `multiprocessing`
instead of `threading`. As noted above, I'm writing this article,
because I'm writing device control code, which needs to be
[asynchronous](https://en.wikipedia.org/wiki/Asynchrony_(computer_programming)),
not necessarily parallel. For the most part, device control code ends
up waiting for devices or control requests, that is, unless it is
implemented using
[polling](https://en.wikipedia.org/wiki/Polling_(computer_science)).

Much EPICS control code uses polling, even though EPICS is designed to
be fully asynchronous.
[PyEpics Advanced Topic with Python Channel Access](https://pyepics.github.io/pyepics/advanced.html)
suggests code be written like this:

```py
pvnamelist = read_list_pvs()
for i in range(10):
    values = epics.caget_many(pvlist)
    time.sleep(0.01)
```

While this does work, it's inefficient from a CPU utilization
perspective, and it creates unnecessary latency in device driver. In
this case, the code blocks for 100 milliseconds even when all the
devices respond immediately to their "channel access" requests
(`caget`). Moreover, it's likely that this code will make too many
`caget` requests, because the actual values have not changed from the
last `caget`.

The EPICS protocol is fully asynchronous, just like the vast majority
of device drivers in operating system kernels. Another term for this
is
[event-driven programming](https://en.wikipedia.org/wiki/Event-driven_programming). At
the kernel, this is handled via device interrupts. In EPICS, it's
handled by registering for asynchronous messages for device
updates. At the Python level, PyEpics allows Python code to
[register for callbacks](https://pyepics.github.io/pyepics/pv.html#pv.add_callback)
to receive these messages so no polling is necessary. When the
callback occurs, new data is available from the device. This is why
[polling is considered an anti-pattern](https://en.wikipedia.org/wiki/Busy_waiting).

### GIL Aware

While polling can
[reduce latency in certain situations](https://events.static.linuxfound.org/sites/events/files/slides/lemoal-nvme-polling-vault-2017-final_0.pdf),
in Python code, it is an anti-pattern due to the GIL, and, as noted,
each Python opcode requiring many CPU instructions to execute. When
Python is waiting on events from the operating system, it is like any
other program, even ones written in a compiled language. This is why
writing device control code in Python is almost as efficient as
programming C.

The GIL prevents scientific code from executing in parallel, which is
the space where EPICS (Experimental Physics and Industrial Control
System) is mostly used. I think this may be the source of the
confusion. Often, the reason to use EPICS is to perform intense
computation with the results from EPICS requests. For HPC
applications, it's important to use packages like `multiprocessing`,
[dask](https://www.dask.org), and
[MPI](https://www.mpi-forum.org/docs/) in Python to avoid issues with
the GIL. For device control code, write Python with asynchronous
libraries and ignore the GIL.
