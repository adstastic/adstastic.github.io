---
layout: post
title: Mental Forex
tags: [software, ai, project]
---

**tl;dr** I used OpenAI's `o1-preview` model to code a web app that uses `gpt-4o-mini` to generate simple mental maths rules for converting between currencies. If you have an OpenAI API key, go check it out at https://adim.in/mental-forex/

---
Recently, a friend was travelling to Columbia and asked me how to convert prices back to GBP while out and about. I looked it up: `1 GBP = 5486 COP` (Columbian Pesos). I thought about it for a bit and said "Drop the last 3 digits and divide by 5". 

I'd just got access to OpenAI's o1-preview, so I thought this would be a cute little website to try and build. Initially I wanted to use o1-preview's superior reasoning[^superior] to generate the rule but I don't qualify for API access (and it'd be damn expensive), so I [argued with 4o-mini](https://platform.openai.com/docs/guides/prompt-engineering) until we had an agreement. It's entirelty coded by o1-preview, including some of the prompt engineering[^meta].

This is how far my weird intern[^weird-intern] & I got until the rate limits hit: [https://adim.in/mental-forex/](https://adim.in/mental-forex/)

If you're sus and think I'm farming API keys[^gleb], feel free to compare what your browser loads with the [source](https://github.com/adstastic/mental-forex/blob/main/index.html).

Footnotes:

[^superior]: It really is a step change IMO but people are obviously over-hyping it. It's not AGI, even [Sam Altman said so](https://x.com/sama/status/1834283100639297910).
[^meta]: [Dude, that's so meta](https://www.urbandictionary.com/define.php?term=That%27s%20so%20meta)
[^weird-intern]: [Simon Willison coined this wonderful phrase](https://simonwillison.net/2024/Sep/10/software-misadventures/#the-weird-intern)
[^gleb]: cc [@glukicov](https://github.com/glukicov)