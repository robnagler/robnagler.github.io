---
layout: post
title: "Major Release Syndrome: A Case for Chronological Versioning"
date: 2015-04-11T12:00:00Z
---


> "Personally,
> I like to think of version numbers as dogtags for your software.
> Like dogtags, they're primarily designed for use
> in the event of an emergency." --
> [Jeff Atwood, 15 Feb 2007](http://n99.us/coy)

Version numbers are a necessary evil. Users and programmers need them
when something goes wrong. When you search for the bug on the web,
you want to know if there is a _newer_ version released, which contains a
fix. That's it.

Marketing people need version numbers to generate excitement.
These days they have switched to code words like Jelly Bean, Yosemite, and Trusty Tahr
to make releases even more exciting. I think they are more confusing for
users who are not "in the know", but I'm not a marketeer so don't listen to me.

As a programmer, I am concerned with two things: version numbers need to
be sequential and easy to manage. Dates are god's solution to this problem.
At Bivio, we've been using Chronological Versioning for 15 years, and it's always easy to
know the answer to these three questions:

1. What version is deployed?
2. What's the next number?
3. When was it built?

In order to make them a bit more digestible, we split the date and the time, e.g.
20150410.205405. Not much to say about it.

## Semantic Versioning

Many people believe that
[Semantic Versioning](http://n99.us/dui) is the right approach to numbering releases. This approach supposedly avoids
"dependency hell", because users can know which releases break backwards
compatibility. To solve this problem, version numbers are clearly specified
as follows:


> Given a version number MAJOR.MINOR.PATCH, increment the:
> 1. MAJOR version when you make incompatible API changes,
> 2. MINOR version when you add functionality in a backwards-compatible manner, and
> 3. PATCH version when you make backwards-compatible bug fixes.


For simple systems, this works just fine. The programmers know the system well enough
to understand when a change is not backwards-compatible.

## Irrevocable Compatibility


> "The first rule of kernel development is: we don't cause regressions." --
> [Linus Torvalds, 26 Oct 2017](http://n99.us/slo)

Semantic Versioning assumes that APIs must at times be incompatible. This need
not be the case. Unix has had compatible APIs for decades.

Really! Go back to
[Volume 1 of comp.sources.unix](http://n99.us/yvp), and download
[cshar](http://n99.us/pev), which was published by Gary Perlman on June 2, 1985.
You can then
[unshar it](http://n99.us/ssr) and run make.

You can then use the resultant program "shar" to recreate the shell archive from which
it was built. The only change I had to make was to run make with "CFLAGS=-w" to turn
off warnings, which did not exist in 1985, but the feature "make CFLAGS=-w" did exist
in 1985.

Let's consider just how many APIs are 100% compatible three decades later:

* C programming language and preprocessor
* C libraries: stdio.h, sys/types.h, sys/stat.h, ctype.h, sys/dir.h
* C compiler
* Unix shell
* make
* nroff
* Utilities: mkdir, chmod, test, wc, echo, cat, sed, cd
* man macros (shar.1 man page formats perfectly)
* Names of all the above utilities (cc, Makefile, /bin/sh, etc.)
* Program invocation API (argv, argc, stdin, stdout, stderr)

Even better, the mail message sent by Perlman contains properly formed RFC 822
header lines (some were stripped by the archiver):


> From: decvax!wanginst!perlman
> Date: Sun, 2 Jun 85 16:35:35 edt
> Subject: improved version of shar (shell archiver)


This message is 100% compatible with today's mail systems, and I sent it to gmail verbatim
to see it worked:

![From wanginst!perlman](/assets/i/19850602-cshar.png)

Note that the text in the message: "Here is a new version of my C share program."
No version number, but the shar does have a perfectly valid and understandable
release identifier:


> # This archive created: Tue Jun  4 01:07:18 1985
> # By:   Gary Perlman (Wang Institute, Tyngsboro, MA 01879 USA)


There are many other examples of maintaining compatibility over decades such as
HTML, MS-DOS, Perl, Lisp, qwerty, etc. I think it is safe to say that the most successful systems
out there are the ones which have taken great pains to be keep their APIs compatible
over the years.

## Release Promotion

Chronological Versioning is in use on a few systems such as
[Ubuntu](ubuntu.com) and
[CoreOS](coreos.com). Ubuntu 10.4 was released in April 2010. Ubuntu takes Chronological Versioning
one step further by forcing releases to be time-based, that is, new release are
promoted on a fixed schedule: 6 month releases with a long term support release
every two years. In any given release, backwards compatibility will almost certainly
break, because Ubuntu is far too complex to know if any one API is not backwards
compatible.

Ubuntu's release promotion schedule avoids Major Release Syndrome, which is
the idea that software is reliable if it is delivered in well-defined and completely
understood chunks. This is the core philosophy behind Semantic Versioning, which
works fine for simple systems. However, any sufficiently complex system such as Ubuntu are
not knowable.

An Ubuntu release is a point in time snapshot in a stream of updates
so no one really knows what version they are running. If you "apt-get" a package
that wasn't previously on your system, your system has just been updated to
a unique version of Ubuntu. Your computer is running a unique combination of
packages installed at a specific time, which has its own unique set of bugs.

The folks at CoreOS take time-based releases one step further:


> "CoreOS releases progress through each channel from Alpha &rarr; Beta &rarr;
> Stable. You can think of each release on a lower channel as a release-candidate
> for the next channel. Once a release is considered bug-free, it is promoted bit-for-bit
> to the next channel.
> 
> If you're deploying a new machine, it is recommended to deploy a version attached to a channel instead of the highest version number available." --
> [CoreOS Release Notes](http://n99.us/nft)

There are no major releases with CoreOS. Users get to choose an update stream, and
the releases flow after they are promoted to that stream (alpha, beta, or stable). Their
update philosophy is simple:
[We believe that frequent, reliable updates are critical to good security.](http://n99.us/sxk)
What matters to the CoreOS team and their customers is release promotion, not
version numbers. CoreOS has version numbers, but they are the same across alpha,
beta, and stable channels, which means that you know that by the time a version is
promoted to stable, it has gone through the alpha and beta channels.

With semantic
versioning, alpha, beta, release candidates, and final versions all have different
numbers. This usually means the promotion process involves recompiling the code.
While this theoretically will produces exactly the same package as the previous
release level, there's no guarantee that the underlying operating system hasn't been
updated between compiles. A small bug fix might introduce an incompatibility between
promotion levels. This is why CoreOS promotes the already compiled packages, not
the source code.

## Patches are Dangerous

Semantic versioning makes the assumption that patches are "better" in some sense
than backwards-compatible features. I don't see it that way.

A backwards-compatible feature is new code. An API is less likely to break when
someone is focusing on a new feature. Refactoring can break code, of course, but
that can happen with any change.

Patches fix existing APIs. If anything is going to break an API, it's changing the
code that underlies. Bugs are often caused by copy-and-paste errors so the proper
patch is to refactor the code. To my mind, there's very little difference between
a patch and feature, that is, if they are both coded to be backward compatible.

## Maintaining Compatibility

While backwards compatibility can be guaranteed, programmers want to take advantage
of newer APIs for better security, faster performance, etc. We can take advantage of
new APIs through two mechanisms: feature testing and shims.

Shims are easy to explain:


> "A shim is a small library that transparently intercepts API calls and changes the arguments passed, handles the operation itself, or redirects the operation elsewhere. Shims typically come about when the behavior of an API changes, thereby causing compatibility issues for older applications which still rely on the older functionality. In such cases, the older API can still be supported by a thin compatibility layer on top of the newer code. Web polyfills are a related concept." --
> [Shim (computing), Wikipedia](http://n99.us/wdv)

Many programming languages have builtin shims. For example, you can use the "future"
module in Python to make your code both forwards and backwards compatible.

An older feature is called "feature testing", which first came about to support software
portability. The article
[*Feature-Based Portability* by Glenn S Fowler, David G Korn, J J Snyder, Kiem-Phong Vo, 1994](http://n99.us/xop)explains the problem quite clearly:


> Current computer platforms encompass a dizzying variety of hardware and software.
> A software application may live or die based on how portable it is.
> [...] This paper describes IFFE, a tool and an accompanying programming style
> that supports software portability. IFFE has enable the porting and construction
> of many large software applications on heterogeneous platforms with virtually no user
> intervention.


[IFFE](http://n99.us/uwv) is still available.
[Autotools](http://n99.us/ipf) is a build system designed to make portable programming easy.

## Version Testing is Evil

One of the biggest dangers of Semantic Versioning is that programmers will rely
on a version number to ensure compatibility instead of using feature testing or
shims. Version testing is using the version number to drive the way the software
behaves. Here's an example from
[Writing Backward-Compatible Code: Appendix A - Ruby Best Practices](http://n99.us/kdz)by Gregory Brown:

```ruby
def my_method(string)
  lines = if RUBY_VERSION < "1.9"
    string.to_a
  else
    string.lines
  end
  do_something_with(lines)
end
```

Brown warns us to "Resist this temptation! If you aren't careful, this
will result in a giant mess that will be difficult to refactor,
and will make your code less readable. Instead, we can
approach this in a more organized fashion."

Instead he recommends, Selective Backporting where he creates a shim as follows:

```ruby
class String
  unless "".respond_to?(:lines)
    alias_method :lines, :to_a
  end
end
```

This encapsulation depends on the feature test for the "lines" method. It's clear
what's going on, and keeps the code modular and maintainable. With version
testing, there is an implicit coupling between the feature and the version number.
If you happen to get the version number wrong, or worse, the feature changes
yet again in another version, your code will break. It's much more reliable to
test for feature existence.

## KISS

This article does not have a version. It has an original release date (below)
and with luck, I'll improve it over time. Nobody cares about those updates.
If someone finds a bug in this article, they'll email me around the same time,
and I'll know which version they are talking about. Nothing more is needed.

Semantic Versioning is much more complex. There are 11 clauses
[in the specification](http://n99.us/dui). Chronological Versioning is so simple that it needs only one rule:
YYYYMMDD.HHMMSS. This numbering system complies with all build
systems so it's plug and play.

Dependency hell is the driving force behind Semantic Versioning. Unfortunately,
Semantic Versioning promotes the poor programming practice of not maintaining
backwards compatibility and relying on version numbers for API changes.

These poor programming practices cause dependency hell, not the other
way around.  We have known how to make systems which survive API changes
for decades. Well-written and (surprise!) popular software maintain backwards
compatibility for this very reason. Feature tests and shims allow code to take
advantage of newer APIs seamlessly. Version numbers are not required for
either of these practices.

Versions are a necessary evil. Chronological versions allow us to manage releases
as simply as possible.


