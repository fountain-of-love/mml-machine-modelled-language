import json
import unittest
from pathlib import Path

import numpy as np

from elaborations.mml_graph import (
    GraphModel,
    graph_snapshot_id,
    load_aliases,
    load_relations,
    stable_sentence_id,
)


ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "data" / "construction" / "gdpr_law_corpus.txt"
RELATIONS = ROOT / "data" / "construction" / "gdpr_relations.jsonl"
ALIASES = ROOT / "data" / "construction" / "gdpr_aliases.jsonl"


def gdpr_model():
    sentences = [line.strip() for line in CORPUS.read_text().splitlines() if line.strip()]
    return GraphModel.from_sources(sentences, load_relations(RELATIONS), load_aliases(ALIASES))


class TypedGraphTests(unittest.TestCase):
    def test_relation_loader_and_probability_conservation(self):
        model = gdpr_model()
        self.assertEqual(15, len(model.relations))
        nonempty = model.transition.sum(axis=1) > 0
        np.testing.assert_allclose(model.transition.sum(axis=1)[nonempty], 1.0)
        self.assertTrue(all(edge[2]["evidence_ids"] for edge in model.typed_adjacency))

    def test_longest_alias_match_adds_governed_concept(self):
        model = gdpr_model()
        self.assertIn("information_control", model.resolve_tokens("the office chooses which records to disclose"))
        self.assertIn("verification_blocked", model.resolve_tokens("a missing chronology prevents review"))
        self.assertTrue(all(alias["evidence_ids"] for alias in model.aliases))

    def test_alias_replaces_matched_span_without_component_leakage(self):
        model = gdpr_model()
        resolved = model.resolve_tokens("selected records")
        self.assertEqual(["information_control"], resolved)

    def test_relation_types_have_declared_distinct_strengths(self):
        base = ["source other", "target other"]
        probabilities = {}
        for relation_type in ("supports", "requires", "qualifies"):
            model = GraphModel.from_sources(base, [{
                "id": relation_type, "source": "source", "relation": relation_type,
                "target": "target", "weight": 1,
                "evidence_ids": ["sentence:80160089b27956e5"],
            }])
            probabilities[relation_type] = model.transition[model.word2idx["source"], model.word2idx["target"]]
        self.assertGreater(probabilities["supports"], probabilities["requires"])
        self.assertGreater(probabilities["requires"], probabilities["qualifies"])

    def test_graph_state_is_read_only(self):
        model = gdpr_model()
        with self.assertRaises(ValueError):
            model.transition[0, 0] = 2
        with self.assertRaises(ValueError):
            model.transition.setflags(write=True)
        with self.assertRaises(TypeError):
            model.word2idx["new"] = 1
        with self.assertRaises(TypeError):
            model.relations[0]["weight"] = 0.1

    def test_invalid_relation_contract_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "unknown relation"):
            GraphModel.from_sources(["alpha beta"], [{
                "id": "r1", "source": "alpha", "relation": "resembles",
                "target": "beta", "weight": 1,
                "evidence_ids": ["sentence:1a989ea86150171c"],
            }])

    def test_governed_sources_reject_typos_and_unstable_identity(self):
        evidence = ["sentence:1a989ea86150171c"]
        with self.assertRaisesRegex(ValueError, "not declared construction nodes"):
            GraphModel.from_sources(["alpha beta"], [{
                "id": "relation:typo", "source": "alphaa", "relation": "supports",
                "target": "beta", "weight": 1, "evidence_ids": evidence,
            }])
        with self.assertRaisesRegex(ValueError, "alias targets are not declared"):
            GraphModel.from_sources(["alpha beta"], aliases=[{
                "id": "alias:typo", "phrase": "alpha phrase", "concept": "betaa",
                "evidence_ids": evidence,
            }])
        with self.assertRaisesRegex(ValueError, "stable governed ID"):
            GraphModel.from_sources(["alpha beta"], [{
                "id": "", "source": "alpha", "relation": "supports",
                "target": "beta", "weight": 1, "evidence_ids": evidence,
            }])
        with self.assertRaisesRegex(ValueError, "unknown sentence evidence"):
            GraphModel.from_sources(["alpha beta"], [{
                "id": "relation:unknown-evidence", "source": "alpha",
                "relation": "supports", "target": "beta", "weight": 1,
                "evidence_ids": ["sentence:0000000000000000"],
            }])
        with self.assertRaisesRegex(ValueError, "polarity"):
            GraphModel.from_sources(["alpha beta"], [{
                "id": "r1", "source": "alpha", "relation": "contradicts",
                "target": "beta", "weight": 1, "polarity": 1,
                "evidence_ids": ["sentence:1a989ea86150171c"],
            }])
        with self.assertRaisesRegex(ValueError, "stable construction sentence"):
            GraphModel.from_sources(["alpha beta"], [{
                "id": "r1", "source": "alpha", "relation": "supports",
                "target": "beta", "weight": 1,
                "evidence_ids": ["sentence:does-not-exist"],
            }])

    def test_contradictions_are_not_negative_transition_weights(self):
        model = gdpr_model()
        self.assertTrue(np.all(model.transition >= 0))
        self.assertGreater(len(model.contradiction_adjacency), 0)
        plain = GraphModel.from_sentences(model.sentences)
        query = "incomplete_disclosure"
        text = "complete_disclosure records"
        self.assertLess(model.score(query, text), plain.score(query, text))

    def test_explanation_score_matches_score_and_paths_are_valid(self):
        model = gdpr_model()
        explanation = model.score_with_explanation(
            "information_control", "the institution selected records", path_limit=2
        )
        self.assertAlmostEqual(
            model.score("information_control", "the institution selected records"),
            explanation["score"],
        )
        self.assertEqual(model.snapshot_id, explanation["snapshot_id"])
        self.assertFalse(explanation["limitations"]["causal_decomposition"])
        self.assertTrue(explanation["paths"])
        known_ids = {record["id"] for record in (*model.relations, *model.aliases)}
        for path in explanation["paths"]:
            self.assertEqual(path["source"], path["nodes"][0])
            self.assertEqual(path["target"], path["nodes"][-1])
            self.assertTrue(all(edge["id"] in known_ids for edge in path["edges"]))

    def test_explanation_is_deterministic_and_bounded(self):
        model = gdpr_model()
        first = model.score_with_explanation("verification_blocked", "withheld chronology", path_limit=1)
        second = model.score_with_explanation("verification_blocked", "withheld chronology", path_limit=1)
        self.assertEqual(first, second)
        self.assertLessEqual(len(first["paths"]), 1)

    def test_snapshot_is_content_addressed(self):
        sentences = ["alpha beta", "beta gamma"]
        self.assertEqual(graph_snapshot_id(sentences), graph_snapshot_id(reversed(sentences)))
        self.assertNotEqual(graph_snapshot_id(sentences), graph_snapshot_id(sentences, steps=4))
        self.assertEqual(stable_sentence_id("Alpha, beta!"), stable_sentence_id("alpha beta"))

    def test_alias_update_changes_snapshot_without_mutating_source(self):
        model = gdpr_model()
        update = {
            "id": "gdpr:alias:new-phrase", "phrase": "records left out",
            "concept": "incomplete_disclosure",
            "evidence_ids": ["sentence:05e8a65d8f029785"],
        }
        changed = model.with_alias_update(update)
        self.assertNotEqual(model.snapshot_id, changed.snapshot_id)
        self.assertNotIn("incomplete_disclosure", model.resolve_tokens("records left out"))
        self.assertIn("incomplete_disclosure", changed.resolve_tokens("records left out"))

    def test_relation_update_is_immutable_and_rollback_exact(self):
        model = gdpr_model()
        original_transition = model.transition.copy()
        update = {
            "id": "gdpr:supports:selected-control",
            "source": "selected", "relation": "supports",
            "target": "information_control", "weight": 0.5, "polarity": 1,
            "evidence_ids": ["sentence:d4b62239822d382e"],
        }
        changed = model.with_relation_update(update)
        self.assertNotEqual(model.snapshot_id, changed.snapshot_id)
        np.testing.assert_array_equal(model.transition, original_transition)
        restored = changed.with_relations(model.relations)
        self.assertEqual(model.snapshot_id, restored.snapshot_id)
        np.testing.assert_array_equal(model.transition, restored.transition)
        self.assertEqual(
            model.score_with_explanation("information_control", "selected records"),
            restored.score_with_explanation("information_control", "selected records"),
        )


if __name__ == "__main__":
    unittest.main()
