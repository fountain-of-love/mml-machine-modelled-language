---
artifact: concept-seed
status: candidate
updated: 2026-08-28
local_id: form.discovery_path
canonical_label: discovery_path
ledger: Form-Meta-Concept-Ledger
language: en
last_checked: 2026-08-28
---

# Discovery Path

## Overview

A discovery path is the route by which a question, source, model trace, or reader exploration leads toward new concepts or relations.

In the [[Seed Vault]], discovery paths matter because not all useful structure is known upfront. Some concepts are found by following tension, ambiguity, evidence gaps, or unexpectedly strong links.

Graph links worth following: [[Open Question]], [[Evidence]], [[Semantic Neighborhood]], [[Concept Trail]], [[Follow-Up Link]], [[Movement]], and [[Observatory]].

## Definition

Discovery path is an exploratory route that produces or motivates new concept, relation, evidence, or validation work.

## Relation Interface

```text
(form.discovery_path, is_a, form.concept)
(form.discovery_path, within, form.meta)
(form.discovery_path, associated_with, form.open_question)
(form.discovery_path, uses, form.follow_up_link)
(form.discovery_path, produces, form.concept)
```

## Boundary

Included:

- routes from question to concept
- routes from source to seed
- exploration paths through semantic neighborhoods
- evidence-driven expansion

Excluded:

- arbitrary browsing
- a static reading list
- phase roadmap unless it creates ontology knowledge

## Common Confusions

| Confusion | Boundary correction |
| --- | --- |
| [[Discovery Path]] vs [[Concept Trail]] | A discovery path explores and may create; a concept trail guides through selected known nodes |
| [[Discovery Path]] vs [[Roadmap]] | A roadmap plans work; a discovery path records knowledge emergence |

## Sources

| Source | Role |
| --- | --- |
| [[Semantic Hub]] | Forward-pointer source |
| [[Open Question]] | Common starting point |

## Validation Notes

| Check | Result |
| --- | --- |
| Exploratory nature present | yes |
| Distinct from static trail | yes |

## Open Questions

- Should discovery paths be captured as movement concepts instead of form concepts?
- When does a discovery path become evidence?
