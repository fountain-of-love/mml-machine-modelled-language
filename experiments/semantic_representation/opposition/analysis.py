"""The demonstration's stages as pure functions returning inspectable results."""

from __future__ import annotations

import numpy as np

from experiments.semantic_representation.opposition.cell_types import (
    STORAGE_TYPES,
    neutral_is_exact,
    stored_as_signed,
)
from experiments.semantic_representation.opposition.metrics import (
    auc,
    binary_report,
    entropy_bits,
    pair_values,
    three_state_report,
)
from src.semantic_representation.relation_encoding import (
    ALIKE,
    OPPOSITE,
    SignedRelationMatrix,
    related,
    to_binary,
    to_degree,
    to_three_states,
    two_hop,
)


def stage_lookup(governed: SignedRelationMatrix, animal: str) -> dict:
    """Stages 1-3: the same question asked of three encodings."""
    i = governed.index(animal)
    one_hot = np.zeros(len(governed.labels))
    one_hot[i] = 1.0
    binary_row = one_hot @ to_binary(governed)  # matrix-vector product = lookup
    degree_row = to_degree(governed)[i]
    return {
        "binary_opposites": [a for a, hit in zip(governed.labels, binary_row) if hit],
        "degree_ranking": sorted(
            ((a, float(d)) for a, d in zip(governed.labels, degree_row) if a != animal),
            key=lambda item: (-item[1], item[0]),
        ),
        "signed_opposites": related(governed, animal, OPPOSITE),
        "signed_alike": related(governed, animal, ALIKE),
    }


def stage_encoding_loss(governed: SignedRelationMatrix) -> dict:
    """What each encoding can and cannot distinguish, on the distinct pairs."""
    signed = pair_values(governed.values)
    states = pair_values(to_three_states(governed.values))
    binary = pair_values(to_binary(governed))
    return {
        "pairs": int(len(signed)),
        "binary_ones": int(binary.sum()),
        "binary_zeros_that_are_alike": int(np.sum((binary == 0) & (states == ALIKE))),
        "binary_zeros_that_are_neutral": int(np.sum((binary == 0) & (states == 0))),
        "entropy_bits": {
            "binary": entropy_bits(binary),
            "three_states": entropy_bits(states),
            "graded_values": entropy_bits(np.round(signed, 6)),
        },
    }


def stage_two_hop(governed: SignedRelationMatrix, limit: int = 3) -> dict:
    """Two-step composition: candidates for unstated pairs, conflicts for stated ones."""
    composed = two_hop(governed)
    asserted = governed.is_asserted()
    candidates, conflicts = [], []
    for i, j in zip(*np.triu_indices(len(governed.labels), k=1)):
        score = round(float(composed[i, j]), 6)
        if score == 0:
            continue
        item = {"a": governed.labels[i], "b": governed.labels[j], "inferred": score}
        if not asserted[i, j]:
            candidates.append({**item, "status": "CANDIDATE_NOT_GOVERNED"})
        elif abs(score) >= 0.5 and np.sign(score) != np.sign(governed.values[i, j]):
            conflicts.append({**item, "governed": float(governed.values[i, j]),
                              "status": "INFERENCE_CONTRADICTS_GOVERNANCE"})
    return {
        "candidates": sorted(candidates, key=_strongest_first)[:limit],
        "conflicts": sorted(conflicts, key=_strongest_first),
    }


def _strongest_first(item: dict) -> tuple:
    return (-abs(item["inferred"]), item["a"], item["b"])


MIXED_PATH, TARGET_ON_OTHER_AXIS, SAME_AXIS = "MIXED_PATH", "TARGET_ON_OTHER_AXIS", "SAME_AXIS"


def stage_dimension_mixing(governed: SignedRelationMatrix, relations: list[dict]) -> dict:
    """Exploratory: do two-hop inferences chain different tensions?

    Each authored relation carries a post hoc ``dimension`` tag (interaction or
    likeness). For every two-hop inference, the contributing paths are split
    into single-axis and mixed-axis paths. A conflict is then classified as
    ``MIXED_PATH`` (mixed paths supply most of the inferred magnitude),
    ``TARGET_ON_OTHER_AXIS`` (single-axis paths, but the governed pair lives on
    the other axis), or ``SAME_AXIS`` (the sign algebra itself fails).
    """
    axis = {frozenset((r["a"], r["b"])): r["dimension"] for r in relations}
    labels = governed.labels
    composition = stage_two_hop(governed, limit=len(labels) ** 2)

    def paths(a: str, b: str) -> list[dict]:
        i, j = labels.index(a), labels.index(b)
        found = []
        for k, via in enumerate(labels):
            contribution = round(float(governed.values[i, k] * governed.values[k, j]), 6)
            if k not in (i, j) and contribution:
                axes = (axis[frozenset((a, via))], axis[frozenset((via, b))])
                found.append({"via": via, "contribution": contribution, "axes": list(axes),
                              "mixed": axes[0] != axes[1]})
        return found

    def mixed_share(found: list[dict]) -> float:
        total = sum(abs(p["contribution"]) for p in found)
        return round(sum(abs(p["contribution"]) for p in found if p["mixed"]) / total, 3)

    conflicts = []
    for conflict in composition["conflicts"]:
        found = paths(conflict["a"], conflict["b"])
        share = mixed_share(found)
        single_axes = {p["axes"][0] for p in found if not p["mixed"]}
        target = axis[frozenset((conflict["a"], conflict["b"]))]
        if share > 0.5:
            kind = MIXED_PATH
        elif target not in single_axes:
            kind = TARGET_ON_OTHER_AXIS
        else:
            kind = SAME_AXIS
        conflicts.append({**conflict, "target_axis": target, "paths": found,
                          "mixed_share": share, "classification": kind})
    candidates = [
        {**c, "mixed_share": mixed_share(paths(c["a"], c["b"]))} for c in composition["candidates"]
    ]
    return {
        "status": "EXPLORATORY_POST_HOC",
        "conflicts": conflicts,
        "conflicts_crossing_axes": sum(c["classification"] != SAME_AXIS for c in conflicts),
        "candidates": len(candidates),
        "candidates_mostly_mixed": sum(c["mixed_share"] > 0.5 for c in candidates),
        "single_axis_candidates": [c for c in candidates if c["mixed_share"] == 0.0],
    }


def stage_validate_learned(governed: SignedRelationMatrix, learned: SignedRelationMatrix) -> dict:
    """Check a learned relation against the governed one, cell by cell."""
    g_states = pair_values(to_three_states(governed.values))
    g_values, l_values = pair_values(governed.values), pair_values(learned.values)
    rows, cols = np.triu_indices(len(governed.labels), k=1)
    asserted = g_states != 0
    flags = [
        {
            "a": governed.labels[i], "b": governed.labels[j],
            "governed": float(g), "learned": round(float(l), 3),
            "verdict": "SIGN_AGREES" if np.sign(l) == np.sign(g) else "SIGN_CONTRADICTS",
        }
        for i, j, g, l, keep in zip(rows, cols, g_values, l_values, asserted) if keep
    ]
    polar = g_states != 0
    return {
        "checked_pairs": int(asserted.sum()),
        "sign_agreements": sum(f["verdict"] == "SIGN_AGREES" for f in flags),
        "alike_vs_opposite_auc": auc(l_values[polar], g_states[polar] == ALIKE),
        "learned_range": (round(float(l_values.min()), 3), round(float(l_values.max()), 3)),
        "flags": flags,
    }


def stage_evaluation(governed: SignedRelationMatrix, learned: SignedRelationMatrix) -> dict:
    """IR measures for the learned relation, under the degree and signed scales."""
    truth = pair_values(governed.values) <= -0.5
    signed = pair_values(learned.values)
    degree = pair_values(to_degree(learned))
    at_degree_half = binary_report(truth, degree >= 0.5)
    at_signed_zero = binary_report(truth, signed <= 0.0)
    states = three_state_report(
        pair_values(to_three_states(governed.values)), pair_values(to_three_states(learned.values))
    )
    return {
        "positives": int(truth.sum()),
        "degree_threshold_half": at_degree_half,
        "signed_threshold_zero": at_signed_zero,
        "auc_degree": auc(degree, truth),
        "auc_signed": auc(-signed, truth),
        "three_states": states,
        "learned_cells_in_neutral_band": int(np.sum(np.abs(signed) < 0.5)),
    }


def stage_cell_types(governed: SignedRelationMatrix, learned: SignedRelationMatrix) -> list[dict]:
    """Store the governed and the learned relation in each type; measure the change."""
    g_signed = pair_values(governed.values)
    g_states = to_three_states(g_signed)
    truth = g_signed <= -0.5
    l_signed = pair_values(learned.values)
    names = [f"{governed.labels[i]}–{governed.labels[j]}"
             for i, j in zip(*np.triu_indices(len(governed.labels), k=1))]
    rows = []
    for storage in STORAGE_TYPES:
        g_stored = stored_as_signed(storage, g_signed)
        l_stored = stored_as_signed(storage, l_signed)
        changed = to_three_states(g_stored) != g_states
        rows.append({
            "governed_states_changed": [name for name, flip in zip(names, changed) if flip],
            "type": storage.name,
            "scale": storage.scale,
            "levels": storage.levels,
            "neutral_exact": neutral_is_exact(storage),
            "resolution_at_neutral": storage.resolution_at_neutral,
            "governed_max_error": float(np.max(np.abs(g_stored - g_signed))),
            "governed_states_kept": int(np.sum(to_three_states(g_stored) == g_states)),
            "learned_distinct_values": int(len(np.unique(l_stored))),
            "learned_auc": auc(-l_stored, truth),
        })
    return rows
