# MML Research Contract

## Societal question

> Can Europe organise its knowledge as linked, executable semantic infrastructure that remains inspectable and governable?

The wider ambition is to help Europe evolve with AI, participate in shaping that transformation, remain economically competitive, and explore a more sustainable alternative to concentrating knowledge and capability in ever-larger models. This repository cannot prove that Europe can coordinate the institutions, standards, licensing, funding, maintenance, and participation required. It treats that as a motivating societal and policy question, not as the falsifiable result of the Python prototype.

MML is an executable, weighted knowledge representation whose explicit structure is governed by people and whose weights can be updated from text statistics.

Its learning contract is supervised and governed: humans or accountable institutions author and review semantic identities, aliases, relations, evidence, and corrections. Statistical construction adjusts explicit weights. LLM training is generally self-supervised prediction over large corpora; MML is not evaluated on whether it autonomously rediscovers semantics that its architecture intentionally asks people to govern.

## Hypothesis

Human-governed concepts and relations, augmented by corpus-derived weights, can be executed reproducibly and updated locally at the knowledge-source level while retaining inspectable identity, provenance, consequences, and rollback.

The hypothesis becomes uninteresting if the structure cannot support useful applications, cannot expose valid routes back to governed sources, or offers no operational advantage relative to its construction and governance cost. It does not require universal superiority over TF-IDF and does not ask MML to imitate an LLM.

## Non-claims

- MML is not a generative language model.
- Graph propagation is not transformer attention.
- The authored fixtures do not demonstrate autonomous abstraction or generalization.
- Retrieval scores are not probabilities or legal conclusions.
- A valid path is not automatically a causal decomposition of a score.
- Diffusion and power iteration rank reachable concepts; they are not by themselves validated multi-hop reasoning.
- The dense NumPy prototype does not demonstrate sparse execution at public-graph scale.

## What the prototype demonstrates

### Representation

- balanced, explicit river-bank and financial-bank senses;
- governed concepts, phrase aliases, and typed relations;
- stable identifiers and construction evidence;
- separate corpus-derived and authored structure.

### Execution

- deterministic bounded propagation;
- combinatorial multi-token activation;
- explicit positive and contradictory evidence;
- source-addressed graph paths and score components.

### Evolution

- content-addressed graph snapshots;
- immutable relation and alias changes;
- observable before/after consequences;
- exact reconstruction and rollback.

Deterministic replay is one component of auditability. It does not replace provenance completeness, event logging, validation, documented limitations, human oversight, or governance, and it is not by itself an EU AI Act compliance claim.

These three demonstrations are the current centre of the project.

## Retrieval diagnostic

The 50-document, six-query synthetic fixture is retained as a small downstream diagnostic. It compares lexical overlap, TF-IDF, co-occurrence MML, typed MML, and one fixed multiplicative MML/lexical hybrid. The hybrid makes complementarity reproducible without calibration or parameter search. MML additionally receives supervised concept mappings and negative evidence; the lexical baselines do not. The comparison therefore measures end-to-end treatments, not equal-input algorithms. The diagnostic checks determinism, basic usefulness, and regression; it is not an acceptance test for MML or a production integrity system.

Because the fixture has guided implementation, it is development evidence rather than held-out validation. Earlier challenge slicing, hybrid calibration, sensitivity selection, and threshold verdicts remain documented in [the archived research note](benchmark/archive/v1-retrieval-research.md), not on the active critical path.

Those harder diagnostics compare useful observable outcomes, but they do not define success for a supervised semantic-infrastructure paradigm. They remain opportunities for falsification and failure analysis—especially zero-overlap retrieval and hard-negative intrusion—rather than peer-equivalence tests pretending that TF-IDF and MML have the same inputs or responsibilities.

## Evidence still needed

1. A bounded public domain with appropriately licensed sources and stable identifiers.
2. Independently held-out documents, queries, and judgments.
3. Independent assessors and agreement reporting.
4. Provenance-complete execution over public graph sources.
5. Community proposal, review, correction, fork, and publication history.
6. Sparse performance and resource measurements at meaningful scale.

The active [retrieval report](benchmark/results/v1.md) and [governance contract](sos/Commons-Governance.md) state the present boundary.

## Proposed next step: one Linked Open Data slice

Test technical feasibility without claiming institutional feasibility:

1. Select one narrow GDPR concept already represented in the demo.
2. Identify authoritative, reusable Linked Open Data records from sources such as CELLAR/EUR-Lex and EuroVoc, optionally aligned with Wikidata.
3. Preserve their HTTP URIs as the primary concept and source identities rather than inventing replacement identifiers.
4. Retrieve the RDF through a documented URI or SPARQL query and store a reproducible source snapshot.
5. Adapt a minimal set of triples into governed MML nodes and typed relations while retaining original URI, language, source, and applicable terms.
6. Execute one query and produce a trace from input through activated MML routes back to the originating public URIs.
7. Change or qualify one mapped assertion, regenerate the snapshot, inspect the consequence, and restore the original version through Git history.

Success would show that URI-addressed public knowledge can be compiled and executed by this prototype with preserved identity and provenance. It would not show that Europe has organised the wider commons, that the selected source is sufficient, or that MML governance is socially legitimate.
