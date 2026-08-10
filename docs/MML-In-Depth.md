# MML In Depth

This document focuses on **Machine Modelled Language (MML)** itself: how its explicit representation is constructed and statistically updated, how it executes, why embeddings still matter, and how it can evolve into a multi-dimensional field.

This document describes the executable innovation independently. If that mechanism proves useful, it opens the door to the proposed [dual engine](sos/Dual-Engine.md), [Semantic Operating System](sos/Architecture.md), and [dual persistence](sos/Dual-Persistence.md) architecture.

## MML Initialization: Construction Phase

MML begins with an explicit semantic construction: concepts, aliases, relation types, evidence, and sense distinctions that the machine can execute. The current prototype uses a small local vocabulary and governed records; it does not require the wider SOS architecture to operate.

A future **Common Language Model (CML)** would standardize these semantic contracts across knowledge bases, institutions, MML engines, and applications. CML is therefore a downstream interoperability architecture opened by MML, not a prerequisite already delivered by this prototype.

The current benchmark already uses separate construction nodes for the two tested senses:

- `bank_financial`: financial institution
- `bank_river`: land beside a river

Surface `bank` is resolved from accompanying signals to one or both sense nodes. A production model would extend that small authored mapping through public lexical identifiers rather than force every meaning to emerge from raw statistics.

## Existing Initiative Alignment

MML is not proposed in isolation. Several existing initiatives already point toward parts of the system: small inspectable neural workbenches, sovereign AI pipelines, and long-term preservation models for shared knowledge.

Those initiative alignments are described separately in [Initiative-Alignment.md](sos/Initiative-Alignment.md), including [minGPT](sos/Initiative-Alignment.md#mingpt-small-neural-workbench-for-discovery), [Apertus](sos/Initiative-Alignment.md#apertus-sovereign-ai-pipeline), and the [Svalbard Global Seed Vault](sos/Initiative-Alignment.md#svalbard-global-seed-vault-preservation-analogy) analogy.

## MML Transition Probabilities: Statistical Update Phase

Raw text can be passed through the graph to measure how often one node appears near another in natural context. Those observations update explicit weights; they do not constitute neural training.

If concept `A` repeatedly appears near concept `B`, the edge from `A` to `B` becomes stronger. After normalization, those counts populate a sparse transition matrix `P`.

This is the first literal sense in which words carry weight: addressable words or concepts occupy the matrix, and their structured relationships hold numerical transition weight. The scalar belongs to an edge in a governed snapshot rather than to a word as an eternal, context-free measure of importance.

That is exactly what the code does here at toy scale:

```python
co_occurrence[target_idx, neighbor_idx] += 1.0
P = co_occurrence / row_sums
```

The difference is that a production architecture would update transitions between dictionary-grounded sense nodes rather than plain surface words.

## MML Execution: Runtime Phase

When a user enters a query, the system maps the input tokens onto the designed knowledge representation: graph nodes, sense candidates, ontology links, and contextual edges. Those activated nodes become the teleportation vector `v`.

In the current script, querying `river` creates a vector where all probability mass starts at the `river` index:

```text
v_river = 1.0
```

The benchmark engine then runs a fixed number of local propagation steps:

```text
pi_next = d * (pi @ P) + (1 - d) * v
```

The resulting activation distribution assigns weight to nodes reachable within the declared execution horizon. It deliberately stops after a bounded number of steps rather than converging to a stationary distribution, which helps preserve local query structure. Multiple query fields are propagated independently and combined through a normalized geometric mean. This is graph activation, not transformer attention and not proof that the representation understands the query.

The combination implements **[combinatorial uniqueness](Combinatorial-Uniqueness.md)**: individually broad conceptual fields can form a narrow intersection when they impose distinct constraints. A combination can therefore carry greater discriminative weight than any participating term alone, because a candidate must retain support across the independently propagated fields. This is related to established conjunction, faceted search, and product-of-experts ideas. MML's specific contribution is to execute that intersection over governed, addressable semantic identities and relations.

The minimal script still demonstrates conventional personalized PageRank convergence. That historical demonstration should not be confused with the bounded `GraphModel` used by the development benchmark.

## Governed Typed Relations

Co-occurrence means only that terms appeared nearby. It cannot by itself express whether evidence supports, contradicts, requires, or qualifies a concept. The next representation layer therefore uses a deliberately small governed vocabulary:

- `supports`;
- `contradicts`;
- `requires`;
- `qualifies`.

Governed aliases resolve longest-match first, consuming a mapped phrase once. Positive relation weights use explicit type multipliers: `supports = 1.0`, `requires = 0.8`, and `qualifies = 0.5`. Contradictions remain a separate negative scoring layer; negative weights never enter the row-stochastic transition matrix. Relation identity, type, endpoints, weight, evidence references, jurisdiction, validity, confidence, maturity, and review state remain inspectable. Co-occurrence-only and typed variants are reported separately so a gain can be attributed through ablation.

This layer is not a declaration of legal truth. It executes provisional authored assertions whose source and governance state must remain visible.

## Explanations And Identity

An execution can report resolved concepts, positive and negative score components, strongest paths, typed relation identifiers, evidence references, and a deterministic graph snapshot. These are related but distinct guarantees:

- path validity shows that an executed route exists;
- provenance connects an edge to its source artifact;
- causal decomposition proves how reported contributions produce the final score.

The current mechanism must label unavailable guarantees instead of treating a strongest path as complete causal proof.

The snapshot identity is derived from construction sources, relation artifacts, graph configuration, vocabulary version, and algorithm version. This provides deterministic replay before publication. Once public Git history exists, the governing commit or tag additionally identifies the human review state.

## Why We Still Need Embeddings: A Pragmatic Trade-Off

Pure graph diffusion over a dictionary has strong advantages: efficiency, factual stability, inspectability, and resistance to noisy training data. But classical graph methods have historically struggled with compositional fluid syntax.

Human language is not only meaning lookup. It also involves grammar, style, metaphor, idioms, tone, and multi-word constructions. Deep neural networks are good at these soft, fluid patterns because embeddings and attention can represent graded similarity and composition in ways that fixed symbolic graphs often cannot.

That suggests the most promising immediate architecture is not pure graph reasoning and not pure dense neural generation. It is a Hybrid Graph-Transformer.

## Hybrid Graph-Transformer

**The Graph Engine: MML Diffusion And Dictionary**

The graph engine handles semantic routing, context retrieval, factual grounding, and candidate token or concept weighting. It is cheap, sparse, inspectable, and resistant to drift because knowledge lives in nodes and edges rather than only in neural weights.

**A Mini-Transformer Head**

A smaller Transformer can take the top candidate nodes from the graph engine and perform lightweight local generation for grammar, syntax, and natural phrasing.

In this design, the Transformer does not carry the full burden of memorizing and retrieving semantic knowledge. The graph engine narrows the semantic field first, then a smaller neural model composes the final language.

## Next Evolutionary Step: Multi-Dimensional MML Field

The current Python script uses one flat graph: a single transition matrix `P` built from word co-occurrence. A richer model would need more than one kind of relationship.

The next evolutionary step is to expand from a single graph to a multi-dimensional graph structure. This turns the design into a Multiplex Network, also known as a Heterogeneous Information Network.

This tensor or multiplex engine is a proposed deterministic extension, not a current feature. Given identical layer sources, identifiers, weights, build algorithm, parameters, and execution settings, it should compile to the same tensor and produce the same activation result. That reproducibility must be tested rather than assumed. Sparse execution cost, cross-layer normalization, typed path semantics, and deterministic build artifacts are part of the future implementation contract.

Instead of one flat transition matrix, the engine operates on a 3D tensor:

```text
T in R^(M x N x N)
```

Where:

- `N` is the node universe: vocabulary, concepts, entities, facts, and candidate tokens.
- `M` is the number of relational layers or dimensions.
- Each `N x N` slice is a different kind of transition matrix.

In the current script, `P` is one `N x N` matrix. In the multi-dimensional version, `P` becomes one layer inside a larger tensor `T`.

## The Multi-Dimensional Layer Topology

Each dimension in the tensor encodes a fundamentally different type of human logic:

```text
[Layer 1: Lexical / Synonyms] -> WordNet / Synsets
             |
             |  Inter-layer jumps
             v
[Layer 2: Ontology]           -> Taxonomic hierarchies: IS-A, PART-OF
             |
             v
[Layer 3: Epistemic / Facts]  -> Relational triples: Subject-Predicate-Object
             |
             v
[Layer 4: Topological Syntax] -> Statistical co-occurrence and spatial distance
```

**Layer 1: Lexical And Synonyms**

This layer handles vocabulary mapping. It ensures that words such as `car`, `automobile`, and `vehicle` share high edge capacity without requiring trillions of text examples to rediscover that relationship.

**Layer 2: Ontology**

This layer stores structural hierarchies, such as `Apple IS-A Fruit` or `iPhone IS-A Consumer Electronic`. It acts as a semantic guardrail against category confusion.

**Layer 3: Epistemic And Fact Triples**

This layer stores real-world assertion graphs, such as `CEO_of`, `Located_in`, `Founded_by`, or `Causes`. It is the layer most likely to change as the world changes.

**Layer 4: Topological Syntax**

This layer captures linear sequence, positional distance, and statistical co-occurrence from raw training text. The current Python script lives mostly in this layer: its sliding-window co-occurrence matrix is a tiny version of topological syntax.

## Step-By-Step Architecture Pipeline

### 1. Input Tokens To Disambiguated Query Mapping

Raw tokens are passed through a lightweight parser that identifies entities, parts of speech, and candidate synsets. Instead of mapping a token to a single vector, it activates a multi-layer teleportation vector:

```text
v = [
  v_lexical,
  v_ontology,
  v_epistemic,
  v_syntax
]
```

For example, if the input is `apple stock`, the mapper might inject most of the teleportation weight into `Ontology:FinancialAsset` and `Lexical:Apple_Inc`, while setting `Ontology:Fruit` close to `0`.

This is the multi-layer version of what the current script does here:

```python
v[word2idx[target_word]] = 1.0
```

### 2. Multi-Dimensional MML Diffusion Engine

The engine computes random walks that move both intra-layer, within a single dimension, and inter-layer, jumping between dimensions.

Conceptually:

```text
pi_next = d * sum_over_layers(Omega_alpha * P_alpha * pi_alpha) + (1 - d) * v
```

Where:

- `P_alpha` is the transition matrix for layer `alpha`.
- `Omega_alpha` controls cross-layer navigation and layer weighting.
- `d` is the damping factor.
- `v` is the multi-layer teleportation vector.

### 3. Bounded Propagation To A Structured Activation Field

The planned multiplex executor should preserve the benchmark's bounded, query-local semantics unless an experiment explicitly demonstrates that convergence is preferable. It returns a unified activation field after a declared number of steps:

```text
pi_steps
```

In the current benchmark, `pi` assigns contextual weight to words and concepts. In the multi-dimensional model, `pi_steps` would assign contextual weight to word senses, ontology classes, factual triples, and generation candidates.

## How This Solves AI's Core Bottlenecks

| Current LLM Challenge | Multi-Dimensional MML Field Solution |
| --- | --- |
| Model Drift And Knowledge Decay | Layer isolation: if facts change, update Layer 3, the epistemic layer, by adding or deleting specific edges. Layer 1, synonyms, and Layer 2, ontology, remain undisturbed, reducing the risk of catastrophic forgetting. |
| Energy And Compute Expense | Sparse tensor multiplication: the engine executes Sparse Matrix-Vector Multiplications across multiple sparse matrices instead of relying only on dense float32 matrix operations. This can run efficiently on CPUs or hardware optimized for graph traversal. |
| Hallucination And AI Slop | Dynamic damping control: for legal, medical, or safety-sensitive queries, the engine can increase the weight of verified ontology and fact layers while reducing reliance on raw co-occurrence. This biases the model toward structured knowledge. |
| Black Box Behavior And Unexplainability | Inspectable execution can expose activated layers, graph paths, and their source records. Complete causal attribution remains a separate requirement rather than an automatic property of a non-zero value. |

The simple demo asks: what words carry contextual activation weight when execution is anchored on these query tokens? The proposed CML-shaped multiplex version asks the larger question: what concepts, abstractions, facts, senses, and words carry weight when MML is anchored across several kinds of governed knowledge at once? CML supplies their stable semantic identities and typed relationships; a compiled MML matrix supplies numerical transition weight; query execution supplies contextual activation weight.

## Authored Structure And Statistical Weights

MML deliberately combines authored semantic structure with corpus-derived statistics. Identifiers, definitions, relation types, evidence, constraints, contradictions, and governance states belong to the human-governed layer. Co-occurrence counts and transition weights belong to the statistical layer. Every durable update should preserve its source and history. See [Research-Contract.md](Research-Contract.md) for the evidence boundary and [Commons-Governance.md](sos/Commons-Governance.md) for provenance expectations.

Improvements are accepted from evidence, not intuition alone. The development benchmark first records a co-occurrence baseline, then adds one mechanism family at a time. Supported semantic-slice gains must survive hard-negative, regression, explanation, replay, localized-update, rollback, and ablation checks. See [benchmark/README.md](benchmark/README.md).

The active retrieval diagnostic keeps co-occurrence and typed MML separately named, making their behavior visible without turning ranking into the definition of MML. The broader ablation, sensitivity, and hybrid experiments remain available in the [archived research note](benchmark/archive/v1-retrieval-research.md). They are development observations rather than universal algorithmic claims.
