import unittest

import numpy as np

import mml_elaborate_corpus as mml
import mml_legal_usecase as legal
import pagerank_attention as essence


class TransitionGraphTests(unittest.TestCase):
    def test_non_empty_transition_rows_sum_to_one(self):
        non_empty_rows = mml.co_occurrence.sum(axis=1) > 0
        np.testing.assert_allclose(mml.P[non_empty_rows].sum(axis=1), 1.0)

    def test_single_token_activation_is_deterministic_and_normalized(self):
        first = mml.activation_distribution("bank")
        second = mml.activation_distribution("bank")
        np.testing.assert_allclose(first, second)
        self.assertAlmostEqual(float(first.sum()), 1.0, places=6)

    def test_multi_token_queries_change_the_activation_field(self):
        river_bank = mml.activation_distribution(["river", "bank"])
        financial_bank = mml.activation_distribution(["money", "bank"])
        self.assertFalse(np.allclose(river_bank, financial_bank))
        self.assertGreater(river_bank[mml.word2idx["river"]], financial_bank[mml.word2idx["river"]])
        self.assertGreater(financial_bank[mml.word2idx["money"]], river_bank[mml.word2idx["money"]])

    def test_multi_token_activation_is_combinatorial_not_an_average(self):
        combined = mml.activation_distribution(["river", "bank"])
        additive = (
            mml.activation_distribution("river")
            + mml.activation_distribution("bank")
        ) / 2
        self.assertFalse(np.allclose(combined, additive))

    def test_activation_explanation_contains_valid_paths(self):
        explanations = mml.explain_activation(["river", "bank"], top_n=2)
        self.assertEqual(len(explanations), 2)
        for explanation in explanations:
            for source_word, path in explanation["query_paths"].items():
                self.assertIsNotNone(path)
                self.assertEqual(path["words"][0], source_word)
                self.assertEqual(path["words"][-1], explanation["word"])
                self.assertEqual(len(path["edge_weights"]), len(path["words"]) - 1)
                self.assertGreater(path["probability"], 0.0)

    def test_unknown_tokens_are_ignored_when_query_has_known_tokens(self):
        mixed = mml.activation_distribution(["bank", "not_in_vocabulary"])
        known = mml.activation_distribution("bank")
        np.testing.assert_allclose(mixed, known)

    def test_all_unknown_query_fails_explicitly(self):
        with self.assertRaisesRegex(ValueError, "no words"):
            mml.activation_distribution(["not_in_vocabulary"])

    def test_essence_demo_returns_converged_distribution(self):
        scores = essence.query_anchored_diffusion("river", essence.P)
        self.assertAlmostEqual(float(scores.sum()), 1.0, places=6)

    def test_essence_curation_separates_bank_senses(self):
        result = essence.curation_ab_result()
        river = result["bank_river"]
        financial = result["bank_financial"]

        self.assertGreater(river["own_context_weight"], river["opposite_context_weight"])
        self.assertGreater(financial["own_context_weight"], financial["opposite_context_weight"])

    def test_essence_curation_reduces_cross_sense_leakage(self):
        result = essence.curation_ab_result()
        ambiguous = result["ambiguous"]

        self.assertLess(
            result["bank_river"]["opposite_context_weight"],
            ambiguous["financial_context_weight"],
        )
        self.assertLess(
            result["bank_financial"]["opposite_context_weight"],
            ambiguous["river_context_weight"],
        )


class LegalDemoTests(unittest.TestCase):
    def test_empty_theme_ranking_is_safe_for_package_selection(self):
        self.assertEqual(legal.ranked_emails_for_theme(["not_in_vocabulary"]), [])

    def test_curation_ab_test_exposes_candidate_filtering(self):
        result = legal.curation_ab_result(legal.LEGAL_CASE_THEMES["incomplete_disclosure"]["words"])
        self.assertLessEqual(result["curated_candidate_count"], result["unfiltered_candidate_count"])
        self.assertEqual(result["unfiltered_candidate_count"], len(legal.EMAIL_EVIDENCE_CANDIDATES))


if __name__ == "__main__":
    unittest.main()
