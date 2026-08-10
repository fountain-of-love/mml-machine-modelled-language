# How Machine Modelled Language Works Here

The repository demonstrates representation, execution, and evolution of an explicit semantic weighting matrix. Concepts and governed relations form the source model; the compiled matrix is the numerical object that executes. It does not train or imitate a language model.

Those lifecycle stages implement parts of the canonical research architecture:

| Canonical hypothesis | Current mechanism | Evidence status |
| --- | --- | --- |
| **Representation** | semantic grounding, query focus, and explicit identities | Addressed by the bounded A/B benchmark. |
| **Knowledge State Execution** | deterministic compilation into governed reusable state | One bounded typed-chain experiment compares per-query source reconstruction with compiled reuse; broader independent evidence is still needed. |
| **Combinatorial Uniqueness** | independent propagation and normalized geometric-mean soft intersection | Mechanism present; systematic held-out test still needed. |

In compact form: **Represent meaning. Compile knowledge. Compose concepts.** The sections below retain the prototype lifecycle—representation, execution, and evolution—but each mechanism should be read against that research contract.

## Run it

```bash
make run
make run-elaborate
make run-legal
make trace
make update-demo
make benchmark-check
make test
```

The first three commands show the mechanism at increasing levels of application. `make trace` prints one self-contained representation → execution → evolution record. `make update-demo` shows the wider consequences of the same kind of governed relation change and exact restoration. `make benchmark-check` runs the semantic representation benchmark; the older retrieval application diagnostic remains available through `make retrieval-benchmark-check`.

## Representation

Construction is separated by responsibility:

- `polysemy_corpus.txt` contains ten river-bank and ten financial-bank sentences;
- `gdpr_law_corpus.txt` supplies legal concepts and formulations;
- `gdpr_aliases.jsonl` maps governed phrases to declared concepts;
- `gdpr_relations.jsonl` records typed, weighted relations and evidence.

These inputs populate the weighting matrix. Its values belong primarily to relationships: they express how much transition capacity connects one addressable word or concept to another. After normalisation, the matrix is reproducible for the same governed inputs and construction settings.

Aliases use deterministic longest-match consumption. A phrase such as `selected records` resolves once to `information_control` rather than also leaking both component tokens.

The initial relation vocabulary is `supports`, `contradicts`, `requires`, and `qualifies`. Positive relation weights use visible type multipliers; contradictions remain a separate negative contribution and never become negative transition probabilities.

The prototype currently folds co-occurrence plus the positive relation types into one transition matrix. It does not yet preserve synonymy, hierarchy, opposition, part/whole, causality, role correspondence, association, or temporal relation as independently weighted matrices. That family-of-matrices model is the proposed next representation step: task policy composes the relevant matrices into an operator and only then normalizes it for execution.

## Compilation And Reuse

`compile_transition_model(...)` deterministically transforms grounded source observations into a reusable `TransitionModel`. The minimal application compiles during knowledge construction and can execute multiple focused queries against the resulting model without rebuilding it between queries. The elaborated engine similarly builds named, content-addressed matrix state from corpora, aliases, relations, and settings.

This compile-once, query-repeatedly shape is the mechanism behind the Knowledge State Execution hypothesis. The separate Knowledge Is State experiment compares deterministic per-query source reconstruction with compiled execution in one authored typed-chain task. Snapshots, updates, and rollback support identity and governance around the compiled state. Broader evidence still needs independently authored cases, a measured language-model baseline, meaningful scale, and full accounting of construction cost, query volume, update frequency, latency, resources, correction effort, and result stability.

## Execution

Execution begins only after focus has selected a semantic identity. **Focus is representational narrowing** (`bank -> bank_river`); **activation is the numerical distribution produced after the selected query strategy executes from that identity**. Accordingly, `activate_grounded_focus.py` returns `Activation`, not `Focus`. Attention is not an execution stage or implemented mechanism here.

The minimal demonstration makes that sequence executable: `SemanticFocus` records the broader and focused identities, `focus(...)` validates and applies the narrowing, and `activate(...)` receives only the resulting focused identity.

The construction-side complement is semantic grounding. `SemanticGrounding` records which corpus occurrence denotes which governed identity, and `ground(...)` applies that identification before compilation. Grounding and focus converge on the same identity from corpus and query respectively; neither is numerical activation.

`GraphModel` is the historical name of the current facade over construction, matrix activation, relation-path inspection, and immutable snapshot state. The name reflects how the prototype began, but the class now coordinates more than one responsibility. The intended separation and future naming are documented in [MML in depth](MML-In-Depth.md#implementation-boundaries-matrix-paths-and-events).

Surface `bank` resolves from surrounding context to `bank_river`, `bank_financial`, or both. Each query token produces a bounded local activation field. Multi-token queries combine those fields with a normalized geometric mean, requiring support across fields rather than averaging them.

The execution therefore uses two related kinds of weight: stored transition weights in the matrix and contextual activation weights produced for the current query. Neither is a permanent declaration of a word's universal importance.

This intersection is called **[combinatorial uniqueness](Combinatorial-Uniqueness.md)** here. Broad concepts can be noisy and weakly discriminative alone, while several broad but sufficiently independent constraints can identify a much narrower semantic region. Their combination carries evidentiary weight because support must survive across the independently activated fields. `attention + systems theory + ranking`, for example, specifies a different intent than any term alone. The phrase names an operational design principle—not a claim that MML invented conjunction, product-of-experts inference, faceted retrieval, or vector intersection.

Document scoring combines informative-token weighting, hub correction, graph-field similarity, and declared contradictory evidence. The same calculation powers ordinary and explained scoring.

An explanation can expose:

- resolved query and document concepts;
- positive and negative score components;
- graph paths;
- relation or alias identifiers;
- construction evidence;
- the graph snapshot.

A graph path proves an executable route. Provenance identifies its governed source. Neither automatically provides a full causal decomposition of the final score.

### Activation, propagation, and reasoning

The current engine performs activation and propagation. Power iteration or bounded diffusion moves weight through connected structure and ranks reachable concepts. That can surface candidate multi-hop routes, but it does not by itself prove the logical composition expressed by those routes.

Validated multi-hop reasoning additionally requires typed direction, relation-composition rules, entity identity, constraints, exclusions, provenance, and often a query planner or symbolic verifier. A future MML may add those requirements as deterministic execution layers. Until then, the safer distinction is:

> Diffusion discovers and ranks candidate semantic routes; typed traversal and validation would determine whether a route satisfies a requested reasoning chain.

`activation` is therefore the correct runtime term. It is neither semantic focus nor transformer `attention`, and a high activation score is not automatically `reasoning` or proof.

## Evolution

Snapshots are content-addressed from the executable construction, governed records, and parameters. Relations and aliases are updated by rebuilding immutable state rather than mutating the running model.

Evolution makes compiled reuse governable: it answers which source state produced an operator, what changed, what consequences followed, and whether the previous artifact can be reconstructed exactly. It does not by itself show that compilation is cheaper or more useful than repeated reconstruction.

`make update-demo` performs:

```text
baseline sources -> baseline snapshot and rankings
one governed relation addition -> new snapshot and observable effects
original sources -> exact baseline snapshot and rankings
```

The demo reports how widely the effect propagates without declaring broad propagation a failure. Structural locality means the authored change itself is explicit and bounded; consequence breadth is a separate observation that must remain traceable.

## Semantic representation benchmark

The primary benchmark reuses the `words_carry_weight` comparison across three scenarios: `bank`, `bass`, and `crane`. Every scenario runs the same co-occurrence compiler and Personalized PageRank strategy over an ambiguous representation and a semantically grounded representation. Only identity grounding and query focus change.

For each focused identity, the benchmark checks:

- whether intended-context activation exceeds contrast-context activation;
- whether the intended-versus-contrast margin improves;
- whether cross-meaning activation decreases; and
- whether exact replay produces the same result.

This is authored development evidence for one kind of richer representation: governed semantic identity. It does not yet validate synonymy, hierarchy, semantic roles, relation-specific matrices, or policy composition. See the [benchmark proposal](benchmark/semantic-operator-benchmark-proposal.md) and [v1 result](benchmark/results/semantic-representation-v1.md).

## Retrieval application diagnostic

The legacy diagnostic ranks 20 polysemy and 30 GDPR documents using lexical overlap, TF-IDF, co-occurrence MML, typed MML, and one fixed hybrid:

```text
hybrid = mml_typed × (0.2 + 0.8 × lexical_overlap)
```

This formula is not selected through a calibration search. It exists to make the complementary lexical/semantic observation reproducible. Rankers receive documents and queries, never judgments. Judgments are used only afterward for P@5, R@10, MRR, and nDCG@10.

The diagnostic performs prototype checks for selected hashes, balance, determinism, low absolute floors, and reference regression. It is not a production integrity framework. Missing opportunities include complete schema and judgment validation, leakage diagnostics, independent artifact signing, protected release history, and held-out evaluation. A regressed reference cannot be overwritten silently; `--accept-regression` is an explicit reviewed escape hatch. It is synthetic development evidence, not an MML verdict. See [benchmark/README.md](benchmark/README.md).

MML receives governed concept mappings and negative evidence that lexical and TF-IDF baselines do not receive. This is inherent to the supervised mechanism, but it makes the systems different treatments rather than identical-input algorithms. The table measures end-to-end retrieval behavior, not the isolated value of graph propagation.

## Current limits

- Construction and demonstrations remain authored.
- The graph is small and in memory.
- Typed relation coverage is provisional and narrow.
- Explanations are not complete causal decompositions.
- There is no public graph ingestion, API/UI, access-control layer, or community review process yet.
- The code does not determine legal merits.
- `make trace` deliberately selects one legible QG3/G14 example; it is not representative coverage.
- The legal demo reports an A/B diagnostic comparing curated lexical candidate generation with graph scoring over all authored candidates. It demonstrates the effect of curation, not generalization.

See [Research-Contract.md](Research-Contract.md) for the claim and [Commons-Governance.md](sos/Commons-Governance.md) for the intended public workflow.
