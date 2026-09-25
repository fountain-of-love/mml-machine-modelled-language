---
artifact: governance
status: active
authority: concept-maturity
updated: 2026-08-27
---

# Concept Ledger

## Purpose

This ledger records the current concept identities governed by the `form/concepts` layer. It tracks maturity, boundary confidence, and whether a concept is ready to be referenced by other Seed Vault elements.

The ledger is now split into subledgers so the concept inventory can grow without collapsing into one oversized table.
Its first tree follows the Seed Vault's three-element spine: `form`, `movement`, and `direction`.

## Maturity States

| State | Meaning |
| --- | --- |
| `candidate` | Proposed concept identity with an initial boundary, still open to revision |
| `reviewed` | Boundary and exclusions have been reviewed for local consistency |
| `stable` | Suitable for reuse across Seed Vault elements, subject to later refinement with provenance |
| `deprecated` | Kept for provenance but not preferred for new work |

## First Tree

```text
concept-ledger
  -> form
     -> meta form concepts
     -> core form concepts
     -> science domains
     -> natural sciences
     -> formal and computing
     -> technology and engineering
  -> relation
     -> predicate concepts
  -> movement
     -> core movement concepts
     -> observatory movement concepts
     -> RCL movement concepts
  -> direction
     -> core direction concepts
     -> governance direction concepts
     -> alignment direction concepts
```

## Tree Index

| Branch | Ledger | Current role |
| --- | --- | --- |
| `form` | [Form Meta Concept Ledger](subledgers/Form-Meta-Concept-Ledger.md) | vault self-description and governance concepts |
| `form` | [Form Core Concept Ledger](subledgers/Form-Core-Concept-Ledger.md) | structural Seed Vault concepts |
| `form` | [Form Science Domain Concept Ledger](subledgers/Form-Science-Domain-Concept-Ledger.md) | top-level science and technology domains |
| `form` | [Form Natural Science Concept Ledger](subledgers/Form-Natural-Science-Concept-Ledger.md) | first-pass science expansion |
| `form` | [Form Formal And Computing Concept Ledger](subledgers/Form-Formal-Computing-Concept-Ledger.md) | first-pass formal/computing expansion |
| `form` | [Form Technology And Engineering Concept Ledger](subledgers/Form-Technology-And-Engineering-Concept-Ledger.md) | first-pass technology expansion |
| `form` | [Form Computing Foundations Concept Ledger](subledgers/Form-Computing-Foundations-Concept-Ledger.md) | sourced foundational concepts under computing |
| `form` | [Form Computing Systems Concept Ledger](subledgers/Form-Computing-Systems-Concept-Ledger.md) | sourced systems and infrastructure concepts under computing |
| `relation` | [Relation Predicate Concept Ledger](subledgers/Relation-Predicate-Concept-Ledger.md) | relation predicates expressed as concepts |
| `movement` | [Movement Concept Ledger](subledgers/Movement-Concept-Ledger.md) | movement branch index |
| `movement` | [Movement Core Concept Ledger](subledgers/Movement-Core-Concept-Ledger.md) | foundational movement concepts |
| `movement` | [Movement Observatory Concept Ledger](subledgers/Movement-Observatory-Concept-Ledger.md) | discovery and observation movement concepts |
| `movement` | [Movement RCL Concept Ledger](subledgers/Movement-RCL-Concept-Ledger.md) | RCL-derived movement concepts |
| `direction` | [Direction Concept Ledger](subledgers/Direction-Concept-Ledger.md) | direction branch index |
| `direction` | [Direction Core Concept Ledger](subledgers/Direction-Core-Concept-Ledger.md) | foundational direction concepts |
| `direction` | [Direction Governance Concept Ledger](subledgers/Direction-Governance-Concept-Ledger.md) | governance and stewardship concepts |
| `direction` | [Direction Alignment Concept Ledger](subledgers/Direction-Alignment-Concept-Ledger.md) | coordination and interoperability concepts |

## Summary

| Scope | Concept count | Source |
| --- | --- | --- |
| meta form | 21 | Seed Vault governance and inventory architecture |
| relation predicates | 7 | relation ledger and semantic hub active relation table |
| core form | 5 | Seed Vault structural initialization |
| science domains | 7 | science-and-technology inventory seed |
| natural sciences | 15 | science-and-technology inventory seed |
| formal and computing | 12 | science-and-technology inventory seed |
| technology and engineering | 20 | science-and-technology inventory seed |
| computing foundations | 4 | Wikidata and Wikipedia linked data |
| computing systems | 5 | Wikidata and Wikipedia linked data |
| movement core | 9 | movement README and RCL framing |
| movement observatory | 5 | movement observatory framing |
| movement RCL | 6 | RCL materials |
| direction core | 6 | direction README and SOS framing |
| direction governance | 6 | Seed Vault and SOS governance framing |
| direction alignment | 5 | initiative-alignment and SOS framing |

Current total across admitted concept-ledger rows: `133`

## Governance Notes

- A concept may be important even while its maturity remains low.
- Alias richness does not imply boundary maturity.
- Cross-domain reuse requires explicit exclusions, not just broad wording.
- Model observations may propose new concepts or refinements, but the concept ledger remains the authority for accepted identities in `form`.
- `form`, `movement`, and `direction` are the first classification branches and should remain visible even when one branch is temporarily empty.
- New inventory-driven concepts should enter the ledger through the narrowest relevant subledger first.
- Subledgers may later split again by branch once a scope becomes too large for one review surface.
