---
layout: post
title: "Serverless: Bits of History, Words of Advice"
date: 2019-01-29T12:00:00Z
---

[Serverless Computing](http://n99.us/zoy)
is growing rapidly. I've long been a fan of
[stateless programming](http://n99.us/fyq)
so I'm happy to Serverless taking off. I just thought I'd
chime in about the parallels to Transaction Process
Monitors, and the lessons to be learned from them.

When you
[search Serverless Computing](http://n99.us/hxc),
you learn it is pay-as-you-go and *#NoOps*. However, the 
big value of Serverless is the stateless programming model,
which improves makes code more maintainable and reliable
as well as scalable and deployable. That discussion is lost in all
the sales talk about cost savings, which is irrelevant for
most applications.

> In a world full of retried messages, idempotence is an essential
> property for reliable systems. -- [Pat Helland](http://n99.us/vfb)
from: Idempotence Is Not a Medical Condition

Serverless requires idempotent functions. 

DON’T TALK AND LISTEN AT THE SAME TIME
Allowing it to depart before the transaction commits may open up the
possibility of the message being sent but the transaction aborting.

This article has sketched a few principles used by grizzled old-timers
to provide resilience even when “stuff happens.” In most cases, these
programming techniques are used as patches to applications when the
rare anomalies occur in production. As a whole, they are not spoken
about too often and rarely crop up during testing. They typically
happen when the application is under its greatest stress (which may be
the most costly time to realize you have a problem).

Some basic principles are:

* Every message may be retried and, hence, must be idempotent.
* Messages may be reordered.
* Your partner may experience amnesia as a result of failures, poorly
  managed durable state, or load-balancing switchover to its evil
  twin. 
* Guaranteed delivery of the last message is impossible.

Keeping these principles in mind can lead to a more robust
application.



Back in the 1960's, companies realized they had to solve the scaling
problem so they created 
Back in the 1970's, people figured out that statelessness was a
good thing. By the 1980's statelessness was normal. 

there were several OLTP systems 


. All the state resides in a database,
and the serverless functions that execute should be idempotent.
That's a key factor for scaling.

In the 1980's [OLTP](http://n99.us/evw) systems 

see this programming trend where stateless
functions are invoked on demand.

# Background

TODO:

* Serverless vendor locking and version churn https://news.ycombinator.com/item?id=19083713
* Semantic version myth https://news.ycombinator.com/item?id=19084280

http://www.hpl.hp.com/techreports/tandem/TR-89.3.pdf
The TMF Application Programming Interface
Pat Helland
2.5 An important concept for the requester is that a BEGINTRANSACTION must
always be paired with a matching ENDTRANSACTION or
ABORTTRANSACTION. This is true even if the transaction is aborted by
the system or by a server.

3. A context-free server is a server that accepts a single message from a requester, performs a job, and issues a single reply message to respond to the requester. Once the reply message has been issued. the server has no state (or context) that may survive to be used in subsequent requests. A c o n t e x t - sensitive server is a one that engages in a multiple message dialogue with the requester. In between messages, the context-sensitive server retains some state information.

jim gray http://www.hpl.hp.com/techreports/tandem/TR-85.7.pdf
Why Do Computers Stop and What Can Be Done About It?

[p16] Fault containment through fail-fast software modules.
The process approach to fault isolation advocates that the process software module be fail-fast, it should either function correctly or
it should detect the fault, signal failure and stop operating.

[p27] Communications lines are the most unreliable part of a distributed computer system.


What's interesting to me is how no one seems to remember that
the stateless function paradigm was popular several decades ago
in systems built executed by a
[Transaction Process Monitor](http://wiki.c2.com/?TransactionProcessingMonitor).
For example,
[IBM's Transaction Processing Facility](https://en.wikipedia.org/wiki/Transaction_Processing_Facility)
is described on Wikipedia as follows:

> TPF is not a general-purpose operating system (GPOS). TPF's
> specialized role is to process transaction input messages, then
> return output messages on a 1:1 basis at extremely high volume with
> short maximum elapsed time limits.

Compare that to the definition of Function as a Service

similar to large data problem, context id was passed along:
https://serverless.com/blog/api-gateway-websockets-support/
websockets are handled by the API Gateway

The flow will be different in that model than in the two tier application model:
The client side application invokes a "service" with data marshaled in the appropriate format; that means that the client application has some knowledge of:
The TPM remote invocation language (probably a client middleware stack embedded into the client application),
Or the knowledge of a "generic" way to call the TPM services through "standard" protocols (such as LU6.2, RPC, RMI/IIOP, proprietary formats, WSDL, etc.);
The TPM chooses (commonly some kind of intelligent TPM agent) what process will handle the query (based on certain criteria such as addressing or load balancing concerns);
The TPM processes unmarshals the message and calls back the application code;
The application code does its stuff in the database and possibly commit or rollback the transaction;
The TPM process can commit or rollback the transaction as well (when the TPM is configured to handle the database resource manager, the TPM commits or rollbacks);
The answer is wrapped back in the appropriate format and sent back the the client application.
Right after the answer, the same TPM process can:
Process another transaction (note that the TPM process is not suppose to "remember" something about the previous transaction - so the model is basically stateless);
Get a clean context for the application code to run again.
Other TPM services
There are several other potential services provided by the TPM:
Coordination of resource managers (typically a database engine, a transactional file engine, a queue system, coordinated one by one or all together in XA standard, etc.);
Load-balancing and spawning of new TPM processes in case they are needed (dynamic workload management, process restart in case of core dump),
Security access to services,
Routing services (very often, the notion of "domain" is used),
Wrapping and unwrapping respectively data messages into messages and the messages into data structures,
Monitoring for operations,
Protocol stack management,
Quite often "Queue to queue" guaranteed delivery services,
Error handling (such as process restart).
Some specific TPM can provided advanced services such as:
Hot failover (even under high traffic) running in multi-nodes contexts,
Secured and audit-able transaction journal (for applications where one single transaction shall not be lost).


the history of stateless computing.
functions is a new

Transaction managers
Tandem Pathway explanation
