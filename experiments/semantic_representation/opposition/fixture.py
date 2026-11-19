"""Load the governed animal-opposition fixture."""

from __future__ import annotations

from pathlib import Path

from src.helpers.json_io import read_json
from src.semantic_representation.relation_encoding import SignedRelationMatrix, build_signed_matrix


ROOT = Path(__file__).resolve().parents[3]
FIXTURE_PATH = ROOT / "data" / "demonstration" / "animal_opposition_v1.json"


def load_fixture(path: Path = FIXTURE_PATH) -> dict:
    return read_json(path)


def governed_matrix(fixture: dict) -> SignedRelationMatrix:
    return build_signed_matrix(
        fixture["animals"], fixture["relations"], default=fixture["unlisted_pairs"]["value"]
    )
