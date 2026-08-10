# The SOS Architecture Opened By MML

This document describes a proposed **Semantic Operating System (SOS)** made plausible by the problems that **Machine Modelled Language (MML)** begins to address. MML's proposed innovation is the combination of explicit semantic representation, compiled reusable knowledge, and runtime conceptual composition:

> **Represent meaning. Compile knowledge. Compose concepts.**

An execution engine makes those propositions operational; it is one component of MML, not its complete definition. SOS is the downstream architecture they could enable. A structured knowledge base, grounded in a **Common Language Model (CML)**, would supply governed semantic coordinates and knowledge to MML, while **Large Language Models (LLMs)** could support discovery, generation, and under-modelled situations.

The current Python prototype does not implement SOS. It provides bounded Representation evidence plus mechanism seeds for compilation, reuse, soft intersection, provenance, snapshots, and updates. Those mechanisms open the architectural door without validating the complete SOS or all three MML hypotheses.

The name is intentional. SOS is an operating model for meaning, but it is also a small distress signal for the current LLM situation: too much compute, too much opacity, and too much semantic and knowledge work assigned only to latent reconstruction when some of it may be representable, compilable, and reusable.

## Proposed Solution Architecture

SOS starts from a different architectural premise than a standalone LLM. The center is not the neural model. The center is a knowledge base whose data reflects a shared schema of meaning: a **Common Language Model**.

In summary, the architecture has four dual ideas:

- **SOS:** the broader Semantic Operating System that coordinates meaning, discovery, retrieval, and use cases.
- **Dual flows:** runtime flows from prompt to answer; discovery flows from raw material to validated structure.
- **Dual engine:** Machine Modelled Language externalizes semantic specificity, compiles governed knowledge, and composes known coordinates; Large Language Models handle discovery, generation, and under-modelled situations. See [Dual-Engine.md](Dual-Engine.md).
- **Dual persistence:** a human-readable Common Language Model knowledge base stores durable notes/nodes, while the MML matrix/index provides fast weighted navigation over that knowledge. See [Dual-Persistence.md](Dual-Persistence.md).

MML's research architecture and operational components can be summarized as:

```text
documents and public knowledge
  -> explicit semantic identities, roles, and relations
  -> compiler / statistical updater
  -> versioned reusable operators
  -> query focus and conceptual composition
  -> selected execution strategy
  -> inspectable activation and provenance
  -> optional LLM or deterministic application
```

Governed sources represent meaning. The compiler transforms established structure into reusable artifacts. Runtime mapping and composition construct a task-specific field, and an execution strategy activates it. An LLM may help discover, map, validate, or express knowledge, but it is not the MML.

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
- **MML:** the explicit representation, compilation, composition, and deterministic execution layer over CML-shaped knowledge and its compiled indexes.
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

This distinction matters. SOS does not throw away LLMs. It gives them a clearer role and a bounded responsibility. LLMs are useful for discovery, language work, ambiguity exploration, and first-pass interpretation. MML proposes explicit semantic coordinates, compiled reuse, and governed composition for sufficiently established knowledge.

### Dual Engine

The engine is dual because established structure and under-modelled language work deserve different treatment. At runtime, MML can represent the intended coordinates, execute compiled knowledge, and compose governed fields before an LLM is asked to fill gaps or render language. In discovery, an LLM can read raw material and propose candidate abstractions, while MML-oriented governance decides what becomes explicit, compilable, and reusable.

The knowledge base can be fed by LLM-assisted discovery. LLMs are useful for reading large volumes of raw material, spotting candidate structures, proposing relationships, extracting entities, summarising documents, and suggesting abstractions. Once candidates are validated and governed, they can become explicit semantic sources and compiled reusable MML views rather than remaining available only through prose or latent parameters.

### Dual Persistence

The knowledge base has two complementary persistence forms:

- **Human-readable knowledge:** notes, pages, records, explanations, provenance, contradictions, and links that people can inspect.
- **MML matrix/index:** weighted transitions, contextual paths, clusters, and pointers that machines can traverse quickly.

The detailed persistence design lives in [Dual-Persistence.md](Dual-Persistence.md). In short, the knowledge base is the durable semantic store, while the matrix/index is the fast MML navigation layer over that store.

The analogy is the [Svalbard Global Seed Vault](https://www.seedvault.no/): SOS treats knowledge as something worth preserving in readable, inspectable form. The knowledge base should behave like an improved Wikipedia shaped by knowledge engineering: notes as nodes, links as typed relationships, and schemas compatible with traditions such as Schema.org, Linked Open Data, RDF, OWL, and RDF/Turtle.

The MML matrix/index does not replace that knowledge base. It is a compiled reusable view over it and points back into its governed records. Personalized PageRank may propagate weight through one such view, but other execution strategies and composed semantic operators can use the same architectural separation.

### CML As A Query Language

CML should be thought of as the query language of the system. SQL maps human intent onto relational tables. CML maps human intent onto a shared semantic topology: concepts, relations, evidence types, abstractions, and domain-specific meanings.

MML then represents the selected intent in CML-shaped coordinates, composes the relevant semantic dimensions, and executes compiled views over that structure. CML supplies the common semantic contracts; MML makes their governed knowledge reusable and task-specific.

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

That feedback loop matters. An LLM can discover candidate structure, while accountable governance decides what becomes durable semantic representation and which compiled MML artifacts may execute it.

## How The Scripts Reflect The Architecture

The Python scripts do not define the architecture. They reflect it in miniature:

- `activate_grounded_focus.py` provides the functional contracts and initial implementations; `words_carry_weight.py` coordinates them as an operational application flow. The experiment, benchmark, and presentation modules are adapters over that flow.
- `elaborations/mml_elaborate_corpus.py` builds a richer corpus and matrix, acting as a tiny CML-shaped knowledge field.
- `elaborations/mml_legal_usecase.py` acts as the use-case layer, querying that corpus-derived field for an authored GDPR evidence problem.

The scripts are intentionally small. They showcase the architecture, not a production system.

## Dual Persistence In Depth

The detailed persistence design lives in [Dual-Persistence.md](Dual-Persistence.md). In short, SOS persists meaning twice: once as human-readable knowledge that can be inspected, governed, corrected, and linked; and once as an MML matrix/index that lets machines move quickly through the known structure.

- **Knowledge base:** durable notes/nodes, typed links, provenance, contradictions, evidence, schemas, and explanations.
- **MML matrix/index:** weighted transitions, contextual paths, clusters, and pointers into the knowledge base.
- **Seed vault principle:** established semantic identities, knowledge, evidence, constraints, and reusable structures should remain preserved in readable form.
- **Compiled-view principle:** named matrices and indexes can be rebuilt from those sources and executed repeatedly through PageRank or another declared strategy.

## Dual Engine In Depth

The detailed engine design lives in [Dual-Engine.md](Dual-Engine.md). In short, the SOS engine is dual because governed semantic capability and under-modelled language work deserve different treatment.

- **MML** represents governed semantic coordinates, compiles reusable knowledge views, composes task-specific fields, and executes them through declared strategies.
- **LLM** handles discovery, generation, ambiguity, and under-modelled situations.
- **Federation** allows many specialised MMLs and LLMs to cooperate through shared CML contracts instead of forcing one central model to own all meaning.
- **LLM detail** is grounded by [karpathy/minGPT](https://github.com/karpathy/minGPT) as a small, inspectable GPT workbench.
- **MML detail** lives in [MML-In-Depth.md](../MML-In-Depth.md), including transition learning, runtime diffusion, hybrid generation, and multi-dimensional MML fields.
- **Initiative alignment** lives in [Initiative-Alignment.md](Initiative-Alignment.md), covering minGPT, Apertus, Wikipedia/Wikidata, SEMIC, EuroVoc, Cellar/EUR-Lex, and the Svalbard seed-vault analogy.
