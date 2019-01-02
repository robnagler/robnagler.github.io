---
layout: post
title: "The Psychology of Software Testing"
date: 2008-02-03T12:00:00Z
---
Test anxiety is number two right after number one (existential anxiety) on
[Wikipedia's Anxiety page](http://en.wikipedia.org/wiki/Anxiety).  All kinds of tests
provoke anxiety: medical tests ("I'm gonna die!"), Rohrshach inkblot
test ("I'm going crazy!"), and DUI tests ("I'm going to jail!").
Our society trains us to fear tests.

This fear and others hounds programmers into a congitively dissonant
stupor about testing.  Ask a programmer if testing is good, and the
answer will be yes.  Now ask how much time she spends testing.  Get
ready for a litany of excuses about resources and time, or
silence.

The psychology of software testing is a mess.  The demons in the
closet must be challenged.  We need a new software testing ethos.  One
in which tests are seen as collaborative tools and testing more than
quality assurance.  Testing accelerates problem decomposition.

## Quality Insecurity

Tests are a smack in a programmer's face.  A test is a challenge to
your knowledge, your skill as a programmer, and to some, your
identity.  After spending week upon week pawing through excruciating
complexity, your code is sent off to Quality Assurance (QA) whose sole
reason for existence is to break your code.  If they do not break it,
they get in trouble for not writing good enough tests.  If they do
break it, you get in trouble for writing shitty code.  Ugh.

Even when you integrate QA in your development process as recommended
by the
[Extreme Programming](http://www.extremeprogramming.org) gurus, you are still screwed:

* Do the simplest thing that could possibly work (DTSTTCPW)
* Once and only once (OAOO)
* Test what is likely to break

The first two are coding rules, which use definitives and superlatives
to describe exactly what you are supposed to do.  There are no
questions about what you are supposed to do.  The last rule is quite
tricky.  What do they mean by "what" and "likely"?  Way too nebulous
for me.  The first two have acronyms (showing their pervasiveness) and
the last one does not.  Go ahead,
[search on TWILTB](http://www.google.com/search?q=twiltb&lr=lang_en) to see what you come up with.  This page will be the 11th hit once
Google gets to it, and it is the only page which discusses software
testing.

## Software Testing Demons

When I searched for the term
**Software testing ethos**, I came up with
[one hit](http://www.forsv.blogspot.com/2004_06_01_forsv_archive.html), which reads as follows:


> Readers of this site who are unfamiliar with software testing ethos or
> uncomfortable around software testers may find the following material
> objectionable, immoral and/or disturbing. Well tough. Testing isn't
> for choir girls and altar boys.. It is a demanding craft that requires
> of its practitioners: deviousness, a desire to cause harm and a
> general disdain for rules and regulations. Click the Back button to
> retreat to moral high ground.


Wow, that is one powerful psychological punch.  And, if that was not
enough, the blog entry ends with:


> "Tester's Golden Rule"
> 
> Do unto others until they hate you


This is an incredibly biased statement that in a much softer wording
matches the ethos of many QA departments.  Confrontation is the
general approach where collaboration should be the norm.  Even if it
is friendly competition, the language of QA involves: crashing,
attacking, destructive testing, etc.  I am going to delve into this in
greater detail to demonstrate how this becomes a psychological trap
for programmers.

## Let's Get Physical

Software testing psychology is rooted in breaking things, because
that is what all testing was until software was invented.  Your job as
a tester was to break physical objects by heating, freezing, and
heaping abuse on them.  QA is also responsible for non-destructive
testing such as burn-in and stress testing, but even this language is
psychologically biased toward confrontation and abuse.

Software testing has nothing to do with physical objects or abuse.
Typically, software tests validate a specific set of behaviors.  After
software is tested, it is perfectly usable.  And, you only need to test
one copy of the software, since all copies are identical.  I am not
talking about the physical media that the software comes on.  Just the
bits itself that get put on the media.

When a tester "breaks" software, nothing bad happens.  Indeed, it is a
really good thing.  The "break" is knowledge, and the software design
can be improved to correct an incorrect assumption.  That is, after
all, all we mean by "broken software": it is a miscommunication between
the programmer and the customer or an misapplication of a programming
construct or language.  Software ain't broke if the customer agrees
with the way the program behaves -- even when the program and the
specification disagree.

This disconnect between classical QA methodology greatly affects
software testing psychology.  The classical QA approach is **broken**
due to its emphasis on breaking things.  Software testing requires a
clear and distinct shift from testing knowledge to acquiring new
knowledge.  Software testing is about learning; we find out more about
our customer's problem (or his own understanding of it) by creatively
probing the programmer's understanding (as coded) to date.

Unlike hardware, software can be fixed incredibly cheaply.  This means
you can actually start testing software in its infancy -- even before
the customer sees it.  Nothing is broken or damaged by early testing.
On the contrary, tests help programmers -- and I argue later,
customers -- learn what the program is supposed to do.

## Userless Ivory Towers

Learning is dynamic.  Requirements gathering is a give-and-take process.
Not so in university computer science departments.  Students of
software do not learn how to see a program evolves as a user discovers
its power and weaknesses and how it affects the user's workflow.
Instead budding programmers learn the exact science of algorithms,
data structures, combinatorics, graph theory, and so on.

These mathematically-oriented courses form the core curriculum in most
computer science departments.  Testing is rarely covered, and if so,
only in a cursory fashion along side formal verification: the exact
science of proving programs correct.

While I would not say that formal verification is the thrust of most
computer science departments, it is the theme: programs are graded on
correctness, and programs written by students are short, based on
well-known algorithms, and therefore can be feasibly proven correct.
In short, computer science students are taught the fine art of writing
perfect programs.

Some argue that computer science departments do not go far enough in
teaching how to programming perfectly.  Edgar Dijkstra was a thought leader
of this "programming is mathematics" camp.  He
[wrote extensively](http://www.cs.utexas.edu/users/EWD/) on program proving and assuring
[the reliability of programs](http://www.cs.utexas.edu/users/EWD/ewd03xx/EWD303.PDF) through the use of mathematics.  Here is a typical quote from
[EWD641](http://www.cs.utexas.edu/~EWD/transcriptions/EWD06xx/EWD641.html):


> The conclusion that competent programming required a fair amount of
> mathematical skills has been drawn on purely technical grounds and, as
> far as I know, has never been refuted.


I like to think of myself as a competent programmer, but I am lousy at
mathematics.  Dijkstra's observation disagrees with my
self-perception.  Am I really a competent programmer, or am I just
fooling myself?  Self-doubt starts with such statements, and grows
with each contradiction we encounter.  If Dijkstra were my faculty
advisor, he might have convinced me to choose another career.

My customers got lucky.  They are happy with my performance as a
programmer, and so are my fellow programmers.  We create imperfect
software from imperfect requirements.  I say this with some
trepidation.  There is always a nagging doubt that we could do better.
Perfectionism nags me, when I least expect it.

## Entrenched Perfectionism

Dijkstra was not one to shy away from moral imperatives:


> You must make the program in such a way that you can
> give convincing argument for its correctness.


You also cannot prove a program correct through testing:


> That program testing does not provide such a convincing case is well-known.


The student's psychological trap is set: you can write perfect
programs ("look how easy your assignments are!"). Do not waste your
time testing your programs.  Study your code like a mathematician
until you are sure it is perfectly correct.  Only then can the
software be
[used safely](http://www.cs.utexas.edu/users/EWD/transcriptions/EWD06xx/EWD627.html).

Dijkstra should not be held accountable for the psychological failings
of the way we teach programming.  Perfectionism is entrenched in our
teaching methodology and in the history of programming.  The tragedy
of perfectionism in our schools will be with us for a long time to
come.

There is hope.  Testing is in, because
[agile is in](http://www.google.com/search?q=agile+software).  The hype has allowed programmers to try testing and to consider
that testing is integrated quality assurance.  This is an excellent
start.  Programmers are motivated to test.

## Inductive Reasoning

Testing has been an integral part of my software development practices
for my entire professional career.  After I left grad school I landed
a job with some engineers who understood the value of testing.  That
didn't mean we had a conceptual framework to explain why we wrote
tests.  Commonsense drove our thinking more than anything else.

Before I started this essay, I hadn't looked at testing
psychologically -- as is often the case, I was sure I understood what
I was going to write, which isn't what you are reading now.  I knew I
wrote tests to help with problem decomposition, but why?  How does
testing help me decompose problems?  The following is an "Aha!"
experience for me as a result of those questions.

When a child touches a hot stove a number of times, he tends to think
all stoves are hot, and (hopefully!) approaches all stoves cautiously.
That's a reasonable (and safe) generalization.  The child and all
humans use this type of thinking, known as inductive reasoning or
inductive logic, instinctively.  It's how we learn.  All sabretooth
tigers (or animals which _look_like_ sabretooth tigers) are best kept
at a safe distance.

Inductive reasoning is the way we generalize our specific experiences.
Generalizations are useful at times, and can lead us astray other
times.  It's safe to generalize that stoves are hot.  However, it's
not useful to be so terrified of stoves that you cannot approach them.

This helps us see why Dijkstra is right for us to be wary of testing:
you cannot generalize a collection of test cases as a proof of a
program's correctness.  Tests can only prove a specific program
correctly transforms a specific and ordered set of inputs into a
specific output.  This result cannot be generalized into a proof of
correctness.  This does mean this specific result is worthless.

On the contrary, test results are _useful_ to programmers, just as any
empirical result is useful to a scientist.  The experiment teaches the
scientist something about a theory, and a programmer learns something
about a program from test results -- as long as the programmer does
not overgeneralize (overvalue) the meaning of the results.  That
inductive reasoning does not prove anything is besides the point.

## Deductive Reasoning

Test results are valuable _facts_.  We use facts to prove things about
a program.  If a stove feels warm, I can reason that this particular
stove is either on or was on recently.  I combine a fact (warmth) with
a theory (warm stoves are on) to produce a new theory (the stove is
on).  One fact does not prove this theory.  I can use it, however, to
ask another question ("Is the stove on?"), which can help confirm or
negate my theory ("No, I just turned it off.").

This kind of thinking is known as deductive reasoning: working with
facts and theories to produce other (useful) theories.  Programming is
a form of deductive reasoning. A program is a theory -- again I agree
with Dijkstra.  A program's inputs are facts.  Its output is a
theoretical result which negates or helps confirm the theory.

A test is therefore a way of reasoning about a theory of operation,
that is, how we expect the program to behave.  If the test fails, we
have a proof of incorrect behavior.  If the test passes, we can say
conclusively that the program processes this specific set of inputs
correctly.  This is a very important result for a very specific case,
and we can _reasonably_ assume our specific expectation is implemented
correctly.

We do not need to prove the program-theory correct in all cases.  We only
need to be sure the requirements we know about are satisfied.  As the
program-theory is used by real users, the program-theory will be refuted,
that is, bugs will be found.  To me, testability and refutability are
important attributes, dovetailing nicely with
[Karl Popper's Science as Falsification](http://www.stephenjaygould.org/ctrl/popper_falsification.html).  If we believe in Popper's Science, an irrefutable proof is of no value;
proofs only confirm what we want to believe is true.  Tests (or proofs of
contradiction) are valuable intrinsically, according to Popper, since they
_can_refute_ a program-theory.

Since a program-theory is
extremely complex, a specific test only refutes a specific path in the
program-theory.  Inductive reasoning allows us to backtrack: Refutation and
correction are the yin and yang of programming.  But this is not a
philosophical essay!  My conjecture is that tests are valuable.

## Reasonable Programs and Tests

In order to bolster this claim, I think it
would be useful to look at some code.  Here's one case from
USState.bunit, which tests the bOP module Bivio::Type::USState:

```text
unsafe_from_zip_code => [
    '06230' => 'CT',
],
```

With this case, can we conclude that the unsafe_from_zip_code method
is correct?  No.  Consider the following implementation which
satisfies this and any other test case whose output should be 'CT':

```text
sub unsafe_from_zip_code {
    return 'CT';
}
```

However, a _reasonable_ programmer would not implement
unsafe_from_zip_code this way.  It would be pointless -- except,
perhaps, as an example in a article or book about test-driven
programming.

Programmers do not cheat themselves.  If the goal is to write
unsafe_from_zip_code, a programmer would write some reasonable test
cases:

```text
unsafe_from_zip_code => [
    '00100' => [undef],
    '06230' => 'CT',
    '07001' => 'NJ',
    '08904' => 'NJ',
    10037 => 'NY',
    14925 => 'NY',
    52003 => 'IA',
    80022 => 'CO',
    81626 => 'CO',
    90001 => 'CA',
    96003 => 'CA',
    96150 => 'CA',
    96701 => 'HI',
    99999 => 'AK',
    abc => [undef],
    [undef] => [undef],
],
```

And, would write a reasonable implementation to satisfy those cases:

```text
sub unsafe_from_zip_code {
    my(undef, $zip) = @_;
    return $zip && $zip =~ /^(\d{3})/s ? $_MAP->[$1] : undef;
}
```

She might not fill out the values of $_MAP to satisfy all cases right
at the start.  The point would be to test the main algorithm: validate
$zip starts with three digits then look it up in $_MAP.  If the
algorithm contained a defect, we can safely conclude that this
reasonable set of test cases would demonstrate this result.  We cannot
prove this is so, but I would argue any reasonable programmer would
conclude that the above set of test cases was sufficient to judge the
correctness of the algorithm.

## Errors in Tests

A passing test does not mean the implementation is correct.  There was
an error in unsafe_from_zip_code when I first started this essay.
There was _also_ an error in the test cases.  The errant test case
was:

```text
undef => [undef],
```

The correct test case is now:

```text
[undef] => [undef],
```

This correct test case uncovered an annoying but non-critical bug.  A
warning message was output when $zip was undefined.  The
implementation still produced the correct output, but I wanted to
avoid filling up our error logs so I fixed it.  This was the
reasonable thing to do.

## Unknown Unknowns

Mathematicians do not like the term "reasonable".  It's imprecise.
You cannot build mathematically proven theories using imprecise
(imperfect) language.  Conversely, although programs are provably
precise, you cannot prove much about them that is useful.
Furthermore, not all proven mathematical theories are useful.  And,
what I think is quite important, a theoretical framework falls apart
if one its axioms or proofs is incorrect.

Scientists validate the usefulness of theories and the correctness of
theoretical frameworks through testing, a.k.a. experiments.  Since
programs are the most complex theoretical frameworks in existence, we
must test them.  It's insufficient and _unsafe_ to assume they are
correct based on any theoretical framework.  More importantly,
experiments help scientists come up with new and unexpected ideas
-- where would I be without sticky notes!

Tests both explain what we expect, and when they fail to confirm our
expectations, provide us a path towards learning new things about our
program and its environment (programming language, application
framework, operating system, etc.).  Tests teach us to expect the
unexpected.

## What a Fool I am

I used to have a boss who said, "we are all fools".  While this may
be demeaning, it is true.  In one way or another, we fool ourselves
as a coping mechanism.  I could not write this essay without fooling
myself that it will be a great work.  Lots of people have written
about testing.  Why should I bother to write more about it?

I could make money writing code instead of prose.  I can argue that it
will be useful to my co-workers as the sole reason for writing this
essay.  That would be another way of fooling myself.  The truth is
that one of the reasons for this essay is to get a bit of fame and glory.
My ego needs external validation.

That's a scary thought.  What if people read it and laugh silently, or
worse, criticize me publicly, or even call me a fool.  That's not a
coping mechanism for me.  Yikes!  My ego could not stand that.

I began this essay with some thoughts about why we fear testing.  The
above line of reasoning is exactly the same fear-based logic.  My ego
is strong enough to sustain the results of this particular test of
notoriety.  I have been publicly ridiculed before, and will be again.
That's the way my tormentor's ego protects itself, no matter how
uncivil this type of behavior is.  Or, in the words of the anonymous QA
person quoted earlier:


> Do unto others until they hate you


How uncivil, and how true.

## Software Testing Ethos 2.0

External validation is testing.  We fear it, even when we do it in the
privacy of our own office.  Yet it is _imperative_that_we_test_ our
programs and theories, just as a child must learn that some stoves are
hot and others aren't, and how he can learn to tell the difference
between them.  A child learns how to learn by testing.

Tests validate assumptions; tests expose us to the unknown.  Here be
dragons.  Courage is required.


