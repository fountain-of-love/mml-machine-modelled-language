# Form Concepts

This package defines the concepts layer for the `form` element of the Seed Vault.

Its purpose is narrow and structural:

```text
concept
  -> stable identity
  -> explicit boundary
  -> aliases
  -> provenance
  -> maturity
```

The concepts layer stabilizes what a concept is before the vault describes how concepts move, relate, activate, or transform.

## Scope

This package records:

- canonical concept identity;
- meaning boundary;
- included and excluded content;
- aliases and naming variants;
- provenance and review notes; and
- maturity state.

This package does not yet attempt to accept and govern:

- rich relation networks;
- causal chains;
- dynamic flows;
- discovery prompts;
- embedding neighborhoods; or
- model-observation traces.

Those belong primarily under `movement`. The inventory architecture note may still describe the slots that future relation and observation layers will need.

## Current Authorities

- [Concept Ledger](governance/Concept-Ledger.md)
- [Concept Backlog](governance/Concept-Backlog.md)
- [Concept Template](governance/Concept-Template.md)
- [Concept Inventory Workflow](governance/Concept-Inventory-Workflow.md)
- [Seed Tree](governance/Seed-Tree.md)
- [Relation Template](governance/Relation-Template.md)
- [Relation Ledger](governance/Relation-Ledger.md)
- [Seed Expansion Guide](governance/Seed-Expansion-Guide.md)
- [Words Carry Weight Ontology Note](governance/Words-Carry-Weight-Ontology-Note.md)
- [Concept Inventory Architecture](Concept-Inventory-Architecture.md)
- [Concept Subledgers](governance/subledgers/)
- [Concept Candidates Folder](candidates/README.md)
- [Concept Seeds Folder](seeds/README.md)

The current ledger index begins with the first Seed Vault tree: `form`, `movement`, and `direction`.
It now also includes a `meta form` subledger so the vault's own organizing units are governed as concepts.
`movement` and `direction` now also have internal subledgers derived from existing Seed Vault and SOS context.

## Current Inventories

- [Science And Technology Wikipedia Inventory Seed](inventories/Science-and-Technology-Wikipedia-Inventory-Seed.md)

## Current Seed Concepts

Root orientation:

- [Concept](seeds/root-orientation/concept.md)
- [Semantic Hub](seeds/root-orientation/semantic_hub.md)
- [Semantic Neighborhood](seeds/root-orientation/semantic_neighborhood.md)

Form primitives:

- [Capacity](seeds/form-primitives/capacity.md)
- [Boundary](seeds/form-primitives/boundary.md)
- [Substrate](seeds/form-primitives/substrate.md)
- [Activation](seeds/form-primitives/activation.md)
- [Direction](seeds/form-primitives/direction.md)

Vault governance:

- [Ledger](seeds/vault-governance/ledger.md)
- [Inventory](seeds/vault-governance/inventory.md)
- [Seed](seeds/vault-governance/seed.md)
- [Discipline](seeds/vault-governance/discipline.md)
- [Relation](seeds/vault-governance/relation.md)
- [Relation Tuple](seeds/vault-governance/relation_tuple.md)
- [Source Structure](seeds/vault-governance/source_structure.md)
- [Open Question](seeds/vault-governance/open_question.md)
- [Index](seeds/vault-governance/index.md)

Navigation grammar:

- [Follow-Up Link](seeds/navigation-grammar/follow_up_link.md)
- [Link Quality](seeds/navigation-grammar/link_quality.md)
- [Concept Trail](seeds/navigation-grammar/concept_trail.md)
- [Discovery Path](seeds/navigation-grammar/discovery_path.md)

Process grammar:

- [Process Shape](seeds/process-grammar/process_shape.md)

Computing domain:

- [Computing](seeds/computing-domain/computing.md)
- [Computer Science](seeds/computing-domain/computer_science.md)
- [Information Technology](seeds/computing-domain/information_technology.md)
- [Algorithm](seeds/computing-domain/algorithm.md)
- [Data Structure](seeds/computing-domain/data_structure.md)
- [Computer Programming](seeds/computing-domain/computer_programming.md)
- [Operating System](seeds/computing-domain/operating_system.md)
- [Computer Network](seeds/computing-domain/computer_network.md)
- [Database Management System](seeds/computing-domain/database_management_system.md)
- [Distributed Computing](seeds/computing-domain/distributed_computing.md)

## Current Relation Ledgers

- [Relation Ledger](governance/Relation-Ledger.md)
- [Form Computing Relation Ledger](governance/Form-Computing-Relation-Ledger.md)
- [Relation Predicate Concept Ledger](governance/subledgers/Relation-Predicate-Concept-Ledger.md)

## Current Relation Predicate Concepts

- [is_a](seeds/relation-predicates/is_a.md)
- [within](seeds/relation-predicates/within.md)
- [associated_with](seeds/relation-predicates/associated_with.md)
- [uses](seeds/relation-predicates/uses.md)
- [requires](seeds/relation-predicates/requires.md)
- [confused_with](seeds/relation-predicates/confused_with.md)
- [enables](seeds/relation-predicates/enables.md)

## Linked-Data-Oriented Computing Ledgers

- [Form Computing Foundations Concept Ledger](governance/subledgers/Form-Computing-Foundations-Concept-Ledger.md)
- [Form Computing Systems Concept Ledger](governance/subledgers/Form-Computing-Systems-Concept-Ledger.md)

## Use Rule

When a new concept is proposed:

1. define its canonical identity;
2. define its meaning boundary;
3. record what it excludes;
4. record aliases without collapsing distinct meanings prematurely; and
5. assign an explicit maturity state.

The dominant pattern here is one source of truth per concept identity. Relations may later point to these concepts, but they should not replace their structural definition.
