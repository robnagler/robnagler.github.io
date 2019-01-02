---
layout: post
title: "Dispatch, Don't Decorate"
date: 2015-08-24T12:00:00Z
---

A typical Python web application uses decorators
[like this](http://n99.us/sgd):

```python
@app.route('/secrets')
@requires_auth
def api_hello():
    return "Shhh this is top secret spy stuff!"
```

The
 `@app.route`  and
 `@requires_auth`  syntax is known as a decorator in Python, which
is a powerful technique to extend functionality to existing functions.
You can
[learn more about them](http://n99.us/kaj) from Jeff Knupp.

Web frameworks make extensive use of
decorators
 `@require_auth`  to protect functions and
 `@app.route`  to bind URIs to functions.
In this article, I discuss some issues with decoration, and suggest you use
dynamic dispatch instead.

## Static Decoration Hinders Reuse

Python's decoration syntax is static. However, the concept of decoration is
usually referred to in a dynamic context. From Wikipedia, for example, the
[Decorator Pattern](http://n99.us/aay)"allows behavior to be added to an individual object,
either statically or dynamically, without affecting the behavior
of other objects from the same class." Interestingly, the examples are
all written in Java, which is generally thought of as a static language, which
unlike Python, does not allow you to define decorators statically.

Static decoration is problematic, because it reduces reuse. Consider
[this example](http://n99.us/gjj):

```python
@app.route('/')
def show_entries():
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)
```

The
 `@app.route`  decorator statically binds the URI "/" to the function
 `show_entries` . The decorator also checks
 `show_entries` 's parameters to see if they match the URI.

The decorator also has the property of making it impossible
to call
 `show_entries`  outside of the context of a Flask application.
 `app`  is an instance, which must be passed in to the module
both statically and globally. The module cannot be
compiled without
 `app`  being initialized.

You cannot reuse
 `show_entries`  in any other execution context. For example, you might want
to invoke a command line program that calls
 `show_entries` . The command line program must
initialize a Flask app and provide it to the module. What's
more insidious in this case is that
 `app`  is a global attribute of the containing module, which makes
it very difficult to workaround, for example, by monkey
patching
 `app`  as a mock object before the decorator is called.

## Dispatch Enables Reuse

A different approach to wrapping functionality around existing functions
is with a
[Dispatch Table](http://n99.us/igp). Instead of statically binding the routes to functions, you can bind
the functions in a dispatch table like this:

```python
ROUTES = {
    '/': show_entries,
    '/add': add_entry,
    ...
}
```

This simple change decouples
 `show_entries`  from a Flask app, allowing it to be used elsewhere
without the need to load Flask.

When you want to
use Flask, use the
[ `add_url_rule`](http://n99.us/gtc) method:

```python
import my_module
app = Flask(__name__)

for url in my_module.ROUTES:
    app.add_url_rule(url, view_func=my_module.ROUTES[url])
```

This simple change also improves cohesion: Flask routing is
co-located with Flask app management.

## Dispatch Improves Security

You may be wondering about how to implement
dispatch with the
 `@requires_auth`  decorator in the first example, which I'll repeat here:

```python
@requires_auth
def api_hello():
    return "Shhh this is top secret spy stuff!"
```

One problem with this way of ensure authentication is that
the default is "no auth". If you leave off the
 `@requires_auth`  decorator, the web framework will not do any authentication
or authorization. Anybody can execute
 `api_hello` . That's not a good default behavior.

Let's change the dispatch table a bit:

```python
ROUTES = {
    '/': (show_entries, ANYBODY),
    '/add': (add_entry, ADMIN),
}
```

With this change, we are declaring roles required to access
a particular function. Not only that, we have an overview of
all the required authorizations at a glance. This can be very
helpful for security audits.

When we register the endpoint, we can then do something
like this:

```python
for url in my_module.ROUTES:
    fn, role = my_module.ROUTES[url]
    app.add_url_rule(url, view_func=auth_wrapper(fn, role))
```

The function
 `auth_wrapper`  ensures that role is valid, and returns a new function that
wraps the view function
 `fn`  with authorization code. All view functions are wrapped
so there is no "default" security model. Authorization is
required.

Experienced Pythonistas reading the above example
may say, "that's just another way of decorating functions!" True.
I've purposefully
kept out of the weeds here. Dispatches should happen without
wrapping functions, since they
are framework specific. In Flask, I might use a
[signal](http://n99.us/par) to lookup the authorized role(s) in the dispatch table.

## Dispatch with Patterns

In general, I don't like dispatch tables for URL routing. That's
a complex subject, but the more general rule is that you should
use pattern-matching for dispatching when you can.

Here's a less complex problem, implementing
[logging with a decorator](http://n99.us/ksv), which will demonstrate the dispatch using regular
expressions:

```python
@log_event('Delete Invoice', objectid_param='invoiceid')
def delete_invoice(self, invoiceid, **options):
    # delete the object
```

This decorator causes a log message to be output when
the method
 `delete_invoice`  is called. Let's say that we want this type of logging only
when debugging. Indeed, we may only want to debug
the methods having to do with invoicing. To keep things
simple, I'll assume that we have a way of hooking into
the request processing. The
 `before_request`  function might look like this:

```python
def before_request(request, view_func):
    if LOG_REGEXP.search(view_func.__name__):
        _log(view_func, request)
```

Every time a request is called, we check the name of the view
function. If it matches,
 `_log`  is called with the view function and the request object.
 `_log`  might introspect the arguments for the view function
and extract those from the request or simply output the
URL and/or POST arguments. The important thing is that
you know that every function which matches
 `LOG_REGEXP`  will be called without having to worry that someone missed
adding a decorator.

## Special Cases

There are certainly decorators that cannot be dispatched. The
 `@classmethod`  and
 `@staticmethod`  decorators are two obvious examples. These decorators define
semantics about the functions themselves. Python needs
to use decorators in this case to adjust the arguments of the
calling function so that they get the correct object.

I would not call these decorators according to the Decorator
Pattern: to extend functionality to existing function. They
are syntactic sugar to simplify idiosyncrasies of Python's
method dispatch mechanism.

There are certainly other special cases, and I'll be happy
to hear about them. The vast majority of uses of decorators
I've seen (thus far) would be better off defined in centralized
dispatchers.


