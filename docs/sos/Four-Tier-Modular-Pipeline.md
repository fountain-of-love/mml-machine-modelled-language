# Four-Tier Modular Pipeline

> **A modular SOS pipeline can approximate selected observable LLM behaviors—semantic retrieval, evidence-based answering, routing, explanation, and linguistic rendering—without reproducing an LLM's internal mechanism or general capability.**

The pipeline addresses a practical systems problem: one general-purpose model is often expected to interpret intent, remember knowledge, find evidence, reason over it, and explain the result. When those responsibilities remain entangled, it becomes difficult to determine whether a failure came from misunderstood language, missing knowledge, poor retrieval, invalid reasoning, or unsupported generation. Corrections may require prompt changes, retraining, or replacement of the whole model, and the same request may not produce the same result twice.

SOS separates those responsibilities so each failure can be observed and corrected at the layer where it occurs:

- the **MML concept engine** addresses vocabulary mismatch, ambiguity, and terminology drift through governed concepts and typed relations;
- **Document PageRank** addresses information overload by prioritizing structurally important and governed sources without confusing authority with query relevance;
- **Text IR** addresses evidentiary precision by locating the exact passages that support or contradict a response; and
- a **micro language model or deterministic renderer** addresses usability by turning the governed evidence into human-readable language without becoming the primary knowledge store.

Together, the components contribute something none of them provides alone: a traceable path from the user's original words, through governed interpretation and ranked sources, to exact evidence and a constrained answer. The intermediate contracts make it possible to inspect where meaning changed, reproduce a result against a named knowledge snapshot, update knowledge without retraining the renderer, and benchmark the cost and quality of each layer independently.

This is stronger and more precise than describing MML alone as an LLM alternative. MML is the governed concept-execution component; SOS is the complete behavioral stack. The objective is not to recreate a transformer out of smaller technologies. It is to avoid forcing one mega-model to act simultaneously as knowledge store, search engine, semantic router, reasoner, and communicator—and thereby make bounded knowledge work more governable, reproducible, correctable, and potentially less resource-intensive.

The resource claim remains a hypothesis to measure. Sparse deterministic routing and retrieval can reduce how much material reaches the language model, but end-to-end energy, latency, and quality depend on the graph, indexes, iteration count, retrieved context, and chosen renderer.

## Execution architecture

The architecture below shows how those problem boundaries collaborate in one execution path. It is included to make the handoffs and failure boundaries concrete, not to present the mechanisms as ends in themselves.

The tiers describe responsibilities, not a rigid one-way implementation. Concept routing and lexical retrieval begin in parallel and are fused later. This prevents semantic interpretation from discarding literal words, names, and identifiers while still addressing vocabulary mismatch through governed concepts.

A concept engine can fail when:

- the query uses an unknown term;
- the ontology lacks the intended concept;
- a name or identifier must be preserved literally;
- premature concept mapping selects the wrong sense.

The safer execution shape is:

```text
                         ┌─→ Lexical query terms ──────────────┐
[User query] → Normalize│                                      │
                         └─→ Governed concept candidates ───────┤
                                                               ▼
                                                Candidate document generation
                                                               │
                                      ┌────────────────────────┴──────────────┐
                                      ▼                                       ▼
                           Document authority                         Query relevance
                         PageRank / provenance                  concept + lexical scores
                                      └────────────────────────┬──────────────┘
                                                               ▼
                                                    Document-level fusion
                                                               │
                                                               ▼
                                                 Passage/snippet retrieval
                                             BM25 + concepts + typed constraints
                                                               │
                                                               ▼
                                                  Governed evidence packet
                                                               │
                                      ┌────────────────────────┴──────────────┐
                                      ▼                                       ▼
                              Deterministic template                  Micro language model
                                      └────────────────────────┬──────────────┘
                                                               ▼
                                                  Citation/claim verification
                                                               │
                                                               ▼
                                                    Human-friendly output
```

Authority, relevance, and passage evidence may be fused or iterated. The canonical knowledge base remains human-readable and governed; lexical indexes, MML matrices, note graphs, passage indexes, and optional embeddings are reproducible compiled views rather than the only copies of knowledge.

## Refined responsibilities

This section turns the execution architecture above into explicit component contracts. Its purpose is not to showcase four technologies. It explains how the components divide real information problems—ambiguous language, terminology drift, inaccessible evidence, inconsistent answers, high inference cost, and unsupported prose—and what each component contributes to solving them.

The four subsections follow one illustrative request—`treatment for sugar disease`—from ambiguous user language to a governed, human-readable answer:

1. the **MML concept engine** proposes inspectable meanings and query constraints;
2. **Document PageRank** helps prioritize the most relevant and authoritative knowledge sources;
3. **Text IR** retrieves exact supporting passages from those sources; and
4. the **micro language model** renders only the supported material into clear language.

The example is deliberately continuous: each tier enriches or narrows the same request without taking over the work assigned to the other tiers. It demonstrates the intended interfaces, not a claim that the current MML prototype already implements the complete pipeline or is suitable for medical use.

### Problems addressed by the combination

| Real problem | Contribution | Practical value |
| --- | --- | --- |
| People use different words for the same thing | Governed synonyms and aliases connect surface expressions such as `sugar disease`, `diabetes mellitus`, and `diabetes` to explicit candidate concepts. | Relevant knowledge does not disappear merely because the query and source use different vocabulary. |
| Acronyms are ambiguous | Acronym mappings retain multiple governed expansions and use context to rank them instead of replacing the acronym irreversibly. | `T2D` can be resolved to `type_2_diabetes` in a clinical context while uncertain or conflicting expansions remain visible. |
| Related concepts are not identical | An ontology records distinctions such as disease type, treatment class, broader concept, narrower concept, and contraindication. | Expansion can improve recall without silently treating Type-1 and Type-2 diabetes as interchangeable. |
| Meaning depends on relationships | Typed topology captures how concepts, evidence, sources, and constraints are connected; propagation can surface candidates reached through several governed relations. | The system can find structurally relevant material even when no single document contains every query term, while retaining the path that caused it to surface. |
| Terminology and policy change over time | Concepts, aliases, relations, validity periods, and provenance are governed data rather than meanings hidden only inside model weights. | A renamed term or corrected relation can be changed explicitly, reviewed, versioned, and recompiled without retraining a language model. |
| Answers drift between runs | Frozen inputs, normalization, weights, algorithm version, and execution settings produce the same ranked output for the same request. | Results can be reproduced, compared, investigated, and audited. Determinism controls execution variance; governed updates control knowledge drift. |
| Large models repeatedly spend compute recovering stable context | Sparse concept propagation and classical retrieval narrow the evidence before language rendering. A propagation iteration is proportional to the traversed nodes and edges, although total cost also depends on iteration count and retrieval scope. | Bounded tasks may require less memory, energy, and inference compute; the actual saving remains an empirical benchmark question rather than a guaranteed property. |
| Fluent output can obscure unsupported claims | The renderer receives an explicit evidence packet and is checked against it. | Language generation becomes a constrained communication step rather than the uninspected source of facts. |

These contributions are complementary. Synonyms and acronyms improve access to concepts; ontology preserves distinctions; topology exposes useful connections; deterministic compilation and execution make the result repeatable; retrieval anchors it in exact evidence; and constrained rendering makes that evidence usable. No individual mechanism solves the whole problem.

### 1. MML concept engine

The concept engine addresses ambiguity, vocabulary mismatch, and semantic drift before they contaminate retrieval. It should not claim to know what the user actually means with certainty. It produces ranked, inspectable interpretations while preserving stable senses, synonyms, acronyms, aliases, typed relations, constraints, contradictions, unresolved terms, validity, and provenance.

Its governed structures contribute in different ways:

- **synonyms and aliases** connect different expressions without erasing the original query;
- **acronyms** preserve and rank possible expansions instead of assuming one universal meaning;
- **ontology** records what kind of concept something is and which distinctions must survive expansion;
- **typed relations** state why two concepts are connected, such as `ALIAS_OF`, `IS_A`, `TREATS`, or `CONTRAINDICATED_FOR`;
- **topology** lets activation reach related candidates through those governed connections;
- **provenance and validity** identify who asserted a mapping and when it applies.

The added value is controlled semantic expansion. The engine can broaden a search enough to overcome vocabulary mismatch while using types, exclusions, and provenance to prevent that expansion from becoming uncontrolled semantic drift.

An illustrative output contract is:

```json
{
  "surface_query": "treatment for sugar disease",
  "candidate_intents": [
    {
      "concept": "type_2_diabetes",
      "score": 0.72,
      "evidence": ["alias:sugar-disease", "context:treatment"]
    },
    {
      "concept": "diabetes_unspecified",
      "score": 0.24,
      "evidence": ["broader-concept:diabetes"]
    }
  ],
  "unresolved_terms": [],
  "constraints": [],
  "contradictions": []
}
```

For this example, the concept engine does not answer the treatment question. A synonym or alias relation connects `sugar disease` to diabetes; an ontology keeps `type_2_diabetes`, `type_1_diabetes`, and `diabetes_unspecified` distinct; contextual topology makes the relation between `treatment` and the type-2 candidate relevant; and provenance shows where those mappings came from. If the user had written `T2D`, an acronym relation could reach the same governed candidate without hard-coding that expansion into every document.

The engine retains the original wording and exposes the evidence behind each mapping. Its output gives the following retrieval tiers a better query while keeping ambiguity visible.

Its job is semantic routing, not final certainty.

The proposed multiplex implementation can remain deterministic if it freezes:

- layer sources;
- identifiers;
- relation weights;
- normalization rules;
- propagation horizon;
- fusion settings;
- algorithm version.

Given the same normalized inputs and execution environment, it should compile the same graph or tensor and produce the same activation. This addresses reproducibility and run-to-run variance: an unexpected result can be recreated against a named knowledge snapshot and algorithm version. It does not guarantee that the governed knowledge is correct, only that its effect is inspectable and repeatable.

For sparse propagation, each iteration visits the relevant nodes and edges rather than performing dense transformer inference over a large parameter set. This creates an opportunity to reduce compute and energy for bounded retrieval tasks. The full cost is not simply “linear” in every circumstance: it also depends on convergence iterations, active graph size, indexing, and any downstream renderer. Energy and latency benefits therefore need to be measured against comparable alternatives.

### 2. Document PageRank

Document PageRank supplies authority and structural importance through links, citations, source relationships, and provenance context. Authority must remain distinct from relevance: a highly cited document can be irrelevant to the current query, while a newly issued authoritative correction may have few incoming links.

Continuing the example, this tier uses the concept candidates and original lexical terms to identify which parts of the governed knowledge base deserve attention. It might prioritize a current clinical guideline about type-2 diabetes management, an applicable formulary, and a governed concept note that links the colloquial term to the clinical concept. It should demote an otherwise prominent source about type-1 diabetes when the available constraints point elsewhere.

Document PageRank does not yet fetch the final pieces of evidence. It ranks candidate documents or notes so that the next tier can search the strongest sources first. Where the intent remains ambiguous, it should preserve documents for multiple candidate interpretations rather than silently collapse them into one.

Document selection should therefore combine declared features such as:

```text
document score
= query relevance
+ source authority
+ citation topology
+ provenance quality
+ recency/applicability
- contradiction or invalidity penalties
```

The exact fusion function must be versioned and tested. PageRank contributes one feature rather than acting as the complete selector or an oracle of truth.

### 3. Text information retrieval

This tier extracts exact, high-density passages from selected records. BM25 is the preferred first implementation, with TF-IDF retained as a simpler reference. Dense or hybrid retrieval may be added without changing the responsibility boundary.

For `treatment for sugar disease`, Text IR searches within the documents prioritized by the previous tier. It combines the literal query with governed expansions such as `type 2 diabetes`, `diabetes mellitus`, `management`, and `treatment`, while applying any type, validity, or source constraints. It then returns the exact passages that support a response—for example, a guideline passage describing first-line management—rather than treating the document's authority score as evidence for a particular claim.

Text IR receives:

- original query terms;
- concept aliases;
- required phrases;
- entity identifiers;
- prohibited senses;
- document restrictions;
- jurisdiction or validity constraints.

Its output preserves exact offsets so the evidence remains independently verifiable:

```json
{
  "document_id": "guideline:type-2-diabetes-management:2026",
  "passage_id": "initial-management:paragraph-2",
  "start": 412,
  "end": 687,
  "text": "[Exact illustrative guideline passage returned here]",
  "lexical_score": 0.81,
  "concept_score": 0.74,
  "authority_score": 0.96
}
```

### 4. Micro language model

The micro language model is a linguistic renderer: it turns the governed evidence packet into fluent output. Deterministic templates remain preferable for operations where exact wording, reproducibility, or risk requires them.

In the running example, the renderer receives the candidate intent, its unresolved ambiguity, the selected passages, their citations, and any applicability constraints. It can explain that `sugar disease` was interpreted as type-2 diabetes, summarize only the supported management information, preserve qualifications from the sources, and ask for clarification or refuse a definitive answer when the evidence packet is insufficient. It must not rely on its parameter memory to add a treatment that was not retrieved.

An illustrative rendering instruction could be:

```text
[INTERPRETATION]: "sugar disease" most likely refers to Type-2 Diabetes;
                  preserve uncertainty if the diabetes type is not established.
[EVIDENCE]:       Use only the attached, cited guideline passages.
[CONSTRAINT]:     Do not provide individualized medical advice.
[TASK]:           Explain the supported treatment information in plain language
                  and state what requires confirmation by a clinician.
```

Supplying evidence reduces the model's memory burden but does not prevent hallucination by itself. A small model can still:

- invent a bridge between snippets;
- remove an important qualification;
- state correlation as causation;
- confuse absence of evidence with evidence of absence;
- add plausible but unsupported details.

The safe contract is:

> The micro model may select, compress, order, and paraphrase supported claims. It may not introduce claims absent from the evidence packet.

Enforcement can include:

- sentence-level citations;
- claim extraction after generation;
- entailment or lexical-support checks;
- structured output;
- low-variance decoding;
- deterministic templates for high-risk tasks;
- refusal when evidence is insufficient.

The medical query above is illustrative only. Real medical use requires authoritative sources, applicability checks, professional oversight, and appropriate regulatory handling.

## Activation, propagation, and reasoning

Diffusion, activation, personalized PageRank, and power iteration can discover and rank candidate multi-hop semantic routes. They do not automatically validate the logical composition expressed by those routes.

> **Diffusion discovers and ranks candidate semantic routes; typed traversal and validation determine whether a route satisfies a requested reasoning chain.**

Validated multi-hop reasoning additionally requires:

- typed direction;
- relation-composition rules;
- stable entity identity;
- constraints and exclusions;
- provenance and applicability;
- often a query planner or symbolic verifier.

Those capabilities can become future deterministic MML layers. They are not properties already established by the current bounded activation engine. Activation is also not transformer attention, and high activation is not automatically reasoning or proof.

## Governed evidence packet

MML should not emit prose directly. The first shared output of the retrieval tiers should be a structured evidence packet:

```json
{
  "intent_candidates": [],
  "resolved_concepts": [],
  "ranked_notes": [],
  "supporting_passages": [],
  "supporting_paths": [],
  "contradictions": [],
  "source_citations": [],
  "applicability_constraints": [],
  "confidence_limits": [],
  "snapshot_id": "sha256:..."
}
```

This packet is the contract between retrieval and rendering. It enables deterministic templates, small language models, alternative renderers, and post-generation verification to consume the same governed evidence.

## What remains an empirical hypothesis

It is too strong to assume that a one-billion-parameter model can render evidence as effectively as a much larger model or that it will use a fixed fraction of the energy. That is what the proposed minGPT experiment must test.

The safer claim is:

> **Externalizing stable knowledge may allow a substantially smaller language model to perform bounded evidence-rendering tasks with competitive quality and lower resource use.**

Measure rather than assume:

- answer quality;
- evidence faithfulness;
- unsupported-claim rate;
- parameter count;
- training tokens;
- peak memory;
- latency;
- energy proxies;
- correction cost.

A useful comparison is the same small transformer under four conditions:

1. model alone;
2. model with ordinary lexical retrieval;
3. model with modern hybrid RAG;
4. model with the complete SOS evidence packet.

TF-IDF, dense retrieval, note PageRank, MML, and their fusions remain ablations underneath that top-level experiment.

## Recommended storage architecture

The storage formats have distinct responsibilities. The knowledge base is authoritative; indexes are disposable and reproducible.

### Canonical layer: structured Markdown

Human-readable notes are the governed source of truth:

```yaml
---
id: concept:type-2-diabetes
type: concept
labels:
  en: Type 2 diabetes
aliases:
  - type-2 diabetes
  - diabetes mellitus type 2
source_uris:
  - https://example.eu/authoritative-concept
status: reviewed
valid_from: 2026-01-01
---
```

The body contains explanation, evidence, qualifications, disagreement, and history.

### Machine-readable contracts: JSON-LD or RDF

Machine-readable records preserve:

- stable identifiers;
- typed relations;
- source URIs;
- qualifiers;
- jurisdiction;
- validity;
- confidence;
- review state.

This creates a path to Linked Open Data interoperability without replacing original public identifiers.

### Compiled execution layer

Build disposable indexes from the canonical records:

- BM25 or another inverted index;
- MML concept matrix;
- note-level PageRank;
- passage index;
- provenance lookup;
- optional embeddings.

SQLite is sufficient for a first bounded implementation. A dedicated graph database should be introduced only when scale or query complexity justifies it.

### Source-evidence layer

PDFs, webpages, RDF responses, legislation, and other source materials remain evidence artifacts rather than the canonical semantic model. Preserve them with:

- URI;
- retrieval timestamp;
- content hash;
- license or applicable terms;
- extraction method;
- page, section, or character offsets.

The storage flow is:

```text
Source artifacts
      │
      ▼
Governed Markdown + JSON-LD/RDF
      │
      ├─→ lexical index
      ├─→ MML concept matrix
      ├─→ note PageRank
      ├─→ passage index
      ├─→ provenance lookup
      └─→ optional embeddings
```

## Core claim

> **MML does not approximate an LLM by imitating neural computation. SOS approximates selected LLM behaviors by decomposing them into governed semantic routing, authoritative knowledge selection, precise evidence retrieval, and constrained linguistic rendering.**

This is a meaningful and testable alternative architecture. Its value must be established through bounded implementation, ablation, source-grounded evaluation, resource measurement, and comparison with ordinary retrieval and small-model baselines.
