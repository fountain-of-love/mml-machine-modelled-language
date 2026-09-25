---
artifact: architecture-note
status: candidate
updated: 2026-08-27
---

# Concept Inventory Architecture

## Purpose

This note defines the first structure for a Seed Vault concept inventory.

The inventory is not a tokenizer vocabulary. A tokenizer vocabulary stores surface fragments such as `play`, `##ing`, or `football`. The concept inventory stores governed semantic primitives and then records how surface language maps onto them.

The intended flow is:

```text
surface language
  -> morphology and syntax
  -> concepts
  -> relations
  -> governed semantic representation
```

## Inventory Layers

The inventory should be separated into three governed layers.

### 1. Concepts

Concepts name stable semantic identities.

Examples:

```text
PLAYER
PERSON
FOOTBALL
PLAY
TEAM
BALL
GAME
```

A concept record should include:

- canonical id;
- semantic type;
- meaning boundary;
- aliases;
- language-specific surface forms;
- sense distinctions;
- provenance;
- maturity state; and
- validation evidence.

Example:

```yaml
id: concept.player
label: PLAYER
type: entity
semantic_role: agent
aliases:
  en:
    - player
    - footballer
    - athlete
  fr:
    - joueur
  nl:
    - speler
status: candidate
```

### 2. Relations And Operators

Relations and operators describe how concepts compose.

Examples:

```text
BE
HAVE
DO
CAUSE
MOVE
LOCATED_IN
PART_OF
AGENT_OF
OBJECT_OF
```

These are not ordinary lexical concepts. They are semantic composition operators. Some may be language-visible, such as `be`; others may be introduced by analysis, such as `AGENT_OF`.

Example:

```yaml
id: relation.agent_of
label: AGENT_OF
type: semantic-role
directional: true
source_constraint: PERSON | ANIMATE_ENTITY | ACTOR
target_constraint: ACTION | EVENT
status: candidate
```

### 3. Grammatical Features

Grammatical features modify concepts, relations, or whole propositions.

Examples:

```text
PAST
PRESENT
FUTURE
SINGULAR
PLURAL
MALE
FEMALE
PROGRESSIVE
PERFECT
NEGATION
QUESTION
```

Features should be represented separately from concept identity. `players` should not become a separate concept from `player`; it should map to `PLAYER + PLURAL`.

Example:

```yaml
surface: players
maps_to:
  concept: concept.player
  features:
    - grammar.plural
```

## Surface Mapping

The inventory needs a mapping layer from observed language to governed semantics.

Examples:

```text
"player"   -> PLAYER
"players"  -> PLAYER + PLURAL
"play"     -> PLAY
"plays"    -> PLAY + PRESENT + THIRD_PERSON_SINGULAR
"played"   -> PLAY + PAST
"playing"  -> PLAY + PROGRESSIVE
```

The same concept can be reached through different languages:

```text
English:  player
French:   joueur
Dutch:    speler
German:   Spieler
Spanish:  jugador

              ->

           PLAYER
```

This makes the inventory an interlingual semantic layer, not a list of words.

## Example Analysis

Sentence:

```text
The players are playing football.
```

Tokenizer-level view:

```text
["The", " players", " are", " playing", " football", "."]
```

Linguistic analysis:

```text
PLAYER + PLURAL
BE + PRESENT + PLURAL
PLAY + PROGRESSIVE
FOOTBALL
```

Conceptual representation:

```text
PLAY(
  agents = PLAYER[plural],
  activity = FOOTBALL,
  aspect = PROGRESSIVE
)
```

Alternative proposition form:

```text
BE(
  subject = PLAYER[plural],
  state = PLAY(
    agent = PLAYER[plural],
    activity = FOOTBALL,
    aspect = PROGRESSIVE
  )
)
```

The representation should preserve the difference between:

- `BE` as a state or identity relation;
- `PLAY` as an action concept; and
- `PROGRESSIVE` as aspect.

## Sense And Context

Word forms cannot be collapsed directly into concepts.

`play` may refer to:

- playing a sport;
- playing a musical recording;
- playing an instrument;
- playing a theatrical role;
- playing a game;
- playing as pretending; or
- play as looseness in a mechanism.

Therefore surface mappings need sense constraints.

Example:

```yaml
surface: play
senses:
  - concept: concept.play_sport
    constraints:
      object: SPORT | GAME | ACTIVITY
  - concept: concept.play_music
    constraints:
      object: SONG | RECORDING | INSTRUMENT
  - concept: concept.perform_role
    constraints:
      object: ROLE | CHARACTER
```

The hard problem is not listing aliases. The hard problem is deciding when two observed expressions share a concept identity and when they only share a surface form.

## Discovery Loop

The initial inventory can be seeded manually, but it should be designed for automatic discovery from corpora.

Candidate discovery loop:

```text
corpus
  -> token and phrase collection
  -> morphological families
  -> distributional clusters
  -> candidate concepts
  -> candidate senses
  -> relation/operator hypotheses
  -> validation probes
  -> governed inventory records
```

Example surface family:

```text
player
players
the player
a player
football player
players are playing
the player plays
the player played
```

The system may discover that:

```text
player, players
```

belong to one entity family, while:

```text
play, plays, played, playing
```

belong to an action family.

Only after that observation should the inventory introduce or link canonical records such as `PLAYER` and `PLAY`.

## Minimal Data Model

The smallest useful governed model is:

```text
Concept
RelationOperator
GrammaticalFeature
SurfaceForm
SenseMapping
Proposition
EvidenceRecord
```

Suggested relationships:

```text
SurfaceForm
  -> has one or more SenseMappings

SenseMapping
  -> targets Concept | RelationOperator
  -> may add GrammaticalFeature values
  -> declares language, constraints, and confidence

Proposition
  -> composes Concepts, RelationOperators, and GrammaticalFeatures

EvidenceRecord
  -> supports or challenges Concept, SenseMapping, RelationOperator, or Proposition
```

## Governance Rules

- Do not treat a word as a concept by default.
- Do not create separate concepts for inflectional variants.
- Do not merge senses only because aliases overlap.
- Record language, corpus source, prompt, or observation method for every mapping.
- Keep grammatical features separate from concept identity.
- Promote candidate concepts only when their boundary and exclusions are explicit.
- Preserve competing mappings when context is insufficient.

## Pattern Lens

Dominant pattern intent:

- `Unio / Facade`: expose one concept-library interface across concepts, relations, grammar features, and surface mappings.
- `Circulatio / Adapter`: translate tokenizer outputs and corpus observations into governed semantic records.
- `Expressio / Command`: store discovery probes as replayable mapping commands.
- `Restitutio / Memento`: preserve raw corpus examples, prompts, and model outputs before derived concepts are promoted.

The smallest useful implementation should start as documents and ledgers, not as a full graph engine. Once the records stabilize, the same structure can become a schema for MML experiments.

