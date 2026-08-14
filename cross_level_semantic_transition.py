"""Governed stage-local composition for cross-level semantic transitions.

The direct composition flow treats every constraint as a required property of
one final target.  This module adds a distinct operation: each stage resolves
its own semantic region, while the trace retains the preceding region as
provenance.  Constraint release is explicit and inspectable; it is never
inferred from an expected answer.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from combinatorial_uniqueness_flow import (
    RESOLVED,
    UNRESOLVED,
    CompositionExecution,
    CombinatorialUniquenessFlow,
    CompiledSemanticState,
    ValidityPolicy,
)


@dataclass(frozen=True)
class TransitionStage:
    stage_id: str
    constraints: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.stage_id:
            raise ValueError("transition stage requires a non-empty stage_id")
        if not self.constraints or len(self.constraints) != len(set(self.constraints)):
            raise ValueError("transition stage constraints must be non-empty and unique")


@dataclass(frozen=True)
class StageTransition:
    stage_id: str
    execution: CompositionExecution
    antecedent_region: str | None
    retained_constraints: tuple[str, ...]
    introduced_constraints: tuple[str, ...]
    released_constraints: tuple[str, ...]


@dataclass(frozen=True)
class CrossLevelExecution:
    operation: str
    status: str
    reason_code: str
    stages: tuple[StageTransition, ...]
    final_region: str | None
    flat_control: CompositionExecution
    snapshot_id: str


def _ordered_union(stages: Sequence[TransitionStage]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(constraint for stage in stages for constraint in stage.constraints))


def execute_stage_transition(
    flow: CombinatorialUniquenessFlow,
    state: CompiledSemanticState,
    stages: Sequence[TransitionStage],
    policy: ValidityPolicy,
) -> CrossLevelExecution:
    """Execute explicitly scoped stages and a cumulative-intersection control."""
    ordered_stages = tuple(stages)
    if len(ordered_stages) < 2:
        raise ValueError("cross-level transition requires at least two stages")
    stage_ids = tuple(stage.stage_id for stage in ordered_stages)
    if len(stage_ids) != len(set(stage_ids)):
        raise ValueError("transition stage IDs must be unique")

    records = []
    previous_constraints: tuple[str, ...] = ()
    antecedent = None
    for index, stage in enumerate(ordered_stages):
        execution = flow.execute(state, stage.constraints, policy)
        retained = tuple(item for item in stage.constraints if item in previous_constraints)
        introduced = tuple(item for item in stage.constraints if item not in previous_constraints)
        released = tuple(item for item in previous_constraints if item not in stage.constraints)
        if index and not retained:
            raise ValueError("adjacent transition stages must retain at least one governed constraint")
        records.append(StageTransition(
            stage.stage_id,
            execution,
            antecedent,
            retained,
            introduced,
            released,
        ))
        antecedent = execution.top_candidate
        previous_constraints = stage.constraints

    all_resolved = all(record.execution.status == RESOLVED for record in records)
    status = RESOLVED if all_resolved else UNRESOLVED
    reason = "GOVERNED_STAGE_TRANSITION_RESOLVED" if all_resolved else "STAGE_DID_NOT_RESOLVE"
    flat_control = flow.execute(state, _ordered_union(ordered_stages), policy)
    return CrossLevelExecution(
        "STAGE_RESET_TRANSITION",
        status,
        reason,
        tuple(records),
        records[-1].execution.top_candidate if all_resolved else None,
        flat_control,
        state.snapshot_id,
    )
