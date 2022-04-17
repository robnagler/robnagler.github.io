Enhance with Mazda beep and Linode blocked IP and more explanations

Having run smallish mail servers for about four decades, the oppressors have won "mostly" for me. This week/end I am migrating my partner's single-person firm's domain to Google Workspace. This thread is topical, interesting, and hilarious to skim. Indeed, as I sat down to write this I received "Everything you need for work – right in Gmail" from Workspace. Not!

The first migration (RadiaSoft) happened over a year ago, and I'm relatively happy I did it although one of my co-workers is getting PTSD from Google Drive's weird behavior on her Macbook. I cannot migrate all my domains, e.g. the one I'm sending this from, but I probably would.

Laura, did you notice the To line in the email to which I am replying is "Bill Cole via mailop <mailop@mailop.org>". While I really enjoyed your message(s), I think this is the crux of the problem(s) with "computers these days". Why does mailop mail sometimes take hours to get to me? Why was the certificate on the website broken for so long? Is it still? Where is my message going to go when I see "Bill Cole via mail op" in my MUA? Why does visiting https://mazda.com result in Forbidden? Inquiring minds would like to know. Or maybe it's just me and my pedant for little details like that.

Why migrate a tiny domain? Spam. She's a real estate agent and her address is public and in lots of people's address books. Spam, spam, spam. I try to filter it with tools like Spamassissin, Postgrey, "sleep 8", and so on. I gave up running an MUA years ago. I tell people to use Gmail, perhaps that's wrong, but it's kind of what people did in the day with tiny domains. Zoho had such a bad email reputation that I had to migrate RadiaSoft off it on to our own servers. I certainly couldn't recommend ad-infested MUAs like Yahoo. Gmail seemed like a good thing, and they weren't as evil back then.

It's funny to me that people are saying "Google is just monetizing". Not as such. More like an anarcho-syndicalist commune or the Ben & Jerry's of the Internet. They didn't invent ad-monetized search (or ice cream). They make money off it, and more power to them. Yet the rest of their stuff seems like unmanaged chaos.

For the uninitiated, you cannot convert foo@gmail.com to foo.com to Workspace without some effort. Mail can be migrated relatively easily. Drive cannot be migrated to Drive according to Google. Fun tidbit: Drive allows two files with exactly the same name. Oh, and you can have two YouTube channels with the same name. Rilly?

You can migrate Drive thanks to Rclone. Though, it took me most of the day to figure out how to get Google's Service Accounts to work. Mail migration is only about 35 clicks and is running, but it is going to take a week for one account, which of course is embarrassingly parallel, so it shouldn't. Yesterday, in under an hour, I migrated an entire site from my current colo to Linode with 100GB+ transactional SQL and files. Why is Drive to Drive not just a few clicks like mail? It's even less complicated.

At one point this weekend, my lovely partner said "maybe I should just use foo@gmail.com. Everybody has a gmail address, it's normal." This after years spending time SEOing (more oppression) her own domain. Needless to say I nearly tore my hair out at that point. She had been complaining about having to "pop" her mail into Gmail account from her laptop (not possible on the phone) manually for years, which finally prompted the migration (along with a colo failure, below). She thought it was Google's business plan to make it so difficult to switch from free to fee that she wanted to go back to free and destroy her decade worth of brand building. Gardners do it, which shouldn't she?

As 6p was approaching, she asked "are you going to be able to switch gears?" Fortunately, I got a successful directory listing from rclone, and I was ready to have dinner with friends. If I had not figured it out, dinner would have been ruined by me talking with one of the people about his experience with GCP and Service Accounts. As they were leaving, he mentioned the colo failure (wait for it) and I talked about the migration to Linode, and he said "What's Linode?" He assumed the world ran on AWS, Azure, and reluctantly GCP. "How do they make money?" Another dimension to this "oppression".

I am being oppressed by my one-data-center colo right now, which was down for TWO DAYS a couple of weeks ago. I've been oppressed into this migration to Linode and another DC, because they not only didn't keep their network up for two days but failed miserably to let their customers know what was going on. I still don't know, and I don't care.

One of my co-workers who is early career is helping with the colo-part of the migration. He has never worked in a DC nor really done much with server hardware. He's a serverless-cloud kinda person. He said to me the other day, "I was thinking about you carrying a pager back in the day, and I realized that I don't want to do that." More power to him, frankly. When my "pager" was going off at all hours two weeks ago over network failures I could not control, and I was getting hate mail from people who still use AOL, Hotmail, and Qwest addresses, I would have been happy to hand off the baton.

20 years ago I helped start what is now Validity. George Bilbrey at the time said, "delivery assurance is a two year, $2M business". I'm happy for him that it didn't turn out that way. (And, Laura, at the time, I had to convince Paul Graham to remove Assurance Systems from his How To Spam page so I relate to your current struggles.)

25 years ago, Bob Lucky wrote Bozos on the Bus:

Being bozos, we are relegated to the role of mere passengers in the back of a bus that is speeding recklessly towards somewhere or other. The bus is being driven by someone up front whom we can't quite see, and worse yet, we're not even sure where the destination is supposed to be.

Paul, I respect you. I encourage you to stand up for your values in a world where I feel completely disoriented on a nearly daily basis.

Off to the colo...
