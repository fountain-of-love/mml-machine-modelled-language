import unittest

import numpy as np

from activate_grounded_focus import (
    ActivationStrategy,
    Activation,
    PersonalizedPageRankActivationStrategy,
    SemanticFocus,
    SemanticGrounding,
    activate,
    compile_transition_model,
    focus,
    ground,
)
from words_carry_weight import WordsCarryWeightFlow
from experiment_fixture import load_experiment
from representation_comparison import compare_representations


class FixedActivationStrategy:
    def activate(self, model, semantic_identity):
        weights = np.zeros(len(model.identities))
        weights[model.identity_to_index[semantic_identity]] = 1.0
        return Activation(model, weights)


class ActivateGroundedFocusTests(unittest.TestCase):
    def test_compile_transition_model_normalizes_non_empty_rows(self):
        model = compile_transition_model(("alpha beta gamma", "beta gamma"))
        non_empty_rows = model.transition.sum(axis=1) > 0
        np.testing.assert_allclose(
            model.transition[non_empty_rows].sum(axis=1), 1.0
        )

    def test_personalized_pagerank_returns_normalized_deterministic_activation(self):
        model = compile_transition_model(("river bank water", "money bank loan"))
        strategy = PersonalizedPageRankActivationStrategy()
        first = activate(model, "bank", strategy)
        second = activate(model, "bank", strategy)

        np.testing.assert_allclose(first.weights, second.weights)
        self.assertAlmostEqual(float(first.weights.sum()), 1.0, places=6)
        self.assertGreater(first.weight_for("bank"), 0.0)
        self.assertEqual(first.weight_for("unknown"), 0.0)

    def test_activate_accepts_an_interchangeable_strategy(self):
        model = compile_transition_model(("alpha beta",))
        strategy = FixedActivationStrategy()

        self.assertIsInstance(strategy, ActivationStrategy)
        activation = activate(model, "beta", strategy)
        self.assertEqual(activation.weight_for("beta"), 1.0)
        self.assertEqual(activation.weight_for("alpha"), 0.0)

    def test_unknown_query_identity_fails_explicitly(self):
        model = compile_transition_model(("alpha beta",))
        with self.assertRaisesRegex(ValueError, "not in model"):
            activate(model, "unknown", PersonalizedPageRankActivationStrategy())


class WordsCarryWeightExperimentTests(unittest.TestCase):
    def test_operational_flow_grounds_focuses_and_activates(self):
        flow = WordsCarryWeightFlow()
        grounding = SemanticGrounding(0, "bank", "bank_river")
        semantic_focus = SemanticFocus("bank", "bank_river")

        model = flow.ground_and_compile(
            ("water beside the bank",), (grounding,)
        )
        result = flow.focus_and_activate(model, "bank", semantic_focus)

        self.assertEqual(result.focused_identity, "bank_river")
        self.assertGreater(result.activation.weight_for("bank_river"), 0.0)

    def test_semantic_grounding_is_a_first_class_operation(self):
        grounding = SemanticGrounding(0, "bank", "bank_river")

        grounded = ground(
            ("water beside the bank",), (grounding,)
        )

        self.assertEqual(grounded, ("water beside the bank_river",))

    def test_semantic_grounding_rejects_an_absent_surface_identity(self):
        grounding = SemanticGrounding(0, "bank", "bank_river")

        with self.assertRaisesRegex(ValueError, "occur exactly once"):
            ground(("water beside the shore",), (grounding,))

    def test_semantic_grounding_must_identify_a_different_identity(self):
        grounding = SemanticGrounding(0, "bank", "bank")

        with self.assertRaisesRegex(ValueError, "different identity"):
            ground(("water beside the bank",), (grounding,))

    def test_semantic_focus_is_a_first_class_operation(self):
        semantic_focus = SemanticFocus("bank", "bank_river")

        self.assertEqual(
            focus("bank", semantic_focus), "bank_river"
        )

    def test_semantic_focus_rejects_a_different_source_identity(self):
        semantic_focus = SemanticFocus("bank", "bank_river")

        with self.assertRaisesRegex(ValueError, "does not apply"):
            focus("shore", semantic_focus)

    def test_semantic_focus_must_narrow_the_identity(self):
        semantic_focus = SemanticFocus("bank", "bank")

        with self.assertRaisesRegex(ValueError, "different identity"):
            focus("bank", semantic_focus)

    def test_grounded_identities_activate_their_primary_context(self):
        result = compare_representations(load_experiment())

        for focused_identity, probe in result["grounded"].items():
            self.assertEqual(
                probe["semantic_focus"].focused_identity, focused_identity
            )
            self.assertGreater(
                probe["primary_context"], probe["contrast_context"]
            )

    def test_grounding_reduces_cross_meaning_activation(self):
        result = compare_representations(load_experiment())
        original_contexts = result["original"]["contexts"]

        self.assertLess(
            result["grounded"]["bank_river"]["contrast_context"],
            original_contexts["financial"],
        )
        self.assertLess(
            result["grounded"]["bank_financial"]["contrast_context"],
            original_contexts["river"],
        )


if __name__ == "__main__":
    unittest.main()
