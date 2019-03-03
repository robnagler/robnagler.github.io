---
layout: post
title: "Quantifiably Simple"
date: 2008-04-02T12:00:00Z
---

I'm right.  You're wrong.  Conversations between programmers often
sound like this.  Being right is very important to most people.
Even when we agree to disagree, it is more like a temporary ceasefire
than true peace treaty.

Programmer interactions are fraught.  We are not taught how to
communicate in school, or even in most homes.  I think there are two
problems: emotional immaturity and unscientific frameworks.  This
article covers the latter.  I will let you work out how to become more
emotionally mature on your own.

In The Logic of Scientific Discovery, Karl Popper uses falsifiability
as a means to separate science from meta-physics,
or in philosophical circles, what is known as the
[Demarcation Problem](http://en.wikipedia.org/wiki/Demarcation_problem).  Many people disagree with Popper, and I am not going to justify or
criticize his general conceptional framework as it applies to the
physical world.  I am a programmer, not a philosopher.
I think
[Popper's ideas about falsifiability](http://en.wikipedia.org/wiki/Falsifiability)are extremely relevant to what I do every day.  Falsifiability goes
by many names, and in programming, we use the word testability.

I am talking about testability (falsifiability) of ideas, which is not
the same thing as software testing.  Ideas are not executable,
and code and tests are.
[My other articles about testing](https://duckduckgo.com/?q=site:robnagler.com+testing)focus on the process and psychology around the tests
themselves.  In this article I discuss how testable an
idea is. In particular I will rely on Popper's result that the degree of
testability can be used to define simplicity, and therefore
testability is a way to frame programming discussions to
improve objectivity and collaboration.

At bivio we want to work collaboratively.  We share a single office
(bullpen) and share a large common software framework (bOP).  Sharing
code and office space is not enough, however.  We get as tripped up as
other programmers when it comes to discussions about tough issues,
especially when they involve conflicting experience.  I believe that
the crux of the problem lies in Extreme Programming's (XP) tenet: do
the simplest thing that could possibly work (DTSTTCPW).

DTSTTCPW is also known as "keep it simple, stupid" (KISS).  Or, as
Einstein put it, "everything should be made as simple as possible, but
not simpler".  Great advice as long as we can agree on what it means
for something to be simple.  If we adopt Popper's result that
simplicity and falsifiability are equatable, our programming
discussions can be built on a solid foundation.  This is why I like
the idea of Popperian Programming.

There is a strong relationship between Extreme Programming and
Popperian Programming.  Another XP tenet is once and only once (OAOO),
which is another form of simplicity in programs.  The interesting
thing about OAOO is that it is well-defined.  If you can see
duplication, it is not OAOO.  The test (refutation) for one OAOO is
important, or programmers might loop forever trying to remove
duplication in their code -- and some programmers do!

This asymmetry around refutability between OAOO and DTSTTCPW has
always bothered me.  It is one of the reasons why I disagree with
quality as one of the
[Four Variables](http://c2.com/cgi/wiki?FourVariables)of XP.  To me quality is not knowable.  We only know it when we see
it, and two people's definition of quality is never the same.
The rest of the Four Variables (scope, time, and resources) are
quantifiable, or knowable in the limited Popperian universe of
programming.

In my version of XP, I use ^Risk_as_the_Fourth_Variable, because it is
knowable.  In Popperian terms, risk is simply the quantification of
all possible tests (refutations, falsifications) of a program, or
concept to be programmed.  Neither Popper nor I say you can prove
anything about the existence or completeness of refutations.  Rather,
if you are going to have a discussion about risk (or its subjective
counterpart: quality), you need to be able to define it in concrete
terms, or tests.  In programming, a test is an absolute yes/no
(pass/fail, true/false) question you ask of a program.

The advantage programmers have over philosophers is that our tests are
*executable*.  That's why I am a programmer; it is natural for me to
want to know an exact answer.  Uncertainty is not a happy place for me
-- but I am learning to live with it! Other sciences do not have that
luxury, because the relate to the universe.  The programming language
we use defines our universe, and is absolutely computable for the vast
majority of tests we think up.  This is the trait is what allows me to
believe that simplicity about programs is also knowable.

When we (my fellow bivions and I) define a programming idea's
simplicity as the degree of falsifiability, we have an absolute test
for what it means to be simple.  We tried this the other day, and the
results were extremely interesting: my brilliant idea was refuted.
More important, I was excited that we found a refutation!  Instead of
the discussion wandering between boxes and lines and other whiteboard
scribbles, we focused on listing all the possible refutations for the
idea.  (A practical example would be good at this point, but I
couldn't think of one that was practical in the context of this
article -- suggestions welcome!)

The other nice thing about listing refutations about an idea is that
the work is always useful.  It is just like test-driven development:
the tests are probably the most valuable part of the code base,
because tests are an executable specification for the program.  If a
test identifies a defect in the program, we can either repair the
program, or, more boldly, throw out the whole program and start over.
While the former is much preferrable to the latter, both are
inconsequential in comparison to the executable knowledge embodied in
the test suite.

The same is true for refutations about programming ideas.  When a
discussion group can agree on a valid refutation, it can be applied
over and over again to new ideas.  Just as tests reduce our fears
around coding, refutations free us from fear when brainstorming!

By the way, falsifiability is a very old idea.  The Logic of
Scientific Discovery was first published in 1934.  When I started
writing this, I thought this was an original idea.  Fortunately, there
are many refutations to this statement:

[Popperian Software Design](http://www.bossavit.com/pivot/pivot/entry.php?id=239)
[Karl Popper's Critical Rationalism in Agile Software Development](http://www.springerlink.com/content/n2004645x23k5657/)
[The Concept of Change in XP: Kuhn vs. Popper (PDF)](http://espresso.cs.up.ac.za/publications/MandyNorthover.pdf)
[Agile Software Development: A Contemporary Philosophical Perspective (PDF)](http://portal.acm.org/ft_gateway.cfm?id=1292504&type=pdf)

