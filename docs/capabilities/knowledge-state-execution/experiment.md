# Experiment 2 — Compile Once. Execute What Is Known.

**Status:** bounded development experiment implemented; confirmatory protocol proposed
**Hypothesis:** Knowledge State Execution
**Working title:** *Knowledge Is State, Not Behaviour Buried in a Model*

This document defines the systematic experiment for MML's second hypothesis. The existing six-fact typed-chain experiment demonstrates the local mechanism. It does not complete the broader reuse, governance, provenance, or efficiency protocol.

The canonical capability definition is [Programme 2 — Knowledge State Execution](README.md).

The underlying architectural mechanism is developed in [The Compiled Knowledge Reuse Proposition](proposition.md).

## Hypothesis

> Once established knowledge is compiled into a governed executable state, its declared consequences can be executed repeatedly without reconstructing equivalent task state from the source at every use.

The primary comparison is **reconstruction at use** versus **compile once, execute many** over the same governed facts and the same declared consequence rule.

### Primary empirical outcome

The primary result is a reuse curve showing that **the one-time construction cost of a governed knowledge state is amortized across repeated correct, inspectable executions while per-query source reconstruction work does not recur**.

```text
number of executions -> cumulative construction + execution work
```

Plot at least:

- cumulative work for per-query source reconstruction;
- cumulative work for compile-once execution, including initial compilation;
- correctness and output stability across the same query sequence; and
- correction cost and affected-result scope after a governed mutation.

The exciting outcome is not merely lower local latency. It is a predictable separation between repeated reconstruction and reusable execution, without losing correctness, provenance, inspectability, correction, or rollback.

A convincing result has four inseparable properties:

1. **Semantic equivalence:** reconstruction and compiled execution implement the same governed facts and declared rule.
2. **Reusable state:** compiled queries do not reread or reconstruct the source knowledge.
3. **Governed evolution:** a source correction produces a new immutable state with bounded, explainable consequences.
4. **Complete accounting:** compilation, storage, execution, validation, correction, and governance costs remain visible.

## Claim Boundary

This experiment tests reusable execution of declared knowledge. It does not establish arbitrary inference, language understanding, autonomous knowledge acquisition, universal efficiency, lower energy consumption, or superiority over language models.

Zero source tokens or bytes per compiled query does not mean zero computation. Index lookup, traversal, validation, policy execution, and rendering remain work.

## Current Development Fixture

The implemented v1 contains six synthetic facts, two questions, and one declared rule:

```text
is-a* -> belongs-to
```

It compares:

- lexical one-hop retrieval;
- per-query source reconstruction; and
- compiled typed traversal.

It also replaces one governed fact, confirms the dependent answer changes, preserves an unrelated answer and the original state, and restores exact behavior without retraining.

This is low-strength development evidence. The case is authored, tiny, non-held-out, and unsuitable for general performance conclusions.

## Confirmatory Fixture Programme

Build a frozen suite of independently authored typed-knowledge cases containing:

- several hierarchy depths;
- branching paths and multiple valid terminals;
- irrelevant facts and plausible distractor paths;
- cycles and explicit cycle policy;
- missing links and unsupported queries;
- scope, temporal validity, and exclusion rules;
- governed mutations with declared dependent and protected-independent queries; and
- provenance records identifying every source assertion.

Include at least two contexts:

1. a synthetic suite where every fact and consequence is fully inspectable; and
2. a narrow public-data slice using appropriately licensed sources and stable external identifiers.

The public-data slice must preserve original source URIs, retrieval metadata, terms, language, and mapping provenance. It tests technical traceability, not institutional legitimacy or ontology completeness.

## Freeze And Hold-Out Protocol

1. Define the supported rule family and executor before authoring confirmatory answers.
2. Separate development/calibration cases from confirmatory cases.
3. Freeze source snapshots, facts, queries, expected consequences, mutation plans, protected-independent cases, and thresholds.
4. Hash the source, compiler, compiled state, executor, and evaluation suite.
5. Execute reconstruction and compiled treatments over identical query sequences.
6. Apply frozen mutations, compile replacement states, inspect effects, and restore the original state.
7. Treat any post-freeze correction as a new development version until another confirmatory freeze.

Expected consequences may be encoded in an evaluation artifact, but must not be embedded as executor branches or compiled shortcuts.

## Required Treatments

### 1. Per-query source reconstruction

For every query:

1. read the governed source snapshot;
2. parse or inspect the relevant facts;
3. construct equivalent temporary task state;
4. execute the declared rule; and
5. return the answer and source path.

### 2. Compiled execution

Once per source snapshot:

1. read and validate the governed source;
2. compile a named immutable state;
3. execute all queries against that state; and
4. return answers and paths without source reconstruction.

### 3. Governed mutation and restoration

1. replace, qualify, add, or remove one governed assertion;
2. compile a new content-addressed state;
3. verify expected dependent changes;
4. verify protected-independent results remain stable;
5. preserve the original state; and
6. reproduce the exact original result after restoration.

### 4. Declared probabilistic baseline

At a later evidence level, ask a named model to derive the same consequences from the same source material. Freeze model identity, provider, configuration, prompt, context, tools, repetitions, and evaluation rules. Report provider tokens separately from MML facts, bytes, operations, and timings.

Lexical retrieval may remain an application control, but a first-hop lookup is not equivalent to reconstructing or executing the declared consequence.

## Query Sequence Design

Measure several reuse horizons:

```text
1, 2, 5, 10, 50, 100, ... queries
```

Use both repeated and distinct queries. Randomize or balance treatment order to limit cache and warm-up bias. Separate cold compilation, warm execution, and repeated identical-query caching; cached answers must not be presented as ordinary compiled traversal.

The query suite must include:

- correct resolvable queries;
- unsupported queries that return `NO_DECLARED_CONSEQUENCE`;
- ambiguous multi-result queries;
- cyclic paths governed by explicit policy; and
- queries affected and unaffected by each mutation.

## Measurements

Keep measurement families separate:

| Family | Measures |
| --- | --- |
| Correctness | Exact answer, accepted answer set, unsupported rejection, false consequence rate |
| Source work | Reads, bytes, facts, and declared lexical tokens processed |
| Compilation work | Validation, facts parsed, index entries built, bytes stored, algorithmic operations |
| Execution work | Lookups, edges traversed, rules applied, validation operations |
| Wall-clock | Cold compile, warm query, reconstruction query, mutation, restoration |
| State integrity | Content identity, deterministic replay, immutability, rollback equality |
| Inspectability | Complete path to governing facts and source provenance |
| Evolution | Changed results, protected-independent stability, correction effort, blast radius |
| Resource use | Memory, storage, CPU counters, and energy only where directly instrumented |
| Governance | Authoring, review, correction, publication, and provenance effort |

Report cumulative curves rather than only per-query averages:

```text
W_reconstruct(n) = n * (source read + parse + temporary construction + execution)

W_compiled(n) = one-time compile + n * compiled execution
```

The observed break-even point is descriptive for the named fixture, implementation, and machine. It is not a universal constant.

## Correctness And Refusal Contract

Compiled execution and reconstruction must satisfy the same declared consequence contract.

Return:

```text
NO_DECLARED_CONSEQUENCE
```

when the frozen state and supported rule family do not justify an answer. Preserve separate reasons such as:

```text
MISSING_LINK
AMBIGUOUS_CONSEQUENCE
CYCLE_POLICY_BLOCK
OUT_OF_SCOPE
TEMPORALLY_INAPPLICABLE
EXCLUDED_ROUTE
```

The executor must not fill missing knowledge through lexical resemblance or unstated common sense.

## Ablations And Controls

At minimum:

- disable compilation and reconstruct per query;
- retain serialization but remove the executable index;
- vary query count while holding facts fixed;
- vary fact count and irrelevant-fact density while holding query count fixed;
- remove provenance and verify that inspectability, not answer correctness, is what changes;
- mutate a path fact and a deliberately unrelated fact;
- rebuild the same source twice and compare content identities;
- restore the original source and require exact state and result recovery; and
- compare sparse and dense implementations only as separately named execution treatments.

## Acceptance Criteria

Exact thresholds must be frozen before confirmatory execution. The bounded hypothesis receives support only if:

1. reconstruction and compiled execution achieve equivalent correctness on resolvable and unsupported cases;
2. compiled queries perform no governed source reread or equivalent task-state reconstruction;
3. cumulative compiled work exhibits the preregistered reuse advantage after a reported break-even horizon;
4. every result has a complete inspectable path to governed source assertions;
5. deterministic recompilation produces the same content identity and results;
6. governed mutation changes declared dependent results without changing protected-independent results;
7. restoration reproduces the exact original state and outputs; and
8. construction, storage, validation, governance, and execution costs remain separately reported.

The hypothesis is weakened if compiled state merely hides repeated reconstruction, loses provenance, cannot reject unsupported queries, has uncontrolled correction blast radius, or offers no material reuse benefit after full accounting.

## Threats To Validity And Controls

| Threat | Control |
| --- | --- |
| Reconstruction baseline performs unnecessary work | Implement the simplest equivalent declared reconstruction and inspect its operations |
| Compiled treatment embeds expected answers | Store governed facts and generic indexes, not query-specific answer shortcuts |
| OS caches make compiled execution look better | Balance order and separate cold, warm, and cached treatments |
| Tiny fixture creates meaningless break-even | Report scale curves and avoid general performance claims |
| Different treatments execute different rules | Shared consequence contract and paired correctness tests |
| Zero source reads is presented as zero work | Separate source, algorithmic, timing, memory, and energy measures |
| Mutation test changes only the expected answer | Protected-independent queries and explicit blast-radius checks |
| Determinism is mistaken for governance | Report provenance, review, validation, correction, and publication separately |
| Model comparison uses incomparable accounting | Freeze inputs and report each measurement family without token equivalence claims |

## Required Artifacts

Implementation should produce versioned machine-readable artifacts for:

- governed source snapshots and licenses;
- source-to-fact mappings and provenance;
- frozen queries, consequences, and refusal labels;
- compiler, rule-family, and executor configuration;
- content-addressed compiled states;
- reconstruction and compiled execution traces;
- per-operation and cumulative work measurements;
- mutation and restoration manifests;
- deterministic replay evidence;
- probabilistic-baseline configuration where used; and
- an OSCARC report with claims ladder and evidence boundary.

## Intended Evidence

A successful confirmatory result would show that one bounded family of established knowledge can be compiled into governed state and executed repeatedly with preserved correctness, provenance, inspectability, correction, and rollback, while avoiding repeated source reconstruction. It would not establish arbitrary reasoning, universal efficiency, lower energy use, or the feasibility of a society-wide knowledge commons.
