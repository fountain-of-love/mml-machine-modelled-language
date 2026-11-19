"""Governed mapping from a frozen public RDF snapshot to MML assertions.

The adapter owns everything source-specific: reading the snapshot, applying
the declared mapping policy and corrections, deriving assertion identities
from the exact source triple, and the reconstruction-at-use treatment. The
runtime in ``src.knowledge_state_execution.subject_expansion_state`` stays
source-agnostic.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Mapping

from experiments.knowledge_state_execution.ntriples import Triple, parse_line, parse_ntriples, serialize_triple
from src.helpers.hashing import sha256_bytes
from src.helpers.json_io import read_json
from src.knowledge_state_execution.subject_expansion_state import (
    IS_ABOUT,
    NARROWER_THAN,
    NO_DECLARED_CONSEQUENCE,
    OUT_OF_SCOPE,
    RESOLVED,
    GovernedAssertion,
)


ROOT = Path(__file__).resolve().parents[2]
SNAPSHOT_DIR = ROOT / "data" / "public" / "eurovoc-information-policy-v1"
SKOS_PREF_LABEL = "http://www.w3.org/2004/02/skos/core#prefLabel"
CDM_CELEX = "http://publications.europa.eu/ontology/cdm#resource_legal_id_celex"


@dataclass(frozen=True)
class MappingPolicy:
    """Source predicate -> MML relation decisions, loaded from governed JSON."""

    policy_id: str
    relation_by_predicate: Mapping[str, str]
    decision_by_predicate: Mapping[str, str]

    @classmethod
    def load(cls, path: Path = SNAPSHOT_DIR / "mapping_policy_v1.json") -> "MappingPolicy":
        record = read_json(path)
        decisions = record["decisions"]
        return cls(
            policy_id=record["policy_id"],
            relation_by_predicate={d["source_predicate"]: d["mml_relation"] for d in decisions},
            decision_by_predicate={d["source_predicate"]: d["decision_id"] for d in decisions},
        )


@dataclass(frozen=True)
class GovernedMapping:
    """Admitted assertions plus the provenance needed to trace each one."""

    assertions: tuple[GovernedAssertion, ...]
    provenance: Mapping[str, dict]
    excluded: tuple[str, ...]


@dataclass
class WorkCounters:
    """Deterministic, high-level work counts; not CPU instructions."""

    bytes_read: int = 0
    triples_parsed: int = 0
    assertions_mapped: int = 0
    index_entries_built: int = 0
    concepts_expanded: int = 0
    postings_read: int = 0

    def structural_operations(self) -> int:
        return (
            self.triples_parsed + self.assertions_mapped + self.index_entries_built
            + self.concepts_expanded + self.postings_read
        )

    def as_dict(self) -> dict:
        values = dict(self.__dict__)
        values["structural_operations"] = self.structural_operations()
        return values


@dataclass(frozen=True)
class ReconstructedAnswer:
    status: str
    reason: str | None
    works: tuple[str, ...]
    counters: WorkCounters = field(compare=False)


def assertion_id_for(triple: Triple) -> str:
    """Derive a stable assertion identity from the exact source statement."""
    return "src:" + sha256_bytes(serialize_triple(triple).encode("utf-8"), prefixed=False)[:16]


def read_snapshot(path: Path = SNAPSHOT_DIR / "snapshot.nt") -> tuple[tuple[Triple, ...], int]:
    raw = path.read_bytes()
    return tuple(parse_ntriples(raw.decode("utf-8"))), len(raw)


def load_correction(path: Path = SNAPSHOT_DIR / "correction_v1.json") -> dict:
    correction = read_json(path)
    correction["source_triple_parsed"] = parse_line(correction["source_triple"])
    return correction


def map_assertions(
    triples: Iterable[Triple],
    policy: MappingPolicy,
    excluded_triples: frozenset[Triple] = frozenset(),
) -> GovernedMapping:
    """Admit mapped source triples; keep exclusions visible rather than silent."""
    assertions, provenance, excluded = [], {}, []
    for triple in triples:
        relation = policy.relation_by_predicate.get(triple.predicate)
        if relation is None:
            continue
        assertion_id = assertion_id_for(triple)
        if triple in excluded_triples:
            excluded.append(assertion_id)
            continue
        assertions.append(GovernedAssertion(assertion_id, triple.subject, relation, triple.object))
        provenance[assertion_id] = {
            "source_triple": serialize_triple(triple),
            "source_predicate": triple.predicate,
            "mapping_decision": policy.decision_by_predicate[triple.predicate],
            "policy_id": policy.policy_id,
        }
    return GovernedMapping(tuple(assertions), provenance, tuple(sorted(excluded)))


def labels_by_concept(triples: Iterable[Triple]) -> dict[str, dict[str, str]]:
    labels: dict[str, dict[str, str]] = {}
    for triple in triples:
        if triple.predicate == SKOS_PREF_LABEL and triple.language:
            labels.setdefault(triple.subject, {})[triple.language] = triple.object
    return labels


def celex_by_work(triples: Iterable[Triple]) -> dict[str, str]:
    return {t.subject: t.object for t in triples if t.predicate == CDM_CELEX}


@dataclass(frozen=True)
class WalkIndex:
    """Uncompiled adjacency and postings: what a per-query walk needs."""

    narrower: Mapping[str, tuple[str, ...]]
    postings: Mapping[str, tuple[str, ...]]
    concepts: frozenset[str]


def build_walk_index(
    snapshot_path: Path,
    policy: MappingPolicy,
    counters: WorkCounters,
    excluded_triples: frozenset[Triple] = frozenset(),
) -> WalkIndex:
    """Read, parse, and map the snapshot into adjacency and postings only."""
    raw = snapshot_path.read_bytes()
    counters.bytes_read += len(raw)
    narrower: dict[str, list[str]] = {}
    postings: dict[str, list[str]] = {}
    for line in raw.decode("utf-8").splitlines():
        if not line.strip():
            continue
        triple = parse_line(line)
        counters.triples_parsed += 1
        relation = policy.relation_by_predicate.get(triple.predicate)
        if relation is None or triple in excluded_triples:
            continue
        counters.assertions_mapped += 1
        if relation not in (NARROWER_THAN, IS_ABOUT):
            raise ValueError(f"walk index cannot execute relation: {relation}")
        target = narrower if relation == NARROWER_THAN else postings
        target.setdefault(triple.object, []).append(triple.subject)
        counters.index_entries_built += 1
    concepts = set(narrower) | set(postings)
    concepts.update(child for children in narrower.values() for child in children)
    return WalkIndex(
        {k: tuple(v) for k, v in narrower.items()},
        {k: tuple(v) for k, v in postings.items()},
        frozenset(concepts),
    )


def walk_answer(index: WalkIndex, query: str, counters: WorkCounters) -> ReconstructedAnswer:
    """Breadth-first walk from ``query`` over narrower links, collecting works."""
    if query not in index.concepts:
        return ReconstructedAnswer(NO_DECLARED_CONSEQUENCE, OUT_OF_SCOPE, (), counters)
    works: set[str] = set()
    seen, queue = {query}, deque([query])
    while queue:
        concept = queue.popleft()
        counters.concepts_expanded += 1
        for work in index.postings.get(concept, ()):
            counters.postings_read += 1
            works.add(work)
        for child in index.narrower.get(concept, ()):
            if child not in seen:
                seen.add(child)
                queue.append(child)
    return ReconstructedAnswer(RESOLVED, None, tuple(sorted(works)), counters)


def reconstruct_and_answer(
    snapshot_path: Path,
    policy: MappingPolicy,
    query: str,
    excluded_triples: frozenset[Triple] = frozenset(),
) -> ReconstructedAnswer:
    """Reconstruction at use: reread, reparse, remap, and walk for every query.

    It builds only what one query needs (adjacency, postings, one walk), so it
    is not a strawman that recompiles every closure. It is also an independent
    implementation of the declared rule and serves as a second agreement check.
    """
    counters = WorkCounters()
    index = build_walk_index(snapshot_path, policy, counters, excluded_triples)
    return walk_answer(index, query, counters)
