import unittest
import json
import tempfile
from dataclasses import replace
from types import MappingProxyType
from pathlib import Path

import numpy as np

from experiments.combinatorial_uniqueness.fixture import (
    DEVELOPMENT_LIFECYCLE, _freeze_instant, _validate_epistemic_contract,
    load_experiment_fixture,
)
from src.combinatorial_uniqueness.combinatorial_uniqueness_flow import (
    INVALID, RESOLVED, UNRESOLVED, CombinatorialUniquenessFlow, ValidityPolicy,
)
from elaborations.mml_graph import GraphModel


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "demonstration"


class CombinatorialUniquenessFlowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.physical = load_experiment_fixture(DATA / "combinatorial_uniqueness_v1.json")
        cls.legal = load_experiment_fixture(DATA / "combinatorial_uniqueness_legal_banking_v1.json")
        cls.flow = CombinatorialUniquenessFlow()
        cls.diagnostic_policy = ValidityPolicy(policy_id="zero-threshold-diagnostic-v1")
        cls.physical_state = cls.flow.govern_and_compile(cls.physical.state)
        cls.legal_state = cls.flow.govern_and_compile(cls.legal.state)

    def test_manifest_state_probe_identity_and_development_status(self):
        self.assertEqual(self.physical.state.state_id, self.physical.probes.state_id)
        self.assertEqual(self.physical.lifecycle, DEVELOPMENT_LIFECYCLE)
        self.assertEqual(self.physical.probes.holdout_status, "not_held_out")

    def test_compiler_creates_only_ordinary_trait_relations(self):
        state = self.physical_state
        expected = sum(len(item.traits) for item in self.physical.state.concepts)
        self.assertEqual(len(state.relation_ids), expected)
        self.assertTrue(all(record["relation"] == "supports" for record in state.graph.relations))
        self.assertFalse(any("independent_capacitor" in item for item in state.relation_ids))

    def test_prefix_execution_and_candidate_only_metrics(self):
        result = self.flow.execute(self.physical_state, ("storage", "electrical", "reversible", "electrostatic"), self.diagnostic_policy)
        self.assertEqual(len(result.prefixes), 4)
        self.assertTrue(all(len(prefix.candidate_values) == len(self.physical_state.concepts) for prefix in result.prefixes))
        self.assertTrue(all(np.isclose(sum(prefix.candidate_values), 1.0) for prefix in result.prefixes))
        self.assertEqual(result.top_candidate, "capacitor")
        self.assertEqual(result.status, RESOLVED)

    def test_prefix_carries_selected_top_k_and_actual_top_k_mass(self):
        result = self.flow.execute(self.physical_state, ("storage",), self.diagnostic_policy)
        prefix = result.prefixes[0]
        self.assertEqual(prefix.top_k, 3)
        self.assertGreater(prefix.top_k_mass, prefix.concentration)
        expected = sum(sorted(prefix.candidate_values, reverse=True)[:prefix.top_k])
        self.assertAlmostEqual(prefix.top_k_mass, expected)

    def test_conditional_information_is_incidence_based(self):
        result = self.flow.execute(self.physical_state, ("storage", "containment", "retention"), self.diagnostic_policy)
        self.assertEqual(result.prefixes[1].cumulative_structural_information_bits, result.prefixes[0].cumulative_structural_information_bits)
        self.assertEqual(result.prefixes[2].cumulative_structural_information_bits, result.prefixes[1].cumulative_structural_information_bits)

    def test_scoped_exclusion_is_invalid(self):
        result = self.flow.execute(self.physical_state, ("storage", "electrical", "biological"), self.diagnostic_policy)
        self.assertEqual((result.status, result.reason_code), (INVALID, "DECLARED_CONTRADICTION"))
        self.assertEqual(result.governance_status, INVALID)
        self.assertNotEqual(result.mechanism_reason_code, "DECLARED_CONTRADICTION")

    def test_unsupported_legal_combination_remains_unresolved(self):
        probe = self.legal.probes.probes["unsupported_composition_probes"][0]
        result = self.flow.execute(self.legal_state, probe["constraints"], self.diagnostic_policy)
        self.assertEqual((result.status, result.reason_code), (UNRESOLVED, "UNSUPPORTED_COMBINATION"))
        self.assertEqual(result.mechanism_status, RESOLVED)
        self.assertEqual(result.governance_status, UNRESOLVED)

    def test_epistemic_position_cannot_be_promoted_by_resolution(self):
        result = self.flow.execute(
            self.legal_state,
            ("access", "incomplete_disclosure", "source_coverage", "exclusive_control"),
            self.diagnostic_policy,
        )
        self.assertEqual(result.epistemic_classification, "synthetic_doctrinal_construction")
        with self.assertRaises(TypeError):
            self.flow.execute(
                self.legal_state, ("access",), self.diagnostic_policy,
                epistemic_position="directly_established_fact",
            )

    def test_soft_leader_and_hard_governance_oracle_are_distinct(self):
        result = self.flow.execute(self.physical_state, ("storage", "electrical", "reversible", "electrostatic"), self.diagnostic_policy)
        self.assertIn(result.top_candidate, result.hard_intersection_candidates)
        self.assertEqual(result.soft_top_candidate, result.top_candidate)

    def test_zero_hard_intersection_has_no_resolved_or_arbitrary_top(self):
        probe = self.legal.probes.probes["unsupported_composition_probes"][0]
        result = self.flow.execute(self.legal_state, probe["constraints"], self.diagnostic_policy)
        self.assertIsNone(result.top_candidate)
        self.assertEqual(result.hard_intersection_candidates, ())
        self.assertTrue(all(prefix.cumulative_structural_information_bits is None for prefix in result.prefixes[-1:]))

    def test_zero_numeric_candidate_support_has_null_metrics_and_no_top(self):
        isolated = GraphModel.from_sentences(("dimension", "concept"), damping=1.0)
        state = replace(
            self.physical_state,
            graph=isolated,
            concepts=("concept",),
            dimensions=("dimension",),
            incidence=MappingProxyType({"dimension": frozenset(("concept",))}),
        )
        result = self.flow.execute(state, ("dimension",), self.diagnostic_policy)
        prefix = result.prefixes[0]
        self.assertIsNone(prefix.candidate_values)
        self.assertIsNone(prefix.entropy)
        self.assertIsNone(prefix.concentration)
        self.assertIsNone(result.top_candidate)
        self.assertEqual((result.status, result.reason_code), (UNRESOLVED, "INSUFFICIENT_FIELD_SUPPORT"))

    def test_compiled_state_is_deterministic_and_numeric_arrays_are_read_only(self):
        again = self.flow.govern_and_compile(self.physical.state)
        self.assertEqual(self.physical_state.snapshot_id, again.snapshot_id)
        self.assertFalse(self.physical_state.graph.transition.flags.writeable)
        with self.assertRaises(TypeError):
            self.physical_state.incidence["storage"] = frozenset()

    def test_all_compiled_graph_mutation_surfaces_are_closed(self):
        state = self.physical_state
        before = self.flow.execute(
            state, ("storage", "electrical", "reversible", "electrostatic"),
            self.diagnostic_policy,
        )
        for array in (
            state.graph.transition, state.graph.background, state.graph.token_idf,
            state.graph.inverse_degree,
        ):
            with self.assertRaises(ValueError):
                array.flat[0] = 99.0
            with self.assertRaises(ValueError):
                array.setflags(write=True)
        with self.assertRaises(TypeError):
            state.graph.word2idx["injected"] = 0
        with self.assertRaises(TypeError):
            state.graph.relations[0]["weight"] = 0.2
        with self.assertRaises(AttributeError):
            state.incidence["storage"].add("injected")
        after = self.flow.execute(
            state, ("storage", "electrical", "reversible", "electrostatic"),
            self.diagnostic_policy,
        )
        self.assertEqual(before, after)
        self.assertEqual(state.snapshot_id, self.physical_state.snapshot_id)

    def test_epistemic_classification_is_separate_and_malformed_contracts_rejected(self):
        classification, positions, rule = _validate_epistemic_contract({
            "fixture_position": "synthetic_doctrinal_construction",
            "positions": ["directly_established_fact", "reasonable_inference"],
            "rule": "preserve",
        })
        self.assertNotIn(classification, positions)
        self.assertEqual(rule, "preserve")
        for malformed in (
            {"fixture_position": "directly_established_fact", "positions": ["directly_established_fact"], "rule": "preserve"},
            {"fixture_position": "synthetic", "positions": "reasonable_inference", "rule": "preserve"},
            {"fixture_position": "synthetic", "positions": ["reasonable_inference"], "rule": ""},
        ):
            with self.subTest(malformed=malformed), self.assertRaises(ValueError):
                _validate_epistemic_contract(malformed)

    def test_loader_rejects_artifacts_outside_governed_data_directory(self):
        manifest = json.loads((DATA / "combinatorial_uniqueness_v1.json").read_text())
        manifest["artifacts"]["state"]["path"] = "README.md"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.json"
            path.write_text(json.dumps(manifest))
            with self.assertRaisesRegex(ValueError, "data/demonstration"):
                load_experiment_fixture(path)

    def test_loader_rejects_inconsistent_lifecycle(self):
        manifest = json.loads((DATA / "combinatorial_uniqueness_v1.json").read_text())
        manifest["artifacts"]["state"]["freeze_status"] = "state_frozen"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.json"
            path.write_text(json.dumps(manifest))
            with self.assertRaisesRegex(ValueError, "lifecycle"):
                load_experiment_fixture(path)

    def test_execute_requires_an_explicit_versioned_policy(self):
        with self.assertRaises(TypeError):
            self.flow.execute(self.physical_state, ("storage",))
        with self.assertRaisesRegex(ValueError, "policy_id"):
            ValidityPolicy(policy_id="")

    def test_freeze_timestamps_require_timezone_aware_iso_instants(self):
        for invalid in ("tomorrow", "2026-08-11T10:00:00"):
            with self.subTest(invalid=invalid), self.assertRaisesRegex(ValueError, "timezone-aware"):
                _freeze_instant(invalid, "frozen_at")

    def test_freeze_timestamp_offsets_compare_as_instants(self):
        utc = _freeze_instant("2026-08-11T10:00:00Z", "frozen_at")
        offset = _freeze_instant("2026-08-11T12:00:00+02:00", "frozen_at")
        earlier = _freeze_instant("2026-08-11T09:59:59Z", "frozen_at")
        self.assertEqual(utc, offset)
        self.assertGreater(utc, earlier)
        self.assertFalse(earlier >= utc)  # reversed freeze order remains invalid


if __name__ == "__main__":
    unittest.main()
