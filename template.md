---
layout: quote
title: "{{ quote.title }}"
ref: {{ quote.url }}
tags: 
{%- for tag in quote.tags %}
  - {{ tag }}
{%- endfor %}
---

Quoting [{{ quote.author }}]({{ quote.url }}):
{% for highlight in quote.highlights %}
> {{ highlight }}
{% endfor %}