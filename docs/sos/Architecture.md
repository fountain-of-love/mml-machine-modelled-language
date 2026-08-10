# The SOS Architecture Opened By MML

This document describes a proposed **Semantic Operating System (SOS)** made plausible by the problems that **Machine Modelled Language (MML)** begins to solve. MML is the executable innovation in this repository; SOS is the downstream architecture it could enable. A structured knowledge base, grounded in a **Common Language Model (CML)**, would be queried by MML for governed patterns and supported by **Large Language Models (LLMs)** for discovery, generation, and under-modelled situations.

The current Python prototype does not implement SOS. It demonstrates representation, execution, provenance, snapshots, and update mechanics that open the architectural door.

The name is intentional. SOS is an operating model for meaning, but it is also a small distress signal for the current LLM situation: too much compute, too much opacity, and too much rediscovery of patterns that could be stored as explicit structure.

## Proposed Solution Architecture

SOS starts from a different architectural premise than a standalone LLM. The center is not the neural model. The center is a knowledge base whose data reflects a shared schema of meaning: a **Common Language Model**.

In summary, the architecture has four dual ideas:

- **SOS:** the broader Semantic Operating System that coordinates meaning, discovery, retrieval, and use cases.
- **Dual flows:** runtime flows from prompt to answer; discovery flows from raw material to validated structure.
- **Dual engine:** Machine Modelled Language handles known-pattern query and deterministic propagation; Large Language Models handle discovery, generation, and under-modelled situations. See [Dual-Engine.md](Dual-Engine.md).
- **Dual persistence:** a human-readable Common Language Model knowledge base stores durable notes/nodes, while the MML matrix/index provides fast weighted navigation over that knowledge. See [Dual-Persistence.md](Dual-Persistence.md).

MML itself separates four responsibilities:

```text
documents and public knowledge
  -> compiler / statistical updater
  -> versioned weighted representation
  -> query execution engine
  -> inspectable activation and provenance
  -> optional LLM or deterministic application
```

The compiler maps governed knowledge and observations into explicit structure. The artifact stores that structure. The engine executes it. An LLM may help discover or express knowledge, but it is not the MML.

At a high level, the architecture behaves like a portal:

```text
                         SEMANTIC OPERATING SYSTEM (SOS)

Runtime Stream ------------------------------------------------------------>

[Prompt / Use Case] -> [CML Mapping] ->  +----------------------+ -> [UI / Answer]
                                         |    Portal Engine     |
                                         |                      |        +--------------------------------+
                                         |    MML  <-->  LLM    |  <->   | CML Knowledge Base             |
                                         |                      |        | + MML Matrix / Index           |
                                         | runtime: MML first   |        +--------------------------------+
                                         | discovery: LLM first |
               [Validated Structure] <-  +----------------------+  <- [CML Update]  <- [Raw Docs / Data]

                 <---------------------------------------------------------- Discovery Stream
```

The Portal Engine is the crossing point. Runtime and discovery move in different directions through the same dual engine. Runtime starts from use and asks: what known structure answers this? Discovery starts from raw material and asks: what new structure should be added?

The UI/UX is the use case layer. A legal discovery tool, a research assistant, a governance monitor, or a domain expert interface should not care whether the answer came from MML, LLM, or a combination. The portal decides the route.

### Semantic Operating System

SOS is the broader operating model. It coordinates the CML schema, the human-readable knowledge base, the MML matrix/index, the LLM discovery/generation path, and the UI/UX use cases.

The layers are:

- **SOS:** the broader Semantic Operating System.
- **CML:** the Common Language Model, the shared semantic schema or world-view data model.
- **Knowledge Base:** the stored facts, relations, documents, evidence, and abstractions shaped by the CML.
- **MML:** the deterministic query/diffusion engine over the CML-shaped knowledge base and matrix index.
- **LLM:** the stochastic discovery and generation engine used when known structure is insufficient.
- **UI/UX:** the use case layer where people interact with the system.

### Common Language Model

The Common Language Model, or CML, is the world-view schema. It defines the language of the system: concepts, abstractions, relations, legal categories, factual claims, evidence types, contradictions, provenance, and topology. The knowledge base stores information according to that common model. In other words, data is not simply dumped into storage; it is shaped by a shared semantic structure.

The proposed [CML experiment in scientific reasoning](../explorations/seed-vault/05-experiments/CML-Science-Experiment.md) turns this CML architectural claim into a bounded research project. Its documents live in the **Seed Vault**, the durable knowledge base to which CML is applied as a schema. CML is therefore the common semantic language, not the folder or the stored knowledge itself. The experiment showcases a five-domain physical grammar that could recover formulas, transpose relations across domains, preserve provenance, localize updates, and resist semantic drift.

### Dual Flows

The portal supports two streams.

In the **runtime stream**, the order is:

- **MML first:** query the structured knowledge base and its matrix/index layer for known or validated patterns.
- **LLM second:** if MML does not return a suitable response, use an LLM as the alternative trial-and-error path for open-ended reasoning, language generation, or discovery.

In the **discovery stream**, the order is inverted:

- **LLM first:** read raw material, identify candidate entities, extract relationships, propose abstractions, summarise documents, and surface possible patterns.
- **MML second:** organise those discoveries against the CML, test them against the matrix/index, expose clusters, detect contradictions, and make the resulting structure inspectable.

This distinction matters. SOS does not throw away LLMs. It gives them a clearer role and a bounded responsibility. LLMs are excellent for discovery, language work, ambiguity exploration, and first-pass interpretation. MML is excellent for preserving, querying, validating, and reusing what has already been discovered.

### Dual Engine

The engine is dual because known and unknown patterns deserve different treatment. MML is used first in runtime because it can query known structure quickly. LLMs are used first in discovery because they are excellent at reading raw material, proposing candidate abstractions, and handling ambiguity.

The knowledge base can be fed by LLM discovery. LLMs are still extremely useful for reading large volumes of raw material, spotting candidate patterns, proposing relationships, extracting entities, summarising documents, and suggesting abstractions. But once those patterns are discovered and validated, they should not need to be rediscovered through dense stochastic inference every time. They can be stored as explicit structure and reused by MML.

### Dual Persistence

The knowledge base has two complementary persistence forms:

- **Human-readable knowledge:** notes, pages, records, explanations, provenance, contradictions, and links that people can inspect.
- **MML matrix/index:** weighted transitions, contextual paths, clusters, and pointers that machines can traverse quickly.

The detailed persistence design lives in [Dual-Persistence.md](Dual-Persistence.md). In short, the knowledge base is the durable semantic store, while the matrix/index is the fast MML navigation layer over that store.

The analogy is the [Svalbard Global Seed Vault](https://www.seedvault.no/): SOS treats knowledge as something worth preserving in readable, inspectable form. The knowledge base should behave like an improved Wikipedia shaped by knowledge engineering: notes as nodes, links as typed relationships, and schemas compatible with traditions such as Schema.org, Linked Open Data, RDF, OWL, and RDF/Turtle.

The MML matrix/index does not replace that knowledge base. It points into it. Like PageRank over the web, it lets the system propagate weight through known structure instead of rediscovering the same patterns through dense stochastic inference every time.

### CML As A Query Language

CML should be thought of as the query language of the system. SQL maps human intent onto relational tables. CML maps human intent onto a shared semantic topology: concepts, relations, evidence types, abstractions, and domain-specific meanings.

MML is then the execution engine over that CML-shaped structure. CML expresses what the prompt means inside the common language of the knowledge base. MML uses the matrix/index layer to retrieve and propagate through the known structure.

Incoming prompts should be mapped onto the CML first:

```text
Prompt
  -> CML mapping
  -> known concepts, relations, evidence types, and abstractions
  -> MML matrix query
  -> retrieved patterns and supporting records
```

This increases effectiveness and efficiency. The system is not trying to answer from an unconstrained cloud of parameters. It first translates the prompt into the shared language of the knowledge base, then queries known structure.

If that fails, the LLM path remains available:

```text
Prompt
  -> CML mapping
  -> insufficient known pattern
  -> LLM discovery / generation
  -> candidate result
  -> optional validation back into the knowledge base
```

That feedback loop matters. The LLM can discover new candidate patterns, but MML should decide what becomes durable structure.

## How The Scripts Reflect The Architecture

The Python scripts do not define the architecture. They reflect it in miniature:

- `pagerank_attention.py` shows that contextual weight can move through a word graph.
- `mml_elaborate_corpus.py` builds a richer corpus and matrix, acting as a tiny CML-shaped knowledge field.
- `mml_legal_usecase.py` acts as the use-case layer, querying that corpus-derived field for an authored GDPR evidence problem.

The scripts are intentionally small. They showcase the architecture, not a production system.

## Dual Persistence In Depth

The detailed persistence design lives in [Dual-Persistence.md](Dual-Persistence.md). In short, SOS persists meaning twice: once as human-readable knowledge that can be inspected, governed, corrected, and linked; and once as an MML matrix/index that lets machines move quickly through the known structure.

- **Knowledge base:** durable notes/nodes, typed links, provenance, contradictions, evidence, schemas, and explanations.
- **MML matrix/index:** weighted transitions, contextual paths, clusters, and pointers into the knowledge base.
- **Seed vault principle:** known patterns should be preserved in readable form instead of rediscovered from scratch every time.
- **PageRank analogy:** once the graph exists, MML can propagate weight through known structure quickly and deterministically.

## Dual Engine In Depth

The detailed engine design lives in [Dual-Engine.md](Dual-Engine.md). In short, the SOS engine is dual because known and unknown patterns deserve different treatment.

- **MML** handles deterministic propagation over known, validated, CML-shaped structure.
- **LLM** handles discovery, generation, ambiguity, and under-modelled situations.
- **Federation** allows many specialised MMLs and LLMs to cooperate through shared CML contracts instead of forcing one central model to own all meaning.
- **LLM detail** is grounded by [karpathy/minGPT](https://github.com/karpathy/minGPT) as a small, inspectable GPT workbench.
- **MML detail** lives in [MML-In-Depth.md](../MML-In-Depth.md), including transition learning, runtime diffusion, hybrid generation, and multi-dimensional MML fields.
- **Initiative alignment** lives in [Initiative-Alignment.md](Initiative-Alignment.md), covering minGPT, Apertus, Wikipedia/Wikidata, SEMIC, EuroVoc, Cellar/EUR-Lex, and the Svalbard seed-vault analogy.
