# Dual Persistence: Knowledge Base And MML Index

This document focuses on the persistence side of the **Semantic Operating System (SOS)**: how knowledge is stored for humans, how it is indexed for **Machine Modelled Language (MML)**, and why those two forms should remain separate but connected. For the broader architecture, see [What.md](../What.md). For the dual LLM/MML engine, see [Dual-Engine.md](Dual-Engine.md).

## The Core Idea

SOS needs two complementary persistence forms:

- **Human-readable knowledge:** notes, pages, records, explanations, provenance, contradictions, and links that people can inspect.
- **MML matrix/index:** weighted transitions, contextual paths, clusters, and pointers that machines can traverse quickly.

The knowledge base is the durable source of meaning. The matrix is the fast navigational layer over it.

That separation matters. If the matrix becomes the only store of knowledge, the system becomes opaque again. If the knowledge base has no matrix/index, it remains human-readable but slow to query at scale. Dual persistence keeps both properties alive: inspectability and speed.

## The Knowledge Base As A Semantic Seed Vault

The analogy is the [Svalbard Global Seed Vault](https://www.seedvault.no/): a preservation model built around durable, long-term stewardship.

SOS proposes a similar idea for knowledge. The knowledge base is a semantic seed vault: a durable, human-readable store of concepts, evidence, relationships, contradictions, and patterns that humanity should not have to rediscover from scratch every time. The fuller initiative alignment is described in [Initiative-Alignment.md](Initiative-Alignment.md#svalbard-global-seed-vault-preservation-analogy).

This is also a sustainability claim. If useful patterns are already known, verified, and preserved, they should not need to be recomputed endlessly through dense stochastic inference. They should be stored in a form that can be read, reviewed, corrected, linked, and reused.

## Human-Readable Knowledge

The knowledge base should remain human-readable. Think of it as an improved Wikipedia shaped by knowledge engineering: notes as nodes, links as typed relationships, and pages that preserve both explanation and machine-readable structure.

A note can describe:

- a concept;
- a legal issue;
- a factual claim;
- a contradiction;
- an ontology class;
- a synonym set;
- a pattern;
- an evidence cluster;
- a source document;
- a provenance trail.

The links between notes encode semantics, ontology, topology, synonymy, contradiction, provenance, dependency, chronology, authority, and uncertainty.

In a legal context, for example, the knowledge base should not only store a document. It should also store what that document proves, which party controls it, which right it supports, which timeline event it belongs to, which contradiction it creates, and which missing records it points toward.

## Schema-Based Knowledge

The structure should be schema-based and compatible with existing open knowledge standards:

- [Schema.org](https://schema.org/) style vocabularies;
- Linked Open Data;
- RDF triples;
- OWL ontologies;
- RDF/Turtle serializations;
- controlled vocabularies;
- domain-specific taxonomies.

Schema.org is a useful reference because it provides shared schemas for structured data across entities, relationships, and actions, and its data model is derived from RDF Schema.

SOS should stand on that tradition rather than inventing an isolated private format. The goal is not another proprietary memory blob. The goal is a human-readable, machine-queryable knowledge base whose structure can interoperate with public semantic web traditions and domain-specific governance models.

## The MML Matrix / Index

The matrix is not the whole knowledge base. It is the MML-optimized index over that knowledge base.

The human-readable side should be Git-native. Knowledge records, schemas, evidence notes, and governance decisions gain content-addressed history, attribution, diffs, branches, review, tags, forks, and rollback through proven infrastructure. Every generated matrix or index should record the source commit or tag that produced it.

It is similar to an indexed RAG mechanism, but with a stronger semantic contract. Instead of merely retrieving nearby chunks, the matrix stores weighted transitions, contextual paths, clusters, and pointers into the knowledge base.

It tells the system:

- where contextual weight flows;
- which concepts are nearby;
- which senses of an ambiguous word are active;
- which evidence clusters matter;
- which records should be inspected;
- which contradictions are structurally relevant;
- which relations have been validated;
- which paths explain the returned result.

In the current Python prototype, this index appears as a word co-occurrence matrix. In a fuller SOS architecture, it would point into **Common Language Model (CML)-shaped knowledge**: concepts, facts, documents, evidence, definitions, rights, duties, events, and abstractions. The CML role is introduced in [What.md](../What.md#common-language-model).

## Identity, Provenance, And Replay

Durable nodes and edges need stable identifiers, source lineage, applicable terms, validity periods, confidence, maturity, review state, and version history. Corpus-derived weights additionally need the corpus snapshot, update method, parameters, observation count, previous value, and new value.

Every published index should name the exact knowledge snapshot from which it was built. Before public history exists, that identity is a deterministic content hash over construction inputs, governed relations, graph parameters, vocabulary version, and algorithm version. Once published, it should additionally name the governing Git commit or tag. Content identity and governance identity complement one another; neither should be fabricated from unavailable history.

That linkage makes execution reproducible, localized updates inspectable, and rollback possible without erasing history. Competing assertions can coexist in source-specific or community overlays rather than being collapsed into one unqualified truth. The fuller governance contract lives in [Commons-Governance.md](Commons-Governance.md).

## Immutable Update And Restoration

Generated indexes should be rebuilt from versioned sources rather than edited invisibly in place. A controlled update records:

- the before and after content snapshots;
- the exact relation or source change;
- its intended concepts and query scope;
- affected rankings and explanations;
- protected unrelated outputs;
- exact reconstruction of the original snapshot after restoration.

This is a small Memento-like contract at the artifact level: sources are the durable state, generated indexes are reproducible views, and rollback means rebuilding the previous sources to identical outputs. Git later supplies the human-facing diffs, attribution, review, and tags around that technical contract.

## Explanation Is Not Persistence

An execution path references the index structure used for a result. Provenance links those edges back to durable source records. A causal decomposition accounts for the numerical score. Dual persistence must support all three without confusing them: a visually plausible path is not sufficient evidence that an edge was governed, and an evidence link does not prove the path contributed the displayed amount.

## Why MML Can Return Known Patterns Quickly

The analogy is the PageRank algorithm.

Once the graph of pages and links exists, PageRank does not rediscover the web from scratch for every query. It propagates weight through a known link structure. That is why it can return useful importance signals from an already-built graph.

MML uses the same kind of mechanism for language and knowledge. If a relation is already discovered, validated, and encoded in the matrix/index layer, the engine can retrieve and propagate through it deterministically. It does not need to repeatedly ask a dense model to rediscover the same route by next-token trial-and-error.

This is the practical bridge between combinatorial discovery and sustainable AI. Discovery finds useful intersections and patterns. Dual persistence preserves them as human-readable structure plus machine-traversable weight. MML can then reuse those known patterns quickly.

## Matrix As Discovery Surface

The matrix component is useful beyond direct answering.

It can work with classic machine learning to find:

- clusters;
- contradictions;
- outliers;
- dense semantic regions;
- weakly connected concepts;
- bridge terms between domains;
- drift between old and new evidence;
- missing links in a knowledge model.

It can also support visual discovery:

- heat maps;
- transition diagrams;
- evidence clusters;
- contradiction maps;
- topology views;
- timeline overlays;
- layer comparisons.

This matters because the matrix is inspectable. It can show where the system believes weight flows, which relations dominate, and which edges are weak or surprising. That gives humans a way to audit and improve the model instead of merely prompting a black box again.

## LLM Discovery, MML Preservation

The LLM can feed the knowledge base by discovery. It can read large volumes of raw material, spot candidate patterns, propose relationships, extract entities, summarise documents, identify contradictions, and suggest abstractions.

MML can then preserve and query the resulting structure. Once a pattern has been validated and encoded, it becomes part of the durable knowledge layer and the fast matrix/index layer.

The two should cooperate, but they should not be confused.

In this sense, LLMs become less like the final storage location of meaning and more like discovery instruments. They help extract patterns from raw material. MML preserves those patterns in a form that is inspectable, queryable, and reusable.

## How The Prototype Reflects This

The current scripts show dual persistence in miniature:

- `mml_elaborate_corpus.py` contains the small knowledge source: the corpus that expresses distinctions, relationships, contrasts, and escalation patterns.
- The generated vocabulary, co-occurrence matrix, and transition matrix act as the MML index.
- `mml_legal_usecase.py` queries the corpus-derived matrix and uses activation weights to rank authored evidence snippets.

This remains a small in-memory prototype. It now includes explicit bank-sense concepts, governed GDPR aliases and relations, content snapshots, observable update consequences, and exact restoration. Its current revision is dirty and pre-publication, so the snapshot proves content replay rather than public Git governance. The architectural shape is nevertheless testable: readable sources on one side, a reproducible weighted index on the other, and explicit identities connecting them.
