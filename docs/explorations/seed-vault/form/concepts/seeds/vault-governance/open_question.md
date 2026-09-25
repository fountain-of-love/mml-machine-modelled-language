---
artifact: concept-seed
status: candidate
updated: 2026-08-28
local_id: form.open_question
canonical_label: open_question
ledger: Form-Meta-Concept-Ledger
language: en
last_checked: 2026-08-28
---

# Open Question

## Overview

An open question is a named uncertainty that remains attached to a concept, relation, source, or process. It keeps uncertainty visible instead of hiding it in prose.

In the [[Seed Vault]], open questions are productive. They point toward future research, concept splitting, source validation, relation refinement, or deeper seed writing.

Graph links worth following: [[Evidence]], [[Validation Notes]], [[Boundary]], [[Granularity]], [[Alignment]], [[Discovery Path]], and [[Semantic Hub]].

## Definition

Open question is a tracked unresolved issue that preserves uncertainty and gives direction for future ontology work.

## Relation Interface

```text
(form.open_question, is_a, form.concept)
(form.open_question, within, form.meta)
(form.open_question, associated_with, form.evidence)
(form.open_question, associated_with, form.discovery_path)
(form.semantic_hub, associated_with, form.open_question)
```

## Boundary

Included:

- unresolved ontology decisions
- research prompts
- validation gaps
- known ambiguity requiring follow-up

Excluded:

- rhetorical questions
- completed decisions
- vague TODOs without concept impact

## Common Confusions

| Confusion | Boundary correction |
| --- | --- |
| [[Open Question]] vs [[TODO]] | A TODO names work; an open question names unresolved meaning or evidence |
| [[Open Question]] vs [[Validation Note]] | A validation note records a check; an open question records what remains unsettled |

## Sources

| Source | Role |
| --- | --- |
| [[Concept]] | Uses open questions as concept governance |
| [[Semantic Hub]] | Forward-pointer source |

## Validation Notes

| Check | Result |
| --- | --- |
| Uncertainty remains visible | yes |
| Distinct from generic TODO | yes |

## Open Questions

- Should open questions have owners, dates, and resolution states?
- When does an open question become a requirement?
