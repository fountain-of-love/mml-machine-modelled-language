---
artifact: relation-concept-seed
status: candidate
updated: 2026-08-28
local_id: relation.requires
canonical_label: requires
relation_family: dependency
weight_class: operational
directionality: directed
language: en
last_checked: 2026-08-28
---

# requires

## Overview

`requires` is a strong dependency relation. It says the subject cannot be adequately realized, interpreted, or governed without the object.

In the [[Seed Vault]], this relation should be used carefully. It gives strong navigation pressure, so it should not be used where [[uses]] or [[associated_with]] is enough.

Graph links worth following: [[Dependency]], [[uses]], [[depends_on]], [[enables]], [[Boundary]], and [[Validation Notes]].

## Definition

`requires` is a directed dependency relation where the object is necessary for the subject's adequate realization.

## Usage Rule

| Field | Value |
| --- | --- |
| Subject kind | [[Concept]], process, page, system, or practice |
| Object kind | Needed concept, artifact, condition, or governing structure |
| Use when | The subject loses adequacy without the object |
| Do not use when | The object is only commonly useful or merely adjacent |

## Examples

| Subject | Relation | Object | Reading |
| --- | --- | --- | --- |
| [[Semantic Hub]] | [[requires]] | [[Boundary]] | A hub needs a boundary to avoid becoming a vague index |
| [[Semantic Hub]] | [[requires]] | [[Link Quality]] | A hub needs link discipline |

## Boundary

Included:

- necessary conditions
- prerequisites
- strong operational dependency

Excluded:

- optional tools
- frequent association
- broad relevance

## Common Confusions

| Confusion | Boundary correction |
| --- | --- |
| [[requires]] vs [[uses]] | `requires` says necessary; `uses` says operationally employed |
| [[requires]] vs [[depends_on]] | `depends_on` can be broader and less constitutive |

## Sources

| Source | Role |
| --- | --- |
| [[Relation Ledger]] | Governing vocabulary source |
| [[Semantic Hub]] | First active navigation use |

## Open Questions

- Should `requires` demand evidence before admission as a stable relation?
