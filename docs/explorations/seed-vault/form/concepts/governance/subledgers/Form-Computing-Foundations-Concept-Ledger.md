---
artifact: governance
status: active
authority: concept-maturity
updated: 2026-08-27
scope: form-computing-foundations
source_family: wikipedia-wikidata-linked-data
---

# Form Computing Foundations Concept Ledger

## Purpose

This subledger deepens the `computing` umbrella with foundational computing concepts that recur across theory, programming, and system construction.

## Linked Data Fields

- `wikidata_id`: stable item identifier
- `concept_uri`: globally resolvable Wikidata entity URI
- `wikipedia_anchor`: English Wikipedia concept page
- `tuple_hint`: first RDF-like reading for the concept's placement

## Concepts

| Local id | Canonical label | Status | Boundary confidence | Bucket | Wikidata id | Concept URI | Wikipedia anchor | Tuple hint | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `form.algorithm` | `algorithm` | `candidate` | medium | concept-class | `Q8366` | `https://www.wikidata.org/entity/Q8366` | `https://en.wikipedia.org/wiki/Algorithm` | `(form.algorithm, within, form.computer_science)` | Foundational procedural concept in computing and mathematics |
| `form.data_structure` | `data_structure` | `candidate` | medium | concept-class | `Q175263` | `https://www.wikidata.org/entity/Q175263` | `https://en.wikipedia.org/wiki/Data_structure` | `(form.data_structure, within, form.computer_science)` | Structured data-organization concept; should remain distinct from data itself |
| `form.computer_programming` | `computer_programming` | `candidate` | medium | activity-discipline | `Q80006` | `https://www.wikidata.org/entity/Q80006` | `https://en.wikipedia.org/wiki/Computer_programming` | `(form.computer_programming, within, form.computer_science)` | Process and skill concept bridging theory and practice |
| `form.information_theory` | `information_theory` | `candidate` | medium | discipline | `Q1190554` | `https://www.wikidata.org/entity/Q1190554` | `https://en.wikipedia.org/wiki/Information_theory` | `(form.information_theory, adjacent_to, form.computer_science)` | Foundational but not reducible to computer science alone |

## Source Model

These concept rows follow an open linked data pattern:

```text
local concept id
  -> wikidata item id
  -> entity URI
  -> English Wikipedia article
  -> tuple placement inside the Seed Vault
```

## Governance Notes

- `computer_programming` is admitted here as a high-value child under the computing umbrella even though Wikidata also treats it partly as an activity or skill.
- `information_theory` remains here because it is operationally central to computing, while still retaining its formal-science identity elsewhere.

