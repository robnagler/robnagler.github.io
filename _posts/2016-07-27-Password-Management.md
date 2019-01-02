---
layout: post
title: "How to Safely and Easily Manage Passwords"
date: 2016-07-27T12:00:00Z
---


> Too many damn passwords! -- You


Every site these days has a password. You can't remember them all so
what do you do?
Use a
[Password Manager](https://en.wikipedia.org/wiki/Password_manager) such as
[LastPass](https://lastpass.com) or
[1Password](https://1password.com). I use LastPass. However, I take quite a few precautions, which I explain
below.

## Use a Completely New Email Address

The first step with any password manager is creating an account. It's
crucial you create a special and highly confidential email address for this
purpose. This particular email address can be used to recover the
password for your password manager account:

![LastPass Recover Account](/assets/i/lastpass-recover-account.gif)

If you use your regular email address,
[it's likely it can be cracked](http://www.onlinehashcrack.com/how-to-crack-gmail-yahoo-hotmail-account-the-truth.php), and with that information, your password manager account will be cracked as well.

It's very easy to create a new email address on a free email provider
like
[mail.com](http://mail.com),
[Hushmail,](http://hushmail.com)etc. Make sure this completely new email is not easily guessable. Make the password
for the account long, because you won't have to use it much.  Give random answers for the secret questions so that if
someone gets your email, they can't use information about you to crack the account.
Write down the new email, password, and random security answers and store in a secure
location.

Even if you use
[Two Factor Authentication](https://en.wikipedia.org/wiki/Multi-factor_authentication), you can
[disable it](https://lastpass.com/support.php?cmd=showfaq&id=7066) with just your email address. This is why I say you should not bother with multi-factor
authentication: it's
[Security Theater](https://en.wikipedia.org/wiki/Security_theater) when it can be
[so easily circumvented](https://www.wired.com/2016/06/deray-twitter-hack-2-factor-isnt-enough/).

## Pick a Relatively Long Password

Now you can register with LastPass. You will also choose a password for LastPass.
This should be over 12 characters and easy to type especially on a mobile device.
Mix lower and upper case and throw in a few numbers and perhaps a space.
If you use an iPhone, you might want to avoid special characters, because
they are hard to type.

Write down the password and store it in a secure place. It's very important
that you don't lose your password, because I recommend against using a
[Security Email](https://lastpass.com/support.php?cmd=showfaq&id=2465) to allow your account to be recovered. The goal is to make it so no one
can recover your password from any email except the very secure email
address you chose above.

## Install Browser Plugin and Mobile App

Once you've created your account on the LastPass site, you'll want
to download the app and the browser plugin for your laptop. You'll
need to know how to download a browser plugin/extension. There's a long list
so best to go to the
[LastPass Download page](https://lastpass.com/misc_download2.php) to figure out how to do this.

To use LastPass on your phone, you need to pay for the Premium version.
It's only $12 a year so just do it. Just go to your mobile device's app store.
If you don't know how to do this, the
[LastPass Download page](https://lastpass.com/misc_download2.php) covers this as well.

## Configure Account Settings

You now need to configure these programs.
LastPass is a weird in that there is a
[Browser Preferences](https://helpdesk.lastpass.com/extension-preferences/) and a
[Account Settings](https://helpdesk.lastpass.com/account-settings/). You have to configure both. Account Settings are global to all
devices. Browser Preferences are per device.

To configure Account Settings, go to your LastPass Vault, which should
be located in the browser toolbar, e.g. something like this:

![LastPass Select Vault](/assets/i/lastpass-select-vault.gif)

I've circled the LastPass logo in my browser's toolbar to show you where to click.
It's very important that whenever you interact with LastPass in your browser
that you use this logo. It's a bit difficult to explain, but it's important that you
aren't tricked by malicious websites to enter your LastPass login and password
unless you have initiated the login. LastPass won't prompt you for your password
until you click on the logo in the toolbar, especially if you follow the configuration
guide below.

Once you click on the logo, you'll be asked to login. After you login once, you'll
want to click on My Vault to configure the Account Settings. Once in the vault,
there's a "gear" icon to get to your Account Settings. On the Account Settings
page, you'll want to turn off all email subscriptions so scroll to Account Information
and click on Email Subscriptions:

![LastPass Email Subscriptions](/assets/i/lastpass-email-subscriptions.gif)

This will popup a new window or tab, and you'll select the "Never" link box at the
bottom of the list, and click Update:

![LastPass Email Never](/assets/i/lastpass-email-never.gif)

The fewer email interactions you have with LastPass, the better. If you need
to know something, just go to the LastPass Vault. This avoids issues with
phishing and other types of attacks.

That's all for Account Settings.

## Browser Preferences

To eliminate potential phishing attacks from malicious sites, you should disable
all interactions in the browser window itself. You only want to interact with
the toolbar or popups you explicitly initiate from the toolbar, for example,
opening the Vault.

When you click on the LastPass icon in the browser toolbar, select the "Preferences"
in the menu:

![LastPass Select Preferences](/assets/i/lastpass-select-preferences.gif)

The first section is "General", and you'll want to setup the Automatic Logout to both
logout when all browsers are closed as well as after an idle timeout. I recommend 15 minutes,
but shorter is better:

![LastPass Automatic Logout](/assets/i/lastpass-automatic-logout.gif)

In the General section, disable highlighting of input boxes and do not automatically fill
login information:

![LastPass Autofill](/assets/i/lastpass-autofill.gif)

Under the General Appearance section, you should hide context menus:

![LastPass Hide Context](/assets/i/lastpass-hide-context.gif)

Now click on "Notifications" and disable all but the "Toolbar" options as follows:

![LastPass Notifications](/assets/i/lastpass-notifications.gif)

Finally, don't forget to click the Save button.

I haven't gone into the mobile app configuration. It's the same except you don't
want to enable "autofill of apps", which is something LastPass doesn't do well.

## Remember Toolbar Only

That's the LastPass configuration I recommend. If you have other suggestions,
I would be happy to hear them.

Make sure you keep your LastPass browser plugins and mobile apps up to date. If
you set auto-update, this should do it automatically for you.

And, just to make sure I made myself clear: Always click on the icon in the Browser
Toolbar. On your phone, always go to the LastPass app explicitly to make sure
you aren't being tricked by another app.


