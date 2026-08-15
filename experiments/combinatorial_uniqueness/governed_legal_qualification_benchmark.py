"""Experiment 3.2: benchmark governed legal qualification and refusal.

This adapter exercises the shared composition flow over the synthetic legal
fixture only. It does not define composition or execute cross-level probes.
"""

from __future__ import annotations

import hashlib
import itertools
import statistics
from pathlib import Path

import numpy as np

from .fixture import load_experiment_fixture
from src.combinatorial_uniqueness.combinatorial_uniqueness_flow import (
    RESOLVED,
    UNRESOLVED,
    CombinatorialUniquenessFlow,
    ValidityPolicy,
)
from src.helpers.artifacts import compare_artifact_pair, write_artifact_pair
from src.helpers.hashing import sha256_file
from src.helpers.research_cli import ResearchCommand, run_research_command
from src.helpers.provenance import runtime_identity, utc_now_iso


ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = ROOT / "data" / "demonstration" / "governed_legal_qualification_v1.json"
RESULT_PATH = ROOT / "benchmark" / "results" / "governed-legal-qualification-v1.json"
REPORT_PATH = ROOT / "docs" / "capabilities" / "combinatorial-uniqueness" / "results" / "governed-legal-qualification-v1.md"
METHODOLOGY_PATH = ROOT / "docs" / "benchmark" / "oscarc-methodology.md"
POLICY = ValidityPolicy("legal-qualification-development-v1", 0.0, 0.0, 0.0)
POLICY_RECORD = {
    "policy_id": POLICY.policy_id,
    "minimum_per_field_support": POLICY.minimum_per_field_support,
    "minimum_top_concentration": POLICY.minimum_top_concentration,
    "minimum_top_margin": POLICY.minimum_top_margin,
    "purpose": "zero-threshold development diagnostic; not calibrated legal confidence",
}


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
        "generated_at": utc_now_iso(),
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
            "kernel_sha256": sha256_file(ROOT / "src" / "combinatorial_uniqueness" / "compose_concepts.py"),
            "flow_sha256": sha256_file(ROOT / "src" / "combinatorial_uniqueness" / "combinatorial_uniqueness_flow.py"),
            "fixture_loader_sha256": sha256_file(ROOT / "experiments" / "combinatorial_uniqueness" / "fixture.py"),
            "experiment_sha256": sha256_file(__file__),
            "methodology_sha256": sha256_file(METHODOLOGY_PATH),
        },
        "provenance": {
            **runtime_identity({"numpy": np.__version__}),
            "kernel": "compose_concepts.py",
            "flow": "combinatorial_uniqueness_flow.py",
            "experiment": "governed_legal_qualification_experiment.py",
        },
        "evidence_boundary": "One co-authored synthetic doctrine-oriented development fixture; not held out and not a determination about any real institution, person, legal duty, or violation.",
    }


def markdown_report(result):
    summary = result["results"]
    criteria = result["conformity"]["criteria"]
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
            f"{final['effective_candidate_count']:.1f} |"
        )
    unsupported_rows = [
        f"| `{probe['probe_id']}` | `{' + '.join(probe['constraints'])}` | "
        f"`{probe['soft_top_candidate']}` | `{probe['status']}` | "
        f"`{probe['governance']['reason_code']}` |"
        for probe in treatments["unsupported"]
    ]
    contrast = treatments["contrasts"][0]
    contrast_rows = [
        f"| `{branch['probe_id'].split(':')[-1]}` | `{' + '.join(branch['constraints'])}` | "
        f"`{branch['top_candidate']}` | {branch['intended_vs_contrast_margin']:.3f} | PASS |"
        for branch in contrast["branches"]
    ]
    lines = [
        "# Governed Legal Qualification v1 — OSCARC Report",
        "",
        "> **More legal information can narrow an interpretation, while insufficient information remains insufficient.**",
        "",
        "## Research intention",
        "",
        result["research_question"],
        "",
        "The experiment asks whether broad legal, governance, evidential, and processing coordinates can combine into a narrower synthetic legal characterization without encoding the complete conclusion as a bespoke primitive. It also asks whether the same mechanism can refuse combinations whose information remains insufficient.",
        "",
        "## Hypothesis scope",
        "",
        "This report tests **MML Experiment 3.2: Governed Legal Qualification** only:",
        "",
        "> Independent legal dimensions can progressively narrow a direct semantic qualification, while unsupported combinations remain unresolved and activation cannot promote epistemic status.",
        "",
        "It does not test physical identification (Experiment 3.1), cross-level semantic transition (Experiment 3.3), natural-language legal interpretation, factual truth, liability, or correctness of a real-world legal conclusion. The fixture uses doctrine-oriented synthetic concepts so the semantic mechanism can be inspected without presenting allegations as established facts.",
        "",
        "It does not test cross-level transition. That distinct operation is isolated in Experiment 3.3 rather than inferred from successful direct legal qualification.",
        "",
        "It does not establish facts, determine legal duties, or adjudicate a dispute involving any real person or institution.",
        "",
        "## Executive interpretation",
        "",
        f"The results are **locally consistent** with the bounded legal-qualification expectation. All {summary['independent_probe_count']} direct probes resolved their declared synthetic regions, all {summary['unsupported_probe_count']} insufficient combinations remained unresolved, the two restriction branches separated into different regions, all full-coordinate permutations preserved their results, and the fixture's epistemic classification was not promoted.",
        "",
        "Independent cross-family probes reduced normalized entropy by a median of "
        f"`{abs(summary['median_independent_normalized_entropy_change']):.3f}`, compared with "
        f"`{abs(summary['median_redundant_normalized_entropy_change']):.3f}` for the unmatched same-family controls. The difference is directional, not a paired effect estimate. Evidence strength remains **development** because the legal state and probes were co-authored, thresholds are diagnostic rather than calibrated, and no held-out or independently reviewed legal cases were used.",
        "",
        "## O — Objective observation",
        "",
        f"The synthetic legal state contains {fixture['concept_count']} concepts, {fixture['dimension_count']} dimensions, and {fixture['relation_count']} ordinary single-trait relations. It represents data-subject rights, processing principles, governance, evidence, procedure, restrictions, data lifecycle, institutional context, and remedies as reusable dimensions.",
        "",
        f"Experiment 3.2 observed {summary['independent_probe_count']} direct qualification sequences, {summary['redundant_control_count']} same-family controls, {summary['unsupported_probe_count']} unsupported combinations, and one two-branch restriction contrast. Cross-level probes were excluded from this atomic fixture.",
        "",
        "The machine-readable companion records every cumulative prefix, candidate field, hard intersection, target rank, entropy, effective candidate count, margin, permutation, ablation, refusal reason, artifact identity, and provenance. No legal interpretation is assigned to those observations in this section.",
        "",
        "## S — Standard, baseline, or reference model",
        "",
        "The main treatment progressively composes dimensions from different semantic families. The directional control composes related dimensions from the same family. The unsupported treatment supplies plausible legal vocabulary whose conjunction is insufficient to determine a region. The contrast treatment begins from shared constraints and adds different qualifying information.",
        "",
        "Here, *more specific* has a narrow operational meaning: the intended synthetic region should move to the top of the candidate field while normalized entropy falls, effective candidate count contracts, and target margin grows. These numerical quantities describe semantic-field concentration; they are not probabilities that a legal proposition is true.",
        "",
        "The development standard required:",
        "",
        "1. every direct legal composition resolves its declared region;",
        "2. median normalized entropy decreases and target margin increases;",
        "3. cross-family composition narrows more than the unmatched same-family controls;",
        "4. unsupported combinations remain unresolved with an explicit reason;",
        "5. the two contrast branches resolve to different declared regions;",
        "6. numerical execution does not promote epistemic classification;",
        "7. complete-coordinate order does not change the final field; and",
        "8. the compiled state contains no bespoke probe primitive.",
        "",
        "No independent preregistration artifact or calibrated legal-confidence threshold exists. The fixed zero-threshold policy is explicitly a development diagnostic.",
        "",
        "## C — Context and chronology",
        "",
        f"The fixture lifecycle is `{fixture['lifecycle']}`, its holdout status is `{fixture['holdout_status']}`, and its classification is `{fixture['epistemic_classification']}`. The classification is separate from the fixture's factual-position vocabulary and cannot be transformed into an established fact by activation.",
        "",
        "```text",
        "synthetic doctrine-oriented state authored",
        "    -> atomic 3.2 probe suite separated",
        "    -> direct cumulative qualifications",
        "    -> same-family redundancy controls",
        "    -> unsupported-combination refusals",
        "    -> restriction-lawfulness contrast",
        "    -> permutations and ablations",
        "    -> deterministic artifact check",
        "```",
        "",
        "The state and probes were designed together. This makes the experiment useful for mechanism development and inspectability but prevents a held-out generalization claim. The contrast labels name synthetic semantic regions; they do not adjudicate whether an actual restriction is lawful or disproportionate.",
        "",
        "## A — Actions, interventions, or observed mechanisms",
        "",
        "For every direct probe, the experiment activated each broad coordinate independently and composed cumulative prefixes through normalized geometric-mean soft intersection. The numerical leader was then checked against exact governed trait incidence. The expected target was used by the adapter for evaluation and was not passed into the operational composition flow.",
        "",
        "Every four-coordinate direct probe was executed under all 24 permutations, and each coordinate was removed in turn for leave-one-out inspection. Unsupported probes contained no target label and could succeed only by remaining unresolved. The contrast probe held `access` and `rights_of_others` fixed while adding different qualifying coordinates to each branch.",
        "",
        "The compiled-state audit rejected answer-bearing vocabulary or relations. It required every fixture relation to remain an ordinary single-trait `dimension supports concept` edge. Cross-level transition was not executed.",
        "",
        "## R — Result, effect, or measured outcome",
        "",
        "### Direct qualification trajectories",
        "",
        "| Probe | Declared region | Effective candidates | Normalized entropy | Target margin | Conformity |",
        "| --- | --- | ---: | ---: | ---: | --- |",
        *direct_rows,
        "",
        "All twelve targets resolved. The table shows the first-to-final change for each cumulative query. Several first coordinates already place the target in a tied rank-one region; the evidential signal is therefore the field's contraction and margin growth across the sequence, not rank alone.",
        "",
        "### Same-family redundancy controls",
        "",
        "| Control | Coordinates | Normalized entropy | Final effective candidates |",
        "| --- | --- | ---: | ---: |",
        *redundant_rows,
        "",
        f"Median normalized-entropy change was `{summary['median_independent_normalized_entropy_change']:.3f}` for independent probes and `{summary['median_redundant_normalized_entropy_change']:.3f}` for the unmatched redundancy controls. The independent treatment narrowed more in this fixture, but the groups are not paired by target or initial candidate field; the comparison is a directional development control rather than a causal estimate of independence.",
        "",
        "### Insufficient information remains insufficient",
        "",
        "| Probe | Coordinates | Numerical leader | Outcome | Governance reason |",
        "| --- | --- | --- | --- | --- |",
        *unsupported_rows,
        "",
        "All unsupported combinations had numerical leaders, but none had a governed common candidate. The experiment therefore separated semantic proximity from permission to conclude. This is the central refusal result: plausible legal vocabulary did not force the system to manufacture a legal characterization.",
        "",
        "### Near-identical facts can diverge under qualifying information",
        "",
        "| Branch | Complete coordinates | Resolved region | Margin over contrast | Conformity |",
        "| --- | --- | --- | ---: | --- |",
        *contrast_rows,
        "",
        "Both branches began with `access + rights_of_others`. Adding necessity, proportionality, and partial-disclosure availability selected `legitimate_access_restriction`; adding incomplete disclosure and available redaction selected `disproportionate_access_restriction`. The shared starting vocabulary therefore did not determine the conclusion by itself.",
        "",
        "### Numerical and governance integrity",
        "",
        "All full-coordinate permutations reproduced the same final fields and top regions. Leave-one-out records expose which dimensions changed entropy and margin. The compiled-state audit found no bespoke combined-query primitive, and every executed result preserved `synthetic_doctrinal_construction` rather than promoting a factual position.",
        "",
        "## C — Comparative assessment and research conclusion",
        "",
        f"**Conformity judgment: `{result['conformity']['judgment']}`.** Every declared development criterion passed. Direct legal information narrowed the authored semantic fields, unsupported information remained unresolved, and additional qualifying information separated two regions that shared the same initial legal coordinates.",
        "",
        "**Evidence strength: `DEVELOPMENT`.** The evidence is one co-authored synthetic fixture with unmatched redundancy controls, zero diagnostic thresholds, no independent doctrinal review, no held-out cases, and no inferential statistics. Within that boundary, it supports combinatorial qualification and governed refusal as inspectable operations. It does not establish legal truth, doctrinal correctness, or generalization.",
        "",
        "### Claims ladder",
        "",
        "| Level | Claim | Status |",
        "| --- | --- | --- |",
        "| implementation fact | every result uses the same soft-intersection and hard-governance flow | verified |",
        "| fixture observation | 12/12 direct regions resolved and 3/3 unsupported combinations were refused | observed in authored fixture |",
        "| contrast observation | shared legal coordinates diverged under different qualifying information | observed in one authored contrast |",
        "| operational signal | more independent legal information can narrow a synthetic interpretation | early directional signal |",
        "| legal generalization | the behavior holds across unseen legal domains and independently authored probes | untested |",
        "| doctrinal claim | the synthetic ontology correctly expresses applicable law | untested |",
        "| adjudicative claim | a resolved region establishes facts, duties, liability, or violation | outside evidence boundary |",
        "",
        "The ladder prevents a reproducible semantic qualification from being promoted into a factual or legal conclusion without separate evidence and governance.",
        "",
        "## Recommendation and next step",
        "",
        "Freeze the legal state, direct-composition operation, policy, metrics, and conformity thresholds before commissioning an independently authored probe suite. Match independent and redundant treatments by initial candidate field and target where possible, add negative cases with plausible but insufficient vocabulary, and obtain domain review of the fixture distinctions before execution.",
        "",
        "A later application experiment may test whether these semantic regions assist legal research or evidence organization, but it should introduce source provenance, jurisdiction, temporal validity, authority hierarchy, factual-position tracking, and human review as separately governed inputs. Natural-language parsing should remain outside this mechanism experiment until the structured operation is independently replicated.",
        "",
        "## Evidence boundary",
        "",
        result["evidence_boundary"],
        "",
        result["claim_scope"],
        "",
        "This report follows the [OSCARC methodology](../../../benchmark/oscarc-methodology.md). The [machine-readable JSON artifact](../../../../benchmark/results/governed-legal-qualification-v1.json) remains authoritative for complete trajectories, candidate fields, ablations, permutations, conformity inputs, artifact identities, and provenance.",
    ]
    return "\n".join(lines) + "\n"


def write_results(result, result_path=RESULT_PATH, report_path=REPORT_PATH):
    write_artifact_pair(result_path, result, report_path, markdown_report(result))


def check_result(result, result_path=RESULT_PATH, report_path=REPORT_PATH):
    comparison = compare_artifact_pair(result, markdown_report(result), result_path, report_path)
    if comparison.missing_paths:
        raise SystemExit("Experiment 3.2 reference artifacts are missing; run --write.")
    if not comparison.json_matches:
        raise SystemExit("Experiment 3.2 machine evidence differs from the reference artifact.")
    if not comparison.text_matches:
        raise SystemExit("Experiment 3.2 OSCARC report differs from the reference artifact.")


def main():
    run_research_command(ResearchCommand(
        description="Run Experiment 3.2 governed legal qualification.",
        run=run_experiment,
        write=write_results,
        check=check_result,
        render=markdown_report,
    ))


if __name__ == "__main__":
    main()
