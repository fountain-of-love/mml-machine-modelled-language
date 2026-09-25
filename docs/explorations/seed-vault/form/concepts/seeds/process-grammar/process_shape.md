---
artifact: concept-seed
status: candidate
updated: 2026-08-28
local_id: form.process_shape
canonical_label: process_shape
ledger: Form-Meta-Concept-Ledger
language: en
last_checked: 2026-08-28
---

# Process Shape

## Overview

Process shape is the recognizable structure of a process: its stages, ordering, inputs, outputs, loops, checks, and revisions.

In the [[Seed Vault]], process shape lets a concept become traversable in time or execution. It is the bridge between a prose process description and a [[Process Graph]] that can be queried.

Graph links worth following: [[Process]], [[Process Graph]], [[Relation Tuple]], [[Stage]], [[Input]], [[Output]], [[Feedback]], and [[Revision]].

## Definition

Process shape is the structured pattern of stages and transitions that describes how a process unfolds.

## Relation Interface

```text
(form.process_shape, is_a, form.concept)
(form.process_shape, within, form.meta)
(form.process_shape, associated_with, form.process_graph)
(form.process_shape, uses, form.relation_tuple)
(form.process_shape, requires, form.stage)
(form.semantic_hub, associated_with, form.process_shape)
```

## Boundary

Included:

- stage ordering
- inputs and outputs
- loops and revisions
- process checkpoints
- graph-ready process descriptions

Excluded:

- topic association without sequence
- static hierarchy
- vague workflow prose with no typed edges

## Common Confusions

| Confusion | Boundary correction |
| --- | --- |
| [[Process Shape]] vs [[Process Graph]] | Shape is the conceptual pattern; graph is its explicit node-edge representation |
| [[Process Shape]] vs [[Procedure]] | A procedure may prescribe steps; process shape describes the structure of unfolding |

## Sources

| Source | Role |
| --- | --- |
| [[Relation Ledger]] | Process relation vocabulary |
| [[Semantic Hub]] | Forward-pointer source |
| [[Computer Programming]] | First concrete process-shape example |

## Validation Notes

| Check | Result |
| --- | --- |
| Stages mentioned | yes |
| Inputs and outputs mentioned | yes |
| Loops and revisions included | yes |

## Open Questions

- When should process shape become a separate process graph file?
- Which process predicates are minimal for useful traversal?
