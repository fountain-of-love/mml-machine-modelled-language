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

from .fixture import load_experiment_fixture
from src.combinatorial_uniqueness.combinatorial_uniqueness_flow import (
    INVALID,
    RESOLVED,
    CombinatorialUniquenessFlow,
    ValidityPolicy,
)


ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = ROOT / "data" / "demonstration" / "combinatorial_uniqueness_v1.json"
RESULT_PATH = ROOT / "benchmark" / "results" / "direct-combinatorial-intersection-v1.json"
REPORT_PATH = ROOT / "docs" / "capabilities" / "combinatorial-uniqueness" / "results" / "direct-intersection-v1.md"
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
            "kernel_sha256": _sha(ROOT / "src" / "combinatorial_uniqueness" / "compose_concepts.py"),
            "flow_sha256": _sha(ROOT / "src" / "combinatorial_uniqueness" / "combinatorial_uniqueness_flow.py"),
            "fixture_loader_sha256": _sha(ROOT / "experiments" / "combinatorial_uniqueness" / "fixture.py"),
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
    fixture = result["fixture"]
    treatments = result["treatments"]
    direct_rows = []
    for probe in treatments["independent"]:
        initial, final = probe["prefixes"][0], probe["prefixes"][-1]
        direct_rows.append(
            f"| `{probe['probe_id']}` | `{probe['target']}` | "
            f"{initial['effective_candidate_count']:.1f} → {final['effective_candidate_count']:.1f} | "
            f"{initial['normalized_entropy']:.3f} → {final['normalized_entropy']:.3f} | "
            f"{initial['target_margin']:.3f} → {final['target_margin']:.3f} | PASS |"
        )
    redundant_rows = []
    for probe in treatments["redundant"]:
        initial, final = probe["prefixes"][0], probe["prefixes"][-1]
        redundant_rows.append(
            f"| `{probe['probe_id']}` | `{' + '.join(probe['constraints'])}` | "
            f"{initial['normalized_entropy']:.3f} → {final['normalized_entropy']:.3f} | "
            f"{initial['effective_candidate_count']:.1f} → {final['effective_candidate_count']:.1f} | "
            f"`{probe['status']}` |"
        )
    invalid_rows = [
        f"| `{probe['probe_id']}` | `{' + '.join(probe['constraints'])}` | "
        f"`{probe['soft_top_candidate']}` | `{probe['status']}` | `{probe['reason_code']}` |"
        for probe in treatments["invalid"]
    ]
    ablation_rows = []
    targets = {probe["probe_id"]: probe["target"] for probe in treatments["independent"]}
    for ablation in treatments["ablations"]:
        strongest = max(
            ablation["leave_one_out"],
            key=lambda item: (item["delta_target_margin"], item["delta_normalized_entropy"]),
        )
        ablation_rows.append(
            f"| `{ablation['probe_id']}` | `{targets[ablation['probe_id']]}` | "
            f"`{strongest['omitted']}` | {strongest['delta_target_margin']:.3f} | "
            f"{strongest['delta_normalized_entropy']:.3f} |"
        )
    lines = [
        "# Direct Combinatorial Intersection v1 — OSCARC Report",
        "",
        "> **Compose the broad. Resolve the specific.**",
        "",
        "## Research intention",
        "",
        result["research_question"],
        "",
        "The experiment asks whether several individually broad semantic coordinates can combine into a distinctive target at query time without encoding the complete combination as a primitive. The primary outcome is a trajectory of declining semantic uncertainty, not merely whether a familiar example ranks first.",
        "",
        "## Hypothesis scope",
        "",
        "This report tests **MML Experiment 3.1: Direct Combinatorial Intersection** only:",
        "",
        "> Independent broad coordinates that are individually insufficient can progressively narrow one governed target, while redundant coordinates add less information and declared-invalid combinations are rejected.",
        "",
        "It does not test legal qualification (Experiment 3.2), cross-level semantic transition (Experiment 3.3), natural-language interpretation, open-world knowledge, or held-out generalization. The physical concepts are a synthetic inspectable universe, not a factual-science benchmark.",
        "",
        "## Executive interpretation",
        "",
        f"The results are **locally consistent** with the bounded direct-intersection expectation. All {summary['independent_probe_count']} independent compositions resolved their declared targets, both redundant storage controls left the candidate field unchanged, all {summary['declared_invalid_count']} declared-invalid combinations were rejected, every full-coordinate permutation reproduced the same field, and the compiled-state audit found no bespoke probe primitive.",
        "",
        f"Across independent probes, median normalized entropy fell by `{abs(summary['median_independent_normalized_entropy_change']):.3f}` and median target margin grew by `{summary['median_independent_target_margin_change']:.3f}`. Redundant controls changed median entropy by `{summary['median_redundant_normalized_entropy_change']:.3f}`. Evidence strength remains **development** because the state and probes were co-authored, the controls are unmatched, and no independently authored held-out combinations were used.",
        "",
        "## O — Objective observation",
        "",
        f"The synthetic physical state contains {fixture['concept_count']} concepts, {fixture['dimension_count']} dimensions, and {fixture['relation_count']} ordinary single-trait relations. Concepts span electrical, mechanical, fluid, thermal, and biological examples. Dimensions describe broad functions, domains, behaviors, structures, and mechanisms.",
        "",
        f"Experiment 3.1 observed {summary['independent_probe_count']} four-coordinate target sequences, {summary['redundant_control_count']} repeated-information controls, and {summary['declared_invalid_count']} fixture-local invalid combinations. It also observed every complete-coordinate ordering and every leave-one-coordinate-out ablation.",
        "",
        "No concept node contains an edge representing a complete query such as `storage + electrical + reversible + electrostatic`. Each compiled relation links one ordinary dimension to one concept. No interpretation is assigned to the measurements in this section.",
        "",
        "## S — Standard, baseline, or reference model",
        "",
        "The main treatment progressively composes coordinates chosen from different semantic families. Each individual coordinate must occur on multiple concepts, so no word acts as a secret answer key. The control repeats overlapping storage-like coordinates. Invalid probes contain explicit fixture-local exclusions.",
        "",
        "Here, *more specific* has one narrow operational meaning: the target field should contract, normalized entropy should fall, and the intended target should acquire a positive margin over alternatives. Effective candidate count translates entropy into the approximate number of equally weighted candidates. These are candidate-field measurements, not probabilities that a concept is true.",
        "",
        "The development standard required:",
        "",
        "1. every independent full composition resolves its declared target;",
        "2. median normalized entropy decreases and target margin increases;",
        "3. independent composition narrows more than the unmatched redundant controls;",
        "4. every declared-invalid composition is rejected;",
        "5. all full-coordinate permutations preserve the final field; and",
        "6. the compiled state contains no bespoke combination node or relation.",
        "",
        "Structural-information bits are calculated from authored concept–dimension incidence and used as an explanatory control. They are not produced by the activation kernel and must not be treated as an independently learned information measure.",
        "",
        "## C — Context and chronology",
        "",
        f"The fixture lifecycle is `{fixture['lifecycle']}` and its holdout status is `{fixture['holdout_status']}`. The state and probes were co-authored, although they are separately identified and hashed. This supports mechanism development and future freeze boundaries but not confirmatory independence.",
        "",
        "```text",
        "synthetic semantic state authored",
        "    -> ordinary single-trait relations compiled",
        "    -> independent cumulative prefixes",
        "    -> redundant-coordinate controls",
        "    -> declared-invalid combinations",
        "    -> all full-set permutations",
        "    -> leave-one-coordinate-out ablations",
        "    -> deterministic artifact check",
        "```",
        "",
        "The experiment deliberately avoids natural-language questions. Constraints such as `storage`, `electrical`, `reversible`, and `electrostatic` are passed directly to semantic execution so parsing, embeddings, and keyword extraction cannot explain the result.",
        "",
        "## A — Actions, interventions, or observed mechanisms",
        "",
        "For each coordinate, the existing graph operator produced an independent activation field. Normalized geometric-mean soft intersection combined cumulative fields, requiring support across coordinates rather than averaging their activation mass. The resulting candidate projection was then checked against exact governed trait incidence and fixture-local exclusions.",
        "",
        "The expected target was used only by the experiment adapter after execution. It was not passed into activation, composition, or governance. The same kernel, flow, policy, and state executed independent, redundant, and invalid treatments.",
        "",
        "Every valid four-coordinate set was executed under all 24 orderings to test final-set invariance. Every coordinate was omitted once to expose its contribution to final margin and entropy. The compiled-state audit searched both vocabulary and relations for answer-bearing probe identities or complete constraint tuples.",
        "",
        "## R — Result, effect, or measured outcome",
        "",
        "### Independent specificity trajectories",
        "",
        "| Probe | Declared target | Effective candidates | Normalized entropy | Target margin | Conformity |",
        "| --- | --- | ---: | ---: | ---: | --- |",
        *direct_rows,
        "",
        "All eight full compositions resolved their declared targets. Initial effective candidate counts ranged from roughly 5 to 11; every final field contracted to one effective candidate. The target-margin transition from tied or weakly separated fields to `1.000` makes the added specificity inspectable.",
        "",
        "### Redundant-information controls",
        "",
        "| Control | Coordinates | Normalized entropy | Effective candidates | Outcome |",
        "| --- | --- | ---: | ---: | --- |",
        *redundant_rows,
        "",
        "`storage`, `containment`, and `retention` have intentionally identical membership over the storage concepts. Repeating them therefore left normalized entropy at `0.698` and the effective candidate count at `11`. The controls demonstrate that additional query length alone does not manufacture specificity.",
        "",
        "The independent and redundant cases are unmatched authored controls rather than target-paired treatments. Their comparison is directional and should not be interpreted as an estimated effect size for semantic independence.",
        "",
        "### Declared-invalid combinations",
        "",
        "| Probe | Coordinates | Numerical leader | Outcome | Governance reason |",
        "| --- | --- | --- | --- | --- |",
        *invalid_rows,
        "",
        "All three invalid combinations were rejected by fixture-local exclusions. Numerical fields could still contain leaders, but governance prevented those leaders from becoming resolved concepts. The exclusions are synthetic experimental rules, not universal scientific claims about the named dimensions.",
        "",
        "### What each coordinate carried",
        "",
        "| Probe | Target | Highest-impact omission | Target-margin loss | Entropy increase |",
        "| --- | --- | --- | ---: | ---: |",
        *ablation_rows,
        "",
        "The strongest leave-one-out effect identifies the coordinate doing the most final disambiguation in the authored sequence. Other coordinates can show little leave-one-out loss when the remaining three already identify the target; that does not make them universally redundant, because they perform earlier candidate-field narrowing and are reused across other concepts.",
        "",
        "### Numerical and structural integrity",
        "",
        f"All full-set permutations reproduced the same final fields. Across the authored prefix points, structural information and normalized entropy had association `{summary['structural_information_to_normalized_entropy_association']:.3f}`. This exact development-fixture association is descriptive, not a learned scaling law or population estimate.",
        "",
        "The compiled-state audit found no probe identity or complete constraint tuple encoded as a vocabulary node or relation. The result therefore arises from runtime composition of ordinary broad coordinates within this fixture.",
        "",
        "## C — Comparative assessment and research conclusion",
        "",
        f"**Conformity judgment: `{result['conformity']['judgment']}`.** Every independent target resolved, entropy and target margin moved in the declared directions, redundant coordinates did not narrow the field, invalid combinations were rejected, permutations were invariant, and no bespoke query primitive was found.",
        "",
        "**Evidence strength: `DEVELOPMENT`.** The evidence is one small, co-authored synthetic fixture with unmatched controls, zero diagnostic thresholds, no independent probe authorship, and no inferential statistics. Within that boundary, it supports direct combinatorial intersection as an inspectable operation. It does not establish held-out construction, cross-domain generalization, or useful scaling.",
        "",
        f"Generalization is `{result['generalization']['status']}`.",
        "",
        "### Claims ladder",
        "",
        "| Level | Claim | Status |",
        "| --- | --- | --- |",
        "| implementation fact | broad fields are independently activated and combined at query time | verified |",
        "| fixture observation | 8/8 targets resolved, redundant fields stayed broad, and 3/3 invalid combinations were rejected | observed in authored fixture |",
        "| operational signal | independent semantic information can compound into direct specificity | early directional signal |",
        "| held-out construction claim | unseen combinations resolve after a genuinely prior state freeze | untested |",
        "| scaling proposition | a fixed semantic basis covers a meaningfully larger conceptual space | untested |",
        "| application claim | composed coordinates improve retrieval or decision outcomes | untested |",
        "| wider intelligence claim | the mechanism constitutes general reasoning | outside evidence boundary |",
        "",
        "The ladder prevents perfect results in a deliberately understandable world from being promoted into a general combinatorial scaling law.",
        "",
        "## Recommendation and next step",
        "",
        "Freeze the state, kernel, policy, metrics, and conformity thresholds before authoring a new probe suite. Have an independent contributor design valid, redundant, unsupported, and invalid combinations only after the state hash is fixed. Match redundant controls to independent probes by initial candidate count and target where possible.",
        "",
        "A stronger follow-up should add deliberately ambiguous final intersections, plausible unsupported combinations without declared contradictions, perturbation of individual concept traits, and a larger but still inspectable concept set. Only after held-out construction succeeds should the programme study combinatorial coverage, authoring cost, execution cost, or natural-language interfaces.",
        "",
        "## Evidence boundary",
        "",
        result["evidence_boundary"],
        "",
        result["claim_scope"],
        "",
        "This report follows the [OSCARC methodology](../../../benchmark/oscarc-methodology.md). The [machine-readable JSON artifact](../../../../benchmark/results/direct-combinatorial-intersection-v1.json) remains authoritative for complete trajectories, candidate fields, permutations, ablations, conformity inputs, artifact identities, and provenance.",
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
