"""Measure reusable information in governed multi-valued dimensions."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Mapping, Sequence


@dataclass(frozen=True)
class ValueObservation:
    """A governed yes/no observation used to condition a candidate region."""

    dimension: str
    value: str
    present: bool = True


@dataclass(frozen=True)
class BinaryValueInformation:
    """Information carried by asking whether one represented value is present."""

    dimension: str
    value: str
    candidate_count: int
    covered_candidate_count: int
    missing_candidate_count: int
    present_candidate_count: int
    absent_candidate_count: int
    coverage: float
    information_gain_bits: float
    coverage_adjusted_information_gain_bits: float
    normalized_information_gain: float


@dataclass(frozen=True)
class MultiValueDimensionInformation:
    """Contribution review for a multi-valued dimension in one candidate context."""

    dimension: str
    candidate_count: int
    covered_candidate_count: int
    missing_candidate_count: int
    vocabulary_size: int
    exact_signature_entropy_bits: float
    best_value_question: BinaryValueInformation | None
    apparent_entropy_inflation_bits: float
    value_questions: tuple[BinaryValueInformation, ...]


def _entropy_from_counts(counts: Sequence[int]) -> float:
    total = sum(counts)
    nonzero_counts = tuple(count for count in counts if count)
    if total <= 1 or len(nonzero_counts) <= 1:
        return 0.0
    return -sum(
        (count / total) * math.log2(count / total)
        for count in nonzero_counts
    )


def _selected_records(
    records: Mapping[str, Mapping[str, Sequence[str]]],
    candidate_ids: Sequence[str] | None,
) -> tuple[tuple[str, Mapping[str, Sequence[str]]], ...]:
    if candidate_ids is None:
        return tuple(records.items())
    unknown = sorted(set(candidate_ids) - set(records))
    if unknown:
        raise ValueError(f"unknown candidate IDs: {', '.join(unknown)}")
    return tuple((identifier, records[identifier]) for identifier in candidate_ids)


def condition_candidates(
    records: Mapping[str, Mapping[str, Sequence[str]]],
    observations: Sequence[ValueObservation],
    candidate_ids: Sequence[str] | None = None,
) -> tuple[str, ...]:
    """Return candidates satisfying known multi-value observations.

    An empty dimension is unknown, not a negative assertion, so it cannot satisfy
    either a positive or a negative observation.
    """
    selected = _selected_records(records, candidate_ids)
    matches = []
    for identifier, dimensions in selected:
        accepted = True
        for observation in observations:
            values = tuple(dimensions.get(observation.dimension, ()))
            if not values or ((observation.value in values) != observation.present):
                accepted = False
                break
        if accepted:
            matches.append(identifier)
    return tuple(matches)


def analyze_multivalue_dimension(
    records: Mapping[str, Mapping[str, Sequence[str]]],
    dimension: str,
    candidate_ids: Sequence[str] | None = None,
) -> MultiValueDimensionInformation:
    """Measure binary value questions without treating complete value sets as labels."""
    selected = _selected_records(records, candidate_ids)
    observed = [
        (identifier, frozenset(dimensions.get(dimension, ())))
        for identifier, dimensions in selected
        if dimensions.get(dimension)
    ]
    candidate_count = len(selected)
    covered_count = len(observed)
    missing_count = candidate_count - covered_count
    vocabulary = sorted({value for _, values in observed for value in values})
    signature_counts: dict[frozenset[str], int] = {}
    for _, values in observed:
        signature_counts[values] = signature_counts.get(values, 0) + 1
    signature_entropy = _entropy_from_counts(tuple(signature_counts.values()))
    coverage = covered_count / candidate_count if candidate_count else 0.0
    prior_identity_entropy = math.log2(covered_count) if covered_count > 1 else 0.0

    questions = []
    for value in vocabulary:
        present_count = sum(value in values for _, values in observed)
        absent_count = covered_count - present_count
        information_gain = _entropy_from_counts((present_count, absent_count))
        questions.append(BinaryValueInformation(
            dimension=dimension,
            value=value,
            candidate_count=candidate_count,
            covered_candidate_count=covered_count,
            missing_candidate_count=missing_count,
            present_candidate_count=present_count,
            absent_candidate_count=absent_count,
            coverage=coverage,
            information_gain_bits=information_gain,
            coverage_adjusted_information_gain_bits=information_gain * coverage,
            normalized_information_gain=(
                information_gain / prior_identity_entropy
                if prior_identity_entropy else 0.0
            ),
        ))
    best = max(
        questions,
        key=lambda item: item.coverage_adjusted_information_gain_bits,
        default=None,
    )
    reusable_gain = (
        best.coverage_adjusted_information_gain_bits if best is not None else 0.0
    )
    return MultiValueDimensionInformation(
        dimension=dimension,
        candidate_count=candidate_count,
        covered_candidate_count=covered_count,
        missing_candidate_count=missing_count,
        vocabulary_size=len(vocabulary),
        exact_signature_entropy_bits=signature_entropy,
        best_value_question=best,
        apparent_entropy_inflation_bits=max(0.0, signature_entropy - reusable_gain),
        value_questions=tuple(questions),
    )
