---
artifact: governance
status: active
authority: relation-governance
updated: 2026-08-27
scope: form-computing-relations
---

# Form Computing Relation Ledger

## Purpose

This ledger records the first explicit relations needed to make the computing branch operational as an ontology rather than a flat list.

## Linked Data Convention

This ledger now treats each relation row as a lightweight tuple:

```text
(subject, predicate, object)
```

The Seed Vault tuple is not identical to a Wikidata statement, but it is designed to be mappable to linked-data style structures.

Useful reference patterns:

- Wikidata statement model: item + property + value
- RDF triple: subject + predicate + object
- OWL or SKOS reading: class hierarchy, broader/narrower, related, or typed association

## Tuple Mapping Hints

| Seed Vault relation | Linked-data style reading | Typical Wikidata pattern |
| --- | --- | --- |
| `is_a` | `rdf:type` or class-membership-like reading | often `P31` or `P279`, depending on whether the target is treated as class or type |
| `within` | `skos:broader` or `part_of` style reading | often `P361`, `facet of`, or contextual `subclass of` |
| `adjacent_to` | `skos:related` style reading | often `different from`, `partially coincident with`, `facet of`, or a governed local relation |
| `specializes_within` | subclassing or scoped specialization | often `P279` with a stricter local boundary |

## Relations

| Tuple | Status | Linked-data reading | Source basis | Notes |
| --- | --- | --- | --- | --- |
| `(form.discipline, specializes_within, form.domain)` | `candidate` | scoped specialization | local Seed Vault governance | Generic governance relation for science-and-technology classification |
| `(form.computing, is_a, form.domain)` | `candidate` | class-membership-like | local Seed Vault governance | Computing is treated as a domain concept |
| `(form.computer_science, is_a, form.discipline)` | `candidate` | class-membership-like | Wikidata and local Seed Vault governance | Computer science is treated as a discipline concept |
| `(form.information_technology, is_a, form.technology)` | `candidate` | class-membership-like | Wikidata and local Seed Vault governance | Information technology is treated as a technology concept |
| `(form.computer_science, within, form.computing)` | `candidate` | broader-scope placement | Wikipedia and Wikidata topic structure | Computer science is one discipline within the broader computing domain |
| `(form.information_technology, within, form.computing)` | `candidate` | broader-scope placement | Wikipedia and Wikidata topic structure | IT sits within the broader computing domain operationally |
| `(form.information_systems, within, form.computing)` | `candidate` | broader-scope placement | Wikipedia inventory seed | Information systems belongs to the computing umbrella |
| `(form.software_engineering, within, form.computing)` | `candidate` | broader-scope placement | Wikipedia inventory seed and Wikidata | Software engineering belongs operationally to the computing umbrella |
| `(form.computer_architecture, within, form.computing)` | `candidate` | broader-scope placement | Wikidata and local Seed Vault governance | Architecture is a computing discipline branch |
| `(form.computer_security, within, form.computing)` | `candidate` | broader-scope placement | Wikipedia inventory seed | Security is a computing branch here |
| `(form.human_computer_interaction, within, form.computing)` | `candidate` | broader-scope placement | Wikidata and local Seed Vault governance | HCI is a computing-adjacent discipline |
| `(form.algorithm, within, form.computer_science)` | `candidate` | broader-scope placement | Wikidata topic structure | Foundational concept placed under computer science |
| `(form.data_structure, within, form.computer_science)` | `candidate` | broader-scope placement | Wikidata topic structure | Foundational concept placed under computer science |
| `(form.computer_programming, within, form.computer_science)` | `candidate` | broader-scope placement | Wikidata topic structure | Programming is operationally placed under computer science |
| `(form.operating_system, within, form.information_technology)` | `candidate` | broader-scope placement | Wikidata topic structure | Operating systems are core to operational IT |
| `(form.computer_network, within, form.information_technology)` | `candidate` | broader-scope placement | Wikidata topic structure | Networks are core to operational IT |
| `(form.database_management_system, within, form.information_technology)` | `candidate` | broader-scope placement | Wikidata topic structure | DBMS is an operational systems concept |
| `(form.distributed_computing, within, form.computer_science)` | `candidate` | broader-scope placement | Wikidata topic structure | Distributed computing is placed provisionally under computer science |
| `(form.computer_networking, within, form.computing)` | `candidate` | broader-scope placement | Wikidata topic structure | Networking is treated as a field within the broader computing domain |
| `(form.information_systems, adjacent_to, form.information_technology)` | `candidate` | related-but-distinct | local Seed Vault governance | Operational overlap without collapse |
| `(form.software_engineering, adjacent_to, form.computer_science)` | `candidate` | related-but-distinct | Wikidata and local Seed Vault governance | Strong overlap with distinct boundary |
| `(form.software_engineering, adjacent_to, form.information_technology)` | `candidate` | related-but-distinct | local Seed Vault governance | Shared operational terrain without identity collapse |
| `(form.computer_network, adjacent_to, form.computer_networking)` | `candidate` | related-but-distinct | Wikidata topic structure | System class versus field of work distinction |
| `(form.database_management_system, adjacent_to, form.information_systems)` | `candidate` | related-but-distinct | local Seed Vault governance | Infrastructure software overlaps with information-system practice without collapse |

## SPARQL Sketch

The following query pattern is sufficient to expand many child concepts under a chosen computing root once the root item is trusted:

```sparql
SELECT ?item ?itemLabel ?article WHERE {
  VALUES ?root { wd:Q21198 wd:Q11661 }
  ?item (wdt:P279|wdt:P361|wdt:P1269) ?root .
  OPTIONAL {
    ?article schema:about ?item ;
             schema:isPartOf <https://en.wikipedia.org/> .
  }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
```

This should be treated as a discovery query, not an automatic truth import. The Seed Vault remains the place where ambiguous returns are normalized.

## OWL And Open Data Notes

- Wikidata entity URIs can act as durable external identifiers for our concept rows.
- Seed Vault local ids remain the internal authority because one Wikidata item may still need local boundary qualification.
- Later, the current tuples could be exported as `RDF`, `OWL`, or `SKOS`-flavored graphs without changing the human-readable ledgers first.

## Governance Notes

- `computing` is treated here as the umbrella the user called `IT`, but the ontology still keeps `information_technology` narrower than `computing`.
- `within` is used provisionally until a more formal relation vocabulary is introduced.
- This ledger is intentionally small and operational: enough structure to classify current computing concepts without pretending the full relation layer is settled.
