# MML Scaling Challenges

This note separates three scaling questions that are easy to conflate when evaluating Machine Modelled Language (MML):

1. computational scaling;
2. semantic scaling; and
3. governance scaling.

The distinction matters because a result in one category does not establish a result in the others. Fast execution does not prove useful semantic coverage. A large semantic basis does not prove maintainable governance. A strong governance process does not prove acceptable runtime cost. Each dimension needs its own measurements and falsification criteria.

## Architectural Context

MML should not be read as claiming that it must interpret raw language, discover all concepts, govern their validity, and execute them through one mechanism. The proposed division of responsibility is closer to:

```text
LLM, CML, expert, source, and community discovery
    -> candidate semantic structure
    -> governance, authority, provenance, voting, and evidence review
    -> stable CML knowledge
    -> MML compilation
    -> deterministic execution
```

This division separates knowledge acquisition from knowledge execution. MML's current implemented role is the compilation and execution side: making accepted semantic structure addressable, reusable, inspectable, and executable. The construction and governance of that structure are upstream responsibilities, even if language models or MML-derived diagnostics assist them.

## 1. Computational Scaling

Computational scaling asks how execution cost grows as the executable representation grows.

The relevant variables include:

- number of concepts or identities;
- number of relations;
- number of relation types or semantic dimensions;
- density or sparsity of the compiled operators;
- number and width of query constraints;
- number of queries;
- update frequency;
- snapshot and rollback requirements; and
- explanation or provenance depth.

For matrix or vector execution, this category should be comparatively straightforward to characterize. A dense `N x N` transition matrix has different cost behavior from a sparse operator. A single-vector activation has different cost behavior from multi-field composition. A converged PageRank-style strategy has different cost behavior from a fixed-step local propagation strategy. Relation-specific operators add another axis: execution may either compose a task-specific operator before activation or retain layer identity during propagation.

The research task is therefore not only to report runtime. It is to bind runtime and resource use to the declared execution contract:

```text
representation size
    -> compiled operator size
    -> activation or traversal work
    -> query result
    -> optional explanation and provenance work
```

Useful measurements include asymptotic cost, wall-clock latency, memory, storage, update cost, snapshot cost, and energy where available. These measurements should distinguish compile-time cost from query-time cost, because a compile-once model can be expensive to build yet inexpensive to reuse.

Open computational questions include:

- When do sparse operators become necessary?
- How does multi-field soft intersection scale with query width?
- How do relation-specific operators change memory and execution cost?
- What is the cost of producing explanations compared with producing only scores?
- What reuse horizon amortizes compilation for a given domain?

## 2. Semantic Scaling

Semantic scaling is the central open question behind the Combinatorial Uniqueness proposition.

It asks how many useful new meanings can be constructed from a reusable semantic basis without explicitly enumerating every possible meaning in advance. If a system contains 100 meaningful dimensions, the research question is not whether it can store 100 dimensions. The question is whether combinations of those dimensions can create a much larger useful semantic space while still preserving specificity, refusal, and interpretability.

This is distinct from ordinary graph connectivity. The proposition is not:

```text
everything is a graph, therefore everything connects
```

It is closer to:

```text
find reusable semantic dimensions
    -> preserve their type, scope, and evidence
    -> translate them across contexts only where valid
    -> compose them at query time
    -> obtain specificity without encoding every combination as a primitive
```

The Semantic Seed Vault illustrates why this is difficult. Roles such as `capacity`, `activation`, `boundary`, `substrate`, `gain`, and `storage` can recur across scientific domains. But those roles do not make mechanics, thermodynamics, acoustics, electromagnetism, and hydraulics identical. A scalable semantic basis must preserve both the reusable role and the domain-specific realization.

Semantic scaling therefore depends on several conditions:

- dimensions must be stable enough to reuse;
- their scope must be explicit;
- their type must survive translation between contexts;
- invalid or unsupported combinations must be rejected;
- successful combinations must add specificity rather than merely echo broad association;
- the system must avoid hidden bespoke primitives for complete query combinations; and
- the basis must cover new useful regions without requiring every region to be pre-authored.

Possible measurements include:

- number of primitive dimensions;
- number of valid composed coordinates tested;
- proportion of useful held-out combinations resolved;
- proportion of unsupported or invalid combinations refused;
- specificity gain from single dimensions to pairs and full combinations;
- redundancy and ablation effects;
- hard-negative intrusion;
- coverage of independently authored probes after a state freeze; and
- construction cost per useful new composed coordinate.

The current repository has development evidence that soft intersection, direct qualification, refusal, and explicit stage-local transition are executable in authored fixtures. It does not yet establish semantic scaling in the stronger sense: useful held-out coverage from a reusable basis across domains.

## 3. Governance Scaling

Governance scaling asks how semantic correctness is maintained as the knowledge base grows.

This is likely to be the limiting practical question. Semantic roles and relations are only useful if their identities, evidence, scope, and maturity remain trustworthy enough for the tasks that execute them. The upstream construction pipeline is therefore central:

```text
LLM or expert proposal
    -> evidence attachment
    -> authority, voting, or review process
    -> provenance and scope declaration
    -> accepted CML record
    -> compiled MML artifact
```

Governance may involve domain experts, public authorities, institutional review, community voting, automated consistency checks, provenance ledgers, contradiction tracking, and maturity labels. Different domains will require different combinations. A scientific claim, a legal doctrine record, a lexical alias, and a user-interface taxonomy do not need the same authority model.

Importantly, governance does not necessarily need to scale linearly with execution workload. Establishing one reusable semantic role may require significant effort:

```text
capacity means X
    under semantic role Y
    with evidence Z
    within scope S
```

Once accepted, that governed record can be reused by many compiled artifacts and by thousands or millions of subsequent computations. This is analogous to the Knowledge State Execution distinction: acquisition and validation can be expensive, while execution over accepted state can be comparatively cheap.

Governance scaling should therefore be measured separately from runtime scaling. Relevant measurements include:

- time and effort to admit or revise a semantic record;
- reviewer or authority requirements by record type;
- provenance completeness;
- contradiction and concern resolution rate;
- rollback and correction cost;
- impact radius of a changed record;
- stale or superseded record detection;
- rate of downstream reuse per governed record; and
- governance cost per useful execution or per useful composed coordinate.

Open governance questions include:

- Which records require expert authority, and which can rely on volume voting or weaker review?
- How are conflicting authorities represented without collapsing them into one score?
- How are scope, jurisdiction, domain, regime, and time validity preserved?
- How are LLM-proposed structures prevented from becoming accepted knowledge without evidence?
- How does the system expose uncertainty without preventing reuse where uncertainty is acceptable?

## Coupling Between The Three Scaling Questions

The three kinds of scaling interact but should remain analytically separate.

Computational improvements can make more queries affordable, but they do not create a valid semantic basis. Semantic composition can increase the number of useful query-time coordinates, but only if governance maintains stable roles and valid scope. Governance can make knowledge reusable, but governance effort may dominate the cost of building a domain.

A complete scaling study should therefore report at least three curves:

| Scaling type | Primary question | Example unit |
| --- | --- | --- |
| Computational | How does execution cost grow? | latency, memory, energy, compile cost, query cost |
| Semantic | How many useful meanings can be composed from a basis? | held-out valid combinations, specificity gain, refusal accuracy |
| Governance | How is correctness maintained as the basis grows? | review effort, provenance completeness, reuse per governed record |

The practical hypothesis is not that any one curve is free. It is that governed knowledge acquisition may be amortized across repeated deterministic execution, and that a reusable semantic basis may cover more useful meanings than explicit enumeration alone. Both claims remain empirical.

## Evidence Boundary

This note describes scaling challenges and measurement categories. It does not establish that MML currently scales computationally, semantically, or institutionally. The current repository provides bounded mechanism evidence and development benchmarks. Stronger scaling claims require sparse execution studies, held-out semantic-composition suites, and governance experiments with explicit authority, provenance, correction, and reuse accounting.
