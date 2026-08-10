import tempfile
import unittest
from pathlib import Path

import benchmark
import retrieval_benchmark
from elaborations.mml_update_demo import run_update_demo
from elaborations.mml_trace_demo import build_trace_record


class RetrievalMetricTests(unittest.TestCase):
    def test_hand_calculated_metrics(self):
        ranked = ["A", "B", "C", "D"]
        relevance = {"A": 3, "B": 0, "C": 1, "D": 0}
        import math
        self.assertAlmostEqual(retrieval_benchmark.precision_at_k(ranked, relevance, 2), 0.5)
        self.assertAlmostEqual(retrieval_benchmark.recall_at_k(ranked, relevance, 3), 1.0)
        self.assertAlmostEqual(retrieval_benchmark.reciprocal_rank(ranked, relevance), 1.0)
        expected = (7 + 1 / math.log2(4)) / (7 + 1 / math.log2(3))
        self.assertAlmostEqual(retrieval_benchmark.ndcg_at_k(ranked, relevance, 4), expected)


class SemanticRepresentationBenchmarkTests(unittest.TestCase):
    def test_scenarios_reuse_operational_words_carry_weight_flow(self):
        scenarios = benchmark.benchmark_scenarios()
        self.assertGreaterEqual(len(scenarios), 3)
        self.assertTrue(all(scenario.experiment["focused_queries"] for scenario in scenarios))

    def test_joint_grounding_and_focus_treatment_improves_every_declared_probe(self):
        result = benchmark.run_benchmark()
        self.assertTrue(result["summary"]["all_scenarios_supported"])
        for scenario in result["scenarios"]:
            self.assertGreater(scenario["sentence_count"], 0)
            self.assertGreater(scenario["grounded_occurrence_count"], 0)
            for probe in scenario["probes"]:
                self.assertGreater(probe["margin_improvement"], 0)
                self.assertTrue(
                    probe["checks"]["intended_versus_contrast_margin_improves"]
                )
                self.assertGreater(probe["contrast_reduction"], 0)
                self.assertGreater(probe["grounded_selectivity"], 0.5)
                self.assertGreater(probe["selectivity_gain"], 0)
                self.assertTrue(probe["convergence"]["baseline"]["converged"])
                self.assertTrue(probe["convergence"]["treatment"]["converged"])

    def test_benchmark_is_deterministic(self):
        first = benchmark.run_benchmark()
        second = benchmark.run_benchmark()
        self.assertEqual(first["scenarios"], second["scenarios"])
        self.assertTrue(first["summary"]["deterministic"])
        self.assertTrue(first["summary"]["all_activations_converged"])

    def test_machine_companion_preserves_modern_oscarc_contract(self):
        result = benchmark.run_benchmark()
        self.assertIn("joint semantic identity grounding", result["independent_variable"])
        self.assertIn("standards", result)
        self.assertIn("context", result)
        self.assertIn("intervention", result)
        self.assertIn("conformity", result)
        self.assertIn("claim_ladder", result)
        self.assertIn("artifact_identities", result)
        self.assertIn("provenance", result)
        self.assertTrue(all(result["conformity"]["criteria"].values()))
        self.assertTrue(result["conformity"]["criteria"]["all_probe_margins_improve"])
        self.assertIn("architecture", result["context"]["runtime"])
        self.assertIn("blas", result["context"]["runtime"])
        for scenario in result["scenarios"]:
            cost = scenario["representation_cost"]
            self.assertGreater(cost["delta"]["identity_count"], 0)
            self.assertGreater(cost["delta"]["nonzero_transition_count"], 0)
            self.assertGreater(cost["delta"]["transition_bytes"], 0)

    def test_checked_in_semantic_artifacts_are_fresh(self):
        benchmark.check_artifact_freshness(benchmark.run_benchmark())

    def test_report_leads_with_project_intention_and_evidence_boundary(self):
        report = benchmark.markdown_report(benchmark.run_benchmark())
        self.assertIn(benchmark.INTENTION, report)
        self.assertIn("O — Objective observation", report)
        self.assertIn("S — Standard, baseline, or reference model", report)
        self.assertIn("C — Context and chronology", report)
        self.assertIn("A — Actions, interventions, or observed mechanisms", report)
        self.assertIn("R — Result, effect, or measured outcome", report)
        self.assertIn("C — Comparative assessment and research conclusion", report)
        self.assertIn("Evidence strength", report)
        self.assertIn("A: intended share", report)
        self.assertIn("B: intended share", report)
        self.assertIn("what percentage reaches the intended field", report)
        self.assertIn("Exploratory secondary observation: evidence volume and gain", report)
        self.assertIn("observed association, not evidence that corpus size caused", report)
        self.assertIn("Claims ladder", report)
        self.assertIn("does not isolate either component", report)
        self.assertIn("Representation cost", report)
        self.assertIn("Numerical integrity", report)
        self.assertIn("Evidence boundary", report)


class RetrievalDiagnosticTests(unittest.TestCase):
    def test_fixture_integrity_and_balance(self):
        validated = retrieval_benchmark.validate_benchmark()
        self.assertEqual(len(validated["documents"]), 50)
        self.assertEqual(len(validated["queries"]), 6)

    def test_only_focused_systems_are_active(self):
        self.assertEqual(
            retrieval_benchmark.SYSTEMS,
            (
                "lexical_overlap",
                "tfidf_cosine",
                "mml_cooccurrence",
                "mml_typed",
                "mml_lexical_hybrid",
            ),
        )

    def test_hybrid_formula_is_reproducible(self):
        validated = retrieval_benchmark.validate_benchmark()
        rankings = retrieval_benchmark.rank_inputs(validated["documents"], validated["queries"])
        query = validated["queries"][0]
        document = next(item for item in validated["documents"] if item["tier"] == query["tier"])
        lexical = retrieval_benchmark.lexical_score(query["terms"], document["text"])
        typed = retrieval_benchmark.mml_score(query, document["text"], typed=True)
        hybrid = next(
            item["score"] for item in rankings["mml_lexical_hybrid"][query["id"]]
            if item["document_id"] == document["id"]
        )
        self.assertAlmostEqual(hybrid, typed * (0.2 + 0.8 * lexical))

    def test_rankings_are_deterministic(self):
        validated = retrieval_benchmark.validate_benchmark()
        first = retrieval_benchmark.rank_inputs(validated["documents"], validated["queries"])
        second = retrieval_benchmark.rank_inputs(validated["documents"], validated["queries"])
        self.assertEqual(first, second)

    def test_typed_and_cooccurrence_are_independently_named(self):
        result = retrieval_benchmark.run_benchmark()
        self.assertIn("mml_cooccurrence", result["metrics"]["macro"])
        self.assertIn("mml_typed", result["metrics"]["macro"])

    def test_report_has_no_project_acceptance_verdict(self):
        report = retrieval_benchmark.markdown_report(retrieval_benchmark.run_benchmark())
        self.assertNotIn("Improvement acceptance", report)
        self.assertNotIn("infrastructure_readiness", report)
        self.assertIn("not an acceptance verdict", report)

    def test_diagnostic_clears_absolute_floors(self):
        result = retrieval_benchmark.run_benchmark()
        self.assertTrue(result["checks"]["quality_floor"])

    def test_regressed_result_cannot_silently_replace_reference(self):
        result = retrieval_benchmark.run_benchmark()
        result["checks"]["regression"] = False
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            with self.assertRaisesRegex(SystemExit, "Refusing to replace"):
                retrieval_benchmark.write_checked_results(result, output)
            self.assertFalse((output / "v1.json").exists())

    def test_regression_override_is_explicit_and_writes(self):
        result = retrieval_benchmark.run_benchmark()
        result["checks"]["regression"] = False
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            retrieval_benchmark.write_checked_results(result, output, accept_regression=True)
            self.assertTrue((output / "v1.json").exists())
            self.assertTrue((output / "v1.md").exists())

    def test_default_outputs_separate_machine_reference_and_human_report(self):
        self.assertEqual(retrieval_benchmark.RESULTS_DIR, retrieval_benchmark.ROOT / "benchmark" / "results")
        self.assertEqual(retrieval_benchmark.REPORTS_DIR, retrieval_benchmark.ROOT / "docs" / "benchmark" / "results")


class EvolutionDemoTests(unittest.TestCase):
    def test_update_is_descriptive_and_reversible(self):
        result = run_update_demo()
        self.assertTrue(result["snapshot_changed"])
        self.assertTrue(result["rollback_snapshot_exact"])
        self.assertTrue(result["rollback_ranking_exact"])
        self.assertIn("no locality verdict", result["purpose"])

    def test_single_trace_connects_source_execution_and_rollback(self):
        trace = build_trace_record()
        self.assertEqual(trace["representation"]["evidence"]["id"],
                         trace["representation"]["proposed_relation"]["evidence_ids"][0])
        self.assertNotEqual(trace["evolution"]["score_delta"], 0.0)
        self.assertTrue(trace["evolution"]["new_paths"])
        self.assertTrue(all(trace["rollback"].values()))
        self.assertFalse(trace["limitations"]["representative_coverage"])


if __name__ == "__main__":
    unittest.main()
