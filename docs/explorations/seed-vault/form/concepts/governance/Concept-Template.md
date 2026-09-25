# Concept Template

Use this template when adding a new concept seed to `form/concepts/seeds/`.

```md
---
artifact: concept-seed
status: candidate
updated: YYYY-MM-DD
wikidata_id: Q...
concept_uri: https://www.wikidata.org/entity/Q...
wikipedia_anchor: https://en.wikipedia.org/wiki/...
---

# Concept Name

## Identity

- Canonical label: `concept-name`
- Local id: `form.concept_name`
- Status: `candidate`

## Human Introduction

Two or three short paragraphs answering:

- what this concept is;
- why it matters; and
- how a human should orient to it quickly.

This section should be readable on its own and should be synthesized in project language rather than copied from one source.

## Definition

One short paragraph defining the concept in structural terms.

## Operational View

- Parent branch: `form|movement|direction`
- Immediate parent concepts:
- Typical child concepts:
- Adjacent concepts:
- Typical relations:

## LLM Synthesis

Short synthesis from multiple model explanations.

Suggested structure:

- shared explanation across models
- useful distinctions one model surfaced better than others
- unresolved ambiguity that still needs human governance

Keep this section short and comparative. Do not paste raw model answers.

## Boundary

Included:

- item
- item

Excluded:

- item
- item

## Aliases

- alias
- alias

## Representation Hints

- Tuple hints:
  - `(local.subject, predicate, local.object)`
- Linked-data hints:
  - `rdf:type`
  - `skos:broader`
  - `skos:related`
- Retrieval phrases:
  - phrase
  - phrase

## Provenance

- source
- source

## Source Packet

- Wikidata item:
- Wikipedia anchor:
- Inventory seed:
- Ledger rows:
- External ontology or schema references:
- LLM synthesis inputs:

## Open Questions

- question
- question
```

## Writing Rule

Prefer stable structure over rhetorical flourish. A concept seed should clarify identity and boundary before it tries to be exhaustive.

## Expansion Rule

When a seed feels too light, expand in this order:

1. improve the `Human Introduction`;
2. sharpen the `Boundary`;
3. add `Operational View` and `Representation Hints`;
4. add `Source Packet` fields; and
5. add only short `LLM Synthesis` notes instead of long pasted summaries.

The goal is human-readable depth plus machine-navigable structure, not encyclopedic bulk.
