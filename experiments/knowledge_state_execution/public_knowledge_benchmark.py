"""Public Knowledge State v1: EuroVoc + CELLAR compiled into reusable MML state.

Public source -> stable identifiers -> governed mapping -> compiled state
-> deterministic query -> provenance trace -> governed correction -> restore.

Stable evidence (answers, agreement, counters, identities, correction
consequences) is checked for freshness. Wall-clock timings are descriptive,
machine-local observations and are excluded from freshness equality.
"""

from __future__ import annotations

import math
import statistics
import time
from pathlib import Path

from experiments.knowledge_state_execution.public_knowledge import (
    SNAPSHOT_DIR,
    MappingPolicy,
    WorkCounters,
    build_walk_index,
    celex_by_work,
    labels_by_concept,
    load_correction,
    map_assertions,
    read_snapshot,
    reconstruct_and_answer,
    walk_answer,
)
from src.helpers.artifacts import compare_artifact_pair, write_artifact_pair
from src.helpers.hashing import sha256_file
from src.helpers.json_io import read_json
from src.helpers.provenance import runtime_identity, utc_now_iso
from src.helpers.research_cli import ResearchCommand, run_research_command
from src.knowledge_state_execution.subject_expansion_state import (
    NO_DECLARED_CONSEQUENCE,
    OUT_OF_SCOPE,
    compile_subject_expansion_state,
    execute_subject_query,
)


ROOT = Path(__file__).resolve().parents[2]
BENCHMARK_ID = "public-knowledge-state-v1"
RESULT_PATH = ROOT / "benchmark" / "results" / f"{BENCHMARK_ID}.json"
REPORT_PATH = ROOT / "docs" / "capabilities" / "knowledge-state-execution" / "results" / f"{BENCHMARK_ID}.md"
SNAPSHOT_PATH = SNAPSHOT_DIR / "snapshot.nt"
OUT_OF_SCOPE_QUERY = "http://eurovoc.europa.eu/5595"  # 'personal data': GDPR subject outside the declared subtree
TRACE_QUERY = "http://eurovoc.europa.eu/2472"
TRACE_WORK = "http://publications.europa.eu/resource/cellar/3e485e15-11bd-11e6-ba9a-01aa75ed71a1"  # GDPR
REUSE_HORIZONS = (1, 2, 5, 10, 19, 50, 100, 1000)
VOLATILE_FIELDS = ("generated_at", "timing", "provenance")


def _median_ns(operation, repetitions: int) -> int:
    samples = []
    for _ in range(repetitions):
        started = time.perf_counter_ns()
        operation()
        samples.append(time.perf_counter_ns() - started)
    return int(statistics.median(samples))


def _compile_from_source(policy, excluded=frozenset()):
    triples, size = read_snapshot(SNAPSHOT_PATH)
    mapping = map_assertions(triples, policy, excluded)
    return triples, size, mapping, compile_subject_expansion_state(mapping.assertions)


def _source_identity(manifest: dict) -> dict:
    actual = sha256_file(SNAPSHOT_PATH)
    return {
        "snapshot_file": "data/public/eurovoc-information-policy-v1/snapshot.nt",
        "snapshot_sha256": actual,
        "matches_manifest": actual == manifest["snapshot_sha256"],
        "retrieved_at": manifest["retrieved_at"],
        "endpoint": manifest["endpoint"],
        "root_concept": manifest["root_concept"],
        "triple_count": manifest["triple_count"],
        "terms_status": manifest["terms"]["status"],
        "governed_inputs": {
            name: sha256_file(SNAPSHOT_DIR / name)
            for name in ("mapping_policy_v1.json", "correction_v1.json", "oracle.json", "manifest.json")
        },
    }


def _agreement(state, policy, oracle, labels) -> tuple[list[dict], dict]:
    rows = []
    for concept in sorted(state.concepts):
        compiled = execute_subject_query(state, concept)
        reconstructed = reconstruct_and_answer(SNAPSHOT_PATH, policy, concept)
        expected = tuple(oracle.get(concept, ()))
        direct = tuple(sorted({work for work, _ in state.postings[concept]}))
        rows.append({
            "concept": concept,
            "label_en": labels.get(concept, {}).get("en"),
            "oracle_works": len(expected),
            "compiled_works": len(compiled.works),
            "reconstruction_works": len(reconstructed.works),
            "direct_only_works": len(direct),
            "compiled_matches_oracle": compiled.works == expected,
            "reconstruction_matches_compiled": reconstructed.works == compiled.works,
            "direct_only_matches_oracle": direct == expected,
            "compiled_query_work": {
                "bytes_read": 0,
                "concepts_expanded": compiled.concepts_expanded,
                "postings_read": compiled.postings_read,
            },
            "reconstruction_query_work": reconstructed.counters.as_dict(),
        })
    expanded_total = sum(r["oracle_works"] for r in rows)
    direct_hits = sum(r["direct_only_works"] for r in rows)
    summary = {
        "queries": len(rows),
        "compiled_matches_oracle": sum(r["compiled_matches_oracle"] for r in rows),
        "reconstruction_matches_compiled": sum(r["reconstruction_matches_compiled"] for r in rows),
        "direct_only_matches_oracle": sum(r["direct_only_matches_oracle"] for r in rows),
        "queries_where_hierarchy_adds_works": sum(r["direct_only_works"] < r["oracle_works"] for r in rows),
        "oracle_work_answers_total": expanded_total,
        "direct_only_work_answers_total": direct_hits,
        "direct_only_recall_of_oracle": round(direct_hits / expanded_total, 4) if expanded_total else None,
    }
    return rows, summary


def _trace(state, mapping, labels, celex) -> dict:
    outcome = execute_subject_query(state, TRACE_QUERY)
    every_evidence = {aid for match in outcome.matches for aid in match.evidence}
    routes = []
    for match in outcome.matches:
        if match.work != TRACE_WORK:
            continue
        routes.append({
            "via_concept": match.via_concept,
            "via_labels": labels.get(match.via_concept, {}),
            "evidence": [
                {"assertion_id": aid, **mapping.provenance[aid]} for aid in match.evidence
            ],
        })
    return {
        "query": TRACE_QUERY,
        "query_labels": labels.get(TRACE_QUERY, {}),
        "work": TRACE_WORK,
        "celex": celex.get(TRACE_WORK),
        "routes": routes,
        "evidence_ids_in_result": len(every_evidence),
        "evidence_ids_resolving_to_source": sum(aid in mapping.provenance for aid in every_evidence),
    }


def _refusal(state, policy) -> dict:
    compiled = execute_subject_query(state, OUT_OF_SCOPE_QUERY)
    reconstructed = reconstruct_and_answer(SNAPSHOT_PATH, policy, OUT_OF_SCOPE_QUERY)
    return {
        "query": OUT_OF_SCOPE_QUERY,
        "compiled": {"status": compiled.status, "reason": compiled.reason},
        "reconstruction": {"status": reconstructed.status, "reason": reconstructed.reason},
        "refused_by_both": all(
            (item.status, item.reason) == (NO_DECLARED_CONSEQUENCE, OUT_OF_SCOPE)
            for item in (compiled, reconstructed)
        ),
    }


def _correction(state, triples, policy, oracle) -> dict:
    correction = load_correction()
    excluded = frozenset({correction["source_triple_parsed"]})
    corrected_mapping = map_assertions(triples, policy, excluded)
    corrected = compile_subject_expansion_state(corrected_mapping.assertions)
    changed, unchanged = {}, 0
    for concept in sorted(state.concepts):
        before = execute_subject_query(state, concept).works
        after = execute_subject_query(corrected, concept).works
        if before == after:
            unchanged += 1
            continue
        changed[concept] = {
            "before": len(before),
            "after": len(after),
            "removed": len(set(before) - set(after)),
            "added": len(set(after) - set(before)),
            "corrected_matches_oracle": after == tuple(oracle.get(concept, ())),
            "corrected_matches_reconstruction": after == reconstruct_and_answer(
                SNAPSHOT_PATH, policy, concept, excluded
            ).works,
        }
    restored_mapping = map_assertions(triples, policy)
    restored = compile_subject_expansion_state(restored_mapping.assertions)
    restored_equal = all(
        execute_subject_query(restored, c).works == execute_subject_query(state, c).works
        for c in state.concepts
    )
    return {
        "correction_id": correction["correction_id"],
        "status": correction["status"],
        "excluded_assertion_ids": list(corrected_mapping.excluded),
        "source_triple_retained_in_snapshot": correction["source_triple_parsed"] in set(triples),
        "corrected_snapshot_id": corrected.snapshot_id,
        "expected_dependent_queries": correction["expected_dependent_queries"],
        "observed_changed_queries": changed,
        "changed_set_matches_expectation": sorted(changed) == sorted(correction["expected_dependent_queries"]),
        "protected_unchanged_queries": unchanged,
        "divergence_from_source_is_governed": all(not v["corrected_matches_oracle"] for v in changed.values()),
        "restored_snapshot_id": restored.snapshot_id,
        "restored_snapshot_equals_original": restored.snapshot_id == state.snapshot_id,
        "restored_answers_equal_original": restored_equal,
    }


def _work_model(state, policy, agreement_rows, triple_count: int, source_bytes: int) -> dict:
    """Deterministic cumulative structural work; separate from wall-clock."""
    queries = [row["concept"] for row in agreement_rows]
    metrics = state.compilation
    compile_once = WorkCounters(
        bytes_read=source_bytes,
        triples_parsed=triple_count,
        assertions_mapped=metrics.assertions_read,
        index_entries_built=metrics.closure_entries + metrics.posting_entries,
    ).structural_operations()
    cached_build = WorkCounters()
    index = build_walk_index(SNAPSHOT_PATH, policy, cached_build)

    def reconstruct(i):
        return agreement_rows[i % len(queries)]["reconstruction_query_work"]["structural_operations"]

    def compiled(i):
        work = agreement_rows[i % len(queries)]["compiled_query_work"]
        return work["concepts_expanded"] + work["postings_read"]

    def cached(i):
        counters = WorkCounters()
        walk_answer(index, queries[i % len(queries)], counters)
        return counters.structural_operations()

    curve = []
    for horizon in REUSE_HORIZONS:
        curve.append({
            "queries": horizon,
            "reconstruction_at_use": sum(reconstruct(i) for i in range(horizon)),
            "cached_source_walk": cached_build.structural_operations() + sum(cached(i) for i in range(horizon)),
            "compiled_state": compile_once + sum(compiled(i) for i in range(horizon)),
        })
    break_even = next(
        (point["queries"] for point in curve if point["compiled_state"] < point["reconstruction_at_use"]), None
    )
    return {
        "unit": "structural operations = triples parsed + assertions mapped + index entries built + concepts expanded + postings read",
        "query_sequence": "cycle over the 19 in-scope concepts in sorted order",
        "compile_once_structural_operations": compile_once,
        "compile_once_bytes_read": source_bytes,
        "cached_build_structural_operations": cached_build.structural_operations(),
        "compiled_query_bytes_read": 0,
        "cumulative_curve": curve,
        "first_listed_horizon_where_compiled_is_cheaper_than_reconstruction": break_even,
        "compiled_minus_cached_at_every_horizon": sorted(
            {point["compiled_state"] - point["cached_source_walk"] for point in curve}
        ),
    }


def _timing(policy, state, concepts, triples) -> dict:
    reconstruction = statistics.mean(
        _median_ns(lambda c=c: reconstruct_and_answer(SNAPSHOT_PATH, policy, c), 5) for c in concepts
    )
    index = build_walk_index(SNAPSHOT_PATH, policy, WorkCounters())
    cached_query = statistics.mean(
        _median_ns(lambda c=c: walk_answer(index, c, WorkCounters()), 51) for c in concepts
    )
    compiled_query = statistics.mean(
        _median_ns(lambda c=c: execute_subject_query(state, c), 51) for c in concepts
    )
    compile_cold = _median_ns(lambda: _compile_from_source(policy), 5)
    cached_build = _median_ns(lambda: build_walk_index(SNAPSHOT_PATH, policy, WorkCounters()), 5)
    excluded = frozenset({load_correction()["source_triple_parsed"]})
    recompile = _median_ns(
        lambda: compile_subject_expansion_state(map_assertions(triples, policy, excluded).assertions), 5
    )
    saving = reconstruction - compiled_query
    return {
        "clock": "time.perf_counter_ns",
        "runtime": runtime_identity({"numpy": "not used"}),
        "interpretation": (
            "Descriptive machine-local observations for this Python process and snapshot; "
            "not a production performance comparison and not an energy measurement."
        ),
        "median_ns": {
            "compiled_cold_read_parse_map_compile": compile_cold,
            "cached_walk_build_read_parse_map": cached_build,
            "correction_remap_and_recompile_from_parsed_triples": recompile,
            "mean_reconstruction_query": int(reconstruction),
            "mean_cached_walk_query": int(cached_query),
            "mean_compiled_query": int(compiled_query),
        },
        "derived": {
            "reconstruction_over_compiled_query_ratio": round(reconstruction / compiled_query, 1),
            "cached_walk_over_compiled_query_ratio": round(cached_query / compiled_query, 2),
            "compiled_break_even_queries_vs_reconstruction": math.ceil(compile_cold / saving) if saving > 0 else None,
            "compile_closure_overhead_vs_cached_build_ns": compile_cold - cached_build,
        },
    }


def run_experiment(*, include_timing: bool = True) -> dict:
    manifest = read_json(SNAPSHOT_DIR / "manifest.json")
    oracle = read_json(SNAPSHOT_DIR / "oracle.json")["expanded_works_by_concept"]
    policy = MappingPolicy.load()
    triples, source_bytes, mapping, state = _compile_from_source(policy)
    replay = compile_subject_expansion_state(tuple(reversed(mapping.assertions)))
    labels, celex = labels_by_concept(triples), celex_by_work(triples)
    source_endpoints = {(t.subject, t.object) for t in triples if t.object_kind == "iri"}
    agreement_rows, agreement = _agreement(state, policy, oracle, labels)
    result = {
        "benchmark": BENCHMARK_ID,
        "generated_at": utc_now_iso(),
        "declared_rule": "works_about(Q) = { w | w is-about c and c narrower-than* Q }",
        "source": _source_identity(manifest),
        "mapping_policy": {
            "policy_id": policy.policy_id,
            "admitted_assertions": len(mapping.assertions),
            "admitted_by_decision": {
                decision: sum(p["mapping_decision"] == decision for p in mapping.provenance.values())
                for decision in sorted(policy.decision_by_predicate.values())
            },
        },
        "compiled_state": {
            "snapshot_id": state.snapshot_id,
            "metrics": dict(state.compilation.__dict__),
            "deterministic_replay": replay.snapshot_id == state.snapshot_id,
            "identities_are_source_iris": all(
                (a.subject, a.object) in source_endpoints for a in state.assertions
            ),
        },
        "agreement": agreement,
        "per_query": agreement_rows,
        "refusal": _refusal(state, policy),
        "trace": _trace(state, mapping, labels, celex),
        "correction": _correction(state, triples, policy, oracle),
        "work_model": _work_model(state, policy, agreement_rows, len(triples), source_bytes),
    }
    result["conformity"] = _conformity(result)
    if include_timing:
        result["timing"] = _timing(policy, state, sorted(state.concepts), triples)
    return result


def _conformity(result: dict) -> dict:
    agreement, correction, trace = result["agreement"], result["correction"], result["trace"]
    criteria = {
        "source_snapshot_matches_manifest": result["source"]["matches_manifest"],
        "identities_are_source_iris": result["compiled_state"]["identities_are_source_iris"],
        "compiled_matches_independent_cellar_oracle": agreement["compiled_matches_oracle"] == agreement["queries"],
        "reconstruction_matches_compiled": agreement["reconstruction_matches_compiled"] == agreement["queries"],
        "deterministic_replay": result["compiled_state"]["deterministic_replay"],
        "out_of_scope_refused_not_answered_empty": result["refusal"]["refused_by_both"],
        "every_result_evidence_resolves_to_source_triple": (
            trace["evidence_ids_in_result"] == trace["evidence_ids_resolving_to_source"] and bool(trace["routes"])
        ),
        "correction_changes_exactly_expected_queries": correction["changed_set_matches_expectation"],
        "correction_keeps_source_statement": correction["source_triple_retained_in_snapshot"],
        "restoration_is_exact": (
            correction["restored_snapshot_equals_original"] and correction["restored_answers_equal_original"]
        ),
    }
    return {"criteria": criteria, "verdict": "CONSISTENT" if all(criteria.values()) else "INCONSISTENT"}


def _short(iri: str) -> str:
    return iri.rsplit("/", 1)[-1]


def markdown_report(result: dict) -> str:
    source, state, agreement = result["source"], result["compiled_state"], result["agreement"]
    correction, trace, work = result["correction"], result["trace"], result["work_model"]
    timing = result.get("timing")
    lines = [
        "# Public Knowledge State v1 — EuroVoc + CELLAR as Compiled MML State",
        "",
        "> **Public knowledge becomes executable state without losing its source identity.**",
        "",
        "## Research intention",
        "",
        "Test the Research Contract's proposed Knowledge State Execution slice: can a narrow, "
        "authoritative Linked Open Data domain be compiled once into governed MML state, queried "
        "deterministically, traced back to its public identifiers, corrected, and restored — and "
        "what does compilation buy over reconstructing the answer at use?",
        "",
        "## O — Objective observation",
        "",
        f"A frozen snapshot of `{source['triple_count']}` triples was captured from the CELLAR SPARQL "
        f"endpoint on `{source['retrieved_at'][:10]}`: the EuroVoc subtree under "
        f"`{source['root_concept']}` (*information policy*) and every in-force legislative work "
        "indexed with one of its concepts. The mapping policy admitted "
        f"`{result['mapping_policy']['admitted_assertions']}` assertions "
        f"({state['metrics']['hierarchy_edges']} `narrower-than`, {state['metrics']['aboutness_edges']} `is-about`) "
        f"over `{state['metrics']['concepts']}` concepts. The compiled state is "
        f"`{state['snapshot_id']}`.",
        "",
        f"Compiled answers matched CELLAR's own property-path evaluation for "
        f"**{agreement['compiled_matches_oracle']}/{agreement['queries']}** concepts and the per-query "
        f"reconstruction for **{agreement['reconstruction_matches_compiled']}/{agreement['queries']}**.",
        "",
        "## S — Standard, baseline, or reference model",
        "",
        "- **Independent oracle:** for every in-scope concept, the works CELLAR's SPARQL engine returns "
        "for `cdm:work_is_about_concept_eurovoc/skos:broader*` under the same filters, captured in the "
        "same session as the snapshot. It shares no code with the MML compiler.",
        "- **Reconstruction at use:** reread, reparse, and remap the snapshot for every query, then walk "
        "the hierarchy from the query concept. It builds only what one query needs.",
        "- **Cached source walk (control):** parse and map once, then walk per query without a "
        "precompiled closure. This separates *not reparsing* from *compiling*.",
        "- **Direct-only ablation:** compiled postings without hierarchy expansion.",
        "",
        "The correction's dependent queries were declared in `correction_v1.json` before the run. "
        "No independent preregistration artifact exists, so the judgment is developmental.",
        "",
        "## C — Context and chronology",
        "",
        "```text",
        "CELLAR SPARQL (live, once) -> snapshot.nt + oracle.json + manifest.json (frozen, hashed)",
        "  -> mapping_policy_v1.json: skos:broader => narrower-than, work_is_about => is-about",
        "  -> compile closure + postings once (content-addressed)",
        "  -> 19 concept queries + 1 out-of-scope query",
        "  -> trace GDPR back to source triples",
        "  -> correction_v1.json: exclude one hierarchy edge -> recompile -> inspect -> restore",
        "```",
        "",
        f"Snapshot integrity against the manifest: `{source['matches_manifest']}`. Source terms status: "
        f"`{source['terms_status']}` — a maintainer must confirm reuse terms before redistribution.",
        "",
        "## A — Actions, interventions, or observed mechanisms",
        "",
        "Each admitted assertion's identity is a hash of its exact source triple, so every edge in "
        "compiled state names the public statement that justified it. Concepts and works keep their "
        "EuroVoc and CELLAR IRIs as identities; labels (en/fr/de) and CELEX numbers are retained for "
        "display only.",
        "",
        "### Trace: GDPR inside *information policy*",
        "",
        f"Work `{_short(trace['work'])}` (CELEX `{trace['celex']}`) is returned for "
        f"`{_short(trace['query'])}` ({trace['query_labels'].get('en')} / "
        f"{trace['query_labels'].get('fr')} / {trace['query_labels'].get('de')}) through "
        f"{len(trace['routes'])} routes:",
        "",
    ]
    for route in trace["routes"]:
        labels = route["via_labels"]
        lines.append(f"- via `{_short(route['via_concept'])}` *{labels.get('en')}* "
                     f"({labels.get('fr')} / {labels.get('de')}):")
        for item in route["evidence"]:
            lines.append(f"  - `{item['assertion_id']}` ← `{item['mapping_decision']}` ← "
                         f"`{item['source_triple']}`")
    lines += [
        "",
        f"All `{trace['evidence_ids_in_result']}` evidence identities used in that query's result "
        f"resolve to a source triple (`{trace['evidence_ids_resolving_to_source']}` resolved).",
        "",
        "## R — Result, effect, or measured outcome",
        "",
        "### Correctness against the independent oracle",
        "",
        "| Concept | Label (en) | Oracle | Compiled | Reconstruction | Direct only |",
        "| --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for row in result["per_query"]:
        lines.append(
            f"| `{_short(row['concept'])}` | {row['label_en']} | {row['oracle_works']} | "
            f"{row['compiled_works']} | {row['reconstruction_works']} | {row['direct_only_works']} |"
        )
    lines += [
        "",
        f"Hierarchy expansion added works for `{agreement['queries_where_hierarchy_adds_works']}` "
        f"queries; direct-only indexing recovers `{agreement['direct_only_recall_of_oracle']}` of the "
        "oracle's work answers. The governed hierarchy therefore carries real retrieval consequence "
        "here, and it is the source's own hierarchy, not an authored one.",
        "",
        f"**Refusal.** `{_short(result['refusal']['query'])}` (*personal data*) is outside the declared "
        f"subtree. Both treatments returned `{result['refusal']['compiled']['status']}` / "
        f"`{result['refusal']['compiled']['reason']}` instead of an empty answer.",
        "",
        "### Governed correction and restoration",
        "",
        f"Correction `{correction['correction_id']}` (`{correction['status']}`) excluded assertion "
        f"`{', '.join(correction['excluded_assertion_ids'])}` from expansion. The source statement "
        f"stayed in the snapshot (`{correction['source_triple_retained_in_snapshot']}`).",
        "",
        "| Changed query | Before | After | Removed | Matches reconstruction | Matches CELLAR |",
        "| --- | ---: | ---: | ---: | --- | --- |",
    ]
    for concept, change in correction["observed_changed_queries"].items():
        lines.append(
            f"| `{_short(concept)}` | {change['before']} | {change['after']} | {change['removed']} | "
            f"{change['corrected_matches_reconstruction']} | {change['corrected_matches_oracle']} |"
        )
    lines += [
        "",
        f"Changed set matched the declared expectation: `{correction['changed_set_matches_expectation']}`. "
        f"Protected queries unchanged: `{correction['protected_unchanged_queries']}`. After correction, "
        "the changed answers deliberately diverge from CELLAR: the divergence is the governed decision, "
        "visible and attributable, not silent drift. Restoring the original policy reproduced snapshot "
        f"`{correction['restored_snapshot_id']}` (equal: `{correction['restored_snapshot_equals_original']}`).",
        "",
        "### Reuse: deterministic structural work",
        "",
        f"Unit: {work['unit']}. Query sequence: {work['query_sequence']}. Compiled queries read "
        f"`{work['compiled_query_bytes_read']}` source bytes.",
        "",
        "| Queries | Reconstruction at use | Cached source walk | Compiled state |",
        "| ---: | ---: | ---: | ---: |",
    ]
    for point in work["cumulative_curve"]:
        lines.append(f"| {point['queries']} | {point['reconstruction_at_use']} | "
                     f"{point['cached_source_walk']} | {point['compiled_state']} |")
    gap = work["compiled_minus_cached_at_every_horizon"]
    lines += [
        "",
        f"Compiled state is cheaper than reconstruction from the "
        f"`{work['first_listed_horizon_where_compiled_is_cheaper_than_reconstruction']}`-query horizon. "
        f"Against the cached source walk, the compiled state's cumulative work differs by `{gap}` "
        "operations at every horizon: it pays for the closure once and then performs the same "
        "per-query expansion and posting reads. **The reuse saving comes from not rereading and "
        "reparsing the source, which a parse-once cache provides equally; precomputing the closure "
        "adds no measurable work benefit on this 19-concept tree.**",
        "",
    ]
    if timing:
        median, derived = timing["median_ns"], timing["derived"]
        lines += [
            "### Wall-clock observations (descriptive, machine-local)",
            "",
            "| Operation | Median (ns) |",
            "| --- | ---: |",
            *[f"| {name.replace('_', ' ')} | {value} |" for name, value in median.items()],
            "",
            f"Reconstruction per query took `{derived['reconstruction_over_compiled_query_ratio']}x` the "
            f"compiled query time; the cached walk took `{derived['cached_walk_over_compiled_query_ratio']}x`. "
            "The compiled query materializes a full evidence chain for every match, while the cached "
            "walk returns bare work identities, so a ratio below 1 is the measured price of "
            "traceability, not a defect hidden by the counters. Cold compilation was recovered after "
            f"about `{derived['compiled_break_even_queries_vs_reconstruction']}` queries versus "
            f"reconstruction. {timing['interpretation']}",
            "",
        ]
    criteria = result["conformity"]["criteria"]
    lines += [
        "## C — Comparative assessment and research conclusion",
        "",
        f"**Conformity judgment: `{result['conformity']['verdict']}`.** "
        f"{sum(criteria.values())}/{len(criteria)} declared criteria held.",
        "",
        *[f"- `{name}`: `{value}`" for name, value in criteria.items()],
        "",
        "**Evidence strength: `LOW`** for generalization (one domain, one tree-shaped 19-concept "
        "hierarchy, one rule, one machine). The independent CELLAR oracle makes the *correctness* "
        "result considerably stronger than the authored v1 fixture.",
        "",
        "**What this shows.** URI-addressed public knowledge can be compiled into content-addressed "
        "MML state that reproduces an independent engine's answers, refuses out-of-scope questions, "
        "traces every result to exact source statements, and accepts a reversible governed correction "
        "whose consequences are enumerable before and after.",
        "",
        "**What it does not show — negative evidence preserved.** At this scale the precompiled "
        "closure is not where any saving comes from: a parse-once cache matches its structural work "
        "and its bare queries are faster than evidence-carrying compiled queries. Compiled state earns "
        "its place here through content identity, traceability, typed refusal, and governed "
        "correction, not latency. Whether closure precomputation pays off needs deeper, wider, or "
        "polyhierarchical vocabularies and is untested. No legal "
        "conclusion follows: `is-about` is documentary indexing, and `skos:broader` is not "
        "subsumption. No energy, LLM, or production-scale claim is made.",
        "",
        "## Next step",
        "",
        "Add a polyhierarchical or `skos:related` slice where expansion is not a tree, so that the "
        "closure, chain selection, and correction blast radius are actually stressed; then add a "
        "measured language-model reconstruction baseline over the same snapshot and questions.",
        "",
        "This report follows the [OSCARC methodology](../../../benchmark/oscarc-methodology.md). The "
        "[machine-readable artifact](../../../../benchmark/results/public-knowledge-state-v1.json) is "
        "authoritative.",
    ]
    return "\n".join(lines) + "\n"


def check_result(result: dict) -> None:
    failed = [name for name, ok in result["conformity"]["criteria"].items() if not ok]
    if failed:
        raise SystemExit(f"Public knowledge state criteria failed: {', '.join(failed)}")


def write_results(result: dict) -> None:
    write_artifact_pair(RESULT_PATH, result, REPORT_PATH, markdown_report(result))


def check_artifact_freshness(result: dict) -> None:
    if not RESULT_PATH.exists() or not REPORT_PATH.exists():
        raise SystemExit("Public knowledge state artifacts are missing; run with --write.")
    reference = read_json(RESULT_PATH)
    comparison = compare_artifact_pair(
        result, markdown_report(reference), RESULT_PATH, REPORT_PATH, volatile_fields=VOLATILE_FIELDS
    )
    if not comparison.json_matches:
        raise SystemExit("Public knowledge state JSON is stale; regenerate with --write.")
    if not comparison.text_matches:
        raise SystemExit("Public knowledge state report is stale; regenerate with --write.")


def main() -> None:
    run_research_command(ResearchCommand(
        description="Run the Public Knowledge State v1 experiment.",
        run=run_experiment,
        validate=check_result,
        write=write_results,
        check=check_artifact_freshness,
        render=markdown_report,
    ))


if __name__ == "__main__":
    main()
