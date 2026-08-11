"""Validated, immutable loaders for Combinatorial Uniqueness fixtures."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping


ROOT = Path(__file__).parent
DEVELOPMENT_LIFECYCLE = "AUTHORED_DEVELOPMENT"


@dataclass(frozen=True)
class Dimension:
    id: str
    family: str


@dataclass(frozen=True)
class Concept:
    id: str
    traits: frozenset[str]


@dataclass(frozen=True)
class CompositionExclusion:
    left: str
    right: str
    scope: str
    kind: str


@dataclass(frozen=True)
class SemanticStateFixture:
    schema_version: str
    state_id: str
    title: str
    source_path: Path
    source_sha256: str
    lifecycle: str
    evidence_boundary: str
    dimensions: tuple[Dimension, ...]
    concepts: tuple[Concept, ...]
    exclusions: tuple[CompositionExclusion, ...]
    epistemic_classification: str | None
    epistemic_positions: tuple[str, ...]
    epistemic_rule: str | None


@dataclass(frozen=True)
class ProbeSuiteFixture:
    schema_version: str
    probe_suite_id: str
    state_id: str
    source_path: Path
    source_sha256: str
    holdout_status: str
    probes: Mapping[str, tuple[Mapping[str, Any], ...]]


@dataclass(frozen=True)
class ExperimentFixture:
    experiment_id: str
    manifest_path: Path
    manifest_sha256: str
    lifecycle: str
    state: SemanticStateFixture
    probes: ProbeSuiteFixture


def _read(path: Path) -> tuple[dict[str, Any], str]:
    raw = path.read_bytes()
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as error:
        raise ValueError(f"invalid fixture JSON: {path}") from error
    return value, f"sha256:{hashlib.sha256(raw).hexdigest()}"


def _unique(records: list[dict[str, Any]], label: str) -> None:
    if any(not isinstance(record, Mapping) for record in records):
        raise ValueError(f"{label} records must be objects")
    ids = [record.get("id") for record in records]
    if any(not isinstance(item, str) or not item for item in ids) or len(ids) != len(set(ids)):
        raise ValueError(f"{label} IDs must be non-empty and unique")


def _required_text(record: Mapping[str, Any], key: str, owner: str) -> str:
    value = record.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{owner} {key} must be a non-empty string")
    return value


def _freeze(value: Any) -> Any:
    """Recursively detach authored JSON into immutable value records."""
    if isinstance(value, dict):
        return MappingProxyType({key: _freeze(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(_freeze(item) for item in value)
    return value


def _validate_constraint_set(constraints: Any, dimension_ids: set[str]) -> None:
    if not isinstance(constraints, (list, tuple)) or not constraints:
        raise ValueError("probe constraints must be a non-empty sequence")
    if len(constraints) != len(set(constraints)):
        raise ValueError("probe constraints must be unique")
    if set(constraints) - dimension_ids:
        raise ValueError("probe references an undeclared dimension")


def _validate_epistemic_contract(contract: Any) -> tuple[str | None, tuple[str, ...], str | None]:
    if contract in ({}, None):
        return None, (), None
    if not isinstance(contract, Mapping):
        raise ValueError("epistemic_contract must be an object")
    classification = contract.get("fixture_position")
    positions = contract.get("positions")
    rule = contract.get("rule")
    if not isinstance(classification, str) or not classification:
        raise ValueError("epistemic fixture classification must be a non-empty string")
    if not isinstance(positions, list) or not positions or any(not isinstance(item, str) or not item for item in positions):
        raise ValueError("epistemic positions must be a non-empty string list")
    if len(positions) != len(set(positions)):
        raise ValueError("epistemic positions must be unique")
    if classification in positions:
        raise ValueError("synthetic fixture classification must remain separate from factual positions")
    if not isinstance(rule, str) or not rule:
        raise ValueError("epistemic preservation rule must be a non-empty string")
    return classification, tuple(positions), rule


def _freeze_instant(value: Any, label: str) -> datetime:
    if not isinstance(value, str):
        raise ValueError(f"{label} must be a timezone-aware ISO-8601 timestamp")
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        instant = datetime.fromisoformat(normalized)
    except ValueError as error:
        raise ValueError(f"{label} must be a timezone-aware ISO-8601 timestamp") from error
    if instant.tzinfo is None or instant.utcoffset() is None:
        raise ValueError(f"{label} must be a timezone-aware ISO-8601 timestamp")
    return instant


def load_experiment_fixture(manifest_path: str | Path) -> ExperimentFixture:
    manifest_path = Path(manifest_path).resolve()
    manifest, manifest_hash = _read(manifest_path)
    experiment_id = _required_text(manifest, "experiment_id", "manifest")
    artifacts = manifest.get("artifacts", {})
    try:
        state_path = (ROOT / artifacts["state"]["path"]).resolve()
        probes_path = (ROOT / artifacts["probes"]["path"]).resolve()
    except KeyError as error:
        raise ValueError("manifest must identify state and probe artifacts") from error
    data_root = (ROOT / "data" / "demonstration").resolve()
    if data_root not in state_path.parents or data_root not in probes_path.parents:
        raise ValueError("manifest artifacts must remain under data/demonstration")
    state_raw, state_hash = _read(state_path)
    probes_raw, probes_hash = _read(probes_path)

    state_id = _required_text(state_raw, "state_id", "state")
    _required_text(probes_raw, "probe_suite_id", "probe suite")
    if not state_id or probes_raw.get("state_id") != state_id:
        raise ValueError("manifest state and probes must agree on state identity")
    dimensions_raw = state_raw.get("dimensions", [])
    concepts_raw = state_raw.get("concepts", [])
    if not isinstance(dimensions_raw, list) or not dimensions_raw:
        raise ValueError("state must declare at least one dimension")
    if not isinstance(concepts_raw, list) or not concepts_raw:
        raise ValueError("state must declare at least one concept")
    _unique(dimensions_raw, "dimension")
    _unique(concepts_raw, "concept")
    dimension_ids = {item["id"] for item in dimensions_raw}
    families = set(state_raw.get("dimension_families", ()))
    dimensions = tuple(
        Dimension(_required_text(item, "id", "dimension"), _required_text(item, "family", "dimension"))
        for item in dimensions_raw
    )
    if not {item.family for item in dimensions}:
        raise ValueError("state must declare at least one non-empty dimension family")
    if families and any(item.family not in families for item in dimensions):
        raise ValueError("dimension references an undeclared family")
    concepts_list = []
    for item in concepts_raw:
        traits = item.get("traits")
        if not isinstance(traits, list) or any(not isinstance(trait, str) or not trait for trait in traits):
            raise ValueError("concept traits must be a non-empty string list")
        concepts_list.append(Concept(_required_text(item, "id", "concept"), frozenset(traits)))
    concepts = tuple(concepts_list)
    if any(not concept.traits for concept in concepts):
        raise ValueError("each concept must declare at least one trait")
    if any(not concept.traits <= dimension_ids for concept in concepts):
        raise ValueError("concept references an undeclared dimension")

    exclusions_raw = state_raw.get("composition_exclusions", ())
    if not isinstance(exclusions_raw, list):
        raise ValueError("composition_exclusions must be a list")
    exclusions = tuple(
        CompositionExclusion(
            _required_text(item, "left", "exclusion"),
            _required_text(item, "right", "exclusion"),
            _required_text(item, "scope", "exclusion"),
            _required_text(item, "kind", "exclusion"),
        )
        for item in exclusions_raw
        if isinstance(item, Mapping)
    )
    if len(exclusions) != len(exclusions_raw):
        raise ValueError("composition exclusion records must be objects")
    for exclusion in exclusions:
        if {exclusion.left, exclusion.right} - dimension_ids:
            raise ValueError("composition exclusion references an undeclared dimension")
        if exclusion.scope != state_id or exclusion.kind != "fixture_local_exclusion":
            raise ValueError("composition exclusions must be explicitly fixture-local")

    probe_groups = {}
    probe_ids: list[str] = []
    concept_ids = {concept.id for concept in concepts}
    for key, value in probes_raw.items():
        if not key.endswith("_probes") or not isinstance(value, list):
            continue
        frozen = []
        for record in value:
            if not isinstance(record, Mapping):
                raise ValueError("probe records must be objects")
            probe_ids.append(_required_text(record, "id", "probe"))
            serialized = json.dumps(record)
            if any(name in serialized for name in ("expected_ranks", "expected_entropy", "expected_margins")):
                raise ValueError("probe fixtures must not encode expected metric trajectories")
            constraints = record.get("constraints")
            if constraints is not None:
                _validate_constraint_set(constraints, dimension_ids)
            for stage in record.get("stages", ()):
                _validate_constraint_set(stage.get("constraints"), dimension_ids)
                if stage.get("expected_region") not in (None, *concept_ids):
                    raise ValueError("probe stage references an undeclared region")
            shared = record.get("shared_constraints")
            if shared is not None:
                _validate_constraint_set(shared, dimension_ids)
                for branch in record.get("branches", ()):
                    _validate_constraint_set(branch.get("additional_constraints"), dimension_ids)
                    if branch.get("expected_region") not in concept_ids:
                        raise ValueError("contrast branch references an undeclared region")
            if "target" in record and record["target"] not in concept_ids:
                raise ValueError("probe references an undeclared target")
            frozen.append(_freeze(record))
        probe_groups[key] = tuple(frozen)
    if len(probe_ids) != len(set(probe_ids)):
        raise ValueError("probe IDs must be unique")

    freeze_status = artifacts["state"].get("freeze_status")
    holdout = probes_raw.get("holdout_status")
    declared_holdout = artifacts["probes"].get("holdout_status")
    if holdout not in {"not_held_out", "held_out_after_state_freeze"} or declared_holdout != holdout:
        raise ValueError("manifest and probe suite must declare a consistent holdout status")
    if freeze_status == "candidate_not_confirmatory_freeze" and holdout == "not_held_out":
        lifecycle = DEVELOPMENT_LIFECYCLE
    elif freeze_status == "state_frozen" and holdout == "held_out_after_state_freeze":
        lifecycle = "PROBES_FROZEN_AFTER_STATE"
        if artifacts["state"].get("sha256") != state_hash or artifacts["probes"].get("sha256") != probes_hash:
            raise ValueError("confirmatory artifact hashes must match")
        try:
            state_at = artifacts["state"]["frozen_at"]
            probes_at = artifacts["probes"]["frozen_at"]
        except KeyError as error:
            raise ValueError("confirmatory artifacts require freeze timestamps") from error
        state_instant = _freeze_instant(state_at, "state frozen_at")
        probe_instant = _freeze_instant(probes_at, "probe frozen_at")
        if state_instant >= probe_instant:
            raise ValueError("probe freeze must chronologically follow state freeze")
    else:
        raise ValueError("unsupported or inconsistent fixture lifecycle")
    epistemic, positions, rule = _validate_epistemic_contract(state_raw.get("epistemic_contract", {}))
    state = SemanticStateFixture(
        state_raw["schema_version"], state_id, state_raw["title"], state_path,
        state_hash, lifecycle, state_raw["evidence_boundary"], dimensions, concepts,
        exclusions, epistemic, positions, rule,
    )
    probes = ProbeSuiteFixture(
        probes_raw["schema_version"], probes_raw["probe_suite_id"], state_id,
        probes_path, probes_hash, holdout, MappingProxyType(probe_groups),
    )
    return ExperimentFixture(
        experiment_id, manifest_path, manifest_hash, lifecycle, state, probes
    )
