import unittest
from pathlib import Path

from combinatorial_uniqueness_fixture import load_experiment_fixture
from combinatorial_uniqueness_flow import (
    RESOLVED,
    UNRESOLVED,
    CombinatorialUniquenessFlow,
    ValidityPolicy,
)


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "demonstration" / "governed_legal_qualification_v1.json"
POLICY = ValidityPolicy("legal-qualification-test-v1", 0.0, 0.0, 0.0)


class GovernedLegalQualificationFlowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = load_experiment_fixture(MANIFEST)
        cls.flow = CombinatorialUniquenessFlow()
        cls.state = cls.flow.govern_and_compile(cls.fixture.state)

    def test_compilation_contains_only_legal_trait_relations(self):
        expected = sum(len(concept.traits) for concept in self.fixture.state.concepts)
        self.assertEqual(len(self.state.relation_ids), expected)
        self.assertFalse(any(node in {"capacitor", "spring", "reservoir"} for node in self.state.graph.vocab))

    def test_direct_qualification_resolves_declared_region(self):
        probe = self.fixture.probes.probes["independent_composition_probes"][0]
        execution = self.flow.execute(self.state, probe["constraints"], POLICY)
        self.assertEqual(execution.status, RESOLVED)
        self.assertEqual(execution.top_candidate, probe["target"])
        self.assertGreater(execution.prefixes[0].normalized_entropy, execution.prefixes[-1].normalized_entropy)

    def test_unsupported_legal_combination_remains_unresolved(self):
        probe = self.fixture.probes.probes["unsupported_composition_probes"][0]
        execution = self.flow.execute(self.state, probe["constraints"], POLICY)
        self.assertEqual(execution.status, UNRESOLVED)
        self.assertEqual(execution.governance_reason_code, "UNSUPPORTED_COMBINATION")

    def test_contrast_branches_resolve_differently(self):
        probe = self.fixture.probes.probes["contrast_probes"][0]
        targets = []
        for branch in probe["branches"]:
            constraints = tuple(probe["shared_constraints"]) + tuple(branch["additional_constraints"])
            execution = self.flow.execute(self.state, constraints, POLICY)
            self.assertEqual(execution.status, RESOLVED)
            self.assertEqual(execution.top_candidate, branch["expected_region"])
            targets.append(execution.top_candidate)
        self.assertEqual(len(set(targets)), 2)

    def test_epistemic_classification_cannot_be_promoted(self):
        probe = self.fixture.probes.probes["independent_composition_probes"][0]
        execution = self.flow.execute(self.state, probe["constraints"], POLICY)
        self.assertEqual(execution.epistemic_classification, "synthetic_doctrinal_construction")
        self.assertNotIn(execution.epistemic_classification, self.fixture.state.epistemic_positions)


if __name__ == "__main__":
    unittest.main()
