"""Deterministic SHA-256 primitives."""

from __future__ import annotations

import hashlib
from pathlib import Path


def sha256_bytes(value: bytes, *, prefixed: bool = True) -> str:
    """Return the SHA-256 identity of ``value``."""
    digest = hashlib.sha256(value).hexdigest()
    return f"sha256:{digest}" if prefixed else digest


def sha256_file(path: str | Path, *, prefixed: bool = True) -> str:
    """Return the SHA-256 identity of a file's exact bytes."""
    return sha256_bytes(Path(path).read_bytes(), prefixed=prefixed)
