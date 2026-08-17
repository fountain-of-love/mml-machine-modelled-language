import unittest

from experiments.semantic_navigation.dimension_contribution_analysis import analyze_seed


class DimensionContributionAnalysisTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = analyze_seed()

    def test_analysis_uses_binary_questions_and_coverage_penalty(self):
        model = self.result["question_model"]

        self.assertEqual(model["multi_value_question"], "binary value presence")
        self.assertIn("coverage penalty", model["missing_value_treatment"])

    def test_biome_signature_entropy_is_exposed_as_apparent_inflation(self):
        biome = self.result["dimensions"]["biome"]["root"]

        self.assertGreater(biome["exact_signature_entropy_bits"], 3.0)
        self.assertLessEqual(biome["best_binary_information_gain_bits"], 1.0)
        self.assertGreater(biome["apparent_entropy_inflation_bits"], 2.0)

    def test_conditional_information_gain_is_measured_in_narrowed_regions(self):
        biome = self.result["dimensions"]["biome"]["conditional"]

        self.assertGreater(biome["eligible_context_count"], 0)
        self.assertGreater(biome["positive_gain_context_count"], 0)
        self.assertGreater(
            biome["maximum_coverage_adjusted_information_gain_bits"],
            0.0,
        )
        self.assertIsNotNone(biome["best_context"])

    def test_default_analysis_excludes_zoological_detail(self):
        self.assertEqual(
            self.result["seed_state_id"],
            "species_ecology_behavior_seed_canidae_v0_1",
        )
        self.assertNotIn("body_length_band", self.result["dimensions"])
        self.assertNotIn("thermoregulation", self.result["dimensions"])


if __name__ == "__main__":
    unittest.main()
