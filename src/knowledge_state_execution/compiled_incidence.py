"""Compile governed coordinate membership once into immutable executable state."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from src.helpers.hashing import sha256_bytes
from src.helpers.json_io import canonical_json_bytes
from src.semantic_representation.governed_coordinates import (
    GovernedCoordinateBasis,
    coordinate_identity,
)


ALGORITHM_VERSION = "compiled-incidence-state-v1"


@dataclass(frozen=True)
class IncidenceCompilationMetrics:
    source_field_reads: int
    posting_entries: int
    signature_writes: int
    entity_index_entries: int
    logical_bytes: int

    @property
    def total_operations(self) -> int:
        return (
            self.source_field_reads
            + self.posting_entries
            + self.signature_writes
            + self.entity_index_entries
        )


@dataclass(frozen=True)
class CompiledIncidenceState:
    """Persistent postings and equivalence classes over one semantic basis."""

    basis: GovernedCoordinateBasis
    postings: Mapping[int, tuple[int, ...]]
    signature_classes: Mapping[tuple[int | None, ...], tuple[str, ...]]
    entity_positions: Mapping[str, int]
    compilation: IncidenceCompilationMetrics
    snapshot_id: str


def compile_incidence_state(basis: GovernedCoordinateBasis) -> CompiledIncidenceState:
    """Compile a many-to-many semantic basis into reusable coordinate postings."""
    mutable_postings = {code: [] for code in basis.coordinate_codes.values()}
    signatures: dict[tuple[int | None, ...], list[str]] = {}

    for position, entity in enumerate(basis.entities):
        signature = []
        for dimension in basis.dimensions:
            value = entity.attributes.get(dimension)
            code = (
                basis.coordinate_codes[coordinate_identity(dimension, value)]
                if value is not None else None
            )
            signature.append(code)
            if code is not None:
                mutable_postings[code].append(position)
        signatures.setdefault(tuple(signature), []).append(entity.id)

    postings = {code: tuple(positions) for code, positions in mutable_postings.items()}
    signature_classes = {signature: tuple(ids) for signature, ids in signatures.items()}
    entity_positions = {entity.id: position for position, entity in enumerate(basis.entities)}
    payload = {
        "algorithm": ALGORITHM_VERSION,
        "basis_snapshot_id": basis.snapshot_id,
        "postings": {str(code): positions for code, positions in postings.items()},
        "signature_classes": [
            {"coordinate_codes": signature, "entity_ids": ids}
            for signature, ids in signature_classes.items()
        ],
        "entity_positions": entity_positions,
    }
    encoded = canonical_json_bytes(payload)
    metrics = IncidenceCompilationMetrics(
        source_field_reads=len(basis.entities) * len(basis.dimensions),
        posting_entries=sum(len(positions) for positions in postings.values()),
        signature_writes=len(basis.entities),
        entity_index_entries=len(entity_positions),
        logical_bytes=len(encoded),
    )
    return CompiledIncidenceState(
        basis=basis,
        postings=MappingProxyType(postings),
        signature_classes=MappingProxyType(signature_classes),
        entity_positions=MappingProxyType(entity_positions),
        compilation=metrics,
        snapshot_id=sha256_bytes(encoded),
    )
