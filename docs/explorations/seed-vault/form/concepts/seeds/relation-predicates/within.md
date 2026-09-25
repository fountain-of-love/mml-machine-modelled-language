---
artifact: relation-concept-seed
status: candidate
updated: 2026-08-28
local_id: relation.within
canonical_label: within
relation_family: hierarchy
weight_class: structural
directionality: directed
language: en
last_checked: 2026-08-28
---

# within

## Overview

`within` is a placement relation. It says a concept sits inside a branch, scope, field, or umbrella without claiming strict type identity.

This relation deserves its own page because many ontology mistakes come from using one hierarchy word for everything. [[within]] keeps placement distinct from [[is_a]] and [[part_of]].

Graph links worth following: [[Hierarchy]], [[Scope]], [[Branch]], [[Field]], [[Concept Ledger]], [[is_a]], and [[part_of]].

## Definition

`within` is a directed hierarchy relation for placing a concept inside a broader scope, field, branch, or umbrella.

## Usage Rule

| Field | Value |
| --- | --- |
| Subject kind | [[Concept]] |
| Object kind | Scope, branch, field, umbrella, or parent concept |
| Use when | Placement matters but strict type or composition would be too strong |
| Do not use when | The subject is literally a part of the object or a subtype of the object |

## Examples

| Subject | Relation | Object | Reading |
| --- | --- | --- | --- |
| [[Semantic Hub]] | [[within]] | [[Meta]] | Semantic hub belongs to the vault self-description layer |
| [[Concept]] | [[within]] | [[Meta]] | Concept is a meta-form concept in this vault |

## Boundary

Included:

- scope placement
- branch placement
- field membership

Excluded:

- strict type identity
- physical or logical component relation
- dependency relation

## Common Confusions

| Confusion | Boundary correction |
| --- | --- |
| [[within]] vs [[is_a]] | `within` places; `is_a` types |
| [[within]] vs [[part_of]] | `within` is broader and softer than compositional part-whole structure |

## Sources

| Source | Role |
| --- | --- |
| [[Relation Ledger]] | Governing vocabulary source |
| [[Concept Ledger]] | Branch-placement usage |

## Open Questions

- Should `within` be replaced by narrower relations for discipline, branch, and scope later?
