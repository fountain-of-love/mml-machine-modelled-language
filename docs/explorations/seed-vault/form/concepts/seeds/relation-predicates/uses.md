---
artifact: relation-concept-seed
status: candidate
updated: 2026-08-28
local_id: relation.uses
canonical_label: uses
relation_family: dependency
weight_class: operational
directionality: directed
language: en
last_checked: 2026-08-28
---

# uses

## Overview

`uses` is an operational dependency relation. It says the subject employs the object as a tool, representation, structure, or method, without claiming that the object is always logically required.

This is a useful middle-strength relation. It is stronger than [[associated_with]] but weaker than [[requires]].

Graph links worth following: [[Dependency]], [[Relation Tuple]], [[requires]], [[depends_on]], [[enables]], and [[used_with]].

## Definition

`uses` is a directed dependency relation where the subject operationally employs the object.

## Usage Rule

| Field | Value |
| --- | --- |
| Subject kind | [[Concept]], process, practice, system, or artifact |
| Object kind | Tool, method, representation, concept, or artifact |
| Use when | The object helps the subject operate or become navigable |
| Do not use when | The object is merely nearby, or when the subject cannot exist without it |

## Examples

| Subject | Relation | Object | Reading |
| --- | --- | --- | --- |
| [[Semantic Hub]] | [[uses]] | [[Relation Tuple]] | Hub structure uses relation tuples for machine navigation |
| [[Process Shape]] | [[uses]] | [[Relation Tuple]] | Process shape uses tuples to become graph-ready |

## Boundary

Included:

- operational employment
- method or artifact use
- medium-strength dependency

Excluded:

- loose association
- logical necessity
- co-use without direction

## Common Confusions

| Confusion | Boundary correction |
| --- | --- |
| [[uses]] vs [[requires]] | `uses` is weaker; `requires` means the subject cannot be adequately realized without the object |
| [[uses]] vs [[used_with]] | `uses` is directed; `used_with` is co-use |

## Sources

| Source | Role |
| --- | --- |
| [[Relation Ledger]] | Governing vocabulary source |
| [[Semantic Hub]] | First active navigation use |

## Open Questions

- Should repeated `uses` relations eventually become typed by role, such as tool, method, or representation?
