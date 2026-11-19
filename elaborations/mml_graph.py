"""Compatibility exports for the runtime-owned semantic graph.

Graph construction and execution belong to the runtime representation layer.
This module remains as a stable import path for existing elaborations,
experiments, and research notebooks while they migrate to the public owner:
``src.semantic_representation.graph``.
"""

from src.semantic_representation.graph import (
    ALGORITHM_VERSION,
    GOVERNED_ID,
    POSITIVE_RELATIONS,
    RELATION_MULTIPLIERS,
    RELATION_TYPES,
    SENTENCE_ID,
    GraphModel,
    graph_snapshot_id,
    load_aliases,
    load_relations,
    stable_sentence_id,
    tokenize,
)

__all__ = (
    "ALGORITHM_VERSION",
    "GOVERNED_ID",
    "POSITIVE_RELATIONS",
    "RELATION_MULTIPLIERS",
    "RELATION_TYPES",
    "SENTENCE_ID",
    "GraphModel",
    "graph_snapshot_id",
    "load_aliases",
    "load_relations",
    "stable_sentence_id",
    "tokenize",
)
