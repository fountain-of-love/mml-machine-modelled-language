# MML Vocabulary

This page is the canonical layer map for the repository. It keeps the names of
the knowledge substrate, executable runtime, research programme, and wider
architecture distinct while showing how they compose.

## The Layer Map

```text
governed sources and expert / LLM proposals
        |
        v
Common Language Model (CML)
shared semantic schema: identities, roles, relations, evidence, constraints,
maturity, provenance, and topology
        |
        v
Semantic Seed Vault
durable, human-readable governed knowledge organized through CML
        |
        v
MML compiler and runtime kernel
representation -> compilation -> composition -> deterministic execution
        |
        v
MML research programme
controlled studies of representation, reuse, composition, and navigation
        |
        v
Semantic Operating System (SOS)
broader composition of MML, LLM discovery and rendering, retrieval, governance,
persistence, and application interfaces
```

## Canonical Definitions

| Term | Canonical meaning | Repository surface |
| --- | --- | --- |
| **CML** | Common Language Model: the shared semantic schema for governed meaning. | Proposed in [`What.md`](What.md) and the [`sos/`](sos/README.md) architecture. |
| **Semantic Seed Vault** | The durable knowledge substrate that stores concepts, roles, relations, equations, evidence, provenance, maturity, and competing interpretations in readable form. | [`explorations/seed-vault/`](explorations/seed-vault/README.md) |
| **MML** | Machine Modelled Language: the executable semantic approach that compiles governed structure into reusable operators and composes it at runtime. | This repository as a whole; the foundation is defined in [`What.md`](What.md). |
| **MML runtime kernel** | The reusable deterministic mechanics that represent identities, compile state or operators, execute declared strategies, preserve provenance, and support correction or replay. | [`src/`](../src/) |
| **MML research programme** | The independently testable sequence of semantic representation, Knowledge State Execution, Combinatorial Uniqueness, and accumulated Semantic Navigation. | [`capabilities/`](capabilities/README.md) |
| **Experiments** | Governed-input evidence adapters that load fixtures, run controls, measure behavior, and publish artifacts and reports. | [`experiments/`](../experiments/) |
| **Elaborations** | Richer graph, provenance, trace, and application-shaped mechanics that extend the minimal kernel through an explicit adapter layer. | [`elaborations/`](../elaborations/) |
| **SOS** | Semantic Operating System: the proposed broader architecture that composes MML with LLM discovery and rendering, retrieval, persistence, governance, and user-facing applications. | [`sos/`](sos/README.md) |
| **LLM** | Large Language Model: a probabilistic system used upstream or alongside MML for discovery, interpretation, open-ended reasoning, and language rendering. | [`sos/Dual-Engine.md`](sos/Dual-Engine.md) |

## The MML Contract

MML is best understood as a lifecycle rather than a single algorithm:

```text
represent governed meaning
        -> compile reusable executable state
        -> compose eligible semantic coordinates
        -> execute deterministically
        -> inspect, correct, version, and replay
```

PageRank, sparse matrices, graph traversal, soft intersection, and
relation-specific operators are implementation strategies or operator forms
beneath this contract. None alone defines MML.

## Runtime Versus Discovery

The architecture deliberately separates two flows:

- **Discovery:** LLMs, experts, public sources, and observatories propose or
  interpret candidate structure; governance decides what becomes CML-shaped
  knowledge.
- **Runtime:** MML compiles accepted structure and executes the eligible
  deterministic operation, preserving ambiguity or refusing when the governed
  state does not license a conclusion.

This division is the central engineering choice. Probabilistic systems remain
valuable where interpretation and novelty are required. MML provides the
reliable execution boundary for represented and governed recurring work.

## Evidence Vocabulary

- **Governed-input development evidence:** authored or curated inputs used to
  validate mechanism conformity, reproducibility, refusal, correction, and
  replay.
- **Held-out evidence:** probes authored after the governed state or operator
  has been frozen.
- **Independent evidence:** inputs, reviewers, or domains separated from the
  construction process.
- **Production evidence:** measurements from operational workloads, cost,
  latency, reliability, and human outcomes.

These categories are complementary. A governed-input fixture is not weakened
by being authored; it answers a mechanism question. Held-out and production
studies answer different questions about transfer and operational value.
