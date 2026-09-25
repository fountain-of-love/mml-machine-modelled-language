---
artifact: governance
status: active
authority: concept-maturity
updated: 2026-08-28
scope: meta-form
---

# Form Meta Concept Ledger

## Purpose

This subledger records concepts the Seed Vault uses to organize, govern, and describe its own semantic materials.

These are not incidental document labels. They are reusable concepts in the vault's own ontology.

## Concepts

| Local id | Canonical label | Status | Boundary confidence | Source | Notes |
| --- | --- | --- | --- | --- | --- |
| `form.concept` | `concept` | `candidate` | high | Seed Vault concept-layer governance | Primary unit of semantic identity in the vault |
| `form.meta` | `meta` | `candidate` | medium | Seed Vault self-description usage | Reflective layer where the ontology describes its own concepts, ledgers, inventories, seeds, and governance |
| `form.semantic_hub` | `semantic_hub` | `candidate` | medium | Seed Vault concept-page design practice | Concept node or page that orients a meaningful neighborhood through selective links, structured relations, and validation |
| `form.relation` | `relation` | `candidate` | high | Relation ledger and semantic hub active relation table | Governed semantic connection between concepts |
| `form.semantic_neighborhood` | `semantic_neighborhood` | `candidate` | medium | Semantic hub relation ring | Meaningful, typed, reviewable field around a concept |
| `form.source_structure` | `source_structure` | `candidate` | medium | Semantic hub relation ring | Organization pattern by which source material is selected, sectioned, attributed, normalized, and validated |
| `form.process_shape` | `process_shape` | `candidate` | medium | Semantic hub relation ring | Structured pattern of stages and transitions that describes how a process unfolds |
| `form.open_question` | `open_question` | `candidate` | medium | Semantic hub relation ring | Tracked unresolved issue that preserves uncertainty and gives direction |
| `form.follow_up_link` | `follow_up_link` | `candidate` | medium | Semantic hub relation ring | Selective outbound link that guides the next useful traversal |
| `form.link_quality` | `link_quality` | `candidate` | medium | Semantic hub relation ring | Governed fitness of links for semantic navigation, readability, and growth |
| `form.concept_trail` | `concept_trail` | `candidate` | medium | Semantic hub relation ring | Selected traversal path through related concepts |
| `form.discovery_path` | `discovery_path` | `candidate` | medium | Semantic hub relation ring | Exploratory route that produces or motivates new concept, relation, evidence, or validation work |
| `form.index` | `index` | `candidate` | medium | Semantic hub relation ring | Structured finding aid that lists entries without necessarily asserting rich semantic relations |
| `form.relation_tuple` | `relation_tuple` | `candidate` | medium | Active relation navigation | Structured subject-predicate-object expression of a relation between concepts |
| `form.ledger` | `ledger` | `candidate` | high | Seed Vault governance usage | Governed record surface that tracks status, maturity, and review state for a bounded semantic set |
| `form.subledger` | `subledger` | `candidate` | high | Seed Vault governance usage | Scoped child ledger used when one ledger becomes too broad for one review surface |
| `form.inventory` | `inventory` | `candidate` | high | Seed Vault inventory architecture | Structured collection of candidate or accepted items gathered for scope, discovery, or review |
| `form.seed` | `seed` | `candidate` | medium | Seed Vault naming and intake practice | Minimal initiating unit from which broader semantic structure can grow |
| `form.discipline` | `discipline` | `candidate` | high | Science-and-technology inventory seed | Stable field or branch of knowledge suitable for reuse as a concept class |
| `form.domain` | `domain` | `candidate` | medium | Science-and-technology inventory seed | Broad scope concept grouping multiple related disciplines or technologies |
| `form.branch` | `branch` | `candidate` | medium | Seed Vault tree structure | Intermediate structural subdivision inside a larger concept family or hierarchy |

## Governance Notes

- `ledger` and `inventory` must remain distinct: a ledger governs accepted records, while an inventory may contain exploratory candidates.
- `seed` should remain broader than a document artifact alone; it names an initiating semantic unit, not only a file type.
- `discipline` is treated as a concept class in its own right and should be reusable across many specific disciplines.
