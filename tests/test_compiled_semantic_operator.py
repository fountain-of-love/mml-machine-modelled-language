import unittest

import numpy as np

from src.knowledge_state_execution.compiled_semantic_operator import (
    CompiledSemanticOperator,
    SemanticOperatorPolicy,
    compile_semantic_operator,
)


class CompiledSemanticOperatorTests(unittest.TestCase):
    def setUp(self):
        self.vocab = ("alpha", "beta", "gamma")
        self.relations = (
            {"id": "r-support", "source": "alpha", "relation": "supports", "target": "beta", "weight": 1.0},
            {"id": "r-require", "source": "alpha", "relation": "requires", "target": "gamma", "weight": 1.0},
            {"id": "r-contradict", "source": "beta", "relation": "contradicts", "target": "gamma", "weight": 1.0},
        )

    def test_compiles_relation_specific_sparse_layers(self):
        state = compile_semantic_operator(
            self.vocab,
            self.relations,
            SemanticOperatorPolicy(
                "retrieval-v1",
                {"supports": 1.0, "requires": 0.5, "contradicts": 1.0},
            ),
        )
        self.assertIsInstance(state, CompiledSemanticOperator)
        self.assertEqual(("requires", "supports"), state.relation_types)
        self.assertEqual(2, state.edge_count)
        self.assertEqual(3, state.source_count)
        self.assertNotIn("contradicts", state.layers)

    def test_policy_coefficients_change_execution_but_keep_layers_inspectable(self):
        balanced = compile_semantic_operator(
            self.vocab, self.relations, SemanticOperatorPolicy(
                "balanced-v1", {"supports": 1.0, "requires": 1.0}
            )
        )
        supports = compile_semantic_operator(
            self.vocab, self.relations, SemanticOperatorPolicy(
                "supports-v1", {"supports": 1.0, "requires": 0.0}
            )
        )
        field = np.array([1.0, 0.0, 0.0])
        np.testing.assert_allclose(balanced.propagate(field), [0.0, 0.5, 0.5])
        np.testing.assert_allclose(supports.propagate(field), [0.0, 1.0, 0.0])
        self.assertNotEqual(supports.snapshot_id, balanced.snapshot_id)

    def test_duplicate_edges_are_coalesced_and_rows_normalized(self):
        relations = (
            {"id": "r1", "source": "alpha", "relation": "supports", "target": "beta", "weight": 1.0},
            {"id": "r2", "source": "alpha", "relation": "supports", "target": "beta", "weight": 3.0},
            {"id": "r3", "source": "alpha", "relation": "supports", "target": "gamma", "weight": 2.0},
        )
        state = compile_semantic_operator(
            self.vocab, relations, SemanticOperatorPolicy("supports-v1", {"supports": 1.0})
        )
        layer = state.layers["supports"]
        self.assertEqual(2, layer.edge_count)
        np.testing.assert_allclose(state.propagate([1.0, 0.0, 0.0]), [0.0, 2 / 3, 1 / 3])

    def test_state_and_arrays_are_read_only_and_replay_is_deterministic(self):
        policy = SemanticOperatorPolicy("retrieval-v1", {"supports": 1.0, "requires": 0.5})
        first = compile_semantic_operator(self.vocab, self.relations, policy)
        second = compile_semantic_operator(tuple(reversed(self.vocab)), tuple(reversed(self.relations)), policy)
        self.assertEqual(first.snapshot_id, second.snapshot_id)
        with self.assertRaises(ValueError):
            first.layers["supports"].values[0] = 2.0
        with self.assertRaises(TypeError):
            first.word2idx["delta"] = 4

    def test_invalid_policy_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "versioned"):
            SemanticOperatorPolicy("retrieval", {"supports": 1.0})
        with self.assertRaisesRegex(ValueError, "unknown"):
            SemanticOperatorPolicy("retrieval-v1", {"synonymy": 1.0})
        with self.assertRaisesRegex(ValueError, "positive relation"):
            SemanticOperatorPolicy("retrieval-v1", {"contradicts": 1.0})


if __name__ == "__main__":
    unittest.main()
