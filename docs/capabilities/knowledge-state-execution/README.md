# Programme 2: Knowledge State Execution

## Capability Target

> **Reconstruction-at-use versus compiled reuse.**

Knowledge State Execution asks whether established knowledge can be compiled once into governed executable state and then serve repeated queries without reconstructing equivalent task state from its source at every use.

In compact form:

```text
established knowledge
  -> compile once into governed state
  -> execute declared consequences many times
```

This is the second MML capability: **Compile knowledge.**

## What The Capability Defines

Knowledge State Execution defines:

- **per-query source reconstruction:** read or inspect the governed source and rebuild the required task state for every question;
- **compiled execution:** validate and compile the source once, then execute questions against a named immutable state;
- explicit fact, rule, identity, and composition contracts;
- inspectable execution paths back to governed source facts;
- content-addressed state and deterministic replay;
- **governed mutation:** replace or qualify a declared fact without mutating the original state;
- consequence inspection after a change;
- protected unrelated outputs;
- exact rollback or reconstruction of the original state;
- refusal for invalid, ambiguous, unsupported, cyclic, or unterminated knowledge; and
- full accounting of construction, governance, storage, execution, correction, and restoration.

The capability is more than serialization or caching. A valid implementation makes compiled semantic state inspectable, correctable, replayable, and connected to governed consequences.

## Research Question

> Across an increasing reuse horizon, when does compile-once execution preserve equivalent correct behavior while avoiding repeated source reconstruction, and what does that advantage cost end to end?

The central comparison is between semantically equivalent treatments over the same source facts and consequence rule.

## Required Treatments

The programme includes:

1. **per-query source reconstruction** over the governed facts;
2. **compiled execution** over one named immutable state;
3. **governed mutation and rollback** with dependent and protected-independent probes;
4. invalid, ambiguous, unsupported, cyclic, and missing-terminal refusal cases;
5. reuse horizons ranging from one query to many repeated queries;
6. source-size and update-frequency sweeps;
7. a future measured **language-model baseline** using the same source material and declared answer contract; and
8. cold-start, warm-reuse, correction, and restoration measurements kept separate.

The deterministic reconstruction treatment is an algorithmic baseline. It is not a proxy measurement for an LLM.

## Measurements

Report separately:

- source bytes, lexical tokens, and facts read during compilation;
- source facts or knowledge tokens reread per reconstructed query;
- source knowledge reread per compiled query;
- facts scanned, index entries built, and edges traversed;
- correctness and refusal accuracy;
- compilation, query, mutation, rollback, and end-to-end latency;
- memory and stored-state size;
- deterministic replay and snapshot identity;
- inspectable path and provenance completeness;
- dependent versus unrelated mutation consequences;
- authoring, review, validation, governance, and correction effort; and
- the reuse horizon at which one-time compilation cost is amortized, if any.

Tokens, bytes, graph operations, wall-clock time, FLOPs, energy, and human effort are different measurement families and must not be collapsed into one number.

## Current Evidence

The [Knowledge State Execution Experiment v1](results/v1.md) uses one governed-input six-fact typed-chain case and one declared `is-a*` then `belongs-to` rule.

Within that bounded fixture:

- per-query reconstruction and compiled execution return the same two declared terminal memberships;
- compiled queries reread zero source-knowledge tokens while still performing lookup and traversal work;
- execution is deterministic and exposes its path;
- a governed fact replacement changes the dependent answer;
- the unrelated answer and original immutable state remain preserved; and
- exact rollback reconstructs the original snapshot and result.

The first public-knowledge slice is reported in [Public Knowledge State v1](results/public-knowledge-state-v1.md). A frozen CELLAR snapshot of the EuroVoc *information policy* subtree (19 concepts) and its 1,503 in-force indexed legislative works is mapped through an explicit, provisional policy (`skos:broader` → `narrower-than`, `work_is_about_concept_eurovoc` → `is-about`) and compiled by `compile_subject_expansion_state`, which keeps public IRIs as identities. Compiled answers match CELLAR's own SPARQL property-path evaluation for 19/19 concepts. Every result traces to exact source triples; an out-of-scope public concept is refused; a governed exclusion changes exactly the two preregistered queries; and restoration reproduces the original snapshot identity. The slice also preserves a negative result: a parse-once cache matches the compiled state's structural work, and its bare queries are faster than evidence-carrying compiled queries. At this scale, compilation earns its place through identity, trace, refusal, and correction, not speed. Reproduce with `make public-knowledge-state-check`.

The operational capability now also exposes `CompiledIncidenceState` for many-to-many semantic membership. It compiles a governed coordinate basis into immutable postings and complete-signature equivalence classes with a separate state snapshot and construction metrics. Experiment 4.1 consumes this contract. The integrated seed demonstrates reuse of the contract, while the independent reuse curve, mutation, rollback, provenance, and public-knowledge studies form the next evidence layer.

The first relation-specific operator slice is documented in [Compiled Relation-Specific Semantic Operator](semantic-operator-design.md). It compiles governed `supports`, `requires`, and `qualifies` records into immutable sparse layers, applies an explicit versioned policy, and reuses the resulting state for repeated propagation. Its benchmark measures edge visits against a dense-cell control. This is implementation evidence for the compilation boundary, not evidence that the chosen coefficients or relation composition are semantically correct.

## Evidence Boundary And Next Validation

The current evidence is one governed-input synthetic task. It establishes local compiled reuse, mutation, replay, and rollback mechanics. The next validation adds a language-model comparison, general reasoning controls, public-knowledge cases, production-scale performance measurements, and realistic reuse horizons that include compilation, governance, update, and query costs.

## Research Layers And Next Step

- **Architectural proposition:** [Compiled Knowledge Reuse](proposition.md)
- **Experiment protocol:** [Experiment 2 — Compile Once. Execute What Is Known.](experiment.md)
- **Current evidence:** [Knowledge State Execution Experiment v1](results/v1.md)
- **Next step:** execute the preregistered reuse curve over independent and public-knowledge cases, then add a measured language-model baseline with full cost and correctness accounting.
