# Experiment 3.1 — Direct Combinatorial Intersection v1

**Claim verdict: `LOCALLY_CONSISTENT`. Evidence strength: `DEVELOPMENT`.**

## Research intention

Do independent broad dimensions increase direct semantic specificity more strongly than redundant dimensions?

This is an atomic test of direct cumulative intersection. It does not test legal qualification, cross-level semantic transition, or generalization.

## O — Objective observation

The frozen development fixture contains 31 concepts, 28 dimensions, and 177 ordinary single-trait relations.

## S — Standard, baseline, or reference model

Independent four-coordinate probes are compared with unmatched redundant storage controls and declared-invalid combinations. Structural information is an authored incidence control, not a kernel outcome.

## C — Context and chronology

The state and probes are `AUTHORED_DEVELOPMENT` and `not_held_out`. They were co-authored and do not constitute held-out evidence.

## A — Actions

Executed 8 independent probes, 2 redundant controls, 3 invalid probes, all 24 permutations per valid probe, and every leave-one-coordinate-out ablation.

## R — Results

| Measure | Result |
| --- | ---: |
| Independent final resolution | 100.0% |
| Invalid-combination rejection | 100.0% |
| Median independent entropy change | -0.698283 |
| Median redundant entropy change | 0.000000 |
| Median independent target-margin change | 1.000000 |
| Structural-information/entropy association | -1.000000 |

The independent and redundant cases are unmatched authored development controls. Their comparison is directional, not a paired estimate.

## C — Comparative assessment and research conclusion

The direct-intersection claim is `LOCALLY_CONSISTENT` within this fixture. Generalization is `UNTESTED`.

| Criterion | Result |
| --- | --- |
| `independent_compositions_resolve_declared_targets` | pass |
| `independent_composition_reduces_median_entropy` | pass |
| `independent_composition_increases_median_margin` | pass |
| `independent_outperforms_unmatched_redundant_control` | pass |
| `declared_invalid_compositions_are_rejected` | pass |
| `full_composition_is_order_invariant` | pass |
| `compiled_state_contains_no_bespoke_probe_primitive` | pass |

## Evidence boundary

One co-authored synthetic physical development fixture; not held out and not evidence of cross-domain generalization.

The [machine-readable artifact](../../../benchmark/results/direct-combinatorial-intersection-v1.json) is authoritative for trajectories, controls, hashes, and provenance. This report follows the [OSCARC methodology](../oscarc-methodology.md).
