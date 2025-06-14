---
title: "The best way to try new models"
date: 2024-11-30
slug: "ollama-modal"
tags:
  - software
  - ai
  - infra
---

_This isn't a sponsored post._

It seems like a new LLM drops every other day. The latest that piqued my interest was [qwq](https://qwenlm.github.io/blog/qwq-32b-preview/), with "o1-like" reasoning capabilities. 

I usually try out new LLMs with Ollama, so satiating my curiosity should have been an `ollama run` away, but I was too impatient to wait for the 25 GB QwQ to download on 1 MB/s down my hotel WiFi so I figured I'd try something new.

I've been a fan of [Modal](https://modal.com/) for a while - it's the simplest way to get from a Python file to a running web service. It's _very_ useful for running AI workloads easily because you can attach GPUs, and with a generous $30 free credit per month, I can play around with LLMs for free.

There's an [official tutorial](https://modal.com/blog/how_to_run_ollama_article) for running Ollama on Modal. In minutes, I had Ollama running `qwq` on a Modal worker, streaming output back to my terminal.

I like to test the "reasoning" capabilities of models with [the world's hardest logic puzzle](https://en.wikipedia.org/wiki/The_Hardest_Logic_Puzzle_Ever). `qwq` struggled with it for 10 minutes before giving up:

![Some quirky reasoning output](/assets/qwq-kidding.jpeg)

Overall, I chatted with it for 18 minutes, which cost me $0.36 on an Nvidia A10G.

![Modal bill](/assets/qwq-modal-bill.png)

This setup boots in ~15s (the first cold start will take a few minutes due to image build/model download), and Modal only bills for usage so with something like:

```
modal run ollama-modal.py --text "Your prompt here"
```

you're only charged for the time spent on inference, and the worker shuts down once the model finishes outputting.

Modal is also good for more advanced setups e.g. models that aren't on Ollama, or other serving frameworks. They have several [well documented examples](https://modal.com/docs/examples) for inference and training, and other non-ML workloads, so it's become go-to for getting something up and running quickly. 

I think this Ollama + Modal setup is the easiest and cheapest way to try open-source LLMs, especially if you don't have the bandwidth to download or hardware to run them yourself.