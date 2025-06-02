---
title: "Remote controlling Claude Code"
date: 2025-06-01
slug: "remote-control-claude-code"
tags:
  - dev
  - ai
  - claude
---

![Remote operating Claude Code from my phone](/assets/cc-remote.jpeg)

[Claude Code](https://www.anthropic.com/claude-code) amazed me at launch.

With Claude 4 release, it cosplays AGI for code & sysadmin tasks, and convinced me to give Anthropic $100/mo.
There's a lot of [good advice](https://www.anthropic.com/engineering/claude-code-best-practices) about how to get the most out of it so I won't cover that - this is about how to remote operate it.

### Why

CC is my [weird intern](https://simonwillison.net/2024/Sep/10/software-misadventures/#the-weird-intern) in a terminal, parked on my second screen.
I mostly keep an eye on it as it works, waiting to respond to permission prompt or steer when I see it going down the wrong path.
With a good plan (don't outsource your thinking!), `Claude.md` (don't outsource your opinions!), it can chip away at a task for hours, but needs steering and approvals.
Headless mode is fine for simple/self-contained tasks, and [I built a thing](https://github.com/adstastic/claude-code-whatsapp-approval) that lets it Whatsapp me for permission, but that doesn't work for interactive mode.

I run CC until I hit rate limits, then take a break - it's a good natural reset.
During these 3-5 hour sessions, each time I go AFK I feel the impulse to rush back and unblock/steer CC.
This is obviously unhealthy and unproductive, so I'd rather live my AFK life while CC makes progress, checking in from time to time.

### How

I'm in the Apple ecosystem, so this is a Mac/iPhone guide, but should be easy to port to Android app + Unix OS.

Prerequisites:
- Sign up for Tailscale

#### On your phone:
1. [Download the Tailscale app](https://tailscale.com/download) and connect to the Tailnet.
1. Install a shell app which supports [Mosh](https://mosh.org/), I use [Blink](https://blink.sh/).
1. Generate an SSH key. Blink has a neat feature to generate it in the secure enclave.

#### On your mac:
1. Install Tailscale.app and connect to the Tailnet. The standalone app is recommended.
1. Copy the **public key** from your phone to your computer, and save it in `~/.ssh/authorized_keys`. Create the directory if not exists.
1. Set permissions:
```
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```
1. [Enable Remote Login in System Preferences](https://support.apple.com/lt-lt/guide/mac-help/mchlp1066/mac), restrict it to your user.
1. Edit `/etc/ssh/sshd_config` (requires sudo) and upsert the following to replace password auth with SSH key:
```
PubkeyAuthentication yes
PasswordAuthentication no
```
1. Restart the SSH service:
```
sudo launchctl stop com.openssh.sshd
sudo launchctl start com.openssh.sshd
```
1. [Install tmux](https://github.com/tmux/tmux/wiki/Installing)
1. Add this to `~/.tmux.conf` to allow mouse scroll and set a large history buffer, very useful on mobile and with claude code.
```
set -g history-limit 1000000
set -g mouse on
```
1. Start a tmux session: `tmux new-session -A -s <session_name>`

#### On your phone:
1. Test the connection: `ssh your_macos_user@mac_tailnet_machine_name`
1. Once connected, run `tmux attach -t <session_name>`

Congratulations! Now your phone and mac are connected to the same shell session. You can run claude code here, and see and interact with it from both sessions.

This gets you working SSH/session sharing, but SSH connections are brittle to changing networks. Mosh fixes this.

#### On your mac:
1. Install Mosh
1. Run `mosh-server`
1. Accept the prompt to allow incoming connections

#### On your phone:
1. Replace the `ssh` command with `mosh`

Mosh should stay connected forever, but if you want to exit without killing the tmux session, use `ctrl-B D` instead of `ctrl-D`.
If you do accidentally kill the shell with claude code, resume it with `claude -c`.

It's far from a good mobile UX, but it works.
Enjoy! Don't forget **start a tmux session before you go AFK**.

### Why not Tailscale SSH?

This would be a lot easier, but Tailscale.app on macOS can't be a Tailscale SSH server.
I got it working with the [open-source go binary `tailscaled`](https://github.com/tailscale/tailscale/wiki/Tailscaled-on-macOS) + manually setting DNS, but reverted to the app and configuring SSH manually because:

- `tailscaled` runs outside userspace, and can't be managed as a VPN in System Settings
- [no support taildrop support & can't use exit nodes](https://tailscale.com/kb/1065/macos-variants#comparison-table)
- no auto updates
- the CLI warned it was unstable, and for experiments and testing only
- I didn't feel like an [experienced macOS system administrator](https://tailscale.com/kb/1065/macos-variants#open-source-tailscaled-variant)
- I was comfortable setting up SSH manually, and the above setup is hardened.
- I was only exposing my Mac's SSH server on the local network, not the public internet. Tailscale is still required to reach the Mac.

I also tried running `tailscaled` and Tailscale.app together, and at one point had 2 different connections to the tailnet from the same machine, but it was brittle and they were sharing state.

I rely on tailscale for important work/personal stuff, so I didn't want to go down a non-recommended path.