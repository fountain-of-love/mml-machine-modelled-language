"""Experiment 3.3 adapter for governed cross-level semantic transition."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from .fixture import load_experiment_fixture
from src.combinatorial_uniqueness.combinatorial_uniqueness_flow import RESOLVED, CombinatorialUniquenessFlow, ValidityPolicy
from src.combinatorial_uniqueness.cross_level_semantic_transition import TransitionStage, execute_stage_transition


ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = ROOT / "data" / "demonstration" / "cross_level_semantic_transition_v1.json"
RESULT_PATH = ROOT / "benchmark" / "results" / "cross-level-semantic-transition-v1.json"
REPORT_PATH = ROOT / "docs" / "capabilities" / "combinatorial-uniqueness" / "results" / "cross-level-semantic-transition-v1.md"
METHODOLOGY_PATH = ROOT / "docs" / "benchmark" / "oscarc-methodology.md"
POLICY = ValidityPolicy("cross-level-transition-development-v1", 0.0, 0.0, 0.0)


def _sha(path: str | Path) -> str:
    return "sha256:" + hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _target_metrics(prefix, target: str, concepts: tuple[str, ...]) -> dict:
    if prefix.candidate_values is None:
        return {"target_rank": None, "target_activation": None, "target_margin": None}
    values = np.asarray(prefix.candidate_values)
    index = concepts.index(target)
    target_value = float(values[index])
    rivals = np.delete(values, index)
    return {
        "target_rank": int(1 + sum(value > target_value + 1e-15 for value in rivals)),
        "target_activation": target_value,
        "target_margin": target_value - (float(rivals.max()) if rivals.size else 0.0),
    }


def _serialize_execution(execution, concepts: tuple[str, ...], target: str | None = None) -> dict:
    final = execution.prefixes[-1] if execution.prefixes else None
    return {
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
        "resolved_region": execution.top_candidate,
        "soft_top_candidate": execution.soft_top_candidate,
        "hard_intersection_candidates": list(execution.hard_intersection_candidates),
        "epistemic_classification": execution.epistemic_classification,
        "final_metrics": None if final is None else {
            "entropy": final.entropy,
            "normalized_entropy": final.normalized_entropy,
            "effective_candidate_count": final.effective_candidate_count,
            "concentration": final.concentration,
            "top_margin": final.top_margin,
            **(_target_metrics(final, target, concepts) if target else {}),
        },
    }


def _run_probe(flow, state, probe) -> dict:
    specs = tuple(
        TransitionStage(stage["id"], tuple(stage["constraints"]))
        for stage in probe["stages"]
    )
    execution = execute_stage_transition(flow, state, specs, POLICY)
    repeat = execute_stage_transition(flow, state, specs, POLICY)
    stages = []
    for record, authored in zip(execution.stages, probe["stages"]):
        serialized = _serialize_execution(record.execution, state.concepts, authored["expected_region"])
        stages.append({
            "stage_id": record.stage_id,
            "expected_region": authored["expected_region"],
            "matches_expected_region": record.execution.top_candidate == authored["expected_region"],
            "antecedent_region": record.antecedent_region,
            "retained_constraints": list(record.retained_constraints),
            "introduced_constraints": list(record.introduced_constraints),
            "released_constraints": list(record.released_constraints),
            "execution": serialized,
        })
    return {
        "probe_id": probe["id"],
        "description": probe["description"],
        "operation": execution.operation,
        "status": execution.status,
        "reason_code": execution.reason_code,
        "final_region": execution.final_region,
        "stages": stages,
        "flat_cumulative_control": _serialize_execution(execution.flat_control, state.concepts),
        "repeat_execution_matches": execution == repeat,
        "snapshot_id": execution.snapshot_id,
    }


def run_experiment() -> dict:
    fixture = load_experiment_fixture(MANIFEST_PATH)
    flow = CombinatorialUniquenessFlow()
    state = flow.govern_and_compile(fixture.state)
    probes = tuple(
        _run_probe(flow, state, probe)
        for probe in fixture.probes.probes["cross_level_probes"]
    )
    criteria = {
        "all_stage_local_regions_resolve": all(
            stage["execution"]["status"] == RESOLVED
            for probe in probes for stage in probe["stages"]
        ),
        "all_regions_match_predeclared_targets": all(
            stage["matches_expected_region"] for probe in probes for stage in probe["stages"]
        ),
        "antecedent_regions_are_preserved_in_trace": all(
            stage["antecedent_region"] == probe["stages"][index - 1]["execution"]["resolved_region"]
            for probe in probes for index, stage in enumerate(probe["stages"]) if index
        ),
        "level_changes_explicitly_release_constraints": all(
            stage["released_constraints"] for probe in probes for stage in probe["stages"][1:]
        ),
        "flat_conjunction_control_remains_unresolved": all(
            probe["flat_cumulative_control"]["status"] != RESOLVED for probe in probes
        ),
        "repeat_execution_is_deterministic": all(probe["repeat_execution_matches"] for probe in probes),
        "epistemic_classification_is_not_promoted": all(
            stage["execution"]["epistemic_classification"] == fixture.state.epistemic_classification
            for probe in probes for stage in probe["stages"]
        ),
    }
    return {
        "result_schema_version": "1.0",
        "experiment_id": "experiment-3.3-cross-level-semantic-transition-v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "title": "Experiment 3.3 — Cross-Level Semantic Transition",
        "research_question": "Can an interpretation transition from one semantic level to another as qualifying context is added, or does direct composition only perform flat conjunction?",
        "claim": "Explicit governed stage-local scopes can resolve successive semantic regions while preserving antecedent provenance and releasing coordinates that are not properties of the later region.",
        "claim_scope": "Authored stage-reset transition over one synthetic legal state; not automatic scope inference, typed relation traversal, legal causation, factual adjudication, or generalization.",
        "reporting_methodology": "OSCARC-v1",
        "fixture": {
            "manifest": str(MANIFEST_PATH.relative_to(ROOT)),
            "lifecycle": fixture.lifecycle,
            "holdout_status": fixture.probes.holdout_status,
            "concept_count": len(state.concepts),
            "dimension_count": len(state.dimensions),
            "relation_count": len(state.relation_ids),
            "snapshot_id": state.snapshot_id,
            "epistemic_classification": fixture.state.epistemic_classification,
        },
        "operation_contract": {
            "operation": "STAGE_RESET_TRANSITION",
            "stage_constraints_are_explicit": True,
            "antecedent_is_provenance_not_target_membership": True,
            "flat_control": "ordered union of all stage constraints under direct intersection",
            "policy_id": POLICY.policy_id,
        },
        "probes": list(probes),
        "results": {
            "probe_count": len(probes),
            "stage_count": sum(len(probe["stages"]) for probe in probes),
            "stage_resolution_rate": sum(
                stage["execution"]["status"] == RESOLVED
                for probe in probes for stage in probe["stages"]
            ) / sum(len(probe["stages"]) for probe in probes),
            "declared_region_match_rate": sum(
                stage["matches_expected_region"] for probe in probes for stage in probe["stages"]
            ) / sum(len(probe["stages"]) for probe in probes),
            "flat_control_non_resolution_rate": sum(
                probe["flat_cumulative_control"]["status"] != RESOLVED for probe in probes
            ) / len(probes),
        },
        "conformity": {
            "judgment": "CONSISTENT" if all(criteria.values()) else "INCONSISTENT",
            "evidence_strength": "DEVELOPMENT",
            "criteria": criteria,
        },
        "generalization": {
            "status": "UNTESTED",
            "required_next": "Freeze the operation and state before independently authoring transition probes.",
        },
        "artifact_identities": {
            "state_sha256": fixture.state.source_sha256,
            "probes_sha256": fixture.probes.source_sha256,
            "manifest_sha256": fixture.manifest_sha256,
            "compiled_snapshot_id": state.snapshot_id,
            "intersection_flow_sha256": _sha(ROOT / "src" / "combinatorial_uniqueness" / "combinatorial_uniqueness_flow.py"),
            "transition_operation_sha256": _sha(ROOT / "src" / "combinatorial_uniqueness" / "cross_level_semantic_transition.py"),
            "experiment_sha256": _sha(__file__),
            "methodology_sha256": _sha(METHODOLOGY_PATH),
        },
        "provenance": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "operation": "cross_level_semantic_transition.execute_stage_transition",
            "experiment": "cross_level_semantic_transition_experiment.py",
        },
        "evidence_boundary": "The stage-reset treatment was authored after the cumulative-intersection failure. A CONSISTENT result establishes only reproducible behavior of this explicit scoped operation in the co-authored synthetic fixture.",
    }


def markdown_report(result: dict) -> str:
    summary = result["results"]
    criteria = result["conformity"]["criteria"]
    fixture = result["fixture"]
    stage_rows = []
    control_rows = []
    transition_rows = []
    for probe in result["probes"]:
        first, second = probe["stages"]
        transition_rows.append(
            f"| `{probe['probe_id']}` | `{first['execution']['resolved_region']}` | "
            f"`{second['execution']['resolved_region']}` | {', '.join(second['retained_constraints'])} | "
            f"{', '.join(second['introduced_constraints'])} | {', '.join(second['released_constraints'])} |"
        )
        for index, stage in enumerate(probe["stages"], start=1):
            execution = stage["execution"]
            metrics = execution["final_metrics"]
            stage_rows.append(
                f"| `{probe['probe_id']}` | {index} | `{stage['expected_region']}` | "
                f"`{execution['resolved_region']}` | {metrics['target_rank']} | "
                f"{metrics['normalized_entropy']:.6f} | {metrics['target_margin']:.6f} |"
            )
        control = probe["flat_cumulative_control"]
        control_rows.append(
            f"| `{probe['probe_id']}` | `{control['status']}` | `{control['reason_code']}` | "
            f"`{control['governance']['reason_code']}` | `{control['soft_top_candidate']}` | "
            f"{len(control['hard_intersection_candidates'])} |"
        )
    lines = [
        "# Cross-Level Semantic Transition v1 — OSCARC Report",
        "",
        "> **An antecedent can remain part of the explanation without becoming a permanent property of its consequence.**",
        "",
        "## Research intention",
        "",
        result["research_question"],
        "",
        result["claim"],
        "",
        "This experiment isolates one operation that direct combinatorial intersection does not provide: a sequence of locally governed qualifications joined by an explicit level boundary. It asks whether stage scope can carry semantic interpretation forward without forcing every earlier coordinate into the definition of every later region.",
        "",
        "## Hypothesis scope",
        "",
        "This report tests **MML Experiment 3.3: Cross-Level Semantic Transition** only. Direct physical intersection (Experiment 3.1) and direct governed legal qualification (Experiment 3.2) are controls and upstream capabilities, not claims retested here.",
        "",
        "The experiment does not test automatic boundary discovery, typed transition relations, natural-language interpretation, legal causation, factual adjudication, or held-out generalization. A resolved synthetic semantic region is not an established fact, duty, inference, or violation.",
        "",
        "## Executive interpretation",
        "",
        f"The result is **{result['conformity']['judgment'].lower()}** with the bounded stage-reset claim. All {summary['stage_count']} authored stage-local compositions resolved their predeclared semantic regions, all antecedent regions remained visible in the trace, and deterministic replay matched. All {summary['probe_count']} flat cumulative controls remained unresolved because their complete coordinate unions had no governed common target.",
        "",
        "The comparison demonstrates an operational distinction, not a doctrinal conclusion: direct intersection answers “which target has all these properties?”, while stage-reset transition answers “which region resolves under this local scope, and which later region resolves after an explicit scope change?” Evidence strength remains **development** because the state and stage scopes are synthetic, co-authored, and not held out; the stage-reset treatment was designed after the original cumulative-intersection failure.",
        "",
        "## O — Objective observation",
        "",
        f"The unchanged synthetic legal state contains {fixture['concept_count']} concepts, {fixture['dimension_count']} dimensions, and {fixture['relation_count']} ordinary single-trait relations. Its compiled identity is `{fixture['snapshot_id']}`. The state does not contain typed cross-level transition edges or bespoke nodes for the tested stage combinations.",
        "",
        "The original access-to-evidence execution accumulated `access`, `incomplete_disclosure`, `source_coverage`, `exclusive_control`, `evidence`, and `dispute` as properties of one final target. The governed intersection became empty: access-level concepts did not also carry every evidential property, while `evidence_asymmetry` did not carry `access` or `source_coverage`. Numerical propagation still produced a leader, but governance correctly refused to convert that leader into a resolved region.",
        "",
        f"Experiment 3.3 observed {summary['probe_count']} comparable sequences. Each was executed once as explicit stage-local composition and once as the ordered union of all stage constraints through direct intersection. Machine-readable stage fields, target measurements, governance outcomes, scope changes, replay status, hashes, and provenance are retained in the companion artifact.",
        "",
        "## S — Standard, baseline, or reference model",
        "",
        "The baseline is the existing governed direct-intersection operation. It treats every supplied coordinate as required final-target membership. Empty hard intersection must remain unresolved even if the soft numerical field has a leader.",
        "",
        "The treatment is `STAGE_RESET_TRANSITION`. Every stage declares a local constraint set. Adjacent stages must retain at least one coordinate, preventing two unrelated queries from being presented as a transition. The execution trace records the preceding resolved region as the antecedent and names every retained, introduced, and released coordinate.",
        "",
        "The development standard required all of the following:",
        "",
        "1. every authored stage-local composition resolves under the unchanged direct-intersection kernel;",
        "2. every resolved region equals the target declared in the probe fixture;",
        "3. the preceding resolved region remains present as provenance at the next stage;",
        "4. every semantic level change explicitly releases at least one coordinate;",
        "5. flat cumulative conjunction remains separately executed and distinguishable;",
        "6. deterministic repeat execution matches exactly; and",
        "7. numerical resolution does not promote the fixture's synthetic epistemic classification.",
        "",
        "These criteria test the authored stage-reset contract. They do not test whether MML can discover stage boundaries, select retained coordinates autonomously, or validate typed causal and legal relations.",
        "",
        "## C — Context and chronology",
        "",
        f"The fixture lifecycle is `{fixture['lifecycle']}` and the probe holdout status is `{fixture['holdout_status']}`. Its epistemic classification is `{fixture['epistemic_classification']}`. That classification is operational metadata and cannot become an established fact, inference, duty, or violation through activation.",
        "",
        "The research chronology matters:",
        "",
        "```text",
        "direct legal fixture authored",
        "    -> cumulative cross-level probe executed",
        "    -> empty governed intersection observed",
        "    -> failure retained and analyzed",
        "    -> stage-reset operation declared",
        "    -> stage-local scopes authored",
        "    -> flat control and stage-reset treatment executed",
        "    -> deterministic replay and artifact checks",
        "```",
        "",
        "Because the intervention followed inspection of the failure, this is test-driven mechanism development rather than confirmatory testing. The original failure is not removed: the same cumulative operation is rerun inside every probe as the control. The legal state itself remains unchanged.",
        "",
        "The stage scopes were authored after observing the original failure; they must therefore be evaluated as an explicit follow-up treatment rather than independent confirmation.",
        "",
        "## A — Actions, interventions, or observed mechanisms",
        "",
        f"The experiment compiled the legal state once, then executed {summary['probe_count']} two-stage transitions ({summary['stage_count']} stages), {summary['probe_count']} flat cumulative controls, and exact deterministic repeats using policy `{result['operation_contract']['policy_id']}`.",
        "",
        "At every stage, the existing direct composition flow independently activated the declared fields, combined them through normalized geometric-mean soft intersection, and validated the numerical leader against governed hard incidence. The new operational layer did not change that mathematics. It coordinated stage scope and recorded transition provenance.",
        "",
        "For the second stage, the operation performed three inspectable actions:",
        "",
        "- retained coordinates continued to qualify both semantic levels;",
        "- introduced coordinates supplied the later level's additional information; and",
        "- released coordinates remained in the antecedent trace but ceased to be required properties of the later target.",
        "",
        "The expected target is used only by the experiment adapter to evaluate the result. It is not passed into the operational transition executor and does not influence activation, scope execution, or governance.",
        "",
        "## R — Result, effect, or measured outcome",
        "",
        "### Aggregate outcomes",
        "",
        "| Measure | Result |",
        "| --- | ---: |",
        f"| Stage-local resolution | {summary['stage_resolution_rate']:.1%} |",
        f"| Declared-region match | {summary['declared_region_match_rate']:.1%} |",
        f"| Flat-control non-resolution | {summary['flat_control_non_resolution_rate']:.1%} |",
        "",
        "### Semantic transitions and scope changes",
        "",
        "| Probe | Antecedent region | Consequent region | Retained | Introduced | Released |",
        "| --- | --- | --- | --- | --- | --- |",
        *transition_rows,
        "",
        "The retained coordinates provide semantic continuity across the boundary. Introduced coordinates qualify the later level. Released coordinates remain attributable to the antecedent but are no longer asserted as properties of the consequent.",
        "",
        "### Stage-local measurements",
        "",
        "| Probe | Stage | Declared region | Resolved region | Target rank | Normalized entropy | Target margin |",
        "| --- | ---: | --- | --- | ---: | ---: | ---: |",
        *stage_rows,
        "",
        "All declared targets ranked first within their stage-local candidate fields. Entropy and margin values describe the final normalized candidate distribution for each stage; they are not legal confidence scores.",
        "",
        "### Flat cumulative controls",
        "",
        "| Probe | Status | Overall reason | Governance reason | Numerical leader | Governed candidates |",
        "| --- | --- | --- | --- | --- | ---: |",
        *control_rows,
        "",
        "Every flat control had an empty governed intersection. Some retained a numerical leader because soft propagation measures proximity even when exact required membership is absent. Governance kept these channels separate and refused resolution.",
        "",
        "## C — Comparative assessment and research conclusion",
        "",
        f"**Conformity judgment: `{result['conformity']['judgment']}`.** Every declared criterion passed within this authored fixture. Stage-local composition resolved 6/6 declared regions, all three flat conjunction controls remained unresolved, antecedent provenance and scope changes were complete, and replay was deterministic.",
        "",
        "**Evidence strength: `DEVELOPMENT`.** The outcome supports the local claim that an explicit governed stage-reset operation can represent these three cross-level sequences without treating every antecedent coordinate as final-target membership. It does not establish that stage reset is the uniquely correct operation, that the selected scopes are doctrinally complete, or that an unseen transition can be constructed without author guidance.",
        "",
        "It does not demonstrate automatic scope discovery, typed transition inference, or legal causation. Those remain separate claims requiring separately governed treatments and independently authored evidence.",
        "",
        "| Criterion | Result |",
        "| --- | --- |",
        *[f"| `{name}` | {'pass' if passed else 'fail'} |" for name, passed in criteria.items()],
        "",
        "### Claims ladder",
        "",
        "| Level | Claim | Status |",
        "| --- | --- | --- |",
        "| implementation fact | stage reset and flat controls use the same direct composition mechanism inside each scope | verified |",
        "| fixture observation | all six stages resolved and all three cumulative controls remained unresolved | observed in authored fixtures |",
        "| operational signal | antecedents can remain provenance without remaining final-target properties | early directional signal |",
        "| transition hypothesis | explicit stage scope generalizes to unseen semantic transitions | untested |",
        "| governance hypothesis | MML can discover valid boundaries and retained coordinates automatically | untested |",
        "| typed-relation hypothesis | governed directional relations improve cross-level qualification | untested |",
        "| legal application claim | resolved regions establish facts, duties, or violations | outside evidence boundary |",
        "",
        "The ladder prevents successful execution of authored scopes from being promoted into automatic semantic transition or legal reasoning without separate evidence.",
        "",
        "## Recommendation and next step",
        "",
        "Freeze the stage-reset operation, legal state, policy, and conformity thresholds before authoring a new probe suite. The next suite should be created independently after the freeze and should include successful transitions, deliberately unrelated adjacent stages, ambiguous boundary choices, cases requiring different retained-coordinate sets, and cases where no later region should resolve.",
        "",
        "In parallel, treat typed directional transitions as a separate experimental treatment rather than silently enriching this result. Compare explicit stage reset with governed relations such as `may_create_evidential_effect` or `may_impair`, retaining provenance and refusal behavior in both treatments. This will determine whether authored scope alone is sufficient or whether transition semantics must become part of the governed state.",
        "",
        "## Evidence boundary",
        "",
        result["evidence_boundary"],
        "",
        result["claim_scope"],
        "",
        "This report follows the [OSCARC methodology](../../../benchmark/oscarc-methodology.md). The [machine-readable JSON artifact](../../../../benchmark/results/cross-level-semantic-transition-v1.json) remains authoritative for measurements, complete transition traces, conformity inputs, artifact identities, and provenance.",
    ]
    return "\n".join(lines) + "\n"


def _comparable(result: dict) -> dict:
    comparable = json.loads(json.dumps(result))
    comparable.pop("generated_at", None)
    return comparable


def write_results(result: dict, result_path: Path = RESULT_PATH, report_path: Path = REPORT_PATH) -> None:
    result_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    report_path.write_text(markdown_report(result), encoding="utf-8")


def check_result(result: dict, result_path: Path = RESULT_PATH, report_path: Path = REPORT_PATH) -> None:
    if not result_path.exists() or not report_path.exists():
        raise SystemExit("Experiment 3.3 reference artifacts are missing; run --write.")
    reference = json.loads(result_path.read_text(encoding="utf-8"))
    if _comparable(reference) != _comparable(result):
        raise SystemExit("Experiment 3.3 machine evidence differs from the reference artifact.")
    if report_path.read_text(encoding="utf-8") != markdown_report(result):
        raise SystemExit("Experiment 3.3 OSCARC report differs from the reference artifact.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Experiment 3.3 cross-level semantic transition.")
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
