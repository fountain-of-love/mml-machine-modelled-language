# Semantic Representation Benchmark v1 — OSCARC Report

> **Richer meaning representation can make established mathematics produce more useful results.**

## Research intention

Richer meaning representation can make established mathematics produce more useful results.

## Hypothesis scope

This report tests **MML Hypothesis 1: Representation** only:

> Meaning represented explicitly and richly enough can make ordinary mathematics semantically useful.

It does not test whether established knowledge can be compiled and reused more effectively than reconstruction at use time (**Hypothesis 2: Knowledge State Execution**), or whether combinations of reusable semantic coordinates create useful specificity and combinatorial coverage (**Hypothesis 3: Combinatorial Uniqueness**). Deterministic compilation and replay are controls in this experiment, not evidence for the whole triad.

## Executive interpretation

The results are **consistent** with the local developmental expectation that jointly grounding ambiguous corpus occurrences and focusing the query onto the matching governed identity improves contextual selectivity while the compiler and activation algorithm remain fixed. All 6 probes across 3 authored scenarios met the four developmental criteria, all activations converged, and same-process repetition passed. Evidence strength is **low** because these are small, authored development fixtures rather than held-out or independently assessed cases. The result is an early directional signal for the joint treatment; it does not isolate grounding from query focus and does not validate other richer representations, Knowledge State Execution, Combinatorial Uniqueness, or the general MML proposition.

## O — Objective observation

On `2026-08-10`, benchmark `semantic-representation-v1` executed 3 authored ambiguity scenarios containing 6 focused semantic-identity probes. The [machine-readable result](../../../benchmark/results/semantic-representation-v1.json) records baseline context activation from an ambiguous surface identity and grounded context activation from each governed identity.

The observed scenarios were:

- `identity-bank` — Grounding bank as river land or a financial institution. (8 sentences; 5 grounded ambiguous-word occurrences)
- `identity-bass` — Grounding bass as a fish or a musical instrument. (6 sentences; 4 grounded ambiguous-word occurrences)
- `identity-crane` — Grounding crane as a bird or lifting machinery. (6 sentences; 4 grounded ambiguous-word occurrences)

No causal interpretation is assigned to those observations in this section.

## S — Standard, baseline, or reference model

This is an A/B joint-treatment test. **A** is the ambiguous representation: one surface identity carries both meanings. **B** is the grounded representation: the same sentences contain separate governed identities and the query selects one of them. The exploratory expectation was that B would make the activation field more useful for distinguishing the intended context without changing the compiler or query mathematics.

Here, *more useful* has one deliberately narrow operational meaning: of the activation that reaches the two declared competing context fields, a larger share should reach the intended field and less activation should leak into the competing field.

Each probe was assessed against four developmental criteria:

1. in B, more than 50% of the activation reaching the two measured context fields lands in the intended field;
2. the intended-field share is higher in B than in A;
3. the intended-versus-contrast margin is higher in B than in A;
4. absolute activation leaking into the competing field is lower in B than in A.

Convergence and same-process deterministic repetition were separate integrity requirements. No independent preregistration artifact exists, so these are developmental exploratory criteria rather than confirmatory standards. This version declared no minimum effect-size or statistical-significance threshold.

## C — Context and chronology

The fixed algorithm contract was `converged-personalized-pagerank-v1`. The independent variable was `joint semantic identity grounding and matching query focus`. The same transition-model compiler and Personalized PageRank strategy were used in both conditions. The compiler uses a two-token co-occurrence window; activation uses damping `0.85`, at most `100` iterations, and L1 tolerance `1e-6`. The numerical operator is not fixed: its identities, dimensions, and transition entries change as the intended consequence of the representation treatment.

```text
authored sentences
    -> A: ambiguous model + surface query
    -> A context measurements
    -> declared corpus grounding
    -> B: grounded model + focused query
    -> B context measurements
    -> paired A/B comparison
    -> deterministic rerun
```

The scenarios and context vocabularies are authored development fixtures. They are not held out, independently judged, or representative of general language. Missing controls include grounding-only, focus-only, swapped-focus, identity-preserving-label, topology, and context/parameter-sensitivity treatments.

## A — Actions, interventions, or observed mechanisms

Between A and B, the intervention replaced each declared occurrence of an ambiguous surface identity with its governed identity—for example, `bank` became `bank_river` or `bank_financial`. The query then targeted that identity. Sentences, compiler, window size, query strategy, damping, convergence tolerance, context definitions, and metrics remained fixed.

The observed mechanism was matrix propagation from the selected identity through the compiled transition model. Because grounding and query focus change together, the design does not isolate either component, semantic identity quality versus added topology, or the proposition that every richer representation will help.

## R — Result, effect, or measured outcome

The transition model produces a normalized activation distribution: all identity weights together sum to 100%. A context value is the portion landing on the small set of words declared for that context. Because those raw portions depend on corpus size and context vocabulary, they are not meaningful as standalone scores.

The report therefore interprets them as **context selectivity**: among activation reaching the two measured competing fields, what percentage reaches the intended field? A value above 50% favors the intended meaning. The A-to-B change is shown in percentage points.

| Scenario | Focused meaning | A: intended share | B: intended share | Gain (percentage points) | Competing-field activation reduced? | Conformity |
| --- | --- | ---: | ---: | ---: | --- | --- |
| identity-bank | bank_river | 56.1% | 85.6% | +29.5 | yes | PASS |
| identity-bank | bank_financial | 43.9% | 65.0% | +21.1 | yes | PASS |
| identity-bass | bass_fish | 45.0% | 51.4% | +6.4 | yes | PASS |
| identity-bass | bass_instrument | 55.0% | 62.3% | +7.3 | yes | PASS |
| identity-crane | crane_bird | 45.3% | 52.2% | +6.9 | yes | PASS |
| identity-crane | crane_machine | 54.7% | 59.8% | +5.1 | yes | PASS |

### Representation cost

The compiler and activation algorithm are fixed, but enrichment changes the compiled operator. The structural cost observed for each scenario was:

| Scenario | Identities A → B | Non-zero transitions A → B | Matrix bytes A → B | Grounded occurrences |
| --- | ---: | ---: | ---: | ---: |
| identity-bank | 60 → 61 | 269 → 271 | 28800 → 29768 | 5 |
| identity-bass | 33 → 34 | 136 → 138 | 8712 → 9248 | 4 |
| identity-crane | 31 → 32 | 138 → 140 | 7688 → 8192 | 4 |

These counts expose representational growth only. Authoring/review effort, compilation latency, query latency, memory outside the dense transition matrix, and energy were not measured.

### Numerical integrity

All `9` activation executions recorded for the first run converged. Iterations ranged from `30` to `47`; final L1 residuals ranged from `7.351e-07` to `9.935e-07`. Same-process repetition was `PASS`.


All `6/6` probes passed because B favored the intended context, improved its intended-context share and margin over A, and reduced absolute activation in the competing context. The intended-context share increased by between `5.1` and `29.5` percentage points across the six probes. Same-process deterministic repetition was `PASS`.

`PASS` means directional conformity with these four criteria; it does not mean the effect is large enough for a production use case. This version has no practical significance threshold.

### Exploratory secondary observation: evidence volume and gain

The larger `bank` fixture contains 8 sentences and 5 grounded occurrences of the ambiguous word. Its two intended-context gains were `21.1` and `29.5` percentage points. The `bass` and `crane` fixtures each contain only 6 sentences—3 for each meaning—and 4 grounded occurrences. Their gains ranged from `5.1` to `7.3` points.

The richer bank fixture therefore shows a substantially clearer separation, while the two compact fixtures already show a positive gain. This is an observed association, not evidence that corpus size caused the larger gain: vocabulary, sentence topology, context balance, and connection strength also differ between scenarios.

These paired outcomes are not population estimates or proof of comparable effects in unseen domains.

## C — Comparative assessment and research conclusion

**Conformity judgment: `CONSISTENT`.** Every joint grounding-and-focus treatment directed a majority of the measured contextual activation to the intended field, increased that share relative to A, improved the intended-versus-contrast margin, reduced competing-field leakage, converged, and repeated deterministically in the same process.

**Evidence strength: `LOW`.** The evidence consists of six authored probes with shared scenario and implementation authorship, no held-out cases, no independent review, and no inferential statistics. Within that boundary, the experiment is consistent with the claim that explicit sense identity plus matching query focus can make the same Personalized PageRank algorithm/settings produce a more discriminating contextual field in these fixtures. It is called more useful here because a query for one meaning yields less evidence from the competing meaning and a larger proportion from the intended one—a candidate mechanism aligned with, but not evidence of, improved sense-sensitive routing or retrieval.

Synonymy, hierarchy, association, semantic roles, relation-specific matrices, and policy composition remain separate untested hypotheses.

### Claims ladder

| Level | Claim | Status |
| --- | --- | --- |
| implementation fact | both conditions use the same compiler and Personalized PageRank algorithm/settings | verified |
| fixture observation | all six joint grounding-and-focus probes improved declared context selectivity and reduced competing-field activation | observed in authored fixtures |
| exploratory signal | explicit sense identity plus matching query focus can produce a more discriminating activation field | early directional signal |
| representation hypothesis | semantic identity enrichment generalizes across unseen language tasks | untested beyond authored fixtures |
| application hypothesis | the activation effect improves routing or retrieval outcomes | untested |
| wider MML proposition | Richer meaning representation can make established mathematics produce more useful results. | research intention, not established |

The ladder prevents fixture-level activation observations from being promoted into application effectiveness or the wider MML proposition without separate evidence.

## Recommendation and next step

The next research phase should first freeze a v2 protocol before implementation changes. Its primary output should be a grounding × query-focus factorial suite over a compatible shared vocabulary, with grounding-only, focus-only, joint-treatment, swapped-focus sham, identity-preserving label, and topology/edge-count controls. This retires the principal v1 attribution uncertainty.

The same frozen protocol should add held-out independently authored cases, context-word and sentence perturbations, leave-one-out stability, and window/damping sensitivity. Before results, it should jointly declare the minimum selectivity benefit and acceptable authoring, latency, memory, and energy costs. Only after attribution and robustness are established should an evidence-volume study test scaling, followed by separate routing or retrieval application outcomes.

## Evidence boundary

Authored development scenarios for the joint semantic grounding-and-focus treatment only; not isolated evidence for grounding alone, not held-out evidence for richer meaning representation generally, and not evidence for MML hypotheses two or three.

This report follows [OSCARC methodology](../oscarc-methodology.md). The [machine-readable JSON artifact](../../../benchmark/results/semantic-representation-v1.json) remains authoritative for measurements, convergence, conformity inputs, artifact identities, and provenance.
