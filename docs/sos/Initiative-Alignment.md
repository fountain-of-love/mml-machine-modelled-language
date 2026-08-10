# Initiative Alignment

This page maps adjacent initiatives that could contribute to the SOS direction. It does not claim that these initiatives already implement Machine Modelled Language. It shows how existing European, Swiss, and authoritative knowledge infrastructures could align with the architecture proposed in this repository.

For the architecture itself, see [What.md](../What.md). For the dual LLM/MML engine, see [Dual-Engine.md](Dual-Engine.md). For MML mechanics, see [MML-In-Depth.md](../MML-In-Depth.md). For persistence, see [Dual-Persistence.md](Dual-Persistence.md).

## Why This Page Exists

SOS is not imagined as something built from nowhere.

Several existing initiatives already express parts of the same shape:

- readable public knowledge bases;
- structured entity graphs;
- semantic interoperability standards;
- controlled vocabularies;
- authoritative legal repositories;
- small, inspectable neural models for controlled discovery;
- sovereign, open AI pipelines with serious governance standards;
- long-term preservation systems designed around resilience and shared stewardship.

The opportunity is to connect these existing strengths through adapters and shared contracts: a Common Language Model, a durable knowledge base, an MML matrix/index, and a dual engine where LLMs and MMLs cooperate. Existing public identifiers, schemas, source communities, and license obligations should be reused rather than replaced.

## Contribution Map

| Initiative | Contribution |
| --- | --- |
| Wikipedia | Readable seed vault |
| Wikidata | Structured seed vault |
| SEMIC | Semantic interoperability / CML discipline |
| EuroVoc | Controlled EU vocabulary |
| Cellar + EUR-Lex | Authoritative EU legal substrate |
| Apertus | Sovereign AI pipeline |
| Oleg Lavrovsky / Datalets | Swiss open-data craft and civic knowledge tooling |
| minGPT | Small inspectable LLM workbench |

This gives SOS a more practical shape:

```text
Wikipedia      -> readable seed vault
Wikidata       -> structured seed vault
SEMIC          -> semantic interoperability / CML discipline
EuroVoc        -> controlled EU vocabulary
Cellar/EUR-Lex -> authoritative EU legal substrate
Apertus        -> sovereign AI pipeline
Oleg/Datalets  -> Swiss open-data craft and civic knowledge tooling
minGPT         -> small inspectable LLM workbench
```

The emphasis is deliberate: prefer public, inspectable, European or Swiss-aligned initiatives where possible, and use broader global infrastructure only when it is clearly authoritative or already foundational.

## Wikipedia: Readable Seed Vault

[Wikipedia](https://www.wikipedia.org/) is the most natural readable seed-vault candidate.

It contains human-readable explanations, summaries, references, categories, multilingual articles, and editorial histories. It is not perfect, and it is not an authority in the same way as legislation, court records, or scientific primary sources. But as a public knowledge commons, it is difficult to ignore.

For SOS, Wikipedia fits the human-readable side of dual persistence:

- concepts explained in natural language;
- links between related topics;
- multilingual coverage;
- page histories and editorial discussion;
- readable context around entities and events.

Wikipedia should not be treated as the final truth layer. It is better understood as a readable semantic seed vault: a place where human-maintained knowledge can be inspected, linked, corrected, and connected to more authoritative sources.

## Wikidata: Structured Seed Vault

[Wikidata](https://www.wikidata.org/) is the structured counterpart to Wikipedia.

Where Wikipedia gives readable articles, Wikidata gives entities, identifiers, claims, properties, qualifiers, references, multilingual labels, and links to other datasets. That makes it much closer to the Common Language Model side of SOS than plain article text.

For SOS, Wikidata could contribute:

- stable entity identifiers;
- multilingual labels and aliases;
- structured claims;
- links to external authority files;
- references and qualifiers;
- a graph substrate for CML mapping.

If Wikipedia is the readable note layer, Wikidata is the structured node layer.

## SEMIC: Semantic Interoperability / CML Discipline

[SEMIC](https://interoperable-europe.ec.europa.eu/collection/semic-support-centre) is perhaps the closest existing European institutional fit for the Common Language Model idea.

SEMIC, through the Interoperable Europe ecosystem, focuses on semantic interoperability: helping public administrations exchange data in ways that preserve meaning across borders, sectors, systems, and institutions. This is very close to the discipline SOS needs for CML.

For SOS, SEMIC could contribute:

- application profiles;
- semantic specifications;
- shared data models;
- controlled vocabularies;
- interoperability governance;
- cross-border public-sector alignment.

This is not “AI” in the hype sense. That is exactly why it matters. It is the quieter infrastructure of meaning: schemas, agreements, definitions, and mappings. MML needs that discipline if it wants to query known structure reliably.

## EuroVoc: Controlled EU Vocabulary

[EuroVoc](https://op.europa.eu/en/web/eu-vocabularies/eurovoc) is a multilingual, multidisciplinary EU thesaurus managed by the Publications Office of the European Union.

It covers the activities of the European Union across the EU's official languages and is already part of the EU vocabulary ecosystem. That makes it a strong controlled-vocabulary layer for a European CML.

For SOS, EuroVoc could contribute:

- multilingual labels;
- concept hierarchies;
- controlled subject terms;
- legal and policy vocabulary;
- alignment across EU institutions;
- a bridge between human terms and machine-readable categories.

EuroVoc is especially useful for legal, governance, policy, and public administration use cases, where loose terminology quickly creates drift.

## Cellar And EUR-Lex: Authoritative EU Legal Substrate

[Cellar](https://op.europa.eu/en/web/cellar/home) is the common data repository of the Publications Office of the European Union. It stores and disseminates EU publications and metadata for humans and machines, including Linked Open Data and SPARQL access.

[EUR-Lex](https://eur-lex.europa.eu/) is the official access point to EU law and related documents.

Together, Cellar and EUR-Lex form a strong authoritative legal substrate for SOS:

- EU law;
- Official Journal material;
- EU case law and legal documents;
- multilingual publications;
- metadata;
- linked data;
- machine-readable access.

For legal MML, this matters enormously. A legal model should not rely only on generic web text or stochastic memory. It should be able to ground legal concepts, obligations, rights, and procedures in authoritative public sources.

In the current GDPR right-of-access demo, this would be the natural next layer: connect the legal vocabulary and evidence patterns to authoritative EU legal sources rather than only to the toy corpus.

## Proposed Linked Open Data Vertical Slice

The next implementation step should be deliberately narrow. It should not attempt to prove that a European semantic commons already exists or can be organised by one project.

Use one GDPR concept and follow one URI-addressed chain:

```text
public HTTP URI
  -> RDF or SPARQL retrieval
  -> preserved triples and source metadata
  -> minimal MML adapter
  -> content-addressed executable snapshot
  -> one query and provenance trace
  -> one Git-recorded qualification or correction
  -> regenerated snapshot and exact restoration
```

CELLAR/EUR-Lex and EuroVoc are the natural first candidates because they already expose authoritative EU material, controlled vocabulary, multilingual metadata, and Linked Open Data access. Wikidata may provide useful cross-domain alignment, but it should not replace the authoritative legal URI.

The purpose is technical feasibility: demonstrate that MML can operate over public identifiers without erasing their original identity or provenance. European coordination, long-term maintenance, participation, and institutional legitimacy remain societal questions outside the proof boundary of this repository.

## Apertus: Sovereign AI Pipeline

[Apertus](https://apertvs.ai/) is useful as a sovereign AI reference.

It is developed by the Swiss AI Initiative as a collaboration between EPFL, ETH Zurich, and CSCS. Its public positioning is a fully open foundation model for sovereign AI, with open weights, open data, open science, documented methods, reproducibility, opt-out respect, PII removal, memorization prevention, multilingual scope, and readiness for European regulatory expectations.

That pipeline matters. MML should avoid reinventing it and would need the same kind of discipline:

- transparent training and data practices;
- responsible handling of personal data;
- governance over bias and drift;
- reproducibility;
- documented alignment principles;
- multilingual and European legal sensitivity;
- public auditability.

The difference is the engine.

Apertus is still an LLM-centered foundation model. SOS proposes that the center could become dual: LLMs for discovery and language, MML for deterministic traversal of known structure. A future Apertus-like pipeline could keep the sovereign quality discipline while replacing part of dense parametric memory with inspectable sparse graph computation.

That makes Apertus feel close in institutional philosophy but different in technical substrate. The opportune direction is to hook MML adapters and governed graph artifacts onto Apertus-compatible data, documentation, reproducibility, privacy, and audit practices rather than build a parallel sovereign pipeline. MML would contribute the executable knowledge representation and index. This is a proposed alignment, not an official collaboration or endorsement.

## Oleg Lavrovsky And Datalets: Swiss Open-Data Craft

[Oleg Lavrovsky](https://datalets.ch/) is relevant less as a single platform and more as a practical open-data pattern.

His work around Datalets, Swiss civic-tech, Wikidata practice, open data workshops, APIs, hackathons, and public-interest data tooling points to a missing ingredient in many AI proposals: the craft of making knowledge usable, inspectable, and maintained by communities.

For SOS, that matters because the Seed Vault cannot be only a static archive. It needs living practices:

- importing and cleaning public data;
- linking records to shared identifiers;
- making datasets usable through APIs and small tools;
- teaching people how to work with structured knowledge;
- supporting civic and institutional data stewardship;
- keeping public knowledge close to the people who understand it.

This is an important complement to minGPT. minGPT keeps the neural side small and inspectable. Open-data craft keeps the knowledge side social, practical, and alive.

## minGPT: Small Neural Workbench For Discovery

[karpathy/minGPT](https://github.com/karpathy/minGPT) is useful because it keeps GPT visible.

The repository describes itself as a minimal PyTorch reimplementation of GPT for training and inference. It is deliberately small, clean, interpretable, and educational, with the core model compact enough to study directly. That makes it valuable as a workbench, not because it is the largest or strongest model, but because it keeps the mechanics close to the surface.

That fits the SOS direction well.

In a dual-engine architecture, the LLM side should not always be a giant opaque system. A minGPT-style model could help discover:

- which graph dimensions are useful;
- where transition weights should change;
- when syntax still needs neural representation;
- where MML propagation is enough;
- where a small Transformer head improves phrasing or composition.

Keeping the model small also keeps the modelling conscious. A bounded experiment around `bank` as a financial institution versus `bank` as a river edge is easier to inspect than an internet-scale language model. If the model drifts, the drift can be seen in the corpus, the CML structure, the MML index, or the neural output.

In this sense, minGPT is not proposed as the production engine. It is a disciplined discovery instrument: small enough to understand, strong enough to reveal patterns, and constrained enough to keep the experiment honest.

## Svalbard Global Seed Vault: Preservation Analogy

The [Svalbard Global Seed Vault](https://www.seedvault.no/) is useful as an analogy for persistence.

Its public purpose is long-term, safe storage of seed duplicates from genebanks and nations, supporting the global effort to preserve future food supply. The important idea is not only storage. It is stewardship: preserve diversity, keep deposits durable, and make regeneration possible later.

SOS applies that metaphor to knowledge.

The Semantic Seed Vault is not a neural model. It is a durable, human-readable knowledge base where concepts, claims, evidence, contradictions, provenance, and patterns can be preserved. The MML matrix/index can then point into that knowledge base and move through it quickly.

The analogy helps clarify the boundary:

- the Seed Vault preserves semantic seeds;
- the Common Language Model defines how those seeds are described;
- the MML matrix/index provides fast traversal;
- the LLM helps discover candidate deposits;
- humans and governance processes decide what becomes durable.

This is why dual persistence matters. Knowledge should not live only inside model weights or only inside a matrix. It should also remain readable, reviewable, correctable, and transferable.

## Combined Alignment

Together, these initiatives sketch a realistic path:

| Initiative | Existing Strength | SOS Alignment |
| --- | --- | --- |
| Wikipedia | Human-readable public knowledge commons | Readable semantic seed vault |
| Wikidata | Structured multilingual knowledge graph | Structured seed vault and CML entity layer |
| SEMIC | European semantic interoperability discipline | CML governance and application-profile discipline |
| EuroVoc | Multilingual EU controlled vocabulary | Legal, policy, and governance vocabulary layer |
| Cellar + EUR-Lex | Authoritative EU legal publications and linked metadata | Legal substrate for rights, duties, procedures, and evidence |
| Apertus | Sovereign, open, accountable AI pipeline | Governance and training discipline for European SOS/MML development |
| Oleg Lavrovsky / Datalets | Swiss open-data and civic-data practice | Living data stewardship, Wikidata practice, public tooling, and community-maintained knowledge |
| minGPT | Small, inspectable GPT implementation for learning and experimentation | Controlled LLM discovery workbench and small generation head |
| Svalbard Global Seed Vault | Long-term preservation model for shared biological diversity | Analogy for a Semantic Seed Vault preserving durable human-readable knowledge |

The shared direction is not anti-LLM. It is anti-monolith.

LLMs remain useful where discovery, expression, ambiguity, and language generation matter. MML becomes useful where known structure, determinism, auditability, and efficient reuse matter. The knowledge base preserves what should not be repeatedly rediscovered.

That is the practical feasibility claim: parts of the ecosystem already exist. The architectural move is to connect them differently.
