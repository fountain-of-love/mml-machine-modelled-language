---
artifact: relation-concept-seed
status: candidate
updated: 2026-08-28
local_id: relation.is_a
canonical_label: is_a
relation_family: hierarchy
weight_class: structural
directionality: directed
language: en
last_checked: 2026-08-28
---

# is_a

## Overview

`is_a` is a structural relation for saying that one concept is a kind, member, or typed instance of another concept. It is one of the strongest navigational links because it places a node inside an ontology.

In Obsidian, [[is_a]] should be clickable because it carries meaning of its own. A reader should be able to ask what kind of relation this is, when to use it, and when a softer relation such as [[within]] or [[associated_with]] would be better.

Graph links worth following: [[Hierarchy]], [[Concept]], [[Class]], [[Instance]], [[Relation]], [[Relation Tuple]], [[within]], and [[part_of]].

## Definition

`is_a` is a directed hierarchy relation used when the subject is treated as a member, instance, subtype, or kind of the object.

## Usage Rule

| Field | Value |
| --- | --- |
| Subject kind | [[Concept]] |
| Object kind | Broader [[Concept]], [[Class]], or type concept |
| Use when | The subject can truthfully be read as a kind or instance of the object |
| Do not use when | The subject is merely located inside, associated with, or operationally dependent on the object |

## Examples

| Subject | Relation | Object | Reading |
| --- | --- | --- | --- |
| [[Semantic Hub]] | [[is_a]] | [[Concept]] | A semantic hub is a concept-level node |
| [[Index]] | [[is_a]] | [[Concept]] | Index is modeled as a concept in this vault |

## Boundary

Included:

- kind-of relation
- instance-of relation
- subtype placement

Excluded:

- loose association
- topical containment
- part-whole membership

## Common Confusions

| Confusion | Boundary correction |
| --- | --- |
| [[is_a]] vs [[within]] | `is_a` says kind or instance; `within` says scoped placement |
| [[is_a]] vs [[part_of]] | `is_a` types a concept; `part_of` composes a whole |

## Sources

| Source | Role |
| --- | --- |
| [[Relation Ledger]] | Governing vocabulary source |
| [[Semantic Hub]] | First active navigation use |

## Open Questions

- Should `is_a` split into instance-of and subclass-of later?
