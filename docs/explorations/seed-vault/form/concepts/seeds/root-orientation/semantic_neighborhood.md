---
artifact: concept-seed
status: candidate
updated: 2026-08-28
local_id: form.semantic_neighborhood
canonical_label: semantic_neighborhood
ledger: Form-Meta-Concept-Ledger
language: en
last_checked: 2026-08-28
---

# Semantic Neighborhood

## Overview

A semantic neighborhood is the meaningful field around a [[Concept]]. It is made of nearby concepts, contrasts, dependencies, aliases, confusions, source structures, and paths worth following.

In the [[Seed Vault]], a semantic neighborhood prevents a concept from becoming a lonely definition. It lets [[Concept]] pages show where a term lives, what it touches, what it should not be confused with, and which links can grow next.

Graph links worth following: [[Concept]], [[Semantic Hub]], [[Relation]], [[Relation Tuple]], [[Graph Structure]], [[Boundary]], [[Link Quality]], [[Concept Trail]], and [[Discovery Path]].

## Key Identity

| Field | Value |
| --- | --- |
| Canonical label | `semantic_neighborhood` |
| Local id | `form.semantic_neighborhood` |
| Status | `candidate` |
| Branch | [[Form]] |
| Ledger placement | [[Form Meta Concept Ledger]] |

## Definition

Semantic neighborhood is the set of meaningful, typed, and reviewable connections surrounding a concept.

## Relation Interface

```text
(form.semantic_neighborhood, is_a, form.concept)
(form.semantic_neighborhood, within, form.meta)
(form.semantic_neighborhood, associated_with, form.semantic_hub)
(form.semantic_neighborhood, uses, form.relation_tuple)
(form.semantic_neighborhood, requires, form.link_quality)
```

## Boundary

Included:

- meaningful neighboring concepts
- relation-linked surroundings
- contrast and confusion context
- follow-up paths from a concept

Excluded:

- every page that happens to link to a concept
- untyped link clutter
- search results
- a category treated as semantic structure without review

## Common Confusions

| Confusion | Boundary correction |
| --- | --- |
| [[Semantic Neighborhood]] vs [[Category]] | A category groups; a semantic neighborhood explains meaningful nearness |
| [[Semantic Neighborhood]] vs [[Index]] | An index lists; a semantic neighborhood relates |
| [[Semantic Neighborhood]] vs [[Semantic Hub]] | The hub orients; the neighborhood is the surrounding field |

## Sources

| Source | Role |
| --- | --- |
| [[Semantic Hub]] | Primary local source |
| [[Concept]] | First page requiring this neighborhood |
| [[Relation Ledger]] | Relation vocabulary used to type the neighborhood |

## Validation Notes

| Check | Result |
| --- | --- |
| Human-readable overview present | yes |
| Relation tuples present | yes |
| Boundary includes exclusions | yes |
| Hub distinction present | yes |

## Open Questions

- Should every mature concept require a semantic-neighborhood table?
- How many links make a neighborhood useful without becoming noisy?
