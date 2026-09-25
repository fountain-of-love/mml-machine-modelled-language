---
artifact: governance
status: active
authority: relation-concept-maturity
updated: 2026-08-28
scope: relation-predicate-concepts
---

# Relation Predicate Concept Ledger

## Purpose

This subledger records relation predicates as concepts in their own right.

The relation ledger governs how predicates are used. This subledger makes those predicates navigable in Obsidian, so a relation such as [[uses]] or [[requires]] can be opened, read, refined, and linked like any other concept.

## Concepts

| Local id | Canonical label | Status | Boundary confidence | Family | Notes |
| --- | --- | --- | --- | --- | --- |
| `relation.is_a` | `is_a` | `candidate` | medium | hierarchy | Strong type or kind relation |
| `relation.within` | `within` | `candidate` | medium | hierarchy | Scope, branch, or umbrella placement relation |
| `relation.associated_with` | `associated_with` | `candidate` | medium | association | Broad semantic-neighborhood relation |
| `relation.uses` | `uses` | `candidate` | medium | dependency | Directed operational-use relation |
| `relation.requires` | `requires` | `candidate` | medium | dependency | Strong prerequisite relation |
| `relation.confused_with` | `confused_with` | `candidate` | medium | confusion | Boundary-drift warning relation |
| `relation.enables` | `enables` | `candidate` | medium | dependency | Possibility or activation relation |

## Governance Notes

- Predicate pages should explain when a relation is useful and when a neighboring relation is sharper.
- Predicate pages should be linked from active relation tables, not only from code-block tuples.
- Relation predicates remain governed by the central relation vocabulary even when they are represented as concepts.
