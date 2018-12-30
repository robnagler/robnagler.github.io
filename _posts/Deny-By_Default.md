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
