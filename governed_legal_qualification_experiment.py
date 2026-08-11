"""Experiment 3.2: benchmark governed legal qualification and refusal.

This adapter exercises the shared composition flow over the synthetic legal
fixture only. It does not define composition or execute cross-level probes.
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
    RESOLVED,
    UNRESOLVED,
    CombinatorialUniquenessFlow,
    ValidityPolicy,
)


ROOT = Path(__file__).parent
MANIFEST_PATH = ROOT / "data" / "demonstration" / "governed_legal_qualification_v1.json"
RESULT_PATH = ROOT / "benchmark" / "results" / "governed-legal-qualification-v1.json"
REPORT_PATH = ROOT / "docs" / "benchmark" / "results" / "governed-legal-qualification-v1.md"
METHODOLOGY_PATH = ROOT / "docs" / "benchmark" / "oscarc-methodology.md"
POLICY = ValidityPolicy("legal-qualification-development-v1", 0.0, 0.0, 0.0)
POLICY_RECORD = {
    "policy_id": POLICY.policy_id,
    "minimum_per_field_support": POLICY.minimum_per_field_support,
    "minimum_top_concentration": POLICY.minimum_top_concentration,
    "minimum_top_margin": POLICY.minimum_top_margin,
    "purpose": "zero-threshold development diagnostic; not calibrated legal confidence",
}


def _sha(path):
    return "sha256:" + hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _target(prefix, target, concepts):
    values = np.asarray(prefix.candidate_values)
    index = concepts.index(target)
    target_value = float(values[index])
    rivals = np.delete(values, index)
    runner_up = float(rivals.max()) if rivals.size else 0.0
    return {
        "target_rank": int(1 + sum(value > target_value + 1e-15 for value in rivals)),
        "target_activation": target_value,
        "runner_up_activation": runner_up,
        "target_margin": target_value - runner_up,
    }


def _serialize(execution, state, probe_id, target=None, families=None):
    families = families or {}
    prefixes = []
    for prefix in execution.prefixes:
        values = np.asarray(prefix.candidate_values)
        family_values = [families.get(constraint) for constraint in prefix.constraints]
        prefixes.append({
            "constraints": list(prefix.constraints),
            "constraint_count": len(prefix.constraints),
            "constraint_families": family_values,
            "family_transitions": sum(a != b for a, b in zip(family_values, family_values[1:])),
            "cumulative_structural_information_bits": prefix.cumulative_structural_information_bits,
            "structural_information_role": "authored incidence control; not a kernel outcome",
            "entropy": prefix.entropy,
            "normalized_entropy": prefix.normalized_entropy,
            "effective_candidate_count": prefix.effective_candidate_count,
            "concentration": prefix.concentration,
            "top_k": prefix.top_k,
            "top_k_mass": prefix.top_k_mass,
            "top_margin": prefix.top_margin,
            "top_tie_count": int(np.isclose(values, values.max(), rtol=0, atol=1e-12).sum()),
            "hard_intersection_candidates": list(prefix.hard_intersection_candidates),
            "candidate_values": list(prefix.candidate_values),
            **(_target(prefix, target, state.concepts) if target else {}),
        })
    return {
        "probe_id": probe_id,
        "target": target,
        "constraints": list(execution.constraints),
        "status": execution.status,
        "reason_code": execution.reason_code,
        "mechanism": {"status": execution.mechanism_status, "reason_code": execution.mechanism_reason_code},
        "governance": {"status": execution.governance_status, "reason_code": execution.governance_reason_code},
        "top_candidate": execution.top_candidate,
        "soft_top_candidate": execution.soft_top_candidate,
        "hard_intersection_candidates": list(execution.hard_intersection_candidates),
        "epistemic_classification": execution.epistemic_classification,
        "snapshot_id": execution.snapshot_id,
        "policy": dict(POLICY_RECORD),
        "prefixes": prefixes,
    }


def _audit_no_bespoke_primitives(state, groups):
    included_groups = (
        "independent_composition_probes",
        "redundant_composition_probes",
        "unsupported_composition_probes",
        "contrast_probes",
    )
    probe_ids = {probe["id"] for group in included_groups for probe in groups.get(group, ())}
    combinations = set()
    for group in included_groups:
        for probe in groups.get(group, ()):
            if len(probe.get("constraints", ())) > 1:
                combinations.add(tuple(probe["constraints"]))
            shared = tuple(probe.get("shared_constraints", ()))
            for branch in probe.get("branches", ()):
                combinations.add(shared + tuple(branch["additional_constraints"]))
    encoded = set(probe_ids)
    for constraints in combinations:
        for separator in ("+", "|", ",", "::", "__"):
            encoded.add(separator.join(constraints))
    vocabulary_violations = sorted(node for node in state.graph.vocab if node in encoded)
    concepts, dimensions = set(state.concepts), set(state.dimensions)
    relation_violations = []
    for relation in state.graph.relations:
        valid = (
            relation["relation"] == "supports"
            and relation["source"] in dimensions
            and relation["target"] in concepts
            and relation["id"] == f"fixture:{relation['target']}:{relation['source']}"
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
    groups = fixture.probes.probes
    families = {dimension.id: dimension.family for dimension in fixture.state.dimensions}
    independent, permutations, ablations = [], [], []

    for probe in groups["independent_composition_probes"]:
        constraints, target = tuple(probe["constraints"]), probe["target"]
        execution = flow.execute(state, constraints, POLICY)
        independent.append(_serialize(execution, state, probe["id"], target, families))
        canonical = np.asarray(execution.prefixes[-1].candidate_values)
        maximum_difference, statuses, tops = 0.0, set(), set()
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
            reduced_final = _serialize(
                flow.execute(state, reduced, POLICY), state, f"{probe['id']}:-{omitted}", target, families,
            )["prefixes"][-1]
            cases.append({
                "omitted": omitted,
                "target_margin": reduced_final["target_margin"],
                "normalized_entropy": reduced_final["normalized_entropy"],
                "delta_target_margin": full["target_margin"] - reduced_final["target_margin"],
                "delta_normalized_entropy": reduced_final["normalized_entropy"] - full["normalized_entropy"],
            })
        ablations.append({"probe_id": probe["id"], "leave_one_out": cases})

    redundant = [
        _serialize(flow.execute(state, probe["constraints"], POLICY), state, probe["id"], families=families)
        for probe in groups["redundant_composition_probes"]
    ]
    unsupported = []
    for probe in groups["unsupported_composition_probes"]:
        record = _serialize(flow.execute(state, probe["constraints"], POLICY), state, probe["id"], families=families)
        record["declared_expectation"] = {
            "status": probe["expected_status"],
            "reason": probe["expected_reason"],
            "matches": (
                record["status"] == UNRESOLVED
                and record["governance"]["reason_code"] == "UNSUPPORTED_COMBINATION"
                and probe["expected_status"] == "no_valid_intersection"
                and probe["expected_reason"] == "unsupported_combination"
            ),
        }
        unsupported.append(record)

    contrasts = []
    for probe in groups["contrast_probes"]:
        branches = []
        for branch in probe["branches"]:
            constraints = tuple(probe["shared_constraints"]) + tuple(branch["additional_constraints"])
            branches.append(_serialize(
                flow.execute(state, constraints, POLICY), state,
                f"{probe['id']}:{branch['id']}", branch["expected_region"], families,
            ))
        for branch, contrast, authored in zip(branches, reversed(branches), probe["branches"]):
            final = branch["prefixes"][-1]
            values = final["candidate_values"]
            branch["intended_vs_contrast_margin"] = (
                values[state.concepts.index(branch["target"])]
                - values[state.concepts.index(contrast["target"])]
            )
            effects = []
            for omitted in authored["additional_constraints"]:
                reduced = tuple(constraint for constraint in branch["constraints"] if constraint != omitted)
                reduced_final = _serialize(
                    flow.execute(state, reduced, POLICY), state, "contrast-ablation", branch["target"], families,
                )["prefixes"][-1]
                effects.append({
                    "omitted": omitted,
                    "delta_target_margin": final["target_margin"] - reduced_final["target_margin"],
                    "delta_normalized_entropy": reduced_final["normalized_entropy"] - final["normalized_entropy"],
                })
            branch["differentiating_constraint_effects"] = effects
        contrasts.append({
            "probe_id": probe["id"],
            "shared_constraints": list(probe["shared_constraints"]),
            "branches": branches,
            "branches_separate": len({branch["top_candidate"] for branch in branches}) == len(branches),
        })
    return state, {
        "independent": independent,
        "redundant": redundant,
        "unsupported": unsupported,
        "contrasts": contrasts,
        "permutations": permutations,
        "ablations": ablations,
        "bespoke_primitive_audit": _audit_no_bespoke_primitives(state, groups),
    }


def _median(values):
    values = [value for value in values if value is not None]
    return statistics.median(values) if values else None


def _summarize(treatments):
    independent_changes = [
        probe["prefixes"][-1]["normalized_entropy"] - probe["prefixes"][0]["normalized_entropy"]
        for probe in treatments["independent"]
    ]
    redundant_changes = [
        probe["prefixes"][-1]["normalized_entropy"] - probe["prefixes"][0]["normalized_entropy"]
        for probe in treatments["redundant"]
    ]
    margin_changes = [
        probe["prefixes"][-1]["target_margin"] - probe["prefixes"][0]["target_margin"]
        for probe in treatments["independent"]
    ]
    return {
        "independent_probe_count": len(treatments["independent"]),
        "redundant_control_count": len(treatments["redundant"]),
        "unsupported_probe_count": len(treatments["unsupported"]),
        "contrast_probe_count": len(treatments["contrasts"]),
        "independent_final_resolution_rate": sum(p["status"] == RESOLVED for p in treatments["independent"]) / len(treatments["independent"]),
        "unsupported_non_resolution_rate": sum(p["status"] == UNRESOLVED for p in treatments["unsupported"]) / len(treatments["unsupported"]),
        "median_independent_normalized_entropy_change": _median(independent_changes),
        "median_redundant_normalized_entropy_change": _median(redundant_changes),
        "median_independent_target_margin_change": _median(margin_changes),
    }


def run_experiment():
    fixture = load_experiment_fixture(MANIFEST_PATH)
    state, treatments = _run_fixture(fixture)
    summary = _summarize(treatments)
    criteria = {
        "direct_legal_compositions_resolve_declared_regions": all(
            probe["status"] == RESOLVED and probe["top_candidate"] == probe["target"]
            for probe in treatments["independent"]
        ),
        "independent_legal_dimensions_reduce_median_entropy": summary["median_independent_normalized_entropy_change"] < 0,
        "independent_legal_dimensions_increase_median_margin": summary["median_independent_target_margin_change"] > 0,
        "independent_outperforms_unmatched_same_family_controls": (
            summary["median_independent_normalized_entropy_change"]
            < summary["median_redundant_normalized_entropy_change"]
        ),
        "unsupported_legal_combinations_remain_unresolved": all(
            probe["declared_expectation"]["matches"] for probe in treatments["unsupported"]
        ),
        "contrast_branches_resolve_to_distinct_declared_regions": all(
            contrast["branches_separate"]
            and all(branch["status"] == RESOLVED and branch["top_candidate"] == branch["target"] for branch in contrast["branches"])
            for contrast in treatments["contrasts"]
        ),
        "epistemic_classification_is_not_promoted": all(
            probe["epistemic_classification"] == fixture.state.epistemic_classification
            for group in ("independent", "redundant", "unsupported")
            for probe in treatments[group]
        ),
        "full_composition_is_order_invariant": all(item["all_fields_equal"] for item in treatments["permutations"]),
        "compiled_state_contains_no_bespoke_probe_primitive": treatments["bespoke_primitive_audit"]["passed"],
    }
    return {
        "result_schema_version": "1.0",
        "experiment_id": "experiment-3.2-governed-legal-qualification-v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "title": "Experiment 3.2 — Governed Legal Qualification",
        "research_question": "Can independent legal dimensions narrow a semantic interpretation while unsupported combinations remain insufficient?",
        "reporting_methodology": "OSCARC-v1",
        "claim_scope": "Direct legal qualification, contrast, and governed refusal only; no physical identification, cross-level transition, factual adjudication, or generalization claim.",
        "fixture": {
            "manifest": str(MANIFEST_PATH.relative_to(ROOT)),
            "lifecycle": fixture.lifecycle,
            "holdout_status": fixture.probes.holdout_status,
            "concept_count": len(state.concepts),
            "dimension_count": len(state.dimensions),
            "relation_count": len(state.relation_ids),
            "snapshot_id": state.snapshot_id,
            "epistemic_classification": fixture.state.epistemic_classification,
            "epistemic_positions": list(fixture.state.epistemic_positions),
        },
        "diagnostic_policy": dict(POLICY_RECORD),
        "treatments": treatments,
        "results": summary,
        "conformity": {
            "judgment": "LOCALLY_CONSISTENT" if all(criteria.values()) else "INCONSISTENT",
            "evidence_strength": "DEVELOPMENT",
            "criteria": criteria,
        },
        "generalization": {"status": "UNTESTED", "required_next": "Post-freeze independently authored legal probes."},
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
            "experiment": "governed_legal_qualification_experiment.py",
        },
        "evidence_boundary": "One co-authored synthetic doctrine-oriented development fixture; not held out and not a determination about any real institution, person, legal duty, or violation.",
    }


def markdown_report(result):
    summary, criteria = result["results"], result["conformity"]["criteria"]
    lines = [
        "# Experiment 3.2 — Governed Legal Qualification v1",
        "",
        f"**Claim verdict: `{result['conformity']['judgment']}`. Evidence strength: `{result['conformity']['evidence_strength']}`.**",
        "",
        "> **More legal information can narrow an interpretation, while insufficient information remains insufficient.**",
        "",
        "## Research intention", "", result["research_question"], "",
        "This atomic experiment tests direct legal qualification, contrast, refusal, and epistemic non-promotion. It does not test cross-level transition. It does not establish facts or adjudicate a real legal dispute.", "",
        "## O — Objective observation", "",
        f"The synthetic legal fixture contains {result['fixture']['concept_count']} concepts, {result['fixture']['dimension_count']} dimensions, and {result['fixture']['relation_count']} ordinary single-trait relations.", "",
        "## S — Standard, baseline, or reference model", "",
        "Independent cross-family legal dimensions are compared with unmatched same-family controls. Unsupported combinations must remain unresolved. Contrast branches must resolve to different declared regions. Hard incidence remains an authored governance/control oracle, not soft-mechanism evidence.", "",
        "## C — Context and chronology", "",
        f"The state and probes are `{result['fixture']['lifecycle']}` and `{result['fixture']['holdout_status']}`. The fixture classification is `{result['fixture']['epistemic_classification']}` and cannot be promoted into a factual legal conclusion by numerical activation.", "",
        "## A — Actions", "",
        f"Executed {summary['independent_probe_count']} direct qualification probes, {summary['redundant_control_count']} redundant controls, {summary['unsupported_probe_count']} unsupported probes, {summary['contrast_probe_count']} contrast probe, all valid-probe permutations, and leave-one-out ablations. Cross-level probes were not executed.", "",
        "## R — Results", "",
        "| Measure | Result |", "| --- | ---: |",
        f"| Direct legal resolution | {summary['independent_final_resolution_rate']:.1%} |",
        f"| Unsupported non-resolution | {summary['unsupported_non_resolution_rate']:.1%} |",
        f"| Median independent entropy change | {summary['median_independent_normalized_entropy_change']:.6f} |",
        f"| Median redundant entropy change | {summary['median_redundant_normalized_entropy_change']:.6f} |",
        f"| Median target-margin change | {summary['median_independent_target_margin_change']:.6f} |", "",
        "The independent and redundant probes are unmatched authored development controls; the comparison is directional rather than paired.", "",
        "## C — Comparative assessment and research conclusion", "",
        f"The governed legal-qualification claim is `{result['conformity']['judgment']}` within this fixture. Generalization is `{result['generalization']['status']}`.", "",
        "| Criterion | Result |", "| --- | --- |",
        *[f"| `{name}` | {'pass' if passed else 'fail'} |" for name, passed in criteria.items()], "",
        "## Evidence boundary", "", result["evidence_boundary"], "",
        "The [machine-readable artifact](../../../benchmark/results/governed-legal-qualification-v1.json) is authoritative for trajectories, controls, hashes, and provenance. This report follows the [OSCARC methodology](../oscarc-methodology.md).",
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
        raise SystemExit("Experiment 3.2 reference artifacts are missing; run --write.")
    reference = json.loads(result_path.read_text(encoding="utf-8"))
    if _comparable(reference) != _comparable(result):
        raise SystemExit("Experiment 3.2 machine evidence differs from the reference artifact.")
    if report_path.read_text(encoding="utf-8") != markdown_report(result):
        raise SystemExit("Experiment 3.2 OSCARC report differs from the reference artifact.")


def main():
    parser = argparse.ArgumentParser(description="Run Experiment 3.2 governed legal qualification.")
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
