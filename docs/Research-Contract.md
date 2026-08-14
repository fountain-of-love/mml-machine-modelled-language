# MML Research Contract

## Societal question

> Can Europe organise its knowledge as linked, executable semantic infrastructure that remains inspectable and governable?

The wider ambition is to help Europe evolve with AI, participate in shaping that transformation, remain economically competitive, and explore a more sustainable alternative to concentrating knowledge and capability in ever-larger models. This repository cannot prove that Europe can coordinate the institutions, standards, licensing, funding, maintenance, and participation required. It treats that as a motivating societal and policy question, not as the falsifiable result of the Python prototype.

MML is an executable, weighted knowledge representation whose explicit structure is governed by people and whose weights can be updated from text statistics.

Its learning contract is supervised and governed: humans or accountable institutions author and review semantic identities, aliases, relations, evidence, and corrections. Statistical construction adjusts explicit weights. LLM training is generally self-supervised prediction over large corpora; MML is not evaluated on whether it autonomously rediscovers semantics that its architecture intentionally asks people to govern.

## The Three Hypotheses

The MML research programme is organized around three cumulative but independently falsifiable hypotheses. Their canonical capability definitions live in the [MML Research Programme](capabilities/README.md):

### 1. [Semantic Representation](capabilities/semantic-representation/README.md)

> Meaning represented explicitly and richly enough can make ordinary mathematics semantically useful.

The controlled intervention changes governed semantic identity while holding the corpus, compiler, query strategy, and numerical settings fixed. This hypothesis is weakened if richer representation does not improve declared semantic outcomes across independently designed ambiguity and relation tasks, or if any observed benefit depends on hidden changes to the mathematics.

### 2. [Knowledge State Execution](capabilities/knowledge-state-execution/README.md)

> Once established knowledge is compiled into an executable representation, it need not be reconstructed from prose or latent model parameters every time it is used.

This hypothesis concerns reusable capability, not merely deterministic serialization. It is weakened if compiling, governing, updating, and executing established knowledge offers no operational advantage over reconstructing the same task state at use time, or if the compiled artifact cannot preserve identity, provenance, correction, replay, and rollback.

### 3. [Combinatorial Uniqueness](capabilities/combinatorial-uniqueness/README.md)

> Several individually broad but sufficiently independent semantic constraints can combine into a narrow, distinctive conceptual coordinate or retrieval target.

This hypothesis is weakened if composed fields do not add useful specificity beyond their individual coordinates, simple additive combination, or relevant retrieval baselines; if useful combinations require bespoke learned primitives after all; or if governance and validation costs erase the proposed advantage.

In compact form: **Represent meaning. Compile knowledge. Compose concepts.**

| Hypothesis | Current status |
| --- | --- |
| **Representation** | Addressed by bounded A/B experiments; not established universally. |
| **Knowledge State Execution** | One bounded exact typed-chain experiment demonstrates compiled reuse and governed mutation; broader independent evidence is still needed. |
| **Combinatorial Uniqueness** | Three atomic authored studies now distinguish direct intersection (`LOCALLY_CONSISTENT`), governed legal qualification (`LOCALLY_CONSISTENT`), and explicit stage-scoped transition (`CONSISTENT`). The original failed flat-conjunction control is preserved. Held-out construction, useful basis coverage, and scaling remain untested. |

The programme becomes uninteresting if the structure cannot support useful applications, cannot expose valid routes back to governed sources, or offers no operational advantage relative to its construction and governance cost. It does not require universal superiority over TF-IDF and does not ask MML to imitate an LLM.

## Non-claims

- MML is not a generative language model.
- Graph propagation is not transformer attention.
- The authored fixtures do not demonstrate autonomous abstraction or generalization.
- Retrieval scores are not probabilities or legal conclusions.
- A valid path is not automatically a causal decomposition of a score.
- Diffusion and power iteration rank reachable concepts; they are not by themselves validated multi-hop reasoning.
- The dense NumPy prototype does not demonstrate sparse execution at public-graph scale.

## What the Prototype Demonstrates

### Representation evidence

- balanced, explicit river-bank and financial-bank senses;
- governed concepts, phrase aliases, and typed relations;
- stable identifiers and construction evidence;
- separate corpus-derived and authored structure.

### Knowledge State Execution mechanics

- deterministic compilation and repeated execution from a named model;
- content-addressed snapshots and exact reconstruction;
- immutable relation and alias changes;
- observable before/after consequences and exact rollback.

These mechanics make compile-once, execute-many testable. They do not yet compare reuse cost, latency, resource demand, correction effort, or result stability against repeated reconstruction.

### Combinatorial Uniqueness development evidence

- independently propagated activation fields;
- normalized geometric-mean combination rather than additive averaging;
- redundant-coordinate, invalidity, permutation, and leave-one-out controls;
- governed direct legal qualification, contrast, unsupported non-resolution, and epistemic non-promotion;
- explicit stage-local semantic transition with antecedent provenance; and
- preservation of failed flat conjunction as a distinct control rather than relabelling it as transition.

These studies make three composition contracts executable and inspectable over co-authored synthetic fixtures. They do not establish independently authored construction, useful combinatorial coverage, real legal validity, automatic stage-boundary discovery, or scaling across held-out domains.

Deterministic replay is one component of auditability. It does not replace provenance completeness, event logging, validation, documented limitations, human oversight, or governance, and it is not by itself an EU AI Act compliance claim.

Bounded development evidence now exists for all three hypotheses. Its maturity differs by programme and remains below confirmatory evidence: the fixtures are authored, small, and not independently held out.

## Semantic representation benchmark

The primary executable benchmark reuses the Words Carry Weight mechanism across three authored ambiguity scenarios. It holds the co-occurrence compiler and Personalized PageRank query strategy fixed while changing semantic identity grounding and query focus. It measures intended-versus-contrast margin, cross-meaning activation, and deterministic replay.

This first version is development evidence that richer semantic identity can improve the usefulness of the same mathematics in these bounded cases. It does not establish the broader hypothesis for association, synonymy, hierarchy, roles, constraints, or policy-composed relation matrices. Those require new controlled suites with the same representation-first experimental discipline.

## Retrieval application diagnostic

The 50-document, six-query synthetic fixture is retained as a small downstream diagnostic. It compares lexical overlap, TF-IDF, co-occurrence MML, typed MML, and one fixed multiplicative MML/lexical hybrid. The hybrid makes complementarity reproducible without calibration or parameter search. MML additionally receives supervised concept mappings and negative evidence; the lexical baselines do not. The comparison therefore measures end-to-end treatments, not equal-input algorithms. The diagnostic checks determinism, basic usefulness, and regression; it is not an acceptance test for MML or a production integrity system.

Because the fixture has guided implementation, it is development evidence rather than held-out validation. Earlier challenge slicing, hybrid calibration, sensitivity selection, and threshold verdicts remain documented in [the archived research note](benchmark/archive/v1-retrieval-research.md), not on the active critical path.

Those harder diagnostics compare useful observable outcomes, but they do not define success for a supervised semantic-infrastructure paradigm. They remain opportunities for falsification and failure analysis—especially zero-overlap retrieval and hard-negative intrusion—rather than peer-equivalence tests pretending that TF-IDF and MML have the same inputs or responsibilities.

## Evidence Still Needed

### Representation

1. Independently authored semantic distinctions, documents, queries, and judgments.
2. Controlled suites for relation type, direction, role, constraint, exclusion, and provenance—not identity alone.
3. Ablations that hold execution mathematics fixed while changing one representational dimension at a time.
4. Independent assessors and agreement reporting.

### Knowledge State Execution

1. A bounded public domain with appropriately licensed sources and stable identifiers.
2. A declared reconstruction baseline that rebuilds equivalent task state from source material at use time.
3. Measurements of compilation cost, repeated execution cost, latency, resource demand, correction effort, and output stability across many queries.
4. Provenance-complete compilation and execution over public knowledge sources.
5. Community proposal, review, correction, fork, publication, and rollback history.

### Combinatorial Uniqueness

1. Held-out tasks comparing single coordinates, pairs, and larger combinations.
2. Comparisons with Boolean conjunction, additive activation, lexical retrieval, and available dense-retrieval baselines.
3. Ablations for coordinate independence, aliases, relation types, policy coefficients, and each participating concept.
4. Measurements of specificity, coverage, invalid-combination rejection, construction cost, and execution cost at meaningful scale.

### Shared production evidence

1. Sparse performance and resource measurements at meaningful scale.
2. Schema validation, access control, operational monitoring, and integrity controls.
3. Representative domain coverage and independent replication.

The active [semantic representation report](capabilities/semantic-representation/results/v1.md), legacy [retrieval report](benchmark/results/v1.md), and [governance contract](sos/Commons-Governance.md) state the present boundary.

## Proposed Next Step: A Knowledge State Execution Slice

The next evidence slice extends the Knowledge State Execution hypothesis through one Linked Open Data domain. It tests technical feasibility without claiming institutional feasibility or combinatorial scaling:

1. Select one narrow GDPR concept already represented in the demo.
2. Identify authoritative, reusable Linked Open Data records from sources such as CELLAR/EUR-Lex and EuroVoc, optionally aligned with Wikidata.
3. Preserve their HTTP URIs as the primary concept and source identities rather than inventing replacement identifiers.
4. Retrieve the RDF through a documented URI or SPARQL query and store a reproducible source snapshot.
5. Adapt a minimal set of triples into governed MML nodes and typed relations while retaining original URI, language, source, and applicable terms.
6. Execute one query and produce a trace from input through activated MML routes back to the originating public URIs.
7. Change or qualify one mapped assertion, regenerate the snapshot, inspect the consequence, and restore the original version through Git history.

Success would show that URI-addressed public knowledge can be compiled once and executed repeatedly by this prototype with preserved identity and provenance. The experiment should compare that reusable artifact with a declared reconstruction-at-use baseline. It would not establish the Representation hypothesis beyond the selected mappings, validate Combinatorial Uniqueness, show that Europe has organised the wider commons, prove that the selected source is sufficient, or establish that MML governance is socially legitimate.
