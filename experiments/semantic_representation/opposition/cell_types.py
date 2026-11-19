"""How the cell value type defines the space a relation can occupy.

Each storage type is applied on its natural scale (signed [-1, 1] or degree
[0, 1]) and read back on the signed scale, so the effect of the type alone is
visible: how many levels exist, whether neutral survives exactly, and how
finely the type can distinguish values just next to neutral.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import ROUND_HALF_EVEN, Decimal
from typing import Callable

import numpy as np

from src.semantic_representation.relation_encoding import to_three_states


# Non-negative IEEE values in [0, 1] are the bit patterns 0 .. bits(1.0).
_FLOAT16_UNIT_LEVELS = 0x3C00 + 1
_FLOAT32_UNIT_LEVELS = 0x3F800000 + 1
_FLOAT64_UNIT_LEVELS = 0x3FF0000000000000 + 1


def _decimal_places(places: int) -> Callable[[np.ndarray], np.ndarray]:
    quantum = Decimal(1).scaleb(-places)

    def store(values: np.ndarray) -> np.ndarray:
        rounded = [
            float(Decimal(repr(float(v))).quantize(quantum, rounding=ROUND_HALF_EVEN))
            for v in values.ravel()
        ]
        return np.array(rounded).reshape(values.shape)

    return store


def _as_float(dtype) -> Callable[[np.ndarray], np.ndarray]:
    return lambda values: np.asarray(values).astype(dtype).astype(float)


@dataclass(frozen=True)
class StorageType:
    """One cell representation. ``resolution_at_neutral`` is in signed units."""

    name: str
    scale: str  # "signed" [-1, 1] or "degree" [0, 1]
    store: Callable[[np.ndarray], np.ndarray]
    levels: int
    resolution_at_neutral: float


STORAGE_TYPES = (
    StorageType("bool: opposite or not", "signed",
                lambda s: np.where(s <= -0.5, -1.0, 0.0), 2, float("nan")),
    StorageType("int8: three states", "signed",
                lambda s: to_three_states(s).astype(float), 3, 1.0),
    StorageType("int8: x127", "signed", lambda s: np.round(s * 127) / 127, 255, 1 / 127),
    StorageType("uint8: x255", "degree", lambda d: np.round(d * 255) / 255, 256, 2 / 255),
    StorageType("decimal: 1 place", "degree", _decimal_places(1), 11, 0.2),
    StorageType("float16", "degree", _as_float(np.float16), _FLOAT16_UNIT_LEVELS,
                2 * float(np.spacing(np.float16(0.5)))),
    StorageType("float16", "signed", _as_float(np.float16), 2 * _FLOAT16_UNIT_LEVELS - 1,
                float(np.spacing(np.float16(0)))),
    StorageType("float32", "signed", _as_float(np.float32), 2 * _FLOAT32_UNIT_LEVELS - 1,
                float(np.spacing(np.float32(0)))),
    StorageType("float64", "signed", _as_float(np.float64), 2 * _FLOAT64_UNIT_LEVELS - 1,
                float(np.spacing(np.float64(0)))),
)


def stored_as_signed(storage: StorageType, signed: np.ndarray) -> np.ndarray:
    """Store signed values with ``storage`` on its own scale; read back as signed."""
    signed = np.asarray(signed, dtype=float)
    if storage.scale == "signed":
        return storage.store(signed)
    return 1.0 - 2.0 * storage.store((1.0 - signed) / 2.0)


def neutral_is_exact(storage: StorageType) -> bool:
    """Whether a neutral cell survives storage exactly as neutral."""
    if storage.levels == 2:
        return False  # neutral and alike collapse into the same 0
    return float(stored_as_signed(storage, np.array([0.0]))[0]) == 0.0
