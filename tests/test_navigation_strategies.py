import unittest
from dataclasses import dataclass

from experiments.semantic_navigation.fixtures import load_compiled_navigation_fixture
from src.semantic_navigation.navigation import SemanticNavigationFlow
from src.semantic_navigation.strategies import (
    FIXED_DIMENSION_ORDER,
    HIGHEST_CARDINALITY,
    HIGHEST_COVERAGE,
    INFORMATION_GAIN,
    RANDOM_ELIGIBLE,
    FixedDimensionOrderNavigationStrategy,
    HighestCardinalityNavigationStrategy,
    HighestCoverageNavigationStrategy,
    InformationGainNavigationStrategy,
    RandomEligibleNavigationStrategy,
    NavigationStrategy,
)


class NavigationStrategyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        _, dimensions, records, _ = load_compiled_navigation_fixture()
        cls.dimensions = dimensions
        cls.state = SemanticNavigationFlow().govern_and_compile(
            "navigation_strategy_tests", dimensions, records
        )

    def _start(self, strategy):
        return SemanticNavigationFlow(strategy).start(self.state)

    def test_information_gain_is_the_default_strategy(self):
        result = SemanticNavigationFlow().start(self.state)

        self.assertEqual(result.strategy_id, INFORMATION_GAIN)
        self.assertEqual(result.next_dimension, "habitat")

    def test_each_strategy_is_available_through_the_same_contract(self):
        cases = (
            (InformationGainNavigationStrategy(), INFORMATION_GAIN),
            (FixedDimensionOrderNavigationStrategy(), FIXED_DIMENSION_ORDER),
            (HighestCardinalityNavigationStrategy(), HIGHEST_CARDINALITY),
            (HighestCoverageNavigationStrategy(), HIGHEST_COVERAGE),
            (RandomEligibleNavigationStrategy(7), RANDOM_ELIGIBLE),
        )

        for strategy, expected_id in cases:
            with self.subTest(strategy=expected_id):
                result = self._start(strategy)
                self.assertEqual(result.strategy_id, expected_id)
                self.assertIn(result.next_dimension, self.dimensions)

    def test_strategy_changes_question_selection_not_candidate_retrieval(self):
        information_gain = self._start(InformationGainNavigationStrategy())
        fixed = self._start(FixedDimensionOrderNavigationStrategy())

        self.assertEqual(information_gain.candidate_ids, fixed.candidate_ids)
        self.assertEqual(information_gain.region, fixed.region)

    def test_seeded_random_selection_is_state_deterministic(self):
        first = self._start(RandomEligibleNavigationStrategy(19))
        second = self._start(RandomEligibleNavigationStrategy(19))

        self.assertEqual(first.next_dimension, second.next_dimension)

    def test_random_strategy_rejects_an_invalid_seed(self):
        with self.assertRaisesRegex(ValueError, "seed must be an integer"):
            RandomEligibleNavigationStrategy(True)

    def test_flow_rejects_an_ineligible_custom_strategy_selection(self):
        @dataclass(frozen=True)
        class InvalidStrategy(NavigationStrategy):
            id = "invalid"

            def select(self, information, dimension_order):
                return "undeclared_dimension"

        with self.assertRaisesRegex(ValueError, "selected an ineligible dimension"):
            self._start(InvalidStrategy())


if __name__ == "__main__":
    unittest.main()
