# Experiment 1 — Represent the Meaning. Change the Field.

**Status:** development experiment implemented; confirmatory protocol proposed
**Hypothesis:** Semantic Representation
**Working title:** *The Mathematics Stays. The Meaning Changes.*

This document defines the systematic experiment for MML's first hypothesis. It is the protocol blueprint beneath the broader benchmark programme. The existing identity-focused v1 report is bounded development evidence, not completion of this protocol.

The canonical capability definition is [Programme 1 — Semantic Representation](README.md).

The underlying architectural mechanism is developed in [The Representational Leverage Proposition](proposition.md).

## Hypothesis

> Given the same source observations, task, and fixed established execution method, a governed representation containing a task-relevant semantic distinction will produce a more useful, discriminating, and attributable result than a representation in which that distinction is absent.

The central intervention is representational. The experiment must not obtain its gain by silently changing the algorithm, source observations, task, evaluation set, or numerical settings.

### Primary empirical outcome

The primary result is a controlled curve or treatment ladder showing that **task-relevant semantic enrichment changes the execution field in the preregistered useful direction while the mathematics remains fixed**.

```text
task-relevant represented meaning -> task-relevant field discrimination
```

The exciting outcome is not that a richer graph scores better in aggregate. It is that one explicit semantic distinction produces one attributable behavioral change, its ablation removes that change, and irrelevant or sham enrichments do not reproduce it.

A convincing result has three inseparable properties:

1. **Fixed execution:** the same declared operator and numerical settings execute every treatment.
2. **Causal attribution:** the relevant represented distinction, rather than added labels, edges, query engineering, or topology, accounts for the change.
3. **Held-out usefulness:** the predicted change appears on probes that were not used to author or tune the representation.

## Claim Boundary

This experiment tests whether explicit representation affects deterministic semantic execution. It does not establish that one ontology is universally correct, that richer representation is always better, that graph propagation is reasoning, or that MML autonomously discovers semantic distinctions.

The authored `bank`, `bass`, and `crane` cases test a joint treatment of grounding plus matching query focus. They do not yet isolate grounding from focus or validate relation type, direction, role, constraint, exclusion, provenance, or policy composition.

## Current Development Fixture

The implemented v1 contains three synthetic ambiguity scenarios and six focused probes:

- `bank`: river land versus financial institution;
- `bass`: fish versus musical instrument; and
- `crane`: bird versus lifting machinery.

It compares an ambiguous surface representation with a jointly grounded-and-focused representation under the same co-occurrence compiler and Personalized PageRank activation strategy. The result is a low-strength directional signal for the joint treatment.

The current fixture remains useful for regression and mechanism development. It must be labelled `not_held_out` because representation, queries, expectations, and implementation share project authorship.

## Confirmatory Fixture Programme

Build several small, inspectable suites. Each suite isolates one representational dimension required by its task.

### Suite A — Identity and ambiguity

Use polysemous concepts with balanced competing senses. Each scenario must contain:

- the same underlying observations in every treatment;
- at least two governed senses;
- intended and contrast context judgments;
- an identity-preserving relabelling control; and
- a swapped-focus sham.

### Suite B — Relation meaning

Use matched endpoint structures in which only the governed relation differs:

- synonym versus opposition;
- hierarchy versus part/whole;
- cause versus temporal succession; and
- association versus role correspondence.

Preserve node and edge counts where practical. A relation label that does not alter execution cannot support a relation-semantics claim.

### Suite C — Semantic roles across domains

Use role coordinates such as `capacity`, `activation`, `boundary`, `substrate`, `gain`, and `storage`. Each case includes:

- a structurally aligned cross-domain counterpart;
- a vocabulary-similar but structurally incorrect hard negative;
- a partial structural match; and
- an explicit non-mapping or scope limitation.

The expected result is stronger support for the declared role correspondence without collapsing different domains into false equivalence.

### Suite D — Constraints and exclusions

Use direction, temporal validity, applicability, opposition, and exclusion to block routes admitted by association alone. Include positive, negative, unsupported, and scope-expired cases.

### Suite E — Task-policy composition

Execute at least two preregistered policies over the same semantic sources, for example a lexical-interpretation policy and a structural-correspondence policy. Coefficient sweeps are sensitivity analyses, not tuning searches.

## Freeze And Hold-Out Protocol

1. Author source observations and semantic distinctions.
2. Divide cases into development/calibration and confirmatory partitions before examining confirmatory outcomes.
3. Freeze the source observations, representation variants, operator, settings, query factors, judgments, and artifact hashes.
4. Independently author or review the confirmatory probes and expected directions.
5. Execute all factorial treatments without post-freeze semantic edits or parameter tuning.
6. Treat any corrected case as a new development version until a new confirmatory suite is frozen.

Held-out status applies to the cases, probes, judgments, and expected directions—not merely to a file that was hashed after co-design.

## Experimental Factors

For identity grounding, use the complete `grounding × query focus` factorial:

| Corpus representation | Query treatment | Purpose |
| --- | --- | --- |
| Ambiguous | Surface query | Baseline |
| Grounded | Surface query | Grounding-only effect |
| Ambiguous | Governed focus | Focus-only behavior or explicit incompatibility |
| Grounded | Matching governed focus | Joint treatment |
| Grounded | Swapped governed focus | Sham-control behavior |

If a focused query cannot execute against an ambiguous vocabulary, record `INCOMPATIBLE_TREATMENT`. Do not substitute another hidden query.

For other suites, use a representation ladder appropriate to the task:

```text
R0 association
R1 governed identity
R2 typed relation
R3 semantic role
R4 constraint or exclusion
R5 declared policy composition
```

The ladder is not a maturity score. A treatment is useful only when its added distinction is relevant to the frozen task.

## Fixed Treatments And Controls

At minimum, compare:

1. representation without the task-relevant distinction;
2. representation with the distinction;
3. identity-preserving relabelling;
4. matched topology or edge-count enrichment with irrelevant semantics;
5. swapped, permuted, or sham semantic labels;
6. ablation of the added distinction; and
7. deterministic replay.

The corpus, observations, candidate universe, operator implementation, normalization, damping, propagation horizon, convergence threshold, and evaluation probes must remain fixed unless declared as independent factors.

## Measurements

Report the complete field and at least:

| Measure | Purpose |
| --- | --- |
| Intended-context activation | Support reaching the declared intended field |
| Contrast-context activation | Cross-meaning or semantically incorrect leakage |
| Intended share | Intended activation divided by intended plus contrast activation |
| Intended-versus-contrast margin | Direct discrimination between competing regions |
| Target rank and nDCG/MRR | Ranking behavior where judgments support it |
| Hard-negative intrusion | Confident support for structurally or semantically wrong candidates |
| Attribution delta | Change produced by the relevant enrichment minus sham-control change |
| Deterministic replay | Exact or tolerance-bounded reproducibility |
| Construction and execution cost | Cost of obtaining and using the added distinction |

Report paired per-case changes, distributions, confidence intervals, failures, and incompatible treatments. Do not collapse the experiment into one aggregate accuracy number.

## Ablations

For every enriched case:

- remove the relevant identity split, relation, role, constraint, or policy term;
- preserve the label while removing its semantics;
- preserve topology while permuting semantic labels;
- remove aliases or query focus separately;
- substitute an irrelevant enrichment of comparable size; and
- vary policy coefficients only within a preregistered sensitivity range.

The gain should disappear or materially weaken when the relevant distinction is removed. If sham enrichments reproduce it, semantic attribution fails.

## Acceptance Criteria

Exact thresholds must be frozen before confirmatory execution. The bounded hypothesis receives support only if:

1. relevant enrichment improves preregistered task-specific discrimination on held-out cases;
2. grounding-only, focus-only, and joint effects are separately visible or explicitly incompatible;
3. sham, relabelling, and matched-topology controls do not reproduce the gain;
4. ablation removes or materially weakens the gain;
5. hard-negative intrusion and unrelated semantic leakage do not increase beyond frozen limits;
6. results replay deterministically and trace to governed records; and
7. the benefit is material relative to additional construction and execution cost.

The hypothesis is weakened when richer representation adds no useful change, when arbitrary enrichment works equally well, or when the effect requires hidden algorithmic changes.

## Threats To Validity And Controls

| Threat | Control |
| --- | --- |
| Grounding and query focus are conflated | Full factorial treatment |
| Extra edges, not semantics, create the gain | Matched topology and edge-count controls |
| Labels leak the expected answer | Identity-preserving relabelling and label permutation |
| Cases are authored to fit the mechanism | Frozen held-out and independently reviewed cases |
| Richness means merely “more relations” | Task-specific necessity and irrelevant-enrichment control |
| One metric hides semantic leakage | Report intended support, contrast support, margin, and hard negatives together |
| Algorithm changes with representation | Fixed operator identity and artifact hash |
| Policy coefficients are tuned on test cases | Preregistered policies and separate sensitivity analysis |

## Required Artifacts

Implementation should produce versioned machine-readable artifacts for:

- source observations and their identities;
- each representation treatment and hash;
- factorial query definitions;
- frozen judgments and expected directions;
- operator and numerical configuration;
- complete execution fields;
- per-case measurements and ablations;
- provenance paths to governed records;
- deterministic replay checks; and
- an OSCARC report with a claims ladder and evidence boundary.

## Intended Evidence

A successful confirmatory result would show that explicit, task-relevant meaning can cause fixed ordinary mathematics to behave more usefully and inspectably on held-out semantic tasks. It would not establish that every semantic enrichment helps, that the representation is complete, or that MML performs general reasoning.
