import tempfile
import unittest
from pathlib import Path

from direct_combinatorial_intersection_experiment import (
    check_result,
    markdown_report,
    run_experiment,
    write_results,
)


class DirectCombinatorialIntersectionExperimentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = run_experiment()

    def test_experiment_is_atomic_and_physical_only(self):
        self.assertEqual(self.result["experiment_id"], "experiment-3.1-direct-combinatorial-intersection-v1")
        self.assertNotIn("contexts", self.result)
        self.assertNotIn("legal", self.result["claim_scope"].lower().split("no legal")[0])
        self.assertNotIn("cross_level", self.result["treatments"])
        self.assertNotIn("contrasts", self.result["treatments"])
        self.assertEqual(self.result["fixture"]["concept_count"], 31)

    def test_claim_is_locally_consistent_but_generalization_untested(self):
        self.assertEqual(self.result["conformity"]["judgment"], "LOCALLY_CONSISTENT")
        self.assertTrue(all(self.result["conformity"]["criteria"].values()))
        self.assertEqual(self.result["generalization"]["status"], "UNTESTED")

    def test_independent_redundant_and_invalid_treatments_are_complete(self):
        treatments = self.result["treatments"]
        self.assertEqual(len(treatments["independent"]), 8)
        self.assertEqual(len(treatments["redundant"]), 2)
        self.assertEqual(len(treatments["invalid"]), 3)
        self.assertTrue(all(item["count"] == 24 for item in treatments["permutations"]))
        self.assertTrue(all(len(item["leave_one_out"]) == 4 for item in treatments["ablations"]))

    def test_report_has_claim_specific_oscarc_boundary(self):
        report = markdown_report(self.result)
        self.assertIn("Direct Combinatorial Intersection", report)
        self.assertIn("LOCALLY_CONSISTENT", report)
        self.assertIn("Generalization is `UNTESTED`", report)
        self.assertIn("does not test legal qualification", report)
        for section in ("## O —", "## S —", "## C — Context", "## A —", "## R —", "## C — Comparative"):
            self.assertIn(section, report)

    def test_checked_in_artifacts_are_fresh_and_check_is_nonmutating(self):
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
