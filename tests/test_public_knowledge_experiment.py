import unittest

from experiments.knowledge_state_execution.ntriples import (
    Triple,
    parse_line,
    parse_ntriples,
    serialize_ntriples,
    serialize_triple,
)
from experiments.knowledge_state_execution.public_knowledge import assertion_id_for
from experiments.knowledge_state_execution.public_knowledge_benchmark import (
    markdown_report,
    run_experiment,
)


class NTriplesSubsetTests(unittest.TestCase):
    def test_round_trip_preserves_language_datatype_and_escapes(self):
        triples = [
            Triple("http://e/s", "http://e/p", "http://e/o"),
            Triple("http://e/s", "http://e/label", 'politique de l\'information "q"\n\\', "literal", "fr"),
            Triple("http://e/s", "http://e/flag", "true", "literal", None, "http://www.w3.org/2001/XMLSchema#boolean"),
        ]
        for triple in triples:
            self.assertEqual(parse_line(serialize_triple(triple)), triple)
        self.assertEqual(sorted(parse_ntriples(serialize_ntriples(triples))), sorted(triples))

    def test_unsupported_syntax_is_refused(self):
        with self.assertRaises(ValueError):
            parse_line("_:b0 <http://e/p> <http://e/o> .")

    def test_assertion_identity_is_derived_from_the_exact_source_statement(self):
        triple = Triple("http://e/s", "http://e/p", "http://e/o")
        self.assertEqual(assertion_id_for(triple), assertion_id_for(Triple("http://e/s", "http://e/p", "http://e/o")))
        self.assertNotEqual(assertion_id_for(triple), assertion_id_for(Triple("http://e/s", "http://e/p", "http://e/x")))


class PublicKnowledgeExperimentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = run_experiment(include_timing=False)

    def test_all_declared_criteria_hold(self):
        self.assertEqual(self.result["conformity"]["verdict"], "CONSISTENT")

    def test_compiled_state_reproduces_independent_cellar_oracle(self):
        agreement = self.result["agreement"]
        self.assertEqual(agreement["queries"], 19)
        self.assertEqual(agreement["compiled_matches_oracle"], 19)
        self.assertEqual(agreement["reconstruction_matches_compiled"], 19)
        self.assertLess(agreement["direct_only_matches_oracle"], 19)

    def test_gdpr_traces_back_to_public_identifiers(self):
        trace = self.result["trace"]
        self.assertEqual(trace["celex"], "32016R0679")
        self.assertEqual(trace["query_labels"]["de"], "Informationspolitik")
        sources = [item["source_triple"] for route in trace["routes"] for item in route["evidence"]]
        self.assertTrue(all(line.startswith("<http") for line in sources))
        self.assertIn("http://eurovoc.europa.eu/5181", {route["via_concept"] for route in trace["routes"]})

    def test_out_of_scope_public_concept_is_refused(self):
        self.assertTrue(self.result["refusal"]["refused_by_both"])

    def test_correction_is_bounded_attributable_and_reversible(self):
        correction = self.result["correction"]
        self.assertEqual(
            sorted(correction["observed_changed_queries"]),
            ["http://eurovoc.europa.eu/2472", "http://eurovoc.europa.eu/453"],
        )
        self.assertTrue(correction["divergence_from_source_is_governed"])
        self.assertTrue(correction["source_triple_retained_in_snapshot"])
        self.assertTrue(correction["restored_snapshot_equals_original"])

    def test_negative_reuse_finding_is_preserved(self):
        work = self.result["work_model"]
        self.assertEqual(work["compiled_query_bytes_read"], 0)
        self.assertEqual(work["first_listed_horizon_where_compiled_is_cheaper_than_reconstruction"], 2)
        self.assertTrue(all(gap >= 0 for gap in work["compiled_minus_cached_at_every_horizon"]))
        report = markdown_report(self.result)
        self.assertIn("negative evidence preserved", report)
        self.assertIn("adds no measurable work benefit", report)
        self.assertIn("Evidence strength: `LOW`", report)


if __name__ == "__main__":
    unittest.main()
