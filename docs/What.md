# What MML Is

Machine Modelled Language (MML) is an **executable, weighted knowledge representation whose human-governed structure can be updated from text statistics**. Its central proposition is that progress may come not only from more complicated computation, but from a representation of meaning rich enough for established mathematical structures to do more useful work. Language is represented as addressable concepts, senses, semantic roles, aliases, relationships, and transition weights; queries activate that structure through deterministic matrix operations whose relational routes can be interpreted as a graph.

The inversion is intentional:

> **An LLM models language inside a machine; MML models language for operation by a machine.**

An LLM may help discover, map, or express knowledge. MML gives validated semantic structure a durable home outside opaque parameters so it can be inspected, corrected, rebuilt, and reused.

## What “Words Carry Weight” Means

MML separates what happens before execution from what happens during execution. **Focus is representational narrowing**: an ambiguous expression such as `bank` is mapped to a more precise identity such as `bank_river`. **Activation is the numerical distribution produced after a query strategy executes from that focused identity.** The kernel therefore returns `Activation`, not `Focus`. Attention remains an inspiration-level analogy; it does not name Personalized PageRank, matrix propagation, or another implemented MML mechanism.

The construction-side complement to focus is **semantic grounding**: a surface occurrence of `bank` in the corpus is identified as `bank_river` before compilation. Grounding and focus are two ingress paths converging on the same governed semantic identity—corpus to identity and query to identity—not inverse functions. Rendering an identity back into surface language would be a separate lexicalization operation.

The phrase begins literally in the executable representation. Words or governed concepts occupy nodes in a weighting matrix, while their relationships supply transition weights. Corpus observations and governed typed relations determine how strongly activation can move from one node to another. At query time, the resulting activation distribution assigns contextual weight to the nodes supported by the query and its reachable structure. A word therefore does not own one permanent importance score; it carries weight in relation to other nodes, a named snapshot, and the current query.

The proposed **Common Language Model (CML)** extends the same idea beyond surface words. Stable senses, conceptual terms, abstractions, facts, evidence types, and constraints become addressable semantic identities. Once compiled into an MML matrix or index, these conceptual nodes and their typed relations can carry transition and activation weight too. “More weight” here means stronger governed or contextual support in a particular execution—not an assertion that an abstract concept is universally more important than a concrete word.

CML also lets a concept occupy a semantic role. `capacity`, `activation`, `boundary`, `substrate`, `gain`, and `storage`, for example, can provide comparable coordinates across domains without claiming that the physical quantities filling those roles are identical. In that list, `activation` names a governed scientific role; `Activation` in the Python kernel names a query result. The qualification and capitalization prevent those two uses from silently merging. Role is therefore part of the representation, not merely another untyped association.

## From One Matrix to Semantic Operators

“Graph” and “matrix” describe two views of the same current mechanism, but they are not interchangeable implementation claims. The graph view names concepts and relations and makes routes explainable. The matrix is the compiled numerical object that the Python code actually executes.

The current prototype combines corpus co-occurrence with the positive governed relations `supports`, `requires`, and `qualifies` in one normalized transition matrix. `contradicts` remains outside that positive matrix as an explicit negative scoring contribution. This is a useful seed, not the intended endpoint.

A richer MML should preserve relation semantics in a family of matrices, for example:

```text
S = synonymy             H = hierarchy
O = opposition           P = part/whole
C = causality            R = role correspondence
A = association          T = temporal relation
```

A task can then construct an operator such as:

```text
M = alpha*A + beta*S + gamma*H + delta*P + epsilon*C + zeta*R - eta*O
```

followed by the normalization appropriate to the execution contract. The coefficients are governed semantic-policy decisions: a legal evidence task, a scientific analogy task, and a lexical disambiguation task need not value the same relation types equally. Execution therefore activates a semantic field shaped by both the governed conceptual model and the declared task policy.

This makes the phrase literal at three levels: relations carry stored transition weight; task policy determines how relation families contribute; and query execution assigns contextual activation weight to the resulting field.

**[Combinatorial uniqueness](Combinatorial-Uniqueness.md)** adds another dimension. A broad concept may carry little discriminative weight alone, while several broad but sufficiently independent concepts form a narrow intersection. `attention + systems theory + ranking`, for example, identifies a more distinctive semantic region than any term by itself. MML executes those fields independently and combines their support, so weight emerges not only from individual nodes but from the structured relation between conceptual coordinates.

## Governed Meaning Made Executable

MML is intentionally supervised semantic construction. People and institutions define stable concepts, sense identities, aliases, typed relations, provenance, and corrections. Corpus statistics adjust explicit weights inside that governed structure. MML therefore does not claim to discover meaning autonomously; it makes curated meaning executable and contestable.

For example, MML does not have to treat `bank` as one undifferentiated token. Governed identities such as `bank_financial` and `bank_river`, their aliases, relations, and the query context make the intended sense addressable. The current prototype demonstrates this distinction directly.

The evidentiary relationship runs in one direction: **MML is the executable innovation demonstrated in this repository. Its ability to preserve and run governed semantic structure motivates Common Language Model (CML) contracts and a wider Semantic Operating System (SOS).** Those downstream proposals are not evidence that MML works.

## Current Evidence and Proposed Direction

The current Python prototype demonstrates:

- governed concepts, aliases, and typed relations;
- deterministic construction and query activation;
- bounded matrix propagation and inspectable relation paths;
- content-addressed snapshots;
- local updates and exact rollback;
- an authored semantic-identity benchmark under fixed mathematics;
- a small legacy retrieval diagnostic beside lexical baselines.

It does not yet demonstrate:

- general semantic understanding or autonomous concept discovery;
- complete logical or multi-hop reasoning;
- relation-specific matrix composition or a complete multi-layer executor;
- production integrity, regulatory compliance, or representative coverage;
- a complete SOS runtime or competitive equivalence with a language model.

See [How](How.md) for the executable mechanics and the [research contract](Research-Contract.md) for the exact claim boundary.

## Why the Wider Comparison Matters

The proposed SOS architecture does not expect one mechanism to solve every problem. It separates responsibilities that a monolithic language model often blends: semantic interpretation, knowledge prioritisation, evidence retrieval, and language generation.

> **A modular SOS pipeline may approximate selected observable LLM behaviours—such as semantic retrieval, evidence-based answering, routing, explanation, and linguistic rendering—without reproducing an LLM's internal mechanism or general capability.**

The complete proposition is described in the [Four-Tier Modular Pipeline](sos/Four-Tier-Modular-Pipeline.md).

| System | Primary representation | Main mechanism | Role in the modular stack | Current limitation |
| --- | --- | --- | --- | --- |
| **TF-IDF / BM25** | Sparse term vectors over notes or chunks | Frequency-weighted lexical matching | Precise and inexpensive surface-language evidence | Semantic equivalence requires stemming, aliases, or query expansion |
| **Dense retrieval** | Learned vectors over notes or chunks | Geometric similarity in embedding space | Fuzzy semantic recall across different wording | Similarity dimensions and boundaries are mostly implicit |
| **Note-level PageRank** | Linked notes, sources, or documents | Propagation over record topology | Authority, connectedness, and provenance context | Topological importance is not query relevance or truth by itself |
| **MML** | Governed concepts, senses, aliases, and typed relations | Deterministic activation and bounded graph diffusion | Explicit semantic identity, concept intersections, opposition, and inspectable routes | Requires supervised construction and lacks complete logical reasoning |
| **RAG** | Retrieved terms, vectors, records, graphs, or combinations | Retrieval followed by a generative or extractive consumer | Grounds output in external knowledge and can use every index above | Results depend on retrieval, evidence assembly, generation, and verification controls |
| **SOS direction** | Governed knowledge plus disposable lexical, concept, dense, and note-graph indexes | Evidence fusion followed by templates or a small language model | Combines the specialised mechanisms while keeping knowledge external | Proposed architecture; the fused engine and minGPT comparison are not implemented |

## Reproducibility and Auditability

For the same normalised sources, governed records, algorithm version, and execution settings, the current MML construction produces the same weights, snapshot, activation, and ranking. This is **deterministic reproducibility**, an important component of auditability—not total auditability by itself.

Complete auditability also requires provenance, logging, validation, documented limitations, human oversight, and governance. This distinction matters wherever accountable AI is expected. In Europe, the EU AI Act emphasises technical documentation and traceability for applicable high-risk systems. MML's reproducible construction may support such an evidence base, but determinism alone neither provides complete auditability nor establishes legal compliance ([Regulation (EU) 2024/1689, Articles 11–12](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)).

Transformer training is ordinarily stochastic: repeating a training run can produce different learned weights unless randomness and the full environment are tightly controlled. Fixed-weight inference can nevertheless be repeatable with deterministic decoding. The relevant distinction is reproducible construction and execution, not “graphs are deterministic while transformers can never be.”

## A European Question

Externalising semantic structure raises a broader question: who can inspect, maintain, connect, and reuse it? Public identifiers, institutional governance, and interoperability become part of the design when knowledge is treated as shared infrastructure rather than confined to model parameters.

Europe—with its multilingual communities, public knowledge institutions, Linked Open Data initiatives, and emphasis on accountable digital systems—provides one relevant setting for that exploration:

> **Can Europe organise its knowledge as linked, executable semantic infrastructure that remains inspectable and governable?**

The wider ambition is to help Europe evolve with AI, participate in shaping that transformation, remain economically competitive, and explore a more sustainable alternative to concentrating knowledge and capability in ever-larger models. This is a motivating societal question, not a result established by the repository.

The proposed next experiment is correspondingly bounded: take one Linked Open Data vertical slice, begin from public URIs, compile their governed relations into an MML snapshot, execute one use case, and trace every result back to its identifiers and sources.

## Continue Reading

- [Why](Why.md) develops the sustainability and architectural motivation.
- [How](How.md) documents what the prototype actually executes.
- [MML in depth](MML-In-Depth.md) covers the mechanism and proposed evolution.
- [Research contract](Research-Contract.md) separates evidence from aspiration.
- [SOS architecture](sos/README.md) contains the downstream system design.
