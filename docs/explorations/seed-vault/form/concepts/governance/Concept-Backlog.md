---
artifact: governance
status: active
authority: concept-intake
updated: 2026-08-28
---

# Concept Backlog

## Purpose

This backlog records concept candidates that are worth investigating but are not yet accepted as governed Seed Vault concept seeds.

The backlog is an intake and prioritization instrument. It is not itself a concept authority.

Use it to:

- collect promising candidate concepts;
- track where they came from;
- record why they matter;
- mark whether they are duplicates, aliases, siblings, or new concepts; and
- decide what should be promoted into a draft seed.

## Workflow States

| State | Meaning |
| --- | --- |
| `captured` | Candidate has been recorded but not yet reviewed |
| `triaged` | Candidate has been grouped, deduplicated, or routed |
| `drafting` | Candidate is ready for a first concept seed draft |
| `blocked` | Candidate cannot progress without more evidence or a boundary decision |
| `promoted` | Candidate has been turned into a concept seed or merged into an existing one |
| `rejected` | Candidate is not useful as a distinct concept under the current vault scope |

## Intake Fields

Each backlog item should capture:

- `candidate label`
- `proposed local id`
- `source type`
- `source reference`
- `rationale`
- `status`
- `suspected action`
- `related concepts`
- `notes`

## Suspected Actions

Use one of these before a concept is formally reviewed:

| Action | Meaning |
| --- | --- |
| `new-concept` | Likely deserves its own concept seed |
| `alias-of-existing` | Likely surface variant of an existing concept |
| `sibling-of-existing` | Close to an existing concept but not identical |
| `split-existing` | Suggests one broad concept may need to be divided |
| `merge-candidates` | Multiple backlog items probably refer to the same concept |
| `relation-predicate` | Better governed as a relation predicate than a structural concept |
| `out-of-scope` | Interesting, but not useful for the current vault boundary |

## Current Intake

| Candidate label | Proposed local id | Source type | Source reference | Status | Suspected action | Related concepts | Rationale |
| --- | --- | --- | --- | --- | --- | --- | --- |
| semantic field | `form.semantic_field` | architectural note | `docs/explorations/llm-concept-inventory.md` | `captured` | `new-concept` | `form.semantic_neighborhood`, `form.concept` | Useful for distinguishing a local governed structure from a looser neighborhood |
| concept inventory | `form.concept_inventory` | existing seed and architecture | `form/concepts` package | `captured` | `alias-of-existing` | `form.inventory` | May already be covered by `inventory`, but could need a more specific structural variant |
| embedding neighborhood | `form.embedding_neighborhood` | observatory proposal | `movement/observatory/vllm.md` | `captured` | `sibling-of-existing` | `form.semantic_neighborhood` | May help distinguish semantic neighborhoods from vector-space neighborhoods |
| concept cluster | `form.concept_cluster` | observatory proposal | `movement/observatory` workflow | `captured` | `new-concept` | `form.semantic_hub`, `form.semantic_neighborhood` | Needed if group-level discovery becomes a governed unit |
| alias set | `form.alias_set` | inventory governance need | `Concept-Inventory-Architecture.md` | `captured` | `new-concept` | `form.concept` | Useful for governing multi-surface identity without flattening distinct senses |

## Triage Rules

1. A backlog item is not promoted because a model produced it once.
2. A backlog item should be compared against existing seeds before drafting.
3. A backlog item should record whether embeddings suggest duplication or clustering pressure.
4. Boundary ambiguity is a reason to pause promotion, not to force a premature decision.
5. Promotion should prefer the smallest useful distinction that preserves clarity.
