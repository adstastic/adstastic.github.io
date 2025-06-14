---
title: "Breaking sudo"
date: 2020-11-06
slug: "breaking-sudo"
tags:
  - programming
  - macOS
---

A while back I wrote about using [TouchID to authenticate sudo](/sudo-touchid). I made this change when I was still using Terminal.app and everything worked fine. 

As we all know, 2020 has been a year full of unexpected changes, the most notable of which is clearly me switching to iTerm2 as my terminal emulator. This broke the TouchID setup I had done earlier and I was back to typing out my password. 

Today I learned why: iTerm2 by default allows sessions to survive logging out and back in again and this breaks[^3] the TouchID authentiation for sudo. 

Turning this off from **Preferences > Advanced > Allow sessions to survive logging out and back in again** will reinstate your ability to give your Macbook the finger to get it to do stuff you probably shouldn't[^1] be doing.

However, once this feature was gone I realised I missed it and it's absence was a black hole[^2] in the fabric of my developer experience so I found a [workaround](https://github.com/fabianishere/pam_reattach). After following the installation and usage instructions, I was ready to use my finger for sudo as well as have my terminal sessions survive logouts.

Here's what happened next:
```
$ sudo ls
sudo: unable to initialize PAM: No such file or directory
```

The magnitude of what had happened dawned on me. I had broken sudo, and I couldn't fix it because I needed sudo to edit the file to undo what I had just done. 

A quick Google suggested rebooting into Single-User mode (power-on then ⌘-S) to get root access to the machine. This didn't work, which made a lot of sense because that T2 chip ain't very useful if someone needs just to reboot holding down 2 keys to get a root shell.

I kept searching, slowing accepting that I would need to reinstall the OS. Just as I was about to give up, I found a way to get a root shell via Recovery mode and it worked! 

1. Boot to Recovery mode (power-on then ⌘-R)
2. Open Disk Utility - there should be 2 unmounted volumes e.g. *Macintosh HD* and *Macintosh HD - Data*. They may be named differently but one will have a "- Data" suffix.
3. Mount *Macintosh HD*
4. Quit Disk Utility
5. Open the Terminal - it's under Utilities in the menu bar
6. `cd /Volumes/"Macintosh HD`
7. `vi /etc/pam.d/sudo`
8. Remove the offending line
9. `!wq` 
10. Restart

So how does this bypass the T2 security chip? It doesn't, my password was required to enter recovery mode as well as to mount the drive.

That was enough fun for a lifetime...I think I'll be okay without my sessions surviving logouts[^4].

Footnotes:

[^1]: Unless you know what you are doing - then of course you should be doing it. 
[^2]: It really wasn't a big deal I just wanted both features to work.
[^3]: <https://gitlab.com/gnachman/iterm2/-/issues/7608#note_153123852>
[^4]: I'll just never logout.