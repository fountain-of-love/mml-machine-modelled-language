# MML Research Programme

Machine Modelled Language is organized around three independently testable foundation capabilities and one accumulated application capability:

> **Represent meaning. Compile knowledge. Compose concepts. Navigate governed knowledge.**

| Programme | Capability target | Canonical document |
| --- | --- | --- |
| **1. Semantic Representation** | Richer explicit meaning under fixed mathematics | [Semantic Representation](semantic-representation/README.md) |
| **2. Knowledge State Execution** | Reconstruction-at-use versus compiled reuse | [Knowledge State Execution](knowledge-state-execution/README.md) |
| **3. Combinatorial Uniqueness** | Specificity created through coordinate composition | [Combinatorial Uniqueness](combinatorial-uniqueness/README.md) |
| **4. Semantic Navigation** | Accumulated retrieval and navigation over represented, compiled, composed knowledge | [Semantic Navigation](semantic-navigation/README.md) |

These are research programmes, not benchmark names. Each programme has four distinct layers:

```text
capability definition
  -> architectural proposition
  -> controlled experiment protocol
  -> implementation and bounded evidence
```

- The **capability document** defines what the programme means, what it does not mean, its dependencies, required measurements, present evidence, and next research step.
- The **architectural proposition** explains why the capability might matter and what mechanism could support it.
- The **experiment protocol** defines interventions, controls, measurements, falsification criteria, freeze rules, and required artifacts.
- The **implementation and evidence** show what the repository currently executes and what the resulting observations do—and do not—support.

Evidence must not leak between programmes. Deterministic replay in a Representation experiment does not validate Knowledge State Execution. A compiled model in a composition experiment does not establish an amortization advantage. Semantic Navigation is intentionally cumulative, but a successful navigation application does not retroactively validate any upstream claim that has not been independently established.

The shared falsification and governance boundary is defined in the [MML Research Contract](../Research-Contract.md). Benchmark protocols and reports live under [`docs/benchmark/`](../benchmark/README.md) as research instruments beneath this structure.
