# Experiment 4.2 - Lens-Aware Dimension Contribution

**Status:** implementation blueprint  
**Research stream:** Programme 4 - Semantic Navigation  
**Operation:** measure how governed semantic dimensions reduce candidate uncertainty under multiple navigation lenses  
**Primary claim:** the contribution of a semantic dimension is contextual and can be measured by the candidate partition it induces, rather than fixed in one authored decision tree

## Research Question

> Across a governed ecology-behavior state, which reusable dimensions reduce ambiguity, in which candidate regions, under which user lenses, and with how much unique or redundant information?

Experiment 4.2 does not search for one universal dimension hierarchy. A lens defines the dimensions eligible in one interaction; the candidate region determines their information value at that moment.

## Explicit Information Contract

For current candidate set `C` and unobserved, lens-eligible dimension `d`, partition the candidates by governed value:

```text
P_d(C) = {C_v : v is a represented value of d, including UNKNOWN}
```

Under the declared uniform candidate prior:

```text
H(C)       = log2 |C|
H(C | d)   = sum_v (|C_v| / |C|) log2 |C_v|
IG(d | C)  = H(C) - H(C | d)
NIG(d | C) = IG(d | C) / H(C)
```

`IG(d | C)` is also the entropy of the disjoint answer partition. The next question is:

```text
d* = argmax IG(d | C)
     over unobserved dimensions eligible under the active lens
```

Ties follow frozen basis order. No target identity, expected answer, or authored question sequence participates in selection. Future non-uniform priors must be a separately identified treatment.

The execution result must expose, for every eligible dimension:

- prior candidate entropy;
- expected posterior entropy;
- information gain and normalized information gain;
- represented answer count;
- missing candidate count; and
- whether the dimension was selected.

## Foundational Dimension Pool

The default experiment uses one horizontal ecology-behavior field. It deliberately contains useful, weak, and potentially redundant dimensions. Contribution is measured rather than assumed. Identity and taxonomy live in the linked species registry and are not candidate coordinates.

| # | Dimension | Initial controlled-value target | Principal lenses |
| ---: | --- | ---: | --- |
| 1 | `environmental_system` | 4 | ecological, open |
| 2 | `biome` | 10-14 | ecological, geographic, open |
| 3 | `microhabitat` | 8-12 | ecological, open |
| 4 | `ecological_stratum` | 7-9 | ecological, open |
| 5 | `climate_zone` | 5-7 | ecological, geographic, open |
| 6 | `trophic_mode` | 3-5 | ecological, open |
| 7 | `primary_food` | 8-12 | ecological, open |
| 8 | `activity_cycle` | 4-6 | behavioral, ecological, open |
| 9 | `social_organization` | 6-8 | behavioral, open |
| 10 | `locomotor_mode` | 7-9 | behavioral, open |
| 11 | `migratory_strategy` | 4-6 | behavioral, geographic, open |
| 12 | `shelter_or_nesting` | 7-10 | behavioral, open |
| 13 | `native_range_realm` | 8-12 | geographic, open |

The original habitat, diet, activity, and sociality concepts remain explicit anchor roles. The other leaves broaden those concepts at the same navigational level.

## Optional Vertical Detail

`body_mass_band`, `body_length_band`, `body_covering`, `thermoregulation`, `reproductive_mode`, and `parental_care` belong to a separately identified zoological-detail seed. They may be evaluated in a follow-on depth treatment after a candidate region has been established, but they are excluded from foundational metrics and MML-control comparisons.

This prevents animal-specific measurement engineering from being mistaken for evidence about the reusable ecology-behavior mechanism. The same layering permits later plant-specific detail without changing the horizontal navigation contract.

## Lenses

Lenses are overlapping governed dimension sets, not separate knowledge states and not permanent trees.

| Lens | Navigation intention |
| --- | --- |
| `open` | Maximize information gain over every foundational dimension |
| `ecological` | Navigate environment, niche, diet, and activity |
| `behavioral` | Navigate activity, organization, movement, migration, and shelter |
| `geographic` | Navigate realm, biome, climate, and migration |

The experiment must also accept an arbitrary governed lens assembled for a particular interaction. Report lens regret as the information difference between the best open question and the best question allowed by the lens. Optional detail lenses are declared against a particular detail seed and reported separately; they do not silently extend `open`.

## Single- And Multi-Valued Dimensions

Phase A assigns one governed canonical value or `UNKNOWN` per entity and dimension, producing disjoint partitions and directly testable entropy.

The source record must still preserve all sourced values. Phase B evaluates genuinely multi-valued dimensions such as habitat and native range through explicit binary coordinate questions. For value `v`, covered candidates are partitioned into `HAS(v)` and `DOES_NOT_HAVE(v)`. Unannotated candidates do not form an `UNKNOWN` semantic answer; they are excluded from the binary partition and coverage multiplies the information gain. Exact value-set entropy is retained only as an apparent-inflation diagnostic.

The initial Canidae pilot also measures conditional information gain after one positive value observation from another dimension narrows the candidate region. Later treatments must add negative observations, multi-step contexts, and declared non-uniform priors.

## Contribution Statistics

Report each dimension globally, by dataset size, by lens, and by query class:

- vocabulary cardinality, effective cardinality, coverage, missingness, and largest-value share;
- root partition entropy;
- mean, median, upper quantile, and maximum conditional information gain;
- mean normalized information gain and positive-gain rate;
- eligible-context count, best-question count, and selection rate;
- expected and observed candidate reduction when selected;
- identifiable and ambiguous regions resolved after asking the dimension;
- minimum navigation-depth reduction;
- leave-one-dimension-out loss;
- pairwise normalized mutual information and conditional redundancy;
- pairwise synergy where one dimension increases another's conditional contribution;
- lens-specific contribution and lens regret; and
- seeded permutation-Shapley estimates with uncertainty, rather than exhaustive subset enumeration.

No dimension is accepted because it has many labels. A sparse near-identity field can have high apparent entropy while providing poor reusable structure. Support, missingness, stability, and redundancy remain visible beside information gain.

The [Canidae layered review](results/canidae-dimension-review-v0-2.md) operationalizes this contract against `species_ecology_behavior_seed_canidae_v0_1`. Its biome exact-set entropy is 3.459 bits, while its best coverage-adjusted reusable value question contributes 0.911 bits, exposing 2.548 bits of apparent inflation. Body-length harmonization is retained as separate detail evidence.

## Experimental Protocol

1. Freeze definitions, controlled values, aliases, lens membership, missing-value semantics, and source priorities.
2. Source and independently review linked 100-, 250-, and 500-species registries and ecology-behavior states.
3. Freeze the animal state before generating navigation queries.
4. Generate complete, partial, ambiguous, unsupported, and lens-constrained query contexts.
5. Record every eligible dimension partition before selecting the maximum-information question.
6. Continue navigation until the region is identifiable, irreducibly ambiguous, or the lens has no informative dimension.
7. Compare open, lens-constrained, fixed-order, random-eligible, highest-cardinality, and highest-coverage question policies over identical state.
8. Publish compact aggregate evidence plus a content hash of complete query and navigation traces; retain failing traces as diagnostics.
9. Run separately identified domain-detail treatments only after the foundational result is frozen.

## Primary Outcomes

- information gained per question;
- questions required to reach an equivalence class;
- residual candidate entropy when navigation stops;
- identifiable, ambiguous, unsupported, and lens-exhausted rates;
- dimension selection and unique-contribution profiles;
- redundancy and synergy map;
- lens regret and lens-specific navigation depth; and
- contribution stability from 100 to 250 to 500 animals.

## Interpretation Boundary

This experiment measures navigation over information already represented in governed state. It does not claim that MML inferred zoological facts or translated unrestricted natural language. A dimension can be operationally useful while its source quality remains weak; provenance and annotation evidence therefore remain separate mandatory gates.
