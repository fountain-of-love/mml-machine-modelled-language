# Dual Engine: LLM And MML

The **Semantic Operating System (SOS)** uses a dual engine because language work has two different modes. For the broader architecture, see [What.md](../What.md). For the persistence layer that stores and indexes knowledge, see [Dual-Persistence.md](Dual-Persistence.md).

Sometimes the system needs to discover, phrase, generalise, or explore. That is where a **Large Language Model (LLM)** is useful.

Sometimes the system needs to reuse known structure quickly, deterministically, and with an audit trail. That is where **Machine Modelled Language (MML)** is useful.

In the SOS architecture, the engine is therefore not a choice between LLM and MML. It is a portal that routes work between them.

LLMs, or Large Language Models, are neural models trained to predict and generate language from patterns learned across large text corpora. They are powerful because they can handle ambiguity, style, syntax, analogy, and open-ended generation without every rule being modelled by hand.

MML, or Machine Modelled Language, is the structured counterpart introduced by this project. It models language as explicit concepts, links, weights, and transitions, so known patterns can be queried through deterministic graph-like propagation instead of being rediscovered by dense stochastic inference every time.

At runtime, SOS prefers MML first for known patterns and uses an LLM when the known structure is insufficient. In discovery, the order is inverted: the LLM reads and proposes, while MML validates, organises, indexes, and preserves.

```text
Runtime:   prompt -> Common Language Model mapping -> MML first -> LLM fallback -> answer
Discovery: raw material -> LLM first -> MML validation/indexing -> knowledge base
```

## LLMs: Discovery And Language

LLMs are good at working with raw, fluid language. They can read emails, summarise documents, extract candidate entities, propose relationships, rewrite text, detect possible themes, and produce natural phrasing.

That strength comes with a cost. The model stores much of its knowledge implicitly in dense neural weights, and inference often navigates learned patterns stochastically. This is valuable when the problem is open, ambiguous, or under-modelled. It is wasteful when the relevant pattern is already known, validated, and could be represented explicitly.

This is why SOS does not throw LLMs away. It narrows their role.

LLMs should be used where they are strongest:

- first-pass discovery from raw material;
- language generation and rewriting;
- ambiguity exploration;
- candidate relationship extraction;
- summarisation;
- open-ended reasoning when structured knowledge is incomplete.

[karpathy/minGPT](https://github.com/karpathy/minGPT) is a useful reference point for this part of the architecture. The repository describes minGPT as a small, clean, interpretable, educational PyTorch reimplementation of GPT for training and inference. Its README also notes that the actual Transformer model definition is compact enough to study directly, which makes it more useful as a learning workbench than a large production framework.

That matters for SOS because a small model can help discover patterns without hiding the experiment inside a massive black box. The broader alignment with minGPT is described in [Initiative-Alignment.md](Initiative-Alignment.md#mingpt-small-neural-workbench-for-discovery).

## MMLs: Known Pattern Propagation

MML is the new part introduced here.

The basic claim is simple: once a pattern has been discovered, validated, and structured, the system should not need to rediscover it through trial-and-error generation. It should preserve that pattern as explicit structure and query it directly.

An MML execution engine operates over **Common Language Model (CML)-shaped knowledge**: concepts, word senses, typed relations, evidence links, ontology edges, contradiction links, and transition weights. The CML itself is introduced in [What.md](../What.md#common-language-model). The result is an activation distribution or structured path that can point back to what produced it; an optional LLM or deterministic application may express that result for a user.

In the current Python prototype, MML is represented at toy scale by a word co-occurrence matrix and a PageRank-style diffusion step. A query word activates a vector, weight moves through the graph, and the result shows which other words carry contextual weight around that query.

That is not production MML yet. It is the smallest visible seed of the idea: words carry weight because they sit inside structured relationships.

The deeper MML design lives in [MML-In-Depth.md](../MML-In-Depth.md). That page covers construction, statistical weight updates, runtime diffusion, hybrid graph-transformer design, and the next step toward multi-dimensional MML fields.

## Federated MML And LLM Models

There does not need to be one giant model. The architecture can support two big model families, MML and LLM, and also many specialised MMLs and LLMs.

The preferred direction is federated:

- domain-specific MMLs for law, finance, medicine, infrastructure, research, and governance;
- smaller LLMs paired with those MMLs for local generation and discovery;
- shared Common Language Model contracts where systems need to interoperate;
- local autonomy with federation rather than one central model owning all meaning.

Think less empire, more Switzerland: cantons, shared protocols, strong local identity, and just enough federation to keep the trains, or in our case the semantic routes, running on time. Yes, that is a small wink to our Suisse love.

This federated view is also how neural models could shrink. If an LLM trains on a knowledge base that already has a Common Language Model with explicit topology in terms of concepts and abstractions, it should not need billions of parameters to rediscover the same structure. The learned model can become smaller because part of the intelligence has moved into the organised knowledge base and matrix layer.

The result is not anti-LLM. It is post-monolith. LLMs remain valuable, but they become members of a larger semantic system instead of being forced to carry discovery, memory, reasoning, retrieval, governance, and generation alone.
