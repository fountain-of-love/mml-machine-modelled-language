---
artifact: governance
status: active
updated: 2026-08-28
scope: concept-seed-authoring
---

# Seed Expansion Guide

## Purpose

This guide explains how to give concept seeds more body without turning them into pasted encyclopedia pages.

The target shape is:

```text
human-readable introduction
  + structural definition
  + ontology hooks
  + linked-data references
  + comparative LLM synthesis
```

## What To Expand

A strong seed usually needs five layers.

### 1. Human Introduction

This is the first-reading layer for people.

It should answer:

- what the concept is in plain language;
- why it matters in this repository; and
- what nearby distinctions matter immediately.

Keep it short. Two or three paragraphs is usually enough.

### 2. Structural Definition

This is the ontology layer.

It should state:

- what kind of thing the concept is;
- what makes it distinct from neighbors; and
- what role it plays in the Seed Vault tree.

### 3. Boundary

This is where the concept becomes governed.

Every useful seed needs:

- included cases;
- excluded cases; and
- at least one non-obvious distinction.

### 4. Representation Hints

This is the LLM-navigation layer.

It should include compact hooks such as:

- tuple hints;
- parent and sibling concepts;
- likely relation predicates;
- retrieval phrases; and
- external identifiers.

### 5. Source Packet

This is the provenance layer.

A good source packet can combine:

- Wikidata item id and URI;
- Wikipedia anchor;
- originating inventory seed;
- ledger rows;
- external schema or ontology references;
- LLM synthesis notes.

## How To Use Multiple LLMs

Use multiple model explanations as comparative evidence, not as final truth.

Recommended flow:

```text
concept
  -> ask 2-4 models for a short explanation
  -> compare overlap
  -> extract stable common core
  -> note one or two useful distinctions
  -> record unresolved ambiguity
  -> write one short synthesis in project language
```

Good questions for models:

- What is this concept in plain language?
- What is it not?
- What nearby concepts are most often confused with it?
- If this concept were placed in a knowledge graph, what would its parent and child concepts likely be?

## What Not To Do

- Do not paste one long model answer into the seed.
- Do not copy Wikipedia prose.
- Do not let the source packet replace the human introduction.
- Do not treat public ontology ids as if they settle every local boundary.

## Suggested Seed Upgrade Path For Computing

The next computing seeds to deepen should usually follow this order:

1. `computer_programming`
2. `software_engineering`
3. `computer_security`
4. `information_systems`
5. `computer_architecture`
6. `computer_networking`

Why this order:

- they are central to operational IT work;
- their boundaries are often confused;
- they benefit immediately from tuple and parent-child clarification.

## Minimal Rich Seed Example

```text
Concept: computer_programming
Human Introduction:
  Programming is the practice of turning problem-solving into executable instructions.
Operational View:
  parent -> computer_science
  adjacent -> software_engineering
  child -> programming_language, compiler, debugger
Representation Hints:
  (form.computer_programming, within, form.computer_science)
Source Packet:
  wikidata_id -> Q80006
  wikipedia_anchor -> /Computer_programming
  source_seed -> science-and-technology inventory
LLM Synthesis:
  models agree that programming is implementation-centered; boundary with software engineering remains broader than coding alone.
```

## Decision Rule

When deciding whether to expand breadth or depth:

- add breadth when a branch is missing crucial neighboring concepts;
- add depth when a concept is already central to many relations;
- prefer depth first for concepts that anchor navigation, retrieval, or classification.

For the current repository, computing has reached the point where depth now gives more value than adding many new top-level labels.
