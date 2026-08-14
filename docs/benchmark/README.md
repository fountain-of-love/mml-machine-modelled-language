# Benchmarks

This directory contains shared benchmark methodology, the cross-programme benchmark proposal, legacy retrieval diagnostics, and links to programme-owned evidence. Each capability now keeps its protocol and human-readable results beside its definition under [`docs/capabilities/`](../capabilities/README.md); machine-readable artifacts remain in the repository-level `benchmark/` tree. Benchmarks are evidence instruments, not capability definitions.

The benchmark programme follows MML's three hypotheses and reports a separate evidence boundary for each:

| Hypothesis | Benchmark | Current status |
| --- | --- | --- |
| **1. Representation** | [Capability definition](../capabilities/semantic-representation/README.md) · [Experiment 1 protocol](../capabilities/semantic-representation/experiment.md) | Identity-focused development benchmark implemented. |
| **2. Knowledge State Execution** | [Capability definition](../capabilities/knowledge-state-execution/README.md) · [Experiment 2 protocol](../capabilities/knowledge-state-execution/experiment.md) | One bounded typed-chain development experiment implemented. |
| **3. Combinatorial Uniqueness** | [Capability definition](../capabilities/combinatorial-uniqueness/README.md) · [Experiment 3 protocol](../capabilities/combinatorial-uniqueness/experiment.md) · [3.1 direct intersection](../capabilities/combinatorial-uniqueness/results/direct-intersection-v1.md) · [3.2 governed qualification](../capabilities/combinatorial-uniqueness/results/governed-legal-qualification-v1.md) · [3.3 cross-level transition](../capabilities/combinatorial-uniqueness/results/cross-level-semantic-transition-v1.md) | Three atomic authored development studies distinguish locally consistent direct intersection and legal qualification from consistent explicit stage-scoped transition; held-out generalization remains untested. |

In compact form: **Represent meaning. Compile knowledge. Compose concepts.** A result for one row is not evidence for the other two.

The earlier [combined Experiment 3 result](../capabilities/combinatorial-uniqueness/results/v1.md) is `SUPERSEDED_BY_DECOMPOSITION`: it no longer acts as the programme-level verdict. The [cross-level root-cause analysis](../capabilities/combinatorial-uniqueness/studies/cross-level-root-cause.md) traces its unresolved access-to-evidence trajectory to the difference between flat conjunction and semantic transition. Experiment 3.3 tests explicit stage-local scope while retaining that failed conjunction as its control.

Run the Representation benchmark with `make benchmark-check`, or regenerate its JSON and Markdown evidence with `make benchmark`.

The [Experiment 1 blueprint](../capabilities/semantic-representation/experiment.md) defines the stronger factorial, held-out, sham-control, and representation-ladder protocol that the current identity-focused report only begins to address.

The orthogonal [Knowledge State Execution Experiment](../capabilities/knowledge-state-execution/results/v1.md) asks whether one exact semantic consequence can be compiled into governed state and reused without rereading the source knowledge for each query. Run it with `make knowledge-state-benchmark-check`, or regenerate its JSON and Markdown evidence with `make knowledge-state-benchmark`. Its local source-reconstruction treatment is not an LLM measurement.

The [Experiment 2 blueprint](../capabilities/knowledge-state-execution/experiment.md) defines the stronger reuse-curve, refusal, mutation, provenance, and full-cost-accounting protocol.

Benchmark and scientific results are reported using the [OSCARC methodology](oscarc-methodology.md), separating observation, standard, chronology/context, actions, measured result, conformity judgment, and recommendation.

## Legacy retrieval diagnostic

The retrieval diagnostic remains an **application-level regression**, not a hypothesis benchmark, and can be run with `make retrieval-benchmark-check`.

The diagnostic is intentionally small. It checks that the current retrieval application remains deterministic and clears low development floors on two authored fixtures. Because it combines representation, governed query inputs, compilation, scoring, and retrieval judgments, it cannot isolate or validate any one hypothesis and does not decide whether MML succeeds as executable semantic infrastructure.

It compares five independently named treatments:

- lexical overlap;
- TF-IDF cosine;
- co-occurrence MML;
- typed MML with governed aliases and relations;
- one named multiplicative MML/lexical hybrid.

TF-IDF and MML are both deterministic here. TF-IDF executes term statistics fitted on the evaluation documents. MML executes a separately constructed graph. Their comparison describes retrieval behavior; universal superiority over TF-IDF is neither expected nor required.

The inputs are intentionally asymmetric. MML receives supervised concept mappings and negative semantic evidence from the query contract; lexical overlap and TF-IDF receive surface terms only. That governed query engineering is part of MML, not an accidental advantage, but the comparison is between end-to-end treatments rather than identical-input algorithms. A future ablation should continue to report terms-only MML beside governed-query MML so the contribution remains visible.

The active prototype checks are limited to:

- artifact hashes and fixture shape;
- the balanced 10/10 bank-sense construction;
- deterministic replay;
- low absolute retrieval floors;
- regression against the recorded reference.

They are opportunities for early failure detection, not production-grade integrity guarantees. The current runner does not yet provide exhaustive schema/judgment validation, signing, protected release history, independent assessment, or held-out evidence. `python3 retrieval_benchmark.py --write` refuses to replace a known regressed reference unless the operator explicitly supplies `--accept-regression`; that override should accompany a documented rationale.

Run `python3 retrieval_benchmark.py --write` to regenerate [the report](results/v1.md) and `make retrieval-benchmark-check` to verify without rewriting it.

Earlier work on challenge slices, seven rankers, hybrid selection, sensitivity tuning, acceptance verdicts, and provisional locality thresholds is preserved in [the archived research note](archive/v1-retrieval-research.md). Those findings remain available without organizing the project around them.

The challenge diagnostics are still relevant as stress tests, especially for semantic distance and hard negatives. They are not treated as peer-equivalence verdicts: supervised MML, unsupervised term statistics, and self-supervised language models solve different parts of the problem and carry different construction costs.

The hybrid is active and reproducible as `mml_typed × (0.2 + 0.8 × lexical_overlap)`. It preserves the useful observation that lexical evidence and explicit semantic activation may be complementary. There is no parameter search, calibration tournament, or claim that this fixed formula is optimal.

The separate `make update-demo` command demonstrates a governed relation change, its observable consequences, and exact restoration. It reports propagation descriptively and does not convert the percentage of changed scores into a locality verdict.

Version 1 remains synthetic development evidence with one assessor. It is not held-out validation or a legal-effectiveness claim.
