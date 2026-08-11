"""Numerical primitives for composing independently activated semantic fields.

This module deliberately knows nothing about graphs, fixtures, targets, or
experiment verdicts.  Callers provide aligned fields and, when appropriate,
the background distribution used by the existing graph operator.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np


_EPSILON = np.finfo(float).tiny


@dataclass(frozen=True)
class ActivatedField:
    """One constraint's independently calculated activation field."""

    constraint: str
    values: tuple[float, ...]

    def __post_init__(self) -> None:
        if not self.constraint:
            raise ValueError("constraint must be non-empty")
        values = _validated_values(self.values, name=f"field {self.constraint!r}")
        object.__setattr__(self, "values", tuple(float(value) for value in values))


@dataclass(frozen=True)
class ComposedField:
    """A normalized composition and the immutable fields that produced it."""

    constraints: tuple[str, ...]
    values: tuple[float, ...]
    per_constraint_support: tuple[ActivatedField, ...]


@dataclass(frozen=True)
class DistributionMetrics:
    """Candidate-only measurements over a normalized activation field."""

    entropy: float
    normalized_entropy: float
    effective_candidate_count: float
    concentration: float
    top_k_mass: float


def _validated_values(values: Sequence[float], *, name: str) -> np.ndarray:
    array = np.asarray(values, dtype=float)
    if array.ndim != 1 or not len(array):
        raise ValueError(f"{name} must be a non-empty one-dimensional field")
    if not np.all(np.isfinite(array)):
        raise ValueError(f"{name} must contain only finite values")
    if np.any(array < 0):
        raise ValueError(f"{name} must not contain negative values")
    return array


def normalize(values: Sequence[float]) -> tuple[float, ...]:
    """Return a finite probability distribution without mutating ``values``."""
    array = _validated_values(values, name="values")
    total = float(array.sum())
    if total <= 0:
        raise ValueError("values must contain positive support")
    return tuple(float(value) for value in array / total)


def soft_intersection(
    fields: Sequence[ActivatedField],
    *,
    background: Sequence[float] | None = None,
) -> ComposedField:
    """Compose aligned fields using the graph operator's normalized geometric mean.

    Background correction is optional so the primitive can also be used for
    already-corrected fields.  When supplied, its placement exactly matches
    :meth:`GraphModel.activation`: geometric mean, correction, normalization.
    """
    supports = tuple(fields)
    if not supports:
        raise ValueError("at least one activated field is required")
    arrays = tuple(
        _validated_values(field.values, name=f"field {field.constraint!r}")
        for field in supports
    )
    width = len(arrays[0])
    if any(len(array) != width for array in arrays[1:]):
        raise ValueError("activated fields must have the same length")

    if len(arrays) == 1:
        combined = arrays[0].copy()
    else:
        combined = np.exp(np.mean(np.log(np.maximum(arrays, _EPSILON)), axis=0))

    if background is not None:
        background_array = _validated_values(background, name="background")
        if len(background_array) != width:
            raise ValueError("background and activated fields must have the same length")
        combined = combined / np.sqrt(np.maximum(background_array, _EPSILON))

    values = normalize(combined)
    return ComposedField(
        constraints=tuple(field.constraint for field in supports),
        values=values,
        per_constraint_support=supports,
    )


def distribution_metrics(values: Sequence[float], *, top_k: int = 1) -> DistributionMetrics:
    """Measure a candidate-only field; oversized ``top_k`` includes all candidates."""
    if top_k < 1:
        raise ValueError("top_k must be at least one")
    probabilities = np.asarray(normalize(values))
    positive = probabilities[probabilities > 0]
    entropy = float(-np.sum(positive * np.log(positive)))
    normalized_entropy = entropy / math.log(len(probabilities)) if len(probabilities) > 1 else 0.0
    return DistributionMetrics(
        entropy=entropy,
        normalized_entropy=normalized_entropy,
        effective_candidate_count=math.exp(entropy),
        concentration=float(probabilities.max()),
        top_k_mass=float(np.sort(probabilities)[-top_k:].sum()),
    )


def target_rank(values: Sequence[float], target_index: int) -> int:
    """Return a one-based competition rank for a target candidate."""
    probabilities = np.asarray(normalize(values))
    if not 0 <= target_index < len(probabilities):
        raise IndexError("target_index is outside the candidate field")
    return int(np.count_nonzero(probabilities > probabilities[target_index]) + 1)


def target_margin(values: Sequence[float], target_index: int) -> float:
    """Return target activation minus the strongest alternative activation."""
    probabilities = np.asarray(normalize(values))
    if not 0 <= target_index < len(probabilities):
        raise IndexError("target_index is outside the candidate field")
    if len(probabilities) == 1:
        return float(probabilities[target_index])
    alternatives = np.delete(probabilities, target_index)
    return float(probabilities[target_index] - alternatives.max())
