"""Demonstrate one inspectable MML change, its consequences, and rollback."""

import json

import benchmark


def rank_with(model, documents, queries):
    rankings = {}
    for query in queries:
        if query["tier"] != "gdpr":
            continue
        terms = query["terms"] + query.get("mml_concepts", [])
        scores = [
            (document["id"], model.score(terms, document["text"], query.get("negative_terms")))
            for document in documents if document["tier"] == "gdpr"
        ]
        rankings[query["id"]] = sorted(scores, key=lambda item: (-item[1], item[0]))
    return rankings


def run_update_demo():
    validated = benchmark.validate_benchmark()
    update = benchmark.load_json(benchmark.UPDATE_PATH)
    before = benchmark.MODELS["gdpr_typed"]
    after = before.with_relation_update(update["relation"])
    before_ranking = rank_with(before, validated["documents"], validated["queries"])
    after_ranking = rank_with(after, validated["documents"], validated["queries"])

    affected = {}
    for query_id in before_ranking:
        old = dict(before_ranking[query_id])
        new = dict(after_ranking[query_id])
        affected[query_id] = sum(abs(old[item] - new[item]) > 1e-12 for item in old)

    rebuilt = benchmark.build_models()["gdpr_typed"]
    rollback = rank_with(rebuilt, validated["documents"], validated["queries"])
    return {
        "purpose": "describe consequences of one governed relation change; no locality verdict",
        "change": update["relation"],
        "before_snapshot": before.snapshot_id,
        "after_snapshot": after.snapshot_id,
        "snapshot_changed": before.snapshot_id != after.snapshot_id,
        "affected_documents_by_query": affected,
        "rollback_snapshot_exact": rebuilt.snapshot_id == before.snapshot_id,
        "rollback_ranking_exact": rollback == before_ranking,
    }


def main():
    result = run_update_demo()
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
