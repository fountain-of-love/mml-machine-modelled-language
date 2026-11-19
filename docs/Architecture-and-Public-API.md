# Architecture and Public API

MML is deliberately organized as a deterministic runtime with governed inputs
and replaceable research surfaces. The repository therefore distinguishes
**ownership** from **usage**: a module may use a capability without owning the
contract that defines it.

## Layer ownership

```text
src/                         Runtime kernel and supported API
  semantic_representation/   governed identity, graph state, grounding
  knowledge_state_execution/ immutable compilation and execution
  combinatorial_uniqueness/ composition, validity, refusal states
  semantic_navigation/       navigation over compiled candidate state
  helpers/                   shared serialization, hashing, provenance

experiments/                 fixtures, benchmarks, controls, reports
elaborations/                richer demonstrations and application adapters
tests/                       executable contracts for all of the above
```

The dependency direction is inward toward the runtime:

```text
experiments  ─┐
elaborations ─┼──> src runtime
tests        ─┘
```

The runtime does not import fixtures, benchmark publication, or application
demos. A richer implementation can depend on the runtime; it does not become
part of the runtime merely because a benchmark exercises it.

## Supported imports

Integration code should prefer the root facade:

```python
from src import (
    CombinatorialUniquenessFlow,
    GraphModel,
    ValidityPolicy,
    compile_knowledge_state,
)
```

Package facades are also supported for focused integrations, for example
`src.semantic_representation` and `src.combinatorial_uniqueness`. Direct
module imports are appropriate for implementation work and focused tests, but
they are not required to be stable across internal refactoring.

`src.semantic_representation.graph` owns the canonical deterministic graph
implementation. `elaborations.mml_graph` remains a compatibility import path
for existing notebooks and demonstrations; it re-exports the runtime-owned
symbols and is not a second implementation.

## Contract rules

1. Governed semantic inputs enter through explicit runtime contracts.
2. Compilation produces immutable, inspectable state with a content identity.
3. Execution returns typed outcomes, including refusal and unresolved states.
4. Experiments publish evidence about runtime behavior; they do not define it.
5. Elaboration code may enrich the runtime, but the runtime must not depend on
   elaboration-only mechanics.
6. Compatibility exports are allowed during migration, but canonical ownership
   must be singular and documented.

This is intentionally a narrow public surface. MML's architectural claim is
stronger when the runtime is small, explicit, deterministic, and independently
replayable.
