# LLM Concept Inventory Exploration

## Exploration Seed

Large language models appear to carry a vast latent field of concepts and concept relations. Open-weight models make the learned parameters inspectable, but those parameters should not be treated as a direct concept graph.

A model weight is not usually an explicit statement such as:

```text
concept A --relation(weight)--> concept B
```

The useful hypothesis is more careful:

```text
model weights and activations
  -> latent conceptual structure
  -> probes and observations
  -> candidate concepts
  -> candidate relations
  -> governed concept inventory
```

The system should therefore inventory concepts by observation, not by assuming that a readable graph already exists inside the model.

## Core Questions

1. Can candidate concepts be extracted from an LLM through repeatable probes?
2. Can candidate relations between two concepts be discovered by querying the model without pre-assuming the relation type?
3. Can the resulting relation be stored with enough provenance, confidence, and validation evidence to remain auditable?
4. Can model-derived concept inventories become useful inputs for MML semantic representation experiments?

## Concepts

A concept inventory should treat concepts as governed records rather than loose strings.

Minimal concept fields:

- `id`: stable internal identifier
- `label`: human-readable name
- `aliases`: alternate surface forms
- `description`: short meaning boundary
- `source`: model, prompt, embedding cluster, activation probe, or external seed
- `provenance`: raw observations that produced the concept
- `maturity`: candidate, reviewed, confirmed, deprecated

Concept extraction methods may include:

- direct model prompting;
- embedding-neighborhood exploration;
- vocabulary or token-neighborhood analysis;
- activation or feature probing in open-weight models;
- expansion from governed seed taxonomies; and
- cross-model agreement checks.

## Relations

Relations should not be inferred from weight magnitude alone. A relation query starts with two concepts and asks the model what relation, if any, is observable.

Example relation probe:

```text
Concept A: photosynthesis
Concept B: chlorophyll

What relationship, if any, exists between these concepts?
Do not assume that a relationship exists.
Return:
- relation label
- direction, if directional
- explanation
- confidence
- counterexamples or limits
- whether the inverse direction changes the meaning
```

Candidate structured result:

```json
{
  "source": "chlorophyll",
  "target": "photosynthesis",
  "relation": "enables",
  "directional": true,
  "confidence": 0.93,
  "description": "Chlorophyll absorbs light energy used in photosynthesis.",
  "status": "candidate"
}
```

Stored relations should include:

- source concept;
- target concept;
- relation label;
- directionality;
- explanation;
- confidence;
- prompt and raw response;
- model identifier and configuration;
- timestamp;
- validation observations; and
- current review state.

## Validation Discipline

The inventory should distinguish model observations from established facts. A relation can move from `candidate` to `confirmed` only through additional evidence.

Validation strategies:

- query the relation in both directions;
- repeat with prompt variants;
- compare multiple models;
- compare embedding or activation neighborhoods;
- check against external governed sources where available;
- ask for limits, counterexamples, and non-relations;
- run sham pairs to estimate false-positive relation creation; and
- preserve raw outputs for replay and audit.

This follows the project preference for truthfulness: evidence, provenance, and replay matter more than apparent fluency.

## Architecture Sketch

Dominant pattern intent:

- **Sensorium / Observer:** observe latent model behavior through probes.
- **Unio / Facade:** expose one concept-inventory interface over multiple probing strategies.
- **Expressio / Command:** store each probe as an auditable query command with inputs and outputs.
- **Restitutio / Memento:** keep raw prompt/response snapshots so derived relations can be revisited.

Minimal components:

```text
ConceptSeed
  -> ConceptProbe
  -> CandidateConcept
  -> RelationProbe(conceptA, conceptB)
  -> CandidateRelation
  -> RelationValidator
  -> ConceptGraphStore
```

Initial use cases:

- `inventariseConcept(seedConcept)`
- `queryRelation(conceptA, conceptB)`
- `validateRelation(candidateRelationId)`
- `exportConceptGraph(scope)`

## Evidence Boundary

This exploration does not claim that open model weights expose direct symbolic concepts or relation weights. It treats model internals and model outputs as evidence sources that require probing, interpretation, and validation.

The resulting concept graph is therefore not objective reality. It is a governed inventory of observed model behavior, with explicit provenance and maturity state.

## Connection To MML

MML already explores explicit semantic representation, typed relations, governed identities, and compiled knowledge state. LLM concept inventories could become an upstream source of candidate semantic material:

```text
LLM observations
  -> candidate concept graph
  -> governed semantic representation
  -> MML compilation and experiments
```

The value is not in trusting the LLM blindly. The value is in using the LLM as a rich latent source of candidate concepts and relations, then converting those observations into explicit, testable, inspectable semantic structure.
