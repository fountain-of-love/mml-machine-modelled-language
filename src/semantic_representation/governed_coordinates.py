"""Represent governed entities as reusable dimension-qualified semantic coordinates."""

from __future__ import annotations

import re
from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping, Sequence

from src.helpers.hashing import sha256_bytes
from src.helpers.json_io import canonical_json_bytes


IDENTITY = re.compile(r"^[a-z][a-z0-9_-]*$")
ALGORITHM_VERSION = "governed-coordinate-basis-v1"


@dataclass(frozen=True)
class SemanticEntity:
    """One governed entity and its values in a declared semantic basis."""

    id: str
    label: str
    attributes: Mapping[str, str | None]

    def __post_init__(self) -> None:
        if not IDENTITY.fullmatch(self.id):
            raise ValueError("entity IDs must be normalized governed identities")
        if not self.label:
            raise ValueError("entity labels must be non-empty")
        object.__setattr__(self, "attributes", MappingProxyType(dict(self.attributes)))


@dataclass(frozen=True)
class RepresentationMetrics:
    source_field_reads: int
    coordinate_assignments: int
    logical_bytes: int

    @property
    def total_operations(self) -> int:
        return self.source_field_reads + self.coordinate_assignments


@dataclass(frozen=True)
class GovernedCoordinateBasis:
    """Validated semantic dimensions, values, and reversible compact codes."""

    basis_id: str
    dimensions: tuple[str, ...]
    entities: tuple[SemanticEntity, ...]
    coordinates: tuple[str, ...]
    coordinate_codes: Mapping[str, int]
    incomplete_entities: Mapping[str, tuple[str, ...]]
    representation: RepresentationMetrics
    snapshot_id: str


@dataclass(frozen=True)
class CodedSemanticQuery:
    """Compact coordinates retaining the dimensions that give them meaning."""

    dimensions: tuple[str, ...]
    coordinate_codes: tuple[int, ...]

    def __post_init__(self) -> None:
        if not self.dimensions:
            raise ValueError("a coded semantic query requires at least one dimension")
        if len(self.dimensions) != len(self.coordinate_codes):
            raise ValueError("coded query dimensions and coordinates must be aligned")
        if len(set(self.dimensions)) != len(self.dimensions):
            raise ValueError("coded query dimensions must be unique")
        if any(
            not isinstance(code, int) or isinstance(code, bool)
            for code in self.coordinate_codes
        ):
            raise TypeError("coded query coordinates must be integers")
        if any(code < -1 for code in self.coordinate_codes):
            raise ValueError("unsupported coded coordinates must use the -1 sentinel")


def coordinate_identity(dimension: str, value: str) -> str:
    return f"{dimension}:{value}"


def _validate_dimensions(dimensions: Sequence[str]) -> tuple[str, ...]:
    declared = tuple(dimensions)
    if not declared or len(set(declared)) != len(declared):
        raise ValueError("semantic dimensions must be non-empty and unique")
    if any(not IDENTITY.fullmatch(dimension) for dimension in declared):
        raise ValueError("semantic dimensions must be normalized governed identities")
    return declared


def represent_coordinate_basis(
    basis_id: str,
    dimensions: Sequence[str],
    entities: Sequence[SemanticEntity],
) -> GovernedCoordinateBasis:
    """Validate governed meaning and assign a stable reversible code projection."""
    declared = _validate_dimensions(dimensions)
    records = tuple(entities)
    if not records:
        raise ValueError("at least one governed semantic entity is required")
    if len({entity.id for entity in records}) != len(records):
        raise ValueError("semantic entity IDs must be unique")

    declared_set = set(declared)
    incomplete = {}
    coordinate_set = set()
    coordinate_assignments = 0
    for entity in records:
        unknown = sorted(set(entity.attributes) - declared_set)
        if unknown:
            raise ValueError(f"entity '{entity.id}' uses undeclared dimensions: {', '.join(unknown)}")
        missing = []
        for dimension in declared:
            value = entity.attributes.get(dimension)
            if value is None:
                missing.append(dimension)
                continue
            if not isinstance(value, str) or not IDENTITY.fullmatch(value):
                raise ValueError("semantic values must be normalized governed identities")
            coordinate_set.add(coordinate_identity(dimension, value))
            coordinate_assignments += 1
        if missing:
            incomplete[entity.id] = tuple(missing)

    coordinates = tuple(sorted(coordinate_set))
    codes = {item: position for position, item in enumerate(coordinates)}
    payload = {
        "algorithm": ALGORITHM_VERSION,
        "basis_id": basis_id,
        "dimensions": declared,
        "entities": [
            {
                "id": entity.id,
                "label": entity.label,
                "attributes": dict(entity.attributes),
            }
            for entity in records
        ],
        "coordinates": coordinates,
    }
    encoded = canonical_json_bytes(payload)
    representation = RepresentationMetrics(
        source_field_reads=len(records) * len(declared),
        coordinate_assignments=coordinate_assignments,
        logical_bytes=len(encoded),
    )
    return GovernedCoordinateBasis(
        basis_id=basis_id,
        dimensions=declared,
        entities=records,
        coordinates=coordinates,
        coordinate_codes=MappingProxyType(codes),
        incomplete_entities=MappingProxyType(incomplete),
        representation=representation,
        snapshot_id=sha256_bytes(encoded),
    )


def validate_query(
    basis: GovernedCoordinateBasis,
    observed: Mapping[str, str],
) -> None:
    if not observed:
        raise ValueError("a semantic query requires at least one observed dimension")
    unknown = sorted(set(observed) - set(basis.dimensions))
    if unknown:
        raise ValueError(f"unknown dimensions: {', '.join(unknown)}")
    if any(
        not isinstance(value, str) or not IDENTITY.fullmatch(value)
        for value in observed.values()
    ):
        raise ValueError("query values must be normalized governed identities")


def encode_query(
    basis: GovernedCoordinateBasis,
    observed: Mapping[str, str],
) -> CodedSemanticQuery:
    """Project governed labels into stable codes; ``-1`` denotes an unsupported value."""
    validate_query(basis, observed)
    dimensions = tuple(
        dimension for dimension in basis.dimensions if dimension in observed
    )
    return CodedSemanticQuery(
        dimensions=dimensions,
        coordinate_codes=tuple(
            basis.coordinate_codes.get(
                coordinate_identity(dimension, observed[dimension]), -1
            )
            for dimension in dimensions
        ),
    )


def decode_query(
    basis: GovernedCoordinateBasis,
    query: CodedSemanticQuery,
) -> Mapping[str, str]:
    """Reverse a compact query while enforcing its dimension-qualified meaning."""
    validate_query(basis, {dimension: "coded" for dimension in query.dimensions})
    decoded = {}
    for dimension, code in zip(query.dimensions, query.coordinate_codes):
        if code < 0 or code >= len(basis.coordinates):
            decoded[dimension] = "UNKNOWN"
        else:
            coordinate = basis.coordinates[code]
            coordinate_dimension, value = coordinate.split(":", 1)
            if coordinate_dimension != dimension:
                raise ValueError(
                    f"coordinate code {code} belongs to '{coordinate_dimension}', not '{dimension}'"
                )
            decoded[dimension] = value
    return MappingProxyType(decoded)
