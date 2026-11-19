# CI and Reproducibility

MML treats reproducibility as a repository contract. A clean checkout must be
able to run the runtime tests, replay the research fixtures, and verify the
checked-in evidence without rewriting it.

## Supported baseline

The maintained baseline is:

- Python `3.9`
- NumPy `2.0.2`, pinned in [`requirements.txt`](../requirements.txt)
- a POSIX shell with `make`

The benchmark artifacts retain runtime provenance, including Python, NumPy,
host, and numerical-library details where relevant. Those fields document the
execution environment; they are not themselves scientific measurements.

## Clean-checkout verification

From the repository root:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
make ci
```

`make ci` is the non-mutating release gate. It runs the unit suite and all
checked-in benchmark and retrieval artifact checks. It must not call `--write`
or modify source, data, benchmark JSON, or report files.

The same gate is executed by [GitHub Actions](../.github/workflows/ci.yml) on
the pinned Python baseline. The workflow uses a fixed Ubuntu runner so the
verification environment is explicit rather than accidental.

## Evidence lifecycle

`--check` means **replay and compare**. It validates deterministic execution,
schema and mechanism contracts, and equality of stable evidence against the
checked-in artifact pair.

`--write` means **regenerate and review**. Use the named `make` target only
after an intentional code, fixture, protocol, or artifact change. Review the
resulting JSON and Markdown together, including updated source hashes and
provenance, before committing them.

Examples:

```bash
make benchmark-check
make experiment-3-1-check
make experiment-4-2-check
make benchmark
```

The first three commands are read-only checks. The final command rewrites the
semantic-representation evidence pair and is therefore a contributor action,
not a CI action.

## What is compared

Stable evidence includes measurements, execution traces, conformity decisions,
fixture identities, source hashes, and report text. Local runtime metadata and
generation timestamps are preserved in published artifacts but excluded from
freshness equality, because a CI runner and a workstation are not the same
machine. This keeps the verification boundary rigorous without confusing
provenance with scientific output.

The pinned NumPy baseline reduces numerical drift. If a future backend change
produces meaningful output differences, update the protocol and artifact pair
deliberately; do not weaken the comparison by adding broad tolerances silently.

## Reproducing a changed artifact

1. Run the focused `--check` command and identify the owning benchmark.
2. Inspect the source, fixture, protocol, and artifact identity changes.
3. Run the owning `--write` target locally.
4. Run `make ci` again.
5. Review the machine-readable JSON and human-readable report together.

The repository is ready to publish when the working tree contains only the
intentional source, documentation, and evidence changes and `make ci` passes
without mutation.
