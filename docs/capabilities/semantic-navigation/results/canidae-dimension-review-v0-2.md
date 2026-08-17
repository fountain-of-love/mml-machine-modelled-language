# Canidae Layered Dimension and Measurement Review

**Status:** development evidence; independent-source cross-check complete, human biological review pending  
**Foundational seed:** `species_ecology_behavior_seed_canidae_v0_1`  
**Detail seed:** `canidae_zoological_detail_seed_v0_1`  
**Animals:** 12 Canidae species

## Layer Boundary

The information-contribution results below are computed only from the 13 ecology-behavior dimensions. Body measurements, physiology, reproduction, and care are held in the linked zoological-detail state and do not participate in the foundational result. Both states resolve species identity through `species_registry_canidae_v0_1`.

## Body-Length Harmonization

Within the optional detail state, the governed measurement is PanTHERIA `13-1_AdultHeadBodyLen_mm`: adult head-body length from the tip of the nose to the anus or base of the tail. PanTHERIA consolidates this as a sex-unspecified unique median. It covers all 12 species and replaces ADW range midpoints as the source of `body_length_band`.

| Species | PanTHERIA mm | ADW midpoint mm | Difference | Review |
| --- | ---: | ---: | ---: | --- |
| Gray wolf | 1055.00 | 1085.0 | 2.8% | Consistent |
| Coyote | 872.39 | 875.0 | 0.3% | Consistent |
| Golden jackal | 827.53 | 775.0 | 6.3% | Consistent |
| Ethiopian wolf | 938.19 | 926.5 | 1.2% | Consistent |
| African wild dog | 923.86 | 925.0 | 0.1% | Consistent |
| Dhole | 987.74 | - | - | No ADW range |
| Red fox | 627.12 | 677.5 | 8.0% | Consistent |
| Arctic fox | 564.81 | - | - | No ADW range |
| Fennec fox | 374.23 | 350.0 | 6.5% | Consistent |
| Northern gray fox | 601.70 | 962.5 | 60.0% | Definition or aggregation conflict |
| Common raccoon dog | 447.38 | 590.0 | 31.9% | Definition or aggregation conflict |
| Bat-eared fox | 537.63 | 560.0 | 4.2% | Consistent |

Eight of ten available ADW comparisons fall within the declared 20% review tolerance. The two conflicts remain visible but cannot affect the canonical band. This is an independent dataset cross-check, not an independent human review; the latter remains explicitly pending.

## Multi-Valued Information Contract

Complete value sets are not treated as categorical labels. For each represented value, the analysis asks a binary question such as:

```text
Does this candidate have biome = forest?
```

Candidates with no governed value for the dimension are excluded from the semantic yes/no partition, and coverage multiplies the resulting information gain. Missingness therefore reduces contribution instead of becoming a distinguishing answer.

Conditional analysis narrows the candidate region with one positive value from another dimension, then recomputes the best reusable value question. Exact-set entropy remains visible only as an inflation diagnostic.

## Root Results

| Dimension | Coverage | Exact-set entropy | Best reusable value | Adjusted IG | Apparent inflation |
| --- | ---: | ---: | --- | ---: | ---: |
| biome | 91.7% | 3.459 | mountains | 0.911 | 2.548 |
| shelter or nesting | 100% | 2.792 | excavated den | 1.000 | 1.792 |
| native range realm | 100% | 2.355 | nearctic | 0.980 | 1.376 |
| activity cycle | 100% | 2.117 | nocturnal-crepuscular | 0.980 | 1.138 |
| microhabitat | 25% | 0.918 | agricultural | 0.230 | 0.689 |

The biome result confirms the original concern: eleven observed records have eleven exact biome sets, but no binary value question can contribute more than one bit. Microhabitat demonstrates the complementary control: apparently useful values receive a strong penalty when annotation coverage is poor.

## Conditional Results

For biome, 41 of 42 eligible one-value contexts have positive adjusted information gain. The maximum reaches 1 bit in balanced narrowed regions. This does not validate biome as globally optimal; it shows that its contribution is contextual and must be evaluated after the current candidate region is known.

The pilot deliberately stops short of causal or biological interpretation. The next foundational experiment must add negative observations, multi-step contexts, pairwise redundancy, source-confidence weighting, and independently reviewed annotations before comparing navigation policies. Zoological-detail contribution is a separate depth treatment.
