# Experiment 3.3 — Cross-Level Semantic Transition Root Cause

**Status:** baseline failure preserved; governed stage-reset follow-up implemented
**Affected probe:** `cross_access_to_evidence`
**Baseline outcome:** `INCONSISTENT` under flat cumulative conjunction
**Experiment 3.3 outcome:** `CONSISTENT` under explicit stage-local scope
**Related report:** [Cross-Level Semantic Transition v1](../results/cross-level-semantic-transition-v1.md)

## Executive Finding

The failed legal cross-level probe is caused primarily by a mismatch between the semantic operation expressed by the probe and the representation executed by version 1.

The probe describes a transition from a data-access problem to an evidential consequence. The engine executes the accumulated coordinates as a flat conjunction. Those are not equivalent operations.

The run also exposed a separate mechanism-validation weakness: geometric-mean epsilon smoothing can leave a candidate numerically competitive despite zero direct support from one required field, while the current mechanism validity check measures field support across the candidate universe rather than support for the winning candidate.

The result must remain part of the version 1 evidence. It should not be repaired by relabelling the observed outcome, adding the expected target to the hard intersection after the run, or introducing an answer-specific relation.

Experiment 3.3 preserves that failed operation as its flat-conjunction control and tests a different, explicit operation. Each semantic level receives a governed local constraint scope; the earlier resolved region remains in the trace as provenance. This follow-up resolves all authored stages without modifying the legal state or pretending that an antecedent must be a defining trait of its consequence.

## Declared Probe

The final cross-level stage was authored as:

```text
access
+ incomplete_disclosure
+ exclusive_control
+ evidence
+ dispute
-> evidence_asymmetry
```

The fixture declared `evidence_asymmetry` as the expected region before execution.

`evidence_asymmetry` is represented with these traits:

```text
exclusive_control
evidence
incomplete_disclosure
dispute
reconstruction
```

It does not have the trait `access`.

## What The Governed Intersection Did

The exact authored incidence intersection evolved as follows:

```text
access
-> 9 candidates

+ incomplete_disclosure
-> disproportionate_access_restriction
   selective_access

+ exclusive_control
-> selective_access

+ evidence
-> empty intersection

+ dispute
-> empty intersection
```

The intersection becomes empty when `evidence` is added because `selective_access` satisfies the accumulated access-related coordinates but does not have `evidence`, while `evidence_asymmetry` satisfies the evidential coordinates but does not have `access`.

The independently declared ordinary probe for `evidence_asymmetry` succeeds with:

```text
exclusive_control
+ evidence
+ incomplete_disclosure
+ dispute
-> evidence_asymmetry
```

The retained `access` coordinate is therefore the exact structural difference between the successful identification probe and the failed cross-level probe.

## Why The Soft Field Still Favored `evidence_asymmetry`

The soft-intersection mechanism independently propagated all five fields. `evidence_asymmetry` had meaningful direct support from `incomplete_disclosure`, `exclusive_control`, `evidence`, and `dispute`. Its direct support from `access` was zero.

The geometric mean uses a tiny epsilon to keep `log(0)` numerically defined. That epsilon is appropriate numerical stabilization, but it is not semantic evidence. After multiplication, background correction, and normalization, a candidate supported strongly by four fields can still lead the final numerical distribution even though one required field contributes only epsilon.

The final channels therefore disagreed:

```text
mechanism:  RESOLVED
governance: UNRESOLVED / UNSUPPORTED_COMBINATION
overall:    UNRESOLVED
```

This separation prevented numerical proximity from becoming a forced legal conclusion. It also revealed that the mechanism-level validity contract is currently too permissive for strict required-field composition.

## Root Causes

### 1. Probe-operation mismatch — primary cause

The probe expresses a semantic transition:

```text
access issue
    -> selective or incomplete access
    -> evidential consequence
    -> evidence asymmetry
```

Version 1 executes cumulative conjunction:

```text
access
AND incomplete disclosure
AND exclusive control
AND evidence
AND dispute
```

An antecedent of a legal consequence is not necessarily a defining property of the consequence. The query kept every earlier coordinate as a permanent `MUST` constraint even after crossing from the processing level into the evidence level.

### 2. Representation gap

The legal development state represents a bipartite incidence structure:

```text
dimension -> concept
```

It does not represent governed cross-level transitions such as:

```text
selective_access
    may_create_evidential_effect
evidence_asymmetry
```

The state is adequate for direct combinatorial qualification. It is not yet adequate for deriving one qualified concept from another while retaining the earlier stage as provenance.

### 3. Governance limitation

Version 1 governance can validate direct shared trait membership, declared fixture-local exclusions, and whether the numerical leader belongs to the exact governed intersection.

It cannot validate a typed semantic transition. Consequently, it correctly rejects the empty direct intersection but cannot distinguish an invalid conjunction from a potentially valid multi-stage derivation that the state does not yet encode.

### 4. Winner-level validity weakness

The current mechanism validity check calculates the minimum total support contributed by each field across the complete candidate universe. It does not calculate the minimum support received by the winning candidate from every required field.

The stronger check is:

```text
minimum_required_support(winner)
    = min(support(winner, field_i) for every required field_i)
```

Under that contract, `evidence_asymmetry` would expose:

```text
missing_required_support: [access]
```

and the mechanism channel would also remain unresolved for the flat-intersection interpretation.

## What This Result Does And Does Not Show

It shows that flat cumulative intersection cannot represent this authored cross-level legal transition under the current state; governance prevents a soft numerical leader from becoming an unsupported legal conclusion; epsilon-supported geometric composition needs candidate-level required-field validation; and physical identification and legal cross-level qualification are not necessarily the same operation.

It does not show that geometric-mean soft intersection generally fails, that `evidence_asymmetry` is an incorrect region for the described progression, that adding `access` to it would be doctrinally correct, or that a typed executor would succeed without a separate experiment.

## Required Preservation In Experiment 3.3

The follow-up retains the cumulative union of every stage constraint as a control. It preserves the empty governed intersection and `UNRESOLVED` outcome rather than overwriting the original operation with the stage-reset result.

The `CONSISTENT` Experiment 3.3 verdict applies only to the separately declared stage-reset claim. It does not relabel the cumulative-intersection result as successful.

## Recommended Development Sequence

### Step 1 — Add probe-operation types

Declare the semantic operation before execution:

```text
INTERSECTION
All coordinates are required properties of the final target.

TRANSITION
Earlier coordinates establish an antecedent or intermediate region;
later coordinates qualify a consequence.

CONTEXT
A coordinate guides interpretation but is not required target membership.
```

For an `INTERSECTION` probe with an expected target, fixture validation should require the target to contain every constraint. The current cross-level probe would then fail validation as an intersection instead of failing only after execution.

### Step 2 — Strengthen mechanism validity

For the numerical winner, record support from every individual field and require a separately frozen non-trivial minimum:

```text
winner_support_by_constraint
minimum_winner_field_support
missing_required_constraints
```

Epsilon must remain a numerical implementation detail and must not satisfy semantic support. This change should first be tested against version 1 as an ablation. It must not overwrite the original evidence.

### Step 3 — Test stage-reset composition — implemented in Experiment 3.3

The smallest new cross-level treatment does not require new relation mathematics:

```text
Stage 1
access + incomplete_disclosure + exclusive_control
-> selective_access

Stage 2
exclusive_control + evidence + dispute
-> evidence_asymmetry
```

The Stage 1 result remains in the trace as provenance, but `access` is not carried into Stage 2 as permanent target membership.

Compare cumulative conjunction and stage reset under the same frozen state. If stage reset succeeds more appropriately, that is evidence that cross-level composition needs stage-local constraint scope.

### Step 4 — Test typed transitions separately

A later state may represent explicit transition candidates such as:

```text
selective_access
    may_create_evidential_effect
evidence_asymmetry

evidence_asymmetry
    may_impair
effective_remedy
```

This requires a new versioned treatment with typed direction, permitted relation composition, provenance, and validation. It must not be silently added to the version 1 operator.

### Step 5 — Compare the alternatives

Run a controlled follow-up with the state and basic propagation settings held fixed:

| Treatment | Semantic interpretation |
| --- | --- |
| Cumulative intersection | Every coordinate remains a final-target requirement |
| Stage reset | Earlier coordinates identify an intermediate state; later stages receive scoped inputs |
| Typed transition | Intermediate concepts connect through governed directional relations |

Measure target rank, margin, entropy, winner-level field support, governance status, and trace completeness. The purpose is to determine which operation fits cross-level legal qualification—not to guarantee that a richer treatment wins.

## Changes To Avoid

Do not repair version 1 by adding `access` to `evidence_asymmetry` solely to make the probe pass, adding a bespoke combination edge, lowering a threshold for this probe, treating epsilon as support, removing governance rejection, or reclassifying the probe after observing the result.

Those changes would erase the evidence instead of learning from it.

## Architectural Implication

The physical fixture tests **combinatorial identification**. The direct legal probes test **combinatorial qualification**. The failed cross-level probe tests a third operation:

> **Combinatorial transition:** an earlier qualified region becomes the governed antecedent of a later semantic consequence.

The baseline establishes that direct soft intersection plus hard incidence governance does not implement that third operation. Experiment 3.3 adds explicit stage scope as a small orchestration layer and reports a `CONSISTENT` development result across three authored transitions.

This establishes only that governed stage reset can represent the tested transitions. Automatic boundary discovery, typed transition relations, independently authored probes, and real legal qualification remain outside the evidence boundary.
