# OSCARC Methodology for Benchmarking and Scientific Research

## Purpose

OSCARC turns measurements into an evidence-led research report. It guides the reader from neutral observation to a bounded interpretation without hiding the standard, chronology, intervention, uncertainty, or next step.

```text
Observation
    -> Standard
    -> Context and chronology
    -> Actions or mechanisms
    -> Result
    -> Conformity judgment
    -> Recommendation
```

The method is suitable for benchmarks, controlled experiments, incident studies, audits, and scientific comparisons. It does not replace statistical design, domain review, preregistration, or independent replication. It is the reporting structure through which those forms of evidence remain visible.

## Core Principles

1. **Evidence before interpretation.** Measurements and sources precede conclusions.
2. **Standards are declared.** Expectations, thresholds, and controls remain traceable to a protocol established before interpretation.
3. **Chronology matters.** Baseline, intervention, and post-intervention measurement remain distinct.
4. **Actions do not prove causes.** Performed interventions, observed mechanisms, and causal hypotheses receive different labels.
5. **Results remain measurable.** Direction, magnitude, uncertainty, and exceptions accompany `PASS` or `FAIL`.
6. **Conformity is local.** A judgment concerns the named expectation and evidence boundary, not universal project success.
7. **Evidence strength is separate.** Authored fixtures cannot support the confidence of held-out, replicated, independently reviewed evidence.
8. **Recommendations address gaps.** The next step targets the most important unresolved limitation.

## O — Objective Observation

State what was observed, when, and through which evidence. Use neutral language and retain raw or minimally processed measurements.

For a controlled benchmark, identify:

- the baseline condition;
- observed inputs and outputs;
- datasets, logs, artifacts, and result identities;
- measurement completeness and missing evidence;
- the date and benchmark version.

Avoid explanations such as “because the representation is better.” When a study contains an intervention, Observation normally records the baseline and comparable measurements; Result later records the measured post-intervention difference.

> During [period/version], [baseline or empirical condition] was observed. The observation is supported by [artifacts and measurements]. No causal interpretation is made here.

## S — Standard, Baseline, or Reference Model

Define the comparison point established before interpretation. This may be a hypothesis, expected direction, control condition, protocol invariant, threshold, or explicitly forbidden behavior.

For the semantic representation benchmark, the standard names each expected behavior separately:

1. intended-context activation exceeds contrast-context activation;
2. the intended-versus-contrast margin improves after enrichment;
3. contrast activation decreases;
4. repeated execution is deterministic.

A standard created after examining measurements must be labeled exploratory rather than confirmatory.

> According to [protocol/hypothesis], the expected behavior was [measurable expectation]. Conformity is assessed against [criteria], declared [when/by whom].

## C — Context and Chronology

Describe the setup and sequence required to interpret the evidence:

```text
source preparation
    -> baseline representation and execution
    -> controlled enrichment or intervention
    -> enriched execution
    -> paired comparison
    -> deterministic replay or restoration
```

Record relevant constraints: authored, held-out, or independent status; sample size; compiler and operator settings; shared authorship; exclusions; preprocessing; measurement definitions; environment; and known scope limitations. State whether expectations were frozen before results and whether tuning followed inspection.

## A — Actions, Interventions, or Observed Mechanisms

Describe what changed, what remained fixed, and who or what performed the change. Distinguish:

- **Performed action:** a known intervention, such as grounding an ambiguous surface identity.
- **Observed mechanism:** directly inspectable execution, such as activation propagating through a transition matrix.
- **Hypothesized causal factor:** an explanation not isolated by the current design.

For a representation benchmark, semantic enrichment should be the independent variable. Mathematics, observations, query protocol, and metrics remain fixed unless the case explicitly evaluates another factor.

> The benchmark performed [intervention]. [Variables] remained fixed. The operator exhibited [observable mechanism]. The study does/does not isolate [causal claim].

## R — Result, Effect, or Measured Outcome

Report what changed between conditions. Include baseline and treatment values, differences, ranges across probes, failed cases, uncertainty, and replay status. Link the narrative to machine-readable artifacts.

Translate machine-native values into quantities a reader can interpret. Raw activation weights, logits, distances, or loss values should not lead the narrative unless their scale has an intrinsic meaning. For competing semantic fields, for example, report the intended field's share of the activation reaching the measured fields and the A-to-B change in percentage points. Preserve raw values in the machine-readable companion for audit and reproduction.

Use “following,” “was associated with,” or “under this controlled treatment” when the design does not justify broader causal attribution. Reserve “caused” for designs that isolate the pathway adequately.

> Following [action], [outcome] changed from [baseline] to [treatment], a difference of [effect]. [Exceptions or uncertainty] were observed.

## C — Comparative Assessment and Research Conclusion

Compare the Result with the Standard using a bounded judgment:

- `CONSISTENT` — all declared criteria are met within the case boundary;
- `PARTIALLY CONSISTENT` — some criteria are met, but exceptions or controls remain unresolved;
- `INCONSISTENT` — one or more required criteria are contradicted;
- `INCONCLUSIVE` — evidence is insufficient or invalid.

Assess evidence strength separately:

- `LOW` — authored development evidence, small sample, no independence or held-out confirmation;
- `MODERATE` — held-out cases or replication with credible controls, but limited external validation;
- `HIGH` — replicated, independently assessed evidence with strong controls and appropriate statistical support;
- `ROBUST` — convergent evidence across independent datasets, methods, environments, and domain review.

Name exactly what is and is not supported. Identity enrichment may be consistent with the project intention while synonymy, hierarchy, semantic roles, and operator composition remain untested.

> The result is [judgment] with [standard]. Evidence strength is [level] because [reasons]. This supports [local claim] but does not establish [broader non-claim].

## Recommendation, Research Implication, or Next Step

End with the most informative next action. Distinguish practical changes, methodological improvements, theoretical implications, and future research. Where possible, identify the responsible research phase, expected output, and uncertainty addressed.

## Report Template

```markdown
# [Benchmark] — OSCARC Report

## Research intention
## Executive interpretation
## O — Objective observation
## S — Standard, baseline, or reference model
## C — Context and chronology
## A — Actions, interventions, or observed mechanisms
## R — Result, effect, or measured outcome
## C — Comparative assessment and research conclusion
## Recommendation and next step
## Evidence boundary
```

## Machine-Readable Companion

The narrative report must be generated from or traceable to a machine-readable result preserving the benchmark and methodology versions, timestamp, intention, standards, context, intervention, baseline and treatment measurements, conformity inputs, evidence boundary, artifact identities, and provenance. The report guides interpretation; it must not become an untraceable replacement for measurements.
