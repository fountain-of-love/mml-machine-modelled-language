# Relation Template

Use this template when adding a governed relation record or relation family to a relation ledger.

```md
---
artifact: relation-record
status: candidate
updated: YYYY-MM-DD
relation_family: equivalence|hierarchy|association|contrast|dependency|process|confusion
weight_class: structural|semantic-neighborhood|operational
directionality: directed|undirected|contextual
---

# Relation Name

## Identity

- Canonical label: `relation_name`
- Status: `candidate`
- Relation family: `equivalence|hierarchy|association|contrast|dependency|process|confusion`
- Weight class: `structural|semantic-neighborhood|operational`
- Directionality: `directed|undirected|contextual`

## Human Introduction

Two short paragraphs answering:

- what this relation means in plain language;
- why it matters in the ontology; and
- what kind of distinction it preserves.

## Definition

One short paragraph defining the relation in governed terms.

## Usage Rule

- Subject kinds:
- Object kinds:
- When to use:
- When not to use:

## Tuple Pattern

```text
(subject, predicate, object)
```

Examples:

- `(concept.a, relation_name, concept.b)`
- `(concept.c, relation_name, concept.d)`

## Process Graph Use

Use this section only for process-family relations.

- Stage ownership pattern:
- Ordering pattern:
- Input pattern:
- Output pattern:
- Feedback or revision pattern:

Example:

```text
(process, has_stage, stage.a)
(stage.a, precedes, stage.b)
(input.artifact, input_to, stage.a)
(stage.b, produces, output.artifact)
(review.stage, revised_into, output.artifact)
```

Process relations should make a process traversable as a graph. If the relation only describes a loose topical association, use an association relation instead.

## Linked-Data Hints

- RDF-like reading:
- SKOS-like reading:
- Wikidata-like pattern:
- OWL-like reading:

## Boundary

Included:

- item
- item

Excluded:

- item
- item

## Common Confusions

- confusion
- confusion

## Layer Coverage

- Identity impact:
- Hierarchy impact:
- Association impact:
- Contrast impact:
- Dependency impact:
- Process impact:
- Confusion risk:

## Provenance

- source
- source

## Source Packet

- Governing note:
- Related ledgers:
- External ontology references:
- LLM synthesis inputs:

## Open Questions

- question
- question
```

## Writing Rule

A relation template should preserve distinction before it maximizes coverage. Prefer a relation that is slightly narrow and reliable over a relation that becomes a vague catch-all.

## Governance Rule

When deciding between two possible relations:

1. choose the one that preserves the sharper boundary;
2. prefer explicit local meanings over borrowed public ontology meanings when they conflict;
3. record the public linked-data analogue in `Linked-Data Hints` rather than pretending the mappings are exact.
