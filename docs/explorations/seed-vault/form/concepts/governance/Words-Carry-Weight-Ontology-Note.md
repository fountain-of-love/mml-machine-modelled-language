---
artifact: governance
status: active
updated: 2026-08-28
scope: ontology-direction
---

# Words Carry Weight Ontology Note

## Purpose

This note documents the next ontology direction for the Seed Vault concept layer.

The current repository already contains many concept labels, ledgers, seeds, and early relation tuples. That is necessary, but not sufficient. A concept inventory becomes meaningful only when concepts carry weight through their distinctions, dependencies, associations, exclusions, and paths of reuse.

The working idea is simple:

```text
concept alone
  -> light label

concept in relation fabric
  -> navigable meaning
  -> usable ontology
```

## Core Claim

A concept by itself is rarely enough.

To make the ontology useful for both humans and language models, every important concept should gradually acquire:

- identity;
- boundary;
- synonyms and aliases;
- parent and child relations;
- adjacent and associated concepts;
- contrasts and exclusions;
- dependencies and enabling conditions;
- process relations where relevant; and
- common confusion surfaces.

This is what makes the words carry weight.

## Why This Matters

Human readers usually do not want only a label and a definition. They want orientation:

- what the thing is;
- what it is close to;
- what it is not;
- where it belongs;
- why it matters; and
- how it behaves with neighboring concepts.

Language models need a similar structure for a different reason. They navigate better when concepts are linked through explicit, inspectable cues rather than left as isolated prose fragments.

The ontology therefore needs to support both:

```text
human readability
  + machine navigability
```

## Required Meaning Layers

The next phase of ontology work should treat the following as first-class meaning layers.

### 1. Identity

The concept itself:

- canonical label;
- local id;
- maturity;
- definition;
- provenance.

### 2. Equivalence

Different expressions that point to the same or nearly the same concept:

- synonyms;
- aliases;
- lexical variants;
- acronyms;
- multilingual correspondences.

Equivalence should not collapse distinct senses prematurely.

### 3. Hierarchy

How concepts sit within broader or narrower structures:

- `is_a`;
- `within`;
- `specializes_within`;
- `part_of`;
- child-of and parent-of views.

Hierarchy gives a concept placement and scale.

### 4. Association

Concepts that commonly travel together without being identical:

- `adjacent_to`;
- `associated_with`;
- `used_with`;
- `often_co_occurs_with`.

Association is where neighborhoods begin to appear.

### 5. Contrast

Concepts become clearer through opposition and non-identity:

- `contrasts_with`;
- `not_equivalent_to`;
- `excluded_from`;
- `negative_control_for`;
- `opposite_of` when a true opposite exists.

Contrast is especially important because it preserves boundary and prevents ontological blur.

### 6. Dependency

Some concepts require or enable others:

- `requires`;
- `enables`;
- `depends_on`;
- `presupposes`.

Dependency adds operational depth.

### 7. Process

Some concepts belong inside a transformation or execution path:

- `input_to`;
- `transforms_into`;
- `produces`;
- `tested_by`;
- `revised_into`.

Process relations are especially important in computing and scientific workflows.

### 8. Confusion

Some concepts are frequently mistaken for each other:

- `confused_with`;
- `flattened_into`;
- `overlaps_with`.

This layer is highly valuable for human readers and highly valuable for LLM navigation because many errors originate in boundary drift rather than missing facts.

## Relation Weight

Not all relations carry the same weight.

The ontology should eventually distinguish at least three levels:

1. `structural`
   Example: `is_a`, `part_of`, `within`
2. `semantic-neighborhood`
   Example: `adjacent_to`, `associated_with`, `contrasts_with`
3. `operational`
   Example: `requires`, `uses`, `produces`, `tested_by`

This allows one concept to be richly connected without pretending every connection has the same force.

## Relation Concepts

Some relations should themselves become governed concepts.

Early candidates:

- `alias_of`
- `is_a`
- `within`
- `part_of`
- `uses`
- `requires`
- `enables`
- `adjacent_to`
- `contrasts_with`
- `confused_with`

This matters because the Seed Vault should be able to speak not only about concepts, but about the meaning of its own relation vocabulary.

## Example: Computer Programming

`computer_programming` becomes more useful when it carries several kinds of weight:

```text
computer_programming
  -> within -> computer_science
  -> within -> computing
  -> uses -> algorithm
  -> uses -> data_structure
  -> adjacent_to -> software_engineering
  -> confused_with -> software_engineering
  -> requires -> programming_language
  -> produces -> source_code
  -> tested_by -> debugging
```

The definition alone is helpful. The relation fabric is what makes it navigable.

## Authoring Rule

When a seed feels too light, do not expand only by adding more descriptive prose.

Expand in at least one of these ways:

- add a sharper exclusion;
- add an adjacent concept;
- add a dependency;
- add a contrast;
- add a common confusion note;
- add tuple hints;
- add parent or child placement.

The goal is not encyclopedic accumulation. The goal is semantic density with readable form.

## Practical Consequence

The next ontology work should not focus only on adding more concept names.

It should also introduce:

- a relation vocabulary;
- a relation template;
- one or more relation ledgers;
- confusion and contrast patterns for key concepts; and
- richer seed sections that expose concept neighborhoods explicitly.

## Decision Rule

If a concept is central to navigation, retrieval, or classification, deepen its relation fabric before adding many new sibling concepts.

If a branch is missing major neighbors, add breadth first.

For the current repository, the computing branch has reached the point where relation depth now adds more value than adding many more top-level labels.
