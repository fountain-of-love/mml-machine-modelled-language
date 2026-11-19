"""Machine Modelled Language's deterministic runtime kernel.

The packages below own representation, compilation, execution, composition,
and navigation. They accept governed semantic inputs and expose inspectable
runtime behavior; fixture construction and evidence publication live in the
separate :mod:`experiments` surface.

The names exported here are the supported MML runtime entry points. Deeper
module paths remain available for implementation-level work, but callers that
build integrations should prefer this facade or the explicitly documented
package facades.
"""

from .combinatorial_uniqueness.combinatorial_uniqueness_flow import (
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
from .knowledge_state_execution.execute_knowledge_state import (
    KnowledgeExecution,
    KnowledgeFact,
    KnowledgeState,
    compile_knowledge_state,
    execute,
    replace_fact,
)
from .semantic_representation.graph import (
    GraphModel,
    graph_snapshot_id,
    stable_sentence_id,
)
from .semantic_representation.governed_coordinates import (
    CodedSemanticQuery,
    GovernedCoordinateBasis,
    SemanticEntity,
    coordinate_identity,
    decode_query,
    encode_query,
    represent_coordinate_basis,
    validate_query,
)

__all__ = (
    "CodedSemanticQuery",
    "CombinatorialUniquenessFlow",
    "CompositionExecution",
    "CompiledSemanticState",
    "GraphModel",
    "GovernedCoordinateBasis",
    "GovernedSemanticState",
    "INVALID",
    "KnowledgeExecution",
    "KnowledgeFact",
    "KnowledgeState",
    "PrefixMeasurement",
    "RESOLVED",
    "SemanticEntity",
    "UNRESOLVED",
    "ValidityPolicy",
    "compile_knowledge_state",
    "coordinate_identity",
    "decode_query",
    "encode_query",
    "execute",
    "graph_snapshot_id",
    "replace_fact",
    "represent_coordinate_basis",
    "stable_sentence_id",
    "validate_query",
)
