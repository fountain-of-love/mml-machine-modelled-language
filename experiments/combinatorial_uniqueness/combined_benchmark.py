"""Benchmark Combinatorial Uniqueness; this adapter does not define composition."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import platform
import statistics
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from .fixture import load_experiment_fixture
from src.combinatorial_uniqueness.combinatorial_uniqueness_flow import (
    INVALID, RESOLVED, UNRESOLVED, CombinatorialUniquenessFlow, ValidityPolicy,
)
from src.combinatorial_uniqueness.compose_concepts import ActivatedField, distribution_metrics


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "demonstration"
RESULT_PATH = ROOT / "benchmark" / "results" / "combinatorial-uniqueness-v1.json"
REPORT_PATH = ROOT / "docs" / "capabilities" / "combinatorial-uniqueness" / "results" / "v1.md"
PHYSICAL_MANIFEST = DATA / "combinatorial_uniqueness_v1.json"
LEGAL_MANIFEST = DATA / "combinatorial_uniqueness_legal_banking_v1.json"
POLICY = ValidityPolicy("composition-validity-development-v1", 0.0, 0.0, 0.0)
POLICY_RECORD = {
    "policy_id": POLICY.policy_id,
    "minimum_per_field_support": POLICY.minimum_per_field_support,
    "minimum_top_concentration": POLICY.minimum_top_concentration,
    "minimum_top_margin": POLICY.minimum_top_margin,
    "purpose": "zero-threshold diagnostic only; not a calibrated validity or confidence policy",
}
SENSITIVITY_POLICIES = (
    POLICY,
    ValidityPolicy("composition-posthoc-sensitivity-low-v1", 0.0, 0.25, 0.01),
    ValidityPolicy("composition-posthoc-sensitivity-high-v1", 0.0, 0.50, 0.05),
)


def _sha(path):
    return "sha256:" + hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _target(prefix, target, concepts):
    if prefix.candidate_values is None or target is None:
        return {"target_rank": None, "target_activation": None, "runner_up_activation": None, "target_margin": None}
    values = np.asarray(prefix.candidate_values)
    index = concepts.index(target)
    target_value = float(values[index])
    rivals = np.delete(values, index)
    runner = float(rivals.max()) if rivals.size else 0.0
    rank = int(1 + sum(value > target_value + 1e-15 for value in rivals))
    return {"target_rank": rank, "target_activation": target_value,
            "runner_up_activation": runner, "target_margin": target_value - runner}


def _execution(execution, state, probe_id, target=None, families=None):
    families = families or {}
    prefixes = []
    for width, prefix in enumerate(execution.prefixes, 1):
        values = np.asarray(prefix.candidate_values) if prefix.candidate_values is not None else None
        constraint_fields = [np.asarray(state.graph.single_field_activation(c)) for c in prefix.constraints]
        concept_indices = [state.graph.word2idx[c] for c in state.concepts]
        support = [float(field[concept_indices].sum()) for field in constraint_fields]
        tie_count = None if values is None else int(np.isclose(values, values.max(), rtol=0, atol=1e-12).sum())
        overlap = None
        if width > 1:
            left, right = state.incidence[prefix.constraints[-2]], state.incidence[prefix.constraints[-1]]
            overlap = len(left & right) / len(left | right) if left | right else None
        prefixes.append({
            "constraints": list(prefix.constraints),
            "constraint_count": len(prefix.constraints),
            "constraint_families": [families.get(c) for c in prefix.constraints],
            "family_transitions": sum(a != b for a, b in zip([families.get(c) for c in prefix.constraints], [families.get(c) for c in prefix.constraints][1:])),
            "incidence_overlap_with_previous": overlap,
            "cumulative_structural_information_bits": prefix.cumulative_structural_information_bits,
            "structural_information_role": "authored incidence control; not a kernel outcome",
            "entropy": prefix.entropy,
            "normalized_entropy": prefix.normalized_entropy,
            "effective_candidate_count": prefix.effective_candidate_count,
            "concentration": prefix.concentration,
            "top_k_mass": prefix.top_k_mass,
            "top_k": prefix.top_k,
            "top_margin": prefix.top_margin,
            "top_tie_count": tie_count,
            "minimum_per_field_support": min(support) if support else None,
            "operator_identity": "normalized-geometric-mean-soft-intersection-v1",
            "snapshot_id": state.snapshot_id,
            "policy_id": POLICY.policy_id,
            "hard_intersection_candidates": list(prefix.hard_intersection_candidates),
            "candidate_values": list(prefix.candidate_values) if prefix.candidate_values is not None else None,
            **_target(prefix, target, state.concepts),
        })
    return {
        "probe_id": probe_id, "target": target, "constraints": list(execution.constraints),
        "status": execution.status, "reason_code": execution.reason_code,
        "mechanism": {"status": execution.mechanism_status, "reason_code": execution.mechanism_reason_code},
        "governance": {"status": execution.governance_status, "reason_code": execution.governance_reason_code},
        "top_candidate": execution.top_candidate, "soft_top_candidate": execution.soft_top_candidate,
        "hard_intersection_candidates": list(execution.hard_intersection_candidates),
        "epistemic_position": execution.epistemic_position, "snapshot_id": execution.snapshot_id,
        "diagnostic_policy": dict(POLICY_RECORD), "prefixes": prefixes,
    }


def _additive_control(state, constraints, target):
    fields = [ActivatedField(c, tuple(state.graph.single_field_activation(c))) for c in constraints]
    indices = [state.graph.word2idx[c] for c in state.concepts]
    values = np.sum(np.asarray([f.values for f in fields]), axis=0)[indices]
    values = values / values.sum()
    metrics = distribution_metrics(values, top_k=min(3, len(values)))
    pseudo = type("P", (), {"candidate_values": tuple(values)})()
    return {"operator": "normalized-additive-control-v1", "diagnostic_policy": dict(POLICY_RECORD), "candidate_values": values.tolist(),
            "entropy": metrics.entropy, "normalized_entropy": metrics.normalized_entropy,
            "effective_candidate_count": metrics.effective_candidate_count,
            "concentration": metrics.concentration, **_target(pseudo, target, state.concepts)}


def _declared_probe_identities(probe_groups):
    """Return probe IDs and complete constraint tuples from every authored treatment."""
    probe_ids, combinations = set(), set()
    for records in probe_groups.values():
        for probe in records:
            probe_ids.add(probe["id"])
            if probe.get("constraints") and len(probe["constraints"]) > 1:
                combinations.add(tuple(probe["constraints"]))
            for stage in probe.get("stages", ()):
                if len(stage["constraints"]) > 1:
                    combinations.add(tuple(stage["constraints"]))
            shared = tuple(probe.get("shared_constraints", ()))
            for branch in probe.get("branches", ()):
                combination = shared + tuple(branch["additional_constraints"])
                if len(combination) > 1:
                    combinations.add(combination)
    return probe_ids, combinations


def audit_no_bespoke_primitives(state, probe_groups):
    """Audit that compilation contains only ordinary declared trait edges."""
    probe_ids, combinations = _declared_probe_identities(probe_groups)
    encoded = set(probe_ids)
    for combination in combinations:
        for separator in ("+", "|", ",", "::", "__"):
            encoded.add(separator.join(combination))
    vocabulary_violations = sorted(item for item in state.graph.vocab if item in encoded)
    relation_violations = []
    concept_set, dimension_set = set(state.concepts), set(state.dimensions)
    for relation in state.graph.relations:
        relation_id = relation["id"]
        valid_single_trait_edge = (
            relation["relation"] == "supports"
            and relation["source"] in dimension_set
            and relation["target"] in concept_set
            and relation_id == f"fixture:{relation['target']}:{relation['source']}"
        )
        encodes_probe = any(identity in relation_id for identity in encoded)
        if not valid_single_trait_edge or encodes_probe:
            relation_violations.append(relation_id)
    expected_relation_count = sum(len(concepts) for concepts in state.incidence.values())
    relation_id_count_matches = len(state.relation_ids) == len(state.graph.relations)
    violations = vocabulary_violations + relation_violations
    if len(state.graph.relations) != expected_relation_count:
        violations.append("RELATION_COUNT_MISMATCH")
    if not relation_id_count_matches:
        violations.append("RELATION_ID_COUNT_MISMATCH")
    return {"passed": not violations, "vocabulary_count": len(state.graph.vocab),
        "compiled_relation_count": len(state.graph.relations),
        "expected_single_trait_relation_count": expected_relation_count,
        "probe_identity_count": len(probe_ids), "complete_constraint_tuple_count": len(combinations),
        "vocabulary_violations": vocabulary_violations, "relation_violations": relation_violations,
        "relation_id_count_matches": relation_id_count_matches, "violations": violations}


def _run_context(name, fixture, flow):
    state = flow.govern_and_compile(fixture.state)
    families = {dimension.id: dimension.family for dimension in fixture.state.dimensions}
    groups = fixture.probes.probes
    independent, redundant, negative = [], [], []
    permutations, ablations = [], []
    for probe in groups.get("independent_composition_probes", ()):
        constraints, target = tuple(probe["constraints"]), probe["target"]
        full = flow.execute(state, constraints, POLICY)
        record = _execution(full, state, probe["id"], target, families)
        record["additive_control"] = _additive_control(state, constraints, target)
        record["hard_reference"] = {"operator": "incidence-intersection-v1",
                                    "role": "authored governance/control oracle; not soft-mechanism evidence",
                                    "diagnostic_policy": dict(POLICY_RECORD),
                                    "candidates": list(full.hard_intersection_candidates),
                                    "target_is_unique": full.hard_intersection_candidates == (target,)}
        independent.append(record)
        canonical_values = np.asarray(full.prefixes[-1].candidate_values)
        canonical_hash = hashlib.sha256(canonical_values.tobytes()).hexdigest()
        max_difference, statuses, tops, ranks = 0.0, set(), set(), set()
        for order in itertools.permutations(constraints):
            result = flow.execute(state, order, POLICY)
            final = result.prefixes[-1]
            values = np.asarray(final.candidate_values)
            max_difference = max(max_difference, float(np.max(np.abs(values - canonical_values))))
            statuses.add((result.status, result.reason_code)); tops.add(result.top_candidate)
            ranks.add(_target(final, target, state.concepts)["target_rank"])
        permutations.append({"probe_id": probe["id"], "count": math.factorial(len(constraints)),
            "canonical_field_sha256": "sha256:" + canonical_hash, "maximum_absolute_field_difference": max_difference,
            "all_fields_equal": max_difference <= 1e-12, "status_preserved": len(statuses) == 1,
            "target_rank_preserved": len(ranks) == 1, "top_candidate_preserved": len(tops) == 1,
            "all_outcomes_equal": len(statuses) == len(tops) == 1, "diagnostic_policy": dict(POLICY_RECORD)})
        full_final = record["prefixes"][-1]
        cases = []
        for omitted in constraints:
            reduced = tuple(c for c in constraints if c != omitted)
            item = _execution(flow.execute(state, reduced, POLICY), state, f"{probe['id']}:-{omitted}", target, families)
            final = item["prefixes"][-1]
            before = next(prefix for prefix in record["prefixes"] if omitted in prefix["constraints"])
            preceding = record["prefixes"][record["prefixes"].index(before) - 1]["cumulative_structural_information_bits"] if record["prefixes"].index(before) else 0.0
            cases.append({"omitted": omitted,
                "structural_information_contribution_bits": None if before["cumulative_structural_information_bits"] is None else before["cumulative_structural_information_bits"] - preceding,
                "ablated_raw": {key: final[key] for key in ("target_rank", "target_activation", "target_margin", "entropy", "normalized_entropy", "effective_candidate_count", "concentration", "top_tie_count")},
                "delta_target_margin": None if final["target_margin"] is None else full_final["target_margin"] - final["target_margin"],
                "delta_entropy": None if final["entropy"] is None else final["entropy"] - full_final["entropy"]})
        ablations.append({"probe_id": probe["id"], "full_raw": {key: full_final[key] for key in ("target_rank", "target_activation", "target_margin", "entropy", "normalized_entropy", "effective_candidate_count", "concentration", "top_tie_count")}, "leave_one_out": cases})
    for probe in groups.get("redundant_composition_probes", ()):
        redundant.append(_execution(flow.execute(state, probe["constraints"], POLICY), state, probe["id"], families=families))
    for group in ("unsupported_composition_probes", "invalid_composition_probes"):
        for probe in groups.get(group, ()):
            item = _execution(flow.execute(state, probe["constraints"], POLICY), state, probe["id"], families=families)
            item["negative_class"] = "unsupported" if group.startswith("unsupported") else "declared_invalid"
            expected_status = UNRESOLVED if group.startswith("unsupported") else INVALID
            expected_reason = "UNSUPPORTED_COMBINATION" if group.startswith("unsupported") else "DECLARED_CONTRADICTION"
            fixture_reason = "unsupported_combination" if group.startswith("unsupported") else "contradictory_constraints"
            item["declared_expectation"] = {"fixture_status": probe.get("expected_status"), "fixture_reason": probe.get("expected_reason"),
                "runtime_status": expected_status, "runtime_reason": expected_reason,
                "observed_governance_reason": item["governance"]["reason_code"],
                "matches": probe.get("expected_status") == "no_valid_intersection" and probe.get("expected_reason") == fixture_reason and item["status"] == expected_status and item["governance"]["reason_code"] == expected_reason}
            negative.append(item)
    cross_level = []
    for probe in groups.get("cross_level_probes", ()):
        stages = []
        declared_region = next((stage.get("expected_region") for stage in reversed(probe["stages"]) if stage.get("expected_region")), None)
        for index, stage in enumerate(probe["stages"], 1):
            stages.append(_execution(flow.execute(state, stage["constraints"], POLICY), state,
                                     f"{probe['id']}:stage-{index}", declared_region, families))
        cross_level.append({"probe_id": probe["id"], "description": probe["description"], "stages": stages})
    contrasts = []
    for probe in groups.get("contrast_probes", ()):
        branches = []
        for branch in probe["branches"]:
            constraints = tuple(probe["shared_constraints"]) + tuple(branch["additional_constraints"])
            branch_record = _execution(flow.execute(state, constraints, POLICY), state,
                                       f"{probe['id']}:{branch['id']}", branch["expected_region"], families)
            branches.append(branch_record)
        for branch, contrast_branch, authored_branch in zip(branches, reversed(branches), probe["branches"]):
            final = branch["prefixes"][-1]; values = final["candidate_values"]
            branch["intended_vs_contrast_margin"] = values[state.concepts.index(branch["target"])] - values[state.concepts.index(contrast_branch["target"])]
            effects = []
            for omitted in authored_branch["additional_constraints"]:
                reduced = tuple(c for c in branch["constraints"] if c != omitted)
                reduced_final = _execution(flow.execute(state, reduced, POLICY), state, "contrast-ablation", branch["target"], families)["prefixes"][-1]
                effects.append({"omitted": omitted,
                    "delta_target_margin": final["target_margin"] - reduced_final["target_margin"],
                    "delta_normalized_entropy": reduced_final["normalized_entropy"] - final["normalized_entropy"]})
            branch["differentiating_constraint_effects"] = effects
        contrasts.append({"probe_id": probe["id"], "shared_constraints": list(probe["shared_constraints"]), "branches": branches,
                          "branches_separate": len({b["top_candidate"] for b in branches}) == len(branches)})
    primitive_audit = audit_no_bespoke_primitives(state, groups)
    return {"context": name, "lifecycle": fixture.lifecycle, "holdout_status": fixture.probes.holdout_status,
            "state": {"id": fixture.state.state_id, "concept_count": len(state.concepts), "dimension_count": len(state.dimensions),
                      "relation_count": len(state.relation_ids), "snapshot_id": state.snapshot_id,
                      "bespoke_primitive_audit": primitive_audit},
            "evidence_boundary": fixture.state.evidence_boundary,
            "treatments": {"independent": independent, "redundant": redundant, "negative": negative,
                           "permutations": permutations, "ablations": ablations,
                           "cross_level": cross_level, "contrasts": contrasts}}


def _median(values):
    values = [v for v in values if v is not None]
    return statistics.median(values) if values else None


def _summaries(contexts):
    independent = [p for c in contexts for p in c["treatments"]["independent"]]
    redundant = [p for c in contexts for p in c["treatments"]["redundant"]]
    negative = [p for c in contexts for p in c["treatments"]["negative"]]
    points = [prefix for p in independent for prefix in p["prefixes"] if prefix["cumulative_structural_information_bits"] is not None]
    initial_ranks = [p["prefixes"][0]["target_rank"] for p in independent]
    final_ranks = [p["prefixes"][-1]["target_rank"] for p in independent]
    entropy_changes = [p["prefixes"][-1]["normalized_entropy"] - p["prefixes"][0]["normalized_entropy"] for p in independent]
    margin_changes = [p["prefixes"][-1]["target_margin"] - p["prefixes"][0]["target_margin"] for p in independent]
    redundant_entropy = [p["prefixes"][-1]["normalized_entropy"] - p["prefixes"][0]["normalized_entropy"] for p in redundant]
    def rate(items, predicate): return sum(predicate(x) for x in items) / len(items) if items else None
    information = np.asarray([p["cumulative_structural_information_bits"] for p in points], dtype=float)
    entropy = np.asarray([p["normalized_entropy"] for p in points], dtype=float)
    information_entropy_correlation = (
        float(np.corrcoef(information, entropy)[0, 1])
        if len(points) > 1 and np.std(information) > 0 and np.std(entropy) > 0 else None
    )
    context_associations = {}
    for context in contexts:
        local = [prefix for probe in context["treatments"]["independent"] for prefix in probe["prefixes"] if prefix["cumulative_structural_information_bits"] is not None]
        x = np.asarray([p["cumulative_structural_information_bits"] for p in local]); y = np.asarray([p["normalized_entropy"] for p in local])
        context_associations[context["context"]] = float(np.corrcoef(x, y)[0, 1]) if len(local) > 1 and np.std(x) and np.std(y) else None
    return {"headline": {"independent": {"count": len(independent), "median_initial_target_rank": _median(initial_ranks),
                    "median_final_target_rank": _median(final_ranks), "median_normalized_entropy_change": _median(entropy_changes),
                    "median_target_margin_change": _median(margin_changes), "overall_resolution_rate": rate(independent, lambda x: x["status"] == RESOLVED)},
                "redundant": {"count": len(redundant), "median_normalized_entropy_change": _median(redundant_entropy),
                              "overall_resolution_rate": rate(redundant, lambda x: x["status"] == RESOLVED)}},
            "specificity_curve": [{"structural_information_bits": p["cumulative_structural_information_bits"],
                                    "constraint_count": p["constraint_count"], "normalized_entropy": p["normalized_entropy"],
                                    "concentration": p["concentration"], "target_rank": p["target_rank"], "target_margin": p["target_margin"]} for p in points],
            "structural_information_to_normalized_entropy_correlation": information_entropy_correlation,
            "association_by_context": context_associations,
            "outcome_rates": {"mechanism_resolution": rate(independent, lambda x: x["mechanism"]["status"] == RESOLVED),
                "governance_resolution": rate(independent, lambda x: x["governance"]["status"] == RESOLVED),
                "overall_resolution": rate(independent, lambda x: x["status"] == RESOLVED),
                "unsupported_non_resolution": rate([x for x in negative if x["negative_class"] == "unsupported"], lambda x: x["status"] == UNRESOLVED),
                "declared_invalid_rejection": rate([x for x in negative if x["negative_class"] == "declared_invalid"], lambda x: x["status"] == INVALID)}}


def run_experiment():
    flow = CombinatorialUniquenessFlow()
    fixtures = [load_experiment_fixture(PHYSICAL_MANIFEST), load_experiment_fixture(LEGAL_MANIFEST)]
    contexts = [_run_context(name, fixture, flow) for name, fixture in zip(("physical_identification", "legal_qualification"), fixtures)]
    summaries = _summaries(contexts)
    sensitivity = []
    for policy in SENSITIVITY_POLICIES:
        mechanism, governance, overall = [], [], []
        for fixture in fixtures:
            state = flow.govern_and_compile(fixture.state)
            for probe in fixture.probes.probes.get("independent_composition_probes", ()):
                execution = flow.execute(state, probe["constraints"], policy)
                mechanism.append(execution.mechanism_status == RESOLVED)
                governance.append(execution.governance_status == RESOLVED)
                overall.append(execution.status == RESOLVED)
        sensitivity.append({"policy": {"policy_id": policy.policy_id,
            "minimum_per_field_support": policy.minimum_per_field_support,
            "minimum_top_concentration": policy.minimum_top_concentration,
            "minimum_top_margin": policy.minimum_top_margin,
            "classification": "diagnostic" if policy is POLICY else "post-hoc development sensitivity; not preregistered or confirmatory"},
            "mechanism_resolution_rate": statistics.mean(mechanism),
            "governance_resolution_rate": statistics.mean(governance),
            "overall_resolution_rate": statistics.mean(overall)})
    all_independent = [p for c in contexts for p in c["treatments"]["independent"]]
    all_permutations = [p for c in contexts for p in c["treatments"]["permutations"]]
    all_negative = [p for c in contexts for p in c["treatments"]["negative"]]
    redundant_change = summaries["headline"]["redundant"]["median_normalized_entropy_change"]
    independent_change = summaries["headline"]["independent"]["median_normalized_entropy_change"]
    criteria = {
        "compiled_states_contain_no_bespoke_probe_primitives": all(c["state"]["bespoke_primitive_audit"]["passed"] for c in contexts),
        "independent_information_is_associated_with_specificity": summaries["structural_information_to_normalized_entropy_correlation"] is not None and summaries["structural_information_to_normalized_entropy_correlation"] < 0,
        "independent_reduces_median_normalized_entropy": independent_change is not None and independent_change < 0,
        "independent_improves_median_target_margin": summaries["headline"]["independent"]["median_target_margin_change"] > 0,
        "independent_outperforms_unmatched_redundant_controls": independent_change is not None and redundant_change is not None and independent_change < redundant_change,
        "valid_compositions_resolve_declared_regions": all(p["status"] == RESOLVED and p["top_candidate"] == p["target"] for p in all_independent),
        "unsupported_legal_compositions_remain_unresolved": all(p["status"] == UNRESOLVED for p in all_negative if p["negative_class"] == "unsupported"),
        "declared_contradictions_are_invalid": all(p["status"] == INVALID for p in all_negative if p["negative_class"] == "declared_invalid"),
        "full_composition_is_order_invariant": all(p["count"] == 24 and p["all_fields_equal"] and p["all_outcomes_equal"] for p in all_permutations),
        "repeat_execution_is_deterministic": contexts == [_run_context(n, f, flow) for n, f in zip(("physical_identification", "legal_qualification"), fixtures)],
        "epistemic_positions_are_not_numerically_promoted": all(p["epistemic_position"] == "synthetic_doctrinal_construction" for p in contexts[1]["treatments"]["independent"]),
        "cross_level_trajectories_improve_toward_declarations": all(
            sequence["stages"][-1]["prefixes"][-1]["target_rank"] is not None and
            sequence["stages"][-1]["prefixes"][-1]["target_rank"] <= sequence["stages"][0]["prefixes"][-1]["target_rank"] and
            sequence["stages"][-1]["prefixes"][-1]["target_margin"] >= sequence["stages"][0]["prefixes"][-1]["target_margin"] and
            sequence["stages"][-1]["status"] == RESOLVED and sequence["stages"][-1]["reason_code"] == "RESOLVED_SEMANTIC_REGION"
            for sequence in contexts[1]["treatments"]["cross_level"]
        ),
        "contrast_branches_resolve_to_different_declared_regions": all(
            contrast["branches_separate"] and all(branch["status"] == RESOLVED and branch["reason_code"] == "RESOLVED_SEMANTIC_REGION" and branch["top_candidate"] == branch["target"] for branch in contrast["branches"])
            for contrast in contexts[1]["treatments"]["contrasts"]
        ),
        "negative_probe_declarations_match_runtime": all(p["declared_expectation"]["matches"] for p in all_negative),
    }
    judgment = "CONSISTENT" if all(criteria.values()) else "INCONSISTENT"
    return {"result_schema_version": "1.0", "benchmark_version": "combinatorial-uniqueness-v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "research_intention": "More independent information can narrow a semantic or legal interpretation, while insufficient information remains insufficient.",
        "reporting_methodology": "OSCARC-v1", "diagnostic_policy": dict(POLICY_RECORD),
        "contexts": contexts, "suite_results": summaries, "threshold_sensitivity": sensitivity,
        "conformity": {"judgment": judgment, "evidence_strength": "DEVELOPMENT", "criteria": criteria},
        "artifact_identities": {"physical_state_sha256": fixtures[0].state.source_sha256, "physical_probes_sha256": fixtures[0].probes.source_sha256,
            "legal_state_sha256": fixtures[1].state.source_sha256, "legal_probes_sha256": fixtures[1].probes.source_sha256,
            "physical_manifest_sha256": fixtures[0].manifest_sha256, "legal_manifest_sha256": fixtures[1].manifest_sha256,
            "compiled_snapshot_ids": [c["state"]["snapshot_id"] for c in contexts], "kernel_sha256": _sha(ROOT / "src" / "combinatorial_uniqueness" / "compose_concepts.py"),
            "operational_flow_sha256": _sha(ROOT / "src" / "combinatorial_uniqueness" / "combinatorial_uniqueness_flow.py"), "experiment_sha256": _sha(__file__),
            "fixture_loader_sha256": _sha(ROOT / "experiments" / "combinatorial_uniqueness" / "fixture.py"), "methodology_sha256": _sha(ROOT / "docs/benchmark/oscarc-methodology.md")},
        "provenance": {"python": platform.python_version(), "numpy": np.__version__, "kernel": "compose_concepts.py", "flow": "combinatorial_uniqueness_flow.py",
                       "experiment": "combinatorial_uniqueness_experiment.py", "fixtures": [str(PHYSICAL_MANIFEST.relative_to(ROOT)), str(LEGAL_MANIFEST.relative_to(ROOT))]},
        "evidence_boundary": "Two co-authored synthetic development fixtures; not held-out generalisation, natural-language understanding, factual legal adjudication, or production-scale performance."}


def markdown_report(result):
    head, rates = result["suite_results"]["headline"], result["suite_results"]["outcome_rates"]
    unsupported_count = sum(p["negative_class"] == "unsupported" for c in result["contexts"] for p in c["treatments"]["negative"])
    invalid_count = sum(p["negative_class"] == "declared_invalid" for c in result["contexts"] for p in c["treatments"]["negative"])
    cross_failures = [
        stage
        for context in result["contexts"]
        for sequence in context["treatments"]["cross_level"]
        for stage in sequence["stages"][-1:]
        if stage["target"] is not None and stage["top_candidate"] != stage["target"]
    ]
    primitive_audits = [context["state"]["bespoke_primitive_audit"] for context in result["contexts"]]
    lines = ["# Combinatorial Uniqueness Experiment v1 — OSCARC Report", "", "> **More information can narrow an interpretation, while insufficient information remains insufficient.**", "",
        "## Research intention", "", result["research_intention"], "", "## O — Objective observation", "",
        f"The same soft-intersection kernel executed two authored development contexts. The physical context tests identification; the legal context tests qualification. {len(result['suite_results']['specificity_curve'])} measured prefix points form the structural-information-to-activation-specificity curve. The observed association between authored structural information and normalized entropy was `{result['suite_results']['structural_information_to_normalized_entropy_correlation']:.6f}`; this is an association in co-authored development data, not a prediction claim.", "",
        "## S — Standard, baseline, or reference model", "", f"Policy `{result['diagnostic_policy']['policy_id']}` uses fixed thresholds recorded in the machine artifact. Additive activation and hard incidence intersection are controls; structural information is an authored incidence control, not a kernel outcome.", "",
        "## C — Context and chronology", "", "Both states and their probes are separately hashed but co-authored and `AUTHORED_DEVELOPMENT`; neither suite is held out. Legal resolution identifies only a synthetic semantic region and cannot promote its epistemic position or establish a real legal conclusion.", "",
        "## A — Actions, interventions, or observed mechanisms", "", "Every valid prefix, redundant probe, unsupported probe, declared invalid probe, additive control, hard reference, all 24 permutations of each four-coordinate valid probe, leave-one-out ablation, legal cross-level stage, and contrast branch was executed mechanically.", "",
        f"The compiled-state audit checked {sum(a['vocabulary_count'] for a in primitive_audits)} vocabulary entries and {sum(a['compiled_relation_count'] for a in primitive_audits)} relations against {sum(a['probe_identity_count'] for a in primitive_audits)} probe identities and {sum(a['complete_constraint_tuple_count'] for a in primitive_audits)} complete constraint tuples. It found {sum(len(a['violations']) for a in primitive_audits)} violations. Relations were required to be exact single-trait `dimension supports concept` edges with deterministic `fixture:concept:dimension` identities.", "",
        "## R — Result, effect, or measured outcome", "", "| Condition | Count | Median initial rank | Median final rank | Median normalized entropy change | Outcome rate |", "| --- | ---: | ---: | ---: | ---: | ---: |",
        f"| Independent | {head['independent']['count']} | {head['independent']['median_initial_target_rank']} | {head['independent']['median_final_target_rank']} | {head['independent']['median_normalized_entropy_change']:.6f} | {head['independent']['overall_resolution_rate']:.1%} |",
        f"| Redundant (unmatched control) | {head['redundant']['count']} | — | — | {head['redundant']['median_normalized_entropy_change']:.6f} | {head['redundant']['overall_resolution_rate']:.1%} |",
        f"| Unsupported legal | {unsupported_count} | — | — | — | {rates['unsupported_non_resolution']:.1%} non-resolution |",
        f"| Declared invalid | {invalid_count} | — | — | — | {rates['declared_invalid_rejection']:.1%} rejection |", "",
        "The independent and redundant fixtures do not declare probe-level matching, so their comparison is an unmatched development control, not a paired estimate. Family transitions and incidence-derived information are reported independently; crossing a family boundary is not assumed to prove independence.", "",
        "The median target rank is `1 → 1`, which is uninformative by itself because early fields contain ties. Tie count, target margin, normalized entropy, effective candidate count, and concentration are therefore foregrounded in the machine artifact.", "",
        "### Separated outcome rates", "", "| Layer | Rate |", "| --- | ---: |",
        f"| Mechanism resolution (valid probes) | {rates['mechanism_resolution']:.1%} |", f"| Governance resolution (valid probes) | {rates['governance_resolution']:.1%} |",
        f"| Overall resolution (valid probes) | {rates['overall_resolution']:.1%} |", f"| Unsupported legal non-resolution | {rates['unsupported_non_resolution']:.1%} |",
        f"| Declared-invalid rejection | {rates['declared_invalid_rejection']:.1%} |", "",
        "### Threshold sensitivity", "", "The zero-threshold policy is diagnostic only and must not be read as validated confidence. The nonzero grid is a fixed generic post-hoc development sensitivity analysis; it is neither preregistered nor confirmatory.", "", "| Policy | Classification | Mechanism | Governance | Overall |", "| --- | --- | ---: | ---: | ---: |",
        *[f"| `{item['policy']['policy_id']}` | {item['policy']['classification']} | {item['mechanism_resolution_rate']:.1%} | {item['governance_resolution_rate']:.1%} | {item['overall_resolution_rate']:.1%} |" for item in result["threshold_sensitivity"]], "",
        "## C — Comparative assessment and research conclusion", "", f"**Conformity judgment: `{result['conformity']['judgment']}`.** A negative scientific result is retained as valid evidence and does not make artifact verification fail.", "",
        *( [f"The cross-level access-to-evidence sequence remained `{cross_failures[0]['status']}` because its governed hard intersection was empty, even though `{cross_failures[0]['soft_top_candidate']}` led the numerical field. This is an informative failed expectation: the probe declared that region before execution, but cumulative intersection retained `access` as a required target property. The separate [root-cause analysis](../studies/cross-level-root-cause.md) examines the representation, query-operation, governance, and winner-support causes without relabelling the outcome.", ""] if cross_failures else [] ),
        "| Criterion | Result |", "| --- | --- |"]
    lines += [f"| `{key}` | {'pass' if value else 'fail'} |" for key, value in result["conformity"]["criteria"].items()]
    lines += ["", "## Evidence boundary", "", result["evidence_boundary"], "", "The [machine-readable JSON artifact](../../../../benchmark/results/combinatorial-uniqueness-v1.json) is authoritative for trajectories, candidate fields, controls, hashes, and provenance. This report follows the [OSCARC methodology](../../../benchmark/oscarc-methodology.md)."]
    return "\n".join(lines) + "\n"


def _comparable(result):
    copy = json.loads(json.dumps(result)); copy.pop("generated_at", None); return copy


def check_result(result, result_path=RESULT_PATH, report_path=REPORT_PATH):
    if not result["conformity"]["criteria"]["repeat_execution_is_deterministic"]:
        raise SystemExit("Experiment replay is nondeterministic.")
    if not all(p["count"] == 24 for c in result["contexts"] for p in c["treatments"]["permutations"]):
        raise SystemExit("Permutation control is incomplete.")
    if not result_path.exists():
        raise SystemExit("Reference artifact is missing; run --write first.")
    reference = json.loads(result_path.read_text())
    if _comparable(reference) != _comparable(result):
        raise SystemExit("Generated evidence differs from the reference artifact.")
    if not report_path.exists() or report_path.read_text(encoding="utf-8") != markdown_report(result):
        raise SystemExit("Generated OSCARC report differs from the reference artifact.")


def write_results(result, result_path=RESULT_PATH, report_path=REPORT_PATH):
    result_path.parent.mkdir(parents=True, exist_ok=True); report_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    report_path.write_text(markdown_report(result), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Run Combinatorial Uniqueness Experiment 3")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true"); mode.add_argument("--check", action="store_true")
    args = parser.parse_args(); result = run_experiment()
    if args.write: write_results(result)
    else: check_result(result)
    print(markdown_report(result))


if __name__ == "__main__": main()
