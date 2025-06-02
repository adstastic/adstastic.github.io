---
title: "The Japanese Immigration test for AGI"
date: 2025-05-20
slug: "agi-test"
tags:
  - ai
  - agi
---

There's no widely agreed-upon definition of AGI, and everything with LLMs is vibes dominated anyway, so the best we have is "I'll know when I see it".

That's not very rigorous, so I've been thinking about concrete tasks that, when completable end-to-end, represent a serious enough step forward in outcomes, and replace a significant chunk of multi-faceted human effort that I'll "feel the AGI".

Here's a task that'll make me feel the AGI:

**Given the details of an applicant and visa application, determine the status of the application from the Japanese Immigration Bureau.**

Here's how I, a general intelligence, did it:
1. Find various phone numbers and extensions to try from the internet/Reddit
1. Come up with a call strategy based on the experiences of people on Reddit/other advice on the internet
1. Keep trying different numbers until you get through to a human. Handle busy messages, call disconnects, endless queueing, redirects, etc.
1. Converse with that human in Japanese. If it's not the department that has the answer, you'll be told to call another number. Plead to be transferred internally rather than having to dial back and get stuck in the queue again. Handle the unsuccessful case.
1. If it is the department with the answer, handle each possible outcome state: success, pending, declined. In the terminal states, get confirmation or instructions on how to get written confirmation of the outcome.
1. If pending, get instructions on how to follow up, and information about specified edge cases.

I did it all manually, of course. My Japanese is rusty so I got through mostly on vibes + asking questions, and transcribing/translating the call recording afterwards with Gemini 2.5 Pro confirmed my understanding. I had walked through the decision tree with o3 in advance, and had several keywords and prompts to guide me through, which helped a lot.

Of course this is a very specific task, but it's subtasks are applicable to many other domains:
1. Creating the decision tree 
1. Using tools like web search and VOIP 
1. Maintaining state and following the decision tree
1. Handling real-time voice conversations

Each of these tasks seem possible in isolation, but composing them in a system that is robust, adaptable to high variance, stays on track, and can handle the last-mile problem is a key step towards AGI which current generation agents lack. 

Even building an overfitted and unreliable solution to this out of the tools available today is a non-trivial task, and requires a lot of engineering effort.