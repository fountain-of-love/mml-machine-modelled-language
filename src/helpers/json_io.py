"""Consistent UTF-8 JSON persistence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def read_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: str | Path, value: Any) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def canonical_json_bytes(value: Any, *, default=None) -> bytes:
    """Serialize a value for deterministic content identity."""
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), default=default
    ).encode()
