# Experiment 3.4 — Compositional Generalization v1

> **Can pairwise-constructed semantic state identify higher-order combinations that never occurred during construction?**

## Executive interpretation

**Conformity judgment: `EXECUTION_CONFORMANT`. Evidence strength: `LOW`.**

Construction retained only coordinate-pair counts from 192 synthetic training entities. The evaluation registry contained 64 disjoint complete signatures, queried at every width from 1 through 20 across six treatments. The coordinate basis permits `1,099,511,627,776` theoretical signatures, but this generator realizes only `256` of them.

**Scaling assessment: `NOT_SUPPORTED_BY_THIS_FIXTURE`.** MML's maximum top-1 advantage over the strongest exact control was `0.000`. The curve therefore tests the protocol successfully but does not provide distinctive evidence for MML in this fixture.

## Accuracy curves

Each sparkline runs from `k=1` to `k=20`; height represents deterministic top-1 accuracy.

| Treatment | Accuracy curve | First k at ≥90% | Final accuracy |
| --- | --- | ---: | ---: |
| `flat_keyword_retrieval` | `▁▃██████████████████` | 3 | 1.000 |
| `embedding_centroid` | `▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▂▂▂▂▂` | — | 0.109 |
| `vector_composition` | `▁▃██████████████████` | 3 | 1.000 |
| `kg_traversal` | `▁▃██████████████████` | 3 | 1.000 |
| `symbolic_conjunction` | `▁▃██████████████████` | 3 | 1.000 |
| `mml_soft_intersection` | `▁▃██████████████████` | 3 | 1.000 |

### Accuracy against dimensions and possible query combinations

| k | Possible queries (`4^k`) | `flat_keyword_retrieval` | `embedding_centroid` | `vector_composition` | `kg_traversal` | `symbolic_conjunction` | `mml_soft_intersection` |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 4 | 0.062 | 0.031 | 0.062 | 0.062 | 0.062 | 0.062 |
| 2 | 16 | 0.250 | 0.000 | 0.250 | 0.250 | 0.250 | 0.250 |
| 3 | 64 | 1.000 | 0.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| 4 | 256 | 1.000 | 0.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| 5 | 1,024 | 1.000 | 0.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| 6 | 4,096 | 1.000 | 0.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| 7 | 16,384 | 1.000 | 0.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| 8 | 65,536 | 1.000 | 0.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| 9 | 262,144 | 1.000 | 0.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| 10 | 1,048,576 | 1.000 | 0.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| 11 | 4,194,304 | 1.000 | 0.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| 12 | 16,777,216 | 1.000 | 0.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| 13 | 67,108,864 | 1.000 | 0.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| 14 | 268,435,456 | 1.000 | 0.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| 15 | 1,073,741,824 | 1.000 | 0.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| 16 | 4,294,967,296 | 1.000 | 0.125 | 1.000 | 1.000 | 1.000 | 1.000 |
| 17 | 17,179,869,184 | 1.000 | 0.141 | 1.000 | 1.000 | 1.000 | 1.000 |
| 18 | 68,719,476,736 | 1.000 | 0.125 | 1.000 | 1.000 | 1.000 | 1.000 |
| 19 | 274,877,906,944 | 1.000 | 0.172 | 1.000 | 1.000 | 1.000 | 1.000 |
| 20 | 1,099,511,627,776 | 1.000 | 0.109 | 1.000 | 1.000 | 1.000 | 1.000 |

## O — Objective observation

The leakage audit found `0` complete-signature overlaps and `0` materialized test-signature leaks. The compiled state contains `80` coordinates and pairwise records only; it retains neither construction entity identities nor complete construction signatures.

## S — Standard and controls

The declared standard required disjoint complete signatures, pairwise-only construction, all six treatments at every `k`, unique held-out targets, and complete-signature resolution by MML. Flat keyword retrieval, a frozen SVD embedding centroid, direct pairwise vector composition, additive graph traversal, symbolic conjunction, and MML soft intersection execute over the same evaluation registry.

## C — Context and chronology

The split is structural and deterministic: latent tuples whose digit sum is zero modulo four are held out; all others contribute aggregate pair counts. The state stores no entity identity or complete signature. Test signatures are materialized only by the evaluation adapter after construction.

## A — Actions and mechanisms

MML independently propagates each query coordinate through the pairwise training graph, combines the fields through a geometric-mean soft intersection, and scores each unseen candidate from its evaluation-side coordinate signature. The KG control adds propagated fields; vector composition uses cosine over explicit multi-hot coordinates; symbolic and lexical controls use explicit query-coordinate membership.

## R — Result

MML first reached at least 90% deterministic top-1 accuracy at `k=3` and 100% at `k=3`. Flat overlap, explicit vector composition, symbolic conjunction, and additive KG traversal reached the same accuracy at the same width. At `k=20`, MML resolved all 64 held-out signatures, but that shared success does not isolate an MML advantage.

### Conformity criteria

| Criterion | Result |
| --- | --- |
| `construction_contains_only_pairwise_coordinate_records` | pass |
| `complete_test_signatures_are_absent_from_training` | pass |
| `test_signatures_are_absent_from_construction_artifact` | pass |
| `all_declared_widths_and_treatments_executed` | pass |
| `all_held_out_targets_are_unique` | pass |
| `mml_resolves_all_complete_held_out_signatures` | pass |

## C — Comparative assessment and research conclusion

This is the first repository experiment in which complete target signatures are structurally absent from construction rather than merely absent as authored query strings. It verifies the stricter protocol and shows that higher-order evaluation can execute from pairwise state. However, exact overlap and symbolic controls match MML's curve, so the observed accuracy is explained by fixture identifiability without requiring soft intersection.

The result remains development evidence and does not support the distinctive scaling claim. The coordinate generator, split, mechanism, and evaluation were authored together; the four-latent-variable algebra realizes only 256 signatures; and evaluation supplies clean held-out candidate attributes. The next fixture must make exact controls insufficient while leaving genuinely inferable lower-order structure, then add irregularity, noise, missing coordinates, a much larger realized candidate universe, and a declared external embedding model.

## Claims ladder

| Level | Claim | Status |
| --- | --- | --- |
| implementation fact | construction retains pairwise coordinate counts only | verified |
| fixture observation | exact held-out signatures are disjoint from construction signatures | verified |
| bounded result | six treatments execute across `k=1..20` and 64 held-out targets | observed |
| architectural signal | pairwise semantic state can execute against unseen complete signatures | bounded mechanism evidence |
| distinctive MML signal | soft intersection outperforms exact or additive controls | not observed |
| scaling hypothesis | accuracy remains useful as meaningful realized combinations explode | not supported by this 256-signature generator |
| application claim | MML generalizes to unseen natural-language or factual entities | not established |

## Evidence boundary

The evaluation is zero-shot with respect to complete entity signatures: construction retains only pairwise coordinate counts. The split is synthetic and structurally held out, not independently authored or real-world evidence.

This tests structural holdout of complete signatures under a deterministic synthetic generator. It does not establish independently authored, natural-language, real-world, or production-scale generalization.

This report follows the [OSCARC methodology](../../../benchmark/oscarc-methodology.md). The [machine-readable JSON artifact](../../../../benchmark/results/compositional-generalization-v1.json) remains authoritative for every query result, metric, leakage check, artifact identity, and conformity input.
