---
artifact: relation-concept-seed
status: candidate
updated: 2026-08-28
local_id: relation.associated_with
canonical_label: associated_with
relation_family: association
weight_class: semantic-neighborhood
directionality: undirected
language: en
last_checked: 2026-08-28
---

# associated_with

## Overview

`associated_with` is a broad neighborhood relation. It says two concepts travel together often enough to help navigation, but not strongly enough to claim identity, hierarchy, dependency, or process.

This relation is useful early in a growing vault because it lets the graph breathe. It can connect [[Semantic Hub]] to [[Semantic Neighborhood]] before every narrower relation has been decided.

Graph links worth following: [[Association]], [[Semantic Neighborhood]], [[Relation]], [[adjacent_to]], [[used_with]], [[not_equivalent_to]], and [[confused_with]].

## Definition

`associated_with` is an undirected semantic-neighborhood relation for concepts that are meaningfully related without a stronger governed relation.

## Usage Rule

| Field | Value |
| --- | --- |
| Subject kind | [[Concept]] |
| Object kind | [[Concept]] |
| Use when | Two concepts are useful neighbors but the exact relation is broad or still emerging |
| Do not use when | Identity, hierarchy, dependency, process, or contrast is already clear |

## Examples

| Subject | Relation | Object | Reading |
| --- | --- | --- | --- |
| [[Semantic Hub]] | [[associated_with]] | [[Semantic Neighborhood]] | A hub orients a neighborhood |
| [[Semantic Hub]] | [[associated_with]] | [[Direction]] | A hub gives traversal direction |

## Boundary

Included:

- broad conceptual neighborhood
- early-stage useful relation
- co-travel without identity

Excluded:

- synonymy
- strict containment
- required dependency
- confusion warning

## Common Confusions

| Confusion | Boundary correction |
| --- | --- |
| [[associated_with]] vs [[confused_with]] | Association is useful nearness; confusion records boundary drift |
| [[associated_with]] vs [[requires]] | Association does not imply a prerequisite |

## Sources

| Source | Role |
| --- | --- |
| [[Relation Ledger]] | Governing vocabulary source |
| [[Semantic Hub]] | First active navigation use |

## Open Questions

- When should a broad association be promoted to a narrower relation?
