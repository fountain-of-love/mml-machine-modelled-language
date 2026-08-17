"""Analyze reusable and conditional information in the Canidae development seed."""

from __future__ import annotations

import statistics
from pathlib import Path

from src.helpers.json_io import read_json
from src.semantic_navigation.multivalue_information import (
    ValueObservation,
    analyze_multivalue_dimension,
    condition_candidates,
)


ROOT = Path(__file__).resolve().parents[2]
SEED_PATH = (
    ROOT
    / "data"
    / "development"
    / "species_ecology_behavior_seed_canidae_v0_1.json"
)


def _records(seed: dict) -> dict[str, dict[str, tuple[str, ...]]]:
    records = {}
    for record in seed["records"]:
        identifier = record.get("species_id", record.get("id"))
        if not identifier:
            raise ValueError("seed record requires species_id or id")
        records[identifier] = {
            dimension: tuple(claim["value"] for claim in claims)
            for dimension, claims in record["dimensions"].items()
        }
    return records


def _root_summary(information) -> dict:
    best = information.best_value_question
    return {
        "candidate_count": information.candidate_count,
        "covered_candidate_count": information.covered_candidate_count,
        "missing_candidate_count": information.missing_candidate_count,
        "vocabulary_size": information.vocabulary_size,
        "exact_signature_entropy_bits": information.exact_signature_entropy_bits,
        "best_binary_value": None if best is None else best.value,
        "best_binary_information_gain_bits": (
            0.0 if best is None else best.information_gain_bits
        ),
        "best_coverage_adjusted_information_gain_bits": (
            0.0 if best is None else best.coverage_adjusted_information_gain_bits
        ),
        "apparent_entropy_inflation_bits": information.apparent_entropy_inflation_bits,
    }


def _conditional_contexts(
    records: dict[str, dict[str, tuple[str, ...]]],
    dimensions: tuple[str, ...],
    target_dimension: str,
) -> list[dict]:
    contexts = []
    for condition_dimension in dimensions:
        if condition_dimension == target_dimension:
            continue
        values = sorted({
            value
            for record in records.values()
            for value in record[condition_dimension]
        })
        for value in values:
            candidates = condition_candidates(
                records,
                (ValueObservation(condition_dimension, value),),
            )
            if len(candidates) < 2 or len(candidates) == len(records):
                continue
            information = analyze_multivalue_dimension(
                records,
                target_dimension,
                candidates,
            )
            best = information.best_value_question
            gain = (
                0.0
                if best is None
                else best.coverage_adjusted_information_gain_bits
            )
            contexts.append({
                "condition_dimension": condition_dimension,
                "condition_value": value,
                "candidate_count": len(candidates),
                "covered_candidate_count": information.covered_candidate_count,
                "best_target_value": None if best is None else best.value,
                "coverage_adjusted_information_gain_bits": gain,
            })
    return contexts


def analyze_seed(seed: dict | None = None) -> dict:
    """Return a compact contribution review over root and one-value contexts."""
    seed = read_json(SEED_PATH) if seed is None else seed
    records = _records(seed)
    dimensions = tuple(seed["dimensions"])
    reviews = {}
    for dimension in dimensions:
        root = analyze_multivalue_dimension(records, dimension)
        contexts = _conditional_contexts(records, dimensions, dimension)
        gains = [item["coverage_adjusted_information_gain_bits"] for item in contexts]
        positive = [gain for gain in gains if gain > 0.0]
        best_context = max(
            contexts,
            key=lambda item: item["coverage_adjusted_information_gain_bits"],
            default=None,
        )
        reviews[dimension] = {
            "root": _root_summary(root),
            "conditional": {
                "eligible_context_count": len(contexts),
                "positive_gain_context_count": len(positive),
                "positive_gain_rate": len(positive) / len(contexts) if contexts else 0.0,
                "mean_coverage_adjusted_information_gain_bits": (
                    statistics.fmean(gains) if gains else 0.0
                ),
                "maximum_coverage_adjusted_information_gain_bits": (
                    max(gains, default=0.0)
                ),
                "best_context": best_context,
            },
        }
    return {
        "analysis_id": "canidae_ecology_behavior_dimension_contribution_v0_1",
        "seed_state_id": seed["state_id"],
        "candidate_count": len(records),
        "question_model": {
            "multi_value_question": "binary value presence",
            "missing_value_treatment": "excluded from semantic partition and applied as coverage penalty",
            "conditional_context": "one positive value observation from another dimension",
            "exact_signature_entropy": "diagnostic only",
        },
        "dimensions": reviews,
    }


if __name__ == "__main__":
    import json

    print(json.dumps(analyze_seed(), indent=2))
