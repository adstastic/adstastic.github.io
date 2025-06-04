---
title: "Claude Code Tips for SWE"
date: 2025-06-01
slug: "claude-code-tips"
tags:
  - ai
  - claude
  - dev
---

I've been been using Claude Code a lot the past 2 weeks, enough that I hit the Max plan rate limits 3-4x daily.
These tips have been the biggest quality of life improvement for me. You can find more in [Anthropic's best practices](https://www.anthropic.com/engineering/claude-code-best-practices).

- Whenever it goes down a wrong path, interrupt immediately and add a memory for the correct action, then tell it to proceed.
- Compact early, often, and with instructions for what to do next.
- If you accidentally close it, or want to resume a session, use `claude -c`.
- Run `/terminal-setup` for shift+enter to insert newlines.
- Run `/config` and set the theme to match your terminal. Makes reading diffs much easier.
- Tune the allowed tools to minimise the permission prompts, but don't allow destructive commands or unrestricted web interaction
- Use it as a shell assistant - it can run any shell command, so it can perform complex workflows like "SSH to the server, connect to the database, run a query to find something that points to a file, and download that file"
- Sonnet requires more steering than Opus. Opus tends to self correct, but Sonnet + more steering can move much faster for simpler tasks. Be mindful of when you've passed the 50% limit and switches, and switch your style.
- Leverage Claude's understanding of `git` and `gh` to interact with it as co-worker: commit code often, push PRs, address review comments. The Github app makes this the easiest but needs API credits, so using Claude Code to read and interact with Github is a decent workaround.
- Put effort into your global and project `Claude.md`. For monorepos, write one for each directory. Iterate them often. Run them through Anthropic's [prompt improver](https://www.anthropic.com/news/prompt-improver) regularly.
- [Setup a remote shell from your phone to where you run Claude Code](/p/remote-control-claude-code). For certain tasks, it just needs a bit of steering or permission every few minutes, and you need to live your AFK life!