# MML Research Contract

## Central research question

> **Can an LLM progressively convert recurring probabilistic tasks into governed deterministic operations without reducing its ability to handle genuinely novel tasks?**

This is the sharper research question for the LLM-to-MML boundary. It turns the
programme into a measurable conversion loop:

```text
probabilistic interaction
  -> recurring task identified
  -> candidate operator proposed
  -> human governance and approval
  -> deterministic execution and monitoring
  -> correction, rollback, or return to probabilistic handling
```

The desired result is not to make every interaction deterministic. MML should
make known, repeated, and governable work cheaper, faster, more reproducible,
and easier to audit, while preserving probabilistic exploration for novel or
insufficiently understood work.

The primary quantities are divided between MML-native operator measurements and
system-level integration measurements:

| Quantity | Operational meaning |
| --- | --- |
| MML-native: deterministic execution error | Incorrect deterministic outcomes under a declared operator contract |
| MML-native: reproducibility | Rate of exact or contract-equivalent replay |
| MML-native: operator coverage | Percentage of governed recurring task classes with a valid operator |
| MML-native: false operator creation | Invalid, unsupported, or non-recurring operators accepted from the proposal set |
| MML-native: regression rate | Previously passing operator cases that fail after updates or recompilation |
| MML-native: compilation and execution cost | Cost of compilation, storage, and deterministic execution |
| MML-native: compilation and execution latency | Cold, warm, and repeated-query latency |
| MML-native: capability extraction rate | Accepted reusable operators divided by recurring task families proposed |
| System-level: deterministic interaction share | Percentage of eligible interactions routed to governed operators |
| System-level: cost and latency reduction | End-to-end change including probabilistic proposal, governance, routing, MML, and fallback |
| System-level: human approval burden | Review time, decisions, corrections, and rejected proposals per accepted operator |
| System-level: novelty detection | Accuracy of routing genuinely novel or unsupported interactions away from deterministic operators |

These quantities must be reported by task class, reuse horizon, operator version,
and measurement layer. Aggregate percentages without denominators, eligibility
rules, or human-effort accounting are insufficient. MML-native measurements must
not be presented as evidence that the surrounding system routed interactions
correctly.

## Societal question

> Can Europe organise its knowledge as linked, executable semantic infrastructure that remains inspectable and governable?

The wider ambition is to help Europe evolve with AI, participate in shaping that transformation, remain economically competitive, and explore a more sustainable alternative to concentrating knowledge and capability in ever-larger models. The repository treats institutional coordination, standards, licensing, funding, maintenance, and participation as the next societal and policy layer beyond the Python prototype.

MML is an executable, weighted knowledge representation whose explicit structure is governed by people and whose weights can be updated from text statistics.

Its learning contract is supervised and governed: humans or accountable institutions author and review semantic identities, aliases, relations, evidence, and corrections. Statistical construction adjusts explicit weights. LLM training is generally self-supervised prediction over large corpora; MML is not evaluated on whether it autonomously rediscovers semantics that its architecture intentionally asks people to govern.

## The Research Streams

The MML research programme is organized around three independently testable foundation hypotheses and one accumulated application hypothesis. Their canonical capability definitions live in the [MML Research Programme](capabilities/README.md):

### 1. [Semantic Representation](capabilities/semantic-representation/README.md)

> Meaning represented explicitly and richly enough can make ordinary mathematics semantically useful.

The controlled intervention changes governed semantic identity while holding the corpus, compiler, query strategy, and numerical settings fixed. The validation test is whether richer representation improves declared semantic outcomes across independently designed ambiguity and relation tasks while the mathematics remains fixed.

### 2. [Knowledge State Execution](capabilities/knowledge-state-execution/README.md)

> Once established knowledge is compiled into an executable representation, it need not be reconstructed from prose or latent model parameters every time it is used.

This hypothesis concerns reusable capability, not deterministic serialization alone. The validation test compares the full lifecycle of compiling, governing, updating, and executing established knowledge with reconstructing the same task state at use time, while preserving identity, provenance, correction, replay, and rollback.

### 3. [Combinatorial Uniqueness](capabilities/combinatorial-uniqueness/README.md)

> Several individually broad but sufficiently independent semantic constraints can combine into a narrow, distinctive conceptual coordinate or retrieval target.

The validation test asks whether composed fields add useful specificity beyond their individual coordinates, simple additive combination, and relevant retrieval baselines, while tracking whether bespoke learned primitives or governance costs erase the proposed advantage.

### 4. [Semantic Navigation](capabilities/semantic-navigation/README.md)

> Represented dimensions, compiled knowledge state, and coordinate composition can accumulate into exact retrieval and useful ambiguity navigation without inventing unsupported specificity.

The validation test checks whether meaning is preserved between capability layers, persistent compilation preserves the answer, exact composition retains compatible candidates, ambiguity remains explicit, navigation keeps imputations governed, and realistic repeated use amortizes represented and compiled state. Its success remains an accumulated result rather than a substitute for the three upstream hypotheses.

In compact form: **Represent meaning. Compile knowledge. Compose concepts. Navigate governed knowledge.**

| Hypothesis | Current status |
| --- | --- |
| **Representation** | Addressed by bounded A/B experiments; the next target is independent relation and ambiguity coverage. |
| **Knowledge State Execution** | One bounded exact typed-chain experiment demonstrates compiled reuse and governed mutation; the next target is independent lifecycle and cost evidence. |
| **Combinatorial Uniqueness** | Three atomic governed-input studies distinguish direct intersection (`LOCALLY_CONSISTENT`), governed legal qualification (`LOCALLY_CONSISTENT`), and explicit stage-scoped transition (`CONSISTENT`). The original flat-conjunction control is preserved. The next target is held-out construction and basis coverage. |
| **Semantic Navigation** | One prompt-provided 60-animal seed composes the four operational contracts and reports exact retrieval, navigation, code equivalence, and deterministic reuse accounting. The next target is independent source quality, larger scale, and wall-clock evidence. |

The programme succeeds when the structure supports useful applications, exposes valid routes back to governed sources, and offers an operational advantage relative to its construction and governance cost. It targets recurring governed work rather than universal superiority over TF-IDF or imitation of an LLM.

## Scope And Architectural Distinctions

- MML is a semantic execution layer, not a generative language model.
- Graph propagation is a distinct execution strategy from transformer attention.
- Curated fixtures establish governed-input mechanics; autonomous abstraction and generalization are separate validation targets.
- Retrieval scores are not probabilities or legal conclusions.
- A valid path is not automatically a causal decomposition of a score.
- Diffusion and power iteration rank reachable concepts; typed traversal and validation are the extension required for multi-hop reasoning.
- The dense NumPy prototype establishes the semantics of the current operator; sparse execution at public-graph scale is a future performance target.

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

These mechanics make compile-once, execute-many testable. The next lifecycle benchmark compares reuse cost, latency, resource demand, correction effort, and result stability against repeated reconstruction.

### Combinatorial Uniqueness development evidence

- independently propagated activation fields;
- normalized geometric-mean combination rather than additive averaging;
- redundant-coordinate, invalidity, permutation, and leave-one-out controls;
- governed direct legal qualification, contrast, unsupported non-resolution, and epistemic non-promotion;
- explicit stage-local semantic transition with antecedent provenance; and
- preservation of failed flat conjunction as a distinct control rather than relabelling it as transition.

These studies make three composition contracts executable and inspectable over governed synthetic fixtures. Independent construction, useful combinatorial coverage, legal validity, automatic stage-boundary discovery, and scaling across held-out domains are the next evidence layer.

### Semantic Navigation accumulated evidence

- governed dimension/value identities and reversible compact codes;
- immutable many-to-many incidence state with separate representation and compilation snapshots;
- exact candidate-region composition without forced top-1 selection;
- deterministic imputation, remaining partitions, commonality, and next-question selection; and
- flat-scan, per-query reconstruction, warm execution, and amortization accounting.

This seed demonstrates that the operational contracts compose. It motivates the controlled evidence required by the three foundation programmes.

Deterministic replay is one component of auditability. It does not replace provenance completeness, event logging, validation, documented limitations, human oversight, or governance, and it is not by itself an EU AI Act compliance claim.

Bounded development evidence now exists for all four streams. Its maturity differs by programme; the next step is to extend the governed-input mechanics to independently sourced, larger, and held-out cases.

## Semantic representation benchmark

The primary executable benchmark reuses the Words Carry Weight mechanism across three authored ambiguity scenarios. It holds the co-occurrence compiler and Personalized PageRank query strategy fixed while changing semantic identity grounding and query focus. It measures intended-versus-contrast margin, cross-meaning activation, and deterministic replay.

This first version is development evidence that richer semantic identity can improve the usefulness of the same mathematics in these bounded cases. The broader hypothesis for association, synonymy, hierarchy, roles, constraints, and policy-composed relation matrices is the next controlled suite under the same representation-first experimental discipline.

## Retrieval application diagnostic

The 50-document, six-query synthetic fixture is retained as a small downstream diagnostic. It compares lexical overlap, TF-IDF, co-occurrence MML, typed MML, and one fixed multiplicative MML/lexical hybrid. The hybrid makes complementarity reproducible without calibration or parameter search. MML additionally receives supervised concept mappings and negative evidence; the lexical baselines do not. The comparison therefore measures end-to-end treatments, not equal-input algorithms. The diagnostic checks determinism, basic usefulness, and regression; production integrity adds the validation and controls defined below.

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

### Semantic Navigation

1. Independently sourced, reviewed, and frozen 100-, 250-, and 500-entity states.
2. Capability-contribution controls for unqualified values, reconstruction, redundant coordinates, forced ranking, and navigation ablation.
3. Wall-clock, memory, update, and realistic reuse-horizon measurements beside deterministic operation counts.
4. A separately evaluated natural-language-to-governed-query translation layer.

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

Success would show that URI-addressed public knowledge can be compiled once and executed repeatedly by this prototype with preserved identity and provenance. The experiment should compare that reusable artifact with a declared reconstruction-at-use baseline. Its scope is deliberately focused on technical feasibility for the selected mappings, leaving Representation breadth, Combinatorial Uniqueness, wider European coordination, source sufficiency, and social legitimacy to their own research and governance tracks.
