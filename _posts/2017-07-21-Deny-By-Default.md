---
layout: post
title: "SecurityTip: Deny by Default"
date: 2018-12-29T22:23:39Z
---

> Around 12:00 PST, an unknown attacker exploited a critical flaw in
> the Parity multi-signature wallet on the Ethereum network, draining
> three massive wallets of over $31,000,000 worth of Ether in a matter
> of minutes. --
> [A hacker stole $31M of Ether@&#8202; by Haseeb Qureshi](http://n99.us/wfy)

This is [a nice article](http://n99.us/wfy) on how a hacker stole $31M
of Ethereum (cryptocurrency). It explains why Ethereum is different
from Bitcoin, something I hadn't known, and explains how the hack
worked and how it was thwarted. Well-written and worth a read for the
more deeply curious.

The one quibble with the article is that the author states, "Mistakes
of this sort are *routinely* made in programming.". That's true, of
course, but a platitude and not a good excuse. Ethereum is special,
and standard security rules should apply when building dispatch
mechanisms. The author notes that "The safer approach here would be to
whitelist specific methods that the user is allowed to call." Yes,
always dispatch with a whitelist or some affirmative action on the
part of the programmer. The default is deny, not allow. A quick search
found [an article from CERT](http://n99.us/fdh) that points to
[a 1975 article](http://n99.us/fss) that in turn mentions the
principle was first suggested by E. Glaser in 1965.

A while ago I wrote
[an article on dispatch, don't decorate](../Dispatch_Do_not_Decorate)
, where I mention that you should use patterns for dispatch. It's a
subtle mention, because the point of the article is about using
dispatch not decorators. If the Ethereum author had used a
pattern-match for allow instead of a pattern match for deny
("internal"), this problem would not have occurred.

Here's what we do in [what we do in Sirepo](http://n99.us/agw) for
method dispatch in the server:

```py
def func_for_api(api_name, api_module):
    res = getattr(api_module, _FUNC_PREFIX + api_name, None)
    # Be very restrictive for this since we are calling arbitrary code
    assert res and isinstance(res, types.FunctionType), \
        '{}: unknown api in {}'.format(api_name, api_module.__name__)
    return res
```

The pattern here is FUNC_PREFIX, which is "api_" so only methods that
begin with "api_" would be called. That's the "whitelist" that the
article's author talks about. You don't need a whitelist as that has
to be maintained and audited. What you want is a name that identifies
the function as a dispatch item. There are some subtleties in choosing
the name. It contains an underscore so that it doesn't collide with
builtins in Python. It doesn't begin with an underscore so we know it
is a public method. Note also that "func_for_api" asserts the object
is a function (not some other callable). And, if the method has some
bug, it'll not dispatch (return the method) by default. That's pointed
out in the CERT article as well.

Dispatch is common programming nowadays. Just make sure it requires
the programmer to state explicitly that the dispatch is allowed.
