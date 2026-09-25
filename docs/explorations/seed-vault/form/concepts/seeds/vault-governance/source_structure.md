---
artifact: concept-seed
status: candidate
updated: 2026-08-28
local_id: form.source_structure
canonical_label: source_structure
ledger: Form-Meta-Concept-Ledger
language: en
last_checked: 2026-08-28
---

# Source Structure

## Overview

Source structure is the way evidence is organized before it becomes ontology material. It includes page sections, headings, tables, metadata, source roles, extraction rules, and validation notes.

In the [[Seed Vault]], source structure matters because a concept should not merely cite a page. It should preserve enough shape from its sources that humans and LLMs can see what kind of evidence was used and where it belongs.

Graph links worth following: [[Source Packet]], [[Evidence]], [[Validation Notes]], [[Concept]], [[Semantic Hub]], [[Extraction Rule]], and [[Provenance]].

## Definition

Source structure is the reusable organization pattern by which source material is selected, sectioned, attributed, normalized, and validated for concept work.

## Relation Interface

```text
(form.source_structure, is_a, form.concept)
(form.source_structure, within, form.meta)
(form.source_structure, associated_with, form.source_packet)
(form.semantic_hub, associated_with, form.source_structure)
(form.source_structure, requires, form.validation_note)
```

## Boundary

Included:

- source headings and sections
- source roles
- extraction mappings
- validation checks
- attribution structure

Excluded:

- copied source text as such
- raw URLs without role
- unsourced claims
- citation style alone

## Common Confusions

| Confusion | Boundary correction |
| --- | --- |
| [[Source Structure]] vs [[Source Packet]] | Structure is the organizing shape; packet is the collected source bundle |
| [[Source Structure]] vs [[Provenance]] | Structure records organization; provenance records origin and trace |

## Sources

| Source | Role |
| --- | --- |
| Amazonite example page | Structural inspiration |
| [[Semantic Hub]] | Forward-pointer source |
| [[Concept]] | Page-contract source |

## Validation Notes

| Check | Result |
| --- | --- |
| Source role visible | yes |
| Boundary excludes raw copying | yes |
| Connected to evidence and validation | yes |

## Open Questions

- Should each source type get a reusable extraction template?
- How much source structure should be preserved when sources disagree?
