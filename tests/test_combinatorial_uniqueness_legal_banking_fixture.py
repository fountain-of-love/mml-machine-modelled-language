import json
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "demonstration"
MANIFEST_PATH = DATA / "combinatorial_uniqueness_legal_banking_v1.json"
STATE_PATH = DATA / "combinatorial_uniqueness_legal_banking_state_v1.json"
PROBES_PATH = DATA / "combinatorial_uniqueness_legal_banking_probes_v1.json"


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


class LegalBankingCombinatorialFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = load_json(MANIFEST_PATH)
        cls.state = load_json(STATE_PATH)
        cls.probes = load_json(PROBES_PATH)
        cls.dimension_ids = {item["id"] for item in cls.state["dimensions"]}
        cls.dimension_families = set(cls.state["dimension_families"])
        cls.concepts = {item["id"]: item for item in cls.state["concepts"]}

    def test_manifest_binds_development_state_and_probes(self):
        self.assertEqual(
            ROOT / self.manifest["artifacts"]["state"]["path"], STATE_PATH
        )
        self.assertEqual(
            ROOT / self.manifest["artifacts"]["probes"]["path"], PROBES_PATH
        )
        self.assertEqual(self.probes["state_id"], self.state["state_id"])
        self.assertEqual(self.probes["holdout_status"], "not_held_out")

    def test_state_has_explicit_non_adjudicative_evidence_boundary(self):
        boundary = self.state["evidence_boundary"].lower()
        self.assertIn("does not", boundary)
        self.assertIn("real institution", boundary)
        self.assertEqual(
            self.state["epistemic_contract"]["fixture_position"],
            "synthetic_doctrinal_construction",
        )
        self.assertEqual(len(self.state["epistemic_contract"]["positions"]), 5)

    def test_state_references_declared_dimensions_and_families(self):
        for dimension in self.state["dimensions"]:
            with self.subTest(dimension=dimension["id"]):
                self.assertIn(dimension["family"], self.dimension_families)

        for concept in self.state["concepts"]:
            with self.subTest(concept=concept["id"]):
                self.assertTrue(set(concept["traits"]) <= self.dimension_ids)

        for group in self.state["redundancy_groups"]:
            with self.subTest(group=group["id"]):
                self.assertTrue(set(group["members"]) <= self.dimension_ids)

    def test_independent_probe_terms_are_broad_and_full_intersections_are_unique(self):
        trait_counts = Counter(
            trait
            for concept in self.state["concepts"]
            for trait in set(concept["traits"])
        )

        for probe in self.probes["independent_composition_probes"]:
            constraints = set(probe["constraints"])
            matches = [
                concept["id"]
                for concept in self.state["concepts"]
                if constraints <= set(concept["traits"])
            ]
            with self.subTest(probe=probe["id"]):
                self.assertIn(probe["target"], self.concepts)
                self.assertTrue(constraints <= self.dimension_ids)
                self.assertTrue(
                    constraints <= set(self.concepts[probe["target"]]["traits"])
                )
                self.assertTrue(
                    all(trait_counts[constraint] >= 2 for constraint in constraints)
                )
                self.assertEqual(matches, [probe["target"]])

    def test_cross_level_and_contrast_regions_are_declared_concepts(self):
        for probe in self.probes["cross_level_probes"]:
            for stage in probe["stages"]:
                with self.subTest(probe=probe["id"], stage=stage):
                    self.assertTrue(set(stage["constraints"]) <= self.dimension_ids)
                    if "expected_region" in stage:
                        self.assertIn(stage["expected_region"], self.concepts)

        for probe in self.probes["contrast_probes"]:
            self.assertTrue(set(probe["shared_constraints"]) <= self.dimension_ids)
            for branch in probe["branches"]:
                constraints = set(probe["shared_constraints"]) | set(
                    branch["additional_constraints"]
                )
                target = self.concepts[branch["expected_region"]]
                with self.subTest(probe=probe["id"], branch=branch["id"]):
                    self.assertTrue(constraints <= set(target["traits"]))

    def test_unsupported_probes_are_not_disguised_expected_conclusions(self):
        for probe in self.probes["unsupported_composition_probes"]:
            with self.subTest(probe=probe["id"]):
                self.assertTrue(set(probe["constraints"]) <= self.dimension_ids)
                self.assertEqual(probe["expected_status"], "no_valid_intersection")
                self.assertEqual(probe["expected_reason"], "unsupported_combination")
                self.assertNotIn("target", probe)

    def test_fixture_does_not_encode_expected_metric_trajectories(self):
        serialized = json.dumps(self.probes)

        self.assertNotIn("expected_ranks", serialized)
        self.assertNotIn("expected_entropy", serialized)
        self.assertNotIn("expected_margins", serialized)


if __name__ == "__main__":
    unittest.main()
