---
layout: post
title: "{{ quote.title }}"
ref: {{ quote.url }}
tags: quote
---

Quoting [{{ quote.author }}]({{ quote.url }}):
{% for highlight in highlights %}
> {{ highlight }}
{% endfor %}