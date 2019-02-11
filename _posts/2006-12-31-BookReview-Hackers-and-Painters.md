---
layout: post
title: "BookNotes: Hackers and Painters: Big Ideas from the Computer Age"
date: 2006-12-31T12:00:00Z
---
By Paul Graham, O'Reilly Media, Inc., May 2004, 0596006624

Paul Graham compares hacking to painting in that hacking is an art
of munging code continuously, and painting was not able to do this
until the invention of oil paints.  The Renaissance created great
painters, because they finally had a great medium to paint with.
The book consists of articles from his website.  In some sense, it may
not be worth buying, but it does come together nicely, and it is handy
to hold.

Graham is an eloquent writer.  Yet, he is often immature or naive;
I'm not sure which.  "Most adults, likewise, deliberately give kids a
misleading view of the world."  To me, we limit a child's world so
children can assimilate its complexity, not because we want to mislead
children.  Our goal is to teach, just like we teach Newtonian
mechanics as if it were the "whole truth", we let children believe in
myths to allow their moral sense and view of the world to develop
slowly with their slowly developing brain.

On the programming side, Graham does not feel that testing is all
that important.  "[At Viaweb, there was no protection against breakage
except the fear of looking like an idiot to one's peers, and that was
more than enough." Repeatable regression testing is what makes software
fungible.  If you don't have a way to testing your past assumptions,
you don't know if you broke any of them.  It seems to me that Graham
hasn't maintained many systems over a long enough period of time.

Here's another example: "In hacking, like painting, work comes in
cycles."  This is silly.  I perform consistently unless I'm scared.
When I'm scared, it's due to a psychological issue, not a complex
problem.  I've learned over time to recognize when I'm afraid and,
more importantly, to accept it.  My next step is to address the issue
head on.

Graham goes on to say that he saves up little tasks for those
periods when he is uninspired, e.g. debugging.  "I like debugging:
it's the one time that hacking is as straightforward as people think
it is."  Most programmers are afraid of debugging.  Indeed, I was once
laughed at by a room full of about 400 programmers who thought I was
crazy when I said debugging was the easy part.

When Graham is inspired, he is in flow, and fear is not a factor.
Flow is extremely important, and I've learned that the best way to get
into flow is to take a step in any direction.  Then I take another,
and another, and soon, I'm back in flow again.

This is not about cycles, rather it is about learning to overcome
your fears.  Cycles are not mythical boogeymen that come out of
nowhere.  And, I bet, when Graham is inspired, he may also be driven
by fear, that is, the fear he has to work 16 hours in a row or he'll
lose his flow or worse, lose the idea completely.  This would surely
be a sign of a deeper psychological issue lurking in the shadows.

That being said, Graham is a master of rhetoric, and the book is a
fun read.


> [p24] The other problem with startups is that there is not much
> overlap between the kind of software that makes money and the kind
> that's interesting to write. Programming languages are interesting to
> write, and Microsoft's first product was one, in fact, but no one will
> pay for programming languages now. If you want to make money, you tend
> to be forced to work on problems that are too nasty for anyone to
> solve for free.



> All makers face this problem. Prices are determined by supply and
> demand, and there is just not as much demand for things that are fun
> to work on as there is for things that solve the mundane problems of
> individual customers.



> [p29] Great software, likewise, requires a fanatical devotion to
> beauty.  If you look inside good software, you find that parts no one
> is ever supposed to see are beautiful too. When it comes to code I
> behave in a way that would make me eligible for prescription drugs if
> I approached everyday life the same way. It drives me crazy to see
> code that's badly indented, or that uses ugly variable names.



> If a hacker were a mere implementor, turning a spec into code, then he
> could just work his way through it from one end to the other like
> someone digging a ditch. But if the hacker is a creator, we have to
> take inspiration into account.



> In hacking, like painting, work comes in cycles. Sometimes you get
> excited about some new project and you want to work sixteen hours a
> day on it. Other times nothing seems interesting.
> q  To do good work you have to take these cycles into account, because
> they're affected by how you react to them. When you're driving a car
> with a manual transmission on a hill, you have to back off the clutch
> sometimes to avoid stalling. Backing off can likewise prevent ambition
> from stalling. In both painting and hacking there are some tasks that
> are terrifyingly ambitious, and others that are comfortingly
> routine. It's a good idea to save some easy tasks for moments when you
> would otherwise stall.



> In hacking, this can literally mean saving up bugs. I like debugging:
> it's the one time that hacking is as straightforward as people think
> it is. You have a totally constrained problem, and all you have to do
> is solve it. Your program is supposed to do x. Instead it does
> y. Where does it go wrong? You know you're going to win in the
> end. It's as relaxing as painting a wall.



> [p30] As far as I know, when painters worked together on a painting, they
> never worked on the same parts. It was common for the master to paint
> the principal figures and for assistants to paint the others and the
> background. But you never had one guy painting over the work of
> another.



> I think this is the right model for collaboration in software
> too. Don't push it too far. When a piece of code is being hacked by
> three or four different people, no one of whom really owns it, it will
> end up being like a common-room. It will tend to feel bleak and
> abandoned, and accumulate cruft. The right way to collaborate, I
> think, is to divide projects into sharply defined modules, each with a
> definite owner, and with interfaces between them that are as carefully
> designed and, if possible, as articulated as programming languages.



> [p31] Most makers make things for a human audience. And to engage an
> audience you have to understand what they need. Nearly all the
> greatest paintings are paintings of people, for example, because
> people are what people are interested in.



> Empathy is probably the single most important difference between a
> good hacker and a great one. Some hackers are quite smart, but when it
> comes to empathy are practically solipsists. It's hard for such people
> to design great software [5], because they can't see things from the
> user's point of view.



> [p32] You need to have empathy not just for your users, but for your
> readers. It's in your interest, because you'll be one of them. Many a
> hacker has written a program only to find on returning to it six
> months later that he has no idea how it works. I know several people
> who've sworn off Perl after such experiences.



> [p40] Most adults, likewise, deliberately give kids a misleading view
> of the world. One of the most obvious examples is Santa Claus. We
> think it's cute for little kids to believe in Santa Claus. I myself
> think it's cute for little kids to believe in Santa Claus. But one
> wonders, do we tell them this stuff for their sake, or for ours?



> [p69] At Viaweb, as at many software companies, most code had one
> definite owner. But when you owned something you really owned it: no
> one except the owner of a piece of software had to approve (or even
> know about) a release. There was no protection against breakage except
> the fear of looking like an idiot to one's peers, and that was more
> than enough. I may have given the impression that we just blithely
> plowed forward writing code. We did go fast, but we thought very
> carefully before we released software onto those servers.



> [p95] For most people the best plan probably is to go to work for some
> existing company. But it is a good idea to understand what's happening
> when you do this. A job means doing something people want, averaged
> together with everyone else in that company.



> Working Harder



> That averaging gets to be a problem. I think the single biggest
> problem afflicting large companies is the difficulty of assigning a
> value to each person's work. For the most part they punt. In a big
> company you get paid a fairly predictable salary for working fairly
> hard. You're expected not to be obviously incompetent or lazy, but
> you're not expected to devote your whole life to your work.



> [p100] Steve Jobs once said that the success or failure of a startup
> depends on the first ten employees. I agree. If anything, it's more
> like the first five. Being small is not, in itself, what makes
> startups kick butt, but rather that small groups can be select. You
> don't want small in the sense of a village, but small in the sense of
> an all-star team.



> [p102] If you can develop technology that's simply too hard for
> competitors to duplicate, you don't need to rely on other
> defenses. Start by picking a hard problem, and then at every decision
> point, take the harder choice.



> [p105] Venture capitalists have a list of danger signs to watch out
> for. Near the top is the company run by techno-weenies who are
> obsessed with solving interesting technical problems, instead of
> making users happy. In a startup, you're not just trying to solve
> problems. You're trying to solve problems that users care about.



> [p167] In practice, writing programs in an imaginary hundred-year
> language will work to varying degrees depending on how close you are
> to the core. Sort routines you can write now. But it would be hard to
> predict now what kinds of libraries might be needed in a hundred
> years. Presumably many libraries will be for domains that don't even
> exist yet. If SETI@home works, for example, we'll need libraries for
> communicating with aliens. Unless of course they are sufficiently
> advanced that they already communicate in XML.



> At the other extreme, I think you might be able to design the core
> language today. In fact, some might argue that it was already mostly
> designed in 1958.



> [p191] In fact, choosing a more powerful language probably decreases
> the size of the team you need, because (a) if you use a more powerful
> language you probably won't need as many hackers, and (b) hackers who
> work in more advanced languages are likely to be smarter.



> [p192] If you start a startup, don't design your product to please VCs
> or potential acquirers. Design your product to please the users. If
> you win the users, everything else will follow. And if you don't, no
> one will care how comfortingly orthodox your technology choices were.



> [p195] As an illustration of what I mean about the relative power of
> programming languages, consider the following problem. We want to
> write a function that generates accumulators-- a function that takes a
> number n, and returns a function that takes another number i and
> returns n incremented by i. (That's incremented by, not plus. An
> accumulator has to accumulate.)



> In Common Lisp this would be



> ```lisp
> (defun foo (n)
>   (lambda (i) (incf n i)))
> ```


 In the book, he includes a Ruby example here "it's almost
identical", but I took the text from his website, which was written in
May 2002, when Ruby wasn't popular -- falling a bit into the trap,
he is trying to tell us not to fall into.


> [p195] and in Perl 5,



> ```perl
> sub foo {
>     my($n) = @_; sub {$n += shift}
> }
> ```



> which has more elements than the Lisp version because you have to
> extract parameters manually in Perl.



> [p213] Users are a double-edged sword. They can help you improve your
> language, but they can also deter you from improving it. So choose
> your users carefully, and be slow to grow their number. Having users
> is like optimization: the wise course is to delay it. Also, as a
> general rule, you can at any given time get away with changing more
> than you think. Introducing change is like pulling off a bandage: the
> pain is a memory almost as soon as you feel it.


 The above is from an earlier essay (2001) than his other essays about
users.  It seems to me he is contradicting himself about users, but
his opinion may have changed.  The next quote is from 2003, and he
seems to think that users are essential to good design, not an
optimization.


> [p217] This focus on the user is a kind of axiom from which most of
> the practice of good design can be derived, and around which most
> design issues center.



> [p219] In the software world, this idea is known as Worse is
> Better. Actually, there are several ideas mixed together in the
> concept of Worse is Better, which is why people are still arguing
> about whether worse is actually better or not. But one of the main
> ideas in that mix is that if you're building something new, you should
> get a prototype in front of users as soon as possible.



> The alternative approach might be called the Hail Mary
> strategy. Instead of getting a prototype out quickly and gradually
> refining it, you try to create the complete, finished, product in one
> long touchdown pass. As far as I know, this is a recipe for
> disaster. Countless startups destroyed themselves this way during the
> Internet bubble. I've never heard of a case where it worked.
> 



