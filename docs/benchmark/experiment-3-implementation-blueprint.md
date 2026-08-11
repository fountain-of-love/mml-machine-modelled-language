# Experiment 3 — Implementation Blueprint

**Status:** pre-implementation design
**Protocol:** [Experiment 3 — Compose the Broad. Resolve the Specific.](experiment-3-combinatorial-uniqueness.md)
**Reporting method:** [OSCARC v1](oscarc-methodology.md)

This blueprint describes how to implement the Combinatorial Uniqueness experiment while preserving the repository's existing separation between operational mechanisms, application flow, experiment adapters, governed fixtures, and generated evidence.

Its central empirical claim is deliberately stronger than “related legal concepts activate each other”:

> **More independent information can narrow a semantic or legal interpretation, while insufficient information remains insufficient.**

For the legal fixture, a `RESOLVED` result means that the declared semantic region was resolved under the fixture and execution contract. It does not establish that a legal conclusion is true, that an allegation is proven, or that a real institution violated an obligation.

## Architectural Outcome

Implement the experiment as five cohesive responsibilities:

```text
governed state + probes
          |
          v
fixture loader and validator
          |
          v
composition flow -----> operational activation/composition kernel
          |
          v
experiment adapter
          |
          +-----> machine-readable JSON evidence
          |
          +-----> OSCARC Markdown report
```

The experiment adapter must not define semantic composition. It coordinates treatments, measurements, conformity checks, artifact identities, and reporting around a separately testable operational mechanism.

## Proposed Repository Shape

Use the existing `data/demonstration`, `benchmark/results`, and `docs/benchmark/results` conventions:

```text
compose_concepts.py
combinatorial_uniqueness_flow.py
combinatorial_uniqueness_fixture.py
combinatorial_uniqueness_experiment.py
run_combinatorial_uniqueness.py

data/demonstration/
  combinatorial_uniqueness_state_v1.json
  combinatorial_uniqueness_probes_v1.json
  combinatorial_uniqueness_v1.json
  combinatorial_uniqueness_legal_banking_state_v1.json
  combinatorial_uniqueness_legal_banking_probes_v1.json
  combinatorial_uniqueness_legal_banking_v1.json

benchmark/results/
  combinatorial-uniqueness-v1.json

docs/benchmark/results/
  combinatorial-uniqueness-v1.md

tests/
  test_compose_concepts.py
  test_combinatorial_uniqueness_flow.py
  test_combinatorial_uniqueness_experiment.py
```

The existing fixture-integrity tests remain responsible for declarative artifact shape. New tests should cover execution rather than duplicate those checks.

## Responsibility Boundaries

### `compose_concepts.py` — operational kernel

This module owns only the fixed numerical and metric primitives required by composition:

- independently activate one governed constraint at a time;
- combine aligned activation fields with the existing normalized geometric mean;
- normalize and validate a resulting field;
- calculate entropy, normalized entropy, effective candidate count, concentration, rank, and margin; and
- expose the per-field support needed for inspection and validity checks.

The dominant pattern intent is a small **Strategy idiom**: activation is supplied as a callable or protocol, while composition remains independent of a concrete graph facade. Do not introduce a class hierarchy unless a second real strategy requires it.

Suggested contracts:

```python
@dataclass(frozen=True)
class ActivatedField:
    constraint: str
    values: tuple[float, ...]


@dataclass(frozen=True)
class ComposedField:
    constraints: tuple[str, ...]
    values: tuple[float, ...]
    per_constraint_support: tuple[ActivatedField, ...]


def soft_intersection(fields: Sequence[ActivatedField]) -> ComposedField:
    ...
```

Do not put targets, thresholds, fixture identities, expected regions, or experiment verdicts in this module.

### Preserve the existing mathematics

`GraphModel.activation` currently:

1. resolves each query token;
2. independently creates a bounded activation field;
3. combines multiple fields using a geometric mean with `np.finfo(float).tiny` as epsilon;
4. applies background correction; and
5. normalizes the final field.

Version 1 must preserve that behavior. The safest implementation sequence is:

1. characterize the current multi-token result with parity tests;
2. extract the exact field-combination calculation into `compose_concepts.py`;
3. make `GraphModel.activation` call the extracted function; and
4. prove byte-close or declared-tolerance parity for the existing tests and representative fixtures.

Do not introduce relation-specific matrices, a new propagation algorithm, learned weights, tuned per-probe coefficients, or a contradiction solver in v1. A failure under the present operator is evidence about the present operator.

### `combinatorial_uniqueness_flow.py` — operational facade

This module owns the use-case flow over compiled state:

```text
compile governed state
activate each constraint independently
compose prefix fields
evaluate declared exclusions and support
classify the semantic outcome
return inspectable execution records
```

Suggested public interface:

```python
class CombinatorialUniquenessFlow:
    def govern_and_compile(self, state_fixture) -> CompiledSemanticState: ...
    def execute(self, state, constraints, validity_policy) -> CompositionExecution: ...
```

This is the **Facade** for callers. It may adapt the fixture's concept–dimension representation into the current `GraphModel`, but the experiment adapter must not coordinate graph construction directly.

The compiled state should be immutable and content-addressed. State construction must create ordinary governed concept–dimension relations; it must never create a node or edge for an entire probe combination.

### `combinatorial_uniqueness_fixture.py` — loading and validation

This module owns file format translation and fail-fast validation:

- manifest, state, and probe identity agreement;
- unique concept, dimension, probe, and relation identities;
- declared dimension families;
- valid trait and target references;
- non-unique independent-probe coordinates;
- absence of expected rank or metric trajectories;
- scoped composition exclusions;
- explicit development versus confirmatory holdout status; and
- manifest hashes when an artifact is declared frozen.

It should return immutable domain records rather than mutable JSON dictionaries where practical. It must not run activation or decide conformity.

### `combinatorial_uniqueness_experiment.py` — experiment adapter

This module follows `knowledge_state_experiment.py`:

```python
run_experiment()
markdown_report()
check_result()
write_results()
main()  # --check | --write
```

It owns:

- treatment enumeration;
- mechanical prefix generation;
- permutation and leave-one-out execution;
- aggregation and paired comparisons;
- conformity criteria;
- OSCARC report generation;
- artifact hashes and provenance; and
- result checking and writing.

Its module docstring should explicitly say:

> This adapter benchmarks the Combinatorial Uniqueness flow; it does not define semantic composition.

### `run_combinatorial_uniqueness.py` — human-facing composition root

This optional console demonstration wires fixtures, flow, and presentation. It can show a few inspectable trajectories but must not become the benchmark implementation or overwrite evidence artifacts.

## State Construction Contract

Compile each concept and dimension as an addressable node. Translate every declared trait into one ordinary governed relation, for example:

```json
{
  "id": "fixture:capacitor:storage",
  "source": "storage",
  "relation": "supports",
  "target": "capacitor",
  "weight": 1.0,
  "evidence_ids": ["fixture:combinatorial_uniqueness_state_v1"]
}
```

The exact direction must be frozen and justified by the query flow. If current graph construction requires sentence evidence identifiers, the fixture adapter should create deterministic synthetic construction records and stable evidence identities rather than weakening the graph contract.

The compiler must report:

- state source identity;
- executable snapshot identity;
- concept and dimension counts;
- relation count;
- operator and policy configuration; and
- confirmation that no full probe combination appears as a compiled primitive.

## Freeze And Holdout States

Use explicit lifecycle states rather than treating every hash as proof of holdout:

```text
AUTHORED_DEVELOPMENT
STATE_FROZEN
PROBES_FROZEN_AFTER_STATE
EXECUTED_CONFIRMATORY
```

The current physical and legal-banking fixtures are `AUTHORED_DEVELOPMENT`: their state and probes are separate and hashable, but they were co-designed. They may validate implementation and reveal failure modes. They cannot establish the held-out construction claim.

A confirmatory manifest must record:

```text
state_sha256
state_frozen_at
probe_sha256
probe_frozen_at
kernel_sha256
flow_sha256
experiment_sha256
fixture_loader_sha256
methodology_sha256
```

The probe freeze timestamp must follow the state freeze. Hashes establish artifact identity; authorship and chronology establish the holdout boundary.

## Independent Information: The Primary X-Axis

Constraint count is easy to report but is not a sufficient measure of independent information. Four redundant labels are not equivalent to four constraints that eliminate different candidates.

Before activation, calculate each constraint's conditional information from the frozen concept–dimension incidence matrix. For prefix candidate set `S_(k-1)` and the subset `S_k` retaining the next constraint:

```text
information_gain_k = -log2(|S_k| / |S_(k-1)|)
```

with declared handling for an empty set. Cumulative independent information is:

```text
I_k = sum(information_gain_1 ... information_gain_k)
```

Properties:

- a constraint that removes no candidates contributes `0` bits;
- an exact redundant dimension contributes `0` after its equivalent is present;
- a constraint retaining half the candidates contributes `1` bit; and
- the measure is calculated from frozen fixture structure, not from MML activation outcomes.

This produces the primary empirical curve:

```text
cumulative independent semantic information -> activation specificity
```

Report constraint count as a secondary x-axis. Also report family transitions and incidence overlap so “cross-family” is not silently equated with “independent.” Dimensions from different families may still be correlated; dimensions from the same family may sometimes add information.

## Outcome State Machine

Keep numerical resolution, semantic governance, and legal truth distinct:

```text
declared exclusion present --------------------------> INVALID
required field absent or common support insufficient -> UNRESOLVED
margin/concentration below frozen threshold --------> UNRESOLVED
all semantic validity checks pass -------------------> RESOLVED
```

Every outcome carries a reason code:

```text
DECLARED_CONTRADICTION
UNKNOWN_CONSTRAINT
UNSUPPORTED_COMBINATION
INSUFFICIENT_FIELD_SUPPORT
AMBIGUOUS_INTERSECTION
RESOLVED_SEMANTIC_REGION
```

For the legal fixture:

- `INVALID` means the governed synthetic state explicitly rejects the combination;
- `UNRESOLVED` means the state and policy do not support a sufficiently specific semantic region; and
- `RESOLVED` means a semantic region cleared the declared mechanism threshold.

None of these statuses adjudicates a real legal claim. The epistemic-position contract must be returned unchanged unless a separate governed evidential transition explicitly permits a change. Numerical concentration alone can never promote `reasonable_inference` to `directly_established_fact`.

The present legal development state declares no universal contradiction. Its negative probes should therefore produce `UNRESOLVED / UNSUPPORTED_COMBINATION`, not `INVALID`, unless a later frozen state introduces scoped mutually exclusive dimensions.

## Treatments

Run these treatments over both contexts with the same kernel and fixed settings:

1. **Independent prefixes:** mechanically derive every prefix from each ordered valid probe.
2. **Matched redundant composition:** same or comparable constraint count, with measured low conditional information.
3. **Unsupported composition:** no declared sufficiently supported region; expected to remain unresolved.
4. **Declared invalid composition:** only where the state contains an explicit scoped exclusion.
5. **Additive activation control:** combine the same independently propagated fields additively.
6. **Hard incidence intersection:** deterministic structural reference, not the tested MML treatment.

The physical fixture currently provides fixture-local invalid cases. The legal fixture provides unsupported cases. Reports must not merge those two negative classes.

### Cross-level legal treatment

The legal fixture additionally evaluates declared stage sequences:

```text
processing dimensions
        + evidential dimensions
        + procedural dimensions
        -> increasingly qualified semantic region
```

Cross-level success requires more than movement toward any legally adjacent node. The intended region must improve in rank and margin, total entropy should fall or concentration rise, and unsupported legal leaps must remain unresolved.

### Contrastive qualification treatment

From shared starting constraints, execute each branch independently:

```text
access + rights_of_others
    + necessity + proportionality
        -> legitimate restriction region

access + rights_of_others
    + incomplete_disclosure + redaction_available
        -> disproportionate restriction region
```

Success requires branch separation, not merely top-1 correctness: report the intended-versus-contrast margin for each branch and the change caused by each differentiating constraint.

## Measurements

Record every complete candidate field. For every prefix report:

| Family | Measures |
| --- | --- |
| Declared input | ordered constraints, count, families, cumulative conditional information |
| Target | rank, activation, runner-up activation, target margin |
| Distribution | entropy, normalized entropy, effective candidate count, top-k mass |
| Validity | status, reason code, minimum per-field support, threshold values |
| Identity | state snapshot, operator identity, probe identity |

Use Shannon entropy over the normalized candidate-only field:

```text
H(p) = -sum(p_i * log(p_i))
```

and effective candidate count:

```text
N_eff = exp(H(p))
```

Exclude dimension nodes from candidate metrics. Otherwise concentration can reflect mass moving from dimensions to concepts rather than specificity among candidate concepts.

### Primary suite-level outcomes

- specificity versus cumulative independent information;
- paired independent-versus-redundant specificity gain;
- valid final-region resolution rate;
- unsupported-combination non-resolution rate;
- declared-invalid rejection rate, reported separately;
- physical identification versus legal qualification profiles; and
- calibration of resolution status against declared fixture labels.

Do not collapse these into one score.

## Permutation Control

The full geometric-mean composition should be order-invariant when it receives the same independently computed fields and fixed normalization. Test all `4! = 24` permutations for four-constraint probes; the fixture is small enough that sampling is unnecessary.

Report separately:

- exact or tolerance-bounded equality of the final activation field;
- preservation of target rank;
- preservation of status and reason code; and
- prefix trajectories, which are intentionally order-dependent because they contain different partial sets.

Do not demand that intermediate prefixes match across permutations.

## Ablation And Contribution

For each full valid composition, execute every leave-one-constraint-out set. Report raw before-and-after measurements and signed contributions:

```text
delta_margin(d) = full_margin - ablated_margin(d)
delta_entropy(d) = ablated_entropy(d) - full_entropy
```

Also report the constraint's incidence-based conditional information. This distinguishes three cases:

- structurally informative and activation-informative;
- structurally informative but suppressed by propagation; and
- structurally redundant but numerically influential, which may indicate activation-mass or hub effects.

This is the inspectable “Words Carry Weight” result: not merely which target won, but what semantic work each coordinate performed.

## Threshold Calibration

Do not choose concentration or margin thresholds from confirmatory probes. Use one of:

1. thresholds fixed from development fixtures, then carried unchanged into confirmatory execution; or
2. a separate calibration subset frozen before the confirmatory probe set.

Record the policy as a versioned object:

```json
{
  "policy_id": "composition-validity-v1",
  "minimum_per_field_support": 0.0,
  "minimum_top_concentration": 0.0,
  "minimum_top_margin": 0.0
}
```

The zeroes above are placeholders, not recommended values. The implemented development run must report sensitivity around the chosen thresholds rather than hiding threshold dependence.

## OSCARC Result Structure

The generated JSON and Markdown report should expose:

- **O — Objective observation:** fixture counts, field behavior, deterministic raw measurements;
- **S — Standard:** preregistered protocol, baselines, thresholds, and conformity criteria;
- **C — Context and chronology:** development versus confirmatory status and freeze order;
- **A — Actions:** compilation, prefix execution, controls, permutations, and ablations;
- **R — Results:** per-case trajectories and suite-level paired distributions; and
- **C — Comparative assessment:** bounded consistency, falsification, or inconclusive judgment.

The report headline table should be generated from actual results:

| Condition | Median initial rank | Median final rank | Median entropy change | Outcome rate |
| --- | ---: | ---: | ---: | ---: |
| Independent composition | measured | measured | measured | measured |
| Redundant composition | measured | measured | measured | measured |
| Unsupported composition | n/a | n/a | measured | measured non-resolution |
| Declared invalid composition | n/a | n/a | n/a | measured rejection |

Never place illustrative values in the evidence artifact.

## Executable Conformity Criteria

Keep each criterion separately visible and capable of failure:

```text
independent_information_predicts_specificity
independent_reduces_median_normalized_entropy
independent_improves_median_target_margin
independent_outperforms_matched_redundancy
valid_compositions_resolve_declared_regions
unsupported_legal_compositions_remain_unresolved
declared_contradictions_are_invalid
full_composition_is_order_invariant
repeat_execution_is_deterministic
epistemic_positions_are_not_numerically_promoted
```

The overall judgment should be:

```text
CONSISTENT
INCONSISTENT
INCONCLUSIVE
```

Do not make `--check` fail merely because the scientific hypothesis is false. `--check` should fail on artifact drift, invalid execution, nondeterminism, broken contracts, or mismatch with a frozen reference. A scientifically negative but correctly generated result is valid evidence and should be reportable as `INCONSISTENT`.

## Artifact Identities And Provenance

Record at least:

```text
physical_state_sha256
physical_probes_sha256
legal_state_sha256
legal_probes_sha256
compiled_snapshot_ids
kernel_sha256
flow_sha256
experiment_sha256
fixture_loader_sha256
methodology_sha256
result_schema_version
python_version
numpy_version
```

Record exact parameters separately from file hashes. If a frozen reference result is introduced, protect replacement with an explicit regression-acceptance flag and documented rationale, following the retrieval benchmark's precedent.

## Makefile Integration

Add repository-consistent targets:

```makefile
.PHONY: run-composition combinatorial-benchmark combinatorial-benchmark-check

run-composition:
	$(PYTHON) run_combinatorial_uniqueness.py

combinatorial-benchmark:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) combinatorial_uniqueness_experiment.py --write

combinatorial-benchmark-check:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) combinatorial_uniqueness_experiment.py --check
```

Add the check command to `make test` only after `--check` is non-mutating, deterministic, and backed by a written reference artifact.

## Test Strategy

### Kernel tests

- geometric-mean parity with current `GraphModel.activation` behavior;
- probability conservation and finite values;
- no mutation of input fields;
- deterministic output;
- identical-field and disjoint-field edge cases; and
- entropy and effective-candidate-count fixtures with analytically known values.

### Flow tests

- independent activation occurs once per declared constraint;
- prefix generation is mechanical;
- candidate metrics exclude dimension nodes;
- scoped exclusions yield `INVALID`;
- insufficient support yields `UNRESOLVED`;
- resolved outcomes preserve the epistemic position;
- compiled state is immutable and content-addressed; and
- no probe-specific primitive is compiled.

### Experiment tests

- all treatments and both contexts execute;
- all 24 four-constraint permutations preserve the final field;
- every leave-one-out ablation is present;
- paired independent/redundant summaries use declared matching rules;
- scientific non-conformity remains a valid report;
- OSCARC sections and evidence boundaries are present;
- hashes and provenance are complete; and
- `--check` writes no files.

## Implementation Sequence

1. **Characterize the existing mechanism.** Add parity tests around current independent-field geometric-mean activation.
2. **Extract the kernel.** Move only the proven composition primitive and distribution metrics into `compose_concepts.py`.
3. **Implement fixture loading.** Validate the existing physical and legal development artifacts without changing their scientific status.
4. **Compile the synthetic states.** Adapt concept–dimension traits into ordinary governed relations and immutable snapshots.
5. **Implement the flow.** Add prefix execution, validity classification, and inspectable results.
6. **Implement controls.** Add additive, hard-intersection, redundant, unsupported/invalid, permutation, and ablation treatments.
7. **Implement the experiment adapter.** Aggregate paired outcomes, evaluate criteria, and emit OSCARC JSON/Markdown.
8. **Wire CLI and Makefile checks.** Keep checks deterministic and non-mutating.
9. **Run development fixtures.** Treat failures as evidence about the present mechanism; do not tune per probe.
10. **Decide v2 from observed failure modes.** Introduce relation-specific operators only if v1 provides a concrete reason.
11. **Freeze confirmatory state and thresholds.** Record hashes and chronology.
12. **Author post-freeze probes.** Prefer independent authorship, then execute without semantic-state or parameter changes.

## Refactoring Gate After Implementation

After each implementation slice, inspect the touched files using the project's 13-law lens. Refactor only consequential drift:

- composition mathematics duplicated between `GraphModel` and the new kernel;
- fixture compatibility leaking into the kernel;
- experiment thresholds leaking into operational flow;
- state flags permitting invalid outcome transitions;
- mutable compiled state or hidden global configuration;
- reporting logic coordinating compilation internals; or
- callers forced to coordinate loader, graph, metrics, and validity subsystems directly.

Prefer extraction, naming, validation, and a small facade over new class hierarchies. The experiment is intentionally bounded; architectural complexity must be earned by observed failure.

## Completion Boundary For Version 1

Version 1 is complete when:

- both development contexts execute through the same unchanged soft-intersection kernel;
- independent, redundant, unsupported, and declared-invalid conditions remain distinct;
- the independent-information-to-specificity curve is generated from measurements;
- legal insufficiency remains unresolved rather than being converted into a conclusion;
- permutations, ablations, deterministic replay, hashes, and provenance are present;
- JSON and OSCARC Markdown artifacts reproduce through `--write` and verify through `--check`; and
- the report states whether observations are consistent, inconsistent, or inconclusive without expanding the claim boundary.
