import json
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from experiments.combinatorial_uniqueness.combined_benchmark import (
    audit_no_bespoke_primitives, check_result, markdown_report, run_experiment, write_results,
)
from experiments.combinatorial_uniqueness.fixture import load_experiment_fixture
from src.combinatorial_uniqueness.combinatorial_uniqueness_flow import CombinatorialUniquenessFlow


class CombinatorialUniquenessExperimentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = run_experiment()

    def test_both_contexts_use_one_policy_and_kernel_contract(self):
        self.assertEqual(len(self.result["contexts"]), 2)
        policy = self.result["diagnostic_policy"]
        self.assertTrue(policy["policy_id"].endswith("-v1"))
        for context in self.result["contexts"]:
            for probe in context["treatments"]["independent"]:
                self.assertEqual(probe["diagnostic_policy"], policy)

    def test_all_four_constraint_permutations_and_ablations_are_present(self):
        for context in self.result["contexts"]:
            for permutation in context["treatments"]["permutations"]:
                self.assertEqual(permutation["count"], 24)
                self.assertTrue(permutation["all_fields_equal"])
            for ablation in context["treatments"]["ablations"]:
                self.assertEqual(len(ablation["leave_one_out"]), 4)

    def test_controls_and_legal_qualification_treatments_are_recorded(self):
        for context in self.result["contexts"]:
            for probe in context["treatments"]["independent"]:
                self.assertIn("additive_control", probe)
                self.assertIn("hard_reference", probe)
        legal = self.result["contexts"][1]["treatments"]
        self.assertTrue(legal["cross_level"])
        self.assertTrue(legal["contrasts"])

    def test_structural_information_is_explicitly_an_authored_control(self):
        points = self.result["suite_results"]["specificity_curve"]
        self.assertTrue(points)
        prefix = self.result["contexts"][0]["treatments"]["independent"][0]["prefixes"][0]
        self.assertIn("not a kernel outcome", prefix["structural_information_role"])

    def test_serialized_prefix_distinguishes_top_k_mass_from_concentration(self):
        prefix = self.result["contexts"][0]["treatments"]["independent"][0]["prefixes"][0]
        self.assertEqual(prefix["top_k"], 3)
        self.assertGreater(prefix["top_k_mass"], prefix["concentration"])
        self.assertAlmostEqual(
            prefix["top_k_mass"],
            sum(sorted(prefix["candidate_values"], reverse=True)[:prefix["top_k"]]),
        )

    def test_mechanism_governance_and_overall_rates_are_separate(self):
        rates = self.result["suite_results"]["outcome_rates"]
        self.assertIn("mechanism_resolution", rates)
        self.assertIn("governance_resolution", rates)
        self.assertIn("overall_resolution", rates)
        self.assertEqual(rates["unsupported_non_resolution"], 1.0)
        self.assertEqual(rates["declared_invalid_rejection"], 1.0)

    def test_report_is_oscarc_and_scientific_nonconformity_is_reportable(self):
        report = markdown_report(self.result)
        for section in ("## O —", "## S —", "## C — Context", "## A —", "## R —", "## C — Comparative"):
            self.assertIn(section, report)
        altered = json.loads(json.dumps(self.result))
        altered["conformity"]["judgment"] = "INCONSISTENT"
        self.assertIn("INCONSISTENT", markdown_report(altered))

    def test_write_emits_json_and_markdown(self):
        with tempfile.TemporaryDirectory() as directory:
            result_path = Path(directory) / "result.json"
            report_path = Path(directory) / "report.md"
            write_results(self.result, result_path, report_path)
            self.assertEqual(json.loads(result_path.read_text())["benchmark_version"], "combinatorial-uniqueness-v1")
            self.assertIn("Evidence boundary", report_path.read_text())

    def test_check_is_nonmutating_and_detects_report_drift(self):
        with tempfile.TemporaryDirectory() as directory:
            result_path = Path(directory) / "result.json"
            report_path = Path(directory) / "report.md"
            write_results(self.result, result_path, report_path)
            before = (result_path.read_bytes(), report_path.read_bytes())
            check_result(self.result, result_path, report_path)
            self.assertEqual(before, (result_path.read_bytes(), report_path.read_bytes()))
            report_path.write_text("drift")
            with self.assertRaisesRegex(SystemExit, "report differs"):
                check_result(self.result, result_path, report_path)

    def test_provenance_and_artifact_identities_are_complete(self):
        identities = self.result["artifact_identities"]
        for key in ("physical_state_sha256", "physical_probes_sha256", "legal_state_sha256",
                    "legal_probes_sha256", "kernel_sha256", "operational_flow_sha256",
                    "experiment_sha256", "fixture_loader_sha256", "methodology_sha256"):
            self.assertTrue(identities[key].startswith("sha256:"))
        self.assertIn("python", self.result["provenance"])
        self.assertIn("numpy", self.result["provenance"])

    def test_checked_in_json_and_markdown_are_fresh(self):
        check_result(self.result)

    def test_bespoke_combination_node_or_relation_is_detected(self):
        root = Path(__file__).resolve().parents[1]
        fixture = load_experiment_fixture(root / "data/demonstration/combinatorial_uniqueness_v1.json")
        state = CombinatorialUniquenessFlow().govern_and_compile(fixture.state)
        combination = "+".join(fixture.probes.probes["independent_composition_probes"][0]["constraints"])
        poisoned_graph = replace(
            state.graph,
            vocab=state.graph.vocab + (combination,),
            relations=state.graph.relations + ({
                "id": "fixture:independent_capacitor:bespoke", "source": "storage",
                "relation": "supports", "target": "capacitor",
            },),
        )
        poisoned = replace(state, graph=poisoned_graph,
                           relation_ids=state.relation_ids + ("fixture:independent_capacitor:bespoke",))
        audit = audit_no_bespoke_primitives(poisoned, fixture.probes.probes)
        self.assertFalse(audit["passed"])
        self.assertIn(combination, audit["vocabulary_violations"])
        self.assertIn("fixture:independent_capacitor:bespoke", audit["relation_violations"])


if __name__ == "__main__":
    unittest.main()
