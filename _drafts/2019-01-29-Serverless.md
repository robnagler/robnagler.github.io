---
layout: post
title: "Serverless: Bits of History, Words of Advice"
date: 2019-01-29T12:00:00Z
---

[Serverless Computing](http://n99.us/zoy) is growing rapidly. I've
long been a fan of [stateless programming](http://n99.us/fyq) so I'm
happy to see Serverless taking off. I thought I'd chime in about the
parallels to [Transaction Process Monitors](http://n99.us/kyf), and
some advice from graybeards about how to build robust Serverless
systems.

> In a world full of retried messages, idempotence is an essential
> property for reliable systems. --
> [Pat Helland](http://n99.us/vfb)

When you
[search for Serverless Computing](http://n99.us/hxc),
you learn it is pay-as-you-go and *#NoOps*. However, the
big value of Serverless is the stateless programming model for which
the biggest win is more maintainable and reliable systems.
That discussion is lost in all the sales talk about cost savings,
which is irrelevant for most applications.

# Bits of History

Serverless requires idempotent functions. You have no choice about it,
and in the good old days, Transaction Process Monitors enforced the
same progamming model. For example,
[IBM's Transaction Processing Facility (TPF)](http://n99.us/caf) is
described on Wikipedia as follows:

> TPF is not a general-purpose operating system (GPOS). TPF's
> specialized role is to process transaction input messages, then
> return output messages on a 1:1 basis at extremely high volume with
> short maximum elapsed time limits.

Another example is Tandem's Transaction Monitoring Facility (TMF). The
[TMF Application Programming Interface](http://n99.us/toz) from 1989
states:

> A context-free server is a server that accepts a single message
> from a requester, performs a job, and issues a single reply message
> to respond to the requester. Once the reply message has been
> issued. the server has no state (or context) that may survive to be
> used in subsequent requests.

That's Serverless in a nutshell, and Transaction Process Monitors were
handling all the world's financial transactions in the 1980's and
1990's, and probably still in operation in many of the big financial
institutions.

In 1985, [Jim Gray](http://n99.us/ner) wrote
[Why Do Computers Stop and What Can Be Done About It?](http://n99.us/xdl)
in which he concluded:

> The implications of these statistics are clear: the key to high-
> availability is tolerating operations and software faults.

That's still true today, even for Serverless: software defects and
sysadmin errors are the major cause of system failures. However, Gray
rightly postulates that Heisenbugs are hard to find and:

> If the program state is reinitialized and the failed operation
> retried, the operation will usually not fail the second time.

This is what makes Serverless hard. It's easy when you are just doing
a basic [CRUD](http://n99.us/gsx) function. Anything more complex, and
you have the complexities of intermittent failures of your code and/or
third party services. With Serverless, there are no real guarantees
about the execution environment. It'll run on some server,
somewhere. Yes, it'll run in a configured container image, but you
don't get to control the operating system kernel or other services
used by the Serverless function.

# Words of Advice

In 2012 [Pat Helland](http://n99.us/hvz) wrote
[Idempotence Is Not a Medical Condition](http://n99.us/vfb), whose
purpose is:

> This article has sketched a few principles used by grizzled old-timers
> to provide resilience even when "stuff happens."

This was two years before AWS Lambda was launched, but the lessons are
timeless for idempotent operations:

> Some basic principles are:
> 
> * Every message may be retried and, hence, must be idempotent.
> * Messages may be reordered.
> * Your partner may experience amnesia as a result of failures, poorly
>   managed durable state, or load-balancing switchover to its evil twin.
> * Guaranteed delivery of the last message is impossible.
>
> Keeping these principles in mind can lead to a more robust application.

Amen.

Pat Helland also wrote
[TMF Application Programming Interface](http://n99.us/toz) (quoted
above), which contains this sage advice:

> 2.5 An important concept for the requester is that a
> BEGINTRANSACTION must always be paired with a matching
> ENDTRANSACTION or ABORTTRANSACTION. This is true even if the
> transaction is aborted by the system or by a server.

This key concept is missing from Serverless frameworks -- at least the
ones I've seen. Transactions should be *bracketed*, and the best way
is for the framework to do this. If it's not available to you,
create a wrapper for all your Serverless APIs that brackets all your
transactions.

When talking about reliable software, I have to mention
[Fail Fast](http://n99.us/uzj), which was also mentioned
in [Jim Gray's report](http://n99.us/xdl) (above):

> The process approach to fault isolation advocates that the process
> software module be fail-fast, it should either function correctly or
> it should detect the fault, signal failure and stop operating.

To learn more about Fail Fast, 
[read Jim Shore's excellent article](http://n99.us/dts),
which will allow you to "Eliminate the debugger". With Serverless, you
won't have one when you need it, anyway.

Serverless is going to be huge, because that's the way transaction
processing systems have been built for decades.  Transaction
Bracketing and Fail Fast are definitely key techniques to make your
Serverless systems robust. I also highly recommend you familiarize
yourself with Transaction Process Managers to help you avoid the
[Heisenbugs](http://n99.us/gth) that stopped the systems Jim Gray
investigated 35 years ago.
