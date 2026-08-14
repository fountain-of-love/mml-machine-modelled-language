"""Load the bounded Knowledge Is State demonstration fixture."""

import json
from pathlib import Path

from src.knowledge_state_execution.execute_knowledge_state import KnowledgeFact


DEFAULT_FIXTURE = (
    Path(__file__).resolve().parents[2] / "data" / "demonstration" / "knowledge_is_state.json"
)


def load_knowledge_state_fixture(path=DEFAULT_FIXTURE):
    with Path(path).open(encoding="utf-8") as source:
        fixture = json.load(source)
    fixture["facts"] = tuple(KnowledgeFact(**record) for record in fixture["facts"])
    fixture["questions"] = tuple(fixture["questions"])
    fixture["mutation"] = {
        "old": KnowledgeFact(**fixture["mutation"]["old"]),
        "new": KnowledgeFact(**fixture["mutation"]["new"]),
    }
    return fixture
