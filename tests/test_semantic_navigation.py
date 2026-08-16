import unittest

from experiments.semantic_navigation.compiled_encyclopedic_navigation_benchmark import (
    REPORT_PATH,
    RESULT_PATH,
    build_queries,
    check_result,
    evidence_manifest,
    run_experiment,
)
from src.combinatorial_uniqueness.candidate_regions import compose_candidate_region
from src.knowledge_state_execution.compiled_incidence import compile_incidence_state
from src.semantic_navigation.navigation import (
    AMBIGUOUS,
    IDENTIFIABLE,
    UNSUPPORTED,
    SemanticNavigationFlow,
)
from src.semantic_representation.governed_coordinates import (
    CodedSemanticQuery,
    SemanticEntity,
    encode_query,
    represent_coordinate_basis,
)


DIMENSIONS = ("habitat", "diet", "activity", "sociality")


def _entity(identifier, label, habitat, diet, activity, sociality):
    return SemanticEntity(identifier, label, {
        "habitat": habitat,
        "diet": diet,
        "activity": activity,
        "sociality": sociality,
    })


def _records():
    return (
        _entity("red_fox", "Red fox", "woodland", "omnivore", "nocturnal", "solitary"),
        _entity("raccoon", "Raccoon", "woodland", "omnivore", "nocturnal", "solitary"),
        _entity("brown_bear", "Brown bear", "woodland", "omnivore", "diurnal", "solitary"),
        _entity("red_panda", "Red panda", "woodland", "omnivore", "crepuscular", "solitary"),
        _entity("polar_bear", "Polar bear", "polar", "carnivore", "diurnal", "solitary"),
        _entity("walrus", "Walrus", "polar", "carnivore", "diurnal", "herd"),
    )


class AccumulatedCapabilityContractTests(unittest.TestCase):
    def setUp(self):
        self.records = _records()
        self.basis = represent_coordinate_basis("test", DIMENSIONS, self.records)
        self.knowledge_state = compile_incidence_state(self.basis)
        self.flow = SemanticNavigationFlow()
        self.state = self.flow.govern_and_compile("test", DIMENSIONS, self.records)

    def test_semantic_representation_owns_qualified_codes_and_missing_fields(self):
        incomplete = self.records + (
            _entity("observation", "Observation", "wetland", None, "nocturnal", None),
        )
        basis = represent_coordinate_basis("incomplete", DIMENSIONS, incomplete)

        self.assertIn("habitat:woodland", basis.coordinate_codes)
        self.assertEqual(basis.incomplete_entities["observation"], ("diet", "sociality"))
        with self.assertRaises(TypeError):
            basis.coordinate_codes["habitat:woodland"] = 999

    def test_semantic_representation_rejects_non_string_values_cleanly(self):
        invalid = SemanticEntity("invalid", "Invalid", {
            "habitat": 42,
            "diet": "omnivore",
            "activity": "nocturnal",
            "sociality": "solitary",
        })

        with self.assertRaisesRegex(ValueError, "normalized governed identities"):
            represent_coordinate_basis("invalid", DIMENSIONS, (invalid,))

    def test_knowledge_state_owns_immutable_postings_and_signature_classes(self):
        woodland = self.basis.coordinate_codes["habitat:woodland"]

        self.assertEqual(self.knowledge_state.postings[woodland], (0, 1, 2, 3))
        self.assertIn(("red_fox", "raccoon"), self.knowledge_state.signature_classes.values())
        with self.assertRaises(TypeError):
            self.knowledge_state.postings[woodland] = ()

    def test_combinatorial_uniqueness_owns_exact_candidate_region_composition(self):
        observed = {
            "habitat": "woodland",
            "diet": "omnivore",
            "activity": "nocturnal",
            "sociality": "solitary",
        }
        region = compose_candidate_region(
            self.knowledge_state,
            encode_query(self.basis, observed).coordinate_codes,
        )

        self.assertEqual(region.entity_ids, ("red_fox", "raccoon"))

    def test_navigation_preserves_an_equivalence_class(self):
        result = self.flow.execute(self.state, {
            "habitat": "woodland",
            "diet": "omnivore",
            "activity": "nocturnal",
            "sociality": "solitary",
        })

        self.assertEqual(result.candidate_ids, ("red_fox", "raccoon"))
        self.assertEqual(result.status, AMBIGUOUS)

    def test_status_is_defined_by_candidate_region_cardinality(self):
        identifiable = self.flow.execute(self.state, {"activity": "crepuscular"})
        ambiguous = self.flow.execute(self.state, {"habitat": "woodland"})
        unsupported = self.flow.execute(self.state, {"habitat": "polar", "diet": "omnivore"})

        self.assertEqual(identifiable.status, IDENTIFIABLE)
        self.assertEqual(ambiguous.status, AMBIGUOUS)
        self.assertEqual(unsupported.status, UNSUPPORTED)

    def test_imputation_requires_unanimous_candidate_values(self):
        result = self.flow.execute(self.state, {"habitat": "polar", "diet": "carnivore"})

        self.assertEqual(result.deterministic_imputations, {"activity": "diurnal"})
        self.assertNotIn("sociality", result.deterministic_imputations)
        self.assertEqual(set(result.distinctions["sociality"]), {"herd", "solitary"})

    def test_next_dimension_maximizes_information_gain(self):
        result = self.flow.execute(self.state, {
            "habitat": "woodland",
            "diet": "omnivore",
            "sociality": "solitary",
        })

        self.assertEqual(result.next_dimension, "activity")
        self.assertEqual(set(result.distinctions["activity"]), {"nocturnal", "diurnal", "crepuscular"})

    def test_commonality_is_a_separate_set_query(self):
        common = self.flow.common_dimensions(
            self.state,
            ("red_fox", "raccoon", "brown_bear"),
        )

        self.assertEqual(common, {
            "habitat": "woodland",
            "diet": "omnivore",
            "sociality": "solitary",
        })

    def test_compact_codes_are_behaviorally_equivalent(self):
        observed = {"habitat": "woodland", "diet": "omnivore", "sociality": "solitary"}
        semantic = self.flow.execute(self.state, observed)
        coded = self.flow.execute_codes(self.state, encode_query(self.state.basis, observed))

        self.assertEqual(coded.candidate_ids, semantic.candidate_ids)
        self.assertEqual(coded.status, semantic.status)
        self.assertEqual(coded.next_dimension, semantic.next_dimension)
        self.assertEqual(coded.distinctions, semantic.distinctions)

    def test_unsupported_compact_value_retains_its_observed_dimension(self):
        observed = {"habitat": "moon", "diet": "omnivore"}
        semantic = self.flow.execute(self.state, observed)
        coded = self.flow.execute_codes(self.state, encode_query(self.state.basis, observed))

        self.assertEqual(coded.status, UNSUPPORTED)
        self.assertEqual(coded.distinctions, semantic.distinctions)
        self.assertNotIn("habitat", coded.distinctions)

    def test_coded_query_rejects_a_code_from_the_wrong_dimension(self):
        habitat_code = self.state.basis.coordinate_codes["habitat:woodland"]
        query = CodedSemanticQuery(("diet",), (habitat_code,))

        with self.assertRaisesRegex(ValueError, "belongs to 'habitat'"):
            self.flow.execute_codes(self.state, query)

    def test_query_contract_rejects_malformed_semantic_and_coded_values(self):
        with self.assertRaisesRegex(ValueError, "query values"):
            self.flow.execute(self.state, {"habitat": "not normalized"})
        with self.assertRaisesRegex(ValueError, "-1 sentinel"):
            CodedSemanticQuery(("habitat",), (-2,))

    def test_identification_depth_reports_unresolvable_identities(self):
        profiles = self.flow.identification_profiles(self.state)
        fox_class = next(profile for profile in profiles if "red_fox" in profile.candidate_ids)

        self.assertEqual(fox_class.candidate_ids, ("red_fox", "raccoon"))
        self.assertFalse(fox_class.uniquely_identifiable)
        self.assertIsNotNone(fox_class.minimum_dimension_count)


class CompiledEncyclopedicNavigationExperimentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = run_experiment()

    def test_query_suite_covers_subsets_and_unsupported_combinations(self):
        queries = build_queries(_records(), DIMENSIONS)

        self.assertTrue(any(query.condition == "complete" for query in queries))
        self.assertTrue(any(query.condition == "one_missing" for query in queries))
        self.assertTrue(any(query.condition == "multiple_missing" for query in queries))
        self.assertTrue(any(query.condition == "unsupported" for query in queries))

    def test_all_conformity_criteria_pass(self):
        self.assertEqual(
            self.result["conformity"]["judgment"],
            "ACCUMULATED_MECHANICS_CONFORMANT",
        )
        self.assertTrue(all(self.result["conformity"]["criteria"].values()))

    def test_result_records_every_capability_contribution(self):
        self.assertEqual(set(self.result["capability_contributions"]), {
            "semantic_representation",
            "knowledge_state_execution",
            "combinatorial_uniqueness",
            "semantic_navigation",
        })
        self.assertEqual(self.result["aggregate"]["exact_set_accuracy"], 1.0)

    def test_published_evidence_is_compact_and_content_addressed(self):
        manifest = evidence_manifest(self.result)

        self.assertNotIn("queries", manifest)
        self.assertEqual(manifest["query_evidence"]["query_count"], 320)
        self.assertEqual(
            set(manifest["query_evidence"]["condition_summaries"]),
            {"complete", "one_missing", "multiple_missing", "unsupported"},
        )
        self.assertEqual(manifest["query_evidence"]["failed_query_count"], 0)
        self.assertEqual(manifest["query_evidence"]["failed_query_ids"], [])
        self.assertEqual(manifest["query_evidence"]["failed_query_samples"], [])
        self.assertRegex(
            manifest["query_evidence"]["trace_sha256"],
            r"^sha256:[0-9a-f]{64}$",
        )

    def test_scaling_reports_warm_query_efficiency_and_amortization(self):
        for row in self.result["scaling"]:
            self.assertLess(row["warm_compiled_vs_scan_operation_ratio"], 1.0)
            self.assertIsNotNone(row["amortization_break_even_query_count"])

    def test_fixture_remains_seed_not_independent_evidence(self):
        self.assertEqual(
            self.result["fixture"]["lifecycle"],
            "USER_PROVIDED_SEED_NOT_INDEPENDENTLY_SOURCED",
        )
        self.assertIn("prompt-provided", self.result["evidence_boundary"])

    def test_checked_in_artifacts_are_fresh(self):
        check_result(self.result, RESULT_PATH, REPORT_PATH)


if __name__ == "__main__":
    unittest.main()
