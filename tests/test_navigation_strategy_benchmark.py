import unittest

from experiments.semantic_navigation.navigation_strategy_benchmark import (
    HIGHEST_CARDINALITY,
    INFORMATION_GAIN,
    RANDOM_ELIGIBLE,
    RANDOM_REPLICATES,
    check_result,
    run_experiment,
)


class NavigationStrategyBenchmarkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = run_experiment()

    def test_strategies_share_the_uniform_mml_candidate_state(self):
        self.assertEqual(self.result["fixture"]["record_count"], 60)
        self.assertEqual(self.result["fixture"]["equivalence_class_count"], 48)
        self.assertEqual(self.result["protocol"]["candidate_prior"], "uniform")
        self.assertEqual(self.result["protocol"]["varied_component"], "NavigationStrategy")
        self.assertTrue(
            self.result["conformity"]["criteria"]["all_strategies_share_initial_state"]
        )

    def test_information_gain_is_locally_optimal_without_claiming_mml_superiority(self):
        open_results = self.result["strategy_results"]["open"]
        information_gain = open_results[INFORMATION_GAIN]
        cardinality = open_results[HIGHEST_CARDINALITY]

        self.assertEqual(information_gain["mean_selected_question_regret_bits"], 0.0)
        self.assertEqual(information_gain["target_class_resolution_rate"], 1.0)
        self.assertEqual(information_gain["mean_questions_asked"], cardinality["mean_questions_asked"])
        self.assertEqual(
            self.result["open_comparison"][
                "information_gain_minus_best_other_strategy_mean_questions"
            ],
            0.0,
        )

    def test_random_strategy_is_replicated_without_hidden_target_input(self):
        random_result = self.result["strategy_results"]["open"][RANDOM_ELIGIBLE]

        self.assertEqual(random_result["trajectory_count"], 48 * RANDOM_REPLICATES)
        self.assertNotIn("target", self.result["protocol"]["varied_component"].lower())

    def test_lenses_preserve_residual_ambiguity_and_report_regret(self):
        ecological = self.result["strategy_results"]["ecological"][INFORMATION_GAIN]
        behavioral = self.result["strategy_results"]["behavioral"][INFORMATION_GAIN]

        self.assertGreater(ecological["mean_lens_regret_bits"], 0.0)
        self.assertGreater(behavioral["mean_lens_regret_bits"], 0.0)
        self.assertGreater(ecological["lens_exhausted_rate"], 0.0)
        self.assertGreater(
            behavioral["mean_residual_entropy_bits"],
            ecological["mean_residual_entropy_bits"],
        )

    def test_unsupported_queries_remain_unsupported(self):
        self.assertEqual(self.result["unsupported_probes"]["unsupported_rate"], 1.0)
        self.assertTrue(
            self.result["conformity"]["criteria"][
                "valid_target_trajectories_never_become_unsupported"
            ]
        )

    def test_non_uniform_llm_and_non_mml_comparisons_are_deferred(self):
        deferred = set(self.result["protocol"]["deferred_treatments"])
        self.assertIn("non_uniform_candidate_priors", deferred)
        self.assertIn("llm_selected_question", deferred)
        self.assertIn("non_mml_system_comparison", deferred)

    def test_checked_in_artifacts_are_fresh(self):
        check_result(self.result)


if __name__ == "__main__":
    unittest.main()
