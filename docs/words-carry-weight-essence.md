# Words Carry Weight: The Essence

[`activate_grounded_focus.py`](../src/semantic_representation/activate_grounded_focus.py) is the technical kernel of the smallest mechanism explored by this repository. [`words_carry_weight.py`](../src/semantic_representation/words_carry_weight.py) is the operational application flow: it coordinates `ground -> compile` for knowledge construction and `focus -> activate` for runtime use. The bounded experiment, benchmark, and console presentation are adapters over that operational flow. The current transition operator is a matrix; the same structure can be interpreted as a graph when relational paths matter.

> **Ground the known. Focus the intended. Activate the related.**

The larger proposition is:

> **We don't necessarily need increasingly complicated computation. We may need a representation of meaning rich enough that powerful mathematical structures already available to us start doing useful work.**

MML develops that proposition through a canonical triad:

> **Represent meaning. Compile knowledge. Compose concepts.**

- **Representation:** make important semantic identities, roles, and relations explicit.
- **Knowledge State Execution:** compile established structure once as governed state so declared consequences can be executed repeatedly.
- **Combinatorial Uniqueness:** compose reusable, sufficiently independent semantic coordinates into a more distinctive query-specific field.

The minimal flow touches all three at different levels of maturity. `ground -> compile` makes a semantic distinction addressable and builds a reusable transition model. `focus -> activate` executes from the selected identity. Separate controlled development experiments now test semantic representation, compiled knowledge-state execution, direct combinatorial intersection, governed legal qualification, and explicit cross-level transition. All remain authored and bounded; held-out construction, comparative efficiency, useful combinatorial coverage, and scaling remain hypotheses to test systematically.

It does not train a language model, reproduce transformer attention, or infer meaning autonomously. It executes the relationships present in a small authored corpus.

The vocabulary boundary is foundational:

> **Focus is representational narrowing** (`bank -> bank_river`), while **activation is the numerical distribution produced after querying that focused identity**. Attention remains an inspiration-level analogy and does not name a mechanism in this project.

Consequently, the kernel result is `Activation`, not `Focus`. Focus projects onto semantic enrichment or query interpretation—the narrowing of an identity before execution. Activation projects onto the numeric runtime result after execution. This ordering must remain explicit:

```text
ambiguous expression -> semantic focus -> selected identity -> query strategy -> activation
```

The code reflects this boundary directly. `SemanticFocus` represents the narrowing and `focus(...)` applies it. Only the returned focused identity is passed to `activate(...)`, which returns `Activation`. Focus is therefore an operation before activation, not a documentation-only synonym for its result.

Construction has a complementary operation: **semantic grounding** identifies a surface occurrence in the corpus as a governed identity before compilation. `SemanticGrounding` and `ground(...)` make `bank occurrence -> bank_river` explicit. Focus and grounding are not inverse functions; they are two ingress paths that converge on the same semantic identity:

```text
corpus occurrence -> semantic grounding --+
                                          +-> bank_river -> transition model/query
query expression  -> semantic focus ------+
```

A true reverse operation, `bank_river -> "river bank"`, would be lexicalization or rendering and is not implemented by this experiment.

## From Text to an Executable Weighting Structure

The minimal demonstration performs five operations:

```text
small text corpus
    -> vocabulary of addressable words
    -> word co-occurrence matrix
    -> normalized transition matrix
    -> Personalized PageRank query strategy
    -> inspectable query-relative activation
```

First, each distinct word becomes a node. Words that occur near one another within a sliding window receive weighted connections in the co-occurrence matrix. Repeated proximity increases the corresponding connection weight.

The matrix is then normalized so that every non-empty row describes a distribution of transition capacity from one word to its neighbours. Given the same corpus and settings, this representation is reproducible.

Semantic focus first narrows an ambiguous expression onto a more specific identity: `bank -> bank_river`, for example. At query time, the current strategy uses Personalized PageRank with its restart distribution anchored on that selected semantic identity. Activation repeatedly moves through the transition matrix while retaining a fixed pull toward the query. The result is a query-relative **activation** distribution over the addressable identities. Personalized PageRank is the first strategy implementation, not part of the `TransitionModel` contract.

The phrase **words carry weight** therefore has three literal consequences:

1. **Semantic coordinates are represented.** Governed identities make distinctions such as `bank_river` and `bank_financial` addressable.
2. **Established relationships are compiled into reusable capacity.** Stored weight belongs to a named transition operator rather than being reconstructed for each query.
3. **Coordinates are composed into query-specific fields.** Focus selects the starting identities; activation and soft intersection determine the contextual field for a particular use.

A word does not possess one universal importance value. Its executable weight depends on represented identity, compiled relationships, task policy, query intent, and the selected execution strategy.

| Phrase | Technical expression |
| --- | --- |
| **Words** | Addressable semantic identities in a `TransitionModel`; future models may also include semantic roles, concepts, or other governed identities. |
| **Carry** | A query strategy propagates transition capacity through the model. |
| **Weight** | The compiled operator stores explicit transition capacity between identities. |
| **Focus** | Semantic enrichment or query interpretation narrows an ambiguous expression to a more precise identity. |
| **Activation** | Query execution produces the contextual numeric distribution for this particular use. |

This table describes the minimal operational vocabulary. The canonical research triad sits above it: grounding and focus contribute to representation, compilation creates reusable execution state, and combined activation fields seed conceptual composition.

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

## From Related Concepts to Semantic Roles

A richer representation does more than state that two concepts are related. A concept can occupy a role such as `capacity`, `activation`, `boundary`, `substrate`, `gain`, or `storage`. The CML experiments use these roles to compare structures across domains while preserving the differences between their physical meanings.

The same principle applies to relation type. Synonymy, hierarchy, opposition, part/whole, causality, role correspondence, association, and temporal order should not be collapsed into one undifferentiated adjacency matrix. They can be compiled as a family of matrices and combined for a task through explicit semantic-policy coefficients:

```text
M = alpha*A + beta*S + gamma*H + delta*P + epsilon*C + zeta*R - eta*O
```

After suitable normalization, `M` becomes the task-specific propagation operator. A query then composes and activates not just a node but a semantic field shaped by identity, role, relation type, and declared policy. This is the stronger MML meaning of **words carry weight** and the bridge from the Compilation hypothesis to Combinatorial Uniqueness.

The current prototype has not implemented this family. It uses one positive transition matrix containing co-occurrence and three typed positive relations, with contradiction handled separately. The prototype demonstrates the seed from which the richer representation can be tested.

## What the Current Queries Show

The demonstration compares three related queries across two representations:

- `bank` queries the original model in which one identity accumulates both meanings;
- `bank_river` queries the grounded model using the river-bank identity; and
- `bank_financial` queries the same grounded model using the financial identity.

The first result exposes the important limitation. The original corpus uses the same surface token, `bank`, for a river bank and a financial institution. Consequently, its transition model contains one addressable identity that merges both meanings:

```text
river -----------+
water -----------|
                  bank
money -----------|
loan ------------+
```

The query strategy is not making an error when it produces mixed activation. It is faithfully executing an unfocused representation. The conceptual distinction between the two meanings was never made addressable.

## How It Contributes to MML

The script establishes the statistical substrate of Machine Modelled Language:

- language is externalized as explicit nodes and weighted relationships;
- those weights can be inspected instead of remaining hidden inside model parameters;
- execution is deterministic for fixed inputs and settings;
- a query produces contextual activation rather than a permanent word ranking;
- the representation can be rebuilt when its source structure changes.

This is necessary for MML, but it is not the complete MML proposition. MML adds governed semantic structure: stable concepts, distinct senses, aliases, typed relations, provenance, corrections, snapshots, and rollback. Human or institutional enrichment decides which distinctions should exist; the machine compiles and executes them.

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

That comparison isolates the essential effect of enriching semantic identity:

> Human enrichment makes meaning addressable; MML compiles that structure into reproducible weights and makes its consequences executable and inspectable.

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

The minimal demonstration isolates one dimension: **semantic identity**. It demonstrates that focusing an ambiguous surface word onto distinct semantic identities changes the compiled transition model—and therefore its graph interpretation—and the activation produced by the same query strategy.

Other experiments are required to isolate the remaining dimensions. A useful progression would compare:

1. ambiguous and enriched identity;
2. untyped and typed relations;
3. undirected and directed relations;
4. reachable paths and composition-valid paths;
5. unconstrained and context-qualified relations;
6. positive-only and contradiction-aware execution;
7. anonymous edges and provenance-bearing edges;
8. ranked candidate routes and symbolically validated answers.

Each experiment should change one governed dimension while holding the other inputs and execution settings stable. That makes the consequence of enrichment observable instead of blending many improvements into one opaque result.

## Evidence Boundary

The demonstration shows transition-model construction, semantic focus through identity enrichment, and query-relative activation over a tiny authored corpus. It does not demonstrate general semantic understanding, automatic word-sense discovery, transformer attention, complete relation composition, symbolic validation, validated reasoning, or superiority over established retrieval systems.

Its value is more foundational: it makes the relationship between representation and execution visible. If two meanings share one node, their weights mix. If governance gives those meanings separate identities, the executable topology—and therefore the resulting activation—can change.

| Hypothesis | Evidence boundary |
| --- | --- |
| **Representation** | The bounded `bank`, `bass`, and `crane` A/B fixtures provide development evidence under fixed compilation and activation mathematics. They do not establish the claim across arbitrary semantic dimensions or domains. |
| **Knowledge State Execution** | The separate Knowledge Is State spine demonstrates exact typed-chain compilation, repeated execution, inspectable consequences, governed correction, and preserved state in one bounded case. |
| **Combinatorial Uniqueness** | Independent fields and normalized geometric-mean composition now have atomic development studies for direct intersection, governed legal qualification, and stage-scoped transition. They have not established held-out specificity, useful combinatorial coverage, automatic transition discovery, or a scaling advantage. |

The current research progression is therefore precise: Representation, compiled Knowledge State Execution, and three distinct composition operations have bounded development evidence. The next evidentiary boundary is independence—freeze governed state first, author probes afterward, and test whether the observed behavior survives held-out combinations and meaningful baselines.
