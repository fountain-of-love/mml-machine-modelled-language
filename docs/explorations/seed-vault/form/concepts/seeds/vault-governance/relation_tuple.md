---
artifact: concept-seed
status: candidate
updated: 2026-08-28
local_id: form.relation_tuple
canonical_label: relation_tuple
ledger: Form-Meta-Concept-Ledger
language: en
last_checked: 2026-08-28
---

# Relation Tuple

## Overview

A relation tuple is a compact way to express a semantic edge: subject, relation, object. It is useful for machines, but in Obsidian it should not stay trapped inside inert code blocks.

In the [[Seed Vault]], relation tuples can be shown as active navigational tables where the subject, predicate, and object are all clickable concepts. This keeps machine shape and human traversal together.

Graph links worth following: [[Relation]], [[Concept]], [[Node]], [[Edge]], [[Graph Structure]], [[Semantic Hub]], [[Link Quality]], and [[RDF]].

## Definition

Relation tuple is a structured subject-predicate-object expression of a relation between concepts.

## Active Obsidian Pattern

| Subject | Relation | Object | Reading |
| --- | --- | --- | --- |
| [[Semantic Hub]] | [[is_a]] | [[Concept]] | A semantic hub is a concept-level node |
| [[Semantic Hub]] | [[uses]] | [[Relation Tuple]] | A hub uses tuples, but should render them as active links |

## Boundary

Included:

- subject-predicate-object relation expression
- graph edge representation
- machine-readable relation hint
- active Obsidian table representation

Excluded:

- prose-only association
- untyped link
- raw code block when navigation is the goal

## Common Confusions

| Confusion | Boundary correction |
| --- | --- |
| [[Relation Tuple]] vs [[Relation]] | A relation tuple is an instance-like expression; a relation is the predicate concept |
| [[Relation Tuple]] vs [[Graph Link]] | A tuple states a typed edge; a graph link may be any clickable note link |

## Sources

| Source | Role |
| --- | --- |
| [[Relation Ledger]] | Tuple convention |
| [[Semantic Hub]] | First active-table conversion |

## Open Questions

- Should relation tuples eventually have IDs and evidence status?
