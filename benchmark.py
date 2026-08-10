"""Benchmark whether richer semantic identity improves fixed matrix execution.

The benchmark deliberately reuses the Words Carry Weight experiment. Every
scenario runs the same compiler and Personalized PageRank query strategy twice:
first over ambiguous surface identities and then over governed identities. The
representation is the independent variable; the mathematics remains fixed.
"""

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from activate_grounded_focus import PersonalizedPageRankActivationStrategy
from experiment_fixture import load_experiment
from representation_comparison import compare_representations


ROOT = Path(__file__).parent
RESULT_PATH = ROOT / "benchmark" / "results" / "semantic-representation-v1.json"
REPORT_PATH = ROOT / "docs" / "benchmark" / "results" / "semantic-representation-v1.md"
BENCHMARK_VERSION = "semantic-representation-v1"
INTENTION = "Richer meaning representation can make established mathematics produce more useful results."
FIXED_MATHEMATICS = "converged-personalized-pagerank-v1"
METHODOLOGY = "OSCARC-v1"


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
    """Measure the effect of grounding while keeping query mathematics fixed."""
    strategy = strategy or PersonalizedPageRankActivationStrategy()
    comparison = compare_representations(scenario.experiment, strategy)
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
        }
        probe["checks"] = {
            "grounded_field_favors_intended_context": probe["grounded_selectivity"] > 0.5,
            "intended_context_share_improves": probe["selectivity_gain"] > 0,
            "contrast_reduces": probe["contrast_reduction"] > 0,
        }
        probe["supported"] = all(probe["checks"].values())
        probes.append(probe)
    return {
        "scenario_id": scenario.scenario_id,
        "description": scenario.description,
        "surface_identity": scenario.experiment["original_query"],
        "sentence_count": len(scenario.experiment["sentences"]),
        "grounded_occurrence_count": len(scenario.experiment["semantic_groundings"]),
        "probes": probes,
        "supported": all(probe["supported"] for probe in probes),
    }


def run_benchmark():
    """Execute every scenario twice and fail closed on nondeterministic behavior."""
    scenarios = benchmark_scenarios()
    first = [evaluate_scenario(scenario) for scenario in scenarios]
    second = [evaluate_scenario(scenario) for scenario in scenarios]
    deterministic = first == second
    supported_scenarios = sum(result["supported"] for result in first)
    result = {
        "benchmark_version": BENCHMARK_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "intention": INTENTION,
        "fixed_mathematics": FIXED_MATHEMATICS,
        "reporting_methodology": METHODOLOGY,
        "independent_variable": "semantic identity grounding and query focus",
        "scenarios": first,
        "summary": {
            "scenario_count": len(first),
            "probe_count": sum(len(item["probes"]) for item in first),
            "supported_scenarios": supported_scenarios,
            "all_scenarios_supported": supported_scenarios == len(first),
            "deterministic": deterministic,
        },
        "evidence_boundary": (
            "Authored development scenarios for semantic identity only; not held-out "
            "evidence for every form of richer meaning representation."
        ),
    }
    return result


def markdown_report(result):
    summary = result["summary"]
    conformity = "CONSISTENT" if summary["all_scenarios_supported"] else "INCONSISTENT"
    evidence_strength = "LOW"
    generated_date = result["generated_at"].split("T", 1)[0]
    lines = [
        "# Semantic Representation Benchmark v1 — OSCARC Report", "",
        f"> **{result['intention']}**", "",
        "## Executive interpretation", "",
        f"The results are **{conformity.lower()}** with the local expectation that grounding "
        "an ambiguous word into governed semantic identities improves contextual focus while "
        f"the mathematics remains fixed. All {summary['probe_count']} probes across "
        f"{summary['scenario_count']} authored scenarios met the three declared criteria, and "
        "deterministic replay passed. Evidence strength is **low** because these are small, "
        "authored development fixtures rather than held-out or independently assessed cases. "
        "The result supports semantic identity enrichment in this bounded experiment; it does "
        "not validate other richer representations or the general MML proposition.", "",
        "## O — Objective observation", "",
        f"On `{generated_date}`, benchmark `{result['benchmark_version']}` executed "
        f"{summary['scenario_count']} authored ambiguity scenarios containing "
        f"{summary['probe_count']} focused semantic-identity probes. The machine-readable result "
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
        "This is an A/B representation test. **A** is the ambiguous representation: one surface "
        "identity carries both meanings. **B** is the grounded representation: the same sentences "
        "contain separate governed identities and the query selects one of them. The local "
        "expectation was that B would make the activation field more useful for distinguishing "
        "the intended context without changing the compiler or query mathematics.", "",
        "Here, *more useful* has one deliberately narrow operational meaning: of the activation "
        "that reaches the two declared competing context fields, a larger share should reach the "
        "intended field and less activation should leak into the competing field.", "",
        "Each probe was required to satisfy three declared criteria:", "",
        "1. in B, more than 50% of the activation reaching the two measured context fields lands "
        "in the intended field;",
        "2. the intended-field share is higher in B than in A;",
        "3. absolute activation leaking into the competing field is lower in B than in A.", "",
        "Deterministic replay was a separate integrity requirement. This development version "
        "declared no minimum effect-size or statistical-significance threshold.", "",
        "## C — Context and chronology", "",
        f"The fixed mathematics was `{result['fixed_mathematics']}`. The independent variable "
        f"was `{result['independent_variable']}`. The same transition-model compiler and "
        "Personalized PageRank strategy were used in both conditions.", "",
        "```text",
        "authored sentences",
        "    -> A: ambiguous model + surface query",
        "    -> A context measurements",
        "    -> identity grounding only",
        "    -> B: grounded model + focused query",
        "    -> B context measurements",
        "    -> paired A/B comparison",
        "    -> deterministic rerun",
        "```", "",
        "The scenarios and context vocabularies are authored development fixtures. They are not "
        "held out, independently judged, or representative of general language.", "",
        "## A — Actions, interventions, or observed mechanisms", "",
        "Between A and B, the intervention replaced each declared occurrence of an ambiguous surface identity "
        "with its governed identity—for example, `bank` became `bank_river` or "
        "`bank_financial`. The query then targeted that identity. Sentences, compiler, window "
        "size, query strategy, damping, convergence, context definitions, and metrics remained fixed.", "",
        "The observed mechanism was matrix propagation from the selected identity through the "
        "compiled transition model. The design isolates identity grounding within these fixtures; "
        "it does not establish that every richer representation will help.", "",
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
        "favored the intended context, improved its intended-context share over A, and reduced "
        "absolute activation in the competing context. The intended-context share increased by "
        f"between `{min(selectivity_gains) * 100:.1f}` and "
        f"`{max(selectivity_gains) * 100:.1f}` percentage "
        "points across the six probes. Deterministic replay was "
        f"`{'PASS' if summary['deterministic'] else 'FAIL'}`.", "",
        "`PASS` means directional conformity with these three criteria; it does not mean the "
        "effect is large enough for a production use case. This version has no practical "
        "significance threshold.", "",
        "### Secondary observation: evidence volume and gain", "",
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
        f"**Conformity judgment: `{conformity}`.** Every B representation directed a majority of "
        "the measured contextual activation to the intended field, increased that share relative "
        "to A, reduced competing-field leakage, and replayed deterministically.", "",
        f"**Evidence strength: `{evidence_strength}`.** The evidence consists of six authored "
        "probes with shared scenario and implementation authorship, no held-out cases, no "
        "independent review, and no inferential statistics. Within that boundary, the experiment "
        "is consistent with the claim that richer identity representation can make unchanged "
        "Personalized PageRank produce a more discriminating contextual field. It is called more "
        "useful here because a query for one meaning yields less evidence from the competing "
        "meaning and a larger proportion from the intended one—the exact behavior needed for "
        "sense-sensitive routing or retrieval.", "",
        "Synonymy, hierarchy, association, semantic roles, relation-specific matrices, and policy "
        "composition remain separate untested hypotheses.", "",
        "## Recommendation and next step", "",
        "First, run a controlled evidence-volume experiment within the same ambiguity scenario. "
        "Build matched A/B corpora with progressively more sentences per meaning, repeat each "
        "level across several independently authored sentence sets, and plot intended-context "
        "gain and competing-field leakage against sentence and occurrence count. This will test "
        "whether enrichment benefit grows with evidence, appears immediately, or reaches a "
        "saturation point while holding vocabulary and topology as stable as possible.", "",
        "Then freeze a held-out identity suite whose scenarios and expected directions are authored "
        "before implementation inspection and repeat this OSCARC analysis. Next, implement a "
        "topology-controlled typed-relation suite with relation-label permutation and edge-count "
        "controls to test relation meaning rather than additional connectivity.", "",
        "## Evidence boundary", "",
        result["evidence_boundary"], "",
        "This report follows [OSCARC methodology](../oscarc-methodology.md). The JSON artifact "
        "remains authoritative for recorded measurements.",
    ])
    return "\n".join(lines) + "\n"


def write_results(result, result_path=RESULT_PATH, report_path=REPORT_PATH):
    result_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    report_path.write_text(markdown_report(result), encoding="utf-8")


def check_result(result):
    summary = result["summary"]
    if not summary["deterministic"]:
        raise SystemExit("Semantic representation benchmark is not deterministic.")
    if not summary["all_scenarios_supported"]:
        raise SystemExit("One or more semantic representation scenarios are not supported.")


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
    print(markdown_report(result))


if __name__ == "__main__":
    main()
