import tempfile
import unittest
from pathlib import Path

from governed_legal_qualification_experiment import (
    check_result,
    markdown_report,
    run_experiment,
    write_results,
)


class GovernedLegalQualificationExperimentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = run_experiment()

    def test_experiment_is_atomic_and_excludes_cross_level_transition(self):
        self.assertEqual(self.result["experiment_id"], "experiment-3.2-governed-legal-qualification-v1")
        self.assertNotIn("cross_level", self.result["treatments"])
        self.assertNotIn("physical", self.result["claim_scope"].lower().split("no physical")[0])
        self.assertEqual(self.result["fixture"]["concept_count"], 33)

    def test_claim_is_locally_consistent_but_generalization_untested(self):
        self.assertEqual(self.result["conformity"]["judgment"], "LOCALLY_CONSISTENT")
        self.assertTrue(all(self.result["conformity"]["criteria"].values()))
        self.assertEqual(self.result["generalization"]["status"], "UNTESTED")

    def test_direct_contrast_and_unsupported_treatments_are_complete(self):
        treatments = self.result["treatments"]
        self.assertEqual(len(treatments["independent"]), 12)
        self.assertEqual(len(treatments["redundant"]), 3)
        self.assertEqual(len(treatments["unsupported"]), 3)
        self.assertEqual(len(treatments["contrasts"]), 1)
        self.assertTrue(all(item["count"] == 24 for item in treatments["permutations"]))
        self.assertTrue(all(len(item["leave_one_out"]) == 4 for item in treatments["ablations"]))

    def test_unsupported_information_remains_insufficient(self):
        self.assertEqual(self.result["results"]["unsupported_non_resolution_rate"], 1.0)
        self.assertTrue(all(
            probe["status"] == "UNRESOLVED" and probe["declared_expectation"]["matches"]
            for probe in self.result["treatments"]["unsupported"]
        ))

    def test_report_is_claim_specific_and_non_adjudicative(self):
        report = markdown_report(self.result)
        self.assertIn("Governed Legal Qualification", report)
        self.assertIn("LOCALLY_CONSISTENT", report)
        self.assertIn("does not test cross-level transition", report)
        self.assertIn("does not establish facts", report.lower())

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
