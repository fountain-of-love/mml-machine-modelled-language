# LLM-to-MML Conversion Boundary

## Architectural Identity

Machine Modelled Language (MML) is the mathematical compilation and execution
layer between probabilistic language capability and a wider AI application.

Its specific architectural question is:

> **Can an LLM progressively convert recurring probabilistic tasks into governed deterministic operations without reducing its ability to handle genuinely novel tasks?**

MML does not attempt to become another language model. It does not own open-ended
language interpretation, discovery, user interaction, workflow orchestration,
tool execution, or the whole application that decides when to invoke it. It
receives governed semantic structure and a declared execution policy, compiles
them into a mathematical operator, and executes that operator reproducibly.

```text
LLM or other probabilistic system
  -> candidate task structure or operator proposal
  -> CML / governance boundary
  -> accepted governed semantic state and policy
  -> MML compilation
  -> deterministic mathematical operator
  -> deterministic execution and provenance
  -> application or probabilistic system
```

The boundary is not a claim that every interaction should become deterministic.
It is a claim that recurring, sufficiently understood, and governable work can
move into a more inspectable execution regime while novel or unsupported work
remains available to probabilistic exploration.

## Layer Ownership

### LLM and probabilistic discovery

The probabilistic layer may:

- interpret raw language;
- identify possible recurring task families;
- propose concepts, aliases, roles, relations, constraints, or policies;
- translate an interaction into a candidate governed query;
- suggest an operator structure from examples; and
- render deterministic results back into natural language.

The probabilistic layer does not directly publish executable MML state. Its
output is a proposal with uncertainty, provenance, and a declared intended
task contract.

### CML and governance

The Common Language Model (CML) is the shared semantic contract for the
structure MML consumes. It defines or carries:

- stable concept and sense identities;
- semantic roles and relation types;
- aliases and normalization rules;
- source evidence and provenance;
- constraints, exclusions, and validity conditions;
- maturity and review state; and
- competing or superseded assertions.

Governance decides whether a proposal has sufficient identity, evidence, scope,
and review status to become accepted semantic state. This may involve people,
institutions, source policies, or a separate review system. Governance is a
prerequisite of MML execution, not a hidden operation inside the numerical
kernel.

### MML compilation and execution

MML owns the transformation:

```text
accepted semantic state + execution policy
  -> relation-specific structures
  -> policy-weighted mathematical operator
  -> persistent executable state
  -> deterministic result
```

MML is responsible for:

- validating the operator input contract;
- preserving relation identity during compilation;
- applying explicit, versioned policy coefficients;
- normalizing operators according to their execution contract;
- producing immutable, content-addressed executable state;
- executing declared mathematical strategies;
- exposing operator and source provenance;
- preserving refusal and ambiguity instead of inventing unsupported answers;
- supporting deterministic replay; and
- detecting regressions when an operator or source snapshot changes.

MML is not responsible for deciding whether an interaction is recurring in the
first place. It can expose the measurements needed for that decision, but the
recurrence detector belongs to the discovery or application layer.

### SOS and application infrastructure

The Semantic Operating System (SOS) is a broader proposed stack. It may own:

- interaction routing;
- novelty detection and escalation;
- LLM selection and prompting;
- human approval interfaces;
- workflow and task orchestration;
- persistence beyond the operator artifact;
- access control and operational monitoring;
- tool invocation and external side effects; and
- user-facing applications.

SOS can call MML and measure its contribution. SOS must not be confused with
the MML mathematical kernel.

## The Conversion Contract

The LLM-to-MML transition should be represented as a typed proposal rather than
an implicit change in model behaviour.

```text
OperatorCandidate
  candidate_id
  task_family
  input_schema
  output_schema
  governed_entities
  relation_records
  policy
  source_evidence
  validation_cases
  limitations
```

The candidate is not executable merely because it is syntactically valid. It
must pass deterministic validation and an explicit governance decision.

```text
PROPOSED
  -> SCHEMA_VALID
  -> SEMANTICALLY_GROUNDED
  -> POLICY_VALID
  -> VALIDATED
  -> APPROVED
  -> COMPILED
  -> ACTIVE
```

Any state may terminate in `REJECTED`, `UNSUPPORTED`, or `SUPERSEDED`. The
transition history belongs to the surrounding governance and evidence system;
the compiled artifact records the accepted source snapshot and policy identity.

### Required proposal checks

Before compilation, the candidate must establish:

1. every referenced concept has a governed identity;
2. every relation has a supported type, direction, endpoint, and weight;
3. every durable assertion has source evidence;
4. every policy coefficient has a versioned policy identity;
5. the input and output contracts are complete;
6. unsupported, ambiguous, and invalid cases have declared outcomes;
7. validation cases are separate from the construction records where required;
8. the candidate does not silently overwrite an active operator;
9. the compiled result can be replayed from its source snapshot; and
10. existing regression cases remain within their declared contract.

The checks are deliberately conservative. A failed check is useful information:
it indicates that the probabilistic proposal has not yet become governed
mathematical knowledge.

## Mathematical Operator Identity

The executable identity of an MML operator is the combination of:

```text
governed source snapshot
  + relation-layer definitions
  + policy coefficients and policy version
  + compilation algorithm version
  + numerical parameters
  + execution contract
```

Changing any of these should either produce a new operator identity or be
explicitly proven equivalent. An operator snapshot must therefore be sufficient
to answer:

- which semantic records were compiled;
- which relation layers were included;
- which coefficients were applied;
- which algorithm and parameters were used;
- which output contract was executed; and
- whether the result can be reproduced.

The current [compiled semantic operator](capabilities/knowledge-state-execution/semantic-operator-design.md)
implements the first bounded form of this identity. It preserves
`supports`, `requires`, and `qualifies` as sparse layers, applies a versioned
policy, excludes contradictions from positive propagation, and creates an
immutable snapshot.

## What MML Can Guarantee

For an accepted operator and a declared execution contract, MML can aim to
guarantee:

- deterministic execution for identical inputs and state;
- stable operator identity;
- explicit relation and policy provenance;
- reproducible compilation;
- bounded output schemas;
- explicit unsupported and ambiguous outcomes;
- immutable source-state preservation;
- correction through replacement and recompilation; and
- regression detection against declared validation cases.

These are execution guarantees. They do not automatically establish that the
governed concepts are true, that a policy is substantively correct, or that an
operator is appropriate for every future interaction.

## What MML Must Not Claim

MML must not claim that:

- a valid operator is a complete model of a domain;
- a high activation score is a probability or a proof;
- a compiled relation is causal merely because it propagates;
- deterministic replay implies semantic correctness;
- operator coverage implies general intelligence;
- a refusal is a failure when the governed state is insufficient; or
- a cheaper operator preserves the capabilities required for novel work.

The last point is central. MML is valuable only if operator extraction reduces
repeated probabilistic reconstruction without collapsing the system's ability
to recognize and handle cases outside the operator's validated scope.

## Measurement Boundary

### MML-native measurements

These belong to the operator and compiler experiments:

- compilation correctness;
- deterministic execution error rate;
- exact or contract-equivalent replay rate;
- operator coverage over governed task families;
- false operator creation;
- regression rate after recompilation;
- compilation cost and latency;
- execution cost and latency;
- persistent state size;
- refusal and ambiguity preservation; and
- capability extraction rate from a frozen proposal set.

### System-level measurements

These belong to an LLM-to-MML integration or SOS experiment:

- percentage of eligible interactions routed to MML;
- novelty detection accuracy;
- human approval time and correction burden;
- end-to-end cost and latency change;
- probabilistic fallback frequency;
- user-visible error rate; and
- retained performance on genuinely novel tasks.

The system-level measures may use MML telemetry, but they must not be presented
as properties of the mathematical operator alone.

## Research Protocol

The first LLM-to-MML experiment should use frozen recorded proposals rather than
a live model integration. This isolates the compilation question.

```text
recorded probabilistic proposal
  -> schema and identity validation
  -> policy validation
  -> deterministic compilation
  -> repeated execution
  -> regression and refusal checks
  -> accept, reject, or unsupported result
```

The fixture should contain:

- recurring task families suitable for extraction;
- proposals that are syntactically valid but semantically incomplete;
- proposals with incorrect or unsupported relations;
- genuinely novel tasks that should not receive an operator;
- existing active operators exposed to regression probes; and
- independent replay cases authored after the operator snapshot is frozen.

The baseline should compare repeated probabilistic handling with the complete
MML lifecycle:

```text
probabilistic baseline
  versus
proposal cost + governance cost + compilation cost
  + storage cost + deterministic execution cost
```

A one-query benchmark is insufficient. Results must be reported across reuse
horizons, update frequencies, task families, operator versions, and novel-task
controls.

## Repository Mapping

The intended implementation boundary is:

```text
src/semantic_representation/
  governed identities, coordinates, grounding, and activation primitives

src/knowledge_state_execution/
  compilation, immutable executable state, snapshots, replay, and correction

src/combinatorial_uniqueness/
  mathematical field composition and candidate-region operations

src/semantic_navigation/
  downstream use of represented and compiled state for exact retrieval and ambiguity

experiments/llm_to_mml/
  recorded proposals, extraction controls, recurrence labels, and conversion metrics

docs/sos/
  downstream architecture for routing, persistence, governance, rendering, and applications
```

The MML kernel should not import `experiments`, an LLM SDK, a UI framework, a
workflow engine, or an external action client. Experiments and applications may
depend on the kernel through explicit contracts.

## Architectural Decision

MML is therefore neither the LLM nor the complete AI system. It is the governed
mathematical middle layer that turns accepted semantic structure into reusable
deterministic operators.

The LLM supplies probabilistic proposal and language capability. CML supplies
the semantic vocabulary and governance-shaped data contract. MML supplies
compilation and mathematical execution. SOS supplies the surrounding routing,
human, persistence, and application capabilities.

The research success condition is not universal conversion. It is selective
conversion: recurring tasks should become more reproducible and operationally
efficient after governance, while unsupported and novel tasks remain visible as
novel and continue through probabilistic handling.
