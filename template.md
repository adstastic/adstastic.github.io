---
layout: quote
title: "{{ quote.title }}"
ref: {{ quote.source_url | default(quote.url) }}
tags: 
{%- for tag in quote.tags %}
  - {{ tag }}
{%- endfor %}
---

Quoting [{{ quote.author }}]({{ quote.source_url | default(quote.url) }}):
{% for highlight in quote.highlights %}
> {{ highlight }}
{% endfor %}