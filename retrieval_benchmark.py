"""Legacy application-level retrieval diagnostic for MML.

This is deliberately not the definition of MML success. It checks that the
current executable representation remains deterministic, useful on two small
authored tasks, and visible beside simple lexical baselines.
"""

import argparse
import json
import math
import subprocess
import tempfile
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

from elaborations.mml_graph import GraphModel, load_aliases, load_relations, tokenize
from src.helpers.artifacts import write_artifact_pair
from src.helpers.hashing import sha256_file
from src.helpers.json_io import read_json
from src.helpers.provenance import runtime_identity, utc_now_iso


ROOT = Path(__file__).parent
BENCHMARK_DIR = ROOT / "benchmark" / "v1"
RESULTS_DIR = ROOT / "benchmark" / "results"
REPORTS_DIR = ROOT / "docs" / "benchmark" / "results"
RUBRIC_PATH = ROOT / "docs" / "benchmark" / "v1" / "rubric.md"
CONSTRUCTION_PATHS = {
    "polysemy": ROOT / "data" / "construction" / "polysemy_corpus.txt",
    "gdpr": ROOT / "data" / "construction" / "gdpr_law_corpus.txt",
}
RELATIONS_PATH = ROOT / "data" / "construction" / "gdpr_relations.jsonl"
ALIASES_PATH = ROOT / "data" / "construction" / "gdpr_aliases.jsonl"
UPDATE_PATH = ROOT / "benchmark" / "updates" / "v1-local-relation.json"
SYSTEMS = (
    "lexical_overlap",
    "tfidf_cosine",
    "mml_cooccurrence",
    "mml_typed",
    "mml_lexical_hybrid",
)
MML_SYSTEMS = ("mml_cooccurrence", "mml_typed")
QUALITY_FLOORS = {"mrr": 0.25, "ndcg_at_10": 0.35}
REGRESSION_TOLERANCE = 0.01


class BenchmarkIntegrityError(ValueError):
    pass


def load_sentences(path):
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def load_json(path):
    return read_json(path)


def load_documents(path):
    documents = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            documents.append(json.loads(line))
        except json.JSONDecodeError as error:
            raise BenchmarkIntegrityError(f"Invalid JSON on documents line {line_number}: {error}") from error
    return documents


def source_revision():
    try:
        revision = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True,
            capture_output=True, text=True,
        ).stdout.strip()
        dirty = subprocess.run(
            ["git", "status", "--porcelain"], cwd=ROOT, check=True,
            capture_output=True, text=True,
        ).stdout.strip()
        return f"{revision}-dirty" if dirty else revision
    except subprocess.CalledProcessError:
        return "uncommitted-pre-publication-dirty"


def build_models(relation_scale=1.0):
    polysemy = load_sentences(CONSTRUCTION_PATHS["polysemy"])
    gdpr = load_sentences(CONSTRUCTION_PATHS["gdpr"])
    relations = [dict(item, weight=item["weight"] * relation_scale) for item in load_relations(RELATIONS_PATH)]
    return {
        "polysemy_cooccurrence": GraphModel.from_sources(polysemy),
        "polysemy_typed": GraphModel.from_sources(polysemy),
        "gdpr_cooccurrence": GraphModel.from_sources(gdpr),
        "gdpr_typed": GraphModel.from_sources(gdpr, relations=relations, aliases=load_aliases(ALIASES_PATH)),
    }


MODELS = build_models()


def validate_benchmark(benchmark_dir=BENCHMARK_DIR):
    paths = {
        "polysemy_corpus": CONSTRUCTION_PATHS["polysemy"],
        "gdpr_law_corpus": CONSTRUCTION_PATHS["gdpr"],
        "gdpr_relations": RELATIONS_PATH,
        "gdpr_aliases": ALIASES_PATH,
        "documents": benchmark_dir / "documents.jsonl",
        "queries": benchmark_dir / "queries.json",
        "judgments": benchmark_dir / "judgments.json",
        "rubric": RUBRIC_PATH,
    }
    manifest = load_json(benchmark_dir / "manifest.json")
    for name, path in paths.items():
        if manifest["sha256"].get(name) != sha256_file(path, prefixed=False):
            raise BenchmarkIntegrityError(f"Hash mismatch for {name}")

    documents = load_documents(paths["documents"])
    queries = load_json(paths["queries"])
    judgments = load_json(paths["judgments"])["judgments"]
    if len(documents) != 50 or len(queries) != 6:
        raise BenchmarkIntegrityError("Version 1 requires 50 documents and 6 queries.")
    if len({item["id"] for item in documents}) != len(documents):
        raise BenchmarkIntegrityError("Duplicate document ids.")
    if len({item["id"] for item in queries}) != len(queries):
        raise BenchmarkIntegrityError("Duplicate query ids.")
    if set(judgments) != {item["id"] for item in queries}:
        raise BenchmarkIntegrityError("Judgment query ids do not match queries.")

    lines = load_sentences(CONSTRUCTION_PATHS["polysemy"])
    river = sum("bank_river" in tokenize(line) for line in lines)
    financial = sum("bank_financial" in tokenize(line) for line in lines)
    if (river, financial) != (10, 10):
        raise BenchmarkIntegrityError("Polysemy construction must remain balanced at 10/10.")

    return {"documents": documents, "queries": queries, "judgments": judgments, "manifest": manifest}


def lexical_score(query_terms, text):
    query = set(tokenize(" ".join(query_terms)))
    document = set(tokenize(text))
    return len(query & document) / len(query) if query else 0.0


def tfidf_scores(query_terms, documents):
    tokenized = [tokenize(item["text"]) for item in documents]
    vocabulary = sorted({word for words in tokenized for word in words} | set(query_terms))
    index = {word: position for position, word in enumerate(vocabulary)}
    frequency = Counter(word for words in tokenized for word in set(words))
    idf = np.array([math.log((1 + len(documents)) / (1 + frequency[word])) + 1 for word in vocabulary])

    def vector(words):
        values = np.zeros(len(vocabulary))
        for word, count in Counter(words).items():
            if word in index:
                values[index[word]] = count * idf[index[word]]
        norm = np.linalg.norm(values)
        return values / norm if norm else values

    query = vector(query_terms)
    return [float(query @ vector(words)) for words in tokenized]


def mml_score(query, text, typed=True):
    suffix = "typed" if typed else "cooccurrence"
    model = MODELS[f"{query['tier']}_{suffix}"]
    # Both MML variants execute the same governed query concepts; only their
    # graph construction differs, keeping the comparison attributable.
    terms = query["terms"] + query.get("mml_concepts", [])
    return model.score(terms, text, query.get("negative_terms"))


def rank_inputs(documents, queries):
    rankings = {system: {} for system in SYSTEMS}
    for query in queries:
        candidates = [item for item in documents if item["tier"] == query["tier"]]
        tfidf = tfidf_scores(query["terms"], candidates)
        scored = {system: [] for system in SYSTEMS}
        for document, tfidf_value in zip(candidates, tfidf):
            values = {
                "lexical_overlap": lexical_score(query["terms"], document["text"]),
                "tfidf_cosine": tfidf_value,
                "mml_cooccurrence": mml_score(query, document["text"], typed=False),
                "mml_typed": mml_score(query, document["text"], typed=True),
            }
            # One deliberately simple hybrid makes the complementary lexical
            # and semantic signals reproducible without a calibration search.
            values["mml_lexical_hybrid"] = values["mml_typed"] * (
                0.2 + 0.8 * values["lexical_overlap"]
            )
            for system, score in values.items():
                scored[system].append({"document_id": document["id"], "score": score})
        for system in SYSTEMS:
            rankings[system][query["id"]] = sorted(
                scored[system], key=lambda item: (-item["score"], item["document_id"])
            )
    return rankings


def relevance_map(query_id, judgments, document_ids):
    positives = judgments[query_id]
    return {item: positives.get(item, {}).get("relevance", 0) for item in document_ids}


def precision_at_k(ranked, relevance, k):
    return sum(relevance[item] >= 1 for item in ranked[:k]) / k


def recall_at_k(ranked, relevance, k):
    total = sum(value >= 1 for value in relevance.values())
    return sum(relevance[item] >= 1 for item in ranked[:k]) / total


def reciprocal_rank(ranked, relevance):
    return next((1 / rank for rank, item in enumerate(ranked, 1) if relevance[item] >= 1), 0.0)


def ndcg_at_k(ranked, relevance, k):
    gains = [relevance[item] for item in ranked[:k]]
    dcg = sum((2 ** gain - 1) / math.log2(position + 2) for position, gain in enumerate(gains))
    ideal = sorted(relevance.values(), reverse=True)[:k]
    best = sum((2 ** gain - 1) / math.log2(position + 2) for position, gain in enumerate(ideal))
    return dcg / best if best else 0.0


def evaluate_rankings(rankings, documents, queries, judgments):
    ids = {item["id"] for item in documents}
    per_query = {system: {} for system in SYSTEMS}
    tier_values = {system: defaultdict(list) for system in SYSTEMS}
    for system in SYSTEMS:
        for query in queries:
            ranked = [item["document_id"] for item in rankings[system][query["id"]]]
            relevance = relevance_map(query["id"], judgments, ids)
            metrics = {
                "precision_at_5": precision_at_k(ranked, relevance, 5),
                "recall_at_10": recall_at_k(ranked, relevance, 10),
                "mrr": reciprocal_rank(ranked, relevance),
                "ndcg_at_10": ndcg_at_k(ranked, relevance, 10),
            }
            per_query[system][query["id"]] = metrics
            tier_values[system][query["tier"]].append(metrics)
    macro = {system: {} for system in SYSTEMS}
    for system in SYSTEMS:
        for tier, values in tier_values[system].items():
            macro[system][tier] = {
                metric: sum(item[metric] for item in values) / len(values)
                for metric in values[0]
            }
    return per_query, macro


def diagnostic_checks(macro, reference=None):
    failures = []
    for system in MML_SYSTEMS:
        for tier in ("polysemy", "gdpr"):
            for metric, floor in QUALITY_FLOORS.items():
                value = macro[system][tier][metric]
                if value < floor:
                    failures.append(f"{system}/{tier}/{metric} below {floor:.2f}")
    regressions = []
    if reference:
        old = reference["metrics"]["macro"]
        for system in MML_SYSTEMS:
            if system not in old:
                continue
            for tier in ("polysemy", "gdpr"):
                for metric, value in old[system][tier].items():
                    if value - macro[system][tier][metric] > REGRESSION_TOLERANCE:
                        regressions.append(f"{system}/{tier}/{metric}")
    return {"quality_floor": not failures, "regression": not regressions,
            "quality_failures": failures, "regressions": regressions}


def run_benchmark(reference=None):
    validated = validate_benchmark()
    first = rank_inputs(validated["documents"], validated["queries"])
    if first != rank_inputs(validated["documents"], validated["queries"]):
        raise BenchmarkIntegrityError("Rankings are not deterministic.")
    per_query, macro = evaluate_rankings(
        first, validated["documents"], validated["queries"], validated["judgments"]
    )
    return {
        "benchmark_version": validated["manifest"]["benchmark_version"],
        "purpose": "small deterministic retrieval diagnostic; not an MML acceptance test",
        "generated_at": utc_now_iso(),
        "source_revision": source_revision(),
        "runtime": runtime_identity({"numpy": np.__version__}),
        "configuration": {"systems": list(SYSTEMS), "quality_floors": QUALITY_FLOORS,
                          "regression_tolerance": REGRESSION_TOLERANCE},
        "snapshots": {name: model.snapshot_id for name, model in MODELS.items()},
        "metrics": {"per_query": per_query, "macro": macro},
        "checks": diagnostic_checks(macro, reference),
    }


def markdown_report(result):
    lines = [
        "# MML Retrieval Diagnostic v1", "",
        f"Generated: `{result['generated_at']}`  ",
        f"Source revision: `{result['source_revision']}`", "",
        "> This is a small development diagnostic, not an acceptance verdict for MML and not held-out evidence.", "",
        "## Checks", "",
        f"- Deterministic integrity: `PASS`",
        f"- Absolute MML quality floors: `{'PASS' if result['checks']['quality_floor'] else 'FAIL'}`",
        f"- Reference regression protection: `{'PASS' if result['checks']['regression'] else 'FAIL'}`", "",
        "## Retrieval metrics", "",
    ]
    for tier in ("polysemy", "gdpr"):
        lines.extend([f"### {tier.title()}", "", "| System | P@5 | R@10 | MRR | nDCG@10 |",
                      "| --- | ---: | ---: | ---: | ---: |"])
        for system in SYSTEMS:
            values = result["metrics"]["macro"][system][tier]
            lines.append(
                f"| {system} | {values['precision_at_5']:.4f} | {values['recall_at_10']:.4f} | "
                f"{values['mrr']:.4f} | {values['ndcg_at_10']:.4f} |"
            )
        lines.append("")
    lines.extend([
        "## Interpretation", "",
        "TF-IDF and MML are deterministic here but execute different representations. These numbers show retrieval behavior on one small synthetic development fixture. They do not determine whether executable semantic infrastructure is successful.", "",
        "The named multiplicative hybrid is computed directly as `mml_typed × (0.2 + 0.8 × lexical_overlap)`. It is retained to test the architectural observation that lexical evidence and explicit semantic activation can be complementary; it is not tuned by a calibration search.", "",
        "The earlier challenge slices, hybrid calibration, sensitivity experiments, and threshold verdicts are preserved in [the archived research note](../archive/v1-retrieval-research.md).", "",
    ])
    return "\n".join(lines)


def report_output_dir(output_dir, report_dir):
    if report_dir is not None:
        return report_dir
    return REPORTS_DIR if output_dir == RESULTS_DIR else output_dir


def write_results(result, output_dir=RESULTS_DIR, report_dir=None):
    report_dir = report_output_dir(output_dir, report_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)
    write_artifact_pair(
        output_dir / "v1.json", result, report_dir / "v1.md", markdown_report(result)
    )


def write_checked_results(result, output_dir=RESULTS_DIR, accept_regression=False):
    """Refuse to replace the reference with a known regression by default."""
    if not result["checks"]["regression"] and not accept_regression:
        raise SystemExit(
            "Refusing to replace the benchmark reference after a regression. "
            "Review the result and rerun with --accept-regression only when the new "
            "reference is an intentional, documented change."
        )
    write_results(result, output_dir)


def check_results():
    reference_path = RESULTS_DIR / "v1.json"
    reference = load_json(reference_path) if reference_path.exists() else None
    result = run_benchmark(reference)
    with tempfile.TemporaryDirectory() as directory:
        write_results(result, Path(directory))
    if not result["checks"]["quality_floor"] or not result["checks"]["regression"]:
        raise SystemExit("Retrieval diagnostic checks failed.")
    print(markdown_report(result))


def main():
    parser = argparse.ArgumentParser(description="Run the small MML retrieval diagnostic.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="Regenerate the diagnostic report.")
    mode.add_argument("--check", action="store_true", help="Verify without rewriting results.")
    parser.add_argument(
        "--accept-regression",
        action="store_true",
        help="With --write, explicitly allow a regressed result to become the new reference.",
    )
    args = parser.parse_args()
    if args.accept_regression and not args.write:
        parser.error("--accept-regression is valid only with --write")
    if args.write:
        reference = load_json(RESULTS_DIR / "v1.json") if (RESULTS_DIR / "v1.json").exists() else None
        result = run_benchmark(reference)
        write_checked_results(result, accept_regression=args.accept_regression)
        print(markdown_report(result))
    else:
        check_results()


if __name__ == "__main__":
    main()
