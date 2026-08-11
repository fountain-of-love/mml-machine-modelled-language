import json
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "demonstration"
MANIFEST_PATH = DATA / "combinatorial_uniqueness_v1.json"
STATE_PATH = DATA / "combinatorial_uniqueness_state_v1.json"
PROBES_PATH = DATA / "combinatorial_uniqueness_probes_v1.json"


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


class CombinatorialUniquenessFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = load_json(MANIFEST_PATH)
        cls.state = load_json(STATE_PATH)
        cls.probes = load_json(PROBES_PATH)
        cls.dimension_ids = {item["id"] for item in cls.state["dimensions"]}
        cls.concepts = {item["id"]: item for item in cls.state["concepts"]}

    def test_manifest_binds_matching_state_and_probe_identities(self):
        state_artifact = ROOT / self.manifest["artifacts"]["state"]["path"]
        probe_artifact = ROOT / self.manifest["artifacts"]["probes"]["path"]

        self.assertEqual(state_artifact, STATE_PATH)
        self.assertEqual(probe_artifact, PROBES_PATH)
        self.assertEqual(self.probes["state_id"], self.state["state_id"])
        self.assertEqual(self.probes["holdout_status"], "not_held_out")

    def test_state_references_only_declared_dimensions(self):
        for concept in self.state["concepts"]:
            with self.subTest(concept=concept["id"]):
                self.assertTrue(set(concept["traits"]) <= self.dimension_ids)

        for group in self.state["redundancy_groups"]:
            with self.subTest(group=group["id"]):
                self.assertTrue(set(group["members"]) <= self.dimension_ids)

        for exclusion in self.state["composition_exclusions"]:
            with self.subTest(exclusion=exclusion):
                self.assertIn(exclusion["left"], self.dimension_ids)
                self.assertIn(exclusion["right"], self.dimension_ids)
                self.assertEqual(exclusion["kind"], "fixture_local_exclusion")
                self.assertEqual(exclusion["scope"], self.state["state_id"])

    def test_probe_references_are_valid_and_targets_satisfy_constraints(self):
        for probe in self.probes["independent_composition_probes"]:
            with self.subTest(probe=probe["id"]):
                self.assertIn(probe["target"], self.concepts)
                self.assertTrue(set(probe["constraints"]) <= self.dimension_ids)
                self.assertTrue(
                    set(probe["constraints"])
                    <= set(self.concepts[probe["target"]]["traits"])
                )

        for group_name in (
            "redundant_composition_probes",
            "invalid_composition_probes",
        ):
            for probe in self.probes[group_name]:
                with self.subTest(group=group_name, probe=probe["id"]):
                    self.assertTrue(set(probe["constraints"]) <= self.dimension_ids)

    def test_no_independent_probe_coordinate_is_a_unique_lookup_key(self):
        trait_counts = Counter(
            trait
            for concept in self.state["concepts"]
            for trait in set(concept["traits"])
        )

        for probe in self.probes["independent_composition_probes"]:
            for constraint in probe["constraints"]:
                with self.subTest(probe=probe["id"], constraint=constraint):
                    self.assertGreaterEqual(trait_counts[constraint], 2)

    def test_redundancy_group_has_identical_concept_membership(self):
        group = self.state["redundancy_groups"][0]
        memberships = {
            member: {
                concept["id"]
                for concept in self.state["concepts"]
                if member in concept["traits"]
            }
            for member in group["members"]
        }

        first_membership = next(iter(memberships.values()))
        self.assertTrue(first_membership)
        self.assertTrue(all(value == first_membership for value in memberships.values()))

    def test_invalid_probes_match_declared_fixture_exclusions(self):
        exclusions = {
            frozenset((item["left"], item["right"]))
            for item in self.state["composition_exclusions"]
        }

        for probe in self.probes["invalid_composition_probes"]:
            constraint_pairs = {
                frozenset((left, right))
                for index, left in enumerate(probe["constraints"])
                for right in probe["constraints"][index + 1 :]
            }
            with self.subTest(probe=probe["id"]):
                self.assertTrue(exclusions & constraint_pairs)
                self.assertEqual(probe["expected_status"], "no_valid_intersection")
                self.assertEqual(probe["expected_reason"], "contradictory_constraints")

    def test_fixture_does_not_encode_expected_rank_trajectories(self):
        serialized = json.dumps(self.probes)

        self.assertNotIn("expected_ranks", serialized)
        self.assertNotIn("expected_entropy", serialized)
        self.assertNotIn("expected_margins", serialized)


if __name__ == "__main__":
    unittest.main()
