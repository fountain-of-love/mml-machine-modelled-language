---
artifact: relation-concept-seed
status: candidate
updated: 2026-08-28
local_id: relation.enables
canonical_label: enables
relation_family: dependency
weight_class: operational
directionality: directed
language: en
last_checked: 2026-08-28
---

# enables

## Overview

`enables` is a directed dependency relation for possibility, support, or activation. It says the subject makes the object possible, easier, or more operative.

This relation matters because some concepts do not contain or require each other, but one still gives the other functional force. A [[Follow-Up Link]] can [[enables|enable]] a [[Concept Trail]] without being the trail itself.

Graph links worth following: [[Dependency]], [[uses]], [[requires]], [[depends_on]], [[Activation]], [[Direction]], and [[Concept Trail]].

## Definition

`enables` is a directed dependency relation where the subject makes the object possible, more accessible, or more operational.

## Usage Rule

| Field | Value |
| --- | --- |
| Subject kind | [[Concept]], artifact, condition, or process |
| Object kind | Enabled concept, practice, process, or structure |
| Use when | The subject opens capacity or possibility for the object |
| Do not use when | The subject merely uses or requires the object |

## Examples

| Subject | Relation | Object | Reading |
| --- | --- | --- | --- |
| [[Follow-Up Link]] | [[enables]] | [[Concept Trail]] | Follow-up links can form guided trails |
| [[Governance]] | [[enables]] | [[Ledger]] | Governance makes ledger authority operative |

## Boundary

Included:

- making possible
- opening operational capacity
- support for traversal or activation

Excluded:

- strict requirement
- simple use
- broad association

## Common Confusions

| Confusion | Boundary correction |
| --- | --- |
| [[enables]] vs [[requires]] | `enables` opens possibility; `requires` states necessity |
| [[enables]] vs [[uses]] | `uses` employs an object; `enables` gives force to another concept or process |

## Sources

| Source | Role |
| --- | --- |
| [[Relation Ledger]] | Governing vocabulary source |
| [[Semantic Hub]] | Relational ring use through follow-up links |

## Open Questions

- Should enabling relations distinguish weak support from strong activation?
