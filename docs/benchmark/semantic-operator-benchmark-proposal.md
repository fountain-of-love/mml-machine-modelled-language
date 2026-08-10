# Semantic Representation Benchmark Proposal

## Purpose

This benchmark is designed around the central intention of Machine Modelled Language:

> **Richer meaning representation can make established mathematics produce more useful results.**

MML does not begin with the claim that PageRank, matrix multiplication, normalization, diffusion, or weighted operator composition are new. It asks whether these established mathematical structures become more useful when the representation they execute contains more explicit meaning.

Association, synonymy, hierarchy, opposition, part/whole, causality, role correspondence, and temporal relation are examples of representational dimensions. They are not the definition of richness and should not become a mandatory universal ontology. A representation is richer when it makes distinctions required by a task explicit, addressable, governed, and executable.

The benchmark must therefore evaluate the consequence of representational enrichment. It must not reduce the project to document retrieval, reward extra algorithmic complexity, or treat a larger relation vocabulary as automatically better.

## Primary Research Question

Given the same source observations, query, task, and established execution method:

> Does a governed representation containing task-relevant semantic distinctions produce results that are more useful, more discriminating, and more attributable than a poorer representation?

The benchmark should also ask four supporting questions:

1. **Necessity:** Does adding a missing semantic distinction enable a result that the poorer representation cannot express reliably?
2. **Specificity:** Does the enrichment improve the intended behavior without creating unrelated gains or semantic leakage?
3. **Policy responsiveness:** When declared relation weights change, does the result change in the predicted direction?
4. **Stewardship:** Can the result be reproduced, explained, updated, and restored from governed inputs?

## What Counts as Validation

The project intention receives support when all of the following hold:

- the mathematics remains fixed or belongs to a small, predeclared family of established operators;
- the richer and poorer treatments differ only in a documented semantic enrichment or policy;
- the richer representation improves task-relevant outcomes on unseen probes;
- the direction of change was declared before execution;
- ablation removes the gain when the relevant semantic dimension is removed;
- unrelated semantic dimensions do not receive unexplained gains;
- the execution remains deterministic and attributable to governed inputs;
- the benefit is material relative to the additional construction and execution cost.

An improvement in a single aggregate ranking metric is not sufficient. The benchmark must show that the intended semantic distinction caused an interpretable change.

## What Would Falsify or Weaken the Intention

The benchmark should report negative results rather than protect the hypothesis. Evidence against the project direction includes:

- richer representations perform no better than association-only representations on tasks that require the added distinctions;
- improvements disappear on held-out probes or independently authored cases;
- unrelated relation families produce the same improvement as the supposedly relevant one;
- useful results require increasingly elaborate algorithms rather than better representation;
- policy coefficients have unstable, discontinuous, or uninterpretable effects;
- added semantics increase confident errors or cross-context leakage;
- the construction and governance cost outweigh the demonstrated benefit;
- explanations cannot identify which semantic records and policy decisions affected the result;
- deterministic replay, update, or rollback fails.

These outcomes may reject one representation, task policy, or compilation method without rejecting every possible MML. Repeated failure across independently designed semantic tasks would weaken the broader proposition.

## Experimental Method: Hold Mathematics Constant

The core experiment is a controlled representation ladder. Each case begins with the same observations and uses the same query strategy, normalization, propagation horizon, and evaluation probes. One semantic distinction is added at a time.

```text
same observations + same query + same mathematics
    -> representation R0
    -> result F0

same observations + one governed semantic enrichment
    -> representation R1
    -> result F1

compare F1 with F0 against a preregistered behavioral expectation
```

The first reference operator should be the repository's existing Personalized PageRank strategy or the bounded propagation strategy, selected before results are examined. Later benchmark versions may include other established operators, but every operator must run across the same representation treatments. This separates the effect of representation from the effect of algorithm choice.

## Representation Ladder

The ladder is experimental, not a maturity score. A higher rung is useful only when its added semantics are relevant to the task.

| Treatment | Representation | Question isolated |
| --- | --- | --- |
| `R0 association` | Surface identities with statistical association or co-occurrence | What does proximity alone produce? |
| `R1 identity` | Distinct governed senses and aliases | Does addressable identity reduce ambiguity? |
| `R2 typed relation` | One task-relevant relation family separated from association | Does relation meaning change the field usefully? |
| `R3 role` | Concepts assigned governed semantic roles | Can structural correspondence be recognized beyond shared vocabulary? |
| `R4 constraint` | Direction, scope, opposition, temporal validity, or applicability | Can the field reject routes that mere connectivity would admit? |
| `R5 policy composition` | Several relation matrices composed with declared coefficients | Can task policy reshape the field predictably? |

Not every benchmark case must traverse every treatment. A sense-disambiguation case may stop at `R1`; a cross-domain structural comparison may begin to differentiate only at `R3`.

## Benchmark Suites

### Suite A: Identity and ambiguity

This suite evolves the existing `bank` demonstration without turning it into the whole benchmark.

- **Poor representation:** `bank` is one identity connected to both river and financial contexts.
- **Enrichment:** `bank_river` and `bank_financial` become distinct governed identities with declared aliases.
- **Fixed mathematics:** the same transition compilation and Personalized PageRank query strategy.
- **Expected result:** each enriched identity concentrates more activation in its intended context and less in the contrast context.

This suite tests the minimal claim that better semantic identity can make unchanged mathematics produce a more useful field.

### Suite B: Relation meaning

This suite uses matched structures where association alone is insufficient. Each case changes one relation family while preserving endpoints and overall edge count where possible.

Example contrasts include:

- synonym versus opposition;
- hierarchy versus part/whole;
- cause versus temporal succession;
- association versus role correspondence.

A query should produce different expected fields depending on the declared relation. If permuting relation labels has no effect, the representation is not executing their meaning.

### Suite C: Semantic roles across domains

This suite tests the CML-inspired roles such as `capacity`, `activation`, `boundary`, `substrate`, `gain`, and `storage`.

Matched systems from different domains should use different vocabulary and physical quantities while sharing a governed structural pattern. The benchmark asks whether role-aware representation can surface the structural correspondence without collapsing the systems into false equivalence.

Each case must contain:

- a genuine role-aligned counterpart;
- a vocabulary-similar but structurally incorrect hard negative;
- a structurally partial counterpart;
- at least one explicit non-mapping or scope limitation.

The expected result is not “the domains are the same.” It is that the operator assigns stronger support to the declared structural correspondence while retaining domain boundaries and negative mappings.

### Suite D: Task-policy composition

This suite evaluates a family of matrices such as association `A`, synonymy `S`, hierarchy `H`, opposition `O`, part/whole `P`, causality `C`, role correspondence `R`, and temporal relation `T`.

A task-specific operator may take the form:

```text
M = alpha*A + beta*S + gamma*H + delta*P + epsilon*C + zeta*R - eta*O
```

The benchmark should define at least two preregistered policies over the same semantic sources. For example:

- a lexical interpretation policy emphasizing identity, synonymy, hierarchy, and opposition;
- a structural analogy policy emphasizing role correspondence, causality, boundary, and part/whole relations.

The expected field changes must be declared before running the cases. Coefficient sweeps are sensitivity analyses, not tuning searches. The benchmark should prefer broad stable regions over one optimized coefficient point.

### Suite E: Evolution, observation, and restoration

This suite tests whether useful semantic behavior remains governable.

For one bounded source change:

1. compile the baseline representation and record its identity;
2. execute the probe and record its activation field;
3. add, qualify, or remove one governed semantic assertion;
4. rebuild and execute again;
5. identify the expected and observed consequences;
6. restore the original sources;
7. reproduce the exact baseline representation and result.

When the event sink exists, the suite must additionally confirm that construction, execution, update, snapshot, and rollback events correspond to the same source and execution identities. Attaching or removing the observer must not change numerical results.

## Case Format

Each benchmark case should be a declarative artifact rather than executable logic containing its own answer. A case should record:

```json
{
  "case_id": "role-capacity-001",
  "intention": "role correspondence distinguishes structural match from lexical match",
  "source_observations": [],
  "representations": ["R0", "R3"],
  "fixed_operator": "personalized-pagerank-v1",
  "query": {},
  "expected_direction": {},
  "hard_negatives": [],
  "non_claims": [],
  "provenance": {},
  "authoring_status": "development|held-out|independent"
}
```

Expected outcomes should specify order, direction, separation, invariants, or forbidden behavior rather than exact floating-point values wherever possible. Exact reference arrays remain useful for deterministic regression but should not define semantic success by themselves.

## Evaluation Dimensions

The benchmark should report a profile instead of collapsing everything into one score.

### 1. Intended-field support

How much activation reaches the concepts or roles declared relevant to the query?

Possible measures:

- relevant field mass;
- target-versus-contrast margin;
- rank of the first intended identity;
- pairwise ordering accuracy over preregistered expectations.

### 2. Semantic leakage

How much activation reaches a confusable but inappropriate field?

Possible measures:

- contrast field mass;
- hard-negative intrusion;
- opposition or exclusion violations;
- cross-sense leakage ratio.

### 3. Enrichment effect

Does adding the relevant semantic distinction improve the intended outcome relative to the poorer representation?

Report paired deltas for every case:

```text
Delta = behavior(richer representation) - behavior(poorer representation)
```

The direction of `Delta` must have been declared before execution.

### 4. Relation specificity

Does the gain disappear when the relevant relation family is removed, zero-weighted, or label-permuted? Do irrelevant relation families leave the behavior substantially unchanged?

This is the central ablation against the claim that “more metadata” alone explains improvement.

### 5. Policy sensitivity and stability

Do coefficient changes move results monotonically or predictably where expected? Are conclusions stable across a reasonable policy region, or do they depend on a fragile tuned value?

### 6. Attribution and traceability

Can every material difference be connected to:

- governed semantic records;
- the compiled relation matrix or matrices;
- declared policy coefficients;
- the operator and normalization version;
- the query and resulting representation identity?

Path display is useful evidence but is not automatically a complete causal decomposition.

### 7. Reproducibility and integrity

The same normalized sources, policies, operator, and settings must produce identical artifacts and results within the declared numerical contract. Invalid identities, relations, evidence references, or coefficient policies must fail explicitly.

### 8. Cost of richness

Report what the enrichment costs:

- number of governed identities and relation records;
- authoring and review effort;
- matrix count, non-zero entries, and memory;
- compilation and execution time;
- event volume when observation is enabled.

The hypothesis concerns usefulness, not free complexity. Benefit should be judged against representational and operational cost.

## Controls and Ablations

Every semantic enrichment should be tested against controls that make accidental success harder:

- **identity-preserving label shuffle:** changes labels without changing semantic identity;
- **relation-label permutation:** preserves topology but assigns incorrect relation meaning;
- **edge-count control:** gives the poorer representation comparable connectivity without the semantic distinction;
- **irrelevant-layer control:** adds an unrelated relation matrix;
- **zero-coefficient control:** includes a matrix but prevents it from affecting the operator;
- **policy swap:** runs the same representation under a policy intended for a different task;
- **hard negatives:** include vocabulary similarity without structural fit and structural partial matches without full applicability;
- **observer control:** event sink attached versus absent must yield the same activation.

These controls distinguish richer meaning from simply adding edges, parameters, or computation.

## Dataset Governance

The benchmark should mature through three evidence levels:

1. **Development cases:** small authored fixtures used to build and debug the mechanism.
2. **Held-out cases:** frozen before implementation changes and evaluated only after the operator contract is fixed.
3. **Independent cases:** authored and judged by domain contributors who did not implement the representation or coefficients.

Every case needs provenance, versioned expectations, review state, and an explicit evidence boundary. Scientific role cases need domain review and must retain failed mappings and counterexamples. Benchmark inputs, expected directions, implementation, and results should have separate content identities so a result cannot silently rewrite its own test.

## Reporting

Benchmark results should be interpreted through the [OSCARC methodology](oscarc-methodology.md): Objective Observation, Standard, Context and chronology, Actions or mechanisms, Result, and Comparative conformity judgment, followed by a recommendation. This prevents a results table from forcing readers to infer the hypothesis, controls, chronology, evidence strength, and limitations for themselves.

Each suite report should include a neutral baseline observation, the declared standard, experimental chronology, exact representational intervention, paired measurements, a local conformity judgment, a separate evidence-strength rating, and a next step tied to the principal evidence gap.

The primary report should lead with the research question and a representation-effect table:

| Suite | Enrichment | Fixed mathematics | Expected effect | Observed effect | Specificity control | Cost | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |

Verdicts should be local:

- `SUPPORTED` — intended improvement reproduced and survived controls;
- `MIXED` — some intended behavior improved but specificity, stability, or cost remains unresolved;
- `NOT SUPPORTED` — no material improvement or controls explain the effect;
- `INSUFFICIENT EVIDENCE` — too few, non-independent, or invalid cases.

There should be no universal “MML wins” score. A suite can support identity enrichment while rejecting a proposed causal representation or coefficient policy.

## Relationship to the Existing Retrieval Diagnostic

The current retrieval benchmark remains useful as an application regression. It tests whether the present prototype continues to rank its authored polysemy and GDPR documents deterministically beside lexical baselines.

It should not be the primary benchmark for this project because it combines representation, query engineering, document scoring, and retrieval judgments into one downstream outcome. It cannot isolate whether richer meaning representation made the established mathematics more useful.

Under this proposal, retrieval becomes one optional application suite fed by a validated semantic operator. TF-IDF and lexical overlap remain contextual baselines for that application, not the definition of MML success.

## Recommended First Implementation

The identity-focused first version is now implemented in [`benchmark.py`](../../benchmark.py), with its report in [Semantic Representation Benchmark v1](results/semantic-representation-v1.md). Its experiment adapter reuses the operational `WordsCarryWeightFlow` across `bank`, `bass`, and `crane` scenarios while keeping the compiler and Personalized PageRank strategy fixed. The remaining steps below describe its intended evolution.

The first version should remain small and build directly on the current code:

1. Convert the existing ambiguous/enriched `bank` experiment into the `R0 association` versus `R1 identity` case format.
2. Add one matched `R1 identity` versus `R2 typed relation` suite with topology-preserving relation-label controls.
3. Add one bounded CML role suite using `capacity`, `activation`, `boundary`, `substrate`, `gain`, and `storage`, including a lexical hard negative and an explicit non-mapping.
4. Implement paired representation-effect metrics, leakage metrics, determinism checks, and ablations.
5. Freeze a small held-out second set before changing operator composition.
6. Add policy-composition and event-sink suites only when those implementation contracts exist.

This sequence tests the essence before expanding the mechanism:

> Does making meaning more explicit allow the same well-understood mathematics to produce a result that is more useful for the declared task?
