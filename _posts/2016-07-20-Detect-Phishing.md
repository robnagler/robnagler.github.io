---
layout: post
title: "How To Detect Phishing Emails"
date: 2016-07-20T12:00:00Z
---


> [Phishing](https://en.wikipedia.org/wiki/Phishing)>  is the attempt to acquire sensitive information such as usernames, passwords, and credit card details (and sometimes, indirectly, money), often for malicious reasons, by masquerading as a trustworthy entity in an electronic communication. -- Wikipedia


Phishing emails are getting more difficult to detect. If you have a public email
address, you will be approached by the general public. Here is an example:

![Intro email](/assets/i/phishing-intro-email.gif)

The target (recipient) of this phishing attack is a real estate agent so the
email contains enough information to make the email appear legitimate. This
is what makes this type of attack so dangerous. Most phishing attacks
are obvious, because someone is asking you for your bank account or
some other information in the first email. In this case, the attacker is
not asking for any information. The purpose is to engage the target
in a conversation.

The person's name and English are non-native. You don't want to appear
rude or xenophobic so you respond politely. The person already has your
email address so you won't be giving anything away if you do so you
reply. The response to your reply looks like this:

![Phishing email](/assets/i/phishing-hover-link.gif)

The attacker has the target engaged, and the response might be
legitimate in the context of a real estate transaction. However, the
insistence of clicking on a link from "Google Docs" is the telltale
sign of phishing.

Normally, some would would attach a PDF to the email. It's unusual
to share such a small file (a letter) via Google Docs or other file
sharing service. The goal here is to get someone to click on the link,
which is illegitimate.

## Hover over links

How do you know the link is dangerous? When you hover your mouse
over the link, it shows an address at the bottom of your browser
window. In the image above, I've highlighted this box in red. You
can see the web address is:

```text
herdinitiative.org/herdinitiativetest/document/googledoc3/
```

If this were a link to Google Docs, the link would look something like:

```text
docs.google.com/document/d/14JfWScOSTi...
```

Note that the first part of the address is *docs.google.com*. This
is a safe address.

At this point, you know the link is not what you expect so you
wouldn't click on it. Sometimes attackers will make fake names like
*docs.goog1e.com*, which looks almost right. This is sometimes
tricky to see so you might click on the link.

## Never enter information

Let's assume you clicked on the link. This is what you'd see:

![Phishing site](/assets/i/phishing-site.gif)

Now you know for sure that this is a phishing attack: the site
is asking for your Google login and password.

You should *never* enter information on unsolicited links or from
someone whom you do not know. You don't know this person, and
the person sent you a link.

## Verify unsolicited links and identities

Even if you get an email with an unsolicited
link from someone you know, you should contact them to verify that the
email was not sent from a virus. This is fairly common, and the
attacks are usually obvious. However, you really never know.
The important point is that the link is unexpected. If
the page the link points to is asking for information, that's a
big red flag.

That's probably the most important advice: links in emails
should be coupled to an exchange with someone known to
you. If not, just don't click.
