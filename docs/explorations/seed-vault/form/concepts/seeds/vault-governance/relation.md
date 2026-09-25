---
artifact: concept-seed
status: candidate
updated: 2026-08-28
local_id: form.relation
canonical_label: relation
ledger: Form-Meta-Concept-Ledger
language: en
last_checked: 2026-08-28
---

# Relation

## Overview

A relation is a meaningful connection between concepts. It is the edge that lets a concept graph say more than "these notes are nearby."

In the [[Seed Vault]], relations should be both governed and navigable. A relation predicate such as [[uses]], [[requires]], or [[confused_with]] should have its own concept page so readers can inspect what the relation means, where it applies, and what it should not be confused with.

Graph links worth following: [[Concept]], [[Relation Tuple]], [[Node]], [[Edge]], [[Graph Structure]], [[Relation Ledger]], [[Relation Predicate Concept Ledger]], [[is_a]], [[within]], [[associated_with]], [[uses]], [[requires]], [[confused_with]], and [[enables]].

## Definition

Relation is a governed semantic connection between concepts, usually expressed through a predicate that can be used in subject-relation-object structures.

## Relation Interface

| Subject | Relation | Object | Reading |
| --- | --- | --- | --- |
| [[Relation]] | [[is_a]] | [[Concept]] | Relation is itself modeled as a concept |
| [[Relation]] | [[associated_with]] | [[Relation Tuple]] | Relation tuples express relation instances |
| [[Relation]] | [[requires]] | [[Boundary]] | Relations need boundary rules to avoid becoming vague |
| [[Relation]] | [[associated_with]] | [[Edge]] | Relations behave like typed graph edges |

## Boundary

Included:

- typed semantic connection
- predicate concept
- graph edge meaning
- governed subject-object connection

Excluded:

- untyped hyperlink
- visual line with no semantic meaning
- loose association without declared predicate
- raw tuple syntax by itself

## Common Confusions

| Confusion | Boundary correction |
| --- | --- |
| [[Relation]] vs [[Relation Tuple]] | Relation is the predicate meaning; relation tuple is a subject-predicate-object expression |
| [[Relation]] vs [[Edge]] | Edge is graph structure; relation is semantic meaning attached to an edge |
| [[Relation]] vs [[Link]] | A link is clickable; a relation is a governed meaning-bearing connection |

## Sources

| Source | Role |
| --- | --- |
| [[Relation Ledger]] | Governing vocabulary source |
| [[Semantic Hub]] | Active relation table use |
| [[Relation Predicate Concept Ledger]] | Predicate concept governance |

## Validation Notes

| Check | Result |
| --- | --- |
| Relation modeled as concept | yes |
| Predicate pages linked | yes |
| Boundary distinguishes relation from raw link | yes |

## Open Questions

- Should every relation predicate receive a full seed before broad use?
- Should relation instances become separate evidence-bearing records?
