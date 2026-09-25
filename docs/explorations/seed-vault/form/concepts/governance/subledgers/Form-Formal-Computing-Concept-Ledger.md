---
artifact: governance
status: active
authority: concept-maturity
updated: 2026-08-27
scope: formal-computing
source_family: wikipedia-wikidata
---

# Form Formal And Computing Concept Ledger

## Purpose

This subledger records formal-science and computing-adjacent disciplines admitted from the science-and-technology inventory seed.

## Concepts

| Local id | Canonical label | Status | Boundary confidence | Bucket | Wikidata id | Concept URI | Wikipedia anchor | Source anchor | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `form.mathematics` | `mathematics` | `candidate` | medium | discipline | `Q395` | `https://www.wikidata.org/entity/Q395` | `https://en.wikipedia.org/wiki/Mathematics` | Wikipedia mathematics and logic | Foundational formal science |
| `form.logic` | `logic` | `candidate` | medium | discipline | `Q8078` | `https://www.wikidata.org/entity/Q8078` | `https://en.wikipedia.org/wiki/Logic` | Wikipedia mathematics and logic | Formal reasoning branch |
| `form.statistics` | `statistics` | `candidate` | medium | discipline | `Q12483` | `https://www.wikidata.org/entity/Q12483` | `https://en.wikipedia.org/wiki/Statistics` | Wikipedia mathematics and logic | Formal and applied bridge discipline |
| `form.applied_mathematics` | `applied_mathematics` | `candidate` | medium | discipline | `Q855744` | `https://www.wikidata.org/entity/Q855744` | `https://en.wikipedia.org/wiki/Applied_mathematics` | Wikipedia mathematics and logic | Applied formal branch with broad reuse |
| `form.computational_science` | `computational_science` | `candidate` | medium | discipline | `Q7553` | `https://www.wikidata.org/entity/Q7553` | `https://en.wikipedia.org/wiki/Computational_science` | Wikipedia mathematics and logic | Bridge discipline across modeling, simulation, and computation |
| `form.operations_research` | `operations_research` | `candidate` | medium | discipline | `Q131524` | `https://www.wikidata.org/entity/Q131524` | `https://en.wikipedia.org/wiki/Operations_research` | Wikipedia mathematics and logic | Planning and optimization branch |
| `form.information_theory` | `information_theory` | `candidate` | medium | discipline | `Q131222` | `https://www.wikidata.org/entity/Q131222` | `https://en.wikipedia.org/wiki/Information_theory` | Wikipedia mathematics and logic | Mathematically grounded concept family |
| `form.computer_science` | `computer_science` | `candidate` | medium | discipline | `Q21198` | `https://www.wikidata.org/entity/Q21198` | `https://en.wikipedia.org/wiki/Computer_science` | Wikipedia technology and applied sciences | Stable core discipline in the computing family |
| `form.computer_architecture` | `computer_architecture` | `candidate` | medium | discipline | `Q173212` | `https://www.wikidata.org/entity/Q173212` | `https://en.wikipedia.org/wiki/Computer_architecture` | Wikipedia technology and applied sciences | Computing branch focused on system design structure |
| `form.computer_security` | `computer_security` | `candidate` | medium | discipline | `Q3510521` | `https://www.wikidata.org/entity/Q3510521` | `https://en.wikipedia.org/wiki/Computer_security` | Wikipedia technology and applied sciences | Computing branch focused on system integrity and defense |
| `form.human_computer_interaction` | `human_computer_interaction` | `candidate` | medium | discipline | `Q207434` | `https://www.wikidata.org/entity/Q207434` | `https://en.wikipedia.org/wiki/Human%E2%80%93computer_interaction` | Wikipedia technology and applied sciences | Interaction and design bridge discipline |
| `form.information_systems` | `information_systems` | `candidate` | medium | discipline | `Q121182` | `https://www.wikidata.org/entity/Q121182` | `https://en.wikipedia.org/wiki/Information_system` | Wikipedia technology and applied sciences | Organizational computing branch; nearest public linked-data item is singular `information system` |

## Governance Notes

- `computational_science` and `computer_science` are intentionally separate candidate concepts.
- `information_theory` should not be collapsed into `computer_science` or `statistics` even when it overlaps both.
- Operational computing work in this repository should usually treat `computing` as the umbrella branch and distinguish `computer_science`, `information_technology`, `information_systems`, and `software_engineering` within it.
