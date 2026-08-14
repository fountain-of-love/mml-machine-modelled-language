import itertools
import math
import unittest

import numpy as np

from src.combinatorial_uniqueness.compose_concepts import (
    ActivatedField,
    distribution_metrics,
    normalize,
    soft_intersection,
    target_margin,
    target_rank,
)
from elaborations.mml_graph import GraphModel


def legacy_activation(model, query):
    """Characterization oracle for the pre-extraction graph implementation."""
    words = model.resolve_tokens(query)
    if not words:
        return np.zeros(len(model.vocab))
    fields = [model._single_field(word) for word in words]
    if len(fields) == 1:
        combined = fields[0]
    else:
        epsilon = np.finfo(float).tiny
        combined = np.exp(np.mean(np.log(np.maximum(fields, epsilon)), axis=0))
    adjusted = combined / np.sqrt(np.maximum(model.background, np.finfo(float).tiny))
    total = adjusted.sum()
    return adjusted / total if total else adjusted


class CompositionKernelTests(unittest.TestCase):
    def test_graph_activation_preserves_existing_operator_exactly(self):
        model = GraphModel.from_sentences([
            "storage capacitor battery spring",
            "electrical capacitor battery transformer",
            "reversible capacitor spring transformer",
        ])
        for query in ("storage", "storage electrical", "storage electrical reversible"):
            np.testing.assert_array_equal(model.activation(query), legacy_activation(model, query))

    def test_graph_preserves_zero_activation_for_fully_damped_isolated_node(self):
        model = GraphModel.from_sentences(["isolated"], damping=1.0, steps=1)
        np.testing.assert_array_equal((0.0,), model.activation("isolated"))

    def test_soft_intersection_is_normalized_finite_deterministic_and_order_invariant(self):
        fields = (
            ActivatedField("a", (0.8, 0.2, 0.0)),
            ActivatedField("b", (0.5, 0.1, 0.4)),
            ActivatedField("c", (0.2, 0.7, 0.1)),
        )
        expected = soft_intersection(fields)
        self.assertAlmostEqual(1.0, sum(expected.values))
        self.assertTrue(all(math.isfinite(value) for value in expected.values))
        self.assertEqual(expected, soft_intersection(fields))
        for permutation in itertools.permutations(fields):
            np.testing.assert_allclose(
                expected.values, soft_intersection(permutation).values, rtol=1e-15, atol=0
            )

    def test_inputs_and_support_records_are_not_mutated(self):
        source = np.array([0.75, 0.25])
        snapshot = source.copy()
        field = ActivatedField("a", tuple(source))
        result = soft_intersection((field,), background=np.array([0.5, 0.5]))
        np.testing.assert_array_equal(source, snapshot)
        self.assertEqual((field,), result.per_constraint_support)
        with self.assertRaises(Exception):
            result.values[0] = 0.0

    def test_identical_fields_preserve_the_distribution(self):
        field = ActivatedField("a", (0.2, 0.3, 0.5))
        result = soft_intersection((field, ActivatedField("b", field.values)))
        np.testing.assert_allclose(field.values, result.values)

    def test_disjoint_fields_remain_finite_with_tiny_joint_support(self):
        result = soft_intersection((
            ActivatedField("left", (1.0, 0.0)),
            ActivatedField("right", (0.0, 1.0)),
        ))
        np.testing.assert_allclose((0.5, 0.5), result.values)
        self.assertTrue(all(math.isfinite(value) for value in result.values))

    def test_entropy_and_effective_count_match_analytical_distributions(self):
        certain = distribution_metrics((1.0, 0.0, 0.0), top_k=2)
        self.assertAlmostEqual(0.0, certain.entropy)
        self.assertAlmostEqual(0.0, certain.normalized_entropy)
        self.assertAlmostEqual(1.0, certain.effective_candidate_count)
        self.assertAlmostEqual(1.0, certain.concentration)
        self.assertAlmostEqual(1.0, certain.top_k_mass)

        uniform = distribution_metrics((1.0, 1.0, 1.0, 1.0), top_k=2)
        self.assertAlmostEqual(math.log(4), uniform.entropy)
        self.assertAlmostEqual(1.0, uniform.normalized_entropy)
        self.assertAlmostEqual(4.0, uniform.effective_candidate_count)
        self.assertAlmostEqual(0.25, uniform.concentration)
        self.assertAlmostEqual(0.5, uniform.top_k_mass)
        self.assertAlmostEqual(
            1.0, distribution_metrics((1.0, 1.0), top_k=3).top_k_mass
        )

    def test_rank_and_margin_measure_target_against_alternatives(self):
        values = (0.2, 0.5, 0.2, 0.1)
        self.assertEqual(1, target_rank(values, 1))
        self.assertEqual(2, target_rank(values, 0))
        self.assertAlmostEqual(0.3, target_margin(values, 1))
        self.assertAlmostEqual(-0.3, target_margin(values, 0))

    def test_invalid_fields_fail_fast(self):
        invalid_calls = (
            lambda: soft_intersection(()),
            lambda: soft_intersection((ActivatedField("a", (1.0, 0.0)), ActivatedField("b", (1.0,)))),
            lambda: soft_intersection((ActivatedField("a", (-1.0, 2.0)),)),
            lambda: soft_intersection((ActivatedField("a", (0.0, 0.0)),)),
            lambda: normalize((float("nan"), 1.0)),
            lambda: distribution_metrics((1.0, 1.0), top_k=0),
        )
        for call in invalid_calls:
            with self.subTest(call=call):
                with self.assertRaises(ValueError):
                    call()


if __name__ == "__main__":
    unittest.main()
