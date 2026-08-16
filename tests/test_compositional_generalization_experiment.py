import tempfile
import unittest
from pathlib import Path

from experiments.combinatorial_uniqueness.compositional_generalization_benchmark import (
    REPORT_PATH,
    RESULT_PATH,
    check_result,
    markdown_report,
    run_experiment,
    write_results,
)


class CompositionalGeneralizationExperimentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = run_experiment()

    def test_leakage_contract_is_strict_and_complete(self):
        audit = self.result["leakage_audit"]
        self.assertTrue(audit["passed"])
        self.assertEqual(audit["complete_signature_overlap_count"], 0)
        self.assertEqual(audit["materialized_test_signature_leaks"], [])
        self.assertEqual(audit["stored_relation_arity"], 2)
        self.assertFalse(audit["compiled_entity_identities_retained"])
        self.assertFalse(audit["compiled_complete_signatures_retained"])

    def test_all_treatments_widths_and_targets_are_recorded_compactly(self):
        self.assertEqual(len(self.result["treatments"]), 6)
        self.assertEqual(len(self.result["aggregate_by_k"]), 6 * 20)
        self.assertEqual(len(self.result["target_traces"]), 64)
        for trace in self.result["target_traces"]:
            self.assertEqual(len(trace["ordered_query_coordinates"]), 20)
            self.assertEqual(set(trace["outcomes"]), set(self.result["treatments"]))
            self.assertTrue(all(len(item["target_ranks"]) == 20 for item in trace["outcomes"].values()))

    def test_negative_comparative_result_is_preserved(self):
        comparison = self.result["comparative_assessment"]
        self.assertEqual(comparison["scaling_claim_status"], "NOT_SUPPORTED_BY_THIS_FIXTURE")
        self.assertEqual(comparison["maximum_mml_top_1_advantage"], 0.0)
        self.assertFalse(comparison["mml_has_distinctive_accuracy_advantage"])
        self.assertEqual(self.result["conformity"]["judgment"], "EXECUTION_CONFORMANT")

    def test_report_leads_with_the_scientific_limitation(self):
        report = markdown_report(self.result)
        self.assertIn("NOT_SUPPORTED_BY_THIS_FIXTURE", report)
        self.assertIn("does not provide distinctive evidence for MML", report)
        self.assertIn("realizes only `256`", report)
        self.assertIn("soft intersection outperforms exact or additive controls | not observed", report)

    def test_checked_in_artifacts_are_fresh(self):
        check_result(self.result, RESULT_PATH, REPORT_PATH)

    def test_write_and_check_are_consistent(self):
        with tempfile.TemporaryDirectory() as directory:
            result_path = Path(directory) / "result.json"
            report_path = Path(directory) / "report.md"
            write_results(self.result, result_path, report_path)
            check_result(self.result, result_path, report_path)


if __name__ == "__main__":
    unittest.main()
