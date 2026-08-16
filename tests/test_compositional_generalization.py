import unittest

import numpy as np

from src.combinatorial_uniqueness.compositional_generalization import (
    FamilySpec,
    compile_pairwise_state,
    materialize_split,
    mml_soft_intersection_scores,
    personalized_field,
    rank_target,
    signature_for_latent,
    vector_composition_scores,
)


FAMILIES = (
    FamilySpec("a", ("a0", "a1", "a2", "a3"), (1, 0, 0, 0)),
    FamilySpec("b", ("b0", "b1", "b2", "b3"), (0, 1, 0, 0)),
    FamilySpec("c", ("c0", "c1", "c2", "c3"), (0, 0, 1, 0)),
    FamilySpec("d", ("d0", "d1", "d2", "d3"), (0, 0, 0, 1)),
)


class CompositionalGeneralizationKernelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.training, cls.held_out = materialize_split(FAMILIES, 4)
        cls.state = compile_pairwise_state("test-state", FAMILIES, cls.training)

    def test_structural_split_is_complete_disjoint_and_deterministic(self):
        again = materialize_split(FAMILIES, 4)

        self.assertEqual((self.training, self.held_out), again)
        self.assertEqual(len(self.training), 192)
        self.assertEqual(len(self.held_out), 64)
        self.assertFalse(
            {item.coordinates for item in self.training}
            & {item.coordinates for item in self.held_out}
        )

    def test_signature_is_constructed_from_declared_coefficients(self):
        self.assertEqual(
            signature_for_latent((1, 2, 3, 0), FAMILIES, 4),
            ("a:a1", "b:b2", "c:c3", "d:d0"),
        )

    def test_compiled_state_retains_pair_counts_not_entity_signatures(self):
        self.assertEqual(self.state.stored_relation_arity, 2)
        self.assertEqual(self.state.training_entity_count, 192)
        self.assertFalse(hasattr(self.state, "entities"))
        self.assertFalse(hasattr(self.state, "signatures"))
        self.assertFalse(self.state.pair_counts.flags.writeable)
        self.assertFalse(self.state.transition.flags.writeable)
        self.assertFalse(self.state.embedding.flags.writeable)

    def test_personalized_field_is_normalized_and_deterministic(self):
        first = personalized_field(self.state, "a:a0")
        second = personalized_field(self.state, "a:a0")

        np.testing.assert_allclose(first, second, rtol=0, atol=0)
        self.assertAlmostEqual(float(first.sum()), 1.0)

    def test_vector_and_mml_scores_rank_complete_held_out_signature(self):
        target = self.held_out[0]
        for scorer in (vector_composition_scores, mml_soft_intersection_scores):
            with self.subTest(scorer=scorer.__name__):
                ranking = rank_target(
                    scorer(self.state, target.coordinates, self.held_out),
                    self.held_out,
                    target.id,
                )
                self.assertEqual(ranking.target_rank, 1)
                self.assertEqual(ranking.top_candidate, target.id)


if __name__ == "__main__":
    unittest.main()
