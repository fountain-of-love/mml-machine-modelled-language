import re
from pathlib import Path
from heapq import heappop, heappush

import numpy as np


def tokenize(text):
    return re.findall(r"[a-z0-9_]+", text.lower())


# 1. Load the balanced polysemy and separate GDPR-law construction layers.
CORPUS_PATHS = [
    Path(__file__).parent / "data" / "construction" / "polysemy_corpus.txt",
    Path(__file__).parent / "data" / "construction" / "gdpr_law_corpus.txt",
]
corpus = [
    line.strip()
    for corpus_path in CORPUS_PATHS
    for line in corpus_path.read_text(encoding="utf-8").splitlines()
    if line.strip()
]

# 2. Build Vocabulary
words = []
for sentence in corpus:
    words.extend(tokenize(sentence))

vocab = sorted(list(set(words)))
word2idx = {w: i for i, w in enumerate(vocab)}
idx2word = {i: w for i, w in enumerate(vocab)}
vocab_size = len(vocab)

display_stop_words = {
    "a",
    "about",
    "after",
    "also",
    "an",
    "and",
    "as",
    "be",
    "became",
    "both",
    "by",
    "can",
    "could",
    "did",
    "during",
    "each",
    "every",
    "for",
    "from",
    "had",
    "in",
    "into",
    "is",
    "it",
    "its",
    "i",
    "more",
    "my",
    "near",
    "no",
    "not",
    "of",
    "on",
    "only",
    "or",
    "over",
    "part",
    "that",
    "the",
    "their",
    "then",
    "therefore",
    "to",
    "was",
    "were",
    "when",
    "where",
    "which",
    "who",
    "with",
    "without",
    "would",
    "we",
    "will",
}

# 3. Construct Co-occurrence Matrix (Sliding Window = 2)
co_occurrence = np.zeros((vocab_size, vocab_size))
window_size = 2

for sentence in corpus:
    tokens = tokenize(sentence)
    for i, token in enumerate(tokens):
        target_idx = word2idx[token]
        start = max(0, i - window_size)
        end = min(len(tokens), i + window_size + 1)
        for j in range(start, end):
            if i != j:
                neighbor_idx = word2idx[tokens[j]]
                co_occurrence[target_idx, neighbor_idx] += 1.0

# 4. Normalize to Row-Stochastic Transition Matrix P
row_sums = co_occurrence.sum(axis=1, keepdims=True)
row_sums[row_sums == 0] = 1.0  # Avoid division by zero
P = co_occurrence / row_sums


def _single_anchor_diffusion(target_word, P, d, max_iter, tol):
    v = np.zeros(vocab_size)
    v[word2idx[target_word]] = 1.0
    pi = v.copy()

    for _ in range(max_iter):
        pi_next = d * (pi @ P) + (1 - d) * v
        if np.linalg.norm(pi_next - pi, ord=1) < tol:
            return pi_next
        pi = pi_next

    return pi


# 5. Combinatorial query activation over the word graph
def query_anchored_diffusion(query_words, P, d=0.85, max_iter=100, tol=1e-6):
    """
    Computes a query-anchored activation distribution over the vocabulary.

    Each known query word creates its own propagated field. Multi-token queries
    combine those fields with a normalized geometric mean, so nodes must receive
    support from every query field instead of merely inheriting their average.
    Unknown words are ignored when at least one query word is known.
    """
    if isinstance(query_words, str):
        query_words = [query_words]

    available_words = list(dict.fromkeys(known_words(query_words)))
    if not available_words:
        raise ValueError("Query contains no words from the vocabulary.")

    fields = [
        _single_anchor_diffusion(word, P, d, max_iter, tol)
        for word in available_words
    ]
    if len(fields) == 1:
        return fields[0]

    epsilon = np.finfo(float).tiny
    combined = np.exp(np.mean(np.log(np.maximum(fields, epsilon)), axis=0))
    total = combined.sum()
    if total == 0:
        raise ValueError("Query fields have no shared activation.")
    return combined / total


def strongest_activation_path(source_word, target_word, P, max_hops=6):
    """Return the highest-probability path within max_hops over non-zero edges."""
    if source_word not in word2idx or target_word not in word2idx:
        raise ValueError("Path endpoints must be words from the vocabulary.")

    source_idx = word2idx[source_word]
    target_idx = word2idx[target_word]
    queue = [(-1.0, 0, source_idx, [source_idx], [])]
    best_probability = {(source_idx, 0): 1.0}

    while queue:
        negative_probability, hops, node_idx, path, edge_weights = heappop(queue)
        probability = -negative_probability
        if node_idx == target_idx:
            return {
                "words": [idx2word[idx] for idx in path],
                "edge_weights": edge_weights,
                "probability": probability,
            }
        if hops == max_hops:
            continue

        for neighbor_idx in np.flatnonzero(P[node_idx]):
            edge_weight = float(P[node_idx, neighbor_idx])
            next_probability = probability * edge_weight
            state = (int(neighbor_idx), hops + 1)
            if next_probability <= best_probability.get(state, 0.0):
                continue
            best_probability[state] = next_probability
            heappush(
                queue,
                (
                    -next_probability,
                    hops + 1,
                    int(neighbor_idx),
                    path + [int(neighbor_idx)],
                    edge_weights + [edge_weight],
                ),
            )

    return None


MML_TARGETS = {
    "Polysemy": [
        "bank",
        "branch",
        "interest",
        "balance",
        "account",
        "record",
        "right",
        "subject",
    ],
    "Relational Escalation": [
        "information",
        "control",
        "evidentiary",
        "procedural",
        "advantage",
    ],
    "Paraphrase-Field Overlap": [
        "asymmetry",
        "imbalance",
        "gap",
        "advantage",
        "uncertainty",
    ],
    "Contrast-Pair Contextual Overlap": [
        "complete",
        "incomplete",
        "disclosed",
        "retained",
        "formal",
        "effective",
    ],
    "Cross-Domain Bridges": [
        "river",
        "money",
        "data",
        "evidence",
        "rights",
        "justice",
    ],
    "Higher-Order Pattern Activation": [
        "pattern",
        "control",
        "evidence",
        "fairness",
        "accountability",
    ],
}

SIMILARITY_PAIRS = [
    ("asymmetry", "imbalance"),
    ("gap", "uncertainty"),
    ("information", "evidence"),
    ("control", "advantage"),
    ("complete", "incomplete"),
    ("disclosed", "retained"),
    ("formal", "effective"),
    ("rights", "remedy"),
]

CONTRASTS = [
    ("complete", "incomplete"),
    ("disclosed", "retained"),
    ("formal", "effective"),
    ("rights", "remedy"),
]

BRIDGE_PATH = ["river", "bank", "account", "data", "evidence", "rights", "justice"]


def known_words(words):
    return [word for word in words if word in word2idx]


def top_weighted_words(scores, top_n=10, exclude_query_words=None):
    exclude_query_words = set(exclude_query_words or [])
    top_indices = [
        idx
        for idx in np.argsort(scores)[::-1]
        if idx2word[idx] not in display_stop_words
        and idx2word[idx] not in exclude_query_words
    ]
    return [(idx2word[idx], scores[idx]) for idx in top_indices[:top_n]]


def activation_distribution(query_words):
    return query_anchored_diffusion(query_words, P)


def explain_activation(query_words, top_n=5, max_hops=6):
    """Explain top activated words with the strongest path from each query word."""
    if isinstance(query_words, str):
        query_words = [query_words]
    available_words = list(dict.fromkeys(known_words(query_words)))
    scores = activation_distribution(available_words)
    explanations = []

    for target_word, score in top_weighted_words(
        scores,
        top_n,
        exclude_query_words=available_words,
    ):
        explanations.append(
            {
                "word": target_word,
                "score": float(score),
                "query_paths": {
                    source_word: strongest_activation_path(
                        source_word,
                        target_word,
                        P,
                        max_hops=max_hops,
                    )
                    for source_word in available_words
                },
            }
        )

    return explanations


def group_activation(words):
    vectors = [activation_distribution(word) for word in known_words(words)]
    if not vectors:
        return np.zeros(vocab_size)
    return np.mean(vectors, axis=0)


def text_activation(text):
    return group_activation(tokenize(text))


def cosine_similarity(left, right):
    denom = np.linalg.norm(left) * np.linalg.norm(right)
    if denom == 0:
        return 0.0
    return float(left @ right / denom)


# 6. Output word-level contextual weight distributions
def display_activation_weights(target_word, top_n=8):
    scores = activation_distribution(target_word)
    print(f"--- Word-Level Activation Weights for Query Token: '{target_word}' ---")
    for rank, (word, score) in enumerate(top_weighted_words(scores, top_n), start=1):
        print(f"{rank:>2}. {word:<16} : {score:.4f}")
    print()


def display_group_activation(label, words, top_n=10):
    available_words = known_words(words)
    missing_words = sorted(set(words) - set(available_words))
    scores = group_activation(available_words)

    print(f"=== {label} ===")
    print(f"Targets: {', '.join(available_words)}")
    if missing_words:
        print(f"Missing from vocabulary: {', '.join(missing_words)}")
    for rank, (word, score) in enumerate(
        top_weighted_words(scores, top_n, exclude_query_words=available_words),
        start=1,
    ):
        print(f"{rank:>2}. {word:<16} : {score:.4f}")
    print()


def display_activation_explanation(query_words, top_n=3):
    print(f"=== Activation Explanation: {' + '.join(query_words)} ===")
    for explanation in explain_activation(query_words, top_n=top_n):
        print(f"{explanation['word']} | activation {explanation['score']:.4f}")
        for source_word, path in explanation["query_paths"].items():
            if path is None:
                print(f"  {source_word}: no path within hop limit")
                continue
            route = " -> ".join(path["words"])
            print(f"  {source_word}: {route} | path probability {path['probability']:.6f}")
    print()


def display_similarity_probes(pairs):
    print("=== Paraphrase And Relatedness Similarity ===")
    for left, right in pairs:
        if left not in word2idx or right not in word2idx:
            print(f"{left:<14} ~ {right:<14} : unavailable")
            continue
        similarity = cosine_similarity(activation_distribution(left), activation_distribution(right))
        print(f"{left:<14} ~ {right:<14} : {similarity:.4f}")
    print()


def display_contrast_probes(contrasts, top_n=6):
    print("=== Contrast-Pair Contextual Overlap ===")
    for left, right in contrasts:
        if left not in word2idx or right not in word2idx:
            print(f"{left} vs {right}: unavailable")
            continue

        left_scores = activation_distribution(left)
        right_scores = activation_distribution(right)
        shared_scores = np.minimum(left_scores, right_scores)
        similarity = cosine_similarity(left_scores, right_scores)
        shared_words = top_weighted_words(
            shared_scores,
            top_n,
            exclude_query_words={left, right},
        )

        print(f"{left} vs {right} | shared-field similarity: {similarity:.4f}")
        print("  " + ", ".join(f"{word} ({score:.4f})" for word, score in shared_words))
    print()


def display_bridge_path(path, top_n=5):
    print("=== Cross-Domain Bridge Path ===")
    for left, right in zip(path, path[1:]):
        if left not in word2idx or right not in word2idx:
            print(f"{left} -> {right}: unavailable")
            continue

        left_scores = activation_distribution(left)
        right_scores = activation_distribution(right)
        overlap = np.minimum(left_scores, right_scores)
        similarity = cosine_similarity(left_scores, right_scores)
        bridge_words = top_weighted_words(
            overlap,
            top_n,
            exclude_query_words={left, right},
        )

        print(f"{left} -> {right} | overlap: {similarity:.4f}")
        print("  " + ", ".join(f"{word} ({score:.4f})" for word, score in bridge_words))
    print()


def main():
    print(f"Corpus sentences: {len(corpus)}")
    print(f"Vocabulary size: {vocab_size}")
    print()

    # These probes turn the corpus into a small MML diagnostic bench:
    # ambiguity, escalation, paraphrase, contrast, bridging, and abstraction.
    print("=== Individual Context Probes ===")
    for query in ["river", "money", "bank", "account", "data", "evidence", "control", "access"]:
        display_activation_weights(query)

    for label, words in MML_TARGETS.items():
        display_group_activation(label, words)

    display_activation_explanation(["river", "bank"])
    display_activation_explanation(["money", "bank"])
    display_similarity_probes(SIMILARITY_PAIRS)
    display_contrast_probes(CONTRASTS)
    display_bridge_path(BRIDGE_PATH)


if __name__ == "__main__":
    main()

