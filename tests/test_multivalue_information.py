import unittest

from src.semantic_navigation.multivalue_information import (
    ValueObservation,
    analyze_multivalue_dimension,
    condition_candidates,
)


RECORDS = {
    "a": {"biome": ("forest", "grassland")},
    "b": {"biome": ("forest", "desert")},
    "c": {"biome": ("forest", "wetland")},
    "d": {"biome": ("forest", "mountain")},
    "unknown": {"biome": ()},
}


class MultiValueInformationTests(unittest.TestCase):
    def test_exact_signatures_are_not_treated_as_reusable_answers(self):
        information = analyze_multivalue_dimension(
            RECORDS,
            "biome",
            candidate_ids=("a", "b", "c", "d"),
        )

        self.assertEqual(information.exact_signature_entropy_bits, 2.0)
        self.assertEqual(information.best_value_question.value, "desert")
        self.assertAlmostEqual(
            information.best_value_question.information_gain_bits,
            0.8112781244591328,
        )
        self.assertGreater(information.apparent_entropy_inflation_bits, 1.18)
        forest = next(q for q in information.value_questions if q.value == "forest")
        self.assertEqual(forest.information_gain_bits, 0.0)
        self.assertEqual(str(forest.information_gain_bits), "0.0")

    def test_missing_records_reduce_coverage_without_becoming_an_answer(self):
        information = analyze_multivalue_dimension(RECORDS, "biome")

        self.assertEqual(information.missing_candidate_count, 1)
        self.assertEqual(information.best_value_question.coverage, 0.8)
        self.assertAlmostEqual(
            information.best_value_question.coverage_adjusted_information_gain_bits,
            0.6490224995673063,
        )

    def test_conditional_context_changes_value_information(self):
        candidates = condition_candidates(
            RECORDS,
            (ValueObservation("biome", "forest", present=True),),
        )
        narrowed = condition_candidates(
            RECORDS,
            (ValueObservation("biome", "grassland", present=False),),
            candidate_ids=candidates,
        )

        self.assertEqual(candidates, ("a", "b", "c", "d"))
        self.assertEqual(narrowed, ("b", "c", "d"))
        conditional = analyze_multivalue_dimension(RECORDS, "biome", narrowed)
        self.assertAlmostEqual(
            conditional.best_value_question.information_gain_bits,
            0.9182958340544896,
        )

    def test_unknown_candidate_ids_fail_fast(self):
        with self.assertRaisesRegex(ValueError, "unknown candidate IDs"):
            analyze_multivalue_dimension(RECORDS, "biome", ("missing",))


if __name__ == "__main__":
    unittest.main()
