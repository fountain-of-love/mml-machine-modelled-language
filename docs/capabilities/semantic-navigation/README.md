# Programme 4: Semantic Navigation

## Capability Target

> **Navigate governed knowledge.**

Semantic Navigation asks whether the first three MML capabilities can accumulate into a useful interaction surface over an explicit knowledge domain.

```text
represent governed coordinates
  -> compile persistent knowledge state
  -> compose coordinates into a candidate region
  -> navigate ambiguity without inventing specificity
```

This is the fourth MML research stream. Unlike the first three, it is intentionally cumulative. It studies whether their contracts compose into useful retrieval, diagnosis, and interaction.

## Why This Is A Separate Stream

Exact encyclopaedic retrieval is not itself evidence for the Combinatorial Uniqueness proposition. A correct multidimensional index and a flat scan should return the same compatible set. The research question is instead whether represented, compiled, and composed knowledge produces a reusable navigation substrate with explicit uncertainty and favorable repeated-use behavior.

Programme 4 must therefore preserve two boundaries:

1. It may consume evidence-backed capabilities from Programmes 1–3.
2. Its success does not retroactively validate claims that those programmes have not independently established.

## Capability Contribution Table

| Capability | Current contribution available to Programme 4 | What the current capability still lacks | Programme 4 integration contract |
| --- | --- | --- | --- |
| **1. Semantic Representation** | Governed identities, explicit distinctions, query focus, deterministic representation, and the principle that labels and meaning must not be conflated. | The v1 implementation is corpus- and co-occurrence-oriented. It lacked a reusable finite dimension/value basis, dimension-qualified value identities, incomplete-record validation, and reversible compact codes. | `GovernedCoordinateBasis` validates entities and recurring dimensions, distinguishes values such as `habitat:woodland` from unrelated uses of `woodland`, reports missing fields, and projects labels into stable codes. |
| **2. Knowledge State Execution** | Compile-once execution, immutable content-addressed state, deterministic replay, reconstruction controls, governed change, rollback, and cost-family separation. | The v1 executable state permits one outgoing `is-a`/`belongs-to` chain per subject. It could not represent many-to-many entity/attribute membership or postings required by multidimensional retrieval. | `CompiledIncidenceState` compiles the governed basis once into immutable coordinate postings and complete-signature equivalence classes while retaining basis and state snapshot identities. |
| **3. Combinatorial Uniqueness** | Independent coordinates, exact incidence intersections, candidate narrowing, structural information, explicit unsupported regions, and the rule that insufficient information must remain insufficient. | The main flow couples exact incidence with graph activation, soft scoring, fixture policy, and resolution thresholds. It lacked a small exact candidate-region operator reusable by downstream applications. | `compose_candidate_region` intersects compiled postings, returns the complete compatible region, preserves empty and non-unique regions, and reports deterministic execution work. |
| **4. Semantic Navigation** | New accumulated capability: status, equivalence classes, deterministic imputation, remaining partitions, information-gain questions, commonality, and interaction-ready evidence. | The seed has no independently sourced ontology, natural-language parser, relational inference, measured wall-clock study, or governed update workflow over the animal state. | `SemanticNavigationFlow` coordinates the three upstream contracts and adds navigation only after exact composition. |

## Source Architecture

```text
src/semantic_representation/governed_coordinates.py
    GovernedCoordinateBasis, SemanticEntity, label/code projection
                         |
                         v
src/knowledge_state_execution/compiled_incidence.py
    CompiledIncidenceState, postings, signatures, snapshot, build cost
                         |
                         v
src/combinatorial_uniqueness/candidate_regions.py
    CandidateRegion, exact coordinate composition, query cost
                         |
                         v
src/semantic_navigation/navigation.py
    SemanticNavigationFlow, ambiguity status, imputation, distinctions,
    next question, commonality, identification depth
```

The dependency direction is one-way. Upstream capabilities do not import Semantic Navigation, and the experiment adapter does not define operational semantics.

## Research Question

> Can independently governed semantic dimensions, compiled once into persistent state and composed at query time, support exact retrieval and useful ambiguity navigation with less repeated execution work than reconstructing or scanning the same knowledge?

## What The Capability Defines

Semantic Navigation defines:

- exact candidate-region retrieval from any supported subset of dimensions;
- `IDENTIFIABLE`, `AMBIGUOUS`, and `UNSUPPORTED` outcomes based on region cardinality;
- construction-time detection of incomplete governed records;
- deterministic imputation only where all candidates agree;
- minimum dimension sets required to isolate each complete-signature equivalence class;
- information-gain selection of the next distinguishing dimension;
- explicit prior entropy, expected posterior entropy, information gain, normalized gain, and missingness for every eligible dimension;
- overlapping governed lenses that constrain the eligible next questions without creating separate knowledge states;
- commonality queries over selected candidate sets;
- behaviorally equivalent label and compact-code execution;
- inspectable contribution and snapshot identities from all upstream capabilities; and
- cold compilation, warm execution, reconstruction, scanning, storage, and amortization accounting.

It does not define natural-language understanding or infer facts absent from governed state.

## Current Evidence

[Experiment 4.1](results/compiled-encyclopedic-navigation-v1.md) is a prompt-provided 60-animal mechanics seed. It exercises the accumulated source path and reports exact retrieval, navigation correctness, code equivalence, incomplete-record diagnostics, equivalence-class resolution, and deterministic operation scaling.

The [layered Canidae source-backed seeds](animal-encyclopedic-navigation-seed.md) begin the data-governance path for Experiment 4.2 with a shared 12-species registry, a 13-dimension ecology-behavior field, and a separate six-dimension zoological-detail field. Claim provenance and unsupported cells remain explicit, while detailed measurements cannot shape the foundational navigation result.

The [Canidae dimension and measurement review](results/canidae-dimension-review-v0-2.md) reports ecology-behavior information contribution separately from the optional PanTHERIA body-length review.

## Evidence Boundary

The current fixture is not independently sourced zoological evidence. Programme 4 does not establish the quality of its canonical animal annotations, production performance, natural-language translation, relational inference, or independent generalization. The planned 100/250/500-animal study must source, review, govern, and freeze its records before evaluation.

## Research Layers And Next Step

- **Experiment blueprint:** [Experiment 4.1 - Compiled Encyclopedic Navigation](experiment.md)
- **Dimension study blueprint:** [Experiment 4.2 - Lens-Aware Dimension Contribution](dimension-contribution-experiment.md)
- **Mechanics evidence:** [Compiled Encyclopedic Navigation v1](results/compiled-encyclopedic-navigation-v1.md)
- **Dimension contribution evidence:** [Layered Canidae review](results/canidae-dimension-review-v0-2.md)
- **Next step:** widen the ecology-behavior registry and seed, freeze the 100-, 250-, and 500-species states, then measure dimension contribution, lens behavior, wall-clock, memory, and deterministic operation scaling. Domain-detail seeds evolve independently.
