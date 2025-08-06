---
layout: post
title: "Python Global Interpreter Lock"
date: 2025-03-01T23:00:00Z
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

This is confusion
[between parallelism and concurrency](https://www.robnagler.com/2025/03/01/Coroutines.html#cooperative-vs-preemptive-multitasking). The
GIL *prevents parallelism*, which *allows concurrent* execution of
threads in the same Python interpreter. A simple example will show the
difference.

### CPU Intense Example

Here's some code, which demonstrates *concurrent* execution of two CPU
intensive Python threads:

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

The output demonstrates that the `shared_value` increases by ones and
millions simultaneously, and the program stops once `shared_value` is
greater than 500,000,000:

```sh
$ python cpu_intense.py
74000077
153000152
232000233
310000313
386000391
465000469
500000500
```

The GIL ensures that `shared_value` is updated atomically. If that
weren't the case, the program might not stop. You can rerun this
program many times, and it will always stop when the millions thread
is finished. If there were contention for `shared_value`, the ones
thread would sometimes overwrite the last update of the millions
thread, and `shared_value` would never get past 500,000,000.

### Parallel vs Concurrent

To demonstrate that the code is executing on a single core, first time
the program:

```sh
$ time python cpu_intense.py
<snip>
real    0m4.418s
```

Now, comment out the ones thread and time again:

```sh
$ time python cpu_intense.py
real    0m2.366s
```

You see that it runs in half the time even though I have multiple
cores on my computer.

### Interpreter is Shared State

In order to understand the GIL, you need to understand what the The
Python interpreter is and what it is not. The interpreter is not a
thread. It's just code and data. The code is the CPython program and
all it's libraries, and at first, the Python program itself is its
only data.

When you execute `python cpu_intense.py`, the kernel starts a process,
which is the code, data, and a thread, known as the main thread in
Python. In the example above, the main thread executes the Python code
which starts the other two threads (ones and millions, in this
example). In Linux, the code is read only and the data is, of course,
writable. The GIL is what keeps this data from getting corrupted.

In other words, the GIL is an instance of a synchronism primitive,
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

That



 One way to think of this is that the interepreter
`multi


`mult


thread that executes the Python interpreter is started


not a thread. This is important. Rather, it
is just like `shared_value`, that is, a chunk of memory that is shared
between threads.

prevents Python from executing concurrently, but
[unlike (asyncio) coroutines](https://www.robnagler.com/2025/03/01/Coroutines.html),
Python threads do preempt one another *at any point*

interpreter is a bunch of memory so it needs lock. you use locks to
update the shared state in the python interpreter. it's not parallel,
which compute intensive tasks need, it's fully asynchoronous which UI
and device driver code needs.

so any code that is compute intensive (aka high throughput or high
performance computing) should run in a separate Python
interpreter. Most applications are not compute intensive. Asynchronous
applications, e.g. user interfaces or EPICS control systems, do
require *preemptable* concurrency, which Python threading supports
very well.

c code

### `in` consumes an iterable

For user-defined classes which do not define `__contains__()` but do
define `__iter__()`, `x in y` is True if some value z, for which the
expression `x is z or x == z` is true, is produced while iterating
over `y`.

[private note](https://github.com/radiasoft/discuss/issues/14)
