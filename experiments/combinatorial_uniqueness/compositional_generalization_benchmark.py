"""Experiment 3.4: structurally held-out compositional generalization."""

from __future__ import annotations

import hashlib
import json
import statistics
from collections import defaultdict
from pathlib import Path

import numpy as np

from src.combinatorial_uniqueness.compositional_generalization import (
    SCORERS,
    EntitySignature,
    FamilySpec,
    compile_pairwise_state,
    flat_keyword_scores,
    materialize_split,
    rank_target,
    symbolic_conjunction_scores,
)
from src.helpers.artifacts import compare_artifact_pair, write_artifact_pair
from src.helpers.hashing import sha256_file
from src.helpers.research_cli import ResearchCommand, run_research_command


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "demonstration"
MANIFEST_PATH = DATA / "compositional_generalization_v1.json"
RESULT_PATH = ROOT / "benchmark" / "results" / "compositional-generalization-v1.json"
REPORT_PATH = ROOT / "docs" / "capabilities" / "combinatorial-uniqueness" / "results" / "compositional-generalization-v1.md"
STUDY_PATH = ROOT / "docs" / "capabilities" / "combinatorial-uniqueness" / "studies" / "3.4-compositional-generalization.md"
KERNEL_PATH = ROOT / "src" / "combinatorial_uniqueness" / "compositional_generalization.py"


def _read_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as source:
        return json.load(source)


def _load_contract() -> tuple[dict, dict, dict, tuple[FamilySpec, ...]]:
    manifest = _read_json(MANIFEST_PATH)
    state_path = ROOT / manifest["artifacts"]["state"]["path"]
    probes_path = ROOT / manifest["artifacts"]["probes"]["path"]
    state = _read_json(state_path)
    probes = _read_json(probes_path)
    if probes["state_id"] != state["state_id"]:
        raise ValueError("state and probes must share one state identity")
    radix = state["latent_radix"]
    families = tuple(
        FamilySpec(
            item["id"],
            tuple(item["labels"]),
            tuple(item["coefficients"]),
        )
        for item in state["families"]
    )
    if len(families) != 20 or any(len(item.labels) != radix for item in families):
        raise ValueError("v1 requires twenty four-valued semantic families")
    return manifest, state, probes, families


def _signature_digest(entity: EntitySignature) -> str:
    encoded = "|".join(entity.coordinates).encode()
    return hashlib.sha256(encoded).hexdigest()


def _leakage_audit(
    state_raw: dict,
    training: tuple[EntitySignature, ...],
    held_out: tuple[EntitySignature, ...],
    compiled_state,
) -> dict:
    training_signatures = {item.coordinates for item in training}
    test_signatures = {item.coordinates for item in held_out}
    overlap = training_signatures & test_signatures
    serialized_construction = json.dumps(state_raw, sort_keys=True)
    materialized_test_leaks = [
        item.id
        for item in held_out
        if item.id in serialized_construction
        or "|".join(item.coordinates) in serialized_construction
        or _signature_digest(item) in serialized_construction
    ]
    pair_record_count = int(np.count_nonzero(np.triu(compiled_state.pair_counts, 1)))
    return {
        "passed": not overlap and not materialized_test_leaks and compiled_state.stored_relation_arity == 2,
        "training_entity_count": len(training),
        "held_out_entity_count": len(held_out),
        "training_complete_signature_count": len(training_signatures),
        "held_out_complete_signature_count": len(test_signatures),
        "complete_signature_overlap_count": len(overlap),
        "materialized_test_signature_leaks": materialized_test_leaks,
        "stored_relation_arity": compiled_state.stored_relation_arity,
        "stored_pair_type_count": pair_record_count,
        "compiled_entity_identities_retained": False,
        "compiled_complete_signatures_retained": False,
        "interpretation": "Construction retains aggregate coordinate-pair counts only; held-out identities and complete signatures are evaluation-side data.",
    }


def _query_for_target(
    target: EntitySignature,
    family_order: tuple[str, ...],
    family_positions: dict[str, int],
    width: int,
) -> tuple[str, ...]:
    return tuple(target.coordinates[family_positions[item]] for item in family_order[:width])


def _score(
    treatment: str,
    state,
    query: tuple[str, ...],
    candidates: tuple[EntitySignature, ...],
) -> np.ndarray:
    if treatment == "flat_keyword_retrieval":
        return flat_keyword_scores(query, candidates)
    if treatment == "symbolic_conjunction":
        return symbolic_conjunction_scores(query, candidates)
    return SCORERS[treatment](state, query, candidates)


def _aggregate(records: list[dict], widths: tuple[int, ...], treatments: tuple[str, ...]) -> list[dict]:
    grouped = defaultdict(list)
    for record in records:
        grouped[(record["treatment"], record["k"])].append(record)
    result = []
    for treatment in treatments:
        for width in widths:
            items = grouped[(treatment, width)]
            result.append({
                "treatment": treatment,
                "k": width,
                "possible_query_combinations": 4 ** width,
                "possible_full_signatures": 4 ** 20,
                "query_count": len(items),
                "top_1_accuracy": statistics.fmean(item["top_candidate"] == item["target"] for item in items),
                "tie_adjusted_accuracy": statistics.fmean(item["tie_adjusted_credit"] for item in items),
                "mean_reciprocal_rank": statistics.fmean(item["reciprocal_rank"] for item in items),
                "mean_target_rank": statistics.fmean(item["target_rank"] for item in items),
                "mean_target_margin": statistics.fmean(item["target_margin"] for item in items),
                "mean_tie_count_at_target": statistics.fmean(item["tie_count_at_target"] for item in items),
            })
    return result


def _compact_target_traces(
    records: list[dict],
    held_out: tuple[EntitySignature, ...],
    family_order: tuple[str, ...],
    family_positions: dict[str, int],
    treatments: tuple[str, ...],
) -> list[dict]:
    indexed = {(item["target"], item["treatment"], item["k"]): item for item in records}
    traces = []
    for target in held_out:
        ordered = [target.coordinates[family_positions[family]] for family in family_order]
        outcomes = {}
        for treatment in treatments:
            items = [indexed[(target.id, treatment, width)] for width in range(1, len(family_order) + 1)]
            outcomes[treatment] = {
                "top_candidates": [item["top_candidate"] for item in items],
                "target_ranks": [item["target_rank"] for item in items],
                "target_tie_counts": [item["tie_count_at_target"] for item in items],
                "target_margins": [item["target_margin"] for item in items],
            }
        traces.append({
            "target": target.id,
            "ordered_query_coordinates": ordered,
            "outcomes": outcomes,
        })
    return traces


def _accuracy_threshold_width(aggregate: list[dict], treatment: str, threshold: float) -> int | None:
    candidates = [
        item["k"]
        for item in aggregate
        if item["treatment"] == treatment and item["top_1_accuracy"] >= threshold
    ]
    return min(candidates) if candidates else None


def _comparative_assessment(aggregate: list[dict], widths: tuple[int, ...]) -> dict:
    mml = {item["k"]: item["top_1_accuracy"] for item in aggregate if item["treatment"] == "mml_soft_intersection"}
    exact_controls = ("flat_keyword_retrieval", "vector_composition", "symbolic_conjunction")
    control = {
        width: max(
            item["top_1_accuracy"]
            for item in aggregate
            if item["k"] == width and item["treatment"] in exact_controls
        )
        for width in widths
    }
    advantages = {width: mml[width] - control[width] for width in widths}
    maximum = max(advantages.values())
    return {
        "demonstrated_capability": (
            "MML executed a 20-dimensional semantic representation generated from "
            "four latent variables while complete target signatures were absent "
            "from construction."
        ),
        "strong_exact_controls": list(exact_controls),
        "mml_top_1_advantage_by_k": {str(key): value for key, value in advantages.items()},
        "maximum_mml_top_1_advantage": maximum,
        "mml_has_distinctive_accuracy_advantage": maximum > 1e-12,
        "scaling_claim_status": "DIRECTIONAL_SIGNAL" if maximum > 1e-12 else "NOT_SUPPORTED_BY_THIS_FIXTURE",
        "interpretation": (
            "The positive result is execution over held-out complete signatures in "
            "a 20-dimensional projection of a four-latent-variable generator. "
            "A distinctive MML scaling claim would require additional value beyond "
            "exact overlap, explicit vectors, and symbolic conjunction."
        ),
    }


def run_experiment() -> dict:
    manifest, state_raw, probes, families = _load_contract()
    training, held_out = materialize_split(families, state_raw["latent_radix"])
    compiled = compile_pairwise_state(state_raw["state_id"], families, training)
    audit = _leakage_audit(state_raw, training, held_out, compiled)
    treatments = tuple(probes["treatments"])
    widths = tuple(probes["holdout_contract"]["query_widths"])
    family_order = tuple(probes["holdout_contract"]["family_order"])
    family_positions = {family.id: index for index, family in enumerate(families)}
    if set(family_order) != set(family_positions):
        raise ValueError("family order must contain every family exactly once")

    records = []
    for width in widths:
        for target in held_out:
            query = _query_for_target(target, family_order, family_positions, width)
            for treatment in treatments:
                ranking = rank_target(_score(treatment, compiled, query, held_out), held_out, target.id)
                records.append({
                    "treatment": treatment,
                    "k": width,
                    "target": target.id,
                    "query": list(query),
                    "top_candidate": ranking.top_candidate,
                    "target_rank": ranking.target_rank,
                    "tie_count_at_target": ranking.tie_count_at_target,
                    "target_margin": ranking.target_margin,
                    "reciprocal_rank": ranking.reciprocal_rank,
                    "tie_adjusted_credit": ranking.tie_adjusted_credit,
                })
    aggregate = _aggregate(records, widths, treatments)
    target_traces = _compact_target_traces(records, held_out, family_order, family_positions, treatments)
    comparative = _comparative_assessment(aggregate, widths)
    mml_final = next(item for item in aggregate if item["treatment"] == "mml_soft_intersection" and item["k"] == 20)
    criteria = {
        "construction_contains_only_pairwise_coordinate_records": compiled.stored_relation_arity == 2,
        "complete_test_signatures_are_absent_from_training": audit["complete_signature_overlap_count"] == 0,
        "test_signatures_are_absent_from_construction_artifact": not audit["materialized_test_signature_leaks"],
        "all_declared_widths_and_treatments_executed": len(records) == len(widths) * len(held_out) * len(treatments),
        "all_held_out_targets_are_unique": len({_signature_digest(item) for item in held_out}) == len(held_out),
        "mml_resolves_all_complete_held_out_signatures": mml_final["top_1_accuracy"] == 1.0,
    }
    return {
        "schema_version": "1.0",
        "experiment_id": manifest["experiment_id"],
        "title": manifest["title"],
        "hypothesis": "Pairwise-constructed governed semantic state can support identification of exact higher-order combinations absent from construction.",
        "reporting_methodology": "OSCARC-v1",
        "fixture": {
            "state_id": state_raw["state_id"],
            "lifecycle": state_raw["lifecycle"],
            "holdout_status": probes["holdout_status"],
            "semantic_family_count": len(families),
            "values_per_family": state_raw["latent_radix"],
            "training_entity_count": len(training),
            "held_out_entity_count": len(held_out),
            "query_widths": list(widths),
            "family_order": list(family_order),
        },
        "compiled_state": {
            "snapshot_id": compiled.snapshot_id,
            "coordinate_count": len(compiled.coordinates),
            "stored_relation_arity": compiled.stored_relation_arity,
            "training_entity_count": compiled.training_entity_count,
            "retained_training_entity_identities": False,
            "retained_complete_training_signatures": False,
        },
        "leakage_audit": audit,
        "treatments": list(treatments),
        "aggregate_by_k": aggregate,
        "target_trace_schema": {
            "array_alignment": "Every outcome array position i corresponds to query width k=i+1 and the prefix of ordered_query_coordinates through i.",
            "derived_metrics": "Reciprocal rank is 1/target_rank; tie-adjusted credit is 1/tie_count only when target_rank is 1, otherwise 0.",
        },
        "target_traces": target_traces,
        "scaling_summary": {
            "possible_full_signatures": 4 ** 20,
            "projected_dimension_count": len(families),
            "latent_variable_count": 4,
            "generator_realizable_complete_signatures": len(training) + len(held_out),
            "evaluated_held_out_complete_signatures": len(held_out),
            "mml_first_k_at_90_percent_top_1": _accuracy_threshold_width(aggregate, "mml_soft_intersection", 0.90),
            "mml_first_k_at_100_percent_top_1": _accuracy_threshold_width(aggregate, "mml_soft_intersection", 1.0),
            "treatment_first_k_at_90_percent_top_1": {
                treatment: _accuracy_threshold_width(aggregate, treatment, 0.90)
                for treatment in treatments
            },
        },
        "comparative_assessment": comparative,
        "conformity": {
            "criteria": criteria,
            "judgment": "EXECUTION_CONFORMANT" if all(criteria.values()) else "EXECUTION_NONCONFORMANT",
            "evidence_strength": "LOW",
        },
        "artifact_identities": {
            "manifest_sha256": sha256_file(MANIFEST_PATH),
            "state_sha256": sha256_file(ROOT / manifest["artifacts"]["state"]["path"]),
            "probes_sha256": sha256_file(ROOT / manifest["artifacts"]["probes"]["path"]),
            "kernel_sha256": sha256_file(KERNEL_PATH),
            "experiment_sha256": sha256_file(Path(__file__)),
            "study_sha256": sha256_file(STUDY_PATH),
        },
        "evidence_boundary": probes["evidence_boundary"],
        "claim_scope": "This tests structural holdout of complete signatures under a deterministic synthetic generator. It does not establish independently authored, natural-language, real-world, or production-scale generalization.",
    }


SPARKS = "▁▂▃▄▅▆▇█"


def _sparkline(values: list[float]) -> str:
    return "".join(SPARKS[min(7, max(0, round(value * 7)))] for value in values)


def markdown_report(result: dict) -> str:
    aggregate = result["aggregate_by_k"]
    treatments = result["treatments"]
    by_treatment = {
        treatment: [item for item in aggregate if item["treatment"] == treatment]
        for treatment in treatments
    }
    lines = [
        "# Experiment 3.4 — Compositional Generalization v1",
        "",
        "> **Can pairwise-constructed semantic state identify higher-order combinations that never occurred during construction?**",
        "",
        "## Executive interpretation",
        "",
        f"**Conformity judgment: `{result['conformity']['judgment']}`. Evidence strength: `{result['conformity']['evidence_strength']}`.**",
        "",
        f"**Demonstrated capability:** {result['comparative_assessment']['demonstrated_capability']}",
        "",
        f"Construction retained only coordinate-pair counts from {result['fixture']['training_entity_count']} synthetic training entities. The evaluation registry contained {result['fixture']['held_out_entity_count']} disjoint complete signatures, queried at every width from 1 through 20 across six treatments. The representation has `{result['scaling_summary']['projected_dimension_count']}` semantic dimensions, but they are generated from `{result['scaling_summary']['latent_variable_count']}` latent variables. The coordinate basis permits `{result['scaling_summary']['possible_full_signatures']:,}` theoretical signatures, while this generator realizes only `{result['scaling_summary']['generator_realizable_complete_signatures']}` of them.",
        "",
        f"**Scaling assessment: `{result['comparative_assessment']['scaling_claim_status']}`.** MML's maximum top-1 advantage over the strongest exact control was `{result['comparative_assessment']['maximum_mml_top_1_advantage']:.3f}`. The curve therefore demonstrates held-out execution in this projected representation, but it does not provide distinctive evidence for MML-specific scaling.",
        "",
        "## Accuracy curves",
        "",
        "Each sparkline runs from `k=1` to `k=20`; height represents deterministic top-1 accuracy.",
        "",
        "| Treatment | Accuracy curve | First k at ≥90% | Final accuracy |",
        "| --- | --- | ---: | ---: |",
    ]
    for treatment in treatments:
        values = [item["top_1_accuracy"] for item in by_treatment[treatment]]
        first = result["scaling_summary"]["treatment_first_k_at_90_percent_top_1"][treatment]
        lines.append(f"| `{treatment}` | `{_sparkline(values)}` | {first if first is not None else '—'} | {values[-1]:.3f} |")
    lines.extend([
        "",
        "### Accuracy against dimensions and possible query combinations",
        "",
        "| k | Possible queries (`4^k`) | " + " | ".join(f"`{item}`" for item in treatments) + " |",
        "| ---: | ---: | " + " | ".join("---:" for _ in treatments) + " |",
    ])
    for width in result["fixture"]["query_widths"]:
        row = [next(item for item in by_treatment[treatment] if item["k"] == width)["top_1_accuracy"] for treatment in treatments]
        lines.append(f"| {width} | {4 ** width:,} | " + " | ".join(f"{value:.3f}" for value in row) + " |")
    lines.extend([
        "",
        "## O — Objective observation",
        "",
        f"The leakage audit found `{result['leakage_audit']['complete_signature_overlap_count']}` complete-signature overlaps and `{len(result['leakage_audit']['materialized_test_signature_leaks'])}` materialized test-signature leaks. The compiled state contains `{result['compiled_state']['coordinate_count']}` coordinates and pairwise records only; it retains neither construction entity identities nor complete construction signatures.",
        "",
        "## S — Standard and controls",
        "",
        "The declared standard required disjoint complete signatures, pairwise-only construction, all six treatments at every `k`, unique held-out targets, and complete-signature resolution by MML. Flat keyword retrieval, a frozen SVD embedding centroid, direct pairwise vector composition, additive graph traversal, symbolic conjunction, and MML soft intersection execute over the same evaluation registry.",
        "",
        "## C — Context and chronology",
        "",
        "The split is structural and deterministic: four-value latent tuples whose digit sum is zero modulo four are held out; all others are projected into 20 semantic dimensions and contribute aggregate coordinate-pair counts. The state stores no entity identity or complete signature. Test signatures are materialized only by the evaluation adapter after construction.",
        "",
        "## A — Actions and mechanisms",
        "",
        "MML independently propagates each query coordinate through the pairwise training graph, combines the fields through a geometric-mean soft intersection, and scores each unseen candidate from its evaluation-side coordinate signature. The KG control adds propagated fields; vector composition uses cosine over explicit multi-hot coordinates; symbolic and lexical controls use explicit query-coordinate membership.",
        "",
        "## R — Result",
        "",
        f"MML first reached at least 90% deterministic top-1 accuracy at `k={result['scaling_summary']['mml_first_k_at_90_percent_top_1']}` and 100% at `k={result['scaling_summary']['mml_first_k_at_100_percent_top_1']}`. Flat overlap, explicit vector composition, symbolic conjunction, and additive KG traversal reached the same accuracy at the same width. At `k=20`, MML resolved all 64 held-out signatures in a 20-dimensional representation generated from four latent variables, but that shared success does not isolate an MML advantage.",
        "",
        "### Conformity criteria",
        "",
        "| Criterion | Result |",
        "| --- | --- |",
        *[f"| `{name}` | {'pass' if passed else 'fail'} |" for name, passed in result["conformity"]["criteria"].items()],
        "",
        "## C — Comparative assessment and research conclusion",
        "",
        "This is the first repository experiment in which complete target signatures are structurally absent from construction rather than merely absent as authored query strings. It verifies the stricter protocol and shows that MML can execute a 20-dimensional semantic representation generated from four latent variables without seeing complete target signatures. However, exact overlap and symbolic controls match MML's curve, so the observed accuracy is explained by fixture identifiability without requiring soft intersection.",
        "",
        "The result remains development evidence and does not support the distinctive scaling claim. The coordinate generator, split, mechanism, and evaluation were authored together; the four-latent-variable algebra realizes only 256 signatures; and evaluation supplies clean held-out candidate attributes. The next fixture must make exact controls insufficient while leaving genuinely inferable lower-order structure, then add irregularity, noise, missing coordinates, a much larger realized candidate universe, and a declared external embedding model.",
        "",
        "## Claims ladder",
        "",
        "| Level | Claim | Status |",
        "| --- | --- | --- |",
        "| implementation fact | construction retains pairwise coordinate counts only | verified |",
        "| fixture observation | exact held-out signatures are disjoint from construction signatures | verified |",
        "| bounded result | six treatments execute across `k=1..20` and 64 held-out targets | observed |",
        "| architectural signal | pairwise semantic state can execute a 20-dimensional projection against unseen complete signatures | bounded mechanism evidence |",
        "| distinctive MML signal | soft intersection outperforms exact or additive controls | not observed |",
        "| scaling hypothesis | accuracy remains useful as meaningful realized combinations explode | not supported by this 256-signature generator |",
        "| application claim | MML generalizes to unseen natural-language or factual entities | not established |",
        "",
        "## Evidence boundary",
        "",
        result["evidence_boundary"],
        "",
        result["claim_scope"],
        "",
        "This report follows the [OSCARC methodology](../../../benchmark/oscarc-methodology.md). The [machine-readable JSON artifact](../../../../benchmark/results/compositional-generalization-v1.json) remains authoritative for every query result, metric, leakage check, artifact identity, and conformity input.",
    ])
    return "\n".join(lines) + "\n"


def write_results(result: dict, result_path: Path = RESULT_PATH, report_path: Path = REPORT_PATH) -> None:
    write_artifact_pair(result_path, result, report_path, markdown_report(result))


def check_result(result: dict, result_path: Path = RESULT_PATH, report_path: Path = REPORT_PATH) -> None:
    comparison = compare_artifact_pair(result, markdown_report(result), result_path, report_path)
    if comparison.missing_paths:
        raise SystemExit("Experiment 3.4 reference artifacts are missing; run --write.")
    if not comparison.json_matches:
        raise SystemExit("Experiment 3.4 machine evidence differs from the reference artifact.")
    if not comparison.text_matches:
        raise SystemExit("Experiment 3.4 OSCARC report differs from the reference artifact.")


def main() -> None:
    run_research_command(ResearchCommand(
        description="Run Experiment 3.4 compositional generalization.",
        run=run_experiment,
        write=write_results,
        check=check_result,
        render=markdown_report,
    ))


if __name__ == "__main__":
    main()
