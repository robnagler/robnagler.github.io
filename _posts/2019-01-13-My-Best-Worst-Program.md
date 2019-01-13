---
layout: post
title: "My Best Worst Program"
date: 2019-01-13T12:00:00Z
---

Ah, Emacs! This is the first post written entirely in Emacs for
robnagler.com after it was migrated from ViaRob. Yay!

The [conversion program](https://github.com/robnagler/robnagler.github.io/blob/master/_viarob/convert.py)
was non-trivial but still under 300 lines. The Python program
reads
[BOP Wiki](https://www.bivio.biz/site-help/bp/Edit_Wiki_Page_Help)
and outputs [Kramdown](https://kramdown.gettalong.org)-flavored
[Jekyll](https://jekyllrb.com) with an
[Nginx map](http://nginx.org/en/docs/http/ngx_http_map_module.html)
for the redirects from viarob.com to robnagler.com to
[maintain backwards compatibility](https://www.robnagler.com/2015/04/11/Major-Release-Syndrome.html).

This was the Best Program I've written in a while, because it solved
one problem, completely. A single file of code that addressed all the
business requirements, which will never be used again, except as an
example for this article. Most

Most of what I do involves tens of files to do anything, usually a lot
more. Even when adding a line or two of code, I may have to read
through tens of packages, comprising hundreds of files.

Much of my software seems to live forever. The BOP Wiki has been
[around since 2006](https://github.com/biviosoftware/perl-Bivio/commit/18cf20d7a984e1b0e62af3f89c89a51ab39a3d2d#diff-0561dfd6c1465d08dc034e23f1d085b7),
and will be in use for many years to come. That means writing tests,
dealing with bugs, and eliciting feedback.

None of this is true about My Worst Program. I employed copy-and-paste
liberally. There are no tests. I didn't talk to anyone about it.
There were plenty of bugs, but I dealt with some of them by
[editing the input files](https://github.com/robnagler/robnagler.github.io/commit/dc79fb742250c87bad779d9445f0097051a0807b)
in Emacs with a macro, because that was faster. Other bugs were
[fixed after the fact](https://github.com/robnagler/robnagler.github.io/commit/34f706528e5c763d13b3294125abda0537be1f2a).

However, even My Worst Program uses techniques that
many programs seem to do without. I'll list three of
the most important here (in order):

1. [Fail Fast](https://github.com/radiasoft/pykern/wiki/DesignHints#fail-fast)
   to catch missed cases, e.g. there shouldn't be
   any [missed at-signs (@)](https://github.com/robnagler/robnagler.github.io/blob/a684612bd9982cd4dfc3f96fc90500c3f613d1e4/_viarob/convert.py#L269)

2. [Constants](https://github.com/radiasoft/pykern/wiki/DesignHints#explicit-coupling-bind-values-programmatically)
   bind concepts explicitly, and help me think clearly about them.

3. [No naked prints](https://github.com/radiasoft/pykern/wiki/DesignHints#output-for-programmers-logging),
   just out of religous habit.

I'm sure you have a different opinion, and feel free to email
me at robnagler.com.

The important thing is that My Best Worst Program worked, and
I'm happy to write that here in my favorite text editor where
I now can commit changes to this article quickly and easily!
