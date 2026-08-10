"""Print one compact representation → execution → evolution MML record."""

import json

import retrieval_benchmark as benchmark
from .mml_graph import stable_sentence_id


QUERY_ID = "QG3"
DOCUMENT_ID = "G14"


def build_trace_record():
    fixture = benchmark.validate_benchmark()
    query = next(item for item in fixture["queries"] if item["id"] == QUERY_ID)
    document = next(item for item in fixture["documents"] if item["id"] == DOCUMENT_ID)
    update = benchmark.load_json(benchmark.UPDATE_PATH)
    before = benchmark.MODELS["gdpr_typed"]
    after = before.with_relation_update(update["relation"])

    query_text = " ".join(query["terms"] + query.get("mml_concepts", []))
    negative_text = " ".join(query.get("negative_terms", []))
    before_explanation = before.score_with_explanation(
        query_text, document["text"], negative_text
    )
    after_explanation = after.score_with_explanation(
        query_text, document["text"], negative_text
    )

    evidence_id = update["relation"]["evidence_ids"][0]
    evidence_text = next(
        sentence for sentence in benchmark.load_sentences(benchmark.CONSTRUCTION_PATHS["gdpr"])
        if stable_sentence_id(sentence) == evidence_id
    )
    rebuilt = benchmark.build_models()["gdpr_typed"]
    rollback_explanation = rebuilt.score_with_explanation(
        query_text, document["text"], negative_text
    )

    return {
        "purpose": "one legible MML representation → execution → evolution trace",
        "limitations": {
            "representative_coverage": False,
            "note": "QG3/G14 is a deliberately selected worked example, not evidence of typical coverage or quality.",
        },
        "input": {
            "query_id": query["id"],
            "query": query["label"],
            "query_terms": query["terms"],
            "governed_concepts": query.get("mml_concepts", []),
            "document_id": document["id"],
            "document": document["text"],
        },
        "representation": {
            "proposed_relation": update["relation"],
            "evidence": {"id": evidence_id, "text": evidence_text},
        },
        "execution_before": before_explanation,
        "evolution": {
            "operation": update["operation"],
            "before_snapshot": before.snapshot_id,
            "after_snapshot": after.snapshot_id,
            "score_before": before_explanation["score"],
            "score_after": after_explanation["score"],
            "score_delta": after_explanation["score"] - before_explanation["score"],
            "new_paths": after_explanation["paths"],
        },
        "rollback": {
            "snapshot_exact": rebuilt.snapshot_id == before.snapshot_id,
            "score_exact": rollback_explanation["score"] == before_explanation["score"],
            "explanation_exact": rollback_explanation == before_explanation,
        },
    }


def main():
    print(json.dumps(build_trace_record(), indent=2))


if __name__ == "__main__":
    main()
