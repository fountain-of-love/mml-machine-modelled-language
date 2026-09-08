"""Interchangeable next-question strategies for semantic navigation."""

from __future__ import annotations

import hashlib
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ClassVar, Mapping, Protocol, Sequence


INFORMATION_GAIN = "information_gain"
FIXED_DIMENSION_ORDER = "fixed_dimension_order"
RANDOM_ELIGIBLE = "random_eligible_dimension"
HIGHEST_CARDINALITY = "highest_cardinality_dimension"
HIGHEST_COVERAGE = "highest_coverage_dimension"


class DimensionInformation(Protocol):
    """Structural view required by navigation strategies."""

    candidate_count: int
    value_count: int
    information_gain_bits: float
    missing_candidate_count: int


class NavigationStrategy(ABC):
    """Select the next informative dimension from a governed candidate state."""

    id: str

    @abstractmethod
    def select(
        self,
        information: Mapping[str, DimensionInformation],
        dimension_order: Sequence[str],
    ) -> str | None:
        """Return one informative dimension, or ``None`` when none remains."""


def _informative_dimensions(
    information: Mapping[str, DimensionInformation],
    dimension_order: Sequence[str],
) -> tuple[str, ...]:
    return tuple(
        dimension
        for dimension in dimension_order
        if dimension in information
        and information[dimension].information_gain_bits > 0.0
    )


@dataclass(frozen=True)
class InformationGainNavigationStrategy(NavigationStrategy):
    """Choose the dimension with maximum uniform-prior information gain."""

    id: ClassVar[str] = INFORMATION_GAIN

    def select(self, information, dimension_order):
        eligible = _informative_dimensions(information, dimension_order)
        order = {dimension: position for position, dimension in enumerate(dimension_order)}
        return max(
            eligible,
            key=lambda dimension: (
                information[dimension].information_gain_bits,
                -order[dimension],
            ),
            default=None,
        )


@dataclass(frozen=True)
class FixedDimensionOrderNavigationStrategy(NavigationStrategy):
    """Choose the first informative dimension in governed basis order."""

    id: ClassVar[str] = FIXED_DIMENSION_ORDER

    def select(self, information, dimension_order):
        eligible = _informative_dimensions(information, dimension_order)
        return eligible[0] if eligible else None


@dataclass(frozen=True)
class HighestCardinalityNavigationStrategy(NavigationStrategy):
    """Choose the informative dimension with most represented answer groups."""

    id: ClassVar[str] = HIGHEST_CARDINALITY

    def select(self, information, dimension_order):
        eligible = _informative_dimensions(information, dimension_order)
        order = {dimension: position for position, dimension in enumerate(dimension_order)}
        return max(
            eligible,
            key=lambda dimension: (
                information[dimension].value_count,
                -order[dimension],
            ),
            default=None,
        )


@dataclass(frozen=True)
class HighestCoverageNavigationStrategy(NavigationStrategy):
    """Choose the informative dimension with most governed candidate values."""

    id: ClassVar[str] = HIGHEST_COVERAGE

    def select(self, information, dimension_order):
        eligible = _informative_dimensions(information, dimension_order)
        order = {dimension: position for position, dimension in enumerate(dimension_order)}
        return max(
            eligible,
            key=lambda dimension: (
                information[dimension].candidate_count
                - information[dimension].missing_candidate_count,
                -order[dimension],
            ),
            default=None,
        )


@dataclass(frozen=True)
class RandomEligibleNavigationStrategy(NavigationStrategy):
    """Choose reproducibly from informative dimensions using visible state only."""

    seed: int
    id: ClassVar[str] = RANDOM_ELIGIBLE

    def __post_init__(self) -> None:
        if not isinstance(self.seed, int) or isinstance(self.seed, bool):
            raise ValueError("random navigation strategy seed must be an integer")

    def select(self, information, dimension_order):
        eligible = _informative_dimensions(information, dimension_order)
        if not eligible:
            return None
        state = tuple(
            (
                dimension,
                item.candidate_count,
                item.value_count,
                item.information_gain_bits,
                item.missing_candidate_count,
            )
            for dimension in dimension_order
            if (item := information.get(dimension)) is not None
        )
        return min(
            eligible,
            key=lambda dimension: hashlib.sha256(
                repr((self.seed, state, dimension)).encode("utf-8")
            ).digest(),
        )


DEFAULT_NAVIGATION_STRATEGY = InformationGainNavigationStrategy()
