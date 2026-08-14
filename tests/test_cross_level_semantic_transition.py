import unittest
from pathlib import Path

from experiments.combinatorial_uniqueness.fixture import load_experiment_fixture
from src.combinatorial_uniqueness.combinatorial_uniqueness_flow import RESOLVED, CombinatorialUniquenessFlow, ValidityPolicy
from src.combinatorial_uniqueness.cross_level_semantic_transition import TransitionStage, execute_stage_transition


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "demonstration" / "cross_level_semantic_transition_v1.json"
POLICY = ValidityPolicy("cross-level-transition-test-v1")


class CrossLevelSemanticTransitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = load_experiment_fixture(MANIFEST)
        cls.flow = CombinatorialUniquenessFlow()
        cls.state = cls.flow.govern_and_compile(cls.fixture.state)

    def _execute(self, probe):
        stages = tuple(
            TransitionStage(stage["id"], tuple(stage["constraints"]))
            for stage in probe["stages"]
        )
        return execute_stage_transition(self.flow, self.state, stages, POLICY)

    def test_every_authored_stage_resolves_its_declared_region(self):
        for probe in self.fixture.probes.probes["cross_level_probes"]:
            result = self._execute(probe)
            with self.subTest(probe=probe["id"]):
                self.assertEqual(result.status, RESOLVED)
                self.assertEqual(
                    [stage.execution.top_candidate for stage in result.stages],
                    [stage["expected_region"] for stage in probe["stages"]],
                )

    def test_original_flat_conjunction_failure_is_preserved_as_control(self):
        for probe in self.fixture.probes.probes["cross_level_probes"]:
            result = self._execute(probe)
            with self.subTest(probe=probe["id"]):
                self.assertNotEqual(result.flat_control.status, RESOLVED)
                self.assertFalse(result.flat_control.hard_intersection_candidates)

    def test_transition_trace_exposes_scope_changes_and_antecedent(self):
        probe = self.fixture.probes.probes["cross_level_probes"][0]
        result = self._execute(probe)
        second = result.stages[1]
        self.assertEqual(second.antecedent_region, "selective_access")
        self.assertEqual(second.retained_constraints, ("exclusive_control", "incomplete_disclosure"))
        self.assertEqual(second.released_constraints, ("access", "source_coverage"))
        self.assertEqual(second.introduced_constraints, ("evidence", "dispute"))

    def test_adjacent_stages_require_semantic_continuity(self):
        stages = (
            TransitionStage("one", ("access",)),
            TransitionStage("two", ("evidence",)),
        )
        with self.assertRaisesRegex(ValueError, "retain at least one"):
            execute_stage_transition(self.flow, self.state, stages, POLICY)

    def test_operation_is_deterministic_and_preserves_epistemic_classification(self):
        probe = self.fixture.probes.probes["cross_level_probes"][0]
        first = self._execute(probe)
        second = self._execute(probe)
        self.assertEqual(first, second)
        self.assertTrue(all(
            stage.execution.epistemic_classification == "synthetic_doctrinal_construction"
            for stage in first.stages
        ))


if __name__ == "__main__":
    unittest.main()
