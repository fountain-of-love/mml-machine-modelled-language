import math
import tempfile
import unittest
from pathlib import Path

import benchmark
from mml_update_demo import run_update_demo
from mml_trace_demo import build_trace_record


class MetricTests(unittest.TestCase):
    def test_hand_calculated_metrics(self):
        ranked = ["A", "B", "C", "D"]
        relevance = {"A": 3, "B": 0, "C": 1, "D": 0}
        self.assertAlmostEqual(benchmark.precision_at_k(ranked, relevance, 2), 0.5)
        self.assertAlmostEqual(benchmark.recall_at_k(ranked, relevance, 3), 1.0)
        self.assertAlmostEqual(benchmark.reciprocal_rank(ranked, relevance), 1.0)
        expected = (7 + 1 / math.log2(4)) / (7 + 1 / math.log2(3))
        self.assertAlmostEqual(benchmark.ndcg_at_k(ranked, relevance, 4), expected)


class RetrievalDiagnosticTests(unittest.TestCase):
    def test_fixture_integrity_and_balance(self):
        validated = benchmark.validate_benchmark()
        self.assertEqual(len(validated["documents"]), 50)
        self.assertEqual(len(validated["queries"]), 6)

    def test_only_focused_systems_are_active(self):
        self.assertEqual(
            benchmark.SYSTEMS,
            (
                "lexical_overlap",
                "tfidf_cosine",
                "mml_cooccurrence",
                "mml_typed",
                "mml_lexical_hybrid",
            ),
        )

    def test_hybrid_formula_is_reproducible(self):
        validated = benchmark.validate_benchmark()
        rankings = benchmark.rank_inputs(validated["documents"], validated["queries"])
        query = validated["queries"][0]
        document = next(item for item in validated["documents"] if item["tier"] == query["tier"])
        lexical = benchmark.lexical_score(query["terms"], document["text"])
        typed = benchmark.mml_score(query, document["text"], typed=True)
        hybrid = next(
            item["score"] for item in rankings["mml_lexical_hybrid"][query["id"]]
            if item["document_id"] == document["id"]
        )
        self.assertAlmostEqual(hybrid, typed * (0.2 + 0.8 * lexical))

    def test_rankings_are_deterministic(self):
        validated = benchmark.validate_benchmark()
        first = benchmark.rank_inputs(validated["documents"], validated["queries"])
        second = benchmark.rank_inputs(validated["documents"], validated["queries"])
        self.assertEqual(first, second)

    def test_typed_and_cooccurrence_are_independently_named(self):
        result = benchmark.run_benchmark()
        self.assertIn("mml_cooccurrence", result["metrics"]["macro"])
        self.assertIn("mml_typed", result["metrics"]["macro"])

    def test_report_has_no_project_acceptance_verdict(self):
        report = benchmark.markdown_report(benchmark.run_benchmark())
        self.assertNotIn("Improvement acceptance", report)
        self.assertNotIn("infrastructure_readiness", report)
        self.assertIn("not an acceptance verdict", report)

    def test_diagnostic_clears_absolute_floors(self):
        result = benchmark.run_benchmark()
        self.assertTrue(result["checks"]["quality_floor"])

    def test_regressed_result_cannot_silently_replace_reference(self):
        result = benchmark.run_benchmark()
        result["checks"]["regression"] = False
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            with self.assertRaisesRegex(SystemExit, "Refusing to replace"):
                benchmark.write_checked_results(result, output)
            self.assertFalse((output / "v1.json").exists())

    def test_regression_override_is_explicit_and_writes(self):
        result = benchmark.run_benchmark()
        result["checks"]["regression"] = False
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            benchmark.write_checked_results(result, output, accept_regression=True)
            self.assertTrue((output / "v1.json").exists())
            self.assertTrue((output / "v1.md").exists())

    def test_default_outputs_separate_machine_reference_and_human_report(self):
        self.assertEqual(benchmark.RESULTS_DIR, benchmark.ROOT / "benchmark" / "results")
        self.assertEqual(benchmark.REPORTS_DIR, benchmark.ROOT / "docs" / "benchmark" / "results")


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
