---
layout: post
title: "How does AI Work?"
date: 2026-07-05T12:00:00Z
---

People ask me this question a fair bit. I mumble something about huge
amounts of data and lots of weights. I got the question last night
from someone who knew that AIs generate one token after another, but
wanted to know **How do AIs work**? They didn't understand how that
simple process could possibly create an image or answer a complex
question.

This morning I woke up with a germ of an idea: DNA. How does DNA work?
I understand the sperm and the egg form a zygote, each donating a half
strand with some copying errors. Then, lots more copying, and a few
months later out pops a baby. Really?!?

How do ants (who all share the same exact DNA) build this?

![Ant hill in a backyard](https://commons.wikimedia.org/wiki/Special:FilePath/Ant_hill_in_backyard.jpg)

Do the ants sit down with an architect first?

We can imagine how an ant builds something out of soil, because we
know how to build sandcastles. Yet, that doesn't capture how an
**ant** thinks, or how an entire colony of ants (clones) can produce
something so varied and complex.

When I see an ant colony or a baby, it explains how AI works. Yes,
really. After decades of working with computers, it seems self-evident
to me that lots of simple steps can produce complex things. It's
definitely not obvious to the people who ask me how AI works so I'm
going to try to connect the dots.

### Space and Time

Two factors shared by ants, cells, and LLMs are time and space. A
zygote takes about a day to split into two cells. That's a slow
process, and a zygote doubles in size, or takes up twice as much
space. Two cells can do twice the work of one so there are four cells
at the end of day two. Four times as much work! Rinse repeat for 275
days, and a baby pops out with 2,500,000,000,000 cells. Working
together, space and time can create wondrous things.

Cells are slow. Artificial neurons are **very** fast. A computer
running an LLM can process a single instruction 86,000,000,000,000
times faster than a cell can divide. Moreover, a leading-edge chatbot
uses 330,000 cores (computing units) so it can actually process
28,380,000,000,000,000,000 (10¹⁹) instructions per day.

For comparison, human brains have about 80,000,000,000 (10¹¹)
neurons, of which about a billion (10⁹) are active at any one
time. Current research suggests neurons fire around 10 to 100 times
per second, putting total brain activity at roughly a maximum of
100,000,000,000 (10¹¹) spikes (or "instructions") per second. For
rhetorical (don't quote me) purposes, let's say an LLM processes about
10,000 times faster than a human brain.

The point is that ants, cells, neurons, and modern computers leverage
both time and space -- in differing amounts -- to produce really big
things. These numbers are so large that they are difficult for us to
comprehend, and this leads to us not being able to understand how they
work. We may know how a cell divides, but no one really knows when a
trophectoderm cell will form. That happens randomly.

### Randomness

How do jazz musicians solo? One note at a time. And, lots of listening
and practice. Why can the same musician have a monumental solo followed
by an ordinary one? Their listening and practice hasn't changed. It
seems random, because it is. More concretely, a jazz solo is the
product of a stochastic generative process, which is how an LLM does
its thing.

Stochastic just means there are random parts to the
process. Generative means the next step in the process depends on the
previous state of the system. A jazz musician chooses the next note(s)
at random, but it fits in with the previous one(s) based on years of
training, which is itself a stochastic generative process.

An LLM is trained in the same way: a stochastic generative
process. The numbers behind training an LLM are staggering (1,000s of
computers over many months). I won't go into zeroes just that the
creation of the LLM is an extremely complex process that would be
impossible without randomness.

We tend to think of computer programs as deterministic, like making a
cake: first you add the flour, then the sugar, then the leavening
agent, etc. Computers themselves do operate that way.  Determinism,
unfortunately, is very expensive in both space and/or time.

### Here's the Problem

Time for a math problem. Given 3, 7, 11, 15, 20, is there a subset
that adds up to 31? Yes, there is. You could eyeball it (stochastic
generative process) or you can write an algorithm:

1. Divide up all the numbers into subsets: (3), (3, 7), (3, 7, 11),
   etc.

2. Add up each subset

3. Determine if a sum is 31

That's a deterministic algorithm. It always finds the correct answer,
but in the worst case it examines an exponential number of subsets
(2ⁿ). For example, for one million numbers, there are
10³⁰¹⁰³⁰ subsets to check. That's a **humongous** number.

In computer-speak, we say there is no algorithm for a deterministic
computer that completes in polynomial time (not exponential). This is
known as a nondeterministic polynomial (NP) time problem. These types
of problems could be solved in polynomial time by a theoretical
nondeterministic (i.e., magical, non-existent) computer.

The subset problem is an example of a search problem. Another example
search problem is: has someone explained NP time problems in
non-theoretical language? That's the problem I had when I began this
section. I used an LLM to help me write this section. I got a **good
enough** answer in seconds from a deterministic computer.

### Summing It Up

LLMs are not algorithms. Rather, they use randomness with massive
amounts of compute to produce very good answers most of the time. As
you probably know, AIs hallucinate. This upsets people. One friend
says "they lie".

They don't lie or hallucinate. These are anthropomorphisms. Their
training is suboptimal, because it has to stop in polynomial (real)
time. They make mistakes, just like jazz musicians, ants, and cell
divisions, because all these processes are stochastic.

But, really, *how do they work*? By the behavior that emerges from a
simple process (artificial neuron networks) operating on very large
amounts of data over very long space-time periods. This is exactly how
DNA works: a simple process (self-replicating molecule) operating on
very large amounts of data (the world) over very long space-time
periods. The individual parts make sense on their own, and the sum of
these parts creates something utterly amazing, e.g. a baby.
