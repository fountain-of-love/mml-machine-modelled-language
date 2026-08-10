# Public Commons Governance

MML asks whether public knowledge can become executable without becoming opaque or captured. Governance is therefore part of the data model and execution contract, not an administrative layer added later.

This repository is currently a pre-publication proposal and mechanism experiment, not an official project or an open call for governance participation. The workflows below state architectural intentions for a first public version.

Whether Europe can organise the institutional cooperation needed for executable public knowledge is a societal question, not a claim established here. The proposed technical next step is smaller: execute one URI-addressed Linked Open Data slice while preserving its public identity, provenance, applicable terms, reproducible snapshot, and correction history. See [Research-Contract.md](../Research-Contract.md#proposed-next-step-one-linked-open-data-slice).

## Reuse Before Reinvention

MML should reuse existing public identifiers, vocabularies, and authoritative sources whenever their terms allow it. Candidate foundations include Wikidata, Wikipedia, EuroVoc, CELLAR and EUR-Lex, SEMIC vocabularies, lexical resources, and domain-specific public ontologies. MML contributes adapters, governed weighting, execution, and inspection; it should not replace source communities or claim ownership of their knowledge.

## Identity And Provenance

Every durable node should carry a stable identifier, type, labels and aliases, language, source, applicable license, validity period, confidence, review state, and version history.

Every durable edge should record its relation type, endpoints, source evidence, jurisdiction or domain, validity period, confidence, maturity, creation method, reviewer state, and version history. A corpus-derived weight additionally records the corpus snapshot, algorithm, parameters, observation count, previous value, new value, and computation time.

An execution result should trace query inputs to resolved identifiers, activated layers, traversed relationships, contributing weights, sources, and the final distribution. Path validity, source provenance, and causal score decomposition are different guarantees: a traversed path is not source lineage unless its edges resolve to evidence, and neither proves that displayed contributions completely account for the score. A result must say which guarantees it provides.

## Disagreement Without Erasure

A public semantic graph must support competing assertions, temporal changes, jurisdictional differences, source-specific viewpoints, uncertainty, minority positions, and unresolved disputes. Community or application overlays can select an execution context without deleting alternative claims from the shared record.

## Participation Workflow

Participation becomes operational only when a first public version, contribution contract, and maintainer process exist. The intended workflow is:

```text
proposal
  -> automated schema, provenance, and license validation
  -> community review
  -> provisional graph layer
  -> evaluation and challenge period
  -> acceptance, revision, or rejection
  -> versioned publication
```

Participants must be able to propose sources, map identifiers, challenge relations, inspect weight changes, reproduce snapshots, submit corrections, maintain domain overlays, export their contributions, and fork the complete infrastructure.

## Git As Knowledge-Base Infrastructure

Git is an architectural requirement for the human-readable knowledge base, not merely a development convenience. It already provides content-addressed history, atomic commits, diffs, branches, attribution, reviewable merges, tags, forks, and rollback. Hosting layers can add pull requests, protected branches, signed contributions, issue discussion, and automated validation without inventing a proprietary governance database.

Before publication, deterministic content hashes identify construction inputs, relation artifacts, configuration, vocabulary, and algorithm version without pretending that an unpublished Git revision provides governance. The first public commit should establish the initial governed snapshot. Later knowledge changes should be reviewable as ordinary diffs and reproducible by commit or tag. Generated matrices and indexes must record both their content snapshot and the exact source commit from which they were constructed.

Git does not replace semantic validation or community judgment. It supplies the proven versioning and audit substrate on which those policies can operate.

## Source-License Interoperability

Executable license compatibility is an intended ingestion requirement, not a facility implemented by the current prototype. A future adapter must preserve source-specific terms and provenance, validate whether sources may be combined for the intended output, and keep repository code, documentation, imported data, derived weights, and exports distinguishable. The governing terms for this repository remain in [LICENSE.md](../../LICENSE.md).

Rather than invent a new sovereign-data pipeline, the preferred direction is to align with and, where collaboration becomes possible, hook into work such as Apertus for data documentation, reproducibility, privacy handling, multilingual scope, and public auditability. MML's distinct contribution would be executable public-graph representation and inspection, not duplication of Apertus infrastructure. This is an opportunity for alignment, not a claim of partnership or endorsement.

## Operational Guarantees

- Versioned snapshots allow deterministic replay.
- Changes are localized, reviewable, and reversible.
- Deprecation preserves history rather than silently deleting it.
- APIs expose identifiers, weights, evidence, and provenance—not only final rankings.
- Export formats avoid platform lock-in and preserve source attribution.
- Governance roles follow least privilege and leave an auditable history.

## Executable Update Evidence

A localized knowledge update should be expressed as a reviewable source change, never as an unexplained in-place matrix edit. The executable check should:

```text
rebuild baseline -> record content identity and outputs
apply one declared relation change -> record scope and deltas
rebuild baseline sources -> reproduce original outputs exactly
```

The change record names its intended concepts, query families, jurisdiction, evidence, and permitted scope. Downstream movement is allowed when it is bounded and explainable; “localized” does not mean that precisely one score changes. Unrelated-tier isolation, explanation differences, and exact rollback must be reported.

The current evolution demo proves that one explicit relation change produces a new content snapshot, observable consequences, and exact restoration. It reports consequence breadth without treating an experimental percentage threshold as governance truth. The revision remains dirty and pre-publication: content-addressed replay and reversibility do not by themselves demonstrate community legitimacy, review quality, or a functioning public governance process.

## Current Boundary

The current development work begins to exercise typed relation records, content snapshots, path-level explanations, localized reconstruction, and rollback checks. These are infrastructure mechanics, not evidence that the full governance model exists. The Seed Vault begins to express provenance and maturity in readable documents; a future public-graph pilot must still turn those expectations into public schemas, validation, APIs, contribution roles, review states, signed history, and durable participation.

Use, modification, and redistribution are governed by [LICENSE.md](../../LICENSE.md). That document is authoritative and is not duplicated here.
