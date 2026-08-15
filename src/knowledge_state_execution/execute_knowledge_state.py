"""Compile governed semantic facts into deterministic executable state.

State the known. Execute the consequence.

This module is the technical expression of "knowledge is state": established
facts are represented once as typed structure, and declared semantic
consequences are obtained by ordinary deterministic traversal.
"""

import re
from dataclasses import dataclass
from types import MappingProxyType

from src.helpers.hashing import sha256_bytes
from src.helpers.json_io import canonical_json_bytes


IDENTITY = re.compile(r"^[a-z][a-z0-9_-]*$")
RELATIONS = frozenset({"is-a", "belongs-to"})
ALGORITHM_VERSION = "knowledge-state-execution-v1"


@dataclass(frozen=True, order=True)
class KnowledgeFact:
    """One governed directed semantic relation."""

    subject: str
    relation: str
    object: str


@dataclass(frozen=True)
class KnowledgeState:
    """Immutable facts and their compiled subject index."""

    facts: tuple
    outgoing: object
    snapshot_id: str


@dataclass(frozen=True)
class KnowledgeExecution:
    """Exact answer and inspectable route through compiled state."""

    query: str
    answer: str
    path: tuple
    relations: tuple
    nodes_visited: int
    edges_traversed: int


def _validate_fact(fact):
    if not isinstance(fact, KnowledgeFact):
        raise TypeError("knowledge facts must be KnowledgeFact instances")
    if not IDENTITY.fullmatch(fact.subject) or not IDENTITY.fullmatch(fact.object):
        raise ValueError("fact identities must be normalized governed identities")
    if fact.relation not in RELATIONS:
        raise ValueError(f"unsupported knowledge relation: {fact.relation}")


def _snapshot_id(facts):
    payload = {
        "algorithm": ALGORITHM_VERSION,
        "facts": [fact.__dict__ for fact in sorted(facts)],
    }
    return sha256_bytes(canonical_json_bytes(payload))


def _build_outgoing(facts):
    outgoing = {}
    for fact in facts:
        _validate_fact(fact)
        existing = outgoing.get(fact.subject)
        if existing is not None:
            raise ValueError(
                f"ambiguous outgoing knowledge for '{fact.subject}': "
                f"{existing.relation} and {fact.relation}"
            )
        outgoing[fact.subject] = fact
    return outgoing


def compile_knowledge_state(facts):
    """Compile governed facts once into an immutable executable index."""
    facts = tuple(facts)
    if not facts:
        raise ValueError("at least one governed knowledge fact is required")
    if len(facts) != len(set(facts)):
        raise ValueError("knowledge facts must be unique")
    outgoing = _build_outgoing(facts)
    return KnowledgeState(
        facts=facts,
        outgoing=MappingProxyType(outgoing),
        snapshot_id=_snapshot_id(facts),
    )


def execute(state, query):
    """Execute the declared ``is-a* -> belongs-to`` composition rule."""
    if not IDENTITY.fullmatch(query):
        raise ValueError("query must be a normalized governed identity")

    path = [query]
    relations = []
    visited = {query}
    current = query

    while True:
        fact = state.outgoing.get(current)
        if fact is None:
            raise ValueError(f"no terminal belongs-to fact reachable from '{query}'")
        if fact.object in visited:
            raise ValueError(f"knowledge cycle reached while executing '{query}'")

        relations.append(fact.relation)
        path.append(fact.object)
        visited.add(fact.object)

        if fact.relation == "belongs-to":
            return KnowledgeExecution(
                query=query,
                answer=fact.object,
                path=tuple(path),
                relations=tuple(relations),
                nodes_visited=len(path),
                edges_traversed=len(relations),
            )
        if fact.relation != "is-a":
            raise ValueError(f"unsupported relation composition: {fact.relation}")
        current = fact.object


def replace_fact(state, old_fact, new_fact):
    """Return new executable state after one governed local correction."""
    _validate_fact(old_fact)
    _validate_fact(new_fact)
    if (old_fact.subject, old_fact.relation) != (
        new_fact.subject,
        new_fact.relation,
    ):
        raise ValueError("a local correction must preserve subject and relation")
    if state.outgoing.get(old_fact.subject) != old_fact:
        raise ValueError("the fact being replaced is not present in this state")

    facts = tuple(new_fact if fact == old_fact else fact for fact in state.facts)
    outgoing = dict(state.outgoing)
    outgoing[new_fact.subject] = new_fact
    return KnowledgeState(
        facts=facts,
        outgoing=MappingProxyType(outgoing),
        snapshot_id=_snapshot_id(facts),
    )
