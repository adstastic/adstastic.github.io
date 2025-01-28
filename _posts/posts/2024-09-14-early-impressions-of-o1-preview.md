---
layout: post
title: Early impressions of o1-preview
tags: [software, ai, project]
---

**tl;dr** I used OpenAI's `o1-preview` model to code a web app that uses `gpt-4o-mini` to generate simple mental maths rules for converting between currencies. If you have an OpenAI API key, go [check it out](https://adim.in/mental-forex/)!

---

Recently I was chatting to a friend in Columbia. An excerpt from the call:

> "I'm gonna buy something, is 8650 pesos a lot?"\
> "1 GBP is 5486 COP"\
> "Ok...that's gonna be annoying to calculate while out and about".

I thought about it for a bit and said "Drop the last 3 digits and divide by 5". 

OpenAI had just dropped `o1-preview`, so I wondered about using its superior reasoning[^superior] to generate such heuristics. Alas, I don't qualify for API access, so I [argued with 4o-mini](https://platform.openai.com/docs/guides/prompt-engineering) until it made usable rules, and got o1-preview to implement it. 

The result is [Mental Forex](https://adim.in/mental-forex/) - how far my weird intern[^weird-intern] & I got in ~2 hours, when I hit the message cap. You'll need an OpenAI API key[^sus] to use it.

I've tried small projects with `claude-3.5-sonnet` or `gpt-4o` before, and this is a significant improvement. My early impressions:
- hallucination, gaslighting, and loops are much rarer
- it often followed all of the specified instructions
- without being asked, it tried to improve things along the way, such as the the prompts
- prompts have a much longer half life - it could remember, follow, and demonstrate that it followed certain instructions long after they were given.
- the abbreviated chain of thought logs are quite useful for understanding and telling it where it went wrong

I'm impressed. It needs hand-holding, but I didn't constantly wonder if DIY would be faster. Excited for similar capabilities from open-source models soon!

Footnotes:

[^superior]: It really is a step change but people are obviously over-hyping it. It's not AGI, even [Sam Altman said so](https://x.com/sama/status/1834283100639297910).
[^weird-intern]: [Simon Willison coined this wonderful phrase](https://simonwillison.net/2024/Sep/10/software-misadventures/#the-weird-intern)
[^sus]: if you're sus (cc [@glukicov](https://github.com/glukicov)), compare what your browser loads with the [source](https://github.com/adstastic/mental-forex/blob/main/index.html)