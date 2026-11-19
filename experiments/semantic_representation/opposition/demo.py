"""Animal opposition, in seven small steps. Run: ``make run-opposition``.

1. Binary matrix        opposite or not (1/0)
2. Degree matrix        how opposite, in [0, 1]
3. Signed matrix        opposite / neutral / alike, in [-1, 1]
4. Composition          opposite of an opposite, as a candidate only
5. Validate learning    check a learned relation against the governed one
6. Evaluate             IR measures, and what the scale does or does not change
7. Cell types           how int, decimal, and float precision shape the space
"""

from __future__ import annotations

import numpy as np

from experiments.semantic_representation.opposition.analysis import (
    stage_cell_types,
    stage_encoding_loss,
    stage_evaluation,
    stage_lookup,
    stage_two_hop,
    stage_validate_learned,
)
from experiments.semantic_representation.opposition.fixture import governed_matrix, load_fixture
from experiments.semantic_representation.opposition.learned import learned_relation
from src.semantic_representation.relation_encoding import to_binary, to_degree

QUERY = "cat"


def _title(number: int, text: str) -> None:
    print(f"\n=== Stage {number}: {text} ===")


def _matrix(labels, values, cell) -> None:
    width = max(len(label) for label in labels)
    print(" " * (width + 1) + " ".join(f"{label[:5]:>5}" for label in labels))
    for label, row in zip(labels, values):
        print(f"{label:>{width}} " + " ".join(f"{cell(v):>5}" for v in row))


def _pairs(items) -> str:
    return ", ".join(f"{name} {value:.2f}" for name, value in items) or "none"


def main() -> None:
    fixture = load_fixture()
    governed, learned = governed_matrix(fixture), learned_relation(fixture)
    labels = governed.labels
    lookup = stage_lookup(governed, QUERY)
    loss = stage_encoding_loss(governed)

    _title(1, "binary matrix (1 = opposite)")
    _matrix(labels, to_binary(governed), lambda v: "1" if v else ".")
    print(f"\nopposite_of({QUERY}) = one_hot({QUERY}) @ B  ->  {', '.join(lookup['binary_opposites'])}")
    print(f"Lost: {loss['binary_zeros_that_are_alike']} 'alike' pairs and "
          f"{loss['binary_zeros_that_are_neutral']} neutral pairs are all just 0.")

    _title(2, "degree matrix (1 = opposite, 0.5 = neutral, 0 = alike)")
    _matrix(labels, to_degree(governed), lambda v: f"{v:.2f}")
    print(f"\nRanking for {QUERY}: {_pairs(lookup['degree_ranking'])}")
    print("A threshold is now a choice; 0.5 is the neutral midpoint.")

    _title(3, "signed matrix (-1 opposite, 0 neutral, +1 alike)")
    _matrix(labels, governed.values, lambda v: f"{v:+.1f}" if v else "0")
    print(f"\nSame matrix, opposite functions (W_equal = I, W_opposite = -I):")
    print(f"  alike({QUERY})    = positive part of  S[{QUERY}]  ->  {_pairs(lookup['signed_alike'])}")
    print(f"  opposite({QUERY}) = positive part of -S[{QUERY}]  ->  {_pairs(lookup['signed_opposites'])}")
    entropy = loss["entropy_bits"]
    print(f"Information per pair: binary {entropy['binary']:.2f} bits, three states "
          f"{entropy['three_states']:.2f} bits, graded values {entropy['graded_values']:.2f} bits.")

    _title(4, "composition: S @ S (opposite of an opposite)")
    composition = stage_two_hop(governed)
    for c in composition["candidates"]:
        print(f"  candidate  {c['a']}-{c['b']}: {c['inferred']:+.2f}  ({c['status']})")
    print(f"  {len(composition['conflicts'])} inferences contradict governed cells, e.g.:")
    for c in composition["conflicts"][:2]:
        print(f"  conflict   {c['a']}-{c['b']}: inferred {c['inferred']:+.2f}, governed {c['governed']:+.1f}")
    print("Cheap maths proposes; governance decides. Inference never becomes knowledge on its own.")

    _title(5, "validate a learned relation against the governed one")
    validation = stage_validate_learned(governed, learned)
    print(f"Learned from {len(fixture['toy_corpus']['sentences'])} sentences by co-occurrence "
          f"(a stand-in for trained weights, not an LLM). Range {validation['learned_range']}.")
    for flag in validation["flags"]:
        mark = "ok " if flag["verdict"] == "SIGN_AGREES" else "!! "
        print(f"  {mark}{flag['a']}-{flag['b']}: governed {flag['governed']:+.1f}, learned {flag['learned']:+.3f}")
    print(f"Sign agrees on {validation['sign_agreements']}/{validation['checked_pairs']} governed pairs; "
          f"alike-vs-opposite AUC {validation['alike_vs_opposite_auc']:.2f} (0.5 = chance).")
    print("Predators and prey share sentences, so co-occurrence makes them look alike.")

    _title(6, "evaluate: does the scale change the measures?")
    ev = stage_evaluation(governed, learned)
    for name, key in (("degree >= 0.5", "degree_threshold_half"), ("signed <= 0  ", "signed_threshold_zero")):
        r = ev[key]
        print(f"  {name}: sensitivity {r.sensitivity:.2f}, specificity {r.specificity:.2f}, "
              f"precision {r.precision:.2f}")
    print(f"  AUC degree {ev['auc_degree']:.3f} | AUC signed {ev['auc_signed']:.3f}")
    print("Same numbers: a linear rescaling with a matching threshold changes nothing.")
    states = ev["three_states"]
    print(f"Three-state task: accuracy {states.accuracy:.2f} but macro-F1 {states.macro_f1:.2f}. "
          f"The learned scores are uncalibrated: {ev['learned_cells_in_neutral_band']}/{loss['pairs']} "
          "fall in the neutral band, so 'everything is neutral' scores well on accuracy alone.")
    print("What the signed scale changes is the task: a neutral state you can measure, and miss.")

    _title(7, "cell types define the space")
    print(f"  {'type':<22}{'scale':<8}{'levels':>22}{'neutral exact':>15}{'resolution@0':>14}"
          f"{'states kept':>13}{'learned AUC':>13}")
    rows = stage_cell_types(governed, learned)
    pairs = loss["pairs"]
    for row in rows:
        resolution = "n/a" if np.isnan(row["resolution_at_neutral"]) else f"{row['resolution_at_neutral']:.1e}"
        print(f"  {row['type']:<22}{row['scale']:<8}{row['levels']:>22,}{str(row['neutral_exact']):>15}"
              f"{resolution:>14}{row['governed_states_kept']:>9}/{pairs}{row['learned_auc']:>13.3f}")
    uint8 = next(row for row in rows if row["type"].startswith("uint8"))
    flattened = [row["type"] for row in rows if row["learned_distinct_values"] == 1]
    print(f"uint8 on [0, 1] cannot hold 0.5 or the 0.25/0.75 band edges exactly: "
          f"{pairs - uint8['governed_states_kept']} governed pairs change state just by being stored.")
    print(f"{' and '.join(flattened)} flatten the learned scores to one value: AUC 0.5, no information left.")
    print("Floats are densest near 0, so a signed scale with neutral at 0 resolves near-neutral far better.")


if __name__ == "__main__":
    main()
