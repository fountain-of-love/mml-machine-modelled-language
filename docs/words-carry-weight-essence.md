# Words Carry Weight: The Essence

`pagerank_attention.py` is the smallest executable expression of the mechanism explored by this repository. It shows how language can be turned into an explicit weighted graph and queried through deterministic activation.

It does not train a language model, reproduce transformer attention, or infer meaning autonomously. It executes the relationships present in a small authored corpus.

## From Text to an Executable Weighting Structure

The script performs five operations:

```text
small text corpus
    -> vocabulary of addressable words
    -> word co-occurrence matrix
    -> normalized transition matrix
    -> query-anchored graph diffusion
    -> inspectable activation weights
```

First, each distinct word becomes a node. Words that occur near one another within a sliding window receive weighted connections in the co-occurrence matrix. Repeated proximity increases the corresponding connection weight.

The matrix is then normalized so that every non-empty row describes a distribution of transition capacity from one word to its neighbours. Given the same corpus and settings, this representation is reproducible.

At query time, Personalized PageRank anchors its restart distribution on one selected word. Activation repeatedly moves through the transition matrix while retaining a fixed pull toward the query. The result is a distribution over the vocabulary: words connected strongly and repeatedly to the query receive more activation weight.

This is the first literal meaning of the repository's phrase **words carry weight**. A word does not possess one universal importance value. Its weight emerges from its relationships, the compiled graph, and the current query.

The phrase also reaches beyond numerical edge weight. What a word or concept can carry depends on how the model perceives and governs it:

- **Identity:** which concept or sense the node represents;
- **Relationships:** which other nodes it can reach and how strongly;
- **Direction:** whether a relation runs from source to target, in both directions, or not at all;
- **Type:** whether a relation supports, requires, qualifies, contradicts, aliases, or expresses another declared meaning;
- **Composition:** which sequences of relation types form a valid semantic route;
- **Context and constraints:** which conditions make a relation applicable;
- **Exclusions:** which routes, interpretations, or combinations are forbidden or contradicted;
- **Provenance:** which source, authority, evidence, and review state justify the structure;
- **Query intent:** which identities and constraints are activated for this particular use;
- **Validation:** which candidate routes survive symbolic or domain-specific checks.

Weight is therefore not merely frequency, popularity, or importance. It is the executable consequence of a concept's identity and position inside a governed semantic structure.

## What the Three Queries Show

The script queries `river`, `money`, and `bank`.

- `river` activates the neighbourhood built from the natural setting.
- `money` activates the neighbourhood built from the financial setting.
- `bank` activates connections accumulated from both settings.

The third result exposes the important limitation. The corpus uses the same surface token, `bank`, for a river bank and a financial institution. Consequently, the graph contains one node that merges both senses:

```text
river -----------+
water -----------|
                  bank
money -----------|
loan ------------+
```

The algorithm is not making an error when it produces a mixed activation field. It is faithfully executing an ambiguous representation. The conceptual distinction between the two meanings was never made addressable.

## How It Contributes to MML

The script establishes the statistical substrate of Machine Modelled Language:

- language is externalized as explicit nodes and weighted relationships;
- those weights can be inspected instead of remaining hidden inside model parameters;
- execution is deterministic for fixed inputs and settings;
- a query produces contextual activation rather than a permanent word ranking;
- the representation can be rebuilt when its source structure changes.

This is necessary for MML, but it is not the complete MML proposition. MML adds governed semantic structure: stable concepts, distinct senses, aliases, typed relations, provenance, corrections, snapshots, and rollback. Human or institutional curation decides which distinctions should exist; the machine compiles and executes them.

The script makes the minimal conceptual step by comparing two controlled scenarios. Scenario A preserves the ambiguous `bank` node. Scenario B separates it into governed identities, `bank_river` and `bank_financial`:

```text
river -------- bank_river

money -------- bank_financial
```

The sentences, construction algorithm, sliding window, and execution settings remain identical. Only the authored semantic identity changes. Rebuilding the mechanism after that intervention produces different transition and activation weights. The natural and financial neighbourhoods become more distinct, and the reported context weights make cross-sense leakage visible.

Run the comparison with:

```bash
make run
```

That comparison isolates the essential effect of conceptual curation:

> Human curation makes meaning addressable; MML compiles that structure into reproducible weights and makes its consequences executable and inspectable.

## From Activation Toward Reasoning

The conceptual split is deliberately the smallest possible example. It changes identity and therefore changes the topology through which activation can travel. This illustrates one prerequisite for reasoning: a system cannot reason reliably about two meanings if its representation gives them the same identity.

Identity alone is not sufficient, however. A fuller MML reasoning layer would have to coordinate several dimensions:

```text
query intent
    -> resolved identities and senses
    -> typed, directed candidate relations
    -> permitted relation compositions
    -> constraints and exclusions
    -> provenance and applicability checks
    -> symbolic validation or query planning
    -> supported result with an inspectable trace
```

### Typed direction

Direction changes meaning. If `A requires B`, it does not follow that `B requires A`. A reasoning engine must preserve the declared direction instead of treating every graph connection as symmetric proximity.

### Relation composition

A reachable path is not automatically a valid inference. The engine needs explicit rules for which relations may compose. For example, two `supports` relations may yield a candidate support route, while `qualifies` followed by `contradicts` may require a different interpretation. Composition rules determine what a multi-hop path is allowed to mean.

### Stable identity

The `bank` experiment demonstrates this dimension directly. Surface equality does not guarantee conceptual identity, and different labels do not automatically guarantee conceptual difference. Governed sense identities, aliases, entities, jurisdictions, and versions determine what each node denotes.

### Constraints and applicability

Relations may hold only under particular conditions: time, jurisdiction, system state, domain, evidence maturity, or another declared scope. Reasoning must carry those conditions through execution rather than activating a relation universally.

### Exclusions and contradiction

Negative knowledge is structure too. Explicit contradictions, incompatible states, forbidden transitions, and rejected mappings prevent the engine from treating every connected route as positive support.

### Provenance

An executable route should remain connected to its sources, authorities, evidence, confidence, review state, and graph snapshot. Provenance does not prove that an inference is valid, but it makes the basis of the inference inspectable and contestable.

### Symbolic validation and query planning

Graph diffusion can discover and rank candidate routes. A symbolic validator or query planner must then determine whether a route satisfies the requested relation pattern, respects its constraints, avoids exclusions, and produces the requested kind of result. Activation proposes where to look; validation decides what the structure licenses the system to conclude.

These dimensions can eventually contribute to reasoning because they turn loose association into constrained semantic execution. Their combination—not PageRank alone—is the broader MML direction.

## One Small Example of a Larger Field

`pagerank_attention.py` isolates one dimension: **conceptual identity**. It demonstrates that splitting an ambiguous surface word changes the compiled graph and the activation weights produced by the same algorithm.

Other experiments are required to isolate the remaining dimensions. A useful progression would compare:

1. ambiguous and curated identity;
2. untyped and typed relations;
3. undirected and directed relations;
4. reachable paths and composition-valid paths;
5. unconstrained and context-qualified relations;
6. positive-only and contradiction-aware execution;
7. anonymous edges and provenance-bearing edges;
8. ranked candidate routes and symbolically validated answers.

Each experiment should change one governed dimension while holding the other inputs and execution settings stable. That makes the consequence of curation observable instead of blending many improvements into one opaque result.

## Evidence Boundary

The script demonstrates weighted graph construction, conceptual identity curation, and query-anchored activation over a tiny authored corpus. It does not demonstrate general semantic understanding, automatic word-sense discovery, transformer attention, complete relation composition, symbolic validation, validated reasoning, or superiority over established retrieval systems.

Its value is more foundational: it makes the relationship between representation and execution visible. If two meanings share one node, their weights mix. If governance gives those meanings separate identities, the executable topology—and therefore the resulting activation—can change.
