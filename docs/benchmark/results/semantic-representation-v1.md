# Semantic Representation Benchmark v1 — OSCARC Report

> **Richer meaning representation can make established mathematics produce more useful results.**

## Executive interpretation

The results are **consistent** with the local expectation that grounding an ambiguous word into governed semantic identities improves contextual focus while the mathematics remains fixed. All 6 probes across 3 authored scenarios met the three declared criteria, and deterministic replay passed. Evidence strength is **low** because these are small, authored development fixtures rather than held-out or independently assessed cases. The result supports semantic identity enrichment in this bounded experiment; it does not validate other richer representations or the general MML proposition.

## O — Objective observation

On `2026-08-10`, benchmark `semantic-representation-v1` executed 3 authored ambiguity scenarios containing 6 focused semantic-identity probes. The machine-readable result records baseline context activation from an ambiguous surface identity and grounded context activation from each governed identity.

The observed scenarios were:

- `identity-bank` — Grounding bank as river land or a financial institution. (8 sentences; 5 grounded ambiguous-word occurrences)
- `identity-bass` — Grounding bass as a fish or a musical instrument. (6 sentences; 4 grounded ambiguous-word occurrences)
- `identity-crane` — Grounding crane as a bird or lifting machinery. (6 sentences; 4 grounded ambiguous-word occurrences)

No causal interpretation is assigned to those observations in this section.

## S — Standard, baseline, or reference model

This is an A/B representation test. **A** is the ambiguous representation: one surface identity carries both meanings. **B** is the grounded representation: the same sentences contain separate governed identities and the query selects one of them. The local expectation was that B would make the activation field more useful for distinguishing the intended context without changing the compiler or query mathematics.

Here, *more useful* has one deliberately narrow operational meaning: of the activation that reaches the two declared competing context fields, a larger share should reach the intended field and less activation should leak into the competing field.

Each probe was required to satisfy three declared criteria:

1. in B, more than 50% of the activation reaching the two measured context fields lands in the intended field;
2. the intended-field share is higher in B than in A;
3. absolute activation leaking into the competing field is lower in B than in A.

Deterministic replay was a separate integrity requirement. This development version declared no minimum effect-size or statistical-significance threshold.

## C — Context and chronology

The fixed mathematics was `converged-personalized-pagerank-v1`. The independent variable was `semantic identity grounding and query focus`. The same transition-model compiler and Personalized PageRank strategy were used in both conditions.

```text
authored sentences
    -> A: ambiguous model + surface query
    -> A context measurements
    -> identity grounding only
    -> B: grounded model + focused query
    -> B context measurements
    -> paired A/B comparison
    -> deterministic rerun
```

The scenarios and context vocabularies are authored development fixtures. They are not held out, independently judged, or representative of general language.

## A — Actions, interventions, or observed mechanisms

Between A and B, the intervention replaced each declared occurrence of an ambiguous surface identity with its governed identity—for example, `bank` became `bank_river` or `bank_financial`. The query then targeted that identity. Sentences, compiler, window size, query strategy, damping, convergence, context definitions, and metrics remained fixed.

The observed mechanism was matrix propagation from the selected identity through the compiled transition model. The design isolates identity grounding within these fixtures; it does not establish that every richer representation will help.

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

All `6/6` probes passed because B favored the intended context, improved its intended-context share over A, and reduced absolute activation in the competing context. The intended-context share increased by between `5.1` and `29.5` percentage points across the six probes. Deterministic replay was `PASS`.

`PASS` means directional conformity with these three criteria; it does not mean the effect is large enough for a production use case. This version has no practical significance threshold.

### Secondary observation: evidence volume and gain

The larger `bank` fixture contains 8 sentences and 5 grounded occurrences of the ambiguous word. Its two intended-context gains were `21.1` and `29.5` percentage points. The `bass` and `crane` fixtures each contain only 6 sentences—3 for each meaning—and 4 grounded occurrences. Their gains ranged from `5.1` to `7.3` points.

The richer bank fixture therefore shows a substantially clearer separation, while the two compact fixtures already show a positive gain. This is an observed association, not evidence that corpus size caused the larger gain: vocabulary, sentence topology, context balance, and connection strength also differ between scenarios.

These paired outcomes are not population estimates or proof of comparable effects in unseen domains.

## C — Comparative assessment and research conclusion

**Conformity judgment: `CONSISTENT`.** Every B representation directed a majority of the measured contextual activation to the intended field, increased that share relative to A, reduced competing-field leakage, and replayed deterministically.

**Evidence strength: `LOW`.** The evidence consists of six authored probes with shared scenario and implementation authorship, no held-out cases, no independent review, and no inferential statistics. Within that boundary, the experiment is consistent with the claim that richer identity representation can make unchanged Personalized PageRank produce a more discriminating contextual field. It is called more useful here because a query for one meaning yields less evidence from the competing meaning and a larger proportion from the intended one—the exact behavior needed for sense-sensitive routing or retrieval.

Synonymy, hierarchy, association, semantic roles, relation-specific matrices, and policy composition remain separate untested hypotheses.

## Recommendation and next step

First, run a controlled evidence-volume experiment within the same ambiguity scenario. Build matched A/B corpora with progressively more sentences per meaning, repeat each level across several independently authored sentence sets, and plot intended-context gain and competing-field leakage against sentence and occurrence count. This will test whether enrichment benefit grows with evidence, appears immediately, or reaches a saturation point while holding vocabulary and topology as stable as possible.

Then freeze a held-out identity suite whose scenarios and expected directions are authored before implementation inspection and repeat this OSCARC analysis. Next, implement a topology-controlled typed-relation suite with relation-label permutation and edge-count controls to test relation meaning rather than additional connectivity.

## Evidence boundary

Authored development scenarios for semantic identity only; not held-out evidence for every form of richer meaning representation.

This report follows [OSCARC methodology](../oscarc-methodology.md). The JSON artifact remains authoritative for recorded measurements.
