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

The capability is not merely serialization or caching. A cache of expected answers, opaque serialized model, or hidden behavior table would not demonstrate compiled semantic state with inspectable governed consequences.

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

The [Knowledge State Execution Experiment v1](results/v1.md) uses one authored six-fact typed-chain case and one declared `is-a*` then `belongs-to` rule.

Within that bounded fixture:

- per-query reconstruction and compiled execution return the same two declared terminal memberships;
- compiled queries reread zero source-knowledge tokens while still performing lookup and traversal work;
- execution is deterministic and exposes its path;
- a governed fact replacement changes the dependent answer;
- the unrelated answer and original immutable state remain preserved; and
- exact rollback reconstructs the original snapshot and result.

## Evidence Boundary

The current evidence is one co-authored synthetic task. It is not a language-model comparison, general reasoning, public-knowledge demonstration, production-scale performance result, or universal efficiency claim. A single short reuse horizon cannot establish amortization across realistic compilation, governance, update, and query costs.

## Research Layers And Next Step

- **Architectural proposition:** [Compiled Knowledge Reuse](proposition.md)
- **Experiment protocol:** [Experiment 2 — Compile Once. Execute What Is Known.](experiment.md)
- **Current evidence:** [Knowledge State Execution Experiment v1](results/v1.md)
- **Next step:** execute the preregistered reuse curve over independent and public-knowledge cases, then add a measured language-model baseline with full cost and correctness accounting.
