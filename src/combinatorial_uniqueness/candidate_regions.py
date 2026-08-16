"""Compose explicit semantic coordinates into exact candidate regions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from src.knowledge_state_execution.compiled_incidence import CompiledIncidenceState


@dataclass(frozen=True)
class RegionExecutionCost:
    coordinate_lookups: int = 0
    posting_entries_inspected: int = 0
    set_intersections: int = 0
    result_materializations: int = 0

    @property
    def total_operations(self) -> int:
        return (
            self.coordinate_lookups
            + self.posting_entries_inspected
            + self.set_intersections
            + self.result_materializations
        )


@dataclass(frozen=True)
class CandidateRegion:
    coordinate_codes: tuple[int, ...]
    entity_positions: tuple[int, ...]
    entity_ids: tuple[str, ...]
    cost: RegionExecutionCost


def compose_candidate_region(
    state: CompiledIncidenceState,
    coordinate_codes: Sequence[int],
) -> CandidateRegion:
    """Intersect independently broad coordinates without forcing a unique identity."""
    codes = tuple(coordinate_codes)
    if not codes:
        raise ValueError("candidate-region composition requires at least one coordinate")

    postings = tuple(state.postings.get(code, ()) for code in codes)
    ordered = sorted(postings, key=len)
    candidates = set(ordered[0])
    inspected = len(ordered[0])
    intersections = 0
    for posting in ordered[1:]:
        inspected += min(len(candidates), len(posting))
        intersections += 1
        candidates.intersection_update(posting)
        if not candidates:
            break

    positions = tuple(sorted(candidates))
    ids = tuple(state.basis.entities[position].id for position in positions)
    return CandidateRegion(
        coordinate_codes=codes,
        entity_positions=positions,
        entity_ids=ids,
        cost=RegionExecutionCost(
            coordinate_lookups=len(codes),
            posting_entries_inspected=inspected,
            set_intersections=intersections,
            result_materializations=len(positions),
        ),
    )
