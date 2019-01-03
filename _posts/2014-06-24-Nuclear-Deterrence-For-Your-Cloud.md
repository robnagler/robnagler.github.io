---
layout: post
title: "Nuclear Deterrence For Your Cloud"
date: 2014-06-24T12:00:00Z
---

"Code Spaces will not be able to operate beyond this point."  That's not
something you want to tweet.  Or this, "The group responsible for the DDOS
are trying to get us to pay them to stop, and are claiming that they have
found a security breach and..."
[An article in The Register](http://www.theregister.co.uk/2014/06/18/code_spaces_destroyed/) provides more details, but the headline says it all:
"Code Spaces goes titsup FOREVER after attacker NUKES its Amazon-hosted data".

I've been afraid of cloud vaporizations since 2011. We operate our cloud
much more securely than Code Spaces as a result.  I'll give an overview
of how we protect our cloud infrastructure later in this article.  First, I want
to address the incorrect headline.

If the attacker nuked Code Spaces, nothing would have been left.  As I
understand the situation, the attacker used a simple, slow torture approach:
"[the attacker] proceeded to randomly delete artifacts from the panel".
This took 12 hours according to the ^codespaces.com home page.  The
attacker's purpose was to extort Code Spaces so using nukes was not an option.

With a collection of physical servers distributed across several data centers,
there is no nuclear option, except real nukes, for which the business continuity
plan is left as an exercise for the reader.
In the virtual server world, you can destroy all your
servers with a few clicks of the mouse.

Your eyes already flew down to this Big Red Button:

![Amazon Close Account](/assets/i/amazon-close-account.png)

You get here by going to "My Account" and clicking on "Close Account", which
you can see grayed out in the image above.  You do have to click the checkbox
as a deterrent for fools and nobody else.  Unbelievably, Amazon doesn't ask
you to re-authenticate.  Your business is gone in 60 seconds.

To be fair to Amazon, all virtual server providers have this option.  It saves
a lot of time for customer support.  Many people
play around with cloud services and want a "do over" before
they get their virtual configuration set up right.

Close account in this context makes sense.  However, you should have the
option of turning off this option.  (Another important feature would be to
rate limit destruction with an exponential shaping function.)   I have asked
other, smaller virtual server providers this question, and none were interested
in providing this option.

For now, the Big Red Button is real threat.  Once you click it,
you'll get this message:

![Amazon Account Closed](/assets/i/amazon-account-closed.png)

This type of message is very appropriately called
[a toast notification]("http://en.wikipedia.org/wiki/Toast_(computing)"), which your servers and backups are at this point.

## Close Account Is Irreversible

To recap, your business can be irreversibly destroyed
from a web browser, which is logged into Amazon Web Services
by clicking on My Account > "I understand ..." > Close Account > Close Account.
No password required.

## Step One: Protect Your Email Address

I hope I have your attention.  (If not, why are you reading this sentence?)

If you forget your password, Amazon will helpfully email you a new one:

![Amazon Check your e-mail](/assets/i/amazon-check-email.png)

This means anybody with access to your email account will be able to get
into your Amazon Web Services
account.  These are the same credentials, by the way, which you use to buy
books, movies, and
[Rolaids](http://www.amazon.com/dp/B00E68O1A2).

Do not use your corporate email.  Do not use your personal email.  Create
a separate email account just to access your Amazon Web Services account.

Do not login to this email from your normal browser.  Reset the browser
completely after logging into this email account or Amazon's console.
Do not forward emails from this account.  Don't add a "secondary email"
for this email account.  Don't add "Alternate Contacts" to your
Amazon account.

Tell no one except the absolutely most privileged people in your
company about this email.
Avoid logging into Amazon's console with this email unless absolutely
necessary, and only login from a computer you know is secure (another
exercise for the reader).

Aye, sir! Mum's the word.

## Step Two: Enable Multi-factor Authentication (MFA)

Amazon allows you to setup
[Multi-Factor Authentication devices](http://aws.amazon.com/iam/details/mfa/) on your account.

As of this writing, AWS Virtual MFA on my Samsung S5 shows this
unhelpful message:

![AWS Virtual MFA Boot Screen](/assets/i/aws-virtual-mfa-bootstrap.png)

[Download Google Authenticator](https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2&hl=en) instead.

Better yet,
[buy a dedicated Gemalto multi-factor authentication device](http://onlinenoram.gemalto.com), and lock it in a safe.

The rest of the multi-factor authentication setup is left as an exercise.

## Step Three: Secret Questions

Secret questions are a necessary evil.  Without them, Amazon customer support
will ask even dumber questions like "what's the last four digits of your
credit card" before letting an attacker close your account.

When you setup your secret questions on your Amazon account,
treat them just like your password: make them very secure.  They need
to be pronounceable, but they don't need to be real words.  Make up some
gibberish.
[Here's a generator](http://thinkzone.wlonk.com/Gibber/GibGen.htm), which does a reasonable job (select level 3).

Again, lock these secret questions in a bank vault, not the safe where
you keep your Gemalto device.  It's better to have to wait a day or two to
get back into your Amazon account after your multi-factor authentication
device breaks than to have the answers to your secret questions fall into
the wrong hands.  Remember that the answers let you bypass your
multi-factor authentication system.

## Step Four: The Usual Stuff

Steps one to three should be an effective nuclear deterrent.  If I missed
something, please let me know!

The Code Spaces attacker didn't go nuclear, and that was lucky for them.
It does sound like the attacker had access to their Amazon root account.  While
the nuclear option (close account) is the fastest way to destroy your
business, it's not the only way.  Ordinary (non-root) users can be
configured to destroy server instances, destroy backups, and so on.

Try to design a system that
requires access to two (or more) accounts to destroy everything.  I'm not
an Amazon Web Services expert so I'll stop here.  If you are one,
drop me a line.

We have to design our systems so they can survive in a world
with high entropy.  Cloud providers should give us the option to
disable the close account button.  I don't want to read about
another company being destroyed by an attacker, especially one
that used that Big Red Button.

To the Code Spaces team: My heart goes out to you all.
I apologize in advance if anything in this article offends you.
My goal was to use the tragedy to prevent another one.
Thank you for being transparent about what
happened so that we can all do better.


