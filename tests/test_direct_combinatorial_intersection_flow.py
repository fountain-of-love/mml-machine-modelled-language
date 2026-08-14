import unittest
from pathlib import Path

from experiments.combinatorial_uniqueness.fixture import load_experiment_fixture
from src.combinatorial_uniqueness.combinatorial_uniqueness_flow import (
    INVALID,
    RESOLVED,
    CombinatorialUniquenessFlow,
    ValidityPolicy,
)


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "demonstration" / "combinatorial_uniqueness_v1.json"
POLICY = ValidityPolicy("direct-intersection-test-v1", 0.0, 0.0, 0.0)


class DirectCombinatorialIntersectionFlowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = load_experiment_fixture(MANIFEST)
        cls.flow = CombinatorialUniquenessFlow()
        cls.state = cls.flow.govern_and_compile(cls.fixture.state)

    def test_compilation_contains_only_physical_trait_relations(self):
        expected = sum(len(concept.traits) for concept in self.fixture.state.concepts)

        self.assertEqual(len(self.state.relation_ids), expected)
        self.assertTrue(all(
            relation["id"] == f"fixture:{relation['target']}:{relation['source']}"
            for relation in self.state.graph.relations
        ))
        self.assertFalse(any("legal" in node for node in self.state.graph.vocab))

    def test_direct_prefixes_narrow_to_the_declared_target(self):
        probe = self.fixture.probes.probes["independent_composition_probes"][0]
        execution = self.flow.execute(self.state, probe["constraints"], POLICY)

        self.assertEqual(execution.status, RESOLVED)
        self.assertEqual(execution.top_candidate, probe["target"])
        self.assertEqual(len(execution.prefixes), 4)
        self.assertGreater(
            execution.prefixes[0].normalized_entropy,
            execution.prefixes[-1].normalized_entropy,
        )
        self.assertGreater(
            len(execution.prefixes[0].hard_intersection_candidates),
            len(execution.prefixes[-1].hard_intersection_candidates),
        )

    def test_redundant_dimensions_do_not_manufacture_information(self):
        probe = self.fixture.probes.probes["redundant_composition_probes"][0]
        execution = self.flow.execute(self.state, probe["constraints"], POLICY)

        self.assertEqual(
            execution.prefixes[0].normalized_entropy,
            execution.prefixes[-1].normalized_entropy,
        )
        self.assertEqual(
            execution.prefixes[0].cumulative_structural_information_bits,
            execution.prefixes[-1].cumulative_structural_information_bits,
        )

    def test_declared_physical_exclusion_is_invalid(self):
        probe = self.fixture.probes.probes["invalid_composition_probes"][0]
        execution = self.flow.execute(self.state, probe["constraints"], POLICY)

        self.assertEqual(execution.status, INVALID)
        self.assertEqual(execution.governance_reason_code, "DECLARED_CONTRADICTION")

    def test_compiled_state_remains_immutable_and_reproducible(self):
        probe = self.fixture.probes.probes["independent_composition_probes"][0]
        before = self.flow.execute(self.state, probe["constraints"], POLICY)

        with self.assertRaises(ValueError):
            self.state.graph.transition[0, 0] = 2.0
        with self.assertRaises(TypeError):
            self.state.incidence["storage"] = frozenset()

        after = self.flow.execute(self.state, probe["constraints"], POLICY)
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
