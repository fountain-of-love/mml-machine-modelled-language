"""Load bounded experiment fixtures from external data."""

import json
from pathlib import Path


DEFAULT_EXPERIMENT = Path(__file__).parent / "data" / "demonstration" / "words_carry_weight.json"


def load_experiment(path=DEFAULT_EXPERIMENT):
    with Path(path).open(encoding="utf-8") as source:
        return json.load(source)
