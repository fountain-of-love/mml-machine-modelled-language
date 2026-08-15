"""Consistent UTF-8 text persistence."""

from __future__ import annotations

from pathlib import Path


def write_text(path: str | Path, value: str) -> None:
    """Persist rendered text without coupling storage to its source format."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")
