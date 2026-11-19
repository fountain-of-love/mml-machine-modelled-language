import contextlib
import io
import unittest

import numpy as np

from experiments.semantic_representation.opposition import demo
from experiments.semantic_representation.opposition.analysis import (
    stage_cell_types,
    stage_dimension_mixing,
    stage_encoding_loss,
    stage_evaluation,
    stage_lookup,
    stage_two_hop,
    stage_validate_learned,
)
from experiments.semantic_representation.opposition.fixture import governed_matrix, load_fixture
from experiments.semantic_representation.opposition.learned import learned_relation
from experiments.semantic_representation.opposition.metrics import auc, binary_report, entropy_bits
from experiments.semantic_representation.opposition.report import render, run_reports
from src.semantic_representation.relation_encoding import (
    ALIKE,
    OPPOSITE,
    build_signed_matrix,
    related,
    to_binary,
    to_degree,
    to_three_states,
    two_hop,
)


LABELS = ("a", "b", "c", "d")
RELATIONS = (
    {"a": "a", "b": "b", "value": -1.0},
    {"a": "b", "b": "c", "value": -1.0},
    {"a": "a", "b": "d", "value": 0.0},
)


class RelationEncodingTests(unittest.TestCase):
    def setUp(self):
        self.m = build_signed_matrix(LABELS, RELATIONS)

    def test_matrix_is_symmetric_with_alike_diagonal(self):
        np.testing.assert_array_equal(self.m.values, self.m.values.T)
        np.testing.assert_array_equal(np.diag(self.m.values), np.ones(4))

    def test_projections_are_explicit(self):
        self.assertEqual(to_binary(self.m)[0, 1], 1)
        self.assertEqual(to_binary(self.m)[0, 0], 0)
        self.assertEqual(to_degree(self.m)[0, 1], 1.0)
        self.assertEqual(to_degree(self.m)[0, 2], 0.5)
        self.assertEqual(to_three_states(np.array([-0.5, -0.49, 0.49, 0.5])).tolist(), [-1, 0, 0, 1])

    def test_one_matrix_answers_both_polarities(self):
        self.assertEqual(related(self.m, "a", OPPOSITE), (("b", 1.0),))
        self.assertEqual(related(self.m, "a", ALIKE), ())
        with self.assertRaises(ValueError):
            related(self.m, "a", 0)

    def test_opposite_of_opposite_is_alike(self):
        self.assertEqual(two_hop(self.m)[0, 2], 1.0)

    def test_explicit_neutral_differs_from_unstated(self):
        asserted = self.m.is_asserted()
        self.assertTrue(asserted[0, 3])
        self.assertFalse(asserted[0, 2])
        self.assertEqual(self.m.values[0, 3], self.m.values[0, 2])

    def test_invalid_governance_is_refused(self):
        cases = {
            "undeclared": [{"a": "a", "b": "z", "value": 0.1}],
            "self": [{"a": "a", "b": "a", "value": 0.1}],
            "range": [{"a": "a", "b": "b", "value": 1.5}],
            "twice": [{"a": "a", "b": "b", "value": 0.1}, {"a": "b", "b": "a", "value": 0.2}],
        }
        for name, relations in cases.items():
            with self.subTest(name), self.assertRaises(ValueError):
                build_signed_matrix(LABELS, relations)

    def test_matrix_is_immutable(self):
        with self.assertRaises(ValueError):
            self.m.values[0, 1] = 0.0


class MetricTests(unittest.TestCase):
    def test_auc_counts_ties_as_half(self):
        self.assertEqual(auc(np.array([1.0, 0.0]), np.array([True, False])), 1.0)
        self.assertEqual(auc(np.array([0.5, 0.5]), np.array([True, False])), 0.5)

    def test_binary_report_and_entropy(self):
        report = binary_report(np.array([1, 1, 0, 0]), np.array([1, 0, 1, 0]))
        self.assertEqual((report.sensitivity, report.specificity), (0.5, 0.5))
        self.assertAlmostEqual(entropy_bits(np.array([0, 1])), 1.0)


class AnimalOppositionStageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fixture = load_fixture()
        cls.governed, cls.learned = governed_matrix(fixture), learned_relation(fixture)

    def test_stages_one_to_three_answer_the_same_question(self):
        lookup = stage_lookup(self.governed, "cat")
        self.assertEqual(lookup["binary_opposites"], ["dog", "mouse"])
        self.assertEqual(lookup["degree_ranking"][0], ("mouse", 1.0))
        self.assertEqual(lookup["signed_alike"], (("lion", 0.5), ("tiger", 0.5)))

    def test_richer_encodings_carry_more_information(self):
        entropy = stage_encoding_loss(self.governed)["entropy_bits"]
        self.assertLess(entropy["binary"], entropy["three_states"])
        self.assertLess(entropy["three_states"], entropy["graded_values"])

    def test_composition_proposes_and_conflicts_are_reported(self):
        result = stage_two_hop(self.governed)
        self.assertIn(("dog", "mouse", 0.6), [(c["a"], c["b"], c["inferred"]) for c in result["candidates"]])
        conflicts = {(c["a"], c["b"]) for c in result["conflicts"]}
        self.assertIn(("dog", "sheep"), conflicts)
        self.assertIn(("zebra", "tiger"), conflicts)  # explicit neutrality is respected

    def test_validation_exposes_distributional_failure(self):
        validation = stage_validate_learned(self.governed, self.learned)
        self.assertEqual(validation["checked_pairs"], 10)
        self.assertLess(validation["alike_vs_opposite_auc"], 0.5)
        lion_zebra = next(f for f in validation["flags"] if {f["a"], f["b"]} == {"lion", "zebra"})
        self.assertEqual(lion_zebra["verdict"], "SIGN_CONTRADICTS")

    def test_linear_rescaling_does_not_change_the_measures(self):
        ev = stage_evaluation(self.governed, self.learned)
        self.assertEqual(ev["degree_threshold_half"], ev["signed_threshold_zero"])
        self.assertEqual(ev["auc_degree"], ev["auc_signed"])
        self.assertLess(ev["three_states"].macro_f1, ev["three_states"].accuracy)

    def test_cell_type_changes_results(self):
        rows = {(r["type"], r["scale"]): r for r in stage_cell_types(self.governed, self.learned)}
        uint8 = rows[("uint8: x255", "degree")]
        self.assertFalse(uint8["neutral_exact"])
        self.assertEqual(uint8["governed_states_kept"], 41)
        self.assertTrue(rows[("int8: x127", "signed")]["neutral_exact"])
        self.assertEqual(rows[("int8: three states", "signed")]["learned_auc"], 0.5)
        self.assertLess(rows[("float16", "signed")]["resolution_at_neutral"],
                        rows[("float16", "degree")]["resolution_at_neutral"])

    def test_two_tension_observation_is_measured(self):
        fixture = load_fixture()
        mixing = stage_dimension_mixing(self.governed, fixture["relations"])
        kinds = {(c["a"], c["b"]): c["classification"] for c in mixing["conflicts"]}
        self.assertEqual(kinds[("dog", "sheep")], "MIXED_PATH")
        self.assertEqual(kinds[("dog", "wolf")], "TARGET_ON_OTHER_AXIS")
        self.assertEqual(kinds[("wolf", "bear")], "SAME_AXIS")
        self.assertEqual(mixing["conflicts_crossing_axes"], 4)
        self.assertIn(("dog", "mouse"), [(c["a"], c["b"]) for c in mixing["single_axis_candidates"]])

    def test_reports_are_reader_first_and_linked(self):
        reports = run_reports()
        self.assertEqual(reports["main"]["conformity"]["verdict"], "MECHANISM_CONFORMANT")
        self.assertEqual(reports["cell_types"]["conformity"]["verdict"], "MECHANISM_CONFORMANT")
        self.assertEqual(reports["two_tensions"]["conformity"]["verdict"], "EXPLORATORY_SIGNAL")
        main = render(reports, "main")
        for marker in ("## OSCARC", "### R —", "### Signal 1 — The storage type changes meaning",
                       "(opposition-cell-types-v1.md)", "(opposition-two-tensions-v1.md)",
                       "Path 2 — Train, test, tune"):
            self.assertIn(marker, main)
        self.assertLess(main.index("cat and a mouse"), main.index("Technically:"))
        for key in ("cell_types", "two_tensions"):
            self.assertIn("(opposition-matrices-v1.md)", render(reports, key))

    def test_plain_examples_are_computed_from_the_data(self):
        reports = run_reports()
        uint8 = next(r for r in reports["cell_types"]["cell_types"] if r["type"].startswith("uint8"))
        self.assertEqual(uint8["governed_states_changed"], ["cat–lion", "cat–tiger", "dog–sheep", "sheep–bear"])
        self.assertIn("cat–lion, cat–tiger, dog–sheep and sheep–bear", render(reports, "cell_types"))
        self.assertNotIn("lion and the tiger stop", render(reports, "cell_types"))

    def test_demo_runs_all_seven_stages(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            demo.main()
        for stage in range(1, 8):
            self.assertIn(f"=== Stage {stage}:", output.getvalue())


if __name__ == "__main__":
    unittest.main()
