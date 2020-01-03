---
layout: post
title: Running out of Google space
tags: [Tech, Cloud Services, Google, Google Drive]
---
I received a notification from Google that I was nearly out of storage, so I started to clean up my Google Drive to free space so my [Gmail wouldn’t stop working](https://support.google.com/mail/answer/6374270?hl=en).

A [hidden way](https://www.labnol.org/internet/google-drive-sort-files-by-size/28745/) to show all the files in your drive, sorted by size, is to click the text in the **Storage** section of the menu on the left (on a desktop browser).

I freed a lot of space by downloading the largest files in this list (mostly videos). As the list shrunk from 100s of MB per file to below 10s, all the items became photos living inside a `Google Photos` folder.

My guess is that although [Google Photos was separated from Drive](https://support.google.com/photos/answer/9316089), the old Google Photos folder remains. Looking inside, I found this a plausible explanation, as the latest photos roughly coincided with the date Google had changed this system.

Given that this folder is essentially a duplicate of what’s in Google Photos anyway, it would save a lot of space to delete it. I downloaded it, and after waiting a while for the ~17 GB[^google-photos-space-oddity] to get zipped up and fired over the internet, it was on my local machine. 

My plan was to add this to the Photo Library on my Mac, but in my experience the upload to iCloud would take days if not weeks, and I wanted to store the archive in a more accessible way.

I had been eyeing up [Backblaze Backup](https://www.backblaze.com/cloud-backup.html) for a while, and I noticed they also offer Cloud Storage with their [B2](https://www.backblaze.com/b2/cloud-storage.html) service (similar to AWS S3), and the first 10 GB is free. 

I created an account, a B2 bucket, and [installed their command line tool](https://www.backblaze.com/b2/docs/quick_command_line.html). After authenticating with my API key, I used it to upload the Google Photos ZIP I had downloaded from Google Drive.

So there you have it! I freed up the majority of space in my Google Drive, downloaded a bunch of my media and backed them up somewhere else.

*Later on, I went further than this and downloaded all my Google Photos. That story has some interesting challenges and good learnings, coming up next.*

Footnotes:

[^google-photos-space-oddity]: Although the free tier of Google Drive only has 15 GB storage, I had over 17 GB of photos in my old Google Photos folder, plus a lot of other stuff. This could be due to [16 MP or smaller photos being stored for free](https://support.google.com/photos/answer/6220791) in Google Photos (i.e. it doesn’t affect your storage). It seems that this behaviour was retained even after Google Photos was split from Drive, so the only space I saved by downloading this folder was the photos and videos higher quality than 16 MP and 1080p, respectively.


