---
title: "{{ quote.title }}"
date: {{ quote.date }}
slug: "{{ quote.slug }}"
tags:
  - quote
{%- for tag in quote.tags %}
  - {{ tag | lower | replace(' ', '-') }}
{%- endfor %}
ref: {{ quote.source_url | default(quote.url) }}
---

Quoting [{{ quote.author }}]({{ quote.source_url | default(quote.url) }}):
{% for highlight in quote.highlights %}
> {{ highlight }}
{% endfor %}