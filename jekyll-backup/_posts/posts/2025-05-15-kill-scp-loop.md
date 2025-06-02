---
layout: post
title: "TIL: Killing an scp loop"
tags: til dev shell
---

### Story

Yesterday I fired off a quick loop to pull down some files from a server:

```bash
for f in $(cat file-list.txt); do
  scp user@hostname:path/to/data/$(basename $f) local_dir/
done
```

I just needed a couple of examples[^head] so I decided to kill the command when I had them.

When I closed the shell, I expected everything to stop—but the downloads kept chugging away.

I ran `ps aux | grep '[s]cp'` and tried `kill $PID`, but got “no such process.”

Opening `htop`, I saw the `scp` process but by the time I grabbed it's PID, it had finished.
I traced the parent with:

```bash
ps -o pid,ppid,command -p $(ps aux | grep '[s]cp' | awk '{print $2}')
```

Examining the parent showed it was `/bin/zsh`, so I killed that, but the downloads continued.

I traced the grandparent and found it to be `login`, which worried me because killing that would log me out.

How was this possible?

`htop` has a nice Tree feature. This is the tree I was climbing:

```
├─ /Applications/Ghostty.app/Contents/MacOS/ghostty
│  ├─ login
│  │  └─ -/bin/zsh
│  │     └─ scp
```

So I quit my terminal app (Ghostty.app), and the downloads stopped.

### Learnings

* **One-liner for fast-moving processes**
  Quickly inspect PID, PPID, command for processes that vanish too fast to track:
  ```bash
  ps -o pid,ppid,command -p $(ps aux | grep '[s]cp' | awk '{print $2}')
  ```

* **htop’s tree mode** makes it easy to inspect and kill at the right level of the process tree.

* **ctrl-D exiting a tab in Ghostty might leave things running** as the shell integration by default may not always detect background processes and loops when closing tabs. There are a number of settings to improve this e.g.
```
shell-integration = zsh
quit-after-last-window-closed = true
wait-after-command = true
```

Quitting the app should clean these up, as all processes are nested under `ghostty`.

### Footnotes

[^head]: That's what `head` is for? Yeah, I know, I know. ![Captain America I Know](/assets/cap-iknow.gif)
