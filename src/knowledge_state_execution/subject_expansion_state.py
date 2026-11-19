"""Compile governed subject indexing over a concept hierarchy into reusable state.

State the known. Execute the consequence.

Declared rule (the only one this module executes)::

    works_about(Q) = { w | w is-about c  and  c narrower-than* Q }

Identities are absolute IRIs, so public identifiers such as
``http://eurovoc.europa.eu/5181`` stay the primary identity instead of being
replaced by local names. Every edge carries the ``assertion_id`` of the governed
assertion that admitted it, so each answer can be traced back to its sources.

The compiled state stores, per concept, the closure of narrower concepts
together with the assertion chain that reaches each of them. A query is then a
lookup plus a posting scan: no source is reread and no hierarchy is rebuilt.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from types import MappingProxyType
from typing import Iterable, Mapping

from src.helpers.hashing import sha256_bytes
from src.helpers.json_io import canonical_json_bytes


ALGORITHM_VERSION = "subject-expansion-state-v1"
NARROWER_THAN = "narrower-than"
IS_ABOUT = "is-about"
RELATIONS = frozenset({NARROWER_THAN, IS_ABOUT})
RESOLVED = "RESOLVED"
NO_DECLARED_CONSEQUENCE = "NO_DECLARED_CONSEQUENCE"
OUT_OF_SCOPE = "OUT_OF_SCOPE"
_IRI = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:[^\s<>\"]+$")


@dataclass(frozen=True, order=True)
class GovernedAssertion:
    """One accepted, typed, IRI-identified statement with a stable identity."""

    assertion_id: str
    subject: str
    relation: str
    object: str


@dataclass(frozen=True)
class SubjectExpansionMetrics:
    """Deterministic one-time compilation work; not CPU instructions."""

    assertions_read: int
    hierarchy_edges: int
    aboutness_edges: int
    concepts: int
    closure_entries: int
    posting_entries: int


@dataclass(frozen=True)
class SubjectMatch:
    """One work reached through one concept, with its complete assertion chain.

    ``evidence`` starts with the ``is-about`` assertion and continues with the
    ``narrower-than`` assertions from ``via_concept`` up to the query concept.
    """

    work: str
    via_concept: str
    evidence: tuple[str, ...]


@dataclass(frozen=True)
class SubjectQueryOutcome:
    """Typed result: resolved matches or an explicit refusal reason."""

    query: str
    status: str
    reason: str | None
    matches: tuple[SubjectMatch, ...]
    concepts_expanded: int
    postings_read: int

    @property
    def works(self) -> tuple[str, ...]:
        return tuple(sorted({match.work for match in self.matches}))


@dataclass(frozen=True)
class SubjectExpansionState:
    """Immutable closure and postings compiled from governed assertions."""

    assertions: tuple[GovernedAssertion, ...]
    closure: Mapping[str, tuple[tuple[str, tuple[str, ...]], ...]]
    postings: Mapping[str, tuple[tuple[str, str], ...]]
    snapshot_id: str
    compilation: SubjectExpansionMetrics

    @property
    def concepts(self) -> frozenset[str]:
        return frozenset(self.closure)


def _validate(assertions: tuple[GovernedAssertion, ...]) -> None:
    if not assertions:
        raise ValueError("at least one governed assertion is required")
    seen_ids: set[str] = set()
    seen_statements: set[tuple[str, str, str]] = set()
    for assertion in assertions:
        if not isinstance(assertion, GovernedAssertion):
            raise TypeError("assertions must be GovernedAssertion instances")
        if assertion.relation not in RELATIONS:
            raise ValueError(f"unsupported relation: {assertion.relation}")
        if not (_IRI.fullmatch(assertion.subject) and _IRI.fullmatch(assertion.object)):
            raise ValueError(f"assertion {assertion.assertion_id} endpoints must be absolute IRIs")
        if assertion.assertion_id in seen_ids:
            raise ValueError(f"duplicate assertion id: {assertion.assertion_id}")
        statement = (assertion.subject, assertion.relation, assertion.object)
        if statement in seen_statements:
            raise ValueError(f"duplicate governed statement: {statement}")
        seen_ids.add(assertion.assertion_id)
        seen_statements.add(statement)


def _narrower_index(hierarchy: list[GovernedAssertion]) -> dict[str, list[tuple[str, str]]]:
    narrower: dict[str, list[tuple[str, str]]] = {}
    for assertion in hierarchy:
        narrower.setdefault(assertion.object, []).append((assertion.subject, assertion.assertion_id))
    return {concept: sorted(children) for concept, children in narrower.items()}


def _closure_from(
    root: str, narrower: Mapping[str, list[tuple[str, str]]]
) -> tuple[tuple[str, tuple[str, ...]], ...]:
    """Breadth-first closure with the shortest, lexicographically first chain."""
    chains: dict[str, tuple[str, ...]] = {root: ()}
    frontier = [root]
    while frontier:
        next_frontier = []
        for concept in frontier:
            for child, assertion_id in narrower.get(concept, ()):
                if child not in chains:
                    chains[child] = (assertion_id,) + chains[concept]
                    next_frontier.append(child)
        frontier = sorted(next_frontier)
    return tuple(sorted(chains.items()))


def _reject_cycles(narrower: Mapping[str, list[tuple[str, str]]]) -> None:
    state: dict[str, int] = {}

    def visit(concept: str) -> None:
        state[concept] = 1
        for child, _ in narrower.get(concept, ()):
            if state.get(child) == 1:
                raise ValueError(f"cycle in narrower-than hierarchy at {child}")
            if child not in state:
                visit(child)
        state[concept] = 2

    for concept in sorted(narrower):
        if concept not in state:
            visit(concept)


def compile_subject_expansion_state(
    assertions: Iterable[GovernedAssertion],
) -> SubjectExpansionState:
    """Validate governed assertions once and compile closure plus postings."""
    ordered = tuple(sorted(assertions))
    _validate(ordered)
    hierarchy = [a for a in ordered if a.relation == NARROWER_THAN]
    aboutness = [a for a in ordered if a.relation == IS_ABOUT]
    narrower = _narrower_index(hierarchy)
    _reject_cycles(narrower)

    concepts = sorted(
        {a.subject for a in hierarchy} | {a.object for a in hierarchy} | {a.object for a in aboutness}
    )
    closure = {concept: _closure_from(concept, narrower) for concept in concepts}
    posting_lists: dict[str, list[tuple[str, str]]] = {concept: [] for concept in concepts}
    for assertion in aboutness:
        posting_lists[assertion.object].append((assertion.subject, assertion.assertion_id))
    postings = {concept: tuple(sorted(items)) for concept, items in posting_lists.items()}

    snapshot_id = sha256_bytes(canonical_json_bytes({
        "algorithm": ALGORITHM_VERSION,
        "assertions": [a.__dict__ for a in ordered],
    }))
    metrics = SubjectExpansionMetrics(
        assertions_read=len(ordered),
        hierarchy_edges=len(hierarchy),
        aboutness_edges=len(aboutness),
        concepts=len(concepts),
        closure_entries=sum(len(entries) for entries in closure.values()),
        posting_entries=sum(len(items) for items in postings.values()),
    )
    return SubjectExpansionState(
        assertions=ordered,
        closure=MappingProxyType(closure),
        postings=MappingProxyType(postings),
        snapshot_id=snapshot_id,
        compilation=metrics,
    )


def execute_subject_query(state: SubjectExpansionState, concept: str) -> SubjectQueryOutcome:
    """Return every work about ``concept`` or a narrower concept, with evidence."""
    if not _IRI.fullmatch(concept):
        raise ValueError("query concept must be an absolute IRI")
    closure = state.closure.get(concept)
    if closure is None:
        return SubjectQueryOutcome(concept, NO_DECLARED_CONSEQUENCE, OUT_OF_SCOPE, (), 0, 0)
    matches = []
    postings_read = 0
    for via_concept, chain in closure:
        for work, assertion_id in state.postings[via_concept]:
            postings_read += 1
            matches.append(SubjectMatch(work, via_concept, (assertion_id,) + chain))
    return SubjectQueryOutcome(
        concept, RESOLVED, None, tuple(sorted(matches, key=lambda m: (m.work, m.via_concept))),
        concepts_expanded=len(closure), postings_read=postings_read,
    )
