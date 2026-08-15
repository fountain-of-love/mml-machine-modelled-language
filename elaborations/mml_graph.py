"""Deterministic construction and execution of a small weighted semantic graph."""

import hashlib
import json
import math
import re
from collections import Counter, deque
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType

import numpy as np

from src.combinatorial_uniqueness.compose_concepts import ActivatedField, soft_intersection
from src.helpers.hashing import sha256_bytes
from src.helpers.json_io import canonical_json_bytes


ALGORITHM_VERSION = "mml-typed-graph-v1"
RELATION_TYPES = frozenset({"supports", "contradicts", "requires", "qualifies"})
POSITIVE_RELATIONS = frozenset({"supports", "requires", "qualifies"})
RELATION_MULTIPLIERS = MappingProxyType({"supports": 1.0, "requires": 0.8, "qualifies": 0.5})
GOVERNED_ID = re.compile(r"^[a-z0-9][a-z0-9:_-]*$")
SENTENCE_ID = re.compile(r"^sentence:[0-9a-f]{16}$")


def tokenize(text):
    return re.findall(r"[a-z0-9_]+", text.lower())


def stable_sentence_id(text):
    normalized = " ".join(tokenize(text))
    return f"sentence:{hashlib.sha256(normalized.encode()).hexdigest()[:16]}"


def load_relations(path):
    """Load authored relations without exposing JSONL details to graph execution."""
    relations = []
    with Path(path).open(encoding="utf-8") as source:
        for line_number, line in enumerate(source, 1):
            if line.strip():
                try:
                    relations.append(json.loads(line))
                except json.JSONDecodeError as error:
                    raise ValueError(f"invalid relation JSON on line {line_number}") from error
    return relations


def load_aliases(path):
    aliases = []
    with Path(path).open(encoding="utf-8") as source:
        for line_number, line in enumerate(source, 1):
            if line.strip():
                try:
                    aliases.append(json.loads(line))
                except json.JSONDecodeError as error:
                    raise ValueError(f"invalid alias JSON on line {line_number}") from error
    return aliases


def _canonical_alias(record):
    required = {"id", "phrase", "concept", "evidence_ids"}
    missing = required - set(record)
    if missing:
        raise ValueError(f"alias missing fields: {sorted(missing)}")
    raw_phrase = record["phrase"]
    phrase = tuple(tokenize(raw_phrase)) if isinstance(raw_phrase, str) else tuple(raw_phrase)
    concept = str(record["concept"])
    alias_id = str(record["id"])
    if not GOVERNED_ID.fullmatch(alias_id):
        raise ValueError("alias id must be a non-empty stable governed ID")
    if not phrase or tokenize(concept) != [concept]:
        raise ValueError("alias phrase and normalized concept are required")
    evidence_ids = tuple(record["evidence_ids"])
    if not evidence_ids or not all(
        isinstance(item, str) and SENTENCE_ID.fullmatch(item) for item in evidence_ids
    ):
        raise ValueError("alias evidence_ids must be stable construction sentence IDs")
    confidence = float(record.get("confidence", 1.0))
    if not 0 <= confidence <= 1:
        raise ValueError("alias confidence must be in [0, 1]")
    return {
        "id": alias_id, "phrase": phrase, "concept": concept,
        "evidence_ids": evidence_ids,
        "confidence": confidence,
        "review_state": record.get("review_state", "provisional"),
    }


def _canonical_relation(record):
    required = {"id", "source", "relation", "target", "weight", "evidence_ids"}
    missing = required - set(record)
    if missing:
        raise ValueError(f"relation missing fields: {sorted(missing)}")
    relation = record["relation"]
    relation_id = str(record["id"])
    if not GOVERNED_ID.fullmatch(relation_id):
        raise ValueError("relation id must be a non-empty stable governed ID")
    if relation not in RELATION_TYPES:
        raise ValueError(f"unknown relation type: {relation}")
    weight = float(record["weight"])
    if not 0 < weight <= 1:
        raise ValueError("relation weight must be in (0, 1]")
    evidence_ids = tuple(record["evidence_ids"])
    if not evidence_ids or not all(
        isinstance(item, str) and SENTENCE_ID.fullmatch(item) for item in evidence_ids
    ):
        raise ValueError("relation evidence_ids must be stable construction sentence IDs")
    expected_polarity = -1 if relation == "contradicts" else 1
    polarity = int(record.get("polarity", expected_polarity))
    if polarity != expected_polarity:
        raise ValueError(f"{relation} relation requires polarity {expected_polarity}")
    source = str(record["source"])
    target = str(record["target"])
    if tokenize(source) != [source] or tokenize(target) != [target]:
        raise ValueError("relation endpoints must be normalized single tokens")
    confidence = float(record.get("confidence", 1.0))
    if not 0 <= confidence <= 1:
        raise ValueError("relation confidence must be in [0, 1]")
    return {
        "id": relation_id,
        "source": source,
        "relation": relation,
        "target": target,
        "weight": weight,
        "polarity": polarity,
        "evidence_ids": evidence_ids,
        "jurisdiction": record.get("jurisdiction"),
        "confidence": confidence,
        "maturity": record.get("maturity", "authored"),
        "review_state": record.get("review_state", "provisional"),
    }


def graph_snapshot_id(sentences, relations=(), aliases=(), window_size=2, damping=0.65, steps=3):
    """Return a deterministic content identity for sources and execution settings."""
    sentence_records = [
        {"id": stable_sentence_id(text), "text": " ".join(tokenize(text))}
        for text in sentences
    ]
    relation_records = [_canonical_relation(record) for record in relations]
    alias_records = [_canonical_alias(record) for record in aliases]
    payload = {
        "algorithm": ALGORITHM_VERSION,
        "sentences": sorted(sentence_records, key=lambda item: item["id"]),
        "relations": sorted(relation_records, key=lambda item: item["id"]),
        "aliases": sorted(alias_records, key=lambda item: item["id"]),
        "relation_multipliers": dict(RELATION_MULTIPLIERS),
        "configuration": {"window_size": window_size, "damping": damping, "steps": steps},
    }
    return sha256_bytes(canonical_json_bytes(payload, default=list))


def _executable_snapshot_id(source_id, vocab, arrays):
    """Bind the declared sources to the exact numeric state that will execute."""
    digest = hashlib.sha256(source_id.encode())
    digest.update(json.dumps(vocab, separators=(",", ":")).encode())
    for array in arrays:
        digest.update(str(array.dtype).encode())
        digest.update(json.dumps(array.shape).encode())
        digest.update(array.tobytes(order="C"))
    return f"sha256:{digest.hexdigest()}"


def _readonly(array):
    """Detach numeric state into an immutable bytes-backed array."""
    return np.frombuffer(array.tobytes(order="C"), dtype=array.dtype).reshape(array.shape)


@dataclass(frozen=True)
class GraphModel:
    vocab: tuple
    word2idx: dict
    idx2word: dict
    transition: np.ndarray
    token_idf: np.ndarray
    inverse_degree: np.ndarray
    background: np.ndarray
    damping: float = 0.65
    steps: int = 3
    relations: tuple = ()
    aliases: tuple = ()
    sentences: tuple = ()
    sentence_ids: tuple = ()
    snapshot_id: str = ""
    typed_adjacency: tuple = ()
    contradiction_adjacency: tuple = ()
    window_size: int = 2

    @classmethod
    def from_sentences(cls, sentences, window_size=2, damping=0.65, steps=3):
        return cls.from_sources(
            sentences, relations=(), aliases=(), window_size=window_size,
            damping=damping, steps=steps,
        )

    @classmethod
    def from_sources(cls, sentences, relations=(), aliases=(), window_size=2, damping=0.65, steps=3):
        sentences = tuple(sentences)
        canonical_relations = tuple(_canonical_relation(record) for record in relations)
        canonical_aliases = tuple(_canonical_alias(record) for record in aliases)
        sentence_ids = tuple(stable_sentence_id(sentence) for sentence in sentences)
        sentence_id_set = set(sentence_ids)
        relation_ids = [record["id"] for record in canonical_relations]
        alias_ids = [record["id"] for record in canonical_aliases]
        if len(relation_ids) != len(set(relation_ids)):
            raise ValueError("relation IDs must be unique")
        if len(alias_ids) != len(set(alias_ids)):
            raise ValueError("alias IDs must be unique")
        dangling_evidence = sorted({
            evidence_id
            for record in (*canonical_relations, *canonical_aliases)
            for evidence_id in record["evidence_ids"]
            if evidence_id.startswith("sentence:") and evidence_id not in sentence_id_set
        })
        if dangling_evidence:
            raise ValueError(f"unknown sentence evidence IDs: {dangling_evidence}")

        tokenized = [tokenize(sentence) for sentence in sentences]
        construction_vocab = {token for tokens in tokenized for token in tokens}
        undeclared_endpoints = sorted({
            token for record in canonical_relations
            for token in (record["source"], record["target"])
            if token not in construction_vocab
        })
        undeclared_targets = sorted({
            record["concept"] for record in canonical_aliases
            if record["concept"] not in construction_vocab
        })
        if undeclared_endpoints:
            raise ValueError(f"relation endpoints are not declared construction nodes: {undeclared_endpoints}")
        if undeclared_targets:
            raise ValueError(f"alias targets are not declared construction nodes: {undeclared_targets}")
        vocab = tuple(sorted(construction_vocab))
        if not vocab:
            raise ValueError("at least one construction token is required")
        word2idx = {word: index for index, word in enumerate(vocab)}
        idx2word = {index: word for word, index in word2idx.items()}
        matrix = np.zeros((len(vocab), len(vocab)))

        for tokens in tokenized:
            for index, token in enumerate(tokens):
                target_idx = word2idx[token]
                start = max(0, index - window_size)
                end = min(len(tokens), index + window_size + 1)
                for neighbor_position in range(start, end):
                    if index != neighbor_position:
                        matrix[target_idx, word2idx[tokens[neighbor_position]]] += 1.0

        typed_adjacency = []
        contradiction_adjacency = []
        for record in canonical_relations:
            edge = (record["source"], record["target"], record)
            if record["relation"] == "contradicts":
                contradiction_adjacency.append(edge)
            else:
                typed_adjacency.append(edge)
                # Authored semantic edges are directed and remain distinguishable
                # from co-occurrence through the retained relation records.
                effective_weight = record["weight"] * RELATION_MULTIPLIERS[record["relation"]]
                matrix[word2idx[record["source"]], word2idx[record["target"]]] += effective_weight

        row_sums = matrix.sum(axis=1, keepdims=True)
        row_sums[row_sums == 0] = 1.0
        transition = matrix / row_sums
        document_frequency = Counter(token for tokens in tokenized for token in set(tokens))
        token_idf = np.array([
            math.log((1 + len(tokenized)) / (1 + document_frequency.get(word, 0))) + 1
            for word in vocab
        ])
        degree = np.count_nonzero(matrix, axis=1)
        inverse_degree = 1.0 / np.sqrt(np.maximum(degree, 1))
        background = np.full(len(vocab), 1.0 / len(vocab))
        for _ in range(20):
            background = background @ transition
            total = background.sum()
            if total:
                background /= total

        transition, token_idf, inverse_degree, background = (
            _readonly(array) for array in (transition, token_idf, inverse_degree, background)
        )
        immutable_relations = tuple(MappingProxyType(record) for record in canonical_relations)
        immutable_aliases = tuple(MappingProxyType(record) for record in canonical_aliases)
        immutable_typed = tuple(
            (source, target, immutable_relations[canonical_relations.index(record)])
            for source, target, record in typed_adjacency
        )
        immutable_contradictions = tuple(
            (source, target, immutable_relations[canonical_relations.index(record)])
            for source, target, record in contradiction_adjacency
        )

        source_snapshot = graph_snapshot_id(
            sentences, canonical_relations, canonical_aliases,
            window_size, damping, steps,
        )
        executable_snapshot = _executable_snapshot_id(
            source_snapshot, vocab, (transition, token_idf, inverse_degree, background)
        )

        return cls(
            vocab, MappingProxyType(word2idx), MappingProxyType(idx2word), transition,
            token_idf, inverse_degree, background, damping, steps,
            immutable_relations, immutable_aliases, sentences,
            sentence_ids,
            executable_snapshot,
            immutable_typed, immutable_contradictions, window_size,
        )

    def with_relations(self, relations):
        """Create a new graph; the current snapshot is never mutated."""
        return type(self).from_sources(
            self.sentences, relations=relations, aliases=self.aliases,
            window_size=self.window_size, damping=self.damping, steps=self.steps
        )

    def with_relation_update(self, relation):
        canonical = _canonical_relation(relation)
        records = [record for record in self.relations if record["id"] != canonical["id"]]
        records.append(canonical)
        return self.with_relations(records)

    def with_aliases(self, aliases):
        return type(self).from_sources(
            self.sentences, relations=self.relations, aliases=aliases,
            window_size=self.window_size, damping=self.damping, steps=self.steps
        )

    def with_alias_update(self, alias):
        canonical = _canonical_alias(alias)
        records = [record for record in self.aliases if record["id"] != canonical["id"]]
        records.append(canonical)
        return self.with_aliases(records)

    def resolve_tokens(self, tokens):
        tokens = tokenize(tokens) if isinstance(tokens, str) else list(tokens)
        alias_concepts = []
        ordered_aliases = sorted(self.aliases, key=lambda item: (-len(item["phrase"]), item["id"]))
        occupied = set()
        for alias in ordered_aliases:
            width = len(alias["phrase"])
            for start in range(len(tokens) - width + 1):
                positions = set(range(start, start + width))
                if not positions & occupied and tuple(tokens[start:start + width]) == alias["phrase"]:
                    alias_concepts.append(alias["concept"])
                    occupied.update(positions)
                    break
        token_set = set(tokens)
        resolved = list(alias_concepts)
        river_signals = {"river", "water", "stream", "shore", "shoreline", "flood", "muddy", "canoe"}
        financial_signals = {"money", "account", "loan", "credit", "interest", "deposit", "savings", "payment", "withdrawals"}
        for position, token in enumerate(tokens):
            if position in occupied:
                continue
            if token == "bank":
                has_river_context = bool(token_set & river_signals)
                has_financial_context = bool(token_set & financial_signals)
                if has_river_context and "bank_river" in self.word2idx:
                    resolved.append("bank_river")
                if has_financial_context and "bank_financial" in self.word2idx:
                    resolved.append("bank_financial")
                if not has_river_context and not has_financial_context:
                    resolved.append("bank")
            else:
                resolved.append(token)
        return list(dict.fromkeys(token for token in resolved if token in self.word2idx))

    def _single_field(self, word):
        anchor = np.zeros(len(self.vocab))
        anchor[self.word2idx[word]] = 1.0
        field = anchor.copy()
        for _ in range(self.steps):
            field = self.damping * (field @ self.transition) + (1 - self.damping) * anchor
        return field

    def single_field_activation(self, word):
        """Return one independently propagated field for a governed graph token."""
        if word not in self.word2idx:
            raise KeyError(f"unknown graph token: {word}")
        return self._single_field(word).copy()

    def activation(self, query):
        words = self.resolve_tokens(query)
        if not words:
            return np.zeros(len(self.vocab))
        fields = tuple(
            ActivatedField(word, tuple(self.single_field_activation(word)))
            for word in words
        )
        # Preserve the accepted legacy result for a fully damped isolated node:
        # there is no probability distribution to normalize in this case.
        if not any(any(field.values) for field in fields):
            return np.zeros(len(self.vocab))
        composed = soft_intersection(fields, background=self.background)
        return np.asarray(composed.values)

    def text_activation(self, text):
        words = self.resolve_tokens(tokenize(text))
        if not words:
            return np.zeros(len(self.vocab))
        weighted = np.zeros(len(self.vocab))
        weight_total = 0.0
        for word in words:
            index = self.word2idx[word]
            weight = self.token_idf[index] * self.inverse_degree[index]
            weighted += self.activation(word) * weight
            weight_total += weight
        return weighted / weight_total if weight_total else weighted

    @staticmethod
    def cosine(left, right):
        denominator = np.linalg.norm(left) * np.linalg.norm(right)
        return float(left @ right / denominator) if denominator else 0.0

    def _contradiction_score(self, query, text):
        query_field = self.activation(query)
        document_tokens = set(self.resolve_tokens(tokenize(text)))
        score = 0.0
        for source, target, record in self.contradiction_adjacency:
            if source in document_tokens:
                score += query_field[self.word2idx[target]] * record["weight"]
        return score

    def score(self, query, text, negative_query=None, negative_weight=0.35):
        document = self.text_activation(text)
        positive = self.cosine(self.activation(query), document)
        negative = self._contradiction_score(query, text)
        if negative_query:
            negative += self.cosine(self.activation(negative_query), document)
        return positive - negative_weight * negative

    def _relation_paths(self, query_tokens, document_tokens, limit=5):
        """Return bounded authored-relation paths, not causal attributions."""
        edges = self.typed_adjacency + self.contradiction_adjacency
        by_source = {}
        for source, target, record in edges:
            by_source.setdefault(source, []).append((target, record))
        results = []
        for start in sorted(set(document_tokens)):
            queue = deque([(start, [start], [])])
            while queue and len(results) < limit:
                node, nodes, path_edges = queue.popleft()
                if node in query_tokens and path_edges:
                    weight = math.prod(edge["weight"] for edge in path_edges)
                    results.append({
                        "source": start, "target": node, "nodes": nodes,
                        "edges": [dict(edge) for edge in path_edges], "path_weight": weight,
                    })
                    continue
                if len(path_edges) >= 3:
                    continue
                for target, record in sorted(by_source.get(node, ()), key=lambda pair: pair[1]["id"]):
                    if target not in nodes:
                        queue.append((target, nodes + [target], path_edges + [record]))
        return results

    def _alias_paths(self, query_tokens, text, limit=5):
        tokens = tokenize(text)
        paths = []
        for alias in sorted(self.aliases, key=lambda item: (-len(item["phrase"]), item["id"])):
            width = len(alias["phrase"])
            matched = any(tuple(tokens[start:start + width]) == alias["phrase"] for start in range(len(tokens) - width + 1))
            if matched and alias["concept"] in query_tokens:
                phrase = " ".join(alias["phrase"])
                paths.append({
                    "source": phrase,
                    "target": alias["concept"],
                    "nodes": [phrase, alias["concept"]],
                    "edges": [{
                        "id": alias["id"], "relation": "alias",
                        "weight": alias["confidence"],
                        "evidence_ids": alias["evidence_ids"],
                    }],
                    "path_weight": alias["confidence"],
                })
                if len(paths) >= limit:
                    break
        return paths

    def score_with_explanation(self, query, text, negative_query=None, negative_weight=0.35, path_limit=5):
        document = self.text_activation(text)
        query_activation = self.activation(query)
        positive = self.cosine(query_activation, document)
        contradiction = self._contradiction_score(query, text)
        negative_query_score = (
            self.cosine(self.activation(negative_query), document) if negative_query else 0.0
        )
        negative = contradiction + negative_query_score
        resolved_query = self.resolve_tokens(query)
        resolved_document = self.resolve_tokens(tokenize(text))
        alias_paths = self._alias_paths(set(resolved_query), text, path_limit)
        remaining_path_slots = max(0, path_limit - len(alias_paths))
        return {
            "score": positive - negative_weight * negative,
            "snapshot_id": self.snapshot_id,
            "resolved_query": resolved_query,
            "resolved_document": resolved_document,
            "unknown_query_tokens": [token for token in tokenize(query) if token not in self.word2idx],
            "positive_score": positive,
            "negative_score": negative,
            "negative_components": {
                "typed_contradiction": contradiction,
                "competing_query": negative_query_score,
                "weight": negative_weight,
            },
            "paths": alias_paths + self._relation_paths(
                set(resolved_query), resolved_document, remaining_path_slots
            ),
            "limitations": {
                "causal_decomposition": False,
                "source_provenance_complete": False,
                "note": "Paths are inspectable graph routes, not a complete causal score decomposition.",
            },
        }
