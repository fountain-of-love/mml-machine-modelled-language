# Retrieval Diagnostic

The active benchmark is intentionally small. It checks that MML remains deterministic and useful on two authored development fixtures; it does not decide whether MML succeeds as executable semantic infrastructure.

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

They are opportunities for early failure detection, not production-grade integrity guarantees. The current runner does not yet provide exhaustive schema/judgment validation, signing, protected release history, independent assessment, or held-out evidence. `make benchmark` refuses to replace a known regressed reference unless the operator explicitly supplies `--accept-regression`; that override should accompany a documented rationale.

Run `make benchmark` to regenerate [the report](results/v1.md) and `make benchmark-check` to verify without rewriting it.

Earlier work on challenge slices, seven rankers, hybrid selection, sensitivity tuning, acceptance verdicts, and provisional locality thresholds is preserved in [the archived research note](archive/v1-retrieval-research.md). Those findings remain available without organizing the project around them.

The challenge diagnostics are still relevant as stress tests, especially for semantic distance and hard negatives. They are not treated as peer-equivalence verdicts: supervised MML, unsupervised term statistics, and self-supervised language models solve different parts of the problem and carry different construction costs.

The hybrid is active and reproducible as `mml_typed × (0.2 + 0.8 × lexical_overlap)`. It preserves the useful observation that lexical evidence and explicit semantic activation may be complementary. There is no parameter search, calibration tournament, or claim that this fixed formula is optimal.

The separate `make update-demo` command demonstrates a governed relation change, its observable consequences, and exact restoration. It reports propagation descriptively and does not convert the percentage of changed scores into a locality verdict.

Version 1 remains synthetic development evidence with one assessor. It is not held-out validation or a legal-effectiveness claim.
