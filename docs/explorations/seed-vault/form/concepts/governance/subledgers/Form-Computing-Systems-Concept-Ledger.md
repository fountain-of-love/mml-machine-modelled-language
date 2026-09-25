---
artifact: governance
status: active
authority: concept-maturity
updated: 2026-08-27
scope: form-computing-systems
source_family: wikipedia-wikidata-linked-data
---

# Form Computing Systems Concept Ledger

## Purpose

This subledger deepens the `computing` umbrella with system and infrastructure concepts that support operational IT work.

## Linked Data Fields

- `wikidata_id`: stable item identifier
- `concept_uri`: globally resolvable Wikidata entity URI
- `wikipedia_anchor`: English Wikipedia concept page
- `tuple_hint`: first RDF-like reading for the concept's placement

## Concepts

| Local id | Canonical label | Status | Boundary confidence | Bucket | Wikidata id | Concept URI | Wikipedia anchor | Tuple hint | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `form.operating_system` | `operating_system` | `candidate` | medium | system-class | `Q9135` | `https://www.wikidata.org/entity/Q9135` | `https://en.wikipedia.org/wiki/Operating_system` | `(form.operating_system, within, form.information_technology)` | Core systems concept for operational computing environments |
| `form.computer_network` | `computer_network` | `candidate` | medium | system-class | `Q1301371` | `https://www.wikidata.org/entity/Q1301371` | `https://en.wikipedia.org/wiki/Computer_network` | `(form.computer_network, within, form.information_technology)` | Networked system concept; should remain distinct from networking as a discipline |
| `form.computer_networking` | `computer_networking` | `candidate` | medium | discipline | `Q10336440` | `https://www.wikidata.org/entity/Q10336440` | `https://en.wikipedia.org/wiki/Computer_networking` | `(form.computer_networking, within, form.computing)` | Field of work concerned with connecting computers |
| `form.database_management_system` | `database_management_system` | `candidate` | medium | software-system | `Q176165` | `https://www.wikidata.org/entity/Q176165` | `https://en.wikipedia.org/wiki/Database#Database_management_system` | `(form.database_management_system, within, form.information_technology)` | Operational database-system concept; narrower than information systems as a whole |
| `form.distributed_computing` | `distributed_computing` | `candidate` | medium | system-paradigm | `Q180634` | `https://www.wikidata.org/entity/Q180634` | `https://en.wikipedia.org/wiki/Distributed_computing` | `(form.distributed_computing, within, form.computer_science)` | Computing paradigm spanning theory and deployed systems |

## Governance Notes

- `computer_network` and `computer_networking` remain distinct: one is a system class, the other a field of work.
- `database_management_system` is chosen over bare `database` for the first operational pass because the software-system boundary is clearer.
- `distributed_computing` spans both theory and infrastructure, so its placement remains provisional.

