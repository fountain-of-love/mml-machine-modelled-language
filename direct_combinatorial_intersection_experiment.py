"""Experiment 3.1: benchmark direct intersection, not legal transition.

This adapter exercises the shared composition flow over the physical synthetic
fixture only. It does not define composition and does not load legal fixtures.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import platform
import statistics
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from combinatorial_uniqueness_fixture import load_experiment_fixture
from combinatorial_uniqueness_flow import (
    INVALID,
    RESOLVED,
    CombinatorialUniquenessFlow,
    ValidityPolicy,
)


ROOT = Path(__file__).parent
MANIFEST_PATH = ROOT / "data" / "demonstration" / "combinatorial_uniqueness_v1.json"
RESULT_PATH = ROOT / "benchmark" / "results" / "direct-combinatorial-intersection-v1.json"
REPORT_PATH = ROOT / "docs" / "benchmark" / "results" / "direct-combinatorial-intersection-v1.md"
METHODOLOGY_PATH = ROOT / "docs" / "benchmark" / "oscarc-methodology.md"
POLICY = ValidityPolicy("direct-intersection-development-v1", 0.0, 0.0, 0.0)
POLICY_RECORD = {
    "policy_id": POLICY.policy_id,
    "minimum_per_field_support": POLICY.minimum_per_field_support,
    "minimum_top_concentration": POLICY.minimum_top_concentration,
    "minimum_top_margin": POLICY.minimum_top_margin,
    "purpose": "zero-threshold development diagnostic; not calibrated confidence",
}


def _sha(path):
    return "sha256:" + hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _target_measurement(prefix, target, concepts):
    values = np.asarray(prefix.candidate_values)
    target_index = concepts.index(target)
    target_value = float(values[target_index])
    rivals = np.delete(values, target_index)
    runner_up = float(rivals.max()) if rivals.size else 0.0
    return {
        "target_rank": int(1 + sum(value > target_value + 1e-15 for value in rivals)),
        "target_activation": target_value,
        "runner_up_activation": runner_up,
        "target_margin": target_value - runner_up,
    }


def _serialize_execution(execution, state, probe_id, target=None, families=None):
    families = families or {}
    prefixes = []
    for prefix in execution.prefixes:
        values = np.asarray(prefix.candidate_values)
        tie_count = int(np.isclose(values, values.max(), rtol=0, atol=1e-12).sum())
        family_values = [families.get(constraint) for constraint in prefix.constraints]
        prefixes.append({
            "constraints": list(prefix.constraints),
            "constraint_count": len(prefix.constraints),
            "constraint_families": family_values,
            "family_transitions": sum(left != right for left, right in zip(family_values, family_values[1:])),
            "cumulative_structural_information_bits": prefix.cumulative_structural_information_bits,
            "structural_information_role": "authored incidence control; not a kernel outcome",
            "entropy": prefix.entropy,
            "normalized_entropy": prefix.normalized_entropy,
            "effective_candidate_count": prefix.effective_candidate_count,
            "concentration": prefix.concentration,
            "top_k": prefix.top_k,
            "top_k_mass": prefix.top_k_mass,
            "top_margin": prefix.top_margin,
            "top_tie_count": tie_count,
            "hard_intersection_candidates": list(prefix.hard_intersection_candidates),
            "candidate_values": list(prefix.candidate_values),
            **(_target_measurement(prefix, target, state.concepts) if target else {}),
        })
    return {
        "probe_id": probe_id,
        "target": target,
        "constraints": list(execution.constraints),
        "status": execution.status,
        "reason_code": execution.reason_code,
        "mechanism": {
            "status": execution.mechanism_status,
            "reason_code": execution.mechanism_reason_code,
        },
        "governance": {
            "status": execution.governance_status,
            "reason_code": execution.governance_reason_code,
        },
        "top_candidate": execution.top_candidate,
        "soft_top_candidate": execution.soft_top_candidate,
        "hard_intersection_candidates": list(execution.hard_intersection_candidates),
        "snapshot_id": execution.snapshot_id,
        "policy": dict(POLICY_RECORD),
        "prefixes": prefixes,
    }


def _primitive_audit(state, fixture):
    probes = tuple(fixture.probes.probes["independent_composition_probes"])
    probe_ids = {probe["id"] for probe in probes}
    combinations = {tuple(probe["constraints"]) for probe in probes}
    encoded = set(probe_ids)
    for constraints in combinations:
        for separator in ("+", "|", ",", "::", "__"):
            encoded.add(separator.join(constraints))
    vocabulary_violations = sorted(node for node in state.graph.vocab if node in encoded)
    relation_violations = []
    concepts, dimensions = set(state.concepts), set(state.dimensions)
    for relation in state.graph.relations:
        expected_id = f"fixture:{relation['target']}:{relation['source']}"
        valid = (
            relation["relation"] == "supports"
            and relation["source"] in dimensions
            and relation["target"] in concepts
            and relation["id"] == expected_id
            and not any(identity in relation["id"] for identity in encoded)
        )
        if not valid:
            relation_violations.append(relation["id"])
    expected_count = sum(len(members) for members in state.incidence.values())
    count_matches = len(state.graph.relations) == expected_count == len(state.relation_ids)
    return {
        "passed": not vocabulary_violations and not relation_violations and count_matches,
        "vocabulary_count": len(state.graph.vocab),
        "relation_count": len(state.graph.relations),
        "expected_single_trait_relation_count": expected_count,
        "probe_identity_count": len(probe_ids),
        "complete_constraint_tuple_count": len(combinations),
        "vocabulary_violations": vocabulary_violations,
        "relation_violations": relation_violations,
        "relation_count_matches": count_matches,
    }


def _run_fixture(fixture):
    flow = CombinatorialUniquenessFlow()
    state = flow.govern_and_compile(fixture.state)
    families = {dimension.id: dimension.family for dimension in fixture.state.dimensions}
    groups = fixture.probes.probes
    independent = []
    permutations = []
    ablations = []

    for probe in groups["independent_composition_probes"]:
        constraints = tuple(probe["constraints"])
        target = probe["target"]
        execution = flow.execute(state, constraints, POLICY)
        independent.append(_serialize_execution(execution, state, probe["id"], target, families))

        canonical = np.asarray(execution.prefixes[-1].candidate_values)
        maximum_difference = 0.0
        statuses, tops = set(), set()
        for order in itertools.permutations(constraints):
            permuted = flow.execute(state, order, POLICY)
            values = np.asarray(permuted.prefixes[-1].candidate_values)
            maximum_difference = max(maximum_difference, float(np.max(np.abs(values - canonical))))
            statuses.add((permuted.status, permuted.reason_code))
            tops.add(permuted.top_candidate)
        permutations.append({
            "probe_id": probe["id"],
            "count": 24,
            "canonical_field_sha256": "sha256:" + hashlib.sha256(canonical.tobytes()).hexdigest(),
            "maximum_absolute_field_difference": maximum_difference,
            "all_fields_equal": maximum_difference <= 1e-12,
            "status_preserved": len(statuses) == 1,
            "top_candidate_preserved": len(tops) == 1,
        })

        full = independent[-1]["prefixes"][-1]
        cases = []
        for omitted in constraints:
            reduced = tuple(constraint for constraint in constraints if constraint != omitted)
            reduced_record = _serialize_execution(
                flow.execute(state, reduced, POLICY), state, f"{probe['id']}:-{omitted}", target, families,
            )["prefixes"][-1]
            cases.append({
                "omitted": omitted,
                "target_margin": reduced_record["target_margin"],
                "normalized_entropy": reduced_record["normalized_entropy"],
                "delta_target_margin": full["target_margin"] - reduced_record["target_margin"],
                "delta_normalized_entropy": reduced_record["normalized_entropy"] - full["normalized_entropy"],
            })
        ablations.append({"probe_id": probe["id"], "leave_one_out": cases})

    redundant = [
        _serialize_execution(flow.execute(state, probe["constraints"], POLICY), state, probe["id"], families=families)
        for probe in groups["redundant_composition_probes"]
    ]
    invalid = [
        _serialize_execution(flow.execute(state, probe["constraints"], POLICY), state, probe["id"], families=families)
        for probe in groups["invalid_composition_probes"]
    ]
    return state, {
        "independent": independent,
        "redundant": redundant,
        "invalid": invalid,
        "permutations": permutations,
        "ablations": ablations,
        "bespoke_primitive_audit": _primitive_audit(state, fixture),
    }


def _median(values):
    values = [value for value in values if value is not None]
    return statistics.median(values) if values else None


def _summarize(treatments):
    independent = treatments["independent"]
    redundant = treatments["redundant"]
    independent_entropy_changes = [
        probe["prefixes"][-1]["normalized_entropy"] - probe["prefixes"][0]["normalized_entropy"]
        for probe in independent
    ]
    redundant_entropy_changes = [
        probe["prefixes"][-1]["normalized_entropy"] - probe["prefixes"][0]["normalized_entropy"]
        for probe in redundant
    ]
    margin_changes = [
        probe["prefixes"][-1]["target_margin"] - probe["prefixes"][0]["target_margin"]
        for probe in independent
    ]
    points = [
        (prefix["cumulative_structural_information_bits"], prefix["normalized_entropy"])
        for probe in independent
        for prefix in probe["prefixes"]
        if prefix["cumulative_structural_information_bits"] is not None
    ]
    correlation = float(np.corrcoef(*zip(*points))[0, 1])
    return {
        "independent_probe_count": len(independent),
        "redundant_control_count": len(redundant),
        "declared_invalid_count": len(treatments["invalid"]),
        "independent_final_resolution_rate": sum(probe["status"] == RESOLVED for probe in independent) / len(independent),
        "declared_invalid_rejection_rate": sum(probe["status"] == INVALID for probe in treatments["invalid"]) / len(treatments["invalid"]),
        "median_independent_normalized_entropy_change": _median(independent_entropy_changes),
        "median_redundant_normalized_entropy_change": _median(redundant_entropy_changes),
        "median_independent_target_margin_change": _median(margin_changes),
        "structural_information_to_normalized_entropy_association": correlation,
        "specificity_curve": [
            {"cumulative_structural_information_bits": information, "normalized_entropy": entropy}
            for information, entropy in points
        ],
    }


def run_experiment():
    fixture = load_experiment_fixture(MANIFEST_PATH)
    state, treatments = _run_fixture(fixture)
    summary = _summarize(treatments)
    criteria = {
        "independent_compositions_resolve_declared_targets": all(
            probe["status"] == RESOLVED and probe["top_candidate"] == probe["target"]
            for probe in treatments["independent"]
        ),
        "independent_composition_reduces_median_entropy": summary["median_independent_normalized_entropy_change"] < 0,
        "independent_composition_increases_median_margin": summary["median_independent_target_margin_change"] > 0,
        "independent_outperforms_unmatched_redundant_control": (
            summary["median_independent_normalized_entropy_change"]
            < summary["median_redundant_normalized_entropy_change"]
        ),
        "declared_invalid_compositions_are_rejected": summary["declared_invalid_rejection_rate"] == 1.0,
        "full_composition_is_order_invariant": all(item["all_fields_equal"] for item in treatments["permutations"]),
        "compiled_state_contains_no_bespoke_probe_primitive": treatments["bespoke_primitive_audit"]["passed"],
    }
    return {
        "result_schema_version": "1.0",
        "experiment_id": "experiment-3.1-direct-combinatorial-intersection-v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "title": "Experiment 3.1 — Direct Combinatorial Intersection",
        "research_question": "Do independent broad dimensions increase direct semantic specificity more strongly than redundant dimensions?",
        "reporting_methodology": "OSCARC-v1",
        "claim_scope": "Direct cumulative intersection only; no legal qualification, cross-level transition, or generalization claim.",
        "fixture": {
            "manifest": str(MANIFEST_PATH.relative_to(ROOT)),
            "lifecycle": fixture.lifecycle,
            "holdout_status": fixture.probes.holdout_status,
            "concept_count": len(state.concepts),
            "dimension_count": len(state.dimensions),
            "relation_count": len(state.relation_ids),
            "snapshot_id": state.snapshot_id,
        },
        "diagnostic_policy": dict(POLICY_RECORD),
        "treatments": treatments,
        "results": summary,
        "conformity": {
            "judgment": "LOCALLY_CONSISTENT" if all(criteria.values()) else "INCONSISTENT",
            "evidence_strength": "DEVELOPMENT",
            "criteria": criteria,
        },
        "generalization": {"status": "UNTESTED", "required_next": "Post-freeze independently authored probes."},
        "artifact_identities": {
            "state_sha256": fixture.state.source_sha256,
            "probes_sha256": fixture.probes.source_sha256,
            "manifest_sha256": fixture.manifest_sha256,
            "compiled_snapshot_id": state.snapshot_id,
            "kernel_sha256": _sha(ROOT / "compose_concepts.py"),
            "flow_sha256": _sha(ROOT / "combinatorial_uniqueness_flow.py"),
            "fixture_loader_sha256": _sha(ROOT / "combinatorial_uniqueness_fixture.py"),
            "experiment_sha256": _sha(__file__),
            "methodology_sha256": _sha(METHODOLOGY_PATH),
        },
        "provenance": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "kernel": "compose_concepts.py",
            "flow": "combinatorial_uniqueness_flow.py",
            "experiment": "direct_combinatorial_intersection_experiment.py",
        },
        "evidence_boundary": "One co-authored synthetic physical development fixture; not held out and not evidence of cross-domain generalization.",
    }


def markdown_report(result):
    summary = result["results"]
    criteria = result["conformity"]["criteria"]
    lines = [
        "# Experiment 3.1 — Direct Combinatorial Intersection v1",
        "",
        f"**Claim verdict: `{result['conformity']['judgment']}`. Evidence strength: `{result['conformity']['evidence_strength']}`.**",
        "",
        "## Research intention",
        "",
        result["research_question"],
        "",
        "This is an atomic test of direct cumulative intersection. It does not test legal qualification, cross-level semantic transition, or generalization.",
        "",
        "## O — Objective observation",
        "",
        f"The frozen development fixture contains {result['fixture']['concept_count']} concepts, {result['fixture']['dimension_count']} dimensions, and {result['fixture']['relation_count']} ordinary single-trait relations.",
        "",
        "## S — Standard, baseline, or reference model",
        "",
        "Independent four-coordinate probes are compared with unmatched redundant storage controls and declared-invalid combinations. Structural information is an authored incidence control, not a kernel outcome.",
        "",
        "## C — Context and chronology",
        "",
        f"The state and probes are `{result['fixture']['lifecycle']}` and `{result['fixture']['holdout_status']}`. They were co-authored and do not constitute held-out evidence.",
        "",
        "## A — Actions",
        "",
        f"Executed {summary['independent_probe_count']} independent probes, {summary['redundant_control_count']} redundant controls, {summary['declared_invalid_count']} invalid probes, all 24 permutations per valid probe, and every leave-one-coordinate-out ablation.",
        "",
        "## R — Results",
        "",
        "| Measure | Result |",
        "| --- | ---: |",
        f"| Independent final resolution | {summary['independent_final_resolution_rate']:.1%} |",
        f"| Invalid-combination rejection | {summary['declared_invalid_rejection_rate']:.1%} |",
        f"| Median independent entropy change | {summary['median_independent_normalized_entropy_change']:.6f} |",
        f"| Median redundant entropy change | {summary['median_redundant_normalized_entropy_change']:.6f} |",
        f"| Median independent target-margin change | {summary['median_independent_target_margin_change']:.6f} |",
        f"| Structural-information/entropy association | {summary['structural_information_to_normalized_entropy_association']:.6f} |",
        "",
        "The independent and redundant cases are unmatched authored development controls. Their comparison is directional, not a paired estimate.",
        "",
        "## C — Comparative assessment and research conclusion",
        "",
        f"The direct-intersection claim is `{result['conformity']['judgment']}` within this fixture. Generalization is `{result['generalization']['status']}`.",
        "",
        "| Criterion | Result |",
        "| --- | --- |",
        *[f"| `{name}` | {'pass' if passed else 'fail'} |" for name, passed in criteria.items()],
        "",
        "## Evidence boundary",
        "",
        result["evidence_boundary"],
        "",
        "The [machine-readable artifact](../../../benchmark/results/direct-combinatorial-intersection-v1.json) is authoritative for trajectories, controls, hashes, and provenance. This report follows the [OSCARC methodology](../oscarc-methodology.md).",
    ]
    return "\n".join(lines) + "\n"


def _comparable(result):
    comparable = json.loads(json.dumps(result))
    comparable.pop("generated_at", None)
    return comparable


def write_results(result, result_path=RESULT_PATH, report_path=REPORT_PATH):
    result_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    report_path.write_text(markdown_report(result), encoding="utf-8")


def check_result(result, result_path=RESULT_PATH, report_path=REPORT_PATH):
    if not result_path.exists() or not report_path.exists():
        raise SystemExit("Experiment 3.1 reference artifacts are missing; run --write.")
    reference = json.loads(result_path.read_text(encoding="utf-8"))
    if _comparable(reference) != _comparable(result):
        raise SystemExit("Experiment 3.1 machine evidence differs from the reference artifact.")
    if report_path.read_text(encoding="utf-8") != markdown_report(result):
        raise SystemExit("Experiment 3.1 OSCARC report differs from the reference artifact.")


def main():
    parser = argparse.ArgumentParser(description="Run Experiment 3.1 direct intersection.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = run_experiment()
    if args.write:
        write_results(result)
    else:
        check_result(result)
    print(markdown_report(result))


if __name__ == "__main__":
    main()
