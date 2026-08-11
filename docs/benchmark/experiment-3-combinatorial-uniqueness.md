# Experiment 3 — Compose the Broad. Resolve the Specific.

**Status:** proposed protocol; not yet implemented or executed
**Hypothesis:** Combinatorial Uniqueness
**Working title:** *The Intersection Becomes the Concept*

This document defines the first systematic experiment for MML's third hypothesis. It is a preregistration target, not an implementation report and not evidence that the hypothesis is true.

The underlying architectural mechanism and scaling argument are developed in [The Combinatorial Scaling Proposition](../Combinatorial-Scaling-Proposition.md).

## Hypothesis

> Given a fixed governed semantic state, independently broad constraints that are individually insufficient to identify a target will, when composed through MML's intersection mechanism, produce progressively greater specificity toward the correct target, while contradictory or unsupported combinations will fail to resolve.

The experiment asks whether semantic information compounds. Ranking the intended target first in a few examples is not sufficient. Each added independent constraint should systematically reduce uncertainty across a suite of targets, and should do so more strongly than redundant constraints of the same count.

### Primary empirical outcome

The exciting outcome would be an empirical curve showing that **specificity increases predictably with independent semantic information, on combinations that did not exist when the knowledge state was built**.

That curve is the primary result of the experiment:

```text
independent semantic information -> semantic specificity
```

Its horizontal axis must represent accumulated independent constraint information, not merely query length. Its vertical axis must report specificity through the preregistered measures of target rank, target margin, plausible candidate count, and activation-field entropy or concentration. The curve should be shown for held-out valid combinations alongside matched redundant combinations and invalid combinations.

A convincing result therefore has two inseparable properties:

1. **Predictable compounding:** specificity improves systematically as independent information accumulates.
2. **Runtime construction:** the tested combinations were absent when the governed knowledge state was authored and compiled; only their reusable primitive coordinates existed.

The first property tests whether semantic information compounds. The second tests whether MML constructs a specific query-time coordinate rather than retrieves a pre-authored combination. Either property without the other is insufficient for the experiment's strongest bounded claim.

The hypothesis is weakened if:

- independent constraints do not systematically improve rank, concentration, or candidate reduction;
- redundant constraints improve specificity as much as independent constraints;
- impossible combinations still resolve confidently;
- held-out combinations work only after combination-specific edges, primitives, or tuning are introduced; or
- apparent gains disappear under ablation, query-order controls, or reasonable execution settings.

## Claim Boundary

This experiment tests semantic execution over explicit primitive coordinates. It does not test natural-language understanding, general reasoning, open-world factual completeness, or performance at production scale.

Queries must therefore use governed coordinate identifiers such as:

```text
storage + boundary + electrical + reversible
```

They must not use natural-language questions such as:

```text
What electrical object stores energy reversibly within a boundary?
```

Language parsing would introduce a separate causal factor and make failures harder to attribute.

## Experimental World

Construct one small, deliberately inspectable semantic world containing:

- **30–50 target concepts** distributed across several domains, such as biology, engineering, computing, and economics;
- **8–12 broad semantic dimensions** that recur across those domains; and
- governed positive, negative, typed, and exclusion relationships sufficient to distinguish valid from invalid compositions.

Candidate concepts may include `battery`, `cell_membrane`, `capacitor`, `reservoir`, `spring`, `muscle`, `transistor`, `enzyme`, and `dam`. Candidate dimensions may include:

- `stores_energy`;
- `has_boundary`;
- `requires_activation`;
- `has_substrate`;
- `amplifies_input`;
- `is_reversible`;
- `is_biological`;
- `is_mechanical`; and
- `is_electrical`.

These are illustrative, not the frozen fixture. The final world must satisfy the following construction rules:

1. No single test dimension uniquely identifies its intended target.
2. Each valid target has at least four declared constraints that can be composed progressively.
3. Independent and redundant constraint sets are labelled using a declared, reproducible criterion rather than intuition alone.
4. No node, edge, alias, primitive, or weight encodes a complete evaluation combination as a bespoke shortcut.
5. Negative relationships and exclusions are represented explicitly where the world claims a combination is contradictory.
6. Every concept, relation, source decision, and fixture revision is inspectable and versioned.

### Two-context development programme

The first development version uses two independently named synthetic contexts under the same eventual composition mechanism:

1. **Physical and functional concepts — combinatorial identification.** Broad properties progressively identify concepts such as `capacitor`, `spring`, or `reservoir`.
2. **Legal and banking doctrine — combinatorial qualification.** Overlapping rights, governance, evidence, restriction, and procedure dimensions progressively qualify a pattern into a narrower legal or procedural region.

The second context adds two structures not required by the first:

- **cross-level composition**, where a processing-level pattern can acquire evidential and then procedural significance as further independent context is added; and
- **contrastive qualification**, where near-identical starting constraints diverge toward different regions after necessity, proportionality, redaction, or other qualifying dimensions are composed.

Both contexts remain synthetic and non-confirmatory. The legal fixture represents doctrine-oriented distinctions and an explicit epistemic-position contract; it does not encode allegations about a real institution as established truth or determine any legal violation.

If both contexts produce the preregistered specificity behavior under the same fixed mechanism, the bounded architectural signal is stronger than success in either context alone. It would suggest that soft intersection can support both **constructing an identifying coordinate** and **qualifying an ambiguous semantic pattern**. It would still not establish cross-domain generalization because both development fixtures share project authorship and were designed alongside their initial probes.

## Freeze And Hold-Out Protocol

The held-out claim concerns **combinations**, not necessarily unseen primitive concepts.

1. Author and validate the semantic world without the final evaluation combinations.
2. Freeze the governed state, compiler settings, propagation settings, and artifact hash.
3. Generate or independently author the evaluation combinations only after that freeze.
4. Classify each combination as valid, redundant, unsupported, or contradictory without changing the frozen state.
5. Freeze the query suite, expected targets or rejection labels, metric definitions, and acceptance thresholds.
6. Execute the benchmark without combination-specific graph edits or parameter tuning.

For example, the frozen state may independently represent that `capacitor` is related to `electrical`, `storage`, `reversible`, and `bounded`. It must not contain a relation equivalent to:

```text
electrical + storage + reversible + bounded -> capacitor
```

Any post-freeze correction invalidates the affected held-out run. The corrected world receives a new version and the case returns to development status until a new query suite is frozen.

## Experimental Conditions

Each target contributes matched queries in three primary conditions. Constraint count should be matched so that improvement cannot be attributed merely to adding more activation mass.

| Condition | Construction | Expected behavior |
| --- | --- | --- |
| One broad constraint | One non-unique coordinate | Weak specificity |
| Redundant composition | Several correlated or restated coordinates | Modest improvement |
| Independent composition | Several constraints that remove different plausible candidates | Stronger, progressive specificity |

Independence is operational: adding a coordinate must remove candidates admitted by the existing coordinates while retaining the intended target. Before execution, quantify coordinate overlap using a declared measure such as Jaccard overlap or mutual information over the frozen concept–dimension incidence matrix. Confirm the distinction after execution through ablation and marginal specificity gain. The post-execution measure explains behavior; it must not be used to relabel failed cases.

### Progressive valid composition

For every intended target, declare an ordered four-constraint sequence:

```text
A
A + B
A + B + C
A + B + C + D
```

The order must be frozen. Because progressive results can depend on the chosen sequence even when the final combination is symmetric, either evaluate every permutation or use a balanced order design across targets. Report the final full-set result separately from the order-sensitive progression.

An illustrative sequence is:

```text
storage                                      -> many candidates
storage + boundary                           -> fewer candidates
storage + boundary + electrical              -> very few candidates
storage + boundary + electrical + reversible -> capacitor
```

The target need not improve at every individual step in every case. The suite-level prediction is a monotonic trend with materially stronger gains for independent than redundant additions.

### Invalid composition

Include two distinct rejection classes:

1. **Contradictory:** the governed state explicitly makes the constraints mutually incompatible, including forms equivalent to `A + not_A`.
2. **Unsupported:** the state contains no sufficiently supported common intersection, without asserting a logical contradiction.

Illustrative examples include:

```text
biological + entirely_metal + photosynthetic + internal_combustion_powered
A + X + not_A
```

The expected outcome is `NO_VALID_INTERSECTION`, not a forced best guess. Contradiction and lack of support must remain different reason codes even if both yield rejection.

## Fixed Treatments

At minimum, execute every frozen query with:

1. each single coordinate;
2. each progressive independent combination;
3. a matched redundant combination;
4. additive activation;
5. normalized geometric-mean MML soft intersection; and
6. a hard Boolean intersection over explicit coordinate membership.

The first implementation should reuse the existing independent-field and soft-intersection mechanism. It must not add operator complexity merely to make this fixture pass. Lexical, BM25, or dense-retrieval baselines belong in a later retrieval-facing extension unless the fixture includes a separately frozen document corpus; they are not necessary to answer the primitive composition question.

All treatments must use the same frozen representation and candidate universe. Record exact operator identity, epsilon handling, normalization, propagation horizon, policy coefficients, tie handling, and rejection rule.

## Measurements

For every step, record the complete activation field and at least:

| Measure | Definition |
| --- | --- |
| Target rank | Rank of the declared target with deterministic tie handling |
| Target margin | Target score minus the highest-scoring non-target |
| Plausible candidate count | Number of candidates above a preregistered plausibility threshold |
| Entropy | Shannon entropy of the normalized candidate activation field |
| Normalized entropy | Entropy divided by `log(candidate_count)` for comparison across candidate universes |
| Concentration | A preregistered complement to entropy, such as `1 - normalized_entropy`, or top-k mass |
| Rejection result | Resolved target or `NO_VALID_INTERSECTION`, plus reason code |
| Constraint contribution | Change in each specificity measure when one constraint is added or removed |

The plausibility and validity thresholds must be frozen before the evaluation run. A top-ranked candidate below the validity threshold is a rejection, not a successful resolution.

Primary suite-level analyses are:

- number of independent constraints versus target rank, margin, candidate count, and entropy;
- marginal specificity gain from each added independent constraint;
- matched independent-versus-redundant gain at equal constraint counts;
- valid-composition resolution rate;
- contradictory-combination rejection rate;
- unsupported-combination rejection rate; and
- calibration of resolved confidence versus actual validity.

Report distributions, paired per-case changes, confidence intervals, ties, and failures. Do not collapse the experiment into one aggregate score.

## Ablations: What Semantic Work Does Each Coordinate Carry?

For every full valid combination, remove each coordinate in turn:

```text
electrical + storage + reversible + bounded -> capacitor
electrical + storage + reversible           -> capacitor / battery
electrical + storage                        -> broader field
storage                                     -> broad field
```

For coordinate `d`, define its marginal contribution to a specificity measure `S` as:

```text
delta_S(d) = S(full combination) - S(full combination without d)
```

Use the sign convention appropriate to each metric: higher margin and concentration are more specific; lower rank, candidate count, and entropy are more specific. Preserve the raw before-and-after values so the contribution remains inspectable.

Also ablate:

- negative and exclusion relationships;
- typed relations;
- each participating query coordinate;
- coordinate weights or policy coefficients within a preregistered sensitivity range; and
- soft intersection versus additive combination.

## Validity And Rejection Rule

A valid resolution requires all of the following:

1. the winning candidate exceeds a frozen minimum support or concentration threshold;
2. its margin over the runner-up exceeds a frozen ambiguity threshold;
3. it has non-trivial support from every required field rather than one dominant field; and
4. no governed contradiction or exclusion invalidates the combination or candidate.

If any condition fails, return:

```text
NO_VALID_INTERSECTION
```

with one of at least these inspectable reasons:

```text
CONTRADICTORY_CONSTRAINTS
UNSUPPORTED_COMBINATION
AMBIGUOUS_INTERSECTION
INSUFFICIENT_FIELD_SUPPORT
```

Thresholds are part of the experimental protocol and must not be selected on the held-out cases. If calibration cases are needed, separate them before the world and evaluation suite are frozen.

## Acceptance Criteria

Exact numerical thresholds should be preregistered after fixture construction but before held-out execution. The benchmark may support the bounded hypothesis only if all of these directional criteria are met:

1. Increasing independent constraint count produces a statistically and practically meaningful suite-level trend toward better rank, larger margin, fewer plausible candidates, and lower normalized entropy.
2. Matched independent combinations produce greater specificity gain than redundant combinations of the same size.
3. Full held-out valid combinations resolve their intended targets at the preregistered success rate without bespoke combination encoding.
4. Contradictory and unsupported combinations are rejected at their separate preregistered rates.
5. Ablations show that participating independent coordinates make non-trivial, inspectable contributions rather than merely repeating one dominant signal.
6. The result remains directionally stable across the preregistered sensitivity range.

Failure of any criterion must be reported as a local falsification or inconclusive result, not repaired through post hoc relabelling.

## Threats To Validity And Controls

| Threat | Control |
| --- | --- |
| The answer is authored into a bespoke edge | Prohibit combination-specific primitives and inspect the frozen graph |
| World and queries are co-designed | Freeze the world before independently producing and hashing the test combinations |
| More constraints merely add activation mass | Match independent and redundant conditions by constraint count and compare additive activation |
| “Independent” is only a linguistic judgment | Declare incidence-based overlap measures and perform per-coordinate ablations |
| Progressive order is cherry-picked | Freeze order and evaluate permutations or use a balanced order design |
| Entropy falls while the wrong target wins | Report rank, margin, candidate count, and entropy together |
| The engine always returns something | Freeze explicit validity thresholds and negative rejection cases |
| Epsilon smoothing manufactures false support | Declare epsilon and test sensitivity around it |
| Hub concepts dominate propagated fields | Report complete fields, hub behavior, and relevant correction settings |
| Thresholds overfit the test suite | Calibrate on separate cases and freeze thresholds before held-out execution |

## Required Artifacts

Implementation of this protocol should produce versioned, machine-readable artifacts for:

- the governed semantic world and its hash;
- the concept–dimension incidence matrix;
- the frozen query suite and classification labels;
- operator and threshold configuration;
- complete activation fields for every treatment;
- per-step and per-ablation measurements;
- invalid-combination reason codes;
- deterministic replay checks; and
- a generated report with the current evidence boundary.

The case format must remain declarative. Executable benchmark logic must not contain target-specific branches or answers.

## Intended Evidence

A successful bounded result would demonstrate that a specific semantic coordinate can be constructed at query time from reusable primitive coordinates without encoding that complete combination beforehand. It would also show that independent constraints contribute more specificity than redundant restatements and that governed composition can refuse invalid intersections.

It would not establish a universal combinatorial scaling law, natural-language reasoning, superiority over language models, useful coverage of open-world knowledge, or acceptable construction and execution cost at meaningful scale. Those claims require later experiments and independent replication.
