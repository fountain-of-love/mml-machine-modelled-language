# Semantic Flow Application Architecture

## A Tiny Experiment With Architectural Direction

The current Words Carry Weight experiment is deliberately small, but it is not architecturally neutral. A few sentences, two meanings of `bank`, one transition model, and one Personalized PageRank strategy already establish a direction for a much larger system.

MML has a canonical **research triad**:

> **Represent meaning. Compile knowledge. Compose concepts.**

This document describes the smaller **operational flow** through which the current application begins to exercise those hypotheses:

> **Ground the known. Focus the intended. Activate the related.**

In functional terms:

> **Ground meaning -> Focus intent -> Activate relationships**

More concretely:

```text
Corpus --ground--> semantic identity <--focus-- Query
                         |
                         `--activate--> semantic field
```

The two levels relate as follows:

```text
Represent meaning
  -> ground corpus identities
  -> focus query identity

Compile knowledge
  -> construct a reusable transition model

Compose concepts
  -> activate independent fields
  -> combine them into a task-specific intersection
```

The minimal experiment directly exercises grounding, focus, compilation, and single-field activation. The elaborated engine supplies independent multi-field activation and soft intersection. Those mechanisms make the hypotheses testable; they do not establish compiled-reuse or combinatorial-scaling advantages by themselves.

### Ground

A surface occurrence is connected to governed meaning:

```text
corpus "bank" -> bank_river
```

Grounding answers: **What does this occurrence mean in the represented knowledge?**

### Focus

An ambiguous query is narrowed to its intended meaning:

```text
query "bank" -> bank_river
```

Focus answers: **Which meaning is relevant to this intent?**

### Activate

The focused identity is executed through the compiled relationships:

```text
bank_river -> river, water, rain, watershed, ...
```

Activation answers: **What semantic field follows from this identity under this strategy?**

Grounding and focus approach the same identity from opposite sides. Activation carries that identity outward into its semantic field.

The experiment proposes this operational semantic flow:

```text
corpus occurrence -> grounding --+
                                 +-> semantic identity -> compile -> transition model
query expression  -> focus -------+                              |
                                                                  v
                                                         query strategy
                                                                  |
                                                                  v
                                                             activation
```

Each operation is a stable conceptual joint:

- **Ground:** identify what a corpus occurrence means.
- **Focus:** narrow a query expression to the intended semantic identity.
- **Activate:** execute a declared strategy and return the query-relative numerical distribution.

Within the operational flow, compilation prepares reusable state between grounded knowledge and runtime activation:

```text
grounded knowledge
       |
       v
    compile
       |
       v
transition model
       ^
       |
focused query
       |
       v
    activate
```

Likewise, Personalized PageRank is not part of the canonical research triad or the operational vocabulary. It is one way activation can be performed.

This is a fishbone architecture. The spine stays small and intelligible; each joint can spiral into a subsystem with multiple implementations:

```text
ground
  |- declared grounding
  |- lexical grounding
  `- ontology grounding

compile
  |- co-occurrence compiler
  |- relation-matrix compiler
  `- multiplex semantic-operator compiler

focus
  |- declared focus
  |- contextual focus
  `- multi-identity focus

activate
  |- Personalized PageRank
  |- bounded diffusion
  `- path-constrained activation
```

The current matrix and Personalized PageRank implementation are branches, not the definition of the system. The lasting application architecture is the operational flow and the contracts between its operations. Above it, the research architecture remains Represent–Compile–Compose.

## Proposed Application Shape

As the experiment grows, the functional representation can become a small composition spine:

```text
activate_grounded_focus.py
  SemanticGrounding
  SemanticFocus
  TransitionModel
  Activation
  ground(...)
  compile_transition_model(...)
  focus(...)
  activate(...)

semantic/
  grounding/      # interchangeable grounding implementations
  compilation/    # matrix, graph, and semantic-operator compilers
  focus/          # query interpretation implementations
  activation/     # Personalized PageRank and future strategies

words_carry_weight.py
  WordsCarryWeightFlow
  ground_and_compile(...)
  focus_and_activate(...)

experiment_fixture.py
  # fixture loading

representation_comparison.py
  # experiment and benchmark comparison

activation_console.py
  # console presentation

run_words_carry_weight.py
  # executable composition root

data/demonstration/
  # authored corpus, groundings, focuses, contexts, and probes
```

`activate_grounded_focus.py` is the small functional facade and contract layer. `words_carry_weight.py` coordinates those functions as an operational application service. Concrete implementations can grow behind the contracts. Demonstrations and benchmarks assemble the operational flow without becoming the architecture itself.

The dependency direction should remain simple:

```text
demonstration/application
        -> semantic-flow contracts
        -> selected implementations
        -> data
```

Grounding and focus must remain distinct even when they select the same identity. Grounding enters from corpus construction; focus enters from query interpretation. Activation occurs only after focus. Attention remains an inspiration-level analogy and does not name an implemented mechanism.

## Why The Foundation Matters

A tiny experiment can set a large direction because its names and boundaries become precedents. Future code, documentation, tests, prompts, and AI-generated extensions will imitate the first visible structure. A small ambiguity at the seed can become a distributed architectural assumption later.

For example:

- calling activation “focus” can merge query interpretation with numerical execution;
- calling every representation a graph can hide the matrix or operator that actually executes;
- putting corpus grounding inside an activation strategy can couple construction to runtime;
- naming Personalized PageRank as the mechanism can make one algorithm appear to define MML;
- allowing demonstration fixtures into the kernel can turn one use case into an accidental platform contract.

These errors are inexpensive to correct in a hundred-line experiment and expensive to remove after many modules, models, datasets, and agents depend on them.

## The Rocket Principle

Giving a software seed to AI can be like attaching it to a rocket. AI can reproduce patterns, fill directories, generate implementations, and extend abstractions at great speed. That acceleration is valuable only when the initial orientation is sound.

```text
small boundary drift
        x rapid AI replication
        x many implementation layers
        = large architectural deviation
```

The answer is not to avoid acceleration. It is to establish the launch coordinates carefully:

- define vocabulary before multiplying implementations;
- make important operations first-class;
- separate enduring contracts from current algorithms;
- encode boundaries in tests as well as prose;
- keep evidence claims proportional to the experiment;
- let new complexity grow from explicit variation points;
- revisit names whenever implementation and meaning diverge.

The purpose of the minimal experiment is therefore larger than proving that one matrix calculation runs. It establishes an orientation: richer governed meaning enters through grounding and focus, becomes executable through compilation, and produces inspectable activation through a selected activation strategy.

If that orientation is correct, AI can help each branch grow. If it is wrong, AI will help the error grow too.

## Current Boundary

Today, the repository implements the pieces across two files:

- [`activate_grounded_focus.py`](../activate_grounded_focus.py) contains first-class semantic grounding and focus, the transition model, activation result, activation-strategy contract, Personalized PageRank implementation, compiler, and activation facade.
- [`words_carry_weight.py`](../words_carry_weight.py) contains the operational construction and runtime flows.
- [`experiment_fixture.py`](../experiment_fixture.py) owns external fixture loading.
- [`representation_comparison.py`](../representation_comparison.py) owns comparison for experiments and benchmarks.
- [`activation_console.py`](../activation_console.py) owns console presentation.
- [`run_words_carry_weight.py`](../run_words_carry_weight.py) is the executable composition root for the current demonstration.

The filename expresses the flow as a small sentence: **activate grounded focus**. Grounding and focus prepare a meaning-bearing coordinate; activation executes its relationships. Concrete grounding, focus, compilation, and activation implementations should move into branches only when an actual next experiment requires more than one implementation.

The accompanying [vocabulary contract](activate-grounded-focus-vocabulary.md) remains authoritative for the current names and their drift boundaries.
