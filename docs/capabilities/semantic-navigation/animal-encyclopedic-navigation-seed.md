# Layered Species Navigation Seeds

## Purpose

The 12-species Canidae spiral now separates horizontal semantic breadth from vertical zoological depth. The foundational navigation experiment identifies species through reusable ecology and behavior coordinates. Detailed zoological fields remain available for drill-down, but cannot inflate or otherwise shape the foundational result.

This is a mechanism-development dataset. Its claims remain source-backed and inspectable, but the experiment does not depend on zoological completeness or claim biological authority.

## Three Linked States

| State | Responsibility | Explicitly excludes |
| --- | --- | --- |
| `species_registry_canidae_v0_1.json` | Stable species identity, taxonomy identifiers, and per-species consultation sources | Navigation dimensions |
| `species_ecology_behavior_seed_canidae_v0_1.json` | Reusable horizontal dimensions for foundational retrieval and navigation | Taxonomy, body measurements, physiology, reproduction, care |
| `canidae_zoological_detail_seed_v0_1.json` | Optional vertical detail and replayable measurement evidence | Foundational contribution analysis |

All records join through `species_id`; both semantic seeds declare `species_registry_state_id`. Their dimension sets are disjoint.

## Foundational Coordinate Field

The ecology-behavior seed contains 13 dimensions grouped beneath two broad concepts:

```text
ecology
  habitat
    environmental system, biome, microhabitat,
    ecological stratum, climate zone
  resource use
    trophic mode, primary food
  distribution
    native range realm
behavior
  temporal strategy
    activity cycle
  organization strategy
    social organization
  movement strategy
    locomotor mode, migratory strategy
  shelter strategy
    shelter or nesting
```

The original `habitat`, `diet`, `activity`, and `sociality` roles remain explicit anchor roles. The additional leaves are analogous reusable coordinates, not species-specific measurements. This layer expresses identity through ecology and behavior and is the input to the default dimension-contribution analysis.

The current field has 124 populated cells out of 156 (79.49%), with 185 traceable claims. Empty arrays mean not yet governed, never a negative biological assertion.

## Optional Zoological Detail

The detail seed contains body mass band, harmonized body-length band, body covering, thermoregulation, reproductive mode, and parental care. It also retains raw EltonTraits, ADW, and PanTHERIA observations required to replay detailed projections.

PanTHERIA adult head-body length remains the canonical length measurement. ADW ranges are independent contextual checks: eight of ten available comparisons agree within 20%; gray fox and raccoon dog remain explicit definition or aggregation conflicts. These facts are useful for deeper navigation, but are no longer mixed into the ecology-behavior field.

## Source Roles

| Source | Governed contribution |
| --- | --- |
| Catalogue of Life 2026-07-17 XR | Accepted identity and taxonomy registry |
| Mammal Diversity Database 2.5 | Identity and native biogeographic realm |
| EltonTraits 1.0 | Diet, activity, and body-mass observations |
| Animal Diversity Web | Habitat, behavior, reproduction, physiology, and contextual measurements |
| IUCN SSC Canid Specialist Group | Per-species consultation list; not a current claim source |
| PanTHERIA 1.0 | Harmonized adult head-body length |

Each populated semantic value names its source and locator. Derived values additionally name a deterministic mapping rule. Independent human biological review remains explicitly pending.

## Expansion Contract

1. Expand the registry with stable species identities and consultation sources.
2. Populate ecology-behavior coordinates first and measure coverage, value balance, conditional information gain, redundancy, and next-question utility.
3. Add domain-specific detail only in a separately identified seed linked through `species_id`.
4. Permit navigation from the broad field into detail, and generalization from detail back to broad concepts, without merging their experimental statistics.

This structure supports a horizontal spiral across more mammals and later plants, while preserving Canidae as the first vertical depth spiral.
