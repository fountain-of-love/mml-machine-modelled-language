# Research Positioning

This document positions Machine Modelled Language (MML) against adjacent ideas in modern AI. MML takes a deliberately different engineering approach: probabilistic systems are used where interpretation and discovery are valuable, while recurring semantic work is promoted into governed deterministic execution. The question is how much reliability, reuse, auditability, and efficiency this division of labour can deliver.

## The Actual Proposal

The strongest reconstruction of MML is:

> When a probabilistic system repeatedly solves the same class of semantic task, extract the recurring structure into a governed semantic operator that can be inspected, replayed, updated, rolled back, and reused. Keep probabilistic computation for language, discovery, interpretation, and genuinely novel cases.

In the current repository, that proposal has four stages:

1. Represent concepts, senses, roles, aliases, typed relations, evidence, and constraints explicitly.
2. Compile accepted structure into deterministic state: matrices, sparse relation layers, incidence state, candidate regions, and typed operators.
3. Compose governed dimensions at query time to narrow a candidate region and preserve ambiguity when the evidence does not identify one answer.
4. Route future interactions between the deterministic operator and an upstream language model or retrieval system, with fallback when the operator is not applicable.

The important unit is therefore not a graph, a matrix, or a language model. It is the operator lifecycle:

```text
probabilistic interaction
  -> recurring task class
  -> candidate operator
  -> human or policy governance
  -> deterministic execution
  -> correction, rollback, or fallback
```

MML is a semantic execution layer that complements language models, retrieval, and agents. It is designed to move recurring work into a more reliable computational substrate while preserving those systems for interpretation, discovery, synthesis, and novel cases.

## What Looks Genuinely Distinct

The distinctive contribution is the combination of four commitments:

- **Conversion as the central metric.** The programme asks what fraction of eligible interactions can move from repeated probabilistic reconstruction to governed execution, including the cost of creating and maintaining the operator.
- **Operators as governed assets.** A semantic operator has provenance, versioned policy, snapshots, correction paths, and rollback. It is treated more like inspectable infrastructure than like an opaque embedding.
- **Ambiguity is preserved as state.** The system is expected to return candidate regions, unresolved distinctions, and useful next questions instead of forcing a top-1 answer when the representation does not justify one.
- **Compilation is separated from discovery.** LLMs, experts, public sources, and evidence processes may propose or enrich structure. MML executes accepted structure and exposes its consequences.

These commitments connect established capabilities into a distinct research object: the governed conversion of probabilistic work into reusable semantic operators. The novelty claim is therefore architectural and operational. MML measures the full lifecycle and amortized value of that conversion rather than treating a graph, rules engine, or model response as the complete unit of progress.

## What Is Familiar Machinery

Several MML mechanisms map directly onto established areas:

| MML language | Closest established idea | Important difference, if demonstrated |
| --- | --- | --- |
| Governed concepts and typed relations | Knowledge graphs, ontologies, provenance graphs | MML emphasizes compilation into reusable execution state and rollback |
| Relation-specific sparse matrices | Graph propagation, label propagation, personalized PageRank | MML assigns explicit policy coefficients to typed layers |
| Candidate regions and semantic navigation | Faceted search, constraint satisfaction, active search, query refinement | MML aims to preserve ambiguity and measure the value of the next distinction |
| LLMs proposing structure and symbolic state executing it | Neuro-symbolic AI, program synthesis, tool use | MML makes operator conversion and governance the primary lifecycle |
| Reusing compiled state | Caching, memoization, materialized views, query planning | MML applies the same intuition to semantic task state |
| Sparse routing between mechanisms | Mixture-of-experts and modular systems | MML routes between computational substrates, not experts inside one neural model |

The opportunity is to show a measurable advantage from this particular composition: semantic structure is governed once, compiled into explicit state, and reused across a task stream with probabilistic systems still available at the boundary.

## Comparison With Frontier AI Approaches

### Transformers

Transformers are the strongest general-purpose substrate for language and learned representation. MML adds a complementary substrate for selected recurring semantic structure. The relevant comparison is whether a transformer plus MML can achieve lower repeated cost, higher replayability, or better auditability on a recurring task while retaining transformer capability for novel inputs.

### Retrieval-Augmented Generation

RAG retrieves documents or chunks at use time and asks a model to interpret them. MML compiles accepted semantic structure ahead of use, then executes a task-specific operator repeatedly. The approaches are complementary: RAG serves changing corpora, open-ended questions, and broad synthesis, while MML is optimized for recurring work where structure can be governed and exact provenance and repeatability matter.

### Knowledge Graphs

Knowledge graphs are the closest comparison. MML builds on graph-like structure with typed relation weights, explicit evidence, semantic navigation, and a governed execution lifecycle. The important extension is to treat compiled semantic state as a reusable operational asset with correction, replay, and rollback. The research claim is that this lifecycle can produce better task outcomes or lower amortized cost than repeatedly interpreting graph queries, graph embeddings, faceted search, or RAG results.

### Neuro-Symbolic AI

MML fits naturally within neuro-symbolic AI: neural systems can interpret language and propose structure, while symbolic or numerical operators execute governed constraints. Its contribution is to make the boundary operational: approval, provenance, update, replay, and rollback are first-class parts of the hybrid system rather than after-the-fact controls.

### Mixture-of-Experts

MoE systems sparsify computation by activating a subset of learned experts. MML applies a related efficiency principle across computational substrates: route a request to a governed operator, a retriever, a language model, or a combination. This creates a broader systems-level routing problem, evaluated through coverage, activation precision, fallback quality, and total lifecycle cost.

### World Models

MML occupies a different point in the design space from world models. World models learn predictive environments and simulate interventions; MML provides explicit, governed semantic state that could serve as a reliable substrate for world-model components, especially in domains with typed causal or temporal relations. These approaches could therefore compose rather than compete.

### Test-Time Compute and Search

MML's most interesting relationship is with test-time scaling. Tree search, self-consistency, verifier loops, and agentic planning spend more computation on each difficult query. MML asks whether recurring parts of those reasoning traces can be compiled once and reused. A strong result would show that MML converts repeated test-time work into a reusable operator while preserving probabilistic reasoning for cases outside the compiled scope.

## Current Evidence And Validation Path

The repository already supports several concrete claims:

- immutable, hashed, inspectable state is useful for deterministic replay and regression checks;
- explicit semantic identities can improve contextual focus in bounded cases;
- typed relations and sparse operators can make policy and execution inspectable;
- candidate-region navigation can represent unresolved ambiguity rather than hiding it;
- governed correction and rollback are technically plausible and already exercised in small examples;
- LLMs and experts are sensible upstream sources of candidate semantic structure.

The current evidence supports a clear validation path for the larger claims:

- rich semantic representation can make ordinary mathematics more useful on real tasks;
- compiled semantic state can reduce latency or energy after amortizing construction and governance;
- reusable dimensions can generalize compositionally beyond authored examples;
- the architecture can complement RAG and agent systems on recurring knowledge work.

MML is not intended to be universally superior to RAG, dense retrieval, knowledge graphs, agents, or test-time search. Its target is recurring, governed semantic work. The next evidence should show where the deliberate trade produces an advantage, how that advantage scales, and how MML composes with the other approaches.

## What MML Deliberately Optimizes

MML makes a deliberate architectural trade: interpretation and governance happen before runtime, while repeated execution becomes deterministic, inspectable, and reusable. The current repository is therefore best understood as a demonstration of the governed execution mechanism, with the next stage being to measure its advantage on independently sourced task streams.

Several observations should be read as design strengths rather than weaknesses:

- Authored fixtures are appropriate for establishing a curated, governed input contract. They show that once semantic structure has been accepted, MML executes it predictably and reproducibly. Independent data and task streams are still useful for measuring how broadly that contract can be applied.
- MML does not need to rediscover the same operator on every interaction. Interpretation is performed upfront, reviewed and governed once, then amortized across repeated use. The relevant comparison is therefore total lifecycle cost, including interpretation, governance, execution, correction, and reuse.
- Determinism is not a limitation of the runtime; it is the point of the runtime boundary. LLMs and other probabilistic systems can propose or interpret, while MML provides a reliable execution layer with explicit state, replay, provenance, and correction.
- The absence of a fully automatic operator-acquisition loop is a scope boundary for the current prototype, not a contradiction in the thesis. The important question is how MML should accept, review, version, and compile proposals from real task traces while keeping governance explicit.
- Strong BM25, dense retrieval, RAG, graph-query, and agent baselines are required to quantify the advantage, not to establish whether the mechanism is coherent. The central comparison should include both cold-start cost and the amortized cost of recurring work.
- “Known,” “recurring,” “semantic,” and “eligible interaction” should be operational definitions. This sharpens the applicability boundary: MML is intended for governed, repeatable semantic work, with probabilistic systems remaining available for discovery, novelty, and fallback.
- The separation between the core execution path and elaboration layer is an architectural boundary worth preserving as the system grows. Clear ownership will make the deterministic kernel easier to test, reuse, and integrate with proposal-generating systems.

The open work is therefore validation and scale: demonstrate that the upfront governed interpretation produces a measurable advantage over repeatedly inferring the same structure, and characterize the domains in which that advantage compounds.

## The Two Decisive Experiments

### 1. Operator Conversion Benchmark

Use a real recurring task stream in a bounded domain such as policy analysis, technical support, or compliance triage.

Compare:

- a strong LLM plus RAG baseline;
- the same system with an operator detector and governed MML compilation;
- routing between MML, RAG, and the LLM fallback.

The system must log the full cost of proposal, review, compilation, execution, correction, and fallback. The primary outcomes should be:

- deterministic interaction share;
- end-to-end cost and latency, including governance amortization;
- answer quality and calibration;
- exact replay rate and regression rate after updates;
- false operator creation and missed recurring-task opportunities;
- human approval time;
- performance as the task stream becomes more repetitive or more novel.

This experiment directly tests whether MML converts recurring probabilistic work into a practical systems advantage.

### 2. Independent Semantic Navigation Challenge

Build the same navigation task over an independently sourced entity state, at increasing scales such as 1,000, 10,000, and 100,000 entities. A public knowledge graph or domain corpus can provide the source, but the evaluation split and query set must be frozen before tuning.

Compare MML against BM25, dense retrieval, RAG, graph embeddings, direct graph queries or faceted search, and an LLM agent. Measure retrieval quality, abstention, ambiguity handling, provenance, update locality, replayability, query latency, and the cost of adding new dimensions. Include held-out compositions and adversarially similar distractors.

This experiment tests how well MML's representation and navigation claims transfer to independently sourced data while preserving the governed-input contract.

Together, these experiments would establish MML as a distinct systems contribution rather than merely another graph representation. The first tests conversion economics. The second tests transfer, navigation quality, and competitive utility.

## Plausible Research Positioning

The strongest role fit is at the intersection of:

- AI systems research;
- research engineering for agent and knowledge infrastructure;
- neuro-symbolic or hybrid reasoning systems;
- semantic and knowledge architecture;
- evaluation and governance infrastructure for AI.

A concise positioning line is:

> I work on converting recurring LLM-mediated knowledge work into governed deterministic semantic operators, with provenance, replay, update, rollback, and ambiguity-preserving navigation.

That claim is technically credible as a systems research agenda with explicit baselines, lifecycle accounting, and clear applicability boundaries. It becomes much stronger when the two experiments above report independent data, full lifecycle costs, and selective fallback behaviour.

## Reference Anchors

- [Attention Is All You Need](https://arxiv.org/abs/1706.03762)
- [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)
- [Switch Transformers](https://arxiv.org/abs/2101.03961)
- [Neuro-Symbolic AI: The State of the Art](https://arxiv.org/abs/2105.05330)
- [Tree of Thoughts](https://arxiv.org/abs/2305.10601)
- [World Models](https://arxiv.org/abs/1803.10122)
