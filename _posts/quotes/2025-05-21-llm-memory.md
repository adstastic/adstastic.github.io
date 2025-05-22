---
layout: quote
title: "LLM Memory"
ref: https://grantslatton.com/llm-memory?utm_source=tldrnewsletter
tags:
---

Quoting [Grant Slatton&#39;s Blog](https://grantslatton.com/llm-memory?utm_source=tldrnewsletter):

> something vector embeddings struggle with is episodic memories. That is, you want to remember a chain of memories in series-order. How do you store the link between the memories in your vector DB? Is it another memory? What text do you embed to query it?

There&#39;s probably *some* way to do it, but it&#39;s a hell of a lot easier to just put an edge between two nodes in a knowledge graph.

> major downside of vector embeddings is they are just hard to reason about. If two vectors are anomalously close or far, you don&#39;t really have much recourse or explanation. Adjust the training data of your embedding network and try again? Use a different distance metric than cosine similarity? Something else?

> All knowledge has an explicit or implicit reference frame for which it is valid.

> there is probably a memory system out there where everything is reference frames, meta-reference frames (where the embedded objects are themselves reference frames)

> The document approach can also pair well with vector embeddings, since you can embed the documents (or embed questions the document answers, etc) and use those embeddings to jump to a bunch of candidate nodes to start the graph traversal from.

> In the fullness of time, it won&#39;t be costly to deploy thousands of little cheap agents to crawl the unlabeled local graph looking for relevant information.

> Suppose you have two nodes that describe two events, and one event happened after another. It feels right to encode that &#34;happened after&#34; semantic information in the edge.

To recover that information without that semantic edge, the nodes would need to internally contain ordering information such as the timestamp the event in the node occurred, or the latter node needs to explicitly refer to the events of the former node.

> simply knowing the timestamp is probably always an option, but still feels wrong. Lots of human memories don&#39;t have timestamps but still have happens-before/after relationships for encoding episodic information.

> Every time you run a query over the knowledge graph, you can store the results of that thing as a meta-document.

> after producing a new document, take every pair of documents in context and ask the model if they should probably be connected. Ask what future queries could be helped by having those documents connected. Are those queries likely? If so, make the connection.

> Since you will create spurious connections, because your connection-creator code won&#39;t be perfect, you need some way to garbage collect connections.
