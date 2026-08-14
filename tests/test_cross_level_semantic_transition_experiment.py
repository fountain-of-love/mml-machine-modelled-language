import tempfile
import unittest
from pathlib import Path

from experiments.combinatorial_uniqueness.cross_level_transition_benchmark import (
    check_result,
    markdown_report,
    run_experiment,
    write_results,
)


class CrossLevelSemanticTransitionExperimentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = run_experiment()

    def test_claim_is_consistent_and_generalization_remains_untested(self):
        self.assertEqual(self.result["conformity"]["judgment"], "CONSISTENT")
        self.assertTrue(all(self.result["conformity"]["criteria"].values()))
        self.assertEqual(self.result["generalization"]["status"], "UNTESTED")

    def test_all_three_transitions_and_flat_controls_are_recorded(self):
        self.assertEqual(self.result["results"]["probe_count"], 3)
        self.assertEqual(self.result["results"]["stage_count"], 6)
        self.assertEqual(self.result["results"]["stage_resolution_rate"], 1.0)
        self.assertEqual(self.result["results"]["flat_control_non_resolution_rate"], 1.0)

    def test_report_preserves_post_failure_evidence_boundary(self):
        report = markdown_report(self.result)
        self.assertIn("CONSISTENT", report)
        self.assertIn("authored after observing the original failure", report)
        self.assertIn("does not demonstrate automatic scope discovery", report)

    def test_artifacts_are_fresh_and_check_is_nonmutating(self):
        check_result(self.result)
        with tempfile.TemporaryDirectory() as directory:
            result_path = Path(directory) / "result.json"
            report_path = Path(directory) / "report.md"
            write_results(self.result, result_path, report_path)
            before = (result_path.read_bytes(), report_path.read_bytes())
            check_result(self.result, result_path, report_path)
            self.assertEqual(before, (result_path.read_bytes(), report_path.read_bytes()))


if __name__ == "__main__":
    unittest.main()
