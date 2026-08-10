# Activate Grounded Focus Vocabulary

LLMs reason with concepts expressed through language. They use names, descriptions, examples, and surrounding context to infer what code is intended to mean. If one term silently acquires several meanings, an LLM—and often a person—can cross a design boundary while still producing locally plausible text or code. Clear vocabulary is therefore part of the executable architecture, not merely editorial polish.

This document governs the vocabulary surrounding [`activate_grounded_focus.py`](../activate_grounded_focus.py), the operational [`words_carry_weight.py`](../words_carry_weight.py) application flow, and their experiment and presentation adapters. Each term is projected onto a concrete function or element and given a drift boundary. If implementation and vocabulary diverge, either the implementation or this contract must be changed explicitly.

> **Ground the known. Focus the intended. Activate the related.**

The sentence names the functional triad: **ground meaning -> focus intent -> activate relationships**. Compilation prepares the transition model between grounding and activation; it is essential infrastructure, not a fourth dancer. Personalized PageRank is one implementation beneath `activate(...)`, not part of the triad itself.

## Focus, Attention, and Activation

These three terms are related but not interchangeable:

```text
surface word          semantic focus                 runtime activation
    bank       ->        bank_river        ->     query-relative distribution
                             |
                             +-- richer, narrower identity
```

- **Focus** is representational narrowing. `bank_river` focuses the ambiguous surface word `bank` onto a more specific semantic identity. Focus happens during enrichment or query interpretation, before numerical execution.
- **Activation** is the numerical result of executing a query strategy from the selected identity. It expresses how much activation reaches each addressable identity for this query.
- **Attention** is not an implemented mechanism in this project. It may describe, informally, where a person or system directs concern, and the original experiment was inspired by the title *Attention Is All You Need*. It must not be used as a synonym for transformer attention, semantic focus, or matrix activation.

Focus can shape activation because a more precise starting identity changes which transitions are available and therefore changes the resulting distribution. Activation does not itself perform semantic disambiguation.

The kernel result should therefore be `Activation`, not `Focus`. Focus projects onto semantic enrichment or query interpretation—the narrowing of an identity before execution. Activation projects onto the numeric runtime result. In compact form: **focus is representational narrowing** (`bank -> bank_river`), while **activation is the numerical distribution produced after querying that focused identity**. Attention remains an inspiration-level analogy and explicitly does not name a mechanism in this project.

## Concept Vocabulary

| Concept | Projected onto | Definition | Role / responsibility | Drift boundary |
| --- | --- | --- | --- | --- |
| Words | `TransitionModel.identities` | Addressable tokens or enriched semantic identities known to a compiled model. | Provide stable coordinates for compilation and query execution. | Do not imply that every identity must remain a surface word; future identities may be concepts, roles, entities, or governed senses. |
| Meaning | `ground(...)`, `focus(...)`, future semantic sources | The governed distinctions and relations represented by identities and transitions. | Determine what the executable structure is capable of distinguishing. | Do not claim the current co-occurrence compiler discovers or understands meaning autonomously. |
| Semantic identity | `TransitionModel.identities`, `semantic_identity` parameters | One addressable meaning-bearing coordinate, such as `bank_river`. | Keep distinct meanings separately queryable. | Do not equate spelling with identity or treat an identifier as proof that its meaning is valid. |
| Semantic role | Proposed future transition sources; CML vocabulary | A function occupied by a concept, such as capacity, activation, boundary, substrate, gain, or storage. | Permit comparison by role without collapsing domain-specific meanings. | Not implemented by the minimal compiler; do not present it as current executable evidence. |
| Focus | `SemanticFocus`; `focus(...)`; the mapping `bank -> bank_river` | Representational narrowing from an ambiguous expression to a more specific semantic identity or field. | Select the intended meaning before execution so the query begins from a better-defined coordinate. | Do not use `SemanticFocus` as the runtime numeric result. Do not imply that focus proves the selected identity is correct. |
| Grounding | `SemanticGrounding`; `ground(...)`; a corpus occurrence of `bank -> bank_river` | Construction-side identification of a surface occurrence as a governed semantic identity. | Make corpus meaning addressable before model compilation. | Do not call grounding focus, activation, automatic discovery, or proof that the mapping is true. |
| Attention | No kernel function or element | An informal orientation metaphor and historical inspiration. Transformer attention is a different, specific mechanism. | Explain inspiration only when the distinction is made explicit. | Never claim that Personalized PageRank or activation implements, simulates, or reproduces transformer attention. |
| Activation | `Activation`; `ActivationStrategy.activate(...)`; `activate(...)` | The query-relative numeric distribution produced by executing a strategy over a transition model. The lowercase CML scientific role `activation` is a separate, governed domain concept. | Report where execution places activation for the selected query identity. | Do not call activation stored knowledge, truth, attention, semantic focus, or a probability that a conclusion is correct; qualify runtime `Activation` versus a domain role. |
| Weight | `TransitionModel.transition`; `Activation.weights` | In the model, explicit transition capacity; in an activation, the numeric mass assigned during this execution. | Make structural and contextual influence numerically inspectable. | Always qualify stored transition weight versus runtime activation weight; never treat either as universal importance. |
| Carry | `PersonalizedPageRankActivationStrategy.activate(...)` and future strategies | Propagation of activation through the transition operator. | Connect the phrase “words carry weight” to executable movement through structured relations. | Do not suggest that an identity physically owns or permanently carries one scalar weight. |
| Transition | `TransitionModel.transition` | Directed numerical capacity from one addressable identity to another after compilation and normalization. | Supply the operator used by query strategies. | A transition is not automatically a valid logical inference, causal relation, or truth claim. |
| Transition model | `TransitionModel` | A neutral executable model containing identities, lookup indexes, and a transition operator. | Keep callers independent of whether future implementations originate from matrices, graphs, or composed semantic sources. | Do not rename it after its current co-occurrence source or assume it already contains every semantic relation family. |
| Matrix | `TransitionModel.transition` as currently compiled | The current `N x N` numerical representation of transitions. | Enable deterministic normalization and matrix-vector propagation. | Do not make matrix storage part of the lasting `TransitionModel` semantic contract if another representation can satisfy it. |
| Graph | Interpretation of non-zero transitions and governed relations | A relational view in which identities are nodes and transitions or declared relations are edges. | Support explanation, paths, provenance, and alternative algorithms. | Do not say the minimal kernel stores an object graph or performs graph traversal; its current operator is a NumPy matrix. |
| Query | Input to `focus(...)` and `activate(...)` | A request whose intended semantic identity must be selected before execution. | Orient focus and subsequent activation. | The minimal flow accepts one declared identity; do not imply natural-language interpretation or multi-concept planning. |
| Activation strategy | `ActivationStrategy` | Contract for interchangeable algorithms that activate a transition model. | Isolate algorithm variation from the model and callers. | Strategies must not load experiment data, ground a corpus, focus identities, format output, or mutate the model. |
| Personalized PageRank | `PersonalizedPageRankActivationStrategy` | The first activation strategy: iterative propagation with restart anchored on the focused identity until convergence or a declared limit. | Provide deterministic, query-anchored activation over the current model. | Do not call it attention, reasoning, semantic focus, or the definition of MML. |
| Algorithm | Each `ActivationStrategy` implementation; compilation procedure | A defined procedure for producing a result from inputs. | Name concrete computation independently from representation. | Do not use “algorithm” as a synonym for the entire kernel, model, architecture, or experiment. |
| Kernel | `activate_grounded_focus.py` as a small module | The reusable functional spine: grounding, focus, model compilation, activation result, strategy contract, PageRank strategy, and activation facade. | Keep reusable mechanics isolated from experiment and presentation concerns. | Do not use “kernel” as a synonym for every algorithm or for the wider MML/SOS architecture. |
| Compile | `compile_transition_model(...)` | Deterministically transform source observations into an executable transition model. | Separate model construction from runtime querying. | Do not call compilation training, inference, enrichment, or autonomous learning. |
| Enrichment | Grounding and focus collectively enrich the representation | Addition of more precise semantic identity on the construction and query sides. | Describe the broader outcome without hiding the two explicit operations. | Do not use enrichment where the code specifically performs grounding or focus. |
| Context | Data file `contexts`; `sum_activation(...)` | A declared diagnostic set used to measure how much activation reaches an expected semantic neighbourhood. | Make cross-meaning activation visible in the demonstration. | Context sets are authored diagnostics, not learned concepts or universal definitions. |
| Operator | `TransitionModel.transition`; proposed composed matrices | A mathematical object on which a strategy performs execution. | Leave room for task-specific matrix composition and richer semantic layers. | Do not claim relation-specific operator families are implemented in the minimal kernel. |

## Function Vocabulary

| Function | Description | Role / responsibility | Drift boundary |
| --- | --- | --- | --- |
| `Activation.by_identity()` | Converts the activation vector into an identity-to-weight mapping. | Provide an inspectable presentation-neutral view of one result. | Must not rank, filter, print, enrich, or reinterpret identities. |
| `Activation.weight_for(identity)` | Returns activation weight for one identity, or zero when absent. | Support bounded diagnostic aggregation without leaking matrix indexes. | Must not fall back to aliases, infer identities, or mutate activation. |
| `ActivationStrategy.activate(model, semantic_identity)` | Declares the interchangeable activation-algorithm contract. | Define the real Strategy variation point. | Must return `Activation`; must not own compilation, grounding, focus, data loading, or presentation. |
| `PersonalizedPageRankActivationStrategy.activate(...)` | Builds a one-hot restart vector and iterates `d * activation @ transition + (1-d) * anchor` until tolerance or iteration limit. | Implement converged Personalized PageRank as one activation strategy. | Must not be described as attention, focus, reasoning, or the only possible MML activation algorithm. |
| `compile_transition_model(sentences, window_size)` | Tokenizes the bounded text source, counts local co-occurrence, row-normalizes the counts, and returns a `TransitionModel`. | Provide the first deterministic compiler for the neutral model contract. | Its current source is co-occurrence; do not silently add semantic relation policy without an explicit compiler contract. |
| `activate(model, semantic_identity, strategy)` | Delegates model execution to the selected activation strategy. | Act as the stable activation facade. | Must not branch on concrete strategy type, focus the identity, format output, or hide errors. |
| `load_experiment(path)` | Reads the demonstration JSON. | Own fixture loading outside the kernel. | Must not compile or query a model. |
| `ground(sentences, semantic_groundings)` | Applies declared corpus-occurrence-to-identity groundings after validating the bounded fixture. | Make corpus grounding a first-class construction operation. | Must remain explicit and authored; must not focus a query or be presented as automatic word-sense discovery. |
| `focus(source_identity, semantic_focus)` | Validates that a declared `SemanticFocus` applies to the source and narrows it to a different identity, then returns that focused identity. | Make focus a first-class operation before activation. | Must not compile a model, calculate activation, infer focus automatically, or validate that the declared meaning is true. |
| `WordsCarryWeightFlow.ground_and_compile(...)` | Coordinates the operational construction flow from source sentences and optional groundings to a transition model. | Provide an application-facing construction operation independent of experiments and storage. | Must not load fixtures, compare treatments, calculate benchmark metrics, or present output. |
| `WordsCarryWeightFlow.focus_and_activate(...)` | Coordinates the operational runtime flow from source identity through optional focus to activation. | Provide an application-facing runtime operation that retains focus with its result. | Must not select benchmark contexts, compare representations, or format output. |
| `sum_activation(activation, identities)` | Adds activation weights for a declared diagnostic context. | Measure activation reaching an authored semantic neighbourhood. | Must not change activation or claim statistical significance. |
| `compare_representations(experiment, strategy)` | Compiles original and grounded corpora, applies declared query focuses, queries the resulting identities, and assembles comparison data. | Orchestrate the bounded representation experiment. | Must not move into the kernel or become a universal quality verdict. |
| `strongest_activations(...)` | Filters and deterministically ranks activation entries for display. | Prepare a human-readable view in the demonstration layer. | Must not affect model construction, query execution, or diagnostic totals. |
| `display_activation(...)` | Prints one formatted activation ranking. | Own console presentation. | Must not calculate the activation it displays. |
| `display_representation_comparison(...)` | Prints original and semantically grounded results plus diagnostic context totals. | Present the experiment comparison. | Must not be described as an automated test or independent evaluation. |
| `main()` | Loads, executes, and displays the default demonstration. | Provide the `make run` entry point. | Must remain orchestration only; reusable mechanics belong below it. |

## Element Vocabulary

| Element | Description | Role / responsibility | Drift boundary |
| --- | --- | --- | --- |
| `TransitionModel.identities` | Ordered tuple defining the coordinates of the operator. | Provide deterministic identity ordering. | Ordering is technical identity, not semantic ranking. |
| `TransitionModel.identity_to_index` | Lookup from semantic identity to operator coordinate. | Hide repeated index searches and keep compilation/query alignment explicit. | Must not contain aliases or perform semantic resolution. |
| `TransitionModel.transition` | Current row-stochastic NumPy transition matrix. | Hold compiled transition capacity. | Must not include negative probabilities or be called activation. |
| `Activation.model` | Model against which this activation was produced. | Preserve coordinate meaning for the activation vector. | Must not imply that activation is durable model state. |
| `Activation.weights` | Query-relative numerical activation vector. | Store one execution result. | Must not be mutated, reused as transition weight, or described as truth probability. |
| `ActivationStrategy` | Structural protocol implemented by activation algorithms. | Decouple callers from a concrete strategy. | Must stay smaller than the algorithms it coordinates; no grounding, focus, data, or presentation responsibilities. |
| `PersonalizedPageRankActivationStrategy.damping` | Fraction of activation propagated through transitions each iteration. | Configure balance between propagation and query restart. | Not a semantic-policy coefficient and not learned. |
| `max_iterations` | Hard upper bound on PageRank iterations. | Guarantee termination. | Not the semantic radius of a bounded graph query. |
| `tolerance` | L1 convergence threshold. | Permit deterministic early convergence. | Not a confidence threshold or answer-quality score. |
| `anchor` | One-hot vector for the queried identity. | Retain query orientation during PageRank restart. | Not transformer attention, semantic focus, or a persistent model element. |
| `DEFAULT_EXPERIMENT` | Path to the default demonstration data. | Keep the entry point configurable and data external to the kernel. | Must not become a hidden global model or authoritative corpus. |
| `sentences` | Authored source text in the demonstration data. | Supply bounded co-occurrence observations. | Not training evidence or representative natural-language coverage. |
| `semantic_groundings` | Declared corpus-occurrence-to-semantic-identity mappings. | Supply the construction-side representational difference under test. | Not autonomous inference or proof that the identity mapping is correct. |
| `SemanticFocus.source_identity` | Ambiguous or broader identity before narrowing. | Preserve the input side of the focus operation explicitly. | Must not be silently replaced with the focused identity. |
| `SemanticFocus.focused_identity` | More specific identity selected before execution. | Supply the identity passed to `activate(...)` after focus validation. | Must not contain activation, strategy configuration, or an assertion of semantic truth. |
| `contexts` | Authored identity sets for river and financial diagnostics. | Measure expected and cross-meaning activation. | Not part of query execution and not selected from results. |
| `original_query` | Ambiguous identity queried in the original model. | Establish the comparison baseline. | Not a natural-language query parser. |
| `focused_queries` | Declared source and focused identity pairs activated in the grounded model. | Construct first-class `SemanticFocus` values and execute the same algorithm from narrower semantic coordinates. | Do not bypass `focus(...)` or treat better separation as generalization evidence. |
| `display_exclusions` | Tokens hidden from printed rankings. | Improve legibility only. | Must never affect compilation, activation, or metrics. |

## Recorded Design Boundary

The following text records the design boundary established during the refactoring:

The recorded text uses the former filename and API names. It is retained as history; the current contract is `activate_grounded_focus.py` with `ground(...)`, `focus(...)`, and `activate(...)`.

> The design boundary is now clear: semantic_matrix_activation.py will contain only the reusable kernel—TransitionModel, Focus, the query-strategy contract, Personalized PageRank, compilation, and the query facade. Corpus enrichment, comparison metrics, ranking, display, and main belong in words_carry_weight.py, backed by a data file. Here “algorithm” is the correct general term; “kernel” is useful only for the small computational core, not as a synonym for every possible query strategy.
>
> The code boundary is in place. Two observations emerged while implementing it: Focus is a useful domain result because it prevents “activation” from being confused with stored matrix weight, and the Strategy pattern is justified here because the variation point is real and explicit—not speculative class structure. Personalized PageRank is now one implementation, while query(...) is the stable interface.
>
> The presentation drift has also been removed from the kernel. strongest_focus, formatted output, representation comparison, and main now live in the demonstration; they are legitimate there because that module owns interpretation and presentation. The kernel has no corpus, no bank, no contexts, no A/B result, and no console output.

### Vocabulary refinement applied after that record

The boundary remains authoritative, but the name `Focus` in the recorded text has been refined. Feedback clarified that focus belongs to semantic narrowing (`bank -> bank_river`), while the numeric result of a strategy is activation. The implementation therefore uses `Activation`, `sum_activation`, `strongest_activations`, and `display_activation`. This is an explicit vocabulary correction, not a change to the architectural boundary.
