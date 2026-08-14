# Dual Engine: LLM And MML

The **Semantic Operating System (SOS)** uses a dual engine because language work has two different modes. For the broader architecture, see [What.md](../What.md). For the persistence layer that stores and indexes knowledge, see [Dual-Persistence.md](Dual-Persistence.md).

Sometimes the system needs to discover, phrase, generalise, or explore. That is where a **Large Language Model (LLM)** is useful.

Sometimes the system needs explicit semantic specificity, reusable established knowledge, or governed composition of known conceptual coordinates. That is where **Machine Modelled Language (MML)** is intended to help.

In the SOS architecture, the engine is therefore not a choice between LLM and MML. It is a portal that routes work between them.

LLMs, or Large Language Models, are neural models trained to predict and generate language from patterns learned across large text corpora. They are powerful because they can handle ambiguity, style, syntax, analogy, and open-ended generation without every rule being modelled by hand.

MML, or Machine Modelled Language, is the structured counterpart introduced by this project. It proposes three transfers of responsibility from learned models:

| Responsibility | Learned-model default | MML direction |
| --- | --- | --- |
| **Semantic specificity** | Recover the intended distinction from latent representation and context. | Represent important identities, roles, relations, and constraints explicitly. |
| **Durable knowledge** | Reconstruct task-relevant knowledge from prose or parameters at use time. | Compile governed knowledge into reusable executable views. |
| **Conceptual resolution** | Depend on a learned latent pattern for each useful combination. | Compose sufficiently independent semantic coordinates into a task-specific field at runtime. |

In compact form: **Represent meaning. Compile knowledge. Compose concepts.** Deterministic propagation is one possible execution mechanism beneath those transfers, not the definition of MML.

At runtime, SOS prefers governed MML capability for represented and compiled tasks, then uses an LLM when the structure is insufficient or language generation is required. In discovery, the order is inverted: the LLM reads and proposes, while accountable governance validates candidates for representation, compilation, and reuse.

```text
Runtime:   prompt -> Common Language Model mapping -> MML first -> LLM fallback -> answer
Discovery: raw material -> LLM first -> MML validation/indexing -> knowledge base
```

## LLMs: Discovery And Language

LLMs are good at working with raw, fluid language. They can read emails, summarise documents, extract candidate entities, propose relationships, rewrite text, detect possible themes, and produce natural phrasing.

That strength comes with a cost. The model stores much of its knowledge implicitly in dense neural weights, and inference produces results through learned representations. This is valuable when the problem is open, ambiguous, or under-modelled. When the relevant distinction or knowledge is already established, explicit representation and compiled reuse may be more controllable; the operational advantage remains to be measured.

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

## MMLs: Representation, Reuse, And Composition

MML is the new part introduced here.

The basic claim is broader than known-pattern propagation. Important meaning can be represented explicitly; established knowledge can be compiled into reusable capability; and broad semantic coordinates can be composed into more specific runtime fields. A propagation algorithm can execute one such field, but it does not supply the representation or establish the combination's validity.

An MML system operates over **Common Language Model (CML)-shaped knowledge**: concepts, word senses, semantic roles, typed relations, evidence links, ontology edges, contradiction links, constraints, and transition weights. It compiles selected structure into executable operators and composes relevant coordinates for a task. An execution strategy may then produce an activation distribution or structured path that points back to what produced it; an optional LLM or deterministic application may express that result for a user.

In the current Python prototype, MML is represented at toy scale by governed semantic identities, a compiled co-occurrence transition matrix, and a Personalized PageRank activation strategy. Grounding and focus change which meanings are addressable; compilation makes the transition model reusable; the elaborated engine independently propagates and softly intersects multiple fields.

That is not production MML yet. Representation, compiled reuse, direct intersection, governed qualification, and explicit stage-scoped transition have bounded authored development evidence. Independently held-out construction, comparative reuse economics, useful combinatorial coverage, and scaling still require controlled tests under the [research contract](../Research-Contract.md).

The deeper MML design lives in [MML-In-Depth.md](../MML-In-Depth.md). That page develops Represent–Compile–Compose, execution strategies, semantic operators, language-model integration, and the next step toward multi-dimensional MML fields.

## Federated MML And LLM Models

There does not need to be one giant model. The architecture can support two big model families, MML and LLM, and also many specialised MMLs and LLMs.

The preferred direction is federated:

- domain-specific MMLs for law, finance, medicine, infrastructure, research, and governance;
- smaller LLMs paired with those MMLs for local generation and discovery;
- shared Common Language Model contracts where systems need to interoperate;
- local autonomy with federation rather than one central model owning all meaning.

Think less empire, more Switzerland: cantons, shared protocols, strong local identity, and just enough federation to keep the trains, or in our case the semantic routes, running on time. Yes, that is a small wink to our Suisse love.

This federated view also creates a hypothesis about smaller neural models. If part of a system's required semantic and knowledge capability moves into explicit CML-shaped sources and compiled MML views, a paired language model may need to carry less of that responsibility in its parameters. Whether this permits a smaller model without unacceptable capability loss requires direct training, quality, latency, and resource comparisons.

The result is not anti-LLM. It is post-monolith. LLMs remain valuable, but they become members of a larger semantic system instead of being forced to carry discovery, memory, reasoning, retrieval, governance, and generation alone.
