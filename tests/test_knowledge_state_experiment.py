import unittest

from experiments.knowledge_state_execution.benchmark import markdown_report, run_experiment


class KnowledgeStateExperimentTests(unittest.TestCase):
    def setUp(self):
        self.result = run_experiment()

    def test_treatments_expose_reconstruction_and_reuse_difference(self):
        accuracy = self.result["accuracy"]
        self.assertEqual(accuracy["lexical_retrieval"], 0)
        self.assertEqual(accuracy["source_reconstruction"], 2)
        self.assertEqual(accuracy["compiled_mml"], 2)

        compiled = self.result["treatments"]["compiled_mml"]
        self.assertTrue(all(item["knowledge_tokens_processed"] == 0 for item in compiled.values()))
        self.assertTrue(all(item["source_file_reads"] == 0 for item in compiled.values()))
        self.assertTrue(all(item["edges_traversed"] == 3 for item in compiled.values()))

        reconstruction = self.result["treatments"]["source_reconstruction"]
        self.assertTrue(all(item["source_file_reads"] == 1 for item in reconstruction.values()))

    def test_mutation_changes_dependent_answer_without_retraining(self):
        mutation = self.result["mutation"]
        self.assertEqual(mutation["changed_execution"]["answer"], "nora")
        self.assertTrue(mutation["original_answer_preserved"])
        self.assertTrue(mutation["unaffected_answer_preserved"])
        self.assertFalse(mutation["retraining_required"])
        self.assertEqual(mutation["entries_replaced"], 1)
        self.assertEqual(mutation["facts_scanned"], 6)
        self.assertEqual(mutation["index_entries_copied"], 6)

    def test_measurement_families_remain_separate(self):
        self.assertIn("source", self.result["fixture"])
        self.assertIn("compile_work", self.result["compiled_state"])
        self.assertEqual(self.result["timing"]["clock"], "time.perf_counter_ns")
        self.assertIn(
            "not a production performance comparison",
            self.result["timing"]["interpretation"],
        )
        observations = self.result["timing"]["derived_observations"]
        self.assertIn("reconstruction_over_compiled_query_ratio", observations)
        self.assertIn("lexical_over_compiled_query_ratio", observations)
        self.assertIn("observed_compile_break_even_queries_vs_reconstruction", observations)

    def test_report_states_concept_and_evidence_boundary(self):
        report = markdown_report(self.result)
        self.assertIn("Knowledge is state, not behaviour buried in a model", report)
        self.assertIn("O — Objective observation", report)
        self.assertIn("S — Standard, baseline, or reference model", report)
        self.assertIn("C — Context and chronology", report)
        self.assertIn("A — Actions, interventions, or observed mechanisms", report)
        self.assertIn("R — Result, effect, or measured outcome", report)
        self.assertIn("C — Comparative assessment and research conclusion", report)
        self.assertIn("Evidence strength: `LOW`", report)
        self.assertIn("luma -> vek -> tor -> nora", report)
        self.assertIn("no language-model treatment", report)
        self.assertIn("not general language understanding", report)
        self.assertIn("Research implication — architectural signal", report)
        self.assertIn(
            "Intelligence can be distributed between a probabilistic learner", report
        )
        self.assertIn(
            "Energy consumption is lower than a language model | Untested hypothesis",
            report,
        )

    def test_machine_result_preserves_oscarc_traceability(self):
        self.assertEqual(self.result["reporting_methodology"], "OSCARC-v1")
        self.assertEqual(self.result["conformity"]["judgment"], "CONSISTENT")
        self.assertTrue(all(self.result["conformity"]["criteria"].values()))
        self.assertIn("source_fixture_sha256", self.result["artifact_identities"])
        self.assertIn("human_report", self.result["provenance"])
        self.assertIn("research_implication", self.result)


if __name__ == "__main__":
    unittest.main()
