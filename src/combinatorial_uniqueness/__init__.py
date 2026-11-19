"""Programme 3: runtime composition of governed semantic coordinates.

Composition remains explicit and stage-aware: candidate regions, transitions,
and refusal states are inspectable outcomes of the represented input.
"""

from .combinatorial_uniqueness_flow import (
    INVALID,
    RESOLVED,
    UNRESOLVED,
    CombinatorialUniquenessFlow,
    CompositionExecution,
    CompiledSemanticState,
    GovernedSemanticState,
    PrefixMeasurement,
    ValidityPolicy,
)

__all__ = (
    "INVALID",
    "RESOLVED",
    "UNRESOLVED",
    "CombinatorialUniquenessFlow",
    "CompositionExecution",
    "CompiledSemanticState",
    "GovernedSemanticState",
    "PrefixMeasurement",
    "ValidityPolicy",
)
