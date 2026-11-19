import unittest

from src.knowledge_state_execution.subject_expansion_state import (
    IS_ABOUT,
    NARROWER_THAN,
    NO_DECLARED_CONSEQUENCE,
    OUT_OF_SCOPE,
    RESOLVED,
    GovernedAssertion,
    compile_subject_expansion_state,
    execute_subject_query,
)


EX = "http://example.org/"
ROOT, MID, LEAF, EMPTY, OTHER = (EX + name for name in ("root", "mid", "leaf", "empty", "other"))
W1, W2, W3 = (EX + f"work/{n}" for n in (1, 2, 3))


def a(assertion_id, subject, relation, obj):
    return GovernedAssertion(assertion_id, subject, relation, obj)


HIERARCHY = (
    a("h-mid", MID, NARROWER_THAN, ROOT),
    a("h-leaf", LEAF, NARROWER_THAN, MID),
    a("h-empty", EMPTY, NARROWER_THAN, ROOT),
)
INDEXING = (
    a("i-1-leaf", W1, IS_ABOUT, LEAF),
    a("i-2-mid", W2, IS_ABOUT, MID),
    a("i-1-root", W1, IS_ABOUT, ROOT),
    a("i-3-other", W3, IS_ABOUT, OTHER),
)


class SubjectExpansionStateTests(unittest.TestCase):
    def setUp(self):
        self.state = compile_subject_expansion_state(HIERARCHY + INDEXING)

    def test_expansion_returns_works_about_narrower_concepts(self):
        outcome = execute_subject_query(self.state, ROOT)
        self.assertEqual(outcome.status, RESOLVED)
        self.assertEqual(outcome.works, (W1, W2))
        self.assertEqual(outcome.concepts_expanded, 4)
        self.assertEqual(execute_subject_query(self.state, MID).works, (W1, W2))
        self.assertEqual(execute_subject_query(self.state, LEAF).works, (W1,))

    def test_evidence_chain_runs_from_aboutness_up_to_query(self):
        matches = execute_subject_query(self.state, ROOT).matches
        via_leaf = next(m for m in matches if m.via_concept == LEAF)
        self.assertEqual(via_leaf.evidence, ("i-1-leaf", "h-leaf", "h-mid"))
        direct = next(m for m in matches if m.via_concept == ROOT)
        self.assertEqual(direct.evidence, ("i-1-root",))

    def test_known_concept_without_works_resolves_empty(self):
        outcome = execute_subject_query(self.state, EMPTY)
        self.assertEqual((outcome.status, outcome.works), (RESOLVED, ()))

    def test_unknown_concept_is_refused_not_answered_empty(self):
        outcome = execute_subject_query(self.state, EX + "unknown")
        self.assertEqual((outcome.status, outcome.reason), (NO_DECLARED_CONSEQUENCE, OUT_OF_SCOPE))
        self.assertEqual(outcome.matches, ())

    def test_identities_must_be_absolute_iris(self):
        with self.assertRaises(ValueError):
            execute_subject_query(self.state, "root")
        with self.assertRaises(ValueError):
            compile_subject_expansion_state([a("x", "mid", NARROWER_THAN, ROOT)])

    def test_invalid_governed_input_is_refused(self):
        cases = {
            "empty": [],
            "relation": [a("x", MID, "related-to", ROOT)],
            "duplicate id": [a("x", MID, NARROWER_THAN, ROOT), a("x", LEAF, NARROWER_THAN, MID)],
            "duplicate statement": [a("x", MID, NARROWER_THAN, ROOT), a("y", MID, NARROWER_THAN, ROOT)],
            "cycle": [a("x", MID, NARROWER_THAN, ROOT), a("y", ROOT, NARROWER_THAN, MID)],
        }
        for name, assertions in cases.items():
            with self.subTest(name), self.assertRaises(ValueError):
                compile_subject_expansion_state(assertions)

    def test_compilation_is_order_independent_and_content_addressed(self):
        replay = compile_subject_expansion_state(tuple(reversed(HIERARCHY + INDEXING)))
        self.assertEqual(replay.snapshot_id, self.state.snapshot_id)
        self.assertTrue(self.state.snapshot_id.startswith("sha256:"))

    def test_correction_changes_dependents_and_restoration_is_exact(self):
        corrected = compile_subject_expansion_state(
            [item for item in HIERARCHY + INDEXING if item.assertion_id != "h-leaf"]
        )
        self.assertNotEqual(corrected.snapshot_id, self.state.snapshot_id)
        self.assertEqual(execute_subject_query(corrected, MID).works, (W2,))
        self.assertEqual(execute_subject_query(corrected, OTHER).works, (W3,))
        self.assertEqual(execute_subject_query(self.state, MID).works, (W1, W2))
        restored = compile_subject_expansion_state(HIERARCHY + INDEXING)
        self.assertEqual(restored.snapshot_id, self.state.snapshot_id)

    def test_compiled_state_is_immutable(self):
        with self.assertRaises(TypeError):
            self.state.closure[ROOT] = ()
        with self.assertRaises(TypeError):
            self.state.postings[ROOT] = ()


if __name__ == "__main__":
    unittest.main()
