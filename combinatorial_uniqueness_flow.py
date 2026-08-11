"""Operational facade for governed combinatorial semantic composition."""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping, Sequence

import numpy as np

from combinatorial_uniqueness_fixture import SemanticStateFixture
from compose_concepts import ActivatedField, distribution_metrics, soft_intersection
from elaborations.mml_graph import GraphModel, stable_sentence_id


RESOLVED = "RESOLVED"
UNRESOLVED = "UNRESOLVED"
INVALID = "INVALID"


@dataclass(frozen=True)
class ValidityPolicy:
    policy_id: str
    minimum_per_field_support: float = 0.0
    minimum_top_concentration: float = 0.0
    minimum_top_margin: float = 0.0

    def __post_init__(self) -> None:
        if not isinstance(self.policy_id, str) or not re.search(r"-v[0-9]+$", self.policy_id):
            raise ValueError("validity policy requires a versioned policy_id ending in -vN")
        thresholds = (
            self.minimum_per_field_support,
            self.minimum_top_concentration,
            self.minimum_top_margin,
        )
        if any(not math.isfinite(value) or value < 0 for value in thresholds):
            raise ValueError("validity thresholds must be finite and non-negative")


@dataclass(frozen=True)
class CompiledSemanticState:
    source_id: str
    source_sha256: str
    snapshot_id: str
    graph: GraphModel
    concepts: tuple[str, ...]
    dimensions: tuple[str, ...]
    incidence: Mapping[str, frozenset[str]]
    exclusions: frozenset[frozenset[str]]
    relation_ids: tuple[str, ...]
    epistemic_classification: str | None


@dataclass(frozen=True)
class PrefixMeasurement:
    constraints: tuple[str, ...]
    candidate_values: tuple[float, ...] | None
    cumulative_structural_information_bits: float | None
    entropy: float | None
    normalized_entropy: float | None
    effective_candidate_count: float | None
    concentration: float | None
    top_k_mass: float | None
    top_k: int | None
    top_margin: float | None
    hard_intersection_candidates: tuple[str, ...]


@dataclass(frozen=True)
class CompositionExecution:
    constraints: tuple[str, ...]
    status: str
    reason_code: str
    mechanism_status: str
    mechanism_reason_code: str
    governance_status: str
    governance_reason_code: str
    prefixes: tuple[PrefixMeasurement, ...]
    top_candidate: str | None
    soft_top_candidate: str | None
    hard_intersection_candidates: tuple[str, ...]
    epistemic_classification: str | None
    snapshot_id: str

    @property
    def epistemic_position(self) -> str | None:
        """Compatibility view; this is a fixture classification, not factual promotion."""
        return self.epistemic_classification


class CombinatorialUniquenessFlow:
    """Compile fixture traits and execute inspectable composition prefixes."""

    def govern_and_compile(self, fixture: SemanticStateFixture) -> CompiledSemanticState:
        concepts = tuple(item.id for item in fixture.concepts)
        dimensions = tuple(item.id for item in fixture.dimensions)
        nodes = tuple(sorted((*concepts, *dimensions)))
        sentences = tuple(nodes)
        evidence = {node: stable_sentence_id(node) for node in nodes}
        relations = []
        incidence = {dimension: set() for dimension in dimensions}
        for concept in fixture.concepts:
            for trait in sorted(concept.traits):
                incidence[trait].add(concept.id)
                relations.append({
                    "id": f"fixture:{concept.id}:{trait}",
                    "source": trait,
                    "relation": "supports",
                    "target": concept.id,
                    "weight": 1.0,
                    "evidence_ids": [evidence[trait]],
                })
        graph = GraphModel.from_sources(sentences, relations=relations)
        return CompiledSemanticState(
            fixture.state_id, fixture.source_sha256, graph.snapshot_id, graph,
            concepts, dimensions,
            MappingProxyType({key: frozenset(value) for key, value in incidence.items()}),
            frozenset(frozenset((item.left, item.right)) for item in fixture.exclusions),
            tuple(record["id"] for record in relations), fixture.epistemic_classification,
        )

    def execute(
        self,
        state: CompiledSemanticState,
        constraints: Sequence[str],
        policy: ValidityPolicy,
    ) -> CompositionExecution:
        ordered = tuple(constraints)
        if not ordered or any(item not in state.dimensions for item in ordered):
            return CompositionExecution(ordered, UNRESOLVED, "UNKNOWN_CONSTRAINT",
                                        UNRESOLVED, "UNKNOWN_CONSTRAINT",
                                        UNRESOLVED, "UNKNOWN_CONSTRAINT", (), None, None, (),
                                        state.epistemic_classification, state.snapshot_id)
        pairs = {frozenset((left, right)) for i, left in enumerate(ordered) for right in ordered[i + 1:]}
        declared_exclusion = bool(pairs & state.exclusions)

        fields = tuple(ActivatedField(item, tuple(state.graph.single_field_activation(item))) for item in ordered)
        concept_indices = tuple(state.graph.word2idx[item] for item in state.concepts)
        prefixes = []
        previous = set(state.concepts)
        cumulative_information: float | None = 0.0
        for width in range(1, len(fields) + 1):
            retained = previous & set(state.incidence[ordered[width - 1]])
            if previous and retained and cumulative_information is not None:
                cumulative_information = cumulative_information - math.log2(len(retained) / len(previous))
            elif not retained:
                # An empty governed intersection has no finite information value;
                # ``None`` is explicit and JSON-safe (unlike positive infinity).
                cumulative_information = None
            previous = retained
            if any(not any(field.values) for field in fields[:width]):
                prefixes.append(PrefixMeasurement(
                    ordered[:width], None, cumulative_information, None, None, None,
                    None, None, None, None, tuple(sorted(retained)),
                ))
                continue
            composed = soft_intersection(fields[:width], background=state.graph.background)
            candidate_values = np.asarray(composed.values)[list(concept_indices)]
            if candidate_values.sum() <= 0:
                prefixes.append(PrefixMeasurement(
                    ordered[:width], None, None, None, None, None, None, None, None, None,
                    tuple(sorted(retained)),
                ))
                continue
            else:
                normalized = candidate_values / candidate_values.sum()
            selected_top_k = min(3, len(normalized))
            metrics = distribution_metrics(normalized, top_k=selected_top_k)
            ordered_values = np.sort(normalized)
            margin = float(ordered_values[-1] - ordered_values[-2]) if len(ordered_values) > 1 else float(ordered_values[-1])
            prefixes.append(PrefixMeasurement(
                ordered[:width], tuple(float(v) for v in normalized), cumulative_information,
                metrics.entropy, metrics.normalized_entropy, metrics.effective_candidate_count,
                metrics.concentration, metrics.top_k_mass, selected_top_k, margin,
                tuple(sorted(retained)),
            ))

        final = prefixes[-1]
        minimum_support = min(float(np.asarray(field.values)[list(concept_indices)].sum()) for field in fields)
        soft_top = None if final.candidate_values is None else state.concepts[int(np.argmax(final.candidate_values))]
        if minimum_support <= policy.minimum_per_field_support or final.concentration is None or final.top_margin is None:
            mechanism_status, mechanism_reason = UNRESOLVED, "INSUFFICIENT_FIELD_SUPPORT"
        elif final.concentration <= policy.minimum_top_concentration or final.top_margin <= policy.minimum_top_margin:
            mechanism_status, mechanism_reason = UNRESOLVED, "AMBIGUOUS_FIELD"
        else:
            mechanism_status, mechanism_reason = RESOLVED, "NUMERIC_FIELD_RESOLVED"

        if declared_exclusion:
            governance_status, governance_reason = INVALID, "DECLARED_CONTRADICTION"
        elif not previous:
            governance_status, governance_reason = UNRESOLVED, "UNSUPPORTED_COMBINATION"
        elif soft_top not in previous:
            governance_status, governance_reason = UNRESOLVED, "SOFT_TOP_OUTSIDE_GOVERNED_INTERSECTION"
        else:
            governance_status, governance_reason = RESOLVED, "GOVERNED_INTERSECTION_SATISFIED"

        if governance_status == INVALID:
            status, reason = INVALID, governance_reason
        elif mechanism_status != RESOLVED:
            status, reason = UNRESOLVED, mechanism_reason
        elif governance_status != RESOLVED:
            status, reason = UNRESOLVED, governance_reason
        else:
            status, reason = RESOLVED, "RESOLVED_SEMANTIC_REGION"
        top = soft_top if status == RESOLVED else None
        return CompositionExecution(ordered, status, reason,
                                    mechanism_status, mechanism_reason,
                                    governance_status, governance_reason,
                                    tuple(prefixes), top, soft_top,
                                    tuple(sorted(previous)), state.epistemic_classification, state.snapshot_id)
