"""Policy-neutral publication and comparison of evidence artifacts."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from .json_io import read_json, write_json
from .text_io import write_text


@dataclass(frozen=True)
class ArtifactComparison:
    missing_paths: tuple[Path, ...] = ()
    json_matches: bool = False
    text_matches: bool = False

    @property
    def matches(self) -> bool:
        return not self.missing_paths and self.json_matches and self.text_matches


def missing_paths(paths: Iterable[str | Path]) -> tuple[Path, ...]:
    """Return every absent path without imposing CLI or exception policy."""
    return tuple(path for item in paths if not (path := Path(item)).exists())


def without_fields(record: dict, fields: Iterable[str] = ("generated_at",)) -> dict:
    """Return a detached record without explicitly volatile top-level fields."""
    stable = deepcopy(record)
    for field in fields:
        stable.pop(field, None)
    return stable


def write_artifact_pair(
    machine_path: str | Path,
    machine_value: Any,
    human_path: str | Path,
    human_text: str,
) -> None:
    """Publish the machine-readable and human-readable forms together."""
    write_json(machine_path, machine_value)
    write_text(human_path, human_text)


def compare_artifact_pair(
    actual_json: dict,
    actual_text: str,
    reference_json_path: str | Path,
    reference_text_path: str | Path,
    *,
    volatile_fields: Iterable[str] = ("generated_at",),
) -> ArtifactComparison:
    """Compare an artifact pair while ignoring declared volatile JSON fields."""
    json_path = Path(reference_json_path)
    text_path = Path(reference_text_path)
    missing = missing_paths((json_path, text_path))
    if missing:
        return ArtifactComparison(missing_paths=missing)

    reference_json = read_json(json_path)
    return ArtifactComparison(
        json_matches=without_fields(reference_json, volatile_fields)
        == without_fields(actual_json, volatile_fields),
        text_matches=text_path.read_text(encoding="utf-8") == actual_text,
    )
