"""Benchmark Experiment 4.1 through the accumulated capability source path."""

from __future__ import annotations

import itertools
import json
import math
import statistics
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path

from src.helpers.artifacts import compare_artifact_pair, write_artifact_pair
from src.helpers.hashing import sha256_bytes, sha256_file
from src.helpers.json_io import canonical_json_bytes
from src.helpers.research_cli import ResearchCommand, run_research_command
from src.semantic_navigation.navigation import (
    AMBIGUOUS,
    IDENTIFIABLE,
    UNSUPPORTED,
    SemanticNavigationFlow,
)
from src.semantic_representation.governed_coordinates import SemanticEntity, encode_query


ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "data" / "demonstration" / "compiled_encyclopedic_navigation_seed_v1.json"
RESULT_PATH = ROOT / "benchmark" / "results" / "compiled-encyclopedic-navigation-v1.json"
REPORT_PATH = ROOT / "docs" / "capabilities" / "semantic-navigation" / "results" / "compiled-encyclopedic-navigation-v1.md"
STUDY_PATH = ROOT / "docs" / "capabilities" / "semantic-navigation" / "experiment.md"
REPRESENTATION_PATH = ROOT / "src" / "semantic_representation" / "governed_coordinates.py"
KNOWLEDGE_STATE_PATH = ROOT / "src" / "knowledge_state_execution" / "compiled_incidence.py"
COMPOSITION_PATH = ROOT / "src" / "combinatorial_uniqueness" / "candidate_regions.py"
NAVIGATION_PATH = ROOT / "src" / "semantic_navigation" / "navigation.py"


@dataclass(frozen=True)
class RetrievalQuery:
    id: str
    condition: str
    observed: dict[str, str]


@dataclass(frozen=True)
class FlatScanCost:
    record_field_comparisons: int
    result_materializations: int

    @property
    def total_operations(self) -> int:
        return self.record_field_comparisons + self.result_materializations


def _entity(item: dict, dimensions: tuple[str, ...]) -> SemanticEntity:
    return SemanticEntity(
        item["id"],
        item["label"],
        {dimension: item.get(dimension) for dimension in dimensions},
    )


def _load_fixture() -> tuple[dict, tuple[str, ...], tuple[SemanticEntity, ...], tuple[SemanticEntity, ...]]:
    fixture = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    dimensions = tuple(fixture["dimensions"])
    records = tuple(_entity(item, dimensions) for item in fixture["records"])
    incomplete = tuple(_entity(item, dimensions) for item in fixture.get("incomplete_records", ()))
    return fixture, dimensions, records, incomplete


def _condition(width: int, dimension_count: int) -> str:
    if width == dimension_count:
        return "complete"
    if width == dimension_count - 1:
        return "one_missing"
    return "multiple_missing"


def build_queries(
    records: tuple[SemanticEntity, ...],
    dimensions: tuple[str, ...],
) -> tuple[RetrievalQuery, ...]:
    unique: dict[tuple[tuple[str, str], ...], RetrievalQuery] = {}
    for record in records:
        available = tuple(dimension for dimension in dimensions if record.attributes[dimension] is not None)
        for width in range(1, len(available) + 1):
            for selected in itertools.combinations(available, width):
                observed = {dimension: record.attributes[dimension] for dimension in selected}
                key = tuple((dimension, observed[dimension]) for dimension in selected)
                if key not in unique:
                    encoded = "+".join(f"{dimension}:{observed[dimension]}" for dimension in selected)
                    unique[key] = RetrievalQuery(
                        f"{_condition(width, len(dimensions))}:{encoded}",
                        _condition(width, len(dimensions)),
                        observed,  # type: ignore[arg-type]
                    )

    unsupported = (
        {"habitat": "polar", "diet": "herbivore", "activity": "nocturnal", "sociality": "colony"},
        {"habitat": "ocean", "diet": "herbivore", "activity": "nocturnal", "sociality": "pack"},
        {"habitat": "desert", "diet": "carnivore", "activity": "diurnal", "sociality": "herd"},
    )
    for position, observed in enumerate(unsupported, 1):
        unique[tuple(observed.items())] = RetrievalQuery(
            f"unsupported:{position}", "unsupported", observed,
        )
    return tuple(unique.values())


def _flat_scan(
    records: tuple[SemanticEntity, ...],
    observed: dict[str, str],
) -> tuple[tuple[str, ...], FlatScanCost]:
    matches = []
    comparisons = 0
    for record in records:
        compatible = True
        for dimension, value in observed.items():
            comparisons += 1
            if record.attributes[dimension] != value:
                compatible = False
                break
        if compatible:
            matches.append(record.id)
    return tuple(matches), FlatScanCost(comparisons, len(matches))


def _precision_recall(actual: tuple[str, ...], expected: tuple[str, ...]) -> tuple[float, float, float]:
    actual_set = set(actual)
    expected_set = set(expected)
    intersection = len(actual_set & expected_set)
    precision = intersection / len(actual_set) if actual_set else (1.0 if not expected_set else 0.0)
    recall = intersection / len(expected_set) if expected_set else (1.0 if not actual_set else 0.0)
    union = len(actual_set | expected_set)
    return precision, recall, intersection / union if union else 1.0


def _equivalent(left, right) -> bool:
    return (
        left.candidate_ids == right.candidate_ids
        and left.status == right.status
        and dict(left.commonality) == dict(right.commonality)
        and dict(left.deterministic_imputations) == dict(right.deterministic_imputations)
        and {key: dict(value) for key, value in left.distinctions.items()}
        == {key: dict(value) for key, value in right.distinctions.items()}
        and left.next_dimension == right.next_dimension
        and math.isclose(
            left.next_dimension_information_gain,
            right.next_dimension_information_gain,
            abs_tol=1e-12,
        )
    )


def _oracle_navigation(
    records: tuple[SemanticEntity, ...],
    dimensions: tuple[str, ...],
    candidate_ids: tuple[str, ...],
    observed: dict[str, str],
) -> dict:
    selected = set(candidate_ids)
    candidates = tuple(record for record in records if record.id in selected)
    commonality = {}
    for dimension in dimensions:
        values = {record.attributes[dimension] for record in candidates}
        if len(values) == 1 and None not in values:
            commonality[dimension] = next(iter(values))

    distinctions = {}
    for dimension in dimensions:
        if dimension in observed:
            continue
        groups = {}
        for record in candidates:
            value = record.attributes[dimension] or "UNKNOWN"
            groups.setdefault(value, []).append(record.id)
        distinctions[dimension] = {
            value: tuple(ids) for value, ids in sorted(groups.items())
        }
    imputations = {
        dimension: next(iter(partition))
        for dimension, partition in distinctions.items()
        if len(partition) == 1 and "UNKNOWN" not in partition
    }
    gains = {}
    for dimension, partition in distinctions.items():
        if len(partition) <= 1:
            continue
        total = sum(len(ids) for ids in partition.values())
        gains[dimension] = -sum(
            (len(ids) / total) * math.log2(len(ids) / total)
            for ids in partition.values()
        )
    next_dimension = max(
        gains,
        key=lambda item: (gains[item], -dimensions.index(item)),
    ) if gains else None
    return {
        "commonality": commonality,
        "deterministic_imputations": imputations,
        "distinctions": distinctions,
        "next_dimension": next_dimension,
        "next_dimension_information_gain": 0.0 if next_dimension is None else gains[next_dimension],
    }


def _serialize_navigation(result) -> dict:
    cost = result.region.cost
    return {
        "candidate_ids": list(result.candidate_ids),
        "status": result.status,
        "commonality": dict(result.commonality),
        "deterministic_imputations": dict(result.deterministic_imputations),
        "distinctions": {
            dimension: {value: list(ids) for value, ids in partition.items()}
            for dimension, partition in result.distinctions.items()
        },
        "next_dimension": result.next_dimension,
        "next_dimension_information_gain": result.next_dimension_information_gain,
        "region_cost": asdict(cost) | {"total_operations": cost.total_operations},
    }


def _serialize_query(flow, state, query: RetrievalQuery) -> dict:
    records = state.basis.entities
    dimensions = state.basis.dimensions
    expected, scan_cost = _flat_scan(records, query.observed)
    semantic = flow.execute(state, query.observed)
    codes = encode_query(state.basis, query.observed)
    coded = flow.execute_codes(state, codes)
    rebuilt = flow.govern_and_compile(f"reconstructed:{query.id}", dimensions, records)
    reconstructed = flow.execute(rebuilt, query.observed)
    reconstruction_operations = (
        rebuilt.basis.representation.total_operations
        + rebuilt.knowledge_state.compilation.total_operations
        + reconstructed.region.cost.total_operations
    )
    precision, recall, jaccard = _precision_recall(semantic.candidate_ids, expected)
    expected_status = UNSUPPORTED if not expected else IDENTIFIABLE if len(expected) == 1 else AMBIGUOUS
    oracle = _oracle_navigation(records, dimensions, expected, query.observed)
    navigation_correct = (
        dict(semantic.commonality) == oracle["commonality"]
        and dict(semantic.deterministic_imputations) == oracle["deterministic_imputations"]
        and {key: dict(value) for key, value in semantic.distinctions.items()} == oracle["distinctions"]
        and semantic.next_dimension == oracle["next_dimension"]
        and math.isclose(
            semantic.next_dimension_information_gain,
            oracle["next_dimension_information_gain"],
            abs_tol=1e-12,
        )
    )
    return {
        "id": query.id,
        "condition": query.condition,
        "observed": query.observed,
        "coded_query": {
            "dimensions": list(codes.dimensions),
            "coordinate_codes": list(codes.coordinate_codes),
        },
        "expected_candidates": list(expected),
        "expected_status": expected_status,
        "compiled_semantic": _serialize_navigation(semantic),
        "compiled_codes": _serialize_navigation(coded),
        "flat_scan_cost": asdict(scan_cost) | {"total_operations": scan_cost.total_operations},
        "reconstructed_execution": {
            "navigation": _serialize_navigation(reconstructed),
            "total_operations": reconstruction_operations,
        },
        "metrics": {
            "exact_set": semantic.candidate_ids == expected,
            "candidate_precision": precision,
            "candidate_recall": recall,
            "candidate_jaccard": jaccard,
            "status_correct": semantic.status == expected_status,
            "commonality_correct": dict(semantic.commonality) == oracle["commonality"],
            "deterministic_imputation_correct": (
                dict(semantic.deterministic_imputations) == oracle["deterministic_imputations"]
            ),
            "next_dimension_correct": (
                semantic.next_dimension == oracle["next_dimension"]
                and math.isclose(
                    semantic.next_dimension_information_gain,
                    oracle["next_dimension_information_gain"],
                    abs_tol=1e-12,
                )
            ),
            "navigation_correct": navigation_correct,
            "code_equivalent": _equivalent(semantic, coded),
            "reconstructed_equivalent": _equivalent(semantic, reconstructed),
        },
    }


def _aggregate_queries(queries: list[dict]) -> dict:
    metrics = [query["metrics"] for query in queries]
    compiled_operations = sum(
        query["compiled_semantic"]["region_cost"]["total_operations"] for query in queries
    )
    scan_operations = sum(query["flat_scan_cost"]["total_operations"] for query in queries)
    reconstructed_operations = sum(query["reconstructed_execution"]["total_operations"] for query in queries)
    return {
        "query_count": len(queries),
        "condition_counts": dict(sorted(Counter(query["condition"] for query in queries).items())),
        "status_counts": dict(sorted(Counter(query["expected_status"] for query in queries).items())),
        "exact_set_accuracy": statistics.fmean(metric["exact_set"] for metric in metrics),
        "mean_candidate_precision": statistics.fmean(metric["candidate_precision"] for metric in metrics),
        "mean_candidate_recall": statistics.fmean(metric["candidate_recall"] for metric in metrics),
        "mean_candidate_jaccard": statistics.fmean(metric["candidate_jaccard"] for metric in metrics),
        "status_accuracy": statistics.fmean(metric["status_correct"] for metric in metrics),
        "commonality_accuracy": statistics.fmean(metric["commonality_correct"] for metric in metrics),
        "deterministic_imputation_accuracy": statistics.fmean(
            metric["deterministic_imputation_correct"] for metric in metrics
        ),
        "next_dimension_accuracy": statistics.fmean(metric["next_dimension_correct"] for metric in metrics),
        "navigation_accuracy": statistics.fmean(metric["navigation_correct"] for metric in metrics),
        "code_equivalence_rate": statistics.fmean(metric["code_equivalent"] for metric in metrics),
        "reconstructed_equivalence_rate": statistics.fmean(metric["reconstructed_equivalent"] for metric in metrics),
        "compiled_query_operations": compiled_operations,
        "flat_scan_operations": scan_operations,
        "reconstructed_execution_operations": reconstructed_operations,
    }


def _query_failed(query: dict) -> bool:
    """Identify a diagnostic trace that must remain visible in published evidence."""
    boolean_metrics = (
        value for value in query["metrics"].values() if isinstance(value, bool)
    )
    return not all(boolean_metrics)


def evidence_manifest(result: dict) -> dict:
    """Project full runtime diagnostics into compact, content-addressed evidence."""
    queries = result["queries"]
    failures = [query for query in queries if _query_failed(query)]
    manifest = {key: value for key, value in result.items() if key != "queries"}
    conditions = sorted({query["condition"] for query in queries})
    manifest["query_evidence"] = {
        "query_count": len(queries),
        "trace_sha256": sha256_bytes(canonical_json_bytes(queries)),
        "condition_summaries": {
            condition: _aggregate_queries([
                query for query in queries if query["condition"] == condition
            ])
            for condition in conditions
        },
        "failed_query_count": len(failures),
        "failed_query_ids": [query["id"] for query in failures],
        "failed_query_samples": failures[:10],
    }
    return manifest


def _identification_summary(flow, state) -> tuple[list[dict], dict]:
    profiles = flow.identification_profiles(state)
    serialized = [{
        "candidate_ids": list(profile.candidate_ids),
        "complete_signature": dict(profile.complete_signature),
        "minimum_dimension_count": profile.minimum_dimension_count,
        "minimum_dimension_sets": [list(items) for items in profile.minimum_dimension_sets],
        "uniquely_identifiable": profile.uniquely_identifiable,
    } for profile in profiles]
    distribution = Counter(profile.minimum_dimension_count for profile in profiles)
    return serialized, {
        "equivalence_class_count": len(profiles),
        "uniquely_identifiable_class_count": sum(profile.uniquely_identifiable for profile in profiles),
        "ambiguous_complete_signature_class_count": sum(not profile.uniquely_identifiable for profile in profiles),
        "animal_count_in_ambiguous_complete_signatures": sum(
            len(profile.candidate_ids) for profile in profiles if not profile.uniquely_identifiable
        ),
        "minimum_dimension_count_distribution": {
            str(key): value
            for key, value in sorted(distribution.items(), key=lambda item: (item[0] is None, item[0]))
        },
    }


def _scaling_row(
    flow: SemanticNavigationFlow,
    records: tuple[SemanticEntity, ...],
    dimensions: tuple[str, ...],
    size: int,
) -> dict:
    subset = records[:size]
    state = flow.govern_and_compile(f"scale:{size}", dimensions, subset)
    serialized = [_serialize_query(flow, state, query) for query in build_queries(subset, dimensions)]
    aggregate = _aggregate_queries(serialized)
    construction = (
        state.basis.representation.total_operations
        + state.knowledge_state.compilation.total_operations
    )
    compiled_total = construction + aggregate["compiled_query_operations"]
    scan_total = aggregate["flat_scan_operations"]
    saving = (
        aggregate["flat_scan_operations"] - aggregate["compiled_query_operations"]
    ) / aggregate["query_count"]
    return {
        "record_count": size,
        "query_count": aggregate["query_count"],
        "exact_set_accuracy": aggregate["exact_set_accuracy"],
        "representation_operations": state.basis.representation.total_operations,
        "knowledge_compilation_operations": state.knowledge_state.compilation.total_operations,
        "compiled_once_operations": compiled_total,
        "flat_scan_operations": scan_total,
        "reconstructed_per_query_operations": aggregate["reconstructed_execution_operations"],
        "warm_compiled_query_operations": aggregate["compiled_query_operations"],
        "compiled_vs_scan_operation_ratio_including_construction": compiled_total / scan_total,
        "warm_compiled_vs_scan_operation_ratio": aggregate["compiled_query_operations"] / scan_total,
        "amortization_break_even_query_count": math.ceil(construction / saving) if saving > 0 else None,
        "represented_logical_bytes": state.basis.representation.logical_bytes,
        "compiled_index_logical_bytes": state.knowledge_state.compilation.logical_bytes,
    }


def run_experiment() -> dict:
    fixture, dimensions, records, incomplete = _load_fixture()
    flow = SemanticNavigationFlow()
    state = flow.govern_and_compile(fixture["state_id"], dimensions, records)
    incomplete_state = flow.govern_and_compile(f"{fixture['state_id']}:incomplete", dimensions, incomplete)
    serialized = [_serialize_query(flow, state, query) for query in build_queries(records, dimensions)]
    aggregate = _aggregate_queries(serialized)
    profiles, identification = _identification_summary(flow, state)
    scaling = [
        _scaling_row(flow, records, dimensions, size)
        for size in dict.fromkeys(size for size in (15, 30, len(records)) if size <= len(records))
    ]
    expected_incomplete = {
        record.id: tuple(dimension for dimension in dimensions if record.attributes[dimension] is None)
        for record in incomplete
    }
    all_metrics = [query["metrics"] for query in serialized]
    criteria = {
        "all_candidate_sets_exact": all(metric["exact_set"] for metric in all_metrics),
        "all_statuses_correct": all(metric["status_correct"] for metric in all_metrics),
        "all_navigation_diagnostics_exact": all(metric["navigation_correct"] for metric in all_metrics),
        "all_semantic_and_code_queries_equivalent": all(metric["code_equivalent"] for metric in all_metrics),
        "all_reconstructed_states_equivalent": all(metric["reconstructed_equivalent"] for metric in all_metrics),
        "incomplete_records_detected": (
            dict(incomplete_state.basis.incomplete_entities) == expected_incomplete and bool(incomplete)
        ),
        "ambiguous_complete_signatures_reported": identification["ambiguous_complete_signature_class_count"] > 0,
        "all_capability_snapshots_present": bool(
            state.basis.snapshot_id and state.knowledge_state.snapshot_id
        ),
        "compiled_warm_queries_cheaper_than_flat_scan": all(
            row["warm_compiled_vs_scan_operation_ratio"] < 1.0 for row in scaling
        ),
        "compiled_cost_amortizes": all(row["amortization_break_even_query_count"] is not None for row in scaling),
    }
    return {
        "schema_version": "3.1",
        "experiment_id": "experiment-4.1-compiled-encyclopedic-navigation-v1",
        "title": "Experiment 4.1 - Compiled Encyclopedic Navigation",
        "research_stream": "Programme 4 - Semantic Navigation",
        "research_question": (
            "Can represented semantic dimensions, compiled once and composed at query time, support exact "
            "candidate retrieval and useful ambiguity navigation with lower repeated work?"
        ),
        "fixture": {
            "state_id": fixture["state_id"],
            "lifecycle": fixture["lifecycle"],
            "annotation_status": fixture["annotation_status"],
            "record_count": len(records),
            "incomplete_probe_count": len(incomplete),
            "dimensions": list(dimensions),
            "evidence_boundary": fixture["evidence_boundary"],
        },
        "capability_contributions": {
            "semantic_representation": {
                "contract": "GovernedCoordinateBasis",
                "snapshot_id": state.basis.snapshot_id,
                "coordinate_count": len(state.basis.coordinates),
                "coordinate_codes": dict(state.basis.coordinate_codes),
                "metrics": asdict(state.basis.representation) | {
                    "total_operations": state.basis.representation.total_operations,
                },
            },
            "knowledge_state_execution": {
                "contract": "CompiledIncidenceState",
                "snapshot_id": state.knowledge_state.snapshot_id,
                "posting_count": len(state.knowledge_state.postings),
                "signature_class_count": len(state.knowledge_state.signature_classes),
                "metrics": asdict(state.knowledge_state.compilation) | {
                    "total_operations": state.knowledge_state.compilation.total_operations,
                },
            },
            "combinatorial_uniqueness": {
                "contract": "compose_candidate_region",
                "query_count": aggregate["query_count"],
                "query_operations": aggregate["compiled_query_operations"],
                "exact_set_accuracy": aggregate["exact_set_accuracy"],
            },
            "semantic_navigation": {
                "contract": "SemanticNavigationFlow",
                "navigation_accuracy": aggregate["navigation_accuracy"],
                "status_accuracy": aggregate["status_accuracy"],
                "code_equivalence_rate": aggregate["code_equivalence_rate"],
            },
        },
        "incomplete_records": {
            key: list(value) for key, value in incomplete_state.basis.incomplete_entities.items()
        },
        "aggregate": aggregate,
        "identification": identification,
        "identification_profiles": profiles,
        "scaling": scaling,
        "queries": serialized,
        "conformity": {
            "judgment": "ACCUMULATED_MECHANICS_CONFORMANT" if all(criteria.values()) else "ACCUMULATED_MECHANICS_NONCONFORMANT",
            "evidence_strength": "PROMPT_PROVIDED_SEED",
            "criteria": criteria,
        },
        "artifact_identities": {
            "fixture_sha256": sha256_file(DATA_PATH),
            "semantic_representation_sha256": sha256_file(REPRESENTATION_PATH),
            "knowledge_state_execution_sha256": sha256_file(KNOWLEDGE_STATE_PATH),
            "combinatorial_uniqueness_sha256": sha256_file(COMPOSITION_PATH),
            "semantic_navigation_sha256": sha256_file(NAVIGATION_PATH),
            "experiment_sha256": sha256_file(Path(__file__)),
            "study_sha256": sha256_file(STUDY_PATH),
        },
        "interpretation": (
            "The seed positively demonstrates one accumulated source path: governed coordinate representation, "
            "persistent incidence compilation, exact candidate-region composition, and explicit semantic navigation. "
            "Accuracy parity with correct exact controls is required."
        ),
        "evidence_boundary": (
            "This is a mechanics result over prompt-provided animal attributes and deterministic operation counts. "
            "It is not the independently sourced 100/250/500-animal study, a wall-clock claim, natural-language "
            "understanding, relational inference, or independent validation of the three upstream programmes."
        ),
    }


def markdown_report(result: dict) -> str:
    aggregate = result["aggregate"]
    identification = result["identification"]
    query_evidence = evidence_manifest(result)["query_evidence"]
    lines = [
        "# Experiment 4.1 - Compiled Encyclopedic Navigation",
        "",
        "## Result",
        "",
        f"Judgment: `{result['conformity']['judgment']}`. Evidence strength: `{result['conformity']['evidence_strength']}`.",
        "",
        result["interpretation"],
        "",
        "## Capability Contributions",
        "",
        "| Capability | Executed contract | Evidence in this experiment |",
        "| --- | --- | --- |",
        f"| Semantic Representation | `{result['capability_contributions']['semantic_representation']['contract']}` | {result['capability_contributions']['semantic_representation']['coordinate_count']} governed coordinates and reversible codes |",
        f"| Knowledge State Execution | `{result['capability_contributions']['knowledge_state_execution']['contract']}` | Persistent postings, {result['capability_contributions']['knowledge_state_execution']['signature_class_count']} signature classes, and named snapshot |",
        f"| Combinatorial Uniqueness | `{result['capability_contributions']['combinatorial_uniqueness']['contract']}` | {aggregate['query_count']} exact candidate-region compositions |",
        f"| Semantic Navigation | `{result['capability_contributions']['semantic_navigation']['contract']}` | Exact statuses, imputations, partitions, next questions, and commonality |",
        "",
        "## Retrieval And Navigation",
        "",
        "| Measure | Result |",
        "| --- | ---: |",
        f"| Structured queries | {aggregate['query_count']} |",
        f"| Exact candidate-set accuracy | {aggregate['exact_set_accuracy']:.3f} |",
        f"| Candidate precision | {aggregate['mean_candidate_precision']:.3f} |",
        f"| Candidate recall | {aggregate['mean_candidate_recall']:.3f} |",
        f"| Status accuracy | {aggregate['status_accuracy']:.3f} |",
        f"| Navigation accuracy | {aggregate['navigation_accuracy']:.3f} |",
        f"| Semantic/code equivalence | {aggregate['code_equivalence_rate']:.3f} |",
        f"| Query-trace digest | `{query_evidence['trace_sha256']}` |",
        "",
        "## Matrix Resolution",
        "",
        f"The {result['fixture']['record_count']}-animal seed contains {identification['equivalence_class_count']} complete-signature equivalence classes. "
        f"{identification['ambiguous_complete_signature_class_count']} classes remain ambiguous with all four dimensions, containing "
        f"{identification['animal_count_in_ambiguous_complete_signatures']} animals.",
        "",
        "| Minimum dimensions | Equivalence classes |",
        "| ---: | ---: |",
    ]
    for width, count in identification["minimum_dimension_count_distribution"].items():
        lines.append(f"| {width} | {count} |")
    lines.extend([
        "",
        "## Compute Scaling",
        "",
        "| Animals | Queries | Warm compiled / scan | Constructed once / scan | Break-even queries |",
        "| ---: | ---: | ---: | ---: | ---: |",
    ])
    for row in result["scaling"]:
        lines.append(
            f"| {row['record_count']} | {row['query_count']} | "
            f"{row['warm_compiled_vs_scan_operation_ratio']:.3f} | "
            f"{row['compiled_vs_scan_operation_ratio_including_construction']:.3f} | "
            f"{row['amortization_break_even_query_count']} |"
        )
    lines.extend([
        "",
        "## Interpretation Boundary",
        "",
        "This is an accumulated-capability experiment. It shows that the four operational contracts compose; it does not replace the controlled evidence required by any upstream programme. Genuine equivalence classes remain ambiguous instead of being ranked into invented specificity.",
        "",
        "Natural-language translation and relational inference remain separate experiments.",
        "",
        "## Evidence Boundary",
        "",
        result["evidence_boundary"],
    ])
    return "\n".join(lines) + "\n"


def write_results(result: dict, result_path: Path = RESULT_PATH, report_path: Path = REPORT_PATH) -> None:
    write_artifact_pair(
        result_path,
        evidence_manifest(result),
        report_path,
        markdown_report(result),
    )


def check_result(result: dict, result_path: Path = RESULT_PATH, report_path: Path = REPORT_PATH) -> None:
    comparison = compare_artifact_pair(
        evidence_manifest(result),
        markdown_report(result),
        result_path,
        report_path,
    )
    if comparison.missing_paths:
        raise SystemExit("Experiment 4.1 reference artifacts are missing; run --write.")
    if not comparison.json_matches:
        raise SystemExit("Experiment 4.1 machine evidence differs from the reference artifact.")
    if not comparison.text_matches:
        raise SystemExit("Experiment 4.1 report differs from the reference artifact.")


def main() -> None:
    run_research_command(ResearchCommand(
        description="Run Experiment 4.1 compiled encyclopedic navigation.",
        run=run_experiment,
        render=markdown_report,
        write=write_results,
        check=check_result,
    ))


if __name__ == "__main__":
    main()
