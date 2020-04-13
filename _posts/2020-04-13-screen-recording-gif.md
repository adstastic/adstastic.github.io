---
layout: post
title: Screen Recording GIFs
tags: [software, tutorial]
---

A picture is worth a thousand words. A video is worth `1000 * frame_rate` words? Probably not, unless every frame is a completely different picture - I've probably taken this aphorism too far.

But a video is _very useful_ at illustrating a series of steps especially when it comes to explaining how to do something on a computer. As I'm doing more tutorials on this blog, I wanted to have GIFs of steps in the process to better explain what's going on. 

Searching the internet for this generally returns dodgy websites that I'd rather not use[^giphy], so I looked for a way to do it using myself. 

MacOS comes built-in with a good Screenshot (née Grab) app, which allows recording sections of the screen on Catalina[^instructions], which will produce a `.mov` file, probably on your `Desktop`.
Once you have a video you want to make a GIF, here's how:

1. Download and install [`ffmpeg`](https://ffmpeg.org/download.html). Easiest way on MacOS is `brew install ffmpeg`[^brew]. 
2. Run the following command[^ffmpeg], changing the filepaths `input.mov`, `output.gif`, and the settings `fps=10` and `scale=640` as required. 
```
ffmpeg -i input.mov -vf "fps=10,scale=640:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0 output.gif
```
3. Preview the GIF and adjust the scale/fps as needed for its level of detail. The height will scale proportionally.

Here's a gif of my screen recording of the intro of ASCII Star Wars Episode IV:
![telnet towel.blinkenlights.nl](/assets/ascii-star-wars.gif)

Footnotes:

[^giphy]: I later discovered [Giphy offers this service]((https://giphy.com/create/gifmaker)), but you have to create an account to use it, and it seems to upload the GIF to the platform.
[^instructions]: I couldn't get it to record it's own interface so [here are some instructions](https://support.apple.com/en-us/HT208721).
[^brew]: If you don't have [Homebrew](https://brew.sh/) installed, consider installing it, or using one of the static builds on the FFmpeg website.
[^ffmpeg]: Modified version of "ffmpeg example" [here](https://superuser.com/a/556031).
[^imagemagick]: Modified version of "imagemagick example" shown [here](https://superuser.com/a/556031).
