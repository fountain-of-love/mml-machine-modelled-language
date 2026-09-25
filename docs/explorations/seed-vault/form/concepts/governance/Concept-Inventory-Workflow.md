---
artifact: workflow
status: active
authority: concept-promotion
updated: 2026-08-28
---

# Concept Inventory Workflow

## Purpose

This workflow defines how candidate concepts move from observation and discovery into the governed `form/concepts` layer.

The core separation is:

```text
movement/observatory
  -> proposes candidates
  -> records raw evidence

form/concepts
  -> governs identity
  -> defines boundaries
  -> accepts or rejects promotion
```

## Pipeline

```text
source material
  -> candidate harvesting
  -> backlog capture
  -> triage
  -> draft seed
  -> boundary review
  -> ledger update
  -> stable concept seed
```

## Candidate Sources

Candidates may come from:

- Seed Vault papers and governance notes;
- SOS and MML architectural documents;
- public corpora and domain inventories;
- open model prompting;
- embedding neighborhoods and clustering;
- relation-probe outputs that imply missing concept nodes; and
- human review and manual synthesis.

## Stage 1: Candidate Harvesting

Candidate harvesting is intentionally generous. Its job is to notice possible concepts, not to settle them.

Typical harvesting operations:

- ask a model for nearby concepts around an existing seed;
- extract frequent domain nouns or noun phrases from curated text;
- inspect embedding neighbors of a concept label;
- compare alias lists across languages or documents; and
- note where one concept seed is doing too much conceptual work.

Output:

- candidate label
- source
- raw evidence
- first rationale

## Stage 2: Backlog Capture

Every harvested item goes into the [Concept Backlog](Concept-Backlog.md) before it becomes a seed candidate.

This preserves:

- provenance;
- candidate status;
- uncertainty;
- duplication pressure; and
- decision history.

## Stage 3: Triage

Each backlog item should be checked against the current concept layer.

Ask:

1. Is this already an existing concept seed?
2. Is this only an alias?
3. Is this a sibling concept that deserves distinction?
4. Is this really a relation predicate instead of a concept?
5. Is this out of scope for the current vault?

Possible results:

- merge with an existing concept;
- draft a new concept seed;
- move to a relation ledger;
- block pending evidence; or
- reject.

## Stage 4: Draft Seed

When triage suggests `new-concept`, `sibling-of-existing`, or `split-existing`, create a concept seed draft from the [Concept Template](Concept-Template.md).

A draft should define:

- canonical label;
- local id;
- definition;
- included content;
- excluded content;
- aliases;
- provenance; and
- open questions.

## Stage 5: Boundary Review

Boundary review is the key governance gate.

The review asks:

- does the concept have a stable identity?
- are the exclusions clear enough?
- is it distinct from its nearest neighbors?
- is it broad enough to be reusable but narrow enough to be meaningful?
- does it preserve cross-domain usefulness without becoming vague?

If not, return the draft to backlog or split it into smaller candidates.

## Stage 6: Promotion

Once a concept is locally coherent:

1. add or update the concept seed file;
2. update the relevant subledger;
3. update the main [Concept Ledger](Concept-Ledger.md);
4. link the seed from [form/concepts/README.md](../README.md); and
5. mark the backlog item as `promoted`.

## Using Open Models

Open models should be used as candidate generators and refinement tools, not as concept authorities.

Useful model tasks:

- propose neighboring concepts;
- propose aliases;
- suggest likely confusions;
- suggest boundary distinctions;
- summarize a cluster theme;
- propose candidate sibling concepts; and
- generate contrast sets for review.

Unsafe shortcut:

- accepting a concept because one model named it confidently

## Using Embeddings

Embeddings are especially useful at the backlog and triage stages.

Use them for:

- nearest-neighbor discovery around an existing concept label;
- duplicate detection across candidate labels;
- cluster discovery from curated domain terms;
- identifying alias candidates across wording variants; and
- spotting broad concepts that may hide several siblings.

Embeddings do not define the boundary of a concept by themselves. They provide neighborhood evidence, not final semantic governance.

## Practical Observatory Bridge

The current observatory can feed this workflow with a simple record shape:

```yaml
candidate_label: semantic field
source_type: open-model-probe
model: Qwen/Qwen3-8B
prompt: "List concepts related to semantic representation."
raw_output_ref: movement/observatory/...
embedding_neighbors:
  - semantic neighborhood
  - concept cluster
status: captured
suspected_action: new-concept
```

That record belongs first in the backlog. Only after review should it become a concept seed.

## Right-Sizing Rule

Prefer the smallest useful governed distinction.

Do not create a new concept when:

- an alias is enough;
- a subledger note is enough;
- a relation predicate is the real missing structure; or
- the concept has no clear boundary yet.
