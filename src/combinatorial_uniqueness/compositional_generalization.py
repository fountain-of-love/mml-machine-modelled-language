"""Pairwise-only construction and zero-shot scoring for compositional generalization."""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from dataclasses import dataclass
from types import MappingProxyType
from typing import Callable, Mapping, Sequence

import numpy as np


@dataclass(frozen=True)
class FamilySpec:
    id: str
    labels: tuple[str, ...]
    coefficients: tuple[int, ...]


@dataclass(frozen=True)
class EntitySignature:
    id: str
    latent: tuple[int, ...]
    coordinates: tuple[str, ...]


@dataclass(frozen=True)
class PairwiseCoordinateState:
    state_id: str
    coordinates: tuple[str, ...]
    coordinate_index: Mapping[str, int]
    pair_counts: np.ndarray
    transition: np.ndarray
    embedding: np.ndarray
    training_entity_count: int
    stored_relation_arity: int
    snapshot_id: str


@dataclass(frozen=True)
class RankedTarget:
    top_candidate: str
    target_rank: int
    tie_count_at_target: int
    target_margin: float
    reciprocal_rank: float
    tie_adjusted_credit: float


def coordinate(family: FamilySpec, value: int) -> str:
    return f"{family.id}:{family.labels[value]}"


def signature_for_latent(
    latent: Sequence[int], families: Sequence[FamilySpec], radix: int,
) -> tuple[str, ...]:
    values = (
        sum(coefficient * digit for coefficient, digit in zip(family.coefficients, latent)) % radix
        for family in families
    )
    return tuple(coordinate(family, value) for family, value in zip(families, values))


def materialize_split(
    families: Sequence[FamilySpec], radix: int,
) -> tuple[tuple[EntitySignature, ...], tuple[EntitySignature, ...]]:
    """Generate the declared train/test partition without storing it in compiled state."""
    training, held_out = [], []
    for latent in itertools.product(range(radix), repeat=4):
        signature = EntitySignature(
            "entity_" + "".join(str(value) for value in latent),
            tuple(latent),
            signature_for_latent(latent, families, radix),
        )
        (held_out if sum(latent) % radix == 0 else training).append(signature)
    return tuple(training), tuple(held_out)


def _readonly(values: np.ndarray) -> np.ndarray:
    result = np.asarray(values, dtype=float)
    result.setflags(write=False)
    return result


def _embedding_from_pair_counts(pair_counts: np.ndarray, rank: int = 16) -> np.ndarray:
    total = float(pair_counts.sum())
    row = pair_counts.sum(axis=1, keepdims=True)
    col = pair_counts.sum(axis=0, keepdims=True)
    expected = row @ col / total if total else np.ones_like(pair_counts)
    with np.errstate(divide="ignore", invalid="ignore"):
        ppmi = np.maximum(np.log2(np.divide(
            pair_counts * total,
            row @ col,
            out=np.ones_like(pair_counts),
            where=(pair_counts > 0) & (expected > 0),
        )), 0.0)
    left, singular, _ = np.linalg.svd(ppmi, full_matrices=False)
    width = min(rank, len(singular))
    return left[:, :width] * np.sqrt(singular[:width])


def compile_pairwise_state(
    state_id: str,
    families: Sequence[FamilySpec],
    training: Sequence[EntitySignature],
) -> PairwiseCoordinateState:
    """Compile only pair counts; complete training signatures are not retained."""
    coordinates = tuple(
        coordinate(family, value)
        for family in families
        for value in range(len(family.labels))
    )
    index = {item: position for position, item in enumerate(coordinates)}
    counts = np.zeros((len(coordinates), len(coordinates)), dtype=float)
    for entity in training:
        positions = [index[item] for item in entity.coordinates]
        for left, right in itertools.combinations(positions, 2):
            counts[left, right] += 1.0
            counts[right, left] += 1.0
    row_sums = counts.sum(axis=1, keepdims=True)
    transition = np.divide(counts, row_sums, out=np.zeros_like(counts), where=row_sums > 0)
    embedding = _embedding_from_pair_counts(counts)
    encoded = json.dumps({
        "state_id": state_id,
        "coordinates": coordinates,
        "pair_counts": counts.astype(int).tolist(),
        "stored_relation_arity": 2,
    }, sort_keys=True, separators=(",", ":")).encode()
    return PairwiseCoordinateState(
        state_id,
        coordinates,
        MappingProxyType(index),
        _readonly(counts),
        _readonly(transition),
        _readonly(embedding),
        len(training),
        2,
        "sha256:" + hashlib.sha256(encoded).hexdigest(),
    )


def personalized_field(
    state: PairwiseCoordinateState,
    query_coordinate: str,
    damping: float = 0.85,
    iterations: int = 100,
    tolerance: float = 1e-12,
) -> np.ndarray:
    if query_coordinate not in state.coordinate_index:
        raise ValueError(f"unknown coordinate: {query_coordinate}")
    seed = np.zeros(len(state.coordinates), dtype=float)
    seed[state.coordinate_index[query_coordinate]] = 1.0
    values = seed.copy()
    dangling = state.transition.sum(axis=1) == 0
    for _ in range(iterations):
        propagated = values @ state.transition
        if dangling.any():
            propagated += values[dangling].sum() * seed
        updated = damping * propagated + (1.0 - damping) * seed
        if np.abs(updated - values).sum() <= tolerance:
            values = updated
            break
        values = updated
    return values / values.sum()


def _candidate_scores_from_coordinate_field(
    state: PairwiseCoordinateState,
    field: np.ndarray,
    candidates: Sequence[EntitySignature],
    geometric: bool,
) -> np.ndarray:
    epsilon = 1e-15
    scores = []
    for candidate in candidates:
        values = np.asarray([field[state.coordinate_index[item]] for item in candidate.coordinates])
        score = math.exp(float(np.log(np.maximum(values, epsilon)).mean())) if geometric else float(values.mean())
        scores.append(score)
    return np.asarray(scores)


def flat_keyword_scores(query: Sequence[str], candidates: Sequence[EntitySignature]) -> np.ndarray:
    required = set(query)
    return np.asarray([len(required & set(candidate.coordinates)) for candidate in candidates], dtype=float)


def symbolic_conjunction_scores(query: Sequence[str], candidates: Sequence[EntitySignature]) -> np.ndarray:
    required = set(query)
    return np.asarray([float(required <= set(candidate.coordinates)) for candidate in candidates])


def embedding_centroid_scores(
    state: PairwiseCoordinateState,
    query: Sequence[str],
    candidates: Sequence[EntitySignature],
) -> np.ndarray:
    query_vector = state.embedding[[state.coordinate_index[item] for item in query]].mean(axis=0)
    query_norm = np.linalg.norm(query_vector)
    scores = []
    for candidate in candidates:
        vector = state.embedding[[state.coordinate_index[item] for item in candidate.coordinates]].mean(axis=0)
        denominator = query_norm * np.linalg.norm(vector)
        scores.append(float(query_vector @ vector / denominator) if denominator else 0.0)
    return np.asarray(scores)


def vector_composition_scores(
    state: PairwiseCoordinateState,
    query: Sequence[str],
    candidates: Sequence[EntitySignature],
) -> np.ndarray:
    """Compose explicit one-hot coordinate vectors and compare by cosine."""
    query_vector = np.zeros(len(state.coordinates), dtype=float)
    query_vector[[state.coordinate_index[item] for item in query]] = 1.0
    query_norm = np.linalg.norm(query_vector)
    scores = []
    for candidate in candidates:
        vector = np.zeros(len(state.coordinates), dtype=float)
        vector[[state.coordinate_index[item] for item in candidate.coordinates]] = 1.0
        scores.append(float(query_vector @ vector / (query_norm * np.linalg.norm(vector))))
    return np.asarray(scores)


def kg_traversal_scores(
    state: PairwiseCoordinateState,
    query: Sequence[str],
    candidates: Sequence[EntitySignature],
) -> np.ndarray:
    fields = np.asarray([personalized_field(state, item) for item in query])
    return _candidate_scores_from_coordinate_field(state, fields.mean(axis=0), candidates, geometric=False)


def mml_soft_intersection_scores(
    state: PairwiseCoordinateState,
    query: Sequence[str],
    candidates: Sequence[EntitySignature],
) -> np.ndarray:
    fields = np.asarray([personalized_field(state, item) for item in query])
    composed = np.exp(np.log(np.maximum(fields, 1e-15)).mean(axis=0))
    composed /= composed.sum()
    return _candidate_scores_from_coordinate_field(state, composed, candidates, geometric=True)


SCORERS: Mapping[str, Callable[[PairwiseCoordinateState, Sequence[str], Sequence[EntitySignature]], np.ndarray]] = {
    "embedding_centroid": embedding_centroid_scores,
    "vector_composition": vector_composition_scores,
    "kg_traversal": kg_traversal_scores,
    "mml_soft_intersection": mml_soft_intersection_scores,
}


def rank_target(scores: np.ndarray, candidates: Sequence[EntitySignature], target_id: str) -> RankedTarget:
    if len(scores) != len(candidates) or not np.isfinite(scores).all():
        raise ValueError("scores must be finite and aligned with candidates")
    target_index = next(index for index, item in enumerate(candidates) if item.id == target_id)
    target_score = float(scores[target_index])
    greater = int(np.sum(scores > target_score + 1e-12))
    tied = np.isclose(scores, target_score, rtol=0, atol=1e-12)
    tie_count = int(tied.sum())
    order = sorted(range(len(candidates)), key=lambda index: (-float(scores[index]), candidates[index].id))
    top_index = order[0]
    rival_scores = np.delete(scores, target_index)
    margin = target_score - float(rival_scores.max()) if len(rival_scores) else target_score
    return RankedTarget(
        candidates[top_index].id,
        greater + 1,
        tie_count,
        margin,
        1.0 / (greater + 1),
        1.0 / tie_count if greater == 0 else 0.0,
    )
