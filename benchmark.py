"""Benchmark whether richer semantic identity improves fixed matrix execution.

The benchmark deliberately reuses the Words Carry Weight experiment. Every
scenario runs the same compiler and Personalized PageRank query strategy twice:
first over ambiguous surface identities and then over governed identities. The
representation is the independent variable; the mathematics remains fixed.
"""

import argparse
import hashlib
import json
import platform
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from activate_grounded_focus import PersonalizedPageRankActivationStrategy
from experiment_fixture import load_experiment
from representation_comparison import compare_representations


ROOT = Path(__file__).parent
RESULT_PATH = ROOT / "benchmark" / "results" / "semantic-representation-v1.json"
REPORT_PATH = ROOT / "docs" / "benchmark" / "results" / "semantic-representation-v1.md"
METHODOLOGY_PATH = ROOT / "docs" / "benchmark" / "oscarc-methodology.md"
KERNEL_PATH = ROOT / "activate_grounded_focus.py"
FLOW_PATH = ROOT / "words_carry_weight.py"
COMPARISON_PATH = ROOT / "representation_comparison.py"
FIXTURE_PATH = ROOT / "data" / "demonstration" / "words_carry_weight.json"
GENERATOR_PATH = ROOT / "benchmark.py"
BENCHMARK_VERSION = "semantic-representation-v1"
INTENTION = "Richer meaning representation can make established mathematics produce more useful results."
FIXED_MATHEMATICS = "converged-personalized-pagerank-v1"
METHODOLOGY = "OSCARC-v1"


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def convergence_record(activation):
    return {
        "converged": activation.converged,
        "iterations": activation.iterations,
        "residual": activation.residual,
    }


def representation_cost(model):
    return {
        "identity_count": len(model.identities),
        "nonzero_transition_count": int(np.count_nonzero(model.transition)),
        "transition_bytes": int(model.transition.nbytes),
    }


def runtime_identity():
    """Return replay-relevant runtime facts without claiming cross-host equivalence."""
    numpy_config = getattr(np.__config__, "CONFIG", {})
    blas = numpy_config.get("Build Dependencies", {}).get("blas", {})
    return {
        "python": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "numpy": np.__version__,
        "operating_system": platform.system(),
        "operating_system_release": platform.release(),
        "architecture": platform.machine(),
        "blas": {
            "name": blas.get("name", "unknown"),
            "version": blas.get("version", "unknown"),
        },
    }


@dataclass(frozen=True)
class BenchmarkScenario:
    """One controlled ambiguous-versus-grounded representation comparison."""

    scenario_id: str
    description: str
    experiment: dict


def _experiment(sentences, surface_identity, meanings, contexts, display_exclusions=()):
    """Build the Words Carry Weight experiment contract for one scenario."""
    semantic_groundings = []
    focused_queries = []
    for meaning in meanings:
        for sentence_index in meaning["sentence_indices"]:
            semantic_groundings.append({
                "sentence_index": sentence_index,
                "surface_identity": surface_identity,
                "grounded_identity": meaning["identity"],
            })
        focused_queries.append({
            "source_identity": surface_identity,
            "focused_identity": meaning["identity"],
            "primary_context": meaning["primary_context"],
            "contrast_context": meaning["contrast_context"],
        })
    return {
        "sentences": sentences,
        "semantic_groundings": semantic_groundings,
        "original_query": surface_identity,
        "focused_queries": focused_queries,
        "contexts": contexts,
        "display_exclusions": list(display_exclusions),
    }


def benchmark_scenarios():
    """Return authored development scenarios executed by the shared experiment."""
    bank = BenchmarkScenario(
        "identity-bank",
        "Grounding bank as river land or a financial institution.",
        load_experiment(),
    )
    bass = BenchmarkScenario(
        "identity-bass",
        "Grounding bass as a fish or a musical instrument.",
        _experiment(
            (
                "the bass swam through the lake beside green reeds",
                "an angler caught the bass in shallow water",
                "the fish moved beneath the quiet surface",
                "the bass played a deep note in the band",
                "the musician tuned the bass before the concert",
                "the rhythm section carried the music through the hall",
            ),
            "bass",
            (
                {"identity": "bass_fish", "sentence_indices": (0, 1),
                 "primary_context": "aquatic", "contrast_context": "musical"},
                {"identity": "bass_instrument", "sentence_indices": (3, 4),
                 "primary_context": "musical", "contrast_context": "aquatic"},
            ),
            {
                "aquatic": ["lake", "water", "fish", "angler"],
                "musical": ["note", "band", "musician", "music"],
            },
            ("the", "a", "an", "in", "through", "before", "beside"),
        ),
    )
    crane = BenchmarkScenario(
        "identity-crane",
        "Grounding crane as a bird or lifting machinery.",
        _experiment(
            (
                "the crane spread its wings above the wetland",
                "a crane searched for fish beside the marsh",
                "the bird nested near the quiet water",
                "the crane lifted steel above the building site",
                "a worker guided the crane beside the tower",
                "the machine moved a heavy beam into place",
            ),
            "crane",
            (
                {"identity": "crane_bird", "sentence_indices": (0, 1),
                 "primary_context": "bird", "contrast_context": "machine"},
                {"identity": "crane_machine", "sentence_indices": (3, 4),
                 "primary_context": "machine", "contrast_context": "bird"},
            ),
            {
                "bird": ["wings", "wetland", "fish", "marsh", "bird"],
                "machine": ["steel", "building", "worker", "tower", "machine", "beam"],
            },
            ("the", "a", "an", "above", "beside", "into", "near"),
        ),
    )
    return bank, bass, crane


def evaluate_scenario(scenario, strategy=None):
    """Measure the joint grounding-and-focus treatment under fixed algorithms."""
    strategy = strategy or PersonalizedPageRankActivationStrategy()
    comparison = compare_representations(scenario.experiment, strategy)
    baseline_activation = comparison["original"]["activation"]
    original_contexts = comparison["original"]["contexts"]
    probes_by_identity = {
        probe["focused_identity"]: probe
        for probe in scenario.experiment["focused_queries"]
    }
    probes = []
    for identity, grounded in comparison["grounded"].items():
        declaration = probes_by_identity[identity]
        baseline_primary = original_contexts[declaration["primary_context"]]
        baseline_contrast = original_contexts[declaration["contrast_context"]]
        baseline_margin = baseline_primary - baseline_contrast
        grounded_margin = grounded["primary_context"] - grounded["contrast_context"]
        baseline_context_total = baseline_primary + baseline_contrast
        grounded_context_total = grounded["primary_context"] + grounded["contrast_context"]
        baseline_selectivity = (
            baseline_primary / baseline_context_total if baseline_context_total else 0.0
        )
        grounded_selectivity = (
            grounded["primary_context"] / grounded_context_total if grounded_context_total else 0.0
        )
        probe = {
            "identity": identity,
            "primary_context": declaration["primary_context"],
            "contrast_context": declaration["contrast_context"],
            "baseline_primary": baseline_primary,
            "baseline_contrast": baseline_contrast,
            "grounded_primary": grounded["primary_context"],
            "grounded_contrast": grounded["contrast_context"],
            "baseline_margin": baseline_margin,
            "grounded_margin": grounded_margin,
            "margin_improvement": grounded_margin - baseline_margin,
            "contrast_reduction": baseline_contrast - grounded["contrast_context"],
            "baseline_selectivity": baseline_selectivity,
            "grounded_selectivity": grounded_selectivity,
            "selectivity_gain": grounded_selectivity - baseline_selectivity,
            "convergence": {
                "baseline": convergence_record(baseline_activation),
                "treatment": convergence_record(grounded["activation"]),
            },
        }
        probe["checks"] = {
            "grounded_field_favors_intended_context": probe["grounded_selectivity"] > 0.5,
            "intended_context_share_improves": probe["selectivity_gain"] > 0,
            "intended_versus_contrast_margin_improves": probe["margin_improvement"] > 0,
            "contrast_reduces": probe["contrast_reduction"] > 0,
        }
        probe["supported"] = all(probe["checks"].values())
        probes.append(probe)
    treatment_model = next(iter(comparison["grounded"].values()))["activation"].model
    baseline_cost = representation_cost(baseline_activation.model)
    treatment_cost = representation_cost(treatment_model)
    return {
        "scenario_id": scenario.scenario_id,
        "description": scenario.description,
        "surface_identity": scenario.experiment["original_query"],
        "sentence_count": len(scenario.experiment["sentences"]),
        "grounded_occurrence_count": len(scenario.experiment["semantic_groundings"]),
        "representation_cost": {
            "baseline": baseline_cost,
            "treatment": treatment_cost,
            "delta": {
                key: treatment_cost[key] - baseline_cost[key]
                for key in baseline_cost
            },
        },
        "probes": probes,
        "supported": all(probe["supported"] for probe in probes),
        "all_activations_converged": all(
            convergence["converged"] is True
            for probe in probes
            for convergence in probe["convergence"].values()
        ),
    }


def run_benchmark():
    """Execute every scenario twice and fail closed on nondeterministic behavior."""
    scenarios = benchmark_scenarios()
    first = [evaluate_scenario(scenario) for scenario in scenarios]
    second = [evaluate_scenario(scenario) for scenario in scenarios]
    deterministic = first == second
    supported_scenarios = sum(result["supported"] for result in first)
    all_converged = all(item["all_activations_converged"] for item in first)
    all_probes_supported = supported_scenarios == len(first)
    result = {
        "benchmark_version": BENCHMARK_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "intention": INTENTION,
        "fixed_mathematics": FIXED_MATHEMATICS,
        "reporting_methodology": METHODOLOGY,
        "independent_variable": "joint semantic identity grounding and matching query focus",
        "standard_status": (
            "developmental exploratory criteria encoded in executable checks; "
            "no independent preregistration artifact exists"
        ),
        "standards": [
            "the treatment directs more than half of measured competing-field activation to the intended field",
            "the intended-field share is higher under treatment than baseline",
            "the intended-versus-contrast margin is higher under treatment than baseline",
            "absolute activation in the competing field is lower under treatment than baseline",
            "all measured activations converge and same-process repetition is deterministic",
        ],
        "context": {
            "fixture_status": "authored development scenarios",
            "sample_size": {"scenarios": len(first), "probes": sum(len(item["probes"]) for item in first)},
            "shared_authorship_declared": True,
            "independent_review_contract": False,
            "held_out": False,
            "tuning_history": "no independent preregistration or frozen tuning history artifact",
            "compiler": {
                "tokenization": "lowercase whitespace split",
                "window_size": 2,
            },
            "activation_strategy": {
                "name": FIXED_MATHEMATICS,
                "damping": 0.85,
                "max_iterations": 100,
                "tolerance": 1e-6,
            },
            "runtime": runtime_identity(),
            "treatment_sequence": [
                "compile ambiguous corpus and activate surface query",
                "measure baseline context fields",
                "ground declared corpus occurrences and compile treatment corpus",
                "focus query onto matching governed identity",
                "measure treatment context fields",
                "compare paired outcomes and repeat in the same process",
            ],
            "missing_controls": [
                "corpus-grounding-only treatment",
                "query-focus-only treatment",
                "swapped or incorrect focus sham",
                "identity-preserving label control",
                "topology and edge-count control",
                "context-vocabulary and parameter sensitivity",
            ],
        },
        "intervention": {
            "performed_action": (
                "jointly replace declared ambiguous corpus occurrences with governed sense "
                "identities and focus each query onto the matching identity"
            ),
            "fixed": [
                "authored sentences apart from declared identity replacement",
                "transition-model compiler",
                "window size",
                "Personalized PageRank algorithm and settings",
                "context vocabularies",
                "metrics",
            ],
            "not_isolated": [
                "the separate effect of corpus grounding",
                "the separate effect of query focus",
                "semantic identity quality versus added topology",
            ],
        },
        "scenarios": first,
        "summary": {
            "scenario_count": len(first),
            "probe_count": sum(len(item["probes"]) for item in first),
            "supported_scenarios": supported_scenarios,
            "all_scenarios_supported": all_probes_supported,
            "deterministic": deterministic,
            "all_activations_converged": all_converged,
        },
        "conformity": {
            "judgment": "CONSISTENT" if all_probes_supported and deterministic and all_converged else "INCONSISTENT",
            "evidence_strength": "LOW",
            "criteria": {
                "all_directional_probe_checks_pass": all_probes_supported,
                "all_probe_margins_improve": all(
                    probe["checks"]["intended_versus_contrast_margin_improves"]
                    for scenario in first
                    for probe in scenario["probes"]
                ),
                "same_process_repetition_is_deterministic": deterministic,
                "all_activations_converged": all_converged,
            },
        },
        "claim_ladder": [
            {
                "level": "implementation fact",
                "claim": "both conditions use the same compiler and Personalized PageRank algorithm/settings",
                "status": "verified",
            },
            {
                "level": "fixture observation",
                "claim": "all six joint grounding-and-focus probes improved declared context selectivity and reduced competing-field activation",
                "status": "observed in authored fixtures",
            },
            {
                "level": "exploratory signal",
                "claim": "explicit sense identity plus matching query focus can produce a more discriminating activation field",
                "status": "early directional signal",
            },
            {
                "level": "representation hypothesis",
                "claim": "semantic identity enrichment generalizes across unseen language tasks",
                "status": "untested beyond authored fixtures",
            },
            {
                "level": "application hypothesis",
                "claim": "the activation effect improves routing or retrieval outcomes",
                "status": "untested",
            },
            {
                "level": "wider MML proposition",
                "claim": INTENTION,
                "status": "research intention, not established",
            },
        ],
        "artifact_identities": {
            "generator_sha256": sha256_file(GENERATOR_PATH),
            "kernel_sha256": sha256_file(KERNEL_PATH),
            "operational_flow_sha256": sha256_file(FLOW_PATH),
            "comparison_adapter_sha256": sha256_file(COMPARISON_PATH),
            "bank_fixture_sha256": sha256_file(FIXTURE_PATH),
            "methodology_sha256": sha256_file(METHODOLOGY_PATH),
        },
        "provenance": {
            "generator": str(GENERATOR_PATH.relative_to(ROOT)),
            "kernel": str(KERNEL_PATH.relative_to(ROOT)),
            "operational_flow": str(FLOW_PATH.relative_to(ROOT)),
            "comparison_adapter": str(COMPARISON_PATH.relative_to(ROOT)),
            "bank_fixture": str(FIXTURE_PATH.relative_to(ROOT)),
            "machine_result": str(RESULT_PATH.relative_to(ROOT)),
            "human_report": str(REPORT_PATH.relative_to(ROOT)),
            "methodology": str(METHODOLOGY_PATH.relative_to(ROOT)),
        },
        "evidence_boundary": (
            "Authored development scenarios for the joint semantic grounding-and-focus "
            "treatment only; not isolated evidence for grounding alone, not held-out evidence "
            "for richer meaning representation generally, and not evidence for MML hypotheses "
            "two or three."
        ),
    }
    return result


def markdown_report(result):
    summary = result["summary"]
    conformity = result["conformity"]["judgment"]
    evidence_strength = result["conformity"]["evidence_strength"]
    generated_date = result["generated_at"].split("T", 1)[0]
    convergence_records = []
    for scenario in result["scenarios"]:
        convergence_records.append(scenario["probes"][0]["convergence"]["baseline"])
        convergence_records.extend(
            probe["convergence"]["treatment"] for probe in scenario["probes"]
        )
    lines = [
        "# Semantic Representation Benchmark v1 — OSCARC Report", "",
        f"> **{result['intention']}**", "",
        "## Research intention", "", result["intention"], "",
        "## Hypothesis scope", "",
        "This report tests **MML Hypothesis 1: Representation** only:", "",
        "> Meaning represented explicitly and richly enough can make ordinary mathematics "
        "semantically useful.", "",
        "It does not test whether established knowledge can be compiled and reused more "
        "effectively than reconstruction at use time (**Hypothesis 2: Knowledge State "
        "Execution**), or whether combinations of reusable semantic coordinates create useful "
        "specificity and combinatorial coverage (**Hypothesis 3: Combinatorial Uniqueness**). "
        "Deterministic compilation and replay are controls in this experiment, not evidence "
        "for the whole triad.", "",
        "## Executive interpretation", "",
        f"The results are **{conformity.lower()}** with the local developmental expectation that "
        "jointly grounding ambiguous corpus occurrences and focusing the query onto the matching "
        "governed identity improves contextual selectivity while the compiler and activation "
        f"algorithm remain fixed. All {summary['probe_count']} probes across "
        f"{summary['scenario_count']} authored scenarios met the four developmental criteria, "
        "all activations converged, and same-process repetition passed. Evidence strength is "
        "**low** because these are small, "
        "authored development fixtures rather than held-out or independently assessed cases. "
        "The result is an early directional signal for the joint treatment; it does not isolate "
        "grounding from query focus and does not validate other richer representations, Knowledge "
        "State Execution, Combinatorial "
        "Uniqueness, or the general MML proposition.", "",
        "## O — Objective observation", "",
        f"On `{generated_date}`, benchmark `{result['benchmark_version']}` executed "
        f"{summary['scenario_count']} authored ambiguity scenarios containing "
        f"{summary['probe_count']} focused semantic-identity probes. The "
        "[machine-readable result](../../../benchmark/results/semantic-representation-v1.json) "
        "records baseline context activation from an ambiguous surface identity and grounded "
        "context activation from each governed identity.", "",
        "The observed scenarios were:", "",
    ]
    for scenario in result["scenarios"]:
        lines.append(
            f"- `{scenario['scenario_id']}` — {scenario['description']} "
            f"({scenario['sentence_count']} sentences; "
            f"{scenario['grounded_occurrence_count']} grounded ambiguous-word occurrences)"
        )
    lines.extend([
        "", "No causal interpretation is assigned to those observations in this section.", "",
        "## S — Standard, baseline, or reference model", "",
        "This is an A/B joint-treatment test. **A** is the ambiguous representation: one surface "
        "identity carries both meanings. **B** is the grounded representation: the same sentences "
        "contain separate governed identities and the query selects one of them. The exploratory "
        "expectation was that B would make the activation field more useful for distinguishing "
        "the intended context without changing the compiler or query mathematics.", "",
        "Here, *more useful* has one deliberately narrow operational meaning: of the activation "
        "that reaches the two declared competing context fields, a larger share should reach the "
        "intended field and less activation should leak into the competing field.", "",
        "Each probe was assessed against four developmental criteria:", "",
        "1. in B, more than 50% of the activation reaching the two measured context fields lands "
        "in the intended field;",
        "2. the intended-field share is higher in B than in A;",
        "3. the intended-versus-contrast margin is higher in B than in A;",
        "4. absolute activation leaking into the competing field is lower in B than in A.", "",
        "Convergence and same-process deterministic repetition were separate integrity requirements. "
        "No independent preregistration artifact exists, so these are developmental exploratory "
        "criteria rather than confirmatory standards. This version declared no minimum effect-size "
        "or statistical-significance threshold.", "",
        "## C — Context and chronology", "",
        f"The fixed algorithm contract was `{result['fixed_mathematics']}`. The independent variable "
        f"was `{result['independent_variable']}`. The same transition-model compiler and "
        "Personalized PageRank strategy were used in both conditions. The compiler uses a "
        "two-token co-occurrence window; activation uses damping `0.85`, at most `100` iterations, "
        "and L1 tolerance `1e-6`. The numerical operator is not fixed: its identities, dimensions, "
        "and transition entries change as the intended consequence of the representation treatment.", "",
        "```text",
        "authored sentences",
        "    -> A: ambiguous model + surface query",
        "    -> A context measurements",
        "    -> declared corpus grounding",
        "    -> B: grounded model + focused query",
        "    -> B context measurements",
        "    -> paired A/B comparison",
        "    -> deterministic rerun",
        "```", "",
        "The scenarios and context vocabularies are authored development fixtures. They are not "
        "held out, independently judged, or representative of general language. Missing controls "
        "include grounding-only, focus-only, swapped-focus, identity-preserving-label, topology, "
        "and context/parameter-sensitivity treatments.", "",
        "## A — Actions, interventions, or observed mechanisms", "",
        "Between A and B, the intervention replaced each declared occurrence of an ambiguous surface identity "
        "with its governed identity—for example, `bank` became `bank_river` or "
        "`bank_financial`. The query then targeted that identity. Sentences, compiler, window "
        "size, query strategy, damping, convergence tolerance, context definitions, and metrics remained fixed.", "",
        "The observed mechanism was matrix propagation from the selected identity through the "
        "compiled transition model. Because grounding and query focus change together, the design "
        "does not isolate either component, semantic identity quality versus added topology, or "
        "the proposition that every richer representation will help.", "",
        "## R — Result, effect, or measured outcome", "",
        "The transition model produces a normalized activation distribution: all identity "
        "weights together sum to 100%. A context value is the portion landing on the small set "
        "of words declared for that context. Because those raw portions depend on corpus size and "
        "context vocabulary, they are not meaningful as standalone scores.", "",
        "The report therefore interprets them as **context selectivity**: among activation reaching "
        "the two measured competing fields, what percentage reaches the intended field? A value "
        "above 50% favors the intended meaning. The A-to-B change is shown in percentage points.", "",
        "| Scenario | Focused meaning | A: intended share | B: intended share | Gain (percentage points) | Competing-field activation reduced? | Conformity |",
        "| --- | --- | ---: | ---: | ---: | --- | --- |",
    ])
    for scenario in result["scenarios"]:
        for probe in scenario["probes"]:
            lines.append(
                f"| {scenario['scenario_id']} | {probe['identity']} | "
                f"{probe['baseline_selectivity']:.1%} | {probe['grounded_selectivity']:.1%} | "
                f"{probe['selectivity_gain'] * 100:+.1f} | "
                f"{'yes' if probe['contrast_reduction'] > 0 else 'no'} | "
                f"{'PASS' if probe['supported'] else 'FAIL'} |"
            )
    lines.extend([
        "", "### Representation cost", "",
        "The compiler and activation algorithm are fixed, but enrichment changes the compiled "
        "operator. The structural cost observed for each scenario was:", "",
        "| Scenario | Identities A → B | Non-zero transitions A → B | Matrix bytes A → B | Grounded occurrences |",
        "| --- | ---: | ---: | ---: | ---: |",
    ])
    for scenario in result["scenarios"]:
        baseline = scenario["representation_cost"]["baseline"]
        treatment = scenario["representation_cost"]["treatment"]
        lines.append(
            f"| {scenario['scenario_id']} | {baseline['identity_count']} → "
            f"{treatment['identity_count']} | {baseline['nonzero_transition_count']} → "
            f"{treatment['nonzero_transition_count']} | {baseline['transition_bytes']} → "
            f"{treatment['transition_bytes']} | {scenario['grounded_occurrence_count']} |"
        )
    lines.extend([
        "", "These counts expose representational growth only. Authoring/review effort, "
        "compilation latency, query latency, memory outside the dense transition matrix, and "
        "energy were not measured.", "",
        "### Numerical integrity", "",
        f"All `{len(convergence_records)}` activation executions recorded for the first run converged. Iterations "
        f"ranged from `{min(item['iterations'] for item in convergence_records)}` to "
        f"`{max(item['iterations'] for item in convergence_records)}`; final L1 residuals ranged "
        f"from `{min(item['residual'] for item in convergence_records):.3e}` to "
        f"`{max(item['residual'] for item in convergence_records):.3e}`. Same-process repetition "
        f"was `{'PASS' if summary['deterministic'] else 'FAIL'}`.", "",
    ])
    selectivity_gains = [
        probe["selectivity_gain"]
        for item in result["scenarios"] for probe in item["probes"]
    ]
    gains_by_scenario = {
        item["scenario_id"]: [probe["selectivity_gain"] for probe in item["probes"]]
        for item in result["scenarios"]
    }
    bank_gains = gains_by_scenario["identity-bank"]
    compact_gains = [
        gain
        for scenario_id, gains in gains_by_scenario.items()
        if scenario_id != "identity-bank"
        for gain in gains
    ]
    lines.extend([
        "", f"All `{summary['probe_count']}/{summary['probe_count']}` probes passed because B "
        "favored the intended context, improved its intended-context share and margin over A, "
        "and reduced absolute activation in the competing context. The intended-context share increased by "
        f"between `{min(selectivity_gains) * 100:.1f}` and "
        f"`{max(selectivity_gains) * 100:.1f}` percentage "
        "points across the six probes. Same-process deterministic repetition was "
        f"`{'PASS' if summary['deterministic'] else 'FAIL'}`.", "",
        "`PASS` means directional conformity with these four criteria; it does not mean the "
        "effect is large enough for a production use case. This version has no practical "
        "significance threshold.", "",
        "### Exploratory secondary observation: evidence volume and gain", "",
        "The larger `bank` fixture contains 8 sentences and 5 grounded occurrences of the "
        "ambiguous word. Its two intended-context gains were "
        f"`{min(bank_gains) * 100:.1f}` and `{max(bank_gains) * 100:.1f}` percentage points. "
        "The `bass` and `crane` fixtures each contain only 6 sentences—3 for each meaning—and "
        "4 grounded occurrences. Their gains ranged from "
        f"`{min(compact_gains) * 100:.1f}` to `{max(compact_gains) * 100:.1f}` points.", "",
        "The richer bank fixture therefore shows a substantially clearer separation, while the "
        "two compact fixtures already show a positive gain. This is an observed association, not "
        "evidence that corpus size caused the larger gain: vocabulary, sentence topology, context "
        "balance, and connection strength also differ between scenarios.", "",
        "These paired outcomes are not population estimates or proof of comparable effects in "
        "unseen domains.", "",
        "## C — Comparative assessment and research conclusion", "",
        f"**Conformity judgment: `{conformity}`.** Every joint grounding-and-focus treatment directed a majority of "
        "the measured contextual activation to the intended field, increased that share relative "
        "to A, improved the intended-versus-contrast margin, reduced competing-field leakage, "
        "converged, and repeated deterministically in the "
        "same process.", "",
        f"**Evidence strength: `{evidence_strength}`.** The evidence consists of six authored "
        "probes with shared scenario and implementation authorship, no held-out cases, no "
        "independent review, and no inferential statistics. Within that boundary, the experiment "
        "is consistent with the claim that explicit sense identity plus matching query focus can "
        "make the same Personalized PageRank algorithm/settings produce a more discriminating "
        "contextual field in these fixtures. It is called more "
        "useful here because a query for one meaning yields less evidence from the competing "
        "meaning and a larger proportion from the intended one—a candidate mechanism aligned with, "
        "but not evidence of, improved sense-sensitive routing or retrieval.", "",
        "Synonymy, hierarchy, association, semantic roles, relation-specific matrices, and policy "
        "composition remain separate untested hypotheses.", "",
        "### Claims ladder", "",
        "| Level | Claim | Status |",
        "| --- | --- | --- |",
    ])
    for claim in result["claim_ladder"]:
        lines.append(f"| {claim['level']} | {claim['claim']} | {claim['status']} |")
    lines.extend([
        "", "The ladder prevents fixture-level activation observations from being promoted into "
        "application effectiveness or the wider MML proposition without separate evidence.", "",
        "## Recommendation and next step", "",
        "The next research phase should first freeze a v2 protocol before implementation changes. "
        "Its primary output should be a grounding × query-focus factorial suite over a compatible "
        "shared vocabulary, with grounding-only, focus-only, joint-treatment, swapped-focus sham, "
        "identity-preserving label, and topology/edge-count controls. This retires the principal "
        "v1 attribution uncertainty.", "",
        "The same frozen protocol should add held-out independently authored cases, context-word "
        "and sentence perturbations, leave-one-out stability, and window/damping sensitivity. "
        "Before results, it should jointly declare the minimum selectivity benefit and acceptable "
        "authoring, latency, memory, and energy costs. Only after attribution and "
        "robustness are established should an evidence-volume study test scaling, followed by "
        "separate routing or retrieval application outcomes.", "",
        "## Evidence boundary", "",
        result["evidence_boundary"], "",
        "This report follows [OSCARC methodology](../oscarc-methodology.md). The "
        "[machine-readable JSON artifact](../../../benchmark/results/semantic-representation-v1.json) "
        "remains authoritative for measurements, convergence, conformity inputs, artifact "
        "identities, and provenance.",
    ])
    return "\n".join(lines) + "\n"


def write_results(result, result_path=RESULT_PATH, report_path=REPORT_PATH):
    result_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    report_path.write_text(markdown_report(result), encoding="utf-8")


def stable_result(result):
    """Remove intentionally volatile fields before artifact comparison."""
    stable = json.loads(json.dumps(result))
    stable.pop("generated_at", None)
    return stable


def check_artifact_freshness(result, result_path=RESULT_PATH, report_path=REPORT_PATH):
    if not result_path.exists() or not report_path.exists():
        raise SystemExit("Semantic representation artifacts are missing; run with --write.")
    reference = json.loads(result_path.read_text(encoding="utf-8"))
    if stable_result(reference) != stable_result(result):
        raise SystemExit("Semantic representation JSON is stale; regenerate with --write.")
    if report_path.read_text(encoding="utf-8") != markdown_report(reference):
        raise SystemExit("Semantic representation report is stale; regenerate with --write.")


def check_result(result):
    summary = result["summary"]
    if not summary["deterministic"]:
        raise SystemExit("Semantic representation benchmark is not deterministic.")
    if not summary["all_scenarios_supported"]:
        raise SystemExit("One or more semantic representation scenarios are not supported.")
    if not summary["all_activations_converged"]:
        raise SystemExit("One or more semantic representation activations did not converge.")
    if not all(result["conformity"]["criteria"].values()):
        raise SystemExit("One or more semantic representation conformity criteria failed.")


def main():
    parser = argparse.ArgumentParser(description="Run the semantic representation benchmark.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="Write JSON and Markdown results.")
    mode.add_argument("--check", action="store_true", help="Run checks without changing results.")
    args = parser.parse_args()
    result = run_benchmark()
    check_result(result)
    if args.write:
        write_results(result)
    else:
        check_artifact_freshness(result)
    print(markdown_report(result))


if __name__ == "__main__":
    main()
