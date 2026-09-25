"""Descriptive benchmark for compiled relation-specific semantic execution."""

from __future__ import annotations

import argparse
import json
import statistics
import time
from pathlib import Path

import numpy as np

from src.knowledge_state_execution.compiled_semantic_operator import (
    SemanticOperatorPolicy,
    compile_semantic_operator,
)


ROOT = Path(__file__).resolve().parents[2]
RESULT_PATH = ROOT / "benchmark" / "results" / "semantic-operator-v1.json"
BENCHMARK_VERSION = "semantic-operator-v1"


def build_fixture(node_count: int = 200, edges_per_node: int = 3):
    vocab = tuple(f"node-{index}" for index in range(node_count))
    relations = []
    relation_types = ("supports", "requires", "qualifies")
    for source in range(node_count):
        for offset in range(1, edges_per_node + 1):
            target = (source + offset * 7) % node_count
            relation = relation_types[(source + offset) % len(relation_types)]
            relations.append({
                "id": f"r-{source}-{offset}",
                "source": vocab[source],
                "relation": relation,
                "target": vocab[target],
                "weight": 1.0,
            })
    return vocab, tuple(relations)


def _timed(operation, repetitions: int = 31) -> dict[str, int]:
    samples = []
    for _ in range(repetitions):
        started = time.perf_counter_ns()
        operation()
        samples.append(time.perf_counter_ns() - started)
    return {
        "repetitions": repetitions,
        "median_ns": int(statistics.median(samples)),
        "minimum_ns": min(samples),
    }


def run_experiment(node_count: int = 200, edges_per_node: int = 3) -> dict:
    vocab, relations = build_fixture(node_count, edges_per_node)
    policy = SemanticOperatorPolicy(
        "retrieval-v1",
        {"supports": 1.0, "requires": 0.8, "qualifies": 0.5},
    )
    state = compile_semantic_operator(vocab, relations, policy)
    field = np.zeros(node_count)
    field[0] = 1.0
    dense_cells = node_count * node_count
    sparse_edges = state.edge_count
    result = {
        "benchmark": BENCHMARK_VERSION,
        "fixture": {
            "nodes": node_count,
            "source_relations": len(relations),
            "compiled_edges": sparse_edges,
        },
        "state": {
            "snapshot_id": state.snapshot_id,
            "policy_id": state.policy.policy_id,
            "relation_types": list(state.relation_types),
        },
        "work_model": {
            "dense_matrix_cells_per_step": dense_cells,
            "compiled_edge_visits_per_step": sparse_edges,
            "dense_to_sparse_ratio": dense_cells / sparse_edges if sparse_edges else None,
        },
        "timing": {"compile": _timed(lambda: compile_semantic_operator(vocab, relations, policy)),
                   "compiled_propagate": _timed(lambda: state.propagate(field, steps=3))},
    }
    replay = compile_semantic_operator(tuple(reversed(vocab)), tuple(reversed(relations)), policy)
    if replay.snapshot_id != state.snapshot_id or not np.isclose(state.propagate(field).sum(), 1.0):
        raise AssertionError("compiled semantic operator failed deterministic replay")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = run_experiment()
    if args.write:
        RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
        RESULT_PATH.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    if args.check:
        assert result["work_model"]["dense_to_sparse_ratio"] > 10
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
