import json
import math
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEVELOPMENT = ROOT / "data" / "development"
REGISTRY_PATH = DEVELOPMENT / "species_registry_canidae_v0_1.json"
ECOLOGY_PATH = DEVELOPMENT / "species_ecology_behavior_seed_canidae_v0_1.json"
DETAIL_PATH = DEVELOPMENT / "canidae_zoological_detail_seed_v0_1.json"

ECOLOGY_DIMENSIONS = {
    "environmental_system",
    "biome",
    "microhabitat",
    "ecological_stratum",
    "climate_zone",
    "trophic_mode",
    "primary_food",
    "activity_cycle",
    "social_organization",
    "locomotor_mode",
    "migratory_strategy",
    "shelter_or_nesting",
    "native_range_realm",
}

DETAIL_DIMENSIONS = {
    "body_mass_band",
    "body_length_band",
    "body_covering",
    "thermoregulation",
    "reproductive_mode",
    "parental_care",
}


def _load(path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


class AnimalEncyclopedicNavigationSeedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = _load(REGISTRY_PATH)
        cls.ecology = _load(ECOLOGY_PATH)
        cls.detail = _load(DETAIL_PATH)

    def test_layers_share_one_species_registry(self):
        registry_ids = {record["species_id"] for record in self.registry["records"]}
        ecology_ids = {record["species_id"] for record in self.ecology["records"]}
        detail_ids = {record["species_id"] for record in self.detail["records"]}

        self.assertEqual(len(registry_ids), 12)
        self.assertEqual(registry_ids, ecology_ids)
        self.assertEqual(registry_ids, detail_ids)
        self.assertEqual(
            self.ecology["species_registry_state_id"], self.registry["state_id"]
        )
        self.assertEqual(
            self.detail["species_registry_state_id"], self.registry["state_id"]
        )

    def test_conceptual_and_zoological_dimensions_are_disjoint(self):
        self.assertEqual(set(self.ecology["dimensions"]), ECOLOGY_DIMENSIONS)
        self.assertEqual(set(self.detail["dimensions"]), DETAIL_DIMENSIONS)
        self.assertFalse(ECOLOGY_DIMENSIONS & DETAIL_DIMENSIONS)
        self.assertNotIn("taxonomic_class", ECOLOGY_DIMENSIONS | DETAIL_DIMENSIONS)

    def test_original_navigation_anchors_are_explicit(self):
        roles = {
            group["anchor_role"]
            for concept in self.ecology["semantic_hierarchy"]
            for group in concept["children"]
            if "anchor_role" in group
        }
        self.assertEqual(roles, {"habitat", "diet", "activity", "sociality"})
        self.assertEqual(
            set(self.ecology["conceptual_contract"]["original_anchor_roles"]),
            roles,
        )
        self.assertEqual(
            self.ecology["conceptual_contract"]["identity_expression"],
            "ecology_and_behavior",
        )

    def test_each_hierarchy_owns_every_dimension_once(self):
        for seed in (self.ecology, self.detail):
            nested = [
                dimension
                for concept in seed["semantic_hierarchy"]
                for group in concept["children"]
                for dimension in group["dimensions"]
            ]
            self.assertEqual(len(nested), len(set(nested)))
            self.assertEqual(set(nested), set(seed["dimensions"]))

    def test_populated_claims_have_resolvable_provenance(self):
        for seed in (self.ecology, self.detail):
            for record in seed["records"]:
                self.assertEqual(set(record["dimensions"]), set(seed["dimensions"]))
                for claims in record["dimensions"].values():
                    for claim in claims:
                        self.assertIn(claim["source_id"], seed["sources"])
                        self.assertTrue(claim["source_locator"])
                        if claim["evidence_type"] == "derived":
                            self.assertIn(claim["mapping_rule_id"], seed["mapping_rules"])

    def test_quality_metrics_are_reproducible_per_layer(self):
        for seed in (self.ecology, self.detail):
            cells = [
                claims
                for record in seed["records"]
                for claims in record["dimensions"].values()
            ]
            claims = [claim for cell in cells for claim in cell]
            quality = seed["data_quality"]

            self.assertEqual(quality["populated_dimension_cells"], sum(map(bool, cells)))
            self.assertEqual(quality["empty_dimension_cells"], sum(not cell for cell in cells))
            self.assertEqual(quality["populated_claims"], len(claims))
            self.assertAlmostEqual(
                quality["dimension_cell_completeness"],
                sum(map(bool, cells)) / len(cells),
                places=6,
            )

    def test_missing_values_are_not_counted_as_partition_information(self):
        for seed in (self.ecology, self.detail):
            for dimension, reported in seed["dimension_statistics"].items():
                signatures = [
                    tuple(sorted(claim["value"] for claim in record["dimensions"][dimension]))
                    for record in seed["records"]
                ]
                observed = [signature for signature in signatures if signature]
                counts = Counter(observed)
                entropy = -sum(
                    (count / len(observed)) * math.log2(count / len(observed))
                    for count in counts.values()
                ) if observed else 0.0

                self.assertEqual(reported["populated_record_count"], len(observed))
                self.assertAlmostEqual(
                    reported["observed_partition_entropy_bits"], entropy, places=6
                )

    def test_registry_owns_identity_and_consultation_sources(self):
        for record in self.registry["records"]:
            self.assertEqual(record["identity"]["catalogue_match"], "EXACT")
            self.assertEqual(len(record["consultation_sources"]), 5)
            self.assertTrue(all(
                source["url"].startswith("https://")
                for source in record["consultation_sources"]
            ))
        for seed in (self.ecology, self.detail):
            self.assertTrue(all("identity" not in record for record in seed["records"]))

    def test_body_length_harmonization_exists_only_in_detail(self):
        self.assertNotIn("body_length_review", self.ecology["data_quality"])
        self.assertEqual(
            self.detail["data_quality"]["body_length_measurement_review"]["canonical_claim_count"],
            12,
        )
        for record in self.detail["records"]:
            claim = record["dimensions"]["body_length_band"][0]
            observation = record["source_observations"]["pantheria_1_0_msw05"]
            self.assertEqual(claim["source_id"], "pantheria_1_0_msw05")
            self.assertGreater(observation["adult_head_body_length_mm"], 0)
            self.assertIn("measurement_review", record)

    def test_detail_observations_do_not_reintroduce_conceptual_fields(self):
        excluded_adw_fields = {
            "habitat_regions",
            "terrestrial_biomes",
            "other_habitat_features",
            "key_behaviors",
            "shelter_projection_values",
        }
        for record in self.detail["records"]:
            observations = record["source_observations"]
            self.assertNotIn("diet_percent", observations["eltontraits_1_0_mammals"])
            self.assertNotIn("activity_flags", observations["eltontraits_1_0_mammals"])
            self.assertFalse(
                excluded_adw_fields
                & set(observations["animal_diversity_web_species_account"])
            )


if __name__ == "__main__":
    unittest.main()
