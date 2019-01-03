---
layout: post
title: "Risk as the Fourth Variable in Extreme Programming"
date: 2003-06-15T12:00:00Z
---

[[Originally posted to Extreme Programming at Yahoo! Groups](http://tech.groups.yahoo.com/group/extremeprogramming/message/75026)]

This note addresses the four variables: time, scope, resources and
quality. The fourth variable quality has been described as "strange"
and non-linear. I think the problem is that it isn't a variable at
all. Rather, quality is a measurable output value, not a controllable
input variable. Risk is the fourth input variable that can be
controlled by the customer.

When time, scope, and resources are defined, the risk of failure is
constrained. And, that's the best you can do. Plenty of projects
have succeeded with reasonably high quality despite shoestring budgets
and unreasonable scope expectations. They are clearly in the
minority, but you don't guarantee failure by unreasonably constraining
the first three variables. You increase the risk, and being the
customer, that's your prerogative. If you want to decrease risk, you
reduce scope. Increasing time decreases implementation risk, and
increases time-to-market risk. Increasing or decreasing resources is
more complicated, but changing resources affects risk whereas it may
have no affect on quality.

The customer models risk to gauge a project's chance of success. The
risk model is usually implicit, but it's as real as the implicit
models programmers use to estimate stories and tasks. One of the
factors in a risk model is historical quality. For most customers,
historical quality boils down to: team A produces better software than
team B, so let's go with team A. As XPers, we can help our customers
do better.

Many people measure quality in terms of MTBF[1] and MTTR[2]. (This is
not internal quality, which I discuss briefly below in [3].) However,
the meaning of F (failure) and R (repair) is often fuzzy and
incomplete. With XP stories, we have an accurate and complete
measure.

I consider a failure to be any event that results in a story--be it
fixing a defect, adding documentation, or enhancing the system.
Failure is failing to meet an expectation. (This may happen multiple
times before the story is implemented, and I'm not exactly sure how to
integrate that data, but counting stories is a reasonable starting
starting point. Another measure of quality is to count defects
instead of failures.) Time to repair is the elapsed time it takes to
deliver a story's implementation. These numbers are readily available
for an XP project, and define quality for its entire life.

With this definition of quality, the customer has practical data about
an XP project's quality at any point in time. That is, the customer
has an actual number instead of a "feeling" which can be used to
refine her risk model for future releases and projects. Quality can't
be guaranteed, but historical quality data allow the customer to
better understand and control the relationship between the four
variables: time, scope, resources, and risk.

[1] MTBF is Mean Time Between Failures

[2] MTTR is Mean Time To Repair

[3] Internal quality is just increased scope. Ron Jeffries says this
at ^http://c2.com/cgi/wiki?FourVariables. Ideally, all work is on
story cards, and that should include the time to refactor,
i.e. increase internal quality. If you don't like that, reduce
resources by X% to account for the implicit work involved in
refactoring. Either way, internal quality is a subjective measure
that probably influences external quality (MTBF and MTTR) but
cannot guarantee a particular value of MTBF and/or MTTR. If it
could, we found the silver bullet to ensuring external quality for
every single project, not just improving the average.


