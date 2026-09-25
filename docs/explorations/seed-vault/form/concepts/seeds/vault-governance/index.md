---
artifact: concept-seed
status: candidate
updated: 2026-08-28
local_id: form.index
canonical_label: index
ledger: Form-Meta-Concept-Ledger
language: en
last_checked: 2026-08-28
---

# Index

## Overview

An index is an organized list of entries that helps a reader find things. It is useful, but it is not the same as a [[Semantic Hub]].

In the [[Seed Vault]], the distinction matters because an index can point to many concepts without explaining why those concepts are near each other. A semantic hub adds orientation, relation structure, boundary, and follow-up direction.

Graph links worth following: [[Semantic Hub]], [[Category]], [[Table Of Contents]], [[Concept Trail]], [[Navigation]], and [[Link Quality]].

## Definition

Index is a structured finding aid that lists entries for lookup without necessarily asserting rich semantic relations among them.

## Relation Interface

```text
(form.index, is_a, form.concept)
(form.index, within, form.meta)
(form.index, associated_with, form.navigation)
(form.index, confused_with, form.semantic_hub)
(form.semantic_hub, confused_with, form.index)
```

## Boundary

Included:

- lookup lists
- alphabetical or topical entry lists
- navigation aids
- finding surfaces

Excluded:

- semantic hub
- semantic neighborhood
- relation ledger
- concept trail

## Common Confusions

| Confusion | Boundary correction |
| --- | --- |
| [[Index]] vs [[Semantic Hub]] | An index lists; a semantic hub orients and relates |
| [[Index]] vs [[Concept Trail]] | An index supports lookup; a trail supports ordered movement |
| [[Index]] vs [[Relation Ledger]] | An index lists entries; a relation ledger governs edge meanings |

## Sources

| Source | Role |
| --- | --- |
| [[Semantic Hub]] | Defines index as a common confusion |
| [[Concept Ledger]] | Example of a governed index-like surface |

## Validation Notes

| Check | Result |
| --- | --- |
| Distinct from semantic hub | yes |
| Finding-aid role present | yes |

## Open Questions

- Should every subledger also expose an index page?
- When does an index become a semantic hub?
