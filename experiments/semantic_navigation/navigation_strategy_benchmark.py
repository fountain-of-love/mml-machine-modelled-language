"""Compare uniform-prior question strategies within Semantic Navigation."""

from __future__ import annotations

import hashlib
import math
import statistics
from pathlib import Path

from src.helpers.artifacts import compare_artifact_pair, write_artifact_pair
from src.helpers.hashing import sha256_file
from src.helpers.json_io import canonical_json_bytes
from src.helpers.research_cli import ResearchCommand, run_research_command
from src.semantic_navigation.navigation import (
    AMBIGUOUS,
    IDENTIFIABLE,
    UNSUPPORTED,
    NavigationLens,
    NavigationResult,
    SemanticNavigationFlow,
)
from src.semantic_navigation.strategies import (
    FIXED_DIMENSION_ORDER,
    HIGHEST_CARDINALITY,
    HIGHEST_COVERAGE,
    INFORMATION_GAIN,
    RANDOM_ELIGIBLE,
    FixedDimensionOrderNavigationStrategy,
    HighestCardinalityNavigationStrategy,
    HighestCoverageNavigationStrategy,
    InformationGainNavigationStrategy,
    NavigationStrategy,
    RandomEligibleNavigationStrategy,
)

from .fixtures import (
    COMPILED_NAVIGATION_SEED_PATH,
    load_compiled_navigation_fixture,
)


ROOT = Path(__file__).resolve().parents[2]
RESULT_PATH = ROOT / "benchmark" / "results" / "semantic-navigation-strategy-v1.json"
REPORT_PATH = (
    ROOT
    / "docs"
    / "capabilities"
    / "semantic-navigation"
    / "results"
    / "semantic-navigation-strategy-v1.md"
)
STUDY_PATH = (
    ROOT
    / "docs"
    / "capabilities"
    / "semantic-navigation"
    / "dimension-contribution-experiment.md"
)
NAVIGATION_PATH = ROOT / "src" / "semantic_navigation" / "navigation.py"
STRATEGIES_PATH = ROOT / "src" / "semantic_navigation" / "strategies.py"

DETERMINISTIC_STRATEGIES = (
    INFORMATION_GAIN,
    FIXED_DIMENSION_ORDER,
    HIGHEST_CARDINALITY,
    HIGHEST_COVERAGE,
)
STRATEGIES = DETERMINISTIC_STRATEGIES + (RANDOM_ELIGIBLE,)
RANDOM_REPLICATES = 32
RANDOM_SEED = 42042

UNSUPPORTED_PROBES = (
    {"habitat": "polar", "diet": "herbivore", "activity": "nocturnal", "sociality": "colony"},
    {"habitat": "ocean", "diet": "herbivore", "activity": "nocturnal", "sociality": "pack"},
    {"habitat": "desert", "diet": "carnivore", "activity": "diurnal", "sociality": "herd"},
)


def _strategy(strategy_id: str, replicate: int) -> NavigationStrategy:
    if strategy_id == INFORMATION_GAIN:
        return InformationGainNavigationStrategy()
    if strategy_id == FIXED_DIMENSION_ORDER:
        return FixedDimensionOrderNavigationStrategy()
    if strategy_id == HIGHEST_CARDINALITY:
        return HighestCardinalityNavigationStrategy()
    if strategy_id == HIGHEST_COVERAGE:
        return HighestCoverageNavigationStrategy()
    if strategy_id == RANDOM_ELIGIBLE:
        return RandomEligibleNavigationStrategy(RANDOM_SEED + replicate)
    raise ValueError(f"unknown navigation strategy: {strategy_id}")


def _best_gain(result: NavigationResult) -> float:
    return max(
        (
            item.information_gain_bits
            for item in result.partition_information.values()
        ),
        default=0.0,
    )


def _run_trajectory(
    state,
    *,
    target_ids: tuple[str, ...],
    target_attributes: dict[str, str | None],
    strategy_id: str,
    lens: NavigationLens,
    replicate: int,
) -> dict:
    flow = SemanticNavigationFlow(_strategy(strategy_id, replicate))
    observed: dict[str, str] = {}
    initial_count = len(state.basis.entities)
    steps = []

    def navigate(active_lens: NavigationLens | None = lens) -> NavigationResult:
        if observed:
            return flow.execute(state, observed, lens=active_lens)
        return flow.start(state, lens=active_lens)

    while True:
        result = navigate()
        if set(result.candidate_ids) == set(target_ids):
            termination = "TARGET_EQUIVALENCE_CLASS_REACHED"
            break
        selected = result.next_dimension
        if selected is None:
            termination = "LENS_EXHAUSTED"
            break
        value = target_attributes[selected]
        if value is None:
            raise AssertionError("foundational strategy fixture must be complete")
        open_result = navigate(None)
        selected_gain = result.partition_information[selected].information_gain_bits
        steps.append({
            "candidate_count_before": len(result.candidate_ids),
            "selected_dimension": selected,
            "observed_value": value,
            "selected_information_gain_bits": selected_gain,
            "selected_question_regret_bits": max(0.0, _best_gain(open_result) - selected_gain),
            "lens_regret_bits": max(0.0, _best_gain(open_result) - _best_gain(result)),
        })
        if result.strategy_id != strategy_id:
            raise AssertionError("navigation result lost its injected strategy identity")
        observed[selected] = value

    final = navigate()
    questions = len(steps)
    reduction = initial_count - len(final.candidate_ids)
    return {
        "strategy_id": strategy_id,
        "lens_id": lens.id,
        "replicate": replicate,
        "target_class": list(target_ids),
        "questions_asked": questions,
        "target_class_reached": set(final.candidate_ids) == set(target_ids),
        "termination": termination,
        "final_status": final.status,
        "final_candidate_count": len(final.candidate_ids),
        "residual_entropy_bits": math.log2(len(final.candidate_ids)) if final.candidate_ids else 0.0,
        "candidate_reduction": reduction,
        "candidate_reduction_fraction": reduction / initial_count,
        "candidate_reduction_per_question": reduction / questions if questions else 0.0,
        "mean_selected_question_regret_bits": statistics.fmean(
            step["selected_question_regret_bits"] for step in steps
        ) if steps else 0.0,
        "mean_lens_regret_bits": statistics.fmean(
            step["lens_regret_bits"] for step in steps
        ) if steps else 0.0,
        "steps": steps,
    }


def _mean(traces: list[dict], field: str) -> float:
    return statistics.fmean(trace[field] for trace in traces) if traces else 0.0


def _aggregate(traces: list[dict]) -> dict:
    reached = [trace for trace in traces if trace["target_class_reached"]]
    return {
        "trajectory_count": len(traces),
        "target_class_resolution_rate": len(reached) / len(traces),
        "mean_questions_asked": _mean(traces, "questions_asked"),
        "mean_questions_to_target_class": (
            _mean(reached, "questions_asked") if reached else None
        ),
        "mean_final_candidate_count": _mean(traces, "final_candidate_count"),
        "mean_residual_entropy_bits": _mean(traces, "residual_entropy_bits"),
        "mean_candidate_reduction": _mean(traces, "candidate_reduction"),
        "mean_candidate_reduction_fraction": _mean(
            traces, "candidate_reduction_fraction"
        ),
        "mean_candidate_reduction_per_question": _mean(
            traces, "candidate_reduction_per_question"
        ),
        "identifiable_rate": sum(
            trace["final_status"] == IDENTIFIABLE for trace in traces
        ) / len(traces),
        "ambiguous_rate": sum(
            trace["final_status"] == AMBIGUOUS for trace in traces
        ) / len(traces),
        "unsupported_rate": sum(
            trace["final_status"] == UNSUPPORTED for trace in traces
        ) / len(traces),
        "lens_exhausted_rate": sum(
            trace["termination"] == "LENS_EXHAUSTED" for trace in traces
        ) / len(traces),
        "mean_selected_question_regret_bits": _mean(
            traces, "mean_selected_question_regret_bits"
        ),
        "mean_lens_regret_bits": _mean(traces, "mean_lens_regret_bits"),
    }


def _target_classes(state) -> tuple[tuple[tuple[str, ...], dict[str, str | None]], ...]:
    targets = []
    for candidate_ids in sorted(state.knowledge_state.signature_classes.values()):
        position = state.knowledge_state.entity_positions[candidate_ids[0]]
        attributes = dict(state.basis.entities[position].attributes)
        targets.append((candidate_ids, attributes))
    return tuple(targets)


def _strategy_runs(strategy_id: str) -> range:
    return range(RANDOM_REPLICATES) if strategy_id == RANDOM_ELIGIBLE else range(1)


def _trace_evidence(traces: list[dict]) -> dict:
    serialized = canonical_json_bytes(traces)
    return {
        "trajectory_count": len(traces),
        "trace_sha256": f"sha256:{hashlib.sha256(serialized).hexdigest()}",
        "sample": traces[:3],
    }


def run_experiment() -> dict:
    fixture, dimensions, records, _ = load_compiled_navigation_fixture()
    flow = SemanticNavigationFlow()
    state = flow.govern_and_compile(
        "semantic_navigation_strategy_v1",
        dimensions,
        records,
    )
    lenses = (
        NavigationLens("open", dimensions),
        NavigationLens("ecological", ("habitat", "diet", "activity")),
        NavigationLens("behavioral", ("activity", "sociality")),
    )
    targets = _target_classes(state)
    traces = []
    grouped: dict[str, dict[str, dict]] = {}
    for lens in lenses:
        grouped[lens.id] = {}
        for strategy_id in STRATEGIES:
            strategy_traces = [
                _run_trajectory(
                    state,
                    target_ids=target_ids,
                    target_attributes=attributes,
                    strategy_id=strategy_id,
                    lens=lens,
                    replicate=replicate,
                )
                for replicate in _strategy_runs(strategy_id)
                for target_ids, attributes in targets
            ]
            traces.extend(strategy_traces)
            grouped[lens.id][strategy_id] = _aggregate(strategy_traces)

    unsupported = [flow.execute(state, probe) for probe in UNSUPPORTED_PROBES]
    open_metrics = grouped["open"]
    other_strategy_questions = {
        strategy: metrics["mean_questions_asked"]
        for strategy, metrics in open_metrics.items()
        if strategy != INFORMATION_GAIN
    }
    best_other_strategy = min(other_strategy_questions, key=other_strategy_questions.get)
    criteria = {
        "uniform_candidate_prior_declared": True,
        "all_strategies_share_initial_state": True,
        "information_gain_questions_maximize_local_information_gain": all(
            trace["mean_selected_question_regret_bits"] == 0.0
            for trace in traces
            if trace["strategy_id"] == INFORMATION_GAIN
            and trace["lens_id"] == "open"
        ),
        "valid_target_trajectories_never_become_unsupported": all(
            trace["final_status"] != UNSUPPORTED for trace in traces
        ),
        "unsupported_probes_remain_unsupported": all(
            result.status == UNSUPPORTED for result in unsupported
        ),
        "random_strategy_is_seeded_and_replicated": RANDOM_REPLICATES > 1,
    }
    return {
        "schema_version": "1.0",
        "experiment_id": "experiment-4.2-semantic-navigation-strategy-v1",
        "title": "Experiment 4.2 - Semantic Navigation Strategy Comparison",
        "research_stream": "Programme 4 - Semantic Navigation",
        "research_question": "Given one shared MML candidate state, which next-question strategy navigates it most effectively?",
        "fixture": {
            "state_id": fixture["state_id"],
            "record_count": len(records),
            "equivalence_class_count": len(targets),
            "dimensions": list(dimensions),
            "complete_scalar_field": True,
            "evidence_boundary": fixture["evidence_boundary"],
        },
        "protocol": {
            "candidate_prior": "uniform",
            "target_unit": "complete-signature equivalence class",
            "question_answer": "target exemplar's governed scalar value",
            "eligible_question": "unobserved lens dimension with positive information gain",
            "random_seed": RANDOM_SEED,
            "random_replicates": RANDOM_REPLICATES,
            "shared_substrate": "MML governed representation, compiled incidence state, exact composition, ambiguity, and refusal",
            "varied_component": "NavigationStrategy",
            "strategies": list(STRATEGIES),
            "lenses": {lens.id: list(lens.dimensions) for lens in lenses},
            "deferred_treatments": [
                "non_uniform_candidate_priors",
                "llm_selected_question",
                "multi_valued_source_state",
                "non_mml_system_comparison",
            ],
        },
        "strategy_results": grouped,
        "open_comparison": {
            "best_other_strategy_by_mean_questions": best_other_strategy,
            "information_gain_minus_best_other_strategy_mean_questions": (
                open_metrics[INFORMATION_GAIN]["mean_questions_asked"]
                - open_metrics[best_other_strategy]["mean_questions_asked"]
            ),
            "information_gain_minus_best_other_strategy_residual_entropy_bits": (
                open_metrics[INFORMATION_GAIN]["mean_residual_entropy_bits"]
                - open_metrics[best_other_strategy]["mean_residual_entropy_bits"]
            ),
        },
        "unsupported_probes": {
            "count": len(unsupported),
            "unsupported_rate": sum(
                result.status == UNSUPPORTED for result in unsupported
            ) / len(unsupported),
        },
        "trace_evidence": _trace_evidence(traces),
        "conformity": {
            "judgment": (
                "UNIFORM_STRATEGY_EXPERIMENT_CONFORMANT"
                if all(criteria.values())
                else "UNIFORM_STRATEGY_EXPERIMENT_NONCONFORMANT"
            ),
            "criteria": criteria,
        },
        "artifact_identities": {
            "fixture_sha256": sha256_file(COMPILED_NAVIGATION_SEED_PATH),
            "navigation_sha256": sha256_file(NAVIGATION_PATH),
            "strategies_sha256": sha256_file(STRATEGIES_PATH),
            "experiment_sha256": sha256_file(Path(__file__)),
            "study_sha256": sha256_file(STUDY_PATH),
        },
        "interpretation_boundary": (
            "This is a strategy ablation within one shared MML substrate: governed representation, compiled state, "
            "exact candidate composition, ambiguity, and refusal are common to every treatment. It does not compare "
            "MML with a non-MML system, learned priors, natural-language generation, an LLM strategy, or the partial "
            "multi-valued Canidae source state."
        ),
    }


def evidence_manifest(result: dict) -> dict:
    return result


def markdown_report(result: dict) -> str:
    lines = [
        "# Experiment 4.2 - Semantic Navigation Strategy Comparison",
        "",
        "## Result",
        "",
        f"Judgment: `{result['conformity']['judgment']}`.",
        "",
        "Every strategy started from the same 60-animal compiled state and was evaluated against the same 48 complete-signature equivalence classes under a uniform candidate prior. Random selection used 32 deterministic replicates.",
        "",
        "## Open-Lens Comparison",
        "",
        "| Strategy | Resolve target class | Questions | Residual entropy | Reduction/question | Ambiguous | Selected regret |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for strategy in STRATEGIES:
        metrics = result["strategy_results"]["open"][strategy]
        lines.append(
            f"| `{strategy}` | {metrics['target_class_resolution_rate']:.1%} | "
            f"{metrics['mean_questions_asked']:.3f} | {metrics['mean_residual_entropy_bits']:.3f} | "
            f"{metrics['mean_candidate_reduction_per_question']:.3f} | "
            f"{metrics['ambiguous_rate']:.1%} | {metrics['mean_selected_question_regret_bits']:.3f} |"
        )
    comparison = result["open_comparison"]
    lines.extend([
        "",
        "Every treatment uses the same MML representation, compiled state, exact retrieval, ambiguity, and refusal contracts; only the injected next-question strategy changes.",
        "",
        f"The best other strategy by mean questions was `{comparison['best_other_strategy_by_mean_questions']}`. "
        f"Information gain minus that strategy was `{comparison['information_gain_minus_best_other_strategy_mean_questions']:.3f}` questions and "
        f"`{comparison['information_gain_minus_best_other_strategy_residual_entropy_bits']:.3f}` residual-entropy bits.",
        "",
        "Because every foundational record is complete, all dimensions have equal coverage. The highest-coverage strategy therefore falls back to frozen basis order and is behaviorally equivalent to fixed order in this treatment; coverage sensitivity remains for the partial-state expansion.",
        "",
        "## Lens Results",
        "",
        "| Lens | Strategy | Resolve target class | Questions | Residual entropy | Lens regret | Lens exhausted |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: |",
    ])
    for lens in ("ecological", "behavioral"):
        for strategy in STRATEGIES:
            metrics = result["strategy_results"][lens][strategy]
            lines.append(
                f"| `{lens}` | `{strategy}` | {metrics['target_class_resolution_rate']:.1%} | "
                f"{metrics['mean_questions_asked']:.3f} | {metrics['mean_residual_entropy_bits']:.3f} | "
                f"{metrics['mean_lens_regret_bits']:.3f} | {metrics['lens_exhausted_rate']:.1%} |"
            )
    lines.extend([
        "",
        "## Refusal And Ambiguity",
        "",
        f"All {result['unsupported_probes']['count']} unsupported combinations remained `UNSUPPORTED` "
        f"({result['unsupported_probes']['unsupported_rate']:.1%}). Valid target trajectories never became unsupported. "
        "Terminal ambiguity represents genuine complete-signature equivalence classes or a lens that cannot express the remaining distinction; it is not forced into top-1 identification.",
        "",
        "## Interpretation Boundary",
        "",
        result["interpretation_boundary"],
        "",
        "Non-uniform `IG(d | C, P)`, LLM-selected questions, comparisons with non-MML systems, and the partial multi-valued Canidae field are separately identified follow-on treatments.",
    ])
    return "\n".join(lines) + "\n"


def write_results(result: dict) -> None:
    write_artifact_pair(
        RESULT_PATH,
        evidence_manifest(result),
        REPORT_PATH,
        markdown_report(result),
    )


def check_result(result: dict) -> None:
    comparison = compare_artifact_pair(
        evidence_manifest(result),
        markdown_report(result),
        RESULT_PATH,
        REPORT_PATH,
    )
    if comparison.missing_paths:
        raise SystemExit("Experiment 4.2 reference artifacts are missing; run --write.")
    if not comparison.json_matches:
        raise SystemExit("Experiment 4.2 machine evidence differs from the reference artifact.")
    if not comparison.text_matches:
        raise SystemExit("Experiment 4.2 report differs from the reference artifact.")


def main() -> None:
    run_research_command(ResearchCommand(
        description="Run Experiment 4.2 semantic navigation strategy comparison.",
        run=run_experiment,
        render=markdown_report,
        write=write_results,
        check=check_result,
    ))


if __name__ == "__main__":
    main()
