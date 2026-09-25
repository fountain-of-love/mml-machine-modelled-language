"""Compile governed relation layers into a compact executable operator."""

from __future__ import annotations

from dataclasses import dataclass
import re
from types import MappingProxyType
from typing import Mapping, Sequence

import numpy as np

from src.helpers.hashing import sha256_bytes
from src.helpers.json_io import canonical_json_bytes


ALGORITHM_VERSION = "compiled-semantic-operator-v1"
POSITIVE_RELATIONS = frozenset({"supports", "requires", "qualifies"})
NEGATIVE_RELATIONS = frozenset({"contradicts"})
ALL_RELATIONS = POSITIVE_RELATIONS | NEGATIVE_RELATIONS


def _readonly(array: np.ndarray) -> np.ndarray:
    result = np.frombuffer(array.tobytes(order="C"), dtype=array.dtype).reshape(array.shape)
    result.setflags(write=False)
    return result


@dataclass(frozen=True)
class SemanticOperatorPolicy:
    """Versioned coefficients that select a task-specific relation operator."""

    policy_id: str
    coefficients: Mapping[str, float]

    def __post_init__(self) -> None:
        if not isinstance(self.policy_id, str) or not re.search(r"-v[0-9]+$", self.policy_id):
            raise ValueError("semantic operator policy requires a versioned policy_id ending in -vN")
        unknown = set(self.coefficients) - ALL_RELATIONS
        if unknown:
            raise ValueError(f"unknown semantic relation coefficients: {sorted(unknown)}")
        normalized = {relation: float(self.coefficients.get(relation, 0.0)) for relation in sorted(ALL_RELATIONS)}
        if any(not np.isfinite(value) or value < 0 for value in normalized.values()):
            raise ValueError("semantic relation coefficients must be finite and non-negative")
        if not any(normalized[relation] for relation in POSITIVE_RELATIONS):
            raise ValueError("semantic operator policy requires a positive relation coefficient")
        object.__setattr__(self, "coefficients", MappingProxyType(normalized))


@dataclass(frozen=True)
class CompiledRelationLayer:
    """One immutable weighted relation layer in CSR form."""

    relation: str
    indptr: np.ndarray
    indices: np.ndarray
    values: np.ndarray
    edge_count: int

    def propagate(self, field: np.ndarray) -> np.ndarray:
        if field.ndim != 1 or field.shape[0] != self.indptr.shape[0] - 1:
            raise ValueError("field shape does not match compiled semantic operator")
        result = np.zeros_like(field, dtype=float)
        for source in range(field.shape[0]):
            start, end = self.indptr[source], self.indptr[source + 1]
            if start != end:
                np.add.at(result, self.indices[start:end], field[source] * self.values[start:end])
        return result


@dataclass(frozen=True)
class CompiledSemanticOperator:
    """Persistent executable state for relation-specific semantic propagation."""

    vocab: tuple[str, ...]
    word2idx: Mapping[str, int]
    policy: SemanticOperatorPolicy
    layers: Mapping[str, CompiledRelationLayer]
    snapshot_id: str
    source_count: int

    @property
    def relation_types(self) -> tuple[str, ...]:
        return tuple(self.layers)

    @property
    def edge_count(self) -> int:
        return sum(layer.edge_count for layer in self.layers.values())

    def propagate(self, field: Sequence[float], *, steps: int = 1) -> np.ndarray:
        """Propagate a field through the policy-selected positive layers."""
        if steps < 1:
            raise ValueError("propagation steps must be positive")
        current = np.asarray(field, dtype=float)
        if current.ndim != 1 or current.shape[0] != len(self.vocab):
            raise ValueError("field shape does not match compiled semantic operator")
        for _ in range(steps):
            next_field = np.zeros_like(current)
            for layer in self.layers.values():
                next_field += layer.propagate(current)
            total = next_field.sum()
            current = next_field / total if total else next_field
        return current


def _compile_layer(
    relation: str,
    edges: list[tuple[int, int, float]],
    node_count: int,
) -> CompiledRelationLayer:
    rows: list[list[tuple[int, float]]] = [[] for _ in range(node_count)]
    for source, target, value in edges:
        rows[source].append((target, value))
    indptr = [0]
    indices: list[int] = []
    values: list[float] = []
    for row in rows:
        totals: dict[int, float] = {}
        for target, value in row:
            totals[target] = totals.get(target, 0.0) + value
        for target in sorted(totals):
            indices.append(target)
            values.append(totals[target])
        indptr.append(len(indices))
    return CompiledRelationLayer(
        relation=relation,
        indptr=_readonly(np.asarray(indptr, dtype=np.int64)),
        indices=_readonly(np.asarray(indices, dtype=np.int64)),
        values=_readonly(np.asarray(values, dtype=float)),
        edge_count=len(indices),
    )


def compile_semantic_operator(
    vocab: Sequence[str],
    relations: Sequence[Mapping[str, object]],
    policy: SemanticOperatorPolicy,
) -> CompiledSemanticOperator:
    """Compile governed relation records into immutable, sparse executable state."""
    ordered_vocab = tuple(sorted(set(vocab)))
    if not ordered_vocab:
        raise ValueError("semantic operator requires at least one vocabulary node")
    word2idx = {word: index for index, word in enumerate(ordered_vocab)}
    grouped: dict[str, list[tuple[int, int, float]]] = {relation: [] for relation in ALL_RELATIONS}
    canonical_records = []
    for record in relations:
        relation = str(record["relation"])
        source = str(record["source"])
        target = str(record["target"])
        if relation not in ALL_RELATIONS:
            raise ValueError(f"unknown semantic relation: {relation}")
        if source not in word2idx or target not in word2idx:
            raise ValueError("relation endpoints must be declared vocabulary nodes")
        weight = float(record["weight"])
        if not np.isfinite(weight) or weight <= 0:
            raise ValueError("relation weights must be finite and positive")
        coefficient = policy.coefficients[relation]
        if coefficient:
            grouped[relation].append((word2idx[source], word2idx[target], weight * coefficient))
        canonical_records.append({
            "id": str(record.get("id", "")),
            "source": source,
            "relation": relation,
            "target": target,
            "weight": weight,
            "coefficient": coefficient,
        })

    layers = {
        relation: _compile_layer(relation, grouped[relation], len(ordered_vocab))
        for relation in sorted(POSITIVE_RELATIONS)
        if grouped[relation]
    }
    payload = {
        "algorithm": ALGORITHM_VERSION,
        "vocab": ordered_vocab,
        "policy_id": policy.policy_id,
        "coefficients": dict(policy.coefficients),
        "relations": sorted(canonical_records, key=lambda record: (record["relation"], record["id"])),
        "layers": {
            relation: {
                "indptr": layer.indptr.tolist(),
                "indices": layer.indices.tolist(),
                "values": layer.values.tolist(),
            }
            for relation, layer in layers.items()
        },
    }
    snapshot_id = sha256_bytes(canonical_json_bytes(payload))
    return CompiledSemanticOperator(
        vocab=ordered_vocab,
        word2idx=MappingProxyType(word2idx),
        policy=policy,
        layers=MappingProxyType(layers),
        snapshot_id=snapshot_id,
        source_count=len(canonical_records),
    )
