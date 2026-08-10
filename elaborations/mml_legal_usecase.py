import json
from pathlib import Path

from .mml_elaborate_corpus import (
    cosine_similarity,
    group_activation,
    known_words,
    text_activation,
    tokenize,
)


DEMO_FIXTURES_PATH = Path(__file__).parent.parent / "data" / "demonstration" / "legal_demo.json"
_DEMO_FIXTURES = json.loads(DEMO_FIXTURES_PATH.read_text(encoding="utf-8"))
LEGAL_CASE_THEMES = _DEMO_FIXTURES["themes"]
EMAIL_EVIDENCE_CANDIDATES = _DEMO_FIXTURES["emails"]


def lexical_overlap_score(email, theme_words):
    email_tokens = set(tokenize(email["text"]))
    theme_tokens = set(theme_words)
    if not theme_tokens:
        return 0.0
    return len(email_tokens & theme_tokens) / len(theme_tokens)


def theme_alignment_score(email, theme_words):
    email_scores = text_activation(email["text"])
    theme_scores = group_activation(theme_words)
    graph_score = cosine_similarity(email_scores, theme_scores)
    lexical_score = lexical_overlap_score(email, theme_words)
    return graph_score * (0.2 + (0.8 * lexical_score))


def ranked_emails_for_theme(theme_words, require_lexical_overlap=True):
    scored_emails = [
        (theme_alignment_score(email, theme_words), email)
        for email in EMAIL_EVIDENCE_CANDIDATES
        if not require_lexical_overlap or lexical_overlap_score(email, theme_words) > 0
    ]
    return sorted(scored_emails, key=lambda item: item[0], reverse=True)


def curation_ab_result(theme_words, top_n=3):
    """Compare curated lexical candidate generation with graph scoring over all fixtures."""
    curated = ranked_emails_for_theme(theme_words, require_lexical_overlap=True)
    unfiltered = ranked_emails_for_theme(theme_words, require_lexical_overlap=False)
    curated_ids = [email["id"] for _, email in curated[:top_n]]
    unfiltered_ids = [email["id"] for _, email in unfiltered[:top_n]]
    return {
        "curated_top_ids": curated_ids,
        "unfiltered_top_ids": unfiltered_ids,
        "agreement": len(set(curated_ids) & set(unfiltered_ids)) / top_n,
        "curated_candidate_count": len(curated),
        "unfiltered_candidate_count": len(unfiltered),
    }


def display_email_discovery(top_n=3):
    print("=== Practical Use Case: Emails Supporting A GDPR Access Lawsuit ===")
    print("Goal: identify communications that support a claim that the bank failed to respect a GDPR right of access.")
    print("Source: uses the corpus-derived transition matrix from elaborations/mml_elaborate_corpus.py.")
    print("Score: graph-activation similarity gated by exact legal signal overlap.")
    print()

    for theme in LEGAL_CASE_THEMES.values():
        words = theme["words"]
        scored_emails = ranked_emails_for_theme(words)

        print(f"--- Issue: {theme['label']} ---")
        print(f"Signal words: {', '.join(known_words(words))}")
        for score, email in scored_emails[:top_n]:
            print(f"{email['id']} | {email['sender']:<8} | theme alignment {score:.4f}")
            print(f"  {email['text']}")
        print()


def display_lawsuit_evidence_package():
    print("=== Candidate Evidence Package ===")
    package_themes = [
        "gdpr_access_request",
        "incomplete_disclosure",
        "bank_information_control",
        "verification_blocked",
        "procedural_imbalance",
        "effective_remedy",
    ]

    selected = {}
    for theme in package_themes:
        words = LEGAL_CASE_THEMES[theme]["words"]
        ranked_emails = ranked_emails_for_theme(words)
        if not ranked_emails:
            continue
        score, email = ranked_emails[0]
        selected[email["id"]] = (email, max(score, selected.get(email["id"], (None, 0.0))[1]))

    for email_id, (email, score) in sorted(selected.items()):
        print(f"{email_id} | {email['sender']:<8} | strongest theme alignment {score:.4f}")
        print(f"  {email['text']}")
    print()


def display_curation_ab_test(top_n=3):
    print("=== Curation A/B Diagnostic ===")
    print("A: exact-overlap candidate generation followed by graph scoring.")
    print("B: graph scoring over every authored candidate.")
    print("This measures the effect of curation; neither arm is held-out validation.")
    for theme in LEGAL_CASE_THEMES.values():
        result = curation_ab_result(theme["words"], top_n)
        print(
            f"{theme['label']}: agreement {result['agreement']:.2f} | "
            f"A candidates {result['curated_candidate_count']} | "
            f"B candidates {result['unfiltered_candidate_count']}"
        )
        print(f"  A top: {', '.join(result['curated_top_ids']) or 'none'}")
        print(f"  B top: {', '.join(result['unfiltered_top_ids']) or 'none'}")
    print()


def main():
    display_email_discovery()
    display_lawsuit_evidence_package()
    display_curation_ab_test()


if __name__ == "__main__":
    main()
