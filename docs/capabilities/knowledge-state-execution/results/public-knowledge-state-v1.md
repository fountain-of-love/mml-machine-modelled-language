# Public Knowledge State v1 — EuroVoc + CELLAR as Compiled MML State

> **Public knowledge becomes executable state without losing its source identity.**

## Research intention

Test the Research Contract's proposed Knowledge State Execution slice: can a narrow, authoritative Linked Open Data domain be compiled once into governed MML state, queried deterministically, traced back to its public identifiers, corrected, and restored — and what does compilation buy over reconstructing the answer at use?

## O — Objective observation

A frozen snapshot of `4824` triples was captured from the CELLAR SPARQL endpoint on `2026-11-19`: the EuroVoc subtree under `http://eurovoc.europa.eu/2472` (*information policy*) and every in-force legislative work indexed with one of its concepts. The mapping policy admitted `1761` assertions (18 `narrower-than`, 1743 `is-about`) over `19` concepts. The compiled state is `sha256:07ee7f79b0fa467571ce2a0b0fcef4d3df41b773c786e17015c1008c4622c09c`.

Compiled answers matched CELLAR's own property-path evaluation for **19/19** concepts and the per-query reconstruction for **19/19**.

## S — Standard, baseline, or reference model

- **Independent oracle:** for every in-scope concept, the works CELLAR's SPARQL engine returns for `cdm:work_is_about_concept_eurovoc/skos:broader*` under the same filters, captured in the same session as the snapshot. It shares no code with the MML compiler.
- **Reconstruction at use:** reread, reparse, and remap the snapshot for every query, then walk the hierarchy from the query concept. It builds only what one query needs.
- **Cached source walk (control):** parse and map once, then walk per query without a precompiled closure. This separates *not reparsing* from *compiling*.
- **Direct-only ablation:** compiled postings without hierarchy expansion.

The correction's dependent queries were declared in `correction_v1.json` before the run. No independent preregistration artifact exists, so the judgment is developmental.

## C — Context and chronology

```text
CELLAR SPARQL (live, once) -> snapshot.nt + oracle.json + manifest.json (frozen, hashed)
  -> mapping_policy_v1.json: skos:broader => narrower-than, work_is_about => is-about
  -> compile closure + postings once (content-addressed)
  -> 19 concept queries + 1 out-of-scope query
  -> trace GDPR back to source triples
  -> correction_v1.json: exclude one hierarchy edge -> recompile -> inspect -> restore
```

Snapshot integrity against the manifest: `True`. Source terms status: `UNVERIFIED` — a maintainer must confirm reuse terms before redistribution.

## A — Actions, interventions, or observed mechanisms

Each admitted assertion's identity is a hash of its exact source triple, so every edge in compiled state names the public statement that justified it. Concepts and works keep their EuroVoc and CELLAR IRIs as identities; labels (en/fr/de) and CELEX numbers are retained for display only.

### Trace: GDPR inside *information policy*

Work `3e485e15-11bd-11e6-ba9a-01aa75ed71a1` (CELEX `32016R0679`) is returned for `2472` (information policy / politique de l'information / Informationspolitik) through 3 routes:

- via `453` *access to information* (accès à l'information / Informationszugang):
  - `src:66c4c0cf7a0dc423` ← `map-work-is-about-v1` ← `<http://publications.europa.eu/resource/cellar/3e485e15-11bd-11e6-ba9a-01aa75ed71a1> <http://publications.europa.eu/ontology/cdm#work_is_about_concept_eurovoc> <http://eurovoc.europa.eu/453> .`
  - `src:c08c29ea7b837814` ← `map-skos-broader-v1` ← `<http://eurovoc.europa.eu/453> <http://www.w3.org/2004/02/skos/core#broader> <http://eurovoc.europa.eu/2472> .`
- via `5181` *data protection* (protection des données / Datenschutz):
  - `src:f35e3839182f6e81` ← `map-work-is-about-v1` ← `<http://publications.europa.eu/resource/cellar/3e485e15-11bd-11e6-ba9a-01aa75ed71a1> <http://publications.europa.eu/ontology/cdm#work_is_about_concept_eurovoc> <http://eurovoc.europa.eu/5181> .`
  - `src:7fe2d8f80bb64d5b` ← `map-skos-broader-v1` ← `<http://eurovoc.europa.eu/5181> <http://www.w3.org/2004/02/skos/core#broader> <http://eurovoc.europa.eu/2472> .`
- via `5334` *disclosure of information* (communication des données / Offenlegung von Daten):
  - `src:e859edcd78ed3095` ← `map-work-is-about-v1` ← `<http://publications.europa.eu/resource/cellar/3e485e15-11bd-11e6-ba9a-01aa75ed71a1> <http://publications.europa.eu/ontology/cdm#work_is_about_concept_eurovoc> <http://eurovoc.europa.eu/5334> .`
  - `src:71038ef81c705ef0` ← `map-skos-broader-v1` ← `<http://eurovoc.europa.eu/5334> <http://www.w3.org/2004/02/skos/core#broader> <http://eurovoc.europa.eu/2472> .`

All `1757` evidence identities used in that query's result resolve to a source triple (`1757` resolved).

## R — Result, effect, or measured outcome

### Correctness against the independent oracle

| Concept | Label (en) | Oracle | Compiled | Reconstruction | Direct only |
| --- | --- | ---: | ---: | ---: | ---: |
| `1367` | information industry | 5 | 5 | 5 | 5 |
| `2472` | information policy | 1503 | 1503 | 1503 | 10 |
| `437539` | right of reply | 0 | 0 | 0 | 0 |
| `437655` | digital literacy | 13 | 13 | 13 | 13 |
| `443` | limited circulation | 1 | 1 | 1 | 1 |
| `453` | access to information | 340 | 340 | 340 | 177 |
| `5181` | data protection | 589 | 589 | 589 | 589 |
| `5196` | law relating to information | 7 | 7 | 7 | 2 |
| `5334` | disclosure of information | 713 | 713 | 713 | 713 |
| `5351` | centralisation of information | 7 | 7 | 7 | 7 |
| `5884` | State secret | 8 | 8 | 8 | 8 |
| `6140` | information society | 44 | 44 | 44 | 44 |
| `7939` | digital divide | 0 | 0 | 0 | 0 |
| `92` | confidentiality | 165 | 165 | 165 | 157 |
| `c_05f9c614` | public data | 0 | 0 | 0 | 0 |
| `c_4cd4362b` | adequacy decision (EU) | 0 | 0 | 0 | 0 |
| `c_5ea6e5c4` | open data | 10 | 10 | 10 | 10 |
| `c_7e60137b` | data governance | 2 | 2 | 2 | 2 |
| `c_d02647e2` | right to reuse information | 5 | 5 | 5 | 5 |

Hierarchy expansion added works for `4` queries; direct-only indexing recovers `0.5108` of the oracle's work answers. The governed hierarchy therefore carries real retrieval consequence here, and it is the source's own hierarchy, not an authored one.

**Refusal.** `5595` (*personal data*) is outside the declared subtree. Both treatments returned `NO_DECLARED_CONSEQUENCE` / `OUT_OF_SCOPE` instead of an empty answer.

### Governed correction and restoration

Correction `exclude-confidentiality-from-access-expansion-v1` (`ILLUSTRATIVE`) excluded assertion `src:f099451c7d396d53` from expansion. The source statement stayed in the snapshot (`True`).

| Changed query | Before | After | Removed | Matches reconstruction | Matches CELLAR |
| --- | ---: | ---: | ---: | --- | --- |
| `2472` | 1503 | 1440 | 63 | True | False |
| `453` | 340 | 190 | 150 | True | False |

Changed set matched the declared expectation: `True`. Protected queries unchanged: `17`. After correction, the changed answers deliberately diverge from CELLAR: the divergence is the governed decision, visible and attributable, not silent drift. Restoring the original policy reproduced snapshot `sha256:07ee7f79b0fa467571ce2a0b0fcef4d3df41b773c786e17015c1008c4622c09c` (equal: `True`).

### Reuse: deterministic structural work

Unit: structural operations = triples parsed + assertions mapped + index entries built + concepts expanded + postings read. Query sequence: cycle over the 19 in-scope concepts in sorted order. Compiled queries read `0` source bytes.

| Queries | Reconstruction at use | Cached source walk | Compiled state |
| ---: | ---: | ---: | ---: |
| 1 | 8352 | 8352 | 8380 |
| 2 | 18460 | 10114 | 10142 |
| 5 | 43515 | 10131 | 10159 |
| 10 | 86930 | 11816 | 11844 |
| 19 | 162288 | 12060 | 12088 |
| 50 | 428252 | 19298 | 19326 |
| 100 | 854955 | 28701 | 28729 |
| 1000 | 8542652 | 204998 | 205026 |

Compiled state is cheaper than reconstruction from the `2`-query horizon. Against the cached source walk, the compiled state's cumulative work differs by `[28]` operations at every horizon: it pays for the closure once and then performs the same per-query expansion and posting reads. **The reuse saving comes from not rereading and reparsing the source, which a parse-once cache provides equally; precomputing the closure adds no measurable work benefit on this 19-concept tree.**

### Wall-clock observations (descriptive, machine-local)

| Operation | Median (ns) |
| --- | ---: |
| compiled cold read parse map compile | 40689584 |
| cached walk build read parse map | 23764875 |
| correction remap and recompile from parsed triples | 20972167 |
| mean reconstruction query | 26254407 |
| mean cached walk query | 48673 |
| mean compiled query | 160100 |

Reconstruction per query took `164.0x` the compiled query time; the cached walk took `0.3x`. The compiled query materializes a full evidence chain for every match, while the cached walk returns bare work identities, so a ratio below 1 is the measured price of traceability, not a defect hidden by the counters. Cold compilation was recovered after about `2` queries versus reconstruction. Descriptive machine-local observations for this Python process and snapshot; not a production performance comparison and not an energy measurement.

## C — Comparative assessment and research conclusion

**Conformity judgment: `CONSISTENT`.** 10/10 declared criteria held.

- `source_snapshot_matches_manifest`: `True`
- `identities_are_source_iris`: `True`
- `compiled_matches_independent_cellar_oracle`: `True`
- `reconstruction_matches_compiled`: `True`
- `deterministic_replay`: `True`
- `out_of_scope_refused_not_answered_empty`: `True`
- `every_result_evidence_resolves_to_source_triple`: `True`
- `correction_changes_exactly_expected_queries`: `True`
- `correction_keeps_source_statement`: `True`
- `restoration_is_exact`: `True`

**Evidence strength: `LOW`** for generalization (one domain, one tree-shaped 19-concept hierarchy, one rule, one machine). The independent CELLAR oracle makes the *correctness* result considerably stronger than the authored v1 fixture.

**What this shows.** URI-addressed public knowledge can be compiled into content-addressed MML state that reproduces an independent engine's answers, refuses out-of-scope questions, traces every result to exact source statements, and accepts a reversible governed correction whose consequences are enumerable before and after.

**What it does not show — negative evidence preserved.** At this scale the precompiled closure is not where any saving comes from: a parse-once cache matches its structural work and its bare queries are faster than evidence-carrying compiled queries. Compiled state earns its place here through content identity, traceability, typed refusal, and governed correction, not latency. Whether closure precomputation pays off needs deeper, wider, or polyhierarchical vocabularies and is untested. No legal conclusion follows: `is-about` is documentary indexing, and `skos:broader` is not subsumption. No energy, LLM, or production-scale claim is made.

## Next step

Add a polyhierarchical or `skos:related` slice where expansion is not a tree, so that the closure, chain selection, and correction blast radius are actually stressed; then add a measured language-model reconstruction baseline over the same snapshot and questions.

This report follows the [OSCARC methodology](../../../benchmark/oscarc-methodology.md). The [machine-readable artifact](../../../../benchmark/results/public-knowledge-state-v1.json) is authoritative.
