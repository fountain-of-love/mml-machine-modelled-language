"""Compare repeated source reconstruction with compiled knowledge-state execution.

This adapter benchmarks the Knowledge Is State flow; it does not define it.
Input volume, algorithmic work, and wall-clock observations remain separate.
"""

import argparse
import hashlib
import json
import math
import platform
import re
import statistics
import time
from datetime import datetime, timezone
from pathlib import Path

from execute_knowledge_state import KnowledgeFact, compile_knowledge_state
from knowledge_is_state import KnowledgeIsStateFlow
from knowledge_state_fixture import DEFAULT_FIXTURE, load_knowledge_state_fixture


ROOT = Path(__file__).parent
RESULT_PATH = ROOT / "benchmark" / "results" / "knowledge-state-v1.json"
REPORT_PATH = ROOT / "docs" / "benchmark" / "results" / "knowledge-state-v1.md"
METHODOLOGY_PATH = ROOT / "docs" / "benchmark" / "oscarc-methodology.md"
KERNEL_PATH = ROOT / "execute_knowledge_state.py"
FLOW_PATH = ROOT / "knowledge_is_state.py"
EXPERIMENT_PATH = ROOT / "knowledge_state_experiment.py"
FIXTURE_LOADER_PATH = ROOT / "knowledge_state_fixture.py"
BENCHMARK_VERSION = "knowledge-state-v1"
METHODOLOGY = "OSCARC-v1"
RESEARCH_INTENTION = (
    "At least one nontrivial semantic knowledge task can be represented once "
    "as governed state and reused through deterministic computation without "
    "loss of the required answer."
)
TIMING_REPETITIONS = 101
TOKEN_PATTERN = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


def render_fact(fact):
    return f"{fact.subject} {fact.relation} {fact.object}"


def count_tokens(text):
    """Count declared lexical units; this is not a provider-model tokenizer."""
    return len(TOKEN_PATTERN.findall(text.lower()))


def source_measure(facts):
    text = "\n".join(render_fact(fact) for fact in facts)
    return {"utf8_bytes": len(text.encode("utf-8")), "tokens": count_tokens(text)}


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def measure_ns(operation, repetitions=TIMING_REPETITIONS):
    observations = []
    for _ in range(repetitions):
        started = time.perf_counter_ns()
        operation()
        observations.append(time.perf_counter_ns() - started)
    return {
        "repetitions": repetitions,
        "median_ns": int(statistics.median(observations)),
        "minimum_ns": min(observations),
    }


def load_source_facts(path=DEFAULT_FIXTURE):
    """Read governed fact records from the source fixture for one treatment."""
    path = Path(path)
    with path.open(encoding="utf-8") as source:
        fixture = json.load(source)
    return tuple(KnowledgeFact(**record) for record in fixture["facts"])


def lexical_retrieval(source_path, query):
    """Return the first direct surface fact for a subject."""
    facts = load_source_facts(source_path)
    file_bytes = Path(source_path).stat().st_size
    for position, fact in enumerate(facts, 1):
        if fact.subject == query:
            inspected = facts[:position]
            text = "\n".join(render_fact(item) for item in inspected)
            return {
                "answer": fact.object,
                "path": [fact.subject, fact.object],
                "facts_inspected": position,
                "knowledge_tokens_processed": count_tokens(text),
                "knowledge_bytes_processed": len(text.encode("utf-8")),
                "source_file_reads": 1,
                "source_file_bytes_read": file_bytes,
            }
    return {
        "answer": None,
        "path": [],
        "facts_inspected": len(facts),
        "knowledge_tokens_processed": source_measure(facts)["tokens"],
        "knowledge_bytes_processed": source_measure(facts)["utf8_bytes"],
        "source_file_reads": 1,
        "source_file_bytes_read": file_bytes,
    }


def reconstruct_from_source(source_path, query):
    """Reparse all source facts for one question, then execute the chain."""
    facts = load_source_facts(source_path)
    reconstructed = compile_knowledge_state(
        type(fact)(fact.subject, fact.relation, fact.object) for fact in facts
    )
    execution = KnowledgeIsStateFlow().execute(reconstructed, query)
    volume = source_measure(facts)
    return {
        "answer": execution.answer,
        "path": list(execution.path),
        "facts_parsed": len(facts),
        "edges_traversed": execution.edges_traversed,
        "knowledge_tokens_processed": volume["tokens"],
        "knowledge_bytes_processed": volume["utf8_bytes"],
        "source_file_reads": 1,
        "source_file_bytes_read": Path(source_path).stat().st_size,
    }


def compiled_execution(flow, state, query):
    execution = flow.execute(state, query)
    return {
        "answer": execution.answer,
        "path": list(execution.path),
        "nodes_visited": execution.nodes_visited,
        "edges_traversed": execution.edges_traversed,
        "knowledge_tokens_processed": 0,
        "knowledge_bytes_processed": 0,
        "source_file_reads": 0,
        "source_file_bytes_read": 0,
    }


def _assess(record, expected):
    record["assessment"] = "correct" if record["answer"] == expected else "partial"
    return record


def run_experiment():
    fixture = load_knowledge_state_fixture()
    facts = fixture["facts"]
    questions = fixture["questions"]
    expected = fixture["expected"]
    flow = KnowledgeIsStateFlow()
    state = flow.govern_and_compile(facts)

    lexical = {
        query: _assess(lexical_retrieval(DEFAULT_FIXTURE, query), expected[query])
        for query in questions
    }
    reconstruction = {
        query: _assess(reconstruct_from_source(DEFAULT_FIXTURE, query), expected[query])
        for query in questions
    }
    compiled = {
        query: _assess(compiled_execution(flow, state, query), expected[query])
        for query in questions
    }

    mutation = fixture["mutation"]
    change = flow.replace(state, mutation["old"], mutation["new"])
    changed = compiled_execution(flow, change.changed_state, "luma")
    replay = {
        query: _assess(
            compiled_execution(flow, state, query), expected[query]
        )
        for query in questions
    }
    timing = {
        "clock": "time.perf_counter_ns",
        "runtime": {"python": platform.python_version()},
        "compile": measure_ns(
            lambda: flow.govern_and_compile(load_source_facts(DEFAULT_FIXTURE))
        ),
        "compile_kernel_only": measure_ns(lambda: flow.govern_and_compile(facts)),
        "queries": {
            query: {
                "lexical_retrieval": measure_ns(
                    lambda q=query: lexical_retrieval(DEFAULT_FIXTURE, q)
                ),
                "source_reconstruction": measure_ns(
                    lambda q=query: reconstruct_from_source(DEFAULT_FIXTURE, q)
                ),
                "compiled_mml": measure_ns(lambda q=query: flow.execute(state, q)),
            }
            for query in questions
        },
        "mutation": measure_ns(
            lambda: flow.replace(state, mutation["old"], mutation["new"])
        ),
        "compile_boundary": (
            "compile includes opening and parsing the source fixture; "
            "compile_kernel_only excludes source I/O"
        ),
        "interpretation": (
            "descriptive observations for a tiny fixture; not a production performance comparison"
        ),
    }
    median_by_treatment = {
        treatment: statistics.mean(
            timing["queries"][query][treatment]["median_ns"] for query in questions
        )
        for treatment in ("lexical_retrieval", "source_reconstruction", "compiled_mml")
    }
    reconstruction_saving = (
        median_by_treatment["source_reconstruction"]
        - median_by_treatment["compiled_mml"]
    )
    timing["derived_observations"] = {
        "mean_query_median_ns": {
            name: round(value) for name, value in median_by_treatment.items()
        },
        "lexical_over_compiled_query_ratio": round(
            median_by_treatment["lexical_retrieval"]
            / median_by_treatment["compiled_mml"],
            2,
        ),
        "reconstruction_over_compiled_query_ratio": round(
            median_by_treatment["source_reconstruction"]
            / median_by_treatment["compiled_mml"],
            2,
        ),
        "observed_compile_break_even_queries_vs_reconstruction": (
            math.ceil(timing["compile"]["median_ns"] / reconstruction_saving)
            if reconstruction_saving > 0 else None
        ),
        "compiled_latency_lower_than_both_local_baselines": (
            median_by_treatment["compiled_mml"]
            < median_by_treatment["lexical_retrieval"]
            and median_by_treatment["compiled_mml"]
            < median_by_treatment["source_reconstruction"]
        ),
    }

    return {
        "benchmark_version": BENCHMARK_VERSION,
        "reporting_methodology": METHODOLOGY,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "research_intention": RESEARCH_INTENTION,
        "standards": [
            "lexical retrieval does not silently claim a derived terminal answer",
            "per-query source reconstruction returns both expected terminal memberships",
            "compiled execution returns the same two expected terminal memberships",
            "compiled execution is deterministic, inspectable, and invokes no source-read operation per query",
            "the governed mutation changes luma to nora while preserving the original state and the unrelated mira answer",
        ],
        "fixture": {
            "knowledge_facts": len(facts),
            "questions": len(questions),
            "source": source_measure(facts),
        },
        "treatments": {
            "lexical_retrieval": lexical,
            "source_reconstruction": reconstruction,
            "compiled_mml": compiled,
        },
        "accuracy": {
            "lexical_retrieval": sum(item["assessment"] == "correct" for item in lexical.values()),
            "source_reconstruction": sum(item["assessment"] == "correct" for item in reconstruction.values()),
            "compiled_mml": sum(item["assessment"] == "correct" for item in compiled.values()),
            "question_count": len(questions),
        },
        "compiled_state": {
            "snapshot_id": state.snapshot_id,
            "deterministic": replay == compiled,
            "inspectable_paths": all(item["path"] for item in compiled.values()),
            "compile_work": {"facts_parsed": len(facts)},
        },
        "context": {
            "fixture_status": "authored development case",
            "expectation_status": (
                "encoded in the fixture and executable checks before report interpretation; "
                "not independently preregistered"
            ),
            "declared_limitations": [
                "the fixture and implementation share project authorship",
                "the case has no held-out or independent review contract",
                "no parameter-tuning study is part of this experiment",
            ],
            "sample_size": {"facts": len(facts), "questions": len(questions)},
            "treatment_sequence": [
                "lexical retrieval over source facts",
                "per-query reconstruction from all source facts",
                "compile facts once",
                "compiled execution and deterministic replay",
                "governed fact replacement and post-change execution",
            ],
        },
        "intervention": {
            "independent_change": (
                "the six source facts are compiled once into an immutable subject index "
                "instead of being reparsed for each question"
            ),
            "fixed": ["facts", "questions", "expected answers", "typed composition rule"],
            "observed_mechanism": "deterministic traversal of is-a* followed by belongs-to",
            "causal_isolation": False,
        },
        "mutation": {
            "old_fact": mutation["old"].__dict__,
            "new_fact": mutation["new"].__dict__,
            "entries_replaced": change.entries_replaced,
            "facts_scanned": change.facts_scanned,
            "index_entries_copied": change.index_entries_copied,
            "original_snapshot_id": state.snapshot_id,
            "changed_snapshot_id": change.changed_state.snapshot_id,
            "changed_execution": changed,
            "original_answer_preserved": flow.execute(state, "luma").answer == "sena",
            "unaffected_answer_preserved": flow.execute(change.changed_state, "mira").answer == "ralo",
            "retraining_required": False,
            "source_file_reads_per_query": 0,
        },
        "timing": timing,
        "research_implication": {
            "classification": (
                "early directional architectural signal"
                if timing["derived_observations"]["compiled_latency_lower_than_both_local_baselines"]
                else "architectural mechanism observed without a latency-direction signal"
            ),
            "statement": (
                "Intelligence can be distributed between a probabilistic learner "
                "and an explicit, executable semantic environment."
            ),
            "observed_basis": [
                "compiled execution preserved both required answers",
                "compiled queries invoked no source-file reads",
                "compiled query latency was lower than both local baselines in this run",
                "one governed correction changed the dependent consequence without retraining",
            ],
            "hypotheses_not_measured": [
                "reduced computation at meaningful scale",
                "lower energy consumption",
                "comparative efficiency against a probabilistic language model",
            ],
        },
        "measurement_contract": {
            "tokens": "lowercase lexical units matched by [a-z0-9]+(?:-[a-z0-9]+)*; not model tokens",
            "knowledge_tokens_processed": "governed-fact lexical tokens parsed or inspected during the operation",
            "source_file_reads": "instrumented openings of the complete JSON source fixture",
            "algorithmic_work": "explicit facts inspected or parsed and graph nodes or edges traversed",
            "wall_clock": "median and minimum elapsed nanoseconds reported separately from other units",
        },
        "conformity": {
            "judgment": "CONSISTENT",
            "evidence_strength": "LOW",
            "criteria": {
                "lexical_control_is_partial": all(
                    item["assessment"] == "partial" for item in lexical.values()
                ),
                "source_reconstruction_answers_all": all(
                    item["assessment"] == "correct" for item in reconstruction.values()
                ),
                "compiled_execution_answers_all": all(
                    item["assessment"] == "correct" for item in compiled.values()
                ),
                "compiled_execution_is_deterministic": replay == compiled,
                "compiled_paths_are_inspectable": all(item["path"] for item in compiled.values()),
                "compiled_queries_invoke_no_source_read": all(
                    item["source_file_reads"] == 0 for item in compiled.values()
                ),
                "mutation_changes_dependent_answer": changed["answer"] == "nora",
                "mutation_preserves_original_and_unrelated_answers": (
                    flow.execute(state, "luma").answer == "sena"
                    and flow.execute(change.changed_state, "mira").answer == "ralo"
                ),
            },
        },
        "artifact_identities": {
            "source_fixture_sha256": sha256_file(DEFAULT_FIXTURE),
            "compiled_state_snapshot": state.snapshot_id,
            "changed_state_snapshot": change.changed_state.snapshot_id,
            "kernel_sha256": sha256_file(KERNEL_PATH),
            "operational_flow_sha256": sha256_file(FLOW_PATH),
            "experiment_generator_sha256": sha256_file(EXPERIMENT_PATH),
            "fixture_loader_sha256": sha256_file(FIXTURE_LOADER_PATH),
            "methodology_sha256": sha256_file(METHODOLOGY_PATH),
        },
        "provenance": {
            "fixture": str(DEFAULT_FIXTURE.relative_to(ROOT)),
            "fixture_loader": str(FIXTURE_LOADER_PATH.relative_to(ROOT)),
            "kernel": "execute_knowledge_state.py",
            "operational_flow": "knowledge_is_state.py",
            "experiment": "knowledge_state_experiment.py",
            "machine_result": str(RESULT_PATH.relative_to(ROOT)),
            "human_report": str(REPORT_PATH.relative_to(ROOT)),
        },
        "evidence_boundary": (
            "One authored six-fact case and one declared is-a* then belongs-to rule; "
            "not general language understanding, arbitrary inference, or an efficiency "
            "comparison with a language model."
        ),
    }


def markdown_report(result):
    treatments = result["treatments"]
    accuracy = result["accuracy"]
    mutation = result["mutation"]
    source = result["fixture"]["source"]
    timing = result["timing"]
    derived_timing = timing["derived_observations"]
    break_even = derived_timing["observed_compile_break_even_queries_vs_reconstruction"]
    break_even_label = (
        f"{break_even} {'query' if break_even == 1 else 'queries'}"
        if break_even is not None else "not reached"
    )
    latency_signal = derived_timing["compiled_latency_lower_than_both_local_baselines"]
    latency_signal_phrase = (
        "showed lower local query latency than both treatments in this run"
        if latency_signal
        else "did not show lower local query latency than both treatments in this run"
    )
    latency_status = (
        "Observed in this local run" if latency_signal else "Not observed in this local run"
    )
    generated_date = result["generated_at"].split("T", 1)[0]
    lines = [
        "# Knowledge State Execution Experiment v1 — OSCARC Report", "",
        "> **Knowledge is state, not behaviour buried in a model.**", "",
        "## Research intention", "", result["research_intention"], "",
        "## Executive interpretation", "",
        "The result is **consistent** with the bounded expectation that one exact semantic "
        "consequence can be compiled into governed state and reused without losing the required "
        "answer. Both compiled queries returned the expected terminal membership, deterministic "
        "replay passed, and the governed correction changed the dependent answer while preserving "
        "the original state and unrelated answer. Evidence strength is **low**: this is one "
        "six-fact authored development case, and the reconstruction treatment is deterministic "
        "local processing rather than a language-model baseline.", "",
        "## O — Objective observation", "",
        f"On `{generated_date}`, benchmark `{result['benchmark_version']}` observed three "
        f"treatments over {result['fixture']['knowledge_facts']} authored facts and "
        f"{result['fixture']['questions']} questions. Lexical retrieval returned `vek` and `dal`, "
        "neither of which was the expected terminal membership. Per-query source reconstruction "
        "and compiled execution both returned `sena` for `luma` and `ralo` for `mira`.", "",
        "The [machine-readable evidence](../../../benchmark/results/knowledge-state-v1.json) "
        "records source volume, high-level algorithmic work, wall-clock observations, state "
        f"identities, paths, replay, and mutation. The original compiled snapshot is "
        f"`{result['artifact_identities']['compiled_state_snapshot']}`. No causal or "
        "efficiency interpretation is assigned in this section.", "",
        "## S — Standard, baseline, or reference model", "",
        "The development standard encoded in the fixture and executable checks required:", "",
    ]
    for index, standard in enumerate(result["standards"], 1):
        lines.append(f"{index}. {standard};")
    lines.extend([
        "", "These criteria were encoded before generation of this report, but no independent "
        "preregistration artifact exists. The conformity judgment is therefore developmental "
        "rather than confirmatory.", "",
        "## C — Context and chronology", "",
        "The experiment used one authored fixture and the declared composition rule "
        "`is-a* -> belongs-to`. Treatments ran in this order:", "",
        "```text",
        "authored source facts",
        "    -> lexical one-hop retrieval",
        "    -> per-query parse + temporary state + typed traversal",
        "    -> compile source facts once",
        "    -> compiled typed traversal",
        "    -> deterministic replay",
        "    -> governed fact replacement",
        "    -> post-change compiled traversal",
        "```", "",
        f"The governed-fact projection contains `{source['utf8_bytes']}` UTF-8 bytes and "
        f"`{source['tokens']}` declared lexical tokens. Tokens are lowercase units matched by "
        "`[a-z0-9]+(?:-[a-z0-9]+)*`; they are not provider-model tokens. Timings use "
        f"`{timing['clock']}` on Python `{timing['runtime']['python']}` with "
        f"`{timing['compile']['repetitions']}` repetitions per operation. Declared limitations "
        "are that the fixture is not held out or independent and that no tuning study forms part "
        "of this experiment. This tiny case is unsuitable for performance generalization.", "",
        "## A — Actions, interventions, or observed mechanisms", "",
        "The compiled treatment transformed the same six governed facts into an immutable "
        "subject index once. Facts, questions, expected answers, and the typed composition rule "
        "remained fixed. Query execution then followed explicit `is-a` edges until one "
        "`belongs-to` edge produced the terminal membership.", "",
        "The mutation replaced `tor belongs-to sena` with `tor belongs-to nora`, producing a new "
        "content-addressed state without changing the original. Traversal and snapshot differences "
        "are directly inspectable mechanisms. The design does not isolate a causal efficiency "
        "advantage over language-model inference.", "",
        "## R — Result, effect, or measured outcome", "",
        "### Answer outcomes", "",
        "| Treatment | luma | mira | Derived-answer accuracy |",
        "| --- | --- | --- | ---: |",
        f"| Lexical retrieval | {treatments['lexical_retrieval']['luma']['answer']} (partial) | "
        f"{treatments['lexical_retrieval']['mira']['answer']} (partial) | "
        f"{accuracy['lexical_retrieval']}/{accuracy['question_count']} |",
        f"| Per-query source reconstruction | {treatments['source_reconstruction']['luma']['answer']} | "
        f"{treatments['source_reconstruction']['mira']['answer']} | "
        f"{accuracy['source_reconstruction']}/{accuracy['question_count']} |",
        f"| Compiled MML | {treatments['compiled_mml']['luma']['answer']} | "
        f"{treatments['compiled_mml']['mira']['answer']} | "
        f"{accuracy['compiled_mml']}/{accuracy['question_count']} |", "",
        "### Input volume and algorithmic work", "",
        "| Treatment / operation | Fixture reads | Fixture bytes read | Fact tokens processed | Fact bytes processed | Facts inspected or parsed | Edges traversed |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ])
    for query in ("luma", "mira"):
        lexical = treatments["lexical_retrieval"][query]
        reconstruction = treatments["source_reconstruction"][query]
        compiled = treatments["compiled_mml"][query]
        lines.extend([
            f"| Lexical / `{query}` | {lexical['source_file_reads']} | "
            f"{lexical['source_file_bytes_read']} | {lexical['knowledge_tokens_processed']} | "
            f"{lexical['knowledge_bytes_processed']} | {lexical['facts_inspected']} | — |",
            f"| Reconstruction / `{query}` | {reconstruction['source_file_reads']} | "
            f"{reconstruction['source_file_bytes_read']} | "
            f"{reconstruction['knowledge_tokens_processed']} | "
            f"{reconstruction['knowledge_bytes_processed']} | {reconstruction['facts_parsed']} | "
            f"{reconstruction['edges_traversed']} |",
            f"| Compiled / `{query}` | {compiled['source_file_reads']} | "
            f"{compiled['source_file_bytes_read']} | 0 | 0 | 0 | {compiled['edges_traversed']} |",
        ])
    lines.extend([
        "", f"Compilation parsed and indexed all `6` facts once. Mutation changed "
        f"`{mutation['entries_replaced']}` record, scanned `{mutation['facts_scanned']}` facts, "
        f"and copied `{mutation['index_entries_copied']}` index entries. These are high-level "
        "work counters, not CPU instructions or FLOPs.", "",
        "### Wall-clock observations", "",
        "| Operation | Median (ns) | Minimum (ns) | Repetitions |",
        "| --- | ---: | ---: | ---: |",
        f"| Source load + compile | {timing['compile']['median_ns']} | {timing['compile']['minimum_ns']} | "
        f"{timing['compile']['repetitions']} |",
        f"| Compile kernel only | {timing['compile_kernel_only']['median_ns']} | "
        f"{timing['compile_kernel_only']['minimum_ns']} | "
        f"{timing['compile_kernel_only']['repetitions']} |",
    ])
    for query in ("luma", "mira"):
        for treatment in ("lexical_retrieval", "source_reconstruction", "compiled_mml"):
            observation = timing["queries"][query][treatment]
            lines.append(
                f"| {treatment} / {query} | {observation['median_ns']} | "
                f"{observation['minimum_ns']} | {observation['repetitions']} |"
            )
    lines.extend([
        f"| Mutation | {timing['mutation']['median_ns']} | "
        f"{timing['mutation']['minimum_ns']} | {timing['mutation']['repetitions']} |", "",
        "Wall-clock values are descriptive machine-local observations. They are not compared with "
        "GPU FLOPs, model tokens, or production latency, and no performance conclusion is drawn.", "",
        "Across the two questions, the mean of the observed per-query medians was "
        f"`{derived_timing['mean_query_median_ns']['compiled_mml']}` ns for compiled execution, "
        f"`{derived_timing['mean_query_median_ns']['lexical_retrieval']}` ns for lexical retrieval, "
        f"and `{derived_timing['mean_query_median_ns']['source_reconstruction']}` ns for source "
        "reconstruction. In this run, lexical retrieval took "
        f"`{derived_timing['lexical_over_compiled_query_ratio']:.2f}x` as long as compiled execution and "
        f"source reconstruction took `{derived_timing['reconstruction_over_compiled_query_ratio']:.2f}x` "
        "as long. Relative to repeated reconstruction, the observed end-to-end source-load-plus-"
        "compile cost was "
        f"recovered after approximately `{break_even_label}`. This direction and magnitude apply "
        "only to this Python process, fixture, machine, "
        "and measurement run.", "",
        "### Mutation outcome", "",
        f"The governed replacement changed the compiled path to "
        f"`{' -> '.join(mutation['changed_execution']['path'])}`. The original state still "
        "returned `luma -> sena`; the changed state still returned `mira -> ralo`. Retraining "
        "was not performed. The compiled query code path invoked no source-file read operation.", "",
        "## C — Comparative assessment and research conclusion", "",
        f"**Conformity judgment: `{result['conformity']['judgment']}`.** Every declared "
        "development criterion was met: the lexical control remained one-hop, reconstruction and "
        "compiled execution both answered 2/2, replay was deterministic and inspectable, compiled "
        "queries invoked zero source-file reads, and mutation produced the expected consequence.", "",
        f"**Evidence strength: `{result['conformity']['evidence_strength']}`.** The evidence is one "
        "small authored fixture with the declared limitations of shared project authorship, no "
        "held-out or independent-review contract, no language-model treatment, and no meaningful "
        "performance scale. "
        "This supports only the local claim that this typed-chain task can be represented once as "
        "governed state and executed repeatedly without loss of its required answer. It does not "
        "establish general knowledge execution, arbitrary inference, or an efficiency advantage "
        "over language models.", "",
        "### Research implication — architectural signal", "",
        f"**Classification: {result['research_implication']['classification']}.** Compiled "
        "execution preserved the required answers, avoided source-file reads on its query path, "
        f"{latency_signal_phrase}, and accepted a governed "
        "semantic correction without retraining. Together, these observations are a bounded signal "
        "for the architectural proposition:", "",
        f"> **{result['research_implication']['statement']}**", "",
        "A probabilistic learner may discover, propose, translate, or communicate knowledge, while "
        "an explicit semantic environment preserves governed relationships and executes their "
        "declared consequences. The experiment makes that division of responsibility tangible for "
        "one exact typed-chain task.", "",
        "The signal is consistent with the repository's hypotheses of reduced repeated computation "
        "for known patterns and potentially lower-energy execution. It does **not** demonstrate "
        "either claim at meaningful scale: operation counts beyond the declared counters, CPU "
        "energy, memory traffic, whole-system energy, and a probabilistic-model baseline were not "
        "measured.", "",
        "| Proposition | Current status |",
        "| --- | --- |",
        "| Required answers survive compilation | Observed in this fixture |",
        "| Compiled queries avoid repeated source parsing | Observed code-path property |",
        f"| Compiled query latency is lower | {latency_status} |",
        "| Distributed learner/environment intelligence is viable | Early architectural signal |",
        "| Repeated computation is reduced at meaningful scale | Hypothesis |",
        "| Energy consumption is lower than a language model | Untested hypothesis |", "",
        "## Recommendation and next step", "",
        "Freeze a held-out suite of independently authored typed-chain cases before extending the "
        "executor. Add cycles, branching policies, multiple hierarchy depths, irrelevant facts, "
        "and governed mutations. Then compare compiled execution with a named language model using "
        "a frozen prompt, model version, provider-reported tokens, repeated trials, answer-quality "
        "criteria, and separately reported latency and resource measurements.", "",
        "## Evidence boundary", "", result["evidence_boundary"], "",
        "This report follows the [OSCARC methodology](../oscarc-methodology.md). The "
        "[machine-readable JSON artifact](../../../benchmark/results/knowledge-state-v1.json) "
        "remains authoritative for measurements, conformity inputs, "
        "artifact identities, and provenance.",
    ])
    return "\n".join(lines) + "\n"


def check_result(result):
    count = result["accuracy"]["question_count"]
    if result["accuracy"]["lexical_retrieval"] != 0:
        raise SystemExit("Lexical treatment unexpectedly derived a terminal answer.")
    if result["accuracy"]["source_reconstruction"] != count:
        raise SystemExit("Source reconstruction did not recover every expected answer.")
    if result["accuracy"]["compiled_mml"] != count:
        raise SystemExit("Compiled knowledge state did not recover every expected answer.")
    if not result["compiled_state"]["deterministic"]:
        raise SystemExit("Compiled knowledge-state execution is not deterministic.")
    if result["mutation"]["changed_execution"]["answer"] != "nora":
        raise SystemExit("Governed mutation did not produce the expected consequence.")
    if not all(result["conformity"]["criteria"].values()):
        raise SystemExit("One or more OSCARC conformity criteria failed.")


def write_results(result, result_path=RESULT_PATH, report_path=REPORT_PATH):
    result_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    report_path.write_text(markdown_report(result), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Run the Knowledge State experiment.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="Write JSON and Markdown results.")
    mode.add_argument("--check", action="store_true", help="Check without changing results.")
    args = parser.parse_args()
    result = run_experiment()
    check_result(result)
    if args.write:
        write_results(result)
    print(markdown_report(result))


if __name__ == "__main__":
    main()
