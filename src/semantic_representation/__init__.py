"""Programme 1: explicit semantic representation under fixed mathematics.

This package establishes the representation boundary: semantic identity is
made explicit before the numerical activation machinery is run.
"""

from .graph import GraphModel, graph_snapshot_id, stable_sentence_id

__all__ = ("GraphModel", "graph_snapshot_id", "stable_sentence_id")
