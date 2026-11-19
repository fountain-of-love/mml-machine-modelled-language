"""Encode one governed relation as a matrix, and project it into simpler forms.

The canonical form is a signed matrix ``S`` with values in [-1, 1]:

    -1  opposite      0  neutral (no relation)      +1  alike

Two simpler forms are projections of ``S``, so their information loss is
explicit rather than accidental:

- **binary**  ``B = [S <= threshold]``: opposite or not. Alike and neutral
  both become 0.
- **degree**  ``D = (1 - S) / 2`` in [0, 1]: how opposite. Neutral sits at 0.5.

The signed form lets one matrix answer both questions with opposite functions:
alike is the positive part of ``S``; opposite is the positive part of ``-S``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

import numpy as np


OPPOSITE, NEUTRAL, ALIKE = -1, 0, 1


def _readonly(values: np.ndarray) -> np.ndarray:
    values = np.array(values, dtype=float)
    values.setflags(write=False)
    return values


@dataclass(frozen=True)
class SignedRelationMatrix:
    """Immutable, symmetric relation over named items; diagonal is +1 (alike).

    ``asserted`` marks cells that carry a governed statement. A value of 0 is
    ambiguous on its own: it can mean "explicitly neutral" or "never stated".
    ``None`` means every cell is asserted, as for a dense learned matrix.
    """

    labels: tuple[str, ...]
    values: np.ndarray
    asserted: np.ndarray | None = None

    def is_asserted(self) -> np.ndarray:
        if self.asserted is None:
            return np.ones(self.values.shape, dtype=bool)
        return self.asserted

    def index(self, label: str) -> int:
        try:
            return self.labels.index(label)
        except ValueError:
            raise KeyError(f"unknown item: {label}") from None

    def off_diagonal(self) -> np.ndarray:
        """Boolean mask of the cells that carry relations between distinct items."""
        return ~np.eye(len(self.labels), dtype=bool)


def build_signed_matrix(
    labels: Iterable[str],
    relations: Iterable[Mapping[str, object]],
    *,
    default: float = 0.0,
) -> SignedRelationMatrix:
    """Build a symmetric signed matrix from governed ``{a, b, value}`` records."""
    labels = tuple(labels)
    if len(set(labels)) != len(labels) or not labels:
        raise ValueError("labels must be unique and non-empty")
    position = {label: i for i, label in enumerate(labels)}
    values = np.full((len(labels), len(labels)), float(default))
    np.fill_diagonal(values, 1.0)
    asserted = np.eye(len(labels), dtype=bool)
    seen: set[frozenset[str]] = set()
    for record in relations:
        a, b, value = str(record["a"]), str(record["b"]), float(record["value"])
        if a not in position or b not in position:
            raise ValueError(f"relation uses an undeclared item: {a}, {b}")
        if a == b:
            raise ValueError("an item's relation to itself is fixed at +1")
        if not -1.0 <= value <= 1.0:
            raise ValueError(f"relation value out of [-1, 1]: {a}-{b} = {value}")
        pair = frozenset((a, b))
        if pair in seen:
            raise ValueError(f"relation declared twice: {a}-{b}")
        seen.add(pair)
        values[position[a], position[b]] = values[position[b], position[a]] = value
        asserted[position[a], position[b]] = asserted[position[b], position[a]] = True
    asserted.setflags(write=False)
    return SignedRelationMatrix(labels, _readonly(values), asserted)


def to_binary(matrix: SignedRelationMatrix, threshold: float = -0.5) -> np.ndarray:
    """1 where the pair is opposite (``S <= threshold``), else 0; diagonal 0."""
    binary = (matrix.values <= threshold).astype(np.int8)
    np.fill_diagonal(binary, 0)
    return binary


def to_degree(matrix: SignedRelationMatrix) -> np.ndarray:
    """Degree of opposition in [0, 1]: 1 opposite, 0.5 neutral, 0 alike."""
    return (1.0 - matrix.values) / 2.0


def to_three_states(values: np.ndarray, band: float = 0.5) -> np.ndarray:
    """Map signed values to -1 / 0 / +1 using a symmetric neutral band."""
    states = np.zeros(values.shape, dtype=np.int8)
    states[values <= -band] = OPPOSITE
    states[values >= band] = ALIKE
    return states


def related(matrix: SignedRelationMatrix, label: str, polarity: int) -> tuple[tuple[str, float], ...]:
    """Items related to ``label`` with the given polarity, strongest first.

    The same matrix serves both directions: ``polarity=+1`` reads the positive
    part of the row (alike), ``polarity=-1`` reads the positive part of the
    negated row (opposite).
    """
    if polarity not in (ALIKE, OPPOSITE):
        raise ValueError("polarity must be +1 (alike) or -1 (opposite)")
    row = polarity * matrix.values[matrix.index(label)]
    hits = [
        (other, float(strength))
        for other, strength in zip(matrix.labels, row)
        if other != label and strength > 0
    ]
    return tuple(sorted(hits, key=lambda item: (-item[1], item[0])))


def two_hop(matrix: SignedRelationMatrix) -> np.ndarray:
    """Signed two-step composition over distinct items: ``S' @ S'``, diagonal 0.

    Signs multiply, so opposite-of-opposite becomes alike. The result is an
    inferred candidate, never governed knowledge until explicitly accepted.
    """
    off = matrix.values * matrix.off_diagonal()
    composed = off @ off
    np.fill_diagonal(composed, 0.0)
    return composed
