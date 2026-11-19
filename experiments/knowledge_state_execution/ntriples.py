"""Minimal N-Triples reading and writing for frozen public-knowledge snapshots.

This is deliberately a subset implementation: absolute IRIs, plain, language-
tagged, and datatyped literals, one triple per line. It covers exactly what the
snapshot fetcher writes. Blank nodes and other RDF syntaxes are refused rather
than guessed, so an unexpected source shape fails loudly.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable, Iterator


_IRI = r"<([^<>\"{}|^`\\\s]+)>"
_LITERAL = r'"((?:[^"\\]|\\.)*)"(?:@([A-Za-z]+(?:-[A-Za-z0-9]+)*)|\^\^' + _IRI + r")?"
_TRIPLE = re.compile(r"^" + _IRI + r"\s+" + _IRI + r"\s+(?:" + _IRI + r"|" + _LITERAL + r")\s*\.\s*$")
_ESCAPES = {"\\": "\\\\", '"': '\\"', "\n": "\\n", "\r": "\\r", "\t": "\\t"}
_UNESCAPES = {"\\\\": "\\", '\\"': '"', "\\n": "\n", "\\r": "\r", "\\t": "\t"}


@dataclass(frozen=True, order=True)
class Triple:
    """One RDF statement; ``object_kind`` is ``iri`` or ``literal``."""

    subject: str
    predicate: str
    object: str
    object_kind: str = "iri"
    language: str | None = None
    datatype: str | None = None


def _escape(value: str) -> str:
    return "".join(_ESCAPES.get(character, character) for character in value)


def _unescape(value: str) -> str:
    return re.sub(r"\\[\\\"nrt]", lambda match: _UNESCAPES[match.group(0)], value)


def serialize_triple(triple: Triple) -> str:
    """Return the canonical one-line N-Triples form of ``triple``."""
    head = f"<{triple.subject}> <{triple.predicate}> "
    if triple.object_kind == "iri":
        return f"{head}<{triple.object}> ."
    literal = f'"{_escape(triple.object)}"'
    if triple.language:
        literal += f"@{triple.language}"
    elif triple.datatype:
        literal += f"^^<{triple.datatype}>"
    return f"{head}{literal} ."


def parse_line(line: str) -> Triple:
    """Parse one non-empty N-Triples line or raise ``ValueError``."""
    match = _TRIPLE.match(line)
    if match is None:
        raise ValueError(f"unsupported N-Triples line: {line[:120]!r}")
    subject, predicate, object_iri, literal, language, datatype = match.groups()
    if object_iri is not None:
        return Triple(subject, predicate, object_iri)
    return Triple(subject, predicate, _unescape(literal), "literal", language, datatype)


def parse_ntriples(text: str) -> Iterator[Triple]:
    """Yield triples from N-Triples text, skipping blank lines and comments."""
    for line in text.splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            yield parse_line(stripped)


def serialize_ntriples(triples: Iterable[Triple]) -> str:
    """Return sorted, de-duplicated N-Triples text with a trailing newline."""
    return "".join(f"{line}\n" for line in sorted({serialize_triple(t) for t in triples}))
