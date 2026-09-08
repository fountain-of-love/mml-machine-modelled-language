"""Shared fixture adapters for Semantic Navigation experiments."""

from __future__ import annotations

import json
from pathlib import Path

from src.semantic_representation.governed_coordinates import SemanticEntity


ROOT = Path(__file__).resolve().parents[2]
COMPILED_NAVIGATION_SEED_PATH = (
    ROOT / "data" / "demonstration" / "compiled_encyclopedic_navigation_seed_v1.json"
)


def _entity(item: dict, dimensions: tuple[str, ...]) -> SemanticEntity:
    return SemanticEntity(
        item["id"],
        item["label"],
        {dimension: item.get(dimension) for dimension in dimensions},
    )


def load_compiled_navigation_fixture(
    path: Path = COMPILED_NAVIGATION_SEED_PATH,
) -> tuple[
    dict,
    tuple[str, ...],
    tuple[SemanticEntity, ...],
    tuple[SemanticEntity, ...],
]:
    """Load the frozen scalar fixture used by foundational navigation studies."""
    fixture = json.loads(path.read_text(encoding="utf-8"))
    dimensions = tuple(fixture["dimensions"])
    records = tuple(_entity(item, dimensions) for item in fixture["records"])
    incomplete = tuple(
        _entity(item, dimensions)
        for item in fixture.get("incomplete_records", ())
    )
    return fixture, dimensions, records, incomplete
