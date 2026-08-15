# Shared Helper Contracts

The modules under `src/helpers` contain application-wide mechanics. They do not
decide scientific meaning, evidence sufficiency, or programme-specific policy.

## Design principles

1. **Canonical intermediate layers.** Hashing, serialization, text persistence,
   artifact coordination, provenance, and command orchestration are separate
   because they have different reasons to change.
2. **Loose coupling.** Higher layers depend on narrow capabilities. Artifact
   publication receives already-rendered text; it does not know which renderer
   produced it.
3. **Build only demonstrated variability.** The repository currently requires
   Markdown reports, so each programme selects `markdown_report` and a `.md`
   report path. There is no renderer registry or strategy hierarchy until a
   second real output format requires one.
4. **Configuration selects policy; helpers execute mechanics.** A programme's
   report path and `ResearchCommand.render` callback express the current format
   choice. Generic persistence remains format-neutral.
5. **Abstractions must earn their cost.** A shared layer is retained when it
   removes repeated policy-neutral behavior, creates one explicit contract, or
   isolates likely change. Convenience aliases without an independent reason to
   change should be removed.
6. **Line count is evidence, not the objective.** Added code is justified only
   by clearer contracts, safer reuse, testability, or maintainability. Future
   flexibility alone is not sufficient without a credible change boundary.

The current canonical flow is:

```text
programme result
  -> programme-selected renderer (currently Markdown)
  -> plain text
  -> format-neutral artifact coordination
  -> write_text()
```

## Provenance contract

- `utc_now_iso()` supplies a timezone-aware UTC generation instant.
- `runtime_identity()` supplies named runtime facts selected by the caller.
- `hash_named_artifacts()` binds caller-owned semantic names to exact file bytes.
- The calling capability decides which packages, files, and names are required
  for its evidence boundary.

## Research command contract

`ResearchCommand` separates common command sequencing from research policy:

1. parse exactly one of `--write` and `--check`;
2. run the programme;
3. apply its optional scientific validation;
4. write artifacts or check references;
5. render the programme-owned report.

The command helper never defines conformity criteria, reference-comparison
policy, report content, output format, or exit messages. The `render` callback
is the programme-level configuration point; it currently references a Markdown
renderer but returns ordinary text.

## Text persistence contract

`write_text()` persists UTF-8 text and creates its parent directory. It does not
offer `write_markdown()`, because Markdown is a rendering choice rather than a
persistence concern. If another human-readable format becomes necessary, it
should supply another renderer while continuing to use the same text boundary.

## Canonical serialization contract

`canonical_json_bytes()` sorts object keys and uses compact separators. Callers
must explicitly provide any conversion policy for non-JSON types. Content
identities hash those canonical bytes through `sha256_bytes()`.
