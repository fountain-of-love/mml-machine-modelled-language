"""Shared provenance facts; callers decide which facts form their evidence contract."""

from __future__ import annotations

import platform
from datetime import datetime, timezone
from pathlib import Path
from typing import Mapping

from .hashing import sha256_file


def utc_now_iso() -> str:
    """Return a timezone-aware UTC instant in ISO-8601 form."""
    return datetime.now(timezone.utc).isoformat()


def runtime_identity(
    package_versions: Mapping[str, str] | None = None,
    *,
    include_host: bool = False,
) -> dict[str, str]:
    """Return replay-relevant runtime facts without claiming host equivalence."""
    identity = {"python": platform.python_version()}
    if package_versions:
        identity.update(package_versions)
    if include_host:
        identity.update({
            "python_implementation": platform.python_implementation(),
            "operating_system": platform.system(),
            "operating_system_release": platform.release(),
            "architecture": platform.machine(),
        })
    return identity


def hash_named_artifacts(
    paths: Mapping[str, str | Path], *, prefixed: bool = True
) -> dict[str, str]:
    """Bind intention-revealing artifact names to exact file identities."""
    return {
        name: sha256_file(path, prefixed=prefixed)
        for name, path in paths.items()
    }

