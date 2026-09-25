# Compiled Relation-Specific Semantic Operator

This slice makes the repository's intended MML architecture executable for one
bounded relation family:

```text
governed relation records
  -> relation-specific sparse layers
  -> versioned policy coefficients
  -> immutable compiled operator
  -> repeatable field propagation
```

The implementation lives in
`src/knowledge_state_execution/compiled_semantic_operator.py`.

Each positive relation type is retained as its own CSR-like layer. `supports`,
`requires`, and `qualifies` remain inspectable after compilation. A policy
assigns explicit non-negative coefficients to relation types; the weighted
layers are combined and normalized only at execution time. This means changing
the policy changes the operator identity and can change the result without
changing the governed source records.

Contradictions are retained in the source contract but are not silently turned
into negative propagation edges. They are currently excluded from this positive
operator, matching the existing `GraphModel` boundary. A future negative
evidence operator can consume them explicitly.

The state is content-addressed by canonical source records, vocabulary, policy,
and compiled arrays. Arrays and mappings are immutable. Rebuilding equivalent
inputs in a different order produces the same snapshot. Repeated propagation
visits compiled edges rather than dense matrix cells; the benchmark reports
this as an operation-count comparison and records wall-clock measurements as
descriptive engineering evidence only.

## Research boundary

This is a functional implementation slice, not confirmation of the full MML
hypothesis. It does not establish that a coefficient policy is semantically
correct, that sparse execution wins at public-graph scale, or that relation
composition provides validated reasoning. The next research step is a frozen,
independently authored relation fixture with ablations for each relation type,
policy coefficient, and dense reconstruction control.
