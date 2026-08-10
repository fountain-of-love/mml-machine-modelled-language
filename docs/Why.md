# Why MML

The current AI race is not sustainable. It is built around ever-larger models, ever-denser computation, and ever-more expensive inference, while many of the patterns being navigated are already known, repeatedly proven, or discoverable as explicit structure.

Current **Large Language Models (LLMs)** repeatedly navigate learned relationships through dense stochastic inference. Even when a semantic route is stable, the model still re-enters a probabilistic next-token process. MML asks whether some stable routes belong in an explicit executable representation instead.

**Machine Modelled Language (MML)** proposes a different route: use combinatorial discovery and PageRank-style graph diffusion to reuse proven semantic routes more directly. Instead of making every query pass through opaque trial-and-error, MML stores more of the structure explicitly, then lets contextual weight propagate through that structure.

This document explains why that matters for sustainability, robustness, drift control, and semantic auditability. For the conceptual portal, see [What](What.md). For the MML mechanics, see [MML in depth](MML-In-Depth.md).

## MML Does Not Discard LLMs

MML is not an argument for throwing LLMs away. LLMs are useful precisely where stochastic exploration is valuable: pattern detection, discovery, creative search, fuzzy synthesis, and trial-and-error over unknown spaces.

The problem is that many everyday tasks sent to Claude, ChatGPT, and similar systems are not truly unknown spaces. They are repetitive, known, or strongly patterned: classify this document, find relevant evidence, summarize this familiar workflow, route this request, identify missing information, apply this known policy, connect this symptom to this procedure.

For those tasks, repeatedly invoking a large stochastic model can be wasteful and unstable. The system is often navigating a route that has already been travelled many times before.

MML is complementary. It lets LLMs help discover patterns, propose structures, and express language, but once relationships are known and governed, MML can preserve them as explicit graph structure. The next query can activate that known structure through deterministic propagation.

That is how MML can resolve many ongoing issues without denying the usefulness of LLMs: use LLMs for discovery, use MML for durable structure.

## A Technology Used Beyond Its Purpose

Large language models are powerful discovery and language-generation tools. The architectural problem begins when the same probabilistic mechanism is also expected to become a knowledge store, truth authority, planner, security principal, and autonomous worker. Trial-and-error next-token prediction is then applied to tasks that require stable identity, exact evidence, reproducible decisions, durable memory, or tightly bounded action.

That mismatch contributes to several connected problems:

- convincing but unsupported answers and semantic or behavioural drift;
- repeated dense computation for patterns that are already known;
- knowledge that is difficult to inspect, correct, or govern inside model parameters;
- tool-enabled agents turning probabilistic mistakes or adversarial instructions into unintended external actions;
- safety harnesses continually trying to contain behaviour produced inside an entangled mechanism they cannot fully inspect;
- concentration of technical and economic power around a few general-purpose models; and
- pressure to automate complete human roles before deciding which responsibilities require judgment, accountability, relationship, or care.

MML does not solve cybersecurity, energy consumption, labour displacement, or institutional governance by itself. It changes the architectural starting point. Governed knowledge and known semantic routes remain explicit; people decide what becomes durable; external actions can be separated behind typed, verifiable contracts; and stochastic models can return to the discovery and linguistic work for which they are best suited.

The value is separation rather than imitation. MML provides governed semantic interpretation without also having to retrieve evidence, generate prose, or hold authority to act. In a wider modular pipeline, meaning can be inspected, corrected at its source, rebuilt against a named snapshot, and traced from a person's words through explicit concepts towards verifiable evidence and a constrained answer.

## From Combinatorial Discovery To Sustainable LLMs

The bridge from combinatorial discovery to PageRank is sustainability. Combinatorial discovery offers a basis for semantic execution: use several broad but orthogonal signals to narrow the active field before doing expensive or generative computation.

If `attention`, `systems theory`, and `ranking` intersect into a precise conceptual region, the model should not need to activate the whole universe of language. It should work inside that constrained region, where fewer relationships are relevant and the structure is easier to inspect.

The PageRank algorithm is a proven concept for this kind of solution because it already solves a similar graph problem: given a network of relationships, calculate how importance flows through that network. The original paper, [The PageRank Citation Ranking: Bringing Order to the Web](https://ilpubs.stanford.edu/422/), describes PageRank as a way to mechanically measure importance from link structure. For MML, the proposal is not to rank web pages. It is to let activation move through a constrained semantic graph so an execution engine can reuse explicit relationships.

This is also where MML differs from the usual Transformer pattern. LLMs navigate learned relationships stochastically: even when a pattern is already known or repeatedly proven by the data, the model still re-enters a probabilistic next-token process and effectively re-discovers the path through dense activation at inference time. That is powerful for open-ended generation, but wasteful when the relationship is already established.

PageRank-style graph diffusion is deterministic and robust once the graph structure and transition weights are known. For proven or discovered patterns, it is more effective to store the relationship explicitly and reuse it directly. The model does not need to spend dense compute repeatedly guessing its way through a known semantic route; it can propagate weight through the known structure.

PageRank measures importance by mapping how items link to one another in a network. A Transformer can be understood, at a high level, as an unsupervised learning system that discovers link-like relationships between words across massive amounts of text. In that sense, one useful mental model is to see a Transformer as a dynamic, AI-learned cousin of PageRank: instead of ranking web pages by fixed hyperlinks, it assigns contextual weight to words based on learned relationships.

The Python script makes that analogy concrete in a small, inspectable way. It does not train a Transformer or implement transformer self-attention. It builds a word graph from local co-occurrence patterns, then uses PageRank-style diffusion to produce a graph-activation distribution anchored on one or more query words.

## Problem Statement Of Current LLMs

Large language models store language capability and much knowledge in dense neural parameters. MML does not reframe those models as graphs; it introduces a separate architectural layer: a structured knowledge representation with query-anchored execution.

Instead of relying on dense computation for every stable semantic route, this approach shifts some work toward explicit graph dynamics. The Python script demonstrates only the seed of that shift. It does not replace transformer attention or demonstrate sparse performance at scale.

### 1. Energy And GPU Demand: Dense Tensor Math Vs. Sparse Graph Diffusion

**The Problem Today:** Transformers perform massive dense matrix multiplications, often summarized as `O(N^2 * d)` per attention layer with respect to sequence length `N` and hidden dimension `d`. These operations run across billions of floating-point parameters on power-hungry GPUs, even when a prompt may require something closer to semantic lookup than deep multi-step reasoning.

**The MML Shift:** MML-style graph diffusion operates naturally on sparse matrices. Calculating a query-anchored distribution over a graph can use Sparse Matrix-Vector Multiplication, with work proportional to `O(|E|)`, where `|E|` is the number of active edges in the graph.

**The Impact:** Graph-based diffusion can require far less memory bandwidth than dense neural inference. A larger version of this demo would keep only meaningful word-to-word or concept-to-concept edges instead of forcing every token to interact through dense tensor operations.

### 2. Content Clutter And AI Slop: Semantic Scaffolding As A Filter

**The Problem Today:** Transformers are trained on enormous web corpora. As the internet fills with AI-generated content, future models risk training on degraded, circular data that can amplify hallucinations, repetition, and low-quality patterns.

**The Lexical Dictionary Fix:** A human-curated lexical foundation, such as a modern WordNet- or ConceptNet-like graph, can act as a semantic anchor.

By defining core nodes and sense relationships, the graph can distinguish meanings such as `bank_financial` and `bank_river`. Web text can then adjust transition weights without redefining those governed semantic identities from scratch. The current prototype demonstrates this explicit distinction in miniature.

### 3. Model Drift And Knowledge Decay: Retraining Vs. Edge Editing

**The Problem Today:** Updating a traditional LLM's parametric memory often requires fine-tuning, reinforcement learning, retrieval augmentation, or full retraining. These updates can be expensive and can introduce model drift or catastrophic forgetting.

**The MML Shift:** Knowledge in a graph structure is topological rather than purely implicit. If a real-world relationship changes, the update can be represented as a local graph edit: insert a node, add an edge, remove an edge, or adjust local transition probabilities such as `P_ij`.

**The Impact:** Updating the representation can become more deterministic, inspectable, and localized. It does not replace learned neural capability, but it offers a path toward lower-cost maintenance and better control over explicit knowledge updates.

## Closing

MML is a proposal to move known patterns out of repeated stochastic rediscovery and into durable, inspectable structure.

LLMs remain valuable for discovering patterns, handling ambiguity, and exploring unknown spaces. But once a pattern is stable enough to be reused, MML gives it a different home: a graph where relationships can be inspected, weighted, updated, and governed.

That is the sustainability hypothesis. The goal is to give stable knowledge an executable home and reserve stochastic exploration for places where it adds value. Performance and energy advantages remain claims to test under the [research contract](Research-Contract.md).
