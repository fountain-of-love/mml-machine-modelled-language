"""Navigate candidate regions produced by represented, compiled, composed knowledge."""

from __future__ import annotations

import itertools
import math
from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping, Sequence

from src.combinatorial_uniqueness.candidate_regions import (
    CandidateRegion,
    compose_candidate_region,
)
from src.knowledge_state_execution.compiled_incidence import (
    CompiledIncidenceState,
    compile_incidence_state,
)
from src.semantic_representation.governed_coordinates import (
    CodedSemanticQuery,
    GovernedCoordinateBasis,
    SemanticEntity,
    decode_query,
    encode_query,
    represent_coordinate_basis,
)


IDENTIFIABLE = "IDENTIFIABLE"
AMBIGUOUS = "AMBIGUOUS"
UNSUPPORTED = "UNSUPPORTED"
UNKNOWN_VALUE = "UNKNOWN"
ALL_DIMENSIONS_LENS = "all_dimensions"


@dataclass(frozen=True)
class NavigationLens:
    """A governed subset of dimensions eligible for navigation questions."""

    id: str
    dimensions: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("a navigation lens requires a non-empty ID")
        if not self.dimensions or len(self.dimensions) != len(set(self.dimensions)):
            raise ValueError("navigation lens dimensions must be non-empty and unique")


@dataclass(frozen=True)
class PartitionInformation:
    """Information contributed by one dimension over the current candidate region."""

    dimension: str
    candidate_count: int
    value_count: int
    prior_entropy_bits: float
    expected_posterior_entropy_bits: float
    information_gain_bits: float
    normalized_information_gain: float
    missing_candidate_count: int


@dataclass(frozen=True)
class SemanticNavigationState:
    knowledge_state: CompiledIncidenceState

    @property
    def basis(self) -> GovernedCoordinateBasis:
        """Expose the basis owned by the compiled knowledge state."""
        return self.knowledge_state.basis


@dataclass(frozen=True)
class NavigationResult:
    candidate_ids: tuple[str, ...]
    status: str
    commonality: Mapping[str, str]
    deterministic_imputations: Mapping[str, str]
    distinctions: Mapping[str, Mapping[str, tuple[str, ...]]]
    partition_information: Mapping[str, PartitionInformation]
    lens_id: str
    next_dimension: str | None
    next_dimension_information_gain: float
    region: CandidateRegion


@dataclass(frozen=True)
class IdentificationProfile:
    candidate_ids: tuple[str, ...]
    complete_signature: Mapping[str, str | None]
    minimum_dimension_count: int | None
    minimum_dimension_sets: tuple[tuple[str, ...], ...]
    uniquely_identifiable: bool


def _freeze(values: Mapping) -> Mapping:
    return MappingProxyType(dict(values))


def _freeze_nested(values: Mapping[str, Mapping[str, tuple[str, ...]]]) -> Mapping:
    return MappingProxyType({
        key: MappingProxyType(dict(value))
        for key, value in values.items()
    })


def _status(candidate_count: int) -> str:
    if candidate_count == 0:
        return UNSUPPORTED
    if candidate_count == 1:
        return IDENTIFIABLE
    return AMBIGUOUS


def _partition_information(
    dimension: str,
    partition: Mapping[str, Sequence[str]],
) -> PartitionInformation:
    total = sum(len(ids) for ids in partition.values())
    prior_entropy = math.log2(total) if total > 1 else 0.0
    expected_posterior = sum(
        (len(ids) / total) * math.log2(len(ids))
        for ids in partition.values()
        if total and ids
    )
    information_gain = max(0.0, prior_entropy - expected_posterior)
    return PartitionInformation(
        dimension=dimension,
        candidate_count=total,
        value_count=sum(bool(ids) for ids in partition.values()),
        prior_entropy_bits=prior_entropy,
        expected_posterior_entropy_bits=expected_posterior,
        information_gain_bits=information_gain,
        normalized_information_gain=(
            information_gain / prior_entropy if prior_entropy else 0.0
        ),
        missing_candidate_count=len(partition.get(UNKNOWN_VALUE, ())),
    )


class SemanticNavigationFlow:
    """Facade accumulating representation, compilation, composition, and navigation."""

    def govern_and_compile(
        self,
        state_id: str,
        dimensions: Sequence[str],
        entities: Sequence[SemanticEntity],
    ) -> SemanticNavigationState:
        basis = represent_coordinate_basis(state_id, dimensions, entities)
        return SemanticNavigationState(compile_incidence_state(basis))

    def execute(
        self,
        state: SemanticNavigationState,
        observed: Mapping[str, str],
        lens: NavigationLens | None = None,
    ) -> NavigationResult:
        return self.execute_codes(
            state,
            encode_query(state.basis, observed),
            lens=lens,
        )

    def execute_codes(
        self,
        state: SemanticNavigationState,
        query: CodedSemanticQuery,
        lens: NavigationLens | None = None,
    ) -> NavigationResult:
        decoded = decode_query(state.basis, query)
        eligible_dimensions = self._eligible_dimensions(state, lens)
        region = compose_candidate_region(
            state.knowledge_state, query.coordinate_codes
        )
        return self._navigate(
            state,
            region,
            tuple(decoded),
            eligible_dimensions,
            ALL_DIMENSIONS_LENS if lens is None else lens.id,
        )

    def common_dimensions(
        self,
        state: SemanticNavigationState,
        candidate_ids: Sequence[str],
    ) -> Mapping[str, str]:
        positions = state.knowledge_state.entity_positions
        unknown = sorted(set(candidate_ids) - set(positions))
        if unknown:
            raise ValueError(f"unknown candidate IDs: {', '.join(unknown)}")
        candidate_positions = tuple(positions[item] for item in candidate_ids)
        return _freeze(self._commonality(state, candidate_positions))

    def identification_profiles(
        self,
        state: SemanticNavigationState,
    ) -> tuple[IdentificationProfile, ...]:
        profiles = []
        for candidate_ids in sorted(state.knowledge_state.signature_classes.values()):
            exemplar = state.basis.entities[
                state.knowledge_state.entity_positions[candidate_ids[0]]
            ]
            complete = dict(exemplar.attributes)
            available = tuple(
                dimension
                for dimension in state.basis.dimensions
                if complete.get(dimension) is not None
            )
            minimum_sets = []
            for width in range(1, len(available) + 1):
                for dimensions in itertools.combinations(available, width):
                    observed = {
                        dimension: value
                        for dimension in dimensions
                        if (value := complete[dimension]) is not None
                    }
                    result = self.execute(state, observed)
                    if set(result.candidate_ids) == set(candidate_ids):
                        minimum_sets.append(dimensions)
                if minimum_sets:
                    break
            profiles.append(IdentificationProfile(
                candidate_ids=candidate_ids,
                complete_signature=_freeze(complete),
                minimum_dimension_count=len(minimum_sets[0]) if minimum_sets else None,
                minimum_dimension_sets=tuple(minimum_sets),
                uniquely_identifiable=len(candidate_ids) == 1,
            ))
        return tuple(profiles)

    def _navigate(
        self,
        state: SemanticNavigationState,
        region: CandidateRegion,
        observed_dimensions: Sequence[str],
        eligible_dimensions: Sequence[str],
        lens_id: str,
    ) -> NavigationResult:
        missing = tuple(
            dimension
            for dimension in eligible_dimensions
            if dimension not in observed_dimensions
        )
        distinctions = self._partitions(state, region.entity_positions, missing)
        imputations = {
            dimension: next(iter(partition))
            for dimension, partition in distinctions.items()
            if len(partition) == 1 and UNKNOWN_VALUE not in partition
        }
        partition_information = {
            dimension: _partition_information(dimension, partition)
            for dimension, partition in distinctions.items()
        }
        gains = {
            dimension: information.information_gain_bits
            for dimension, information in partition_information.items()
            if information.information_gain_bits > 0.0
        }
        next_dimension = max(
            gains,
            key=lambda item: (gains[item], -state.basis.dimensions.index(item)),
        ) if gains else None
        return NavigationResult(
            candidate_ids=region.entity_ids,
            status=_status(len(region.entity_ids)),
            commonality=_freeze(self._commonality(state, region.entity_positions)),
            deterministic_imputations=_freeze(imputations),
            distinctions=_freeze_nested(distinctions),
            partition_information=_freeze(partition_information),
            lens_id=lens_id,
            next_dimension=next_dimension,
            next_dimension_information_gain=(
                0.0 if next_dimension is None else gains[next_dimension]
            ),
            region=region,
        )

    def _eligible_dimensions(
        self,
        state: SemanticNavigationState,
        lens: NavigationLens | None,
    ) -> tuple[str, ...]:
        if lens is None:
            return state.basis.dimensions
        unknown = sorted(set(lens.dimensions) - set(state.basis.dimensions))
        if unknown:
            raise ValueError(f"lens uses unknown dimensions: {', '.join(unknown)}")
        return lens.dimensions

    def _commonality(
        self,
        state: SemanticNavigationState,
        positions: Sequence[int],
    ) -> dict[str, str]:
        if not positions:
            return {}
        common = {}
        for dimension in state.basis.dimensions:
            values = {
                state.basis.entities[position].attributes.get(dimension)
                for position in positions
            }
            if len(values) == 1 and None not in values:
                value = next(iter(values))
                if value is not None:
                    common[dimension] = value
        return common

    def _partitions(
        self,
        state: SemanticNavigationState,
        positions: Sequence[int],
        dimensions: Sequence[str],
    ) -> dict[str, dict[str, tuple[str, ...]]]:
        partitions = {}
        for dimension in dimensions:
            groups: dict[str, list[str]] = {}
            for position in positions:
                entity = state.basis.entities[position]
                value = entity.attributes.get(dimension) or UNKNOWN_VALUE
                groups.setdefault(value, []).append(entity.id)
            partitions[dimension] = {
                value: tuple(ids)
                for value, ids in sorted(groups.items())
            }
        return partitions
