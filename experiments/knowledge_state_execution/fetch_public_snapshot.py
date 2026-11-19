"""Capture a frozen EuroVoc + CELLAR snapshot for the public-knowledge slice.

This is a contributor action that needs network access. CI never runs it: the
benchmark replays only the frozen files it writes. Running it again later will
very likely produce a different snapshot, because CELLAR and EuroVoc are
maintained, living sources; that is a new snapshot version, not a regression.

Scope (declared before fetching):
- EuroVoc concept ``http://eurovoc.europa.eu/2472`` ("information policy") and
  every concept reachable from it by ``skos:narrower`` (``skos:broader*``);
- their ``skos:prefLabel`` in en/fr/de and their ``skos:broader`` edges;
- in-force CELLAR works of sector 3 (legislation) indexed with one of those
  concepts through ``cdm:work_is_about_concept_eurovoc``, with their CELEX ids;
- an independent oracle: for each in-scope concept C, the works that CELLAR's
  own SPARQL engine returns for ``is_about/skos:broader* C`` under the same
  filters.

Usage::

    python3 -m experiments.knowledge_state_execution.fetch_public_snapshot
"""

from __future__ import annotations

import json
import urllib.parse
import urllib.request
from pathlib import Path

from experiments.knowledge_state_execution.ntriples import Triple, serialize_ntriples
from src.helpers.hashing import sha256_bytes
from src.helpers.json_io import write_json
from src.helpers.provenance import utc_now_iso
from src.helpers.text_io import write_text


ROOT = Path(__file__).resolve().parents[2]
SNAPSHOT_DIR = ROOT / "data" / "public" / "eurovoc-information-policy-v1"
ENDPOINT = "https://publications.europa.eu/webapi/rdf/sparql"
ROOT_CONCEPT = "http://eurovoc.europa.eu/2472"
LANGUAGES = ("en", "fr", "de")

SKOS = "http://www.w3.org/2004/02/skos/core#"
CDM = "http://publications.europa.eu/ontology/cdm#"
XSD = "http://www.w3.org/2001/XMLSchema#"

_PREFIXES = f"PREFIX skos: <{SKOS}>\nPREFIX cdm: <{CDM}>\nPREFIX xsd: <{XSD}>\n"
_ACT_FILTER = (
    '?w cdm:resource_legal_in-force "true"^^xsd:boolean ;\n'
    '   cdm:resource_legal_id_sector "3"^^xsd:string .\n'
)

QUERIES = {
    "concepts": _PREFIXES + f"""SELECT ?c ?label WHERE {{
  ?c skos:broader* <{ROOT_CONCEPT}> .
  ?c skos:prefLabel ?label .
  FILTER(lang(?label) IN ({", ".join(f'"{code}"' for code in LANGUAGES)}))
}}""",
    "hierarchy": _PREFIXES + f"""SELECT ?c ?b WHERE {{
  ?c skos:broader* <{ROOT_CONCEPT}> .
  ?c skos:broader ?b .
}}""",
    "acts": _PREFIXES + f"""SELECT ?w ?c ?celex WHERE {{
  ?c skos:broader* <{ROOT_CONCEPT}> .
  ?w cdm:work_is_about_concept_eurovoc ?c .
  {_ACT_FILTER}  OPTIONAL {{ ?w cdm:resource_legal_id_celex ?celex . }}
}}""",
    "oracle": _PREFIXES + f"""SELECT ?q ?w WHERE {{
  ?q skos:broader* <{ROOT_CONCEPT}> .
  ?w cdm:work_is_about_concept_eurovoc/skos:broader* ?q .
  {_ACT_FILTER}}}""",
}


def run_select(query: str) -> tuple[list[dict], bytes]:
    """Execute one SELECT against CELLAR and return bindings plus raw bytes."""
    url = ENDPOINT + "?" + urllib.parse.urlencode({
        "query": query,
        "format": "application/sparql-results+json",
    })
    request = urllib.request.Request(url, headers={"User-Agent": "mml-research-snapshot/1"})
    with urllib.request.urlopen(request, timeout=180) as response:
        raw = response.read()
    return json.loads(raw)["results"]["bindings"], raw


def _value(binding: dict, name: str) -> str:
    return binding[name]["value"]


def build_snapshot(results: dict[str, list[dict]]) -> tuple[list[Triple], dict]:
    """Project the SELECT results onto source-predicate triples and an oracle."""
    triples: list[Triple] = []
    for row in results["concepts"]:
        label = row["label"]
        triples.append(Triple(
            _value(row, "c"), SKOS + "prefLabel", label["value"], "literal",
            label.get("xml:lang"),
        ))
    for row in results["hierarchy"]:
        triples.append(Triple(_value(row, "c"), SKOS + "broader", _value(row, "b")))
    for row in results["acts"]:
        work = _value(row, "w")
        triples.append(Triple(work, CDM + "work_is_about_concept_eurovoc", _value(row, "c")))
        triples.append(Triple(work, CDM + "resource_legal_in-force", "true", "literal", None, XSD + "boolean"))
        if "celex" in row:
            triples.append(Triple(work, CDM + "resource_legal_id_celex", _value(row, "celex"), "literal", None, XSD + "string"))
    oracle: dict[str, set[str]] = {}
    for row in results["oracle"]:
        oracle.setdefault(_value(row, "q"), set()).add(_value(row, "w"))
    return triples, {concept: sorted(works) for concept, works in sorted(oracle.items())}


def main() -> int:
    retrieved_at = utc_now_iso()
    results, raw_hashes = {}, {}
    for name, query in QUERIES.items():
        results[name], raw = run_select(query)
        raw_hashes[name] = sha256_bytes(raw)
        write_text(SNAPSHOT_DIR / "queries" / f"{name}.rq", query + "\n")
    triples, oracle = build_snapshot(results)
    snapshot_text = serialize_ntriples(triples)
    write_text(SNAPSHOT_DIR / "snapshot.nt", snapshot_text)
    write_json(SNAPSHOT_DIR / "oracle.json", {
        "description": (
            "Works returned by CELLAR's own SPARQL engine for "
            "cdm:work_is_about_concept_eurovoc/skos:broader* per in-scope concept. "
            "Independent of the MML compiler; captured in the same session as the snapshot."
        ),
        "query": "queries/oracle.rq",
        "expanded_works_by_concept": oracle,
    })
    write_json(SNAPSHOT_DIR / "manifest.json", {
        "snapshot_id": "eurovoc-information-policy-v1",
        "retrieved_at": retrieved_at,
        "endpoint": ENDPOINT,
        "root_concept": ROOT_CONCEPT,
        "languages": list(LANGUAGES),
        "queries": {name: f"queries/{name}.rq" for name in QUERIES},
        "raw_response_sha256": raw_hashes,
        "row_counts": {name: len(rows) for name, rows in results.items()},
        "snapshot_file": "snapshot.nt",
        "snapshot_sha256": sha256_bytes(snapshot_text.encode("utf-8")),
        "triple_count": snapshot_text.count("\n"),
        "sources": {
            "eurovoc": "EuroVoc thesaurus, Publications Office of the European Union",
            "cellar": "CELLAR common repository metadata, Publications Office of the European Union",
        },
        "terms": {
            "status": "UNVERIFIED",
            "note": (
                "Publications Office metadata and EuroVoc are understood to be reusable under the "
                "Commission reuse policy (Decision 2011/833/EU) with attribution. This was not "
                "confirmed against an authoritative licence statement during capture; a human "
                "maintainer must confirm the terms before the snapshot is redistributed."
            ),
        },
        "living_source_warning": (
            "CELLAR and EuroVoc change over time. Re-running the fetcher creates a new snapshot "
            "version; the frozen files, not the live endpoint, are the experiment input."
        ),
    })
    print(f"wrote {snapshot_text.count(chr(10))} triples to {SNAPSHOT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
