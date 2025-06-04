---
title: "Putting Gemini 2.5 Pro Through Its Paces"
date: 2025-03-26
ref: https://simonwillison.net/2025/Mar/25/gemini/#atom-everything
---


Quoting [Simon Willison's Weblog](https://simonwillison.net/2025/Mar/25/gemini/#atom-everything):

> llm -m gemini-2.5-pro-exp-03-25 \ 'transcribe, first speaker is Christopher, second is Simon' \ -a ten-minutes-of-podcast.mp3 \ --schema-multi 'timestamp str: mm:ss, text, speaker_name'