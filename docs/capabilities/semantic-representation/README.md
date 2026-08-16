# Programme 1: Semantic Representation

## Capability Target

> **Richer explicit meaning under fixed mathematics.**

Semantic Representation asks whether task-relevant meaning made explicit, addressable, and governed can make ordinary fixed mathematics produce more useful and attributable behavior.

In compact form:

```text
meaning
  -> explicit identities, roles, relations, and constraints
  -> executable semantic structure
```

This is the first MML capability: **Represent meaning.**

## What The Capability Defines

Semantic Representation defines:

- explicit semantic identities rather than conflated surface strings;
- construction-side grounding of corpus occurrences;
- query-side focus onto intended identities;
- aliases that preserve governed identity across different wording;
- typed and directed relations rather than undifferentiated connectivity;
- semantic roles such as `capacity`, `activation`, `boundary`, `substrate`, `gain`, and `storage`;
- constraints, exclusions, applicability, provenance, maturity, and review state;
- deterministic compilation of represented distinctions into an executable model; and
- attribution from changed behavior back to the represented distinction that caused it.

The capability does not claim that every richer representation is better. Added semantics matter only when they are required by the task, correctly governed, executable by the selected mathematics, and material relative to their construction cost.

## Research Question

> Given the same source observations, task, operator, and numerical settings, does adding one task-relevant governed semantic distinction produce a more useful, discriminating, and attributable result?

The independent variable must be representation. Algorithm changes, extra source evidence, hidden query transformations, answer-bearing identifiers, and unmatched topology changes are separate causal factors.

## Required Treatments And Controls

The programme includes:

1. a poorer representation without the required semantic distinction;
2. a richer representation with that distinction;
3. a full `grounding × query focus` factorial where identity is tested;
4. identity-preserving relabelling and swapped-focus sham controls;
5. matched topology or edge-count enrichment with irrelevant semantics;
6. relation-label permutation for typed-relation experiments;
7. ablation of the represented distinction;
8. hard negatives and explicit non-mappings; and
9. deterministic replay under one fixed execution method.

The planned representation ladder covers:

```text
R0 association
R1 governed identity
R2 typed relation
R3 semantic role
R4 constraint or exclusion
R5 declared policy composition
```

The ladder is not a maturity score. A higher treatment is useful only when its added distinction is relevant to the frozen task.

## Measurements

Report separately:

- intended-context or intended-field support;
- contrast-field activation and semantic leakage;
- intended-versus-contrast margin;
- target rank, MRR, or nDCG where judgments support them;
- hard-negative intrusion;
- grounding-only, focus-only, joint-treatment, and sham effects;
- relation or role specificity under label and topology controls;
- ablation effect;
- deterministic replay and attribution completeness; and
- representation authoring, review, compilation, memory, and execution cost.

## Current Evidence

The [Semantic Representation Benchmark v1](results/v1.md) applies the same co-occurrence compiler and Personalized PageRank strategy to ambiguous and jointly grounded-and-focused representations across `bank`, `bass`, and `crane`.

All six authored probes produced a consistent directional signal: the represented identity improved intended-context selectivity and reduced competing-context leakage under fixed mathematics. Evidence strength remains low because:

- the fixtures, expectations, and implementation share project authorship;
- the cases are not held out or independently assessed;
- grounding and query focus are changed together rather than isolated factorially; and
- only semantic identity is tested, not relation type, role, constraint, exclusion, or policy composition.

The operational capability now also exposes `GovernedCoordinateBasis` for accumulated experiments. It validates a finite dimension/value vocabulary, qualifies values by dimension, reports incomplete entities, assigns reversible stable codes, and produces a representation snapshot. Experiment 4.1 consumes this contract. Its integration success is mechanics evidence for interoperability, not an additional controlled Representation result.

## Evidence Boundary

The current result supports one bounded joint semantic-identity treatment. It does not establish that richer representation always helps, that the represented identities are universally correct, that MML discovers meaning autonomously, or that hypotheses two and three are valid.

## Research Layers And Next Step

- **Architectural proposition:** [Representational Leverage](proposition.md)
- **Experiment protocol:** [Experiment 1 — Represent the Meaning. Change the Field.](experiment.md)
- **Current evidence:** [Semantic Representation Benchmark v1](results/v1.md)
- **Next step:** execute the frozen factorial protocol, then extend to held-out typed-relation, semantic-role, constraint, and exclusion suites.
