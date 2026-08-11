# Experiment 3.2 — Governed Legal Qualification

## Atomic Claim

> Independent legal, governance, evidential, and processing dimensions can narrow a direct semantic qualification, while unsupported combinations remain insufficient and numerical activation cannot promote epistemic status.

Experiment 3.2 tests direct legal qualification, contrast, governed refusal, and epistemic non-promotion over one synthetic doctrine-oriented state.

It does not test physical identification, cross-level semantic transition, natural-language interpretation, factual adjudication, or generalization.

## Fixture

The experiment uses only:

```text
combinatorial_uniqueness_legal_banking_state_v1.json
governed_legal_qualification_probes_v1.json
```

The physical state and all `cross_level_probes` are absent from the experiment fixture and outside its boundary.

## Treatments

1. Twelve direct independent legal-qualification probes.
2. Three unmatched same-family redundant controls.
3. Three unsupported legal compositions.
4. One two-branch restriction-lawfulness contrast.
5. All 24 permutations of every four-coordinate direct probe.
6. Every leave-one-coordinate-out ablation.
7. Epistemic-classification preservation.

## Verdict Contract

The claim-specific verdict is `LOCALLY_CONSISTENT` or `INCONSISTENT`. Generalization is reported separately as `UNTESTED` until independently authored probes follow a state freeze.

`RESOLVED` identifies only a synthetic semantic region. It does not establish facts, duties, liability, or a legal violation.

## Commands And Artifacts

```bash
make experiment-3-2
make experiment-3-2-benchmark
make experiment-3-2-check
```

```text
benchmark/results/governed-legal-qualification-v1.json
docs/benchmark/results/governed-legal-qualification-v1.md
```

The [OSCARC report](results/governed-legal-qualification-v1.md) and machine-readable companion form one reproducible evidence pair.
