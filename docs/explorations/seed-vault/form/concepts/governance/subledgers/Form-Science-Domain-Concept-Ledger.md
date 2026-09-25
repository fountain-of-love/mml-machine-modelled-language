---
artifact: governance
status: active
authority: concept-maturity
updated: 2026-08-27
scope: science-domains
source_family: wikipedia-wikidata
---

# Form Science Domain Concept Ledger

## Purpose

This subledger records top-level science and technology domain concepts expanded from the Wikipedia inventory seed.

## Concepts

| Local id | Canonical label | Status | Boundary confidence | Bucket | Wikidata id | Concept URI | Wikipedia anchor | Source anchor | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `form.science` | `science` | `candidate` | medium | domain | `Q336` | `https://www.wikidata.org/entity/Q336` | `https://en.wikipedia.org/wiki/Science` | Wikipedia science / Wikidata science | Top-level scientific scope concept |
| `form.technology` | `technology` | `candidate` | medium | domain | `Q11016` | `https://www.wikidata.org/entity/Q11016` | `https://en.wikipedia.org/wiki/Technology` | Wikipedia technology / Wikidata technology | Top-level applied scope concept |
| `form.formal_science` | `formal_science` | `candidate` | medium | domain | `Q816264` | `https://www.wikidata.org/entity/Q816264` | `https://en.wikipedia.org/wiki/Formal_science` | Wikipedia mathematics and logic | Bridge domain for mathematics, logic, statistics, and computation |
| `form.natural_science` | `natural_science` | `candidate` | medium | domain | `Q188638` | `https://www.wikidata.org/entity/Q188638` | `https://en.wikipedia.org/wiki/Natural_science` | Wikipedia natural and physical sciences | Parent grouping for biological and physical branches |
| `form.applied_science` | `applied_science` | `candidate` | medium | domain | `Q1165180` | `https://www.wikidata.org/entity/Q1165180` | `https://en.wikipedia.org/wiki/Applied_science` | Wikipedia technology and applied sciences | Parent grouping for engineering and technology |
| `form.engineering` | `engineering` | `candidate` | medium | domain | `Q811430` | `https://www.wikidata.org/entity/Q811430` | `https://en.wikipedia.org/wiki/Engineering` | Wikipedia portals and categories | Umbrella engineering scope concept |
| `form.computing` | `computing` | `candidate` | medium | domain | `Q179310` | `https://www.wikidata.org/entity/Q179310` | `https://en.wikipedia.org/wiki/Computing` | Wikipedia technology and applied sciences | Umbrella computing scope concept |

## Governance Notes

- These concepts are scope-setting parents, not merely article labels.
- Child disciplines should link upward to one or more of these domain concepts without forcing a single tree too early.
