---
artifact: governance
status: active
authority: relation-governance
updated: 2026-08-28
scope: cross-branch-relations
---

# Relation Ledger

## Purpose

This ledger records the first governed relation vocabulary for the Seed Vault concept layer.

Its purpose is to let the ontology carry more than isolated concept labels. It introduces relation families that support synonymy, contrast, association, dependency, hierarchy, process, and confusion in a readable and machine-navigable way.

## Linked Data Convention

Each relation can be read locally as a governed tuple:

```text
(subject, predicate, object)
```

This local tuple may later be exported to RDF-, SKOS-, OWL-, or Wikidata-flavored structures, but the Seed Vault keeps its own local authority over meaning boundary.

## Relation Families

| Family | Purpose | Typical examples |
| --- | --- | --- |
| `equivalence` | Expressions that point to the same or nearly the same concept | `alias_of`, `acronym_for` |
| `hierarchy` | Broader, narrower, or membership-like placement | `is_a`, `within`, `part_of` |
| `association` | Neighboring concepts that travel together without identity | `adjacent_to`, `associated_with`, `used_with` |
| `contrast` | Relations that preserve difference, exclusion, or opposition | `contrasts_with`, `not_equivalent_to` |
| `dependency` | Relations of requirement, enablement, or presupposition | `uses`, `requires`, `enables`, `depends_on` |
| `process` | Relations inside execution or transformation paths | `has_stage`, `precedes`, `input_to`, `produces`, `tested_by`, `transforms_into`, `revised_into` |
| `confusion` | Relations for frequent conceptual drift or flattening | `confused_with`, `overlaps_with` |

## Relation Vocabulary

| Relation | Family | Weight class | Directionality | Linked-data hint | Notes |
| --- | --- | --- | --- | --- | --- |
| `alias_of` | `equivalence` | `semantic-neighborhood` | `directed` | `skos:altLabel`-like | Use for lexical or naming equivalence without forcing full identity collapse of every sense |
| `acronym_for` | `equivalence` | `semantic-neighborhood` | `directed` | label mapping | Useful for short forms like `IT` |
| [[is_a]] | `hierarchy` | `structural` | `directed` | `rdf:type` / `P31`- or `P279`-like | Use when the subject is treated as a member or kind of the object |
| [[within]] | `hierarchy` | `structural` | `directed` | `skos:broader` / `part_of`-like | Scope-placement relation for branches, fields, and umbrellas |
| `part_of` | `hierarchy` | `structural` | `directed` | `P361`-like | Use for compositional inclusion rather than broad topical placement |
| `adjacent_to` | `association` | `semantic-neighborhood` | `undirected` | `skos:related`-like | Neighbor relation without identity or containment |
| [[associated_with]] | `association` | `semantic-neighborhood` | `undirected` | related-association | Broader co-travel relation than `adjacent_to` |
| `used_with` | `association` | `operational` | `undirected` | tooling or co-use relation | Operational co-use without dependency |
| `contrasts_with` | `contrast` | `semantic-neighborhood` | `undirected` | contrastive relatedness | Use when concepts become clearer through difference |
| `not_equivalent_to` | `contrast` | `structural` | `undirected` | explicit non-identity | Important when two concepts are often collapsed incorrectly |
| [[uses]] | `dependency` | `operational` | `directed` | operational-use relation | Subject operationally employs object; weaker than `requires` because the object may not be constitutive in every realization |
| [[requires]] | `dependency` | `operational` | `directed` | prerequisite relation | Subject cannot be adequately realized without object |
| [[enables]] | `dependency` | `operational` | `directed` | enabling relation | Object makes the subject possible or more operative |
| `depends_on` | `dependency` | `operational` | `directed` | dependency relation | Broader than `requires`; use when dependency is real but not constitutive |
| `has_stage` | `process` | `operational` | `directed` | workflow decomposition | Subject process contains object as a named stage |
| `precedes` | `process` | `operational` | `directed` | ordering relation | Subject stage or event normally comes before object stage or event |
| `input_to` | `process` | `operational` | `directed` | input relation | Subject artifact, state, or concept feeds into object process or stage |
| `produces` | `process` | `operational` | `directed` | output relation | Subject yields object as an output or artifact |
| `tested_by` | `process` | `operational` | `directed` | verification relation | Subject is checked or exercised by object |
| `transforms_into` | `process` | `operational` | `directed` | transformation relation | Use for staged conversion rather than broad association |
| `revised_into` | `process` | `operational` | `directed` | revision relation | Subject is changed into a later version of object through feedback |
| [[confused_with]] | `confusion` | `semantic-neighborhood` | `undirected` | local confusion surface | Record frequent human or model boundary drift |
| `overlaps_with` | `confusion` | `semantic-neighborhood` | `undirected` | partial coincidence | Use when concepts share territory without identity |

## Process Graph Pattern

Processes should be represented as small directed graphs, not only as prose descriptions.

A process concept may own stage nodes through `has_stage`. Stage nodes may be ordered with `precedes`. Artifacts, states, or concepts may enter the process through `input_to`; stages may emit artifacts through `produces`; feedback may be represented through `tested_by`, `transforms_into`, or `revised_into`.

Minimal process skeleton:

```text
(process, has_stage, stage.a)
(stage.a, precedes, stage.b)
(input.artifact, input_to, stage.a)
(stage.b, produces, output.artifact)
```

This keeps process awake inside the graph: a process can be traversed, queried, compared, interrupted, repeated, or audited.

## Initial Relation Records

| Tuple | Status | Family | Weight class | Source basis | Notes |
| --- | --- | --- | --- | --- | --- |
| `(form.information_technology, alias_of, "IT")` | `candidate` | `equivalence` | `semantic-neighborhood` | common usage and computing seed | Acronym relation for operational shorthand |
| `(form.computer_programming, within, form.computer_science)` | `candidate` | `hierarchy` | `structural` | computing ledgers | Programming sits within the computer science branch |
| `(form.computer_science, within, form.computing)` | `candidate` | `hierarchy` | `structural` | computing ledgers | Discipline within broader computing umbrella |
| `(form.information_technology, within, form.computing)` | `candidate` | `hierarchy` | `structural` | computing ledgers | IT sits within computing but is narrower than it |
| `(form.algorithm, associated_with, form.data_structure)` | `candidate` | `association` | `semantic-neighborhood` | computing foundations | Core conceptual pairing without identity |
| `(form.computer_programming, uses, form.algorithm)` | `candidate` | `dependency` | `operational` | computer programming seed | Programming operationally uses algorithms without collapsing programming into algorithm design |
| `(form.computer_programming, uses, form.data_structure)` | `candidate` | `dependency` | `operational` | computer programming seed | Programming operationally uses data structures |
| `(form.computer_programming, adjacent_to, form.software_engineering)` | `candidate` | `association` | `semantic-neighborhood` | computer programming seed | Strong neighborhood relation with distinct boundary |
| `(form.computer_programming, confused_with, form.software_engineering)` | `candidate` | `confusion` | `semantic-neighborhood` | computer programming seed | Frequent flattening in ordinary speech |
| `(form.algorithm, not_equivalent_to, form.heuristic)` | `candidate` | `contrast` | `structural` | algorithm seed boundary | Important distinction for later computing ontology |
| `(form.operating_system, part_of, form.information_technology)` | `candidate` | `hierarchy` | `structural` | computing systems ledger | Operational infrastructure placement |
| `(form.database_management_system, associated_with, form.information_systems)` | `candidate` | `association` | `semantic-neighborhood` | computing systems ledger | Shared operational terrain without identity collapse |
| `(form.computer_programming, requires, form.programming_language)` | `candidate` | `dependency` | `operational` | computer programming seed | Programming normally requires an executable expression medium |
| `(form.computer_programming, produces, form.source_code)` | `candidate` | `process` | `operational` | computer programming seed | Programming produces code artifacts |
| `(form.computer_programming, tested_by, form.debugging)` | `candidate` | `process` | `operational` | computer programming seed | Debugging is one process that checks operative behavior |
| `(form.computer_programming, has_stage, form.problem_framing)` | `candidate` | `process` | `operational` | computer programming seed | Programming begins from a problem or intent that needs executable expression |
| `(form.problem_framing, precedes, form.algorithm_design)` | `candidate` | `process` | `operational` | computer programming seed | Problem framing usually precedes algorithmic or procedural design |
| `(form.algorithm_design, precedes, form.source_code_authoring)` | `candidate` | `process` | `operational` | computer programming seed | Designed steps are expressed through code authoring |
| `(form.source_code_authoring, produces, form.source_code)` | `candidate` | `process` | `operational` | computer programming seed | Code authoring emits source code as an artifact |
| `(form.source_code, input_to, form.testing)` | `candidate` | `process` | `operational` | computer programming seed | Source code becomes an input to testing and validation |
| `(form.testing, precedes, form.debugging)` | `candidate` | `process` | `operational` | computer programming seed | Failed or incomplete tests often lead into debugging |
| `(form.debugging, revised_into, form.source_code)` | `candidate` | `process` | `operational` | computer programming seed | Debugging creates revised source code rather than merely observing defects |
| `(form.semantic_hub, is_a, form.concept)` | `candidate` | `hierarchy` | `structural` | semantic hub seed | Semantic hub is a concept-level orientation node |
| `(form.semantic_hub, within, form.meta)` | `candidate` | `hierarchy` | `structural` | semantic hub seed | Semantic hub belongs to the vault's self-description layer |
| `(form.semantic_hub, associated_with, form.concept)` | `candidate` | `association` | `semantic-neighborhood` | semantic hub seed | Concept is the primary page currently shaped as a semantic hub |
| `(form.semantic_hub, associated_with, form.semantic_neighborhood)` | `candidate` | `association` | `semantic-neighborhood` | relational ring seeds | A hub orients a semantic neighborhood |
| `(form.semantic_hub, associated_with, form.direction)` | `candidate` | `association` | `semantic-neighborhood` | semantic hub seed | A semantic hub gives direction for traversal |
| `(form.semantic_hub, uses, form.relation_tuple)` | `candidate` | `dependency` | `operational` | semantic hub seed | Relation tuples make hub structure machine-navigable |
| `(form.semantic_hub, requires, form.boundary)` | `candidate` | `dependency` | `operational` | semantic hub seed | Hub pages need boundaries to avoid becoming vague indexes |
| `(form.semantic_hub, requires, form.follow_up_link)` | `candidate` | `dependency` | `operational` | relational ring seeds | Hub pages should offer selective next links |
| `(form.semantic_hub, requires, form.link_quality)` | `candidate` | `dependency` | `operational` | relational ring seeds | Hub links need quality pressure, not only quantity |
| `(form.semantic_hub, confused_with, form.index)` | `candidate` | `confusion` | `semantic-neighborhood` | relational ring seeds | Hubs can be mistaken for indexes when relation meaning is weak |
| `(form.follow_up_link, enables, form.concept_trail)` | `candidate` | `dependency` | `operational` | relational ring seeds | Follow-up links can compose into guided trails |
| `(form.discovery_path, associated_with, form.open_question)` | `candidate` | `association` | `semantic-neighborhood` | relational ring seeds | Open questions often initiate discovery paths |
| `(form.process_shape, associated_with, form.process_graph)` | `candidate` | `association` | `semantic-neighborhood` | relational ring seeds | Process shape points toward explicit process graphs |
| `(form.source_structure, associated_with, form.source_packet)` | `candidate` | `association` | `semantic-neighborhood` | relational ring seeds | Source structures organize source packets |
| `(form.index, confused_with, form.semantic_hub)` | `candidate` | `confusion` | `semantic-neighborhood` | relational ring seeds | Reciprocal confusion warning from index to hub |
| `(movement.resonance, contrasts_with, movement.dissipation)` | `candidate` | `contrast` | `semantic-neighborhood` | movement core ledger | Important non-collapse in the RCL neighborhood |
| `(movement.flow, not_equivalent_to, form.capacity)` | `candidate` | `contrast` | `structural` | capacity seed and movement core ledger | Flow is not the same as the capacity that permits or carries it |
| `(direction.governance, enables, form.ledger)` | `candidate` | `dependency` | `operational` | direction governance and meta form ledgers | Governance makes ledger authority operative |
| `(direction.alignment, associated_with, direction.interoperability)` | `candidate` | `association` | `semantic-neighborhood` | direction alignment ledger | Strong neighborhood with distinct role |

## Usage Notes

- `alias_of` should remain narrower than every kind of similarity.
- `within` and `part_of` should not be treated as interchangeable.
- `associated_with` is broader and softer than `adjacent_to`.
- `uses` is weaker than `requires`; use it when an object is operationally employed, not when it is logically unavoidable.
- `has_stage`, `precedes`, and `input_to` should be used together when a process needs to become queryable as a graph.
- `not_equivalent_to` is stronger than `contrasts_with`.
- `confused_with` is about observed drift, not about true equivalence.
- Some tuples use concepts not yet fully seeded, such as `form.programming_language`, `form.source_code`, `form.problem_framing`, `form.algorithm_design`, `form.source_code_authoring`, `form.testing`, and `form.heuristic`. That is allowed as a forward pointer, but those concepts should be seeded soon.

## Coverage Against Meaning Layers

| Meaning layer | Covered by | Status |
| --- | --- | --- |
| Identity | `alias_of`, `acronym_for`, `not_equivalent_to` | Covered enough to separate labels from concepts |
| Equivalence | `alias_of`, `acronym_for` | Covered for lexical and naming convergence |
| Hierarchy | `is_a`, `within`, `part_of` | Covered for kind, branch, and composition |
| Association | `adjacent_to`, `associated_with`, `used_with` | Covered for neighborhoods that are not identity |
| Contrast | `contrasts_with`, `not_equivalent_to` | Covered for tension and boundary sharpening |
| Dependency | `uses`, `requires`, `enables`, `depends_on` | Covered for operational reliance and prerequisites |
| Process | `has_stage`, `precedes`, `input_to`, `produces`, `tested_by`, `transforms_into`, `revised_into` | Covered as directed traversable graph structure |
| Confusion | `confused_with`, `overlaps_with` | Covered for human and model drift |

## Practical Next Step

The next relation-governance move should be:

1. create dedicated relation records for `alias_of`, `uses`, `has_stage`, `precedes`, `confused_with`, and `contrasts_with`;
2. seed the forward-pointer process concepts under computer programming;
3. enrich existing concept seeds with at least one contrast, one dependency, and one confusion relation where useful.
