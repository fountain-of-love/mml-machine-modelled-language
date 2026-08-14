"""Load bounded experiment fixtures from external data."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_EXPERIMENT = ROOT / "data" / "demonstration" / "words_carry_weight.json"


def load_experiment(path=DEFAULT_EXPERIMENT):
    with Path(path).open(encoding="utf-8") as source:
        return json.load(source)
