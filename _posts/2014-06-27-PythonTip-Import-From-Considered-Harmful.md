---
layout: post
title: 'PythonTip: "import from" Considered Harmful'
date: 2014-06-27T12:00:00Z
---

[Namespace pollution](http://bytebaker.com/2008/07/30/python-namespaces/) is the main argument against wildcard imports:

```python
from foo import *
```

While explicit unqualified imports are
[considered fine](https://www.python.org/dev/peps/pep-0008):
```python
from foo import bar
```

There is, however, a harmful side-effect of unqualified imports:

```python
from sys import stdout

stdout = open('stdout.txt', 'w')
print('hello')
stdout.close()
assert open('stdout.txt').read() == 'hello\n'
```

The assertion fails, because the output from
 `print`  does not go to
 `stdout`  rather it goes to the value of
 `sys.stdout` .  Unqualified imports in other languages do not work this way, that is,
the qualified and unqualified names are exactly the same thing.

For qualified imports, the attribute's value is retrieved on every use
so the following example works as you would expect:

```python
import sys

sys.stdout = open('stdout.txt', 'w')
print('hello')
sys.stdout.close()
assert open('stdout.txt').read() == 'hello\n'
```

Python imports values, not names.
The interpreter makes a new variable in the importing
module with the reference of the variable from the exporting module.
When the first example assigns to
 `stdout` , it assigns the newly opened file to the importing module's variable,
which happens to be called
 `stdout` . The
 `as`  keyword makes this behavior explicit.

Here's the first example rewritten with
 `as`  to show this effect:

```python
from sys import stdout as new_stdout

new_stdout = open('stdout.txt', 'w')
print('hello')
new_stdout.close()
assert open('stdout.txt').read() == 'hello\n'
```

While this is not the typical form of using the
 `as`  keyword, it shows more clearly that
 `new_stdout`  is a name defined in the importing module.
The name
 `sys.stdout`  is easily seen to be unrelated by this
atypical usage of the
 `as`   keyword.

Python also creates a new variable for a module import.  All of
these names are all "the same", that is, they are attributes, and
you can do strange things like this:

```python
import sys

sys = 1
assert sys == 1
```

The assertion passes, because the reference to the module
 `sys`   is replaced by the reference to the number
 `1`  by the assignment.  The code on line three does
not reassign the meaning of
 `sys`  globally, that is, another module which imports
 `sys`  will get a copy of the module reference, not a reference to the
number
 `1` .

## `from` impedes `reload()`

To reload a module, you have to pass the reference of the module to the
 `reload`  built-in function.  Reloading a module
has to reuse the exact same reference, because every
 `import`  makes a copy of the reference in the importing module.

The subtle thing about reloading is that any attributes of the module which
are imported unqualified (using
 `from` ) do not change.  The following complex example demonstrates this problem:

```python
import os
import sys

def write_m1(val):
    f = open('m1.py', 'w')
    f.write('''
def f1():
    return {}
'''.format(val))
    f.close()
    os.unlink('m1.pyc')

write_m1('1')
from m1 import f1
assert f1() == 1

write_m1('2')
reload(sys.modules['m1'])
assert f1() == 2
```

The assertion fails on line 20, because
 `f1()`  still returns one, not two.  A qualified call
 `m1.f1()`  would return two.

Reloading modules is very useful for large systems where reloading a
single module is orders of magnitude faster than reloading the whole system.
You can find
[references to this problem](https://docs.python.org/2/howto/doanddont.html#from-module-import-name1-name2), but it's not widely known.  People argue against
 `from`  for stylistic reasons (which I strongly agree with).  I go further
and say that
 `from`  is harmful, and should be deprecated.
