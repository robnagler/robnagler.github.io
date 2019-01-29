---
layout: post
title: "Serverless: Bits of History"
date: 2019-01-29T12:00:00Z
---

[Serverless Computing](https://en.wikipedia.org/wiki/Serverless_computing)
is growing rapidly. I've long been a fan of
[stateless programming](https://www.extremeperl.org/bk/its-a-smop)
so I'm happy to see this programming trend where stateless
functions are invoked on demand.

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
