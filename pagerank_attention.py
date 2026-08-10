from dataclasses import dataclass

import numpy as np


# Scenario A preserves the ambiguous surface word exactly as it appears in text.
AMBIGUOUS_CORPUS = (
    "i ate a crisp apple while sitting by the river bank",
    "a cool breeze moved through the trees and across the water",
    "dark clouds gathered above the river and a storm was coming",
    "i left the river bank before the rain began",
    "i needed money and asked an eu bank for a loan",
    "the process went badly and the bank made several mistakes",
    "i used my gdpr rights to understand what had happened",
    "instead of fixing the problem the bank kept digging a bigger hole",
)

# Scenario B is derived from A through one explicit governed intervention per
# sentence. None means that the sentence contains no occurrence to curate.
BANK_SENSE_ASSIGNMENTS = (
    "bank_river",
    None,
    None,
    "bank_river",
    "bank_financial",
    "bank_financial",
    None,
    "bank_financial",
)


def curate_bank_senses(sentences, assignments):
    if len(sentences) != len(assignments):
        raise ValueError("every sentence requires an explicit bank-sense assignment")
    curated = []
    for sentence, sense in zip(sentences, assignments):
        occurrence_count = sentence.split().count("bank")
        if occurrence_count != (1 if sense else 0):
            raise ValueError("bank-sense assignments must match corpus occurrences exactly")
        curated.append(sentence.replace("bank", sense) if sense else sentence)
    return tuple(curated)


CURATED_CORPUS = curate_bank_senses(AMBIGUOUS_CORPUS, BANK_SENSE_ASSIGNMENTS)

# These diagnostic sets contain words locally authored around each occurrence of
# the sense being measured. They are declared rather than selected from results.
RIVER_CONTEXT = frozenset({"river", "water", "rain"})
FINANCIAL_CONTEXT = frozenset({"money", "loan", "eu", "mistakes"})
DISPLAY_STOP_WORDS = frozenset({
    "a", "an", "and", "before", "by", "for", "i", "instead", "my", "of",
    "the", "to", "was", "what", "while",
})


@dataclass(frozen=True)
class CooccurrenceGraph:
    vocab: tuple
    word2idx: dict
    idx2word: dict
    transition: np.ndarray


def build_graph(sentences, window_size=2):
    """Compile a corpus into a deterministic row-stochastic word graph."""
    tokenized = [sentence.lower().split() for sentence in sentences]
    vocab = tuple(sorted({word for tokens in tokenized for word in tokens}))
    word2idx = {word: index for index, word in enumerate(vocab)}
    idx2word = {index: word for word, index in word2idx.items()}
    co_occurrence = np.zeros((len(vocab), len(vocab)))

    for tokens in tokenized:
        for index, token in enumerate(tokens):
            start = max(0, index - window_size)
            end = min(len(tokens), index + window_size + 1)
            for neighbor_position in range(start, end):
                if index != neighbor_position:
                    neighbor = tokens[neighbor_position]
                    co_occurrence[word2idx[token], word2idx[neighbor]] += 1.0

    row_sums = co_occurrence.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1.0
    transition = co_occurrence / row_sums
    return CooccurrenceGraph(vocab, word2idx, idx2word, transition)


AMBIGUOUS_GRAPH = build_graph(AMBIGUOUS_CORPUS)
CURATED_GRAPH = build_graph(CURATED_CORPUS)

# Keep the original minimal-demo names available for existing callers.
corpus = list(AMBIGUOUS_CORPUS)
vocab = list(AMBIGUOUS_GRAPH.vocab)
word2idx = AMBIGUOUS_GRAPH.word2idx
idx2word = AMBIGUOUS_GRAPH.idx2word
vocab_size = len(vocab)
P = AMBIGUOUS_GRAPH.transition


def query_anchored_diffusion(target_word, graph=AMBIGUOUS_GRAPH, d=0.85, max_iter=100, tol=1e-6):
    """Return Personalized PageRank activation anchored on one graph node."""
    if isinstance(graph, np.ndarray):
        # Backward compatibility for the original query_anchored_diffusion(word, P)
        # interface. Other graph matrices must be passed as CooccurrenceGraph values.
        if graph is not P:
            raise ValueError("pass a CooccurrenceGraph when querying a different graph")
        graph = AMBIGUOUS_GRAPH
    if target_word not in graph.word2idx:
        raise ValueError(f"'{target_word}' not in vocabulary.")

    anchor = np.zeros(len(graph.vocab))
    anchor[graph.word2idx[target_word]] = 1.0
    activation = anchor.copy()

    for _ in range(max_iter):
        next_activation = d * (activation @ graph.transition) + (1 - d) * anchor
        if np.linalg.norm(next_activation - activation, ord=1) < tol:
            return next_activation
        activation = next_activation

    return activation


def activation_by_word(target_word, graph):
    scores = query_anchored_diffusion(target_word, graph)
    return {word: float(scores[index]) for index, word in graph.idx2word.items()}


def context_weight(activation, context):
    """Sum activation carried by named contextual words shared across scenarios."""
    return sum(activation.get(word, 0.0) for word in context)


def curation_ab_result():
    ambiguous = activation_by_word("bank", AMBIGUOUS_GRAPH)
    river = activation_by_word("bank_river", CURATED_GRAPH)
    financial = activation_by_word("bank_financial", CURATED_GRAPH)
    return {
        "ambiguous": {
            "activation": ambiguous,
            "river_context_weight": context_weight(ambiguous, RIVER_CONTEXT),
            "financial_context_weight": context_weight(ambiguous, FINANCIAL_CONTEXT),
        },
        "bank_river": {
            "activation": river,
            "own_context_weight": context_weight(river, RIVER_CONTEXT),
            "opposite_context_weight": context_weight(river, FINANCIAL_CONTEXT),
        },
        "bank_financial": {
            "activation": financial,
            "own_context_weight": context_weight(financial, FINANCIAL_CONTEXT),
            "opposite_context_weight": context_weight(financial, RIVER_CONTEXT),
        },
    }


def top_activations(activation, top_n=8, exclude=()):
    excluded = set(exclude)
    return sorted(
        ((word, weight) for word, weight in activation.items() if word not in excluded),
        key=lambda item: (-item[1], item[0]),
    )[:top_n]


def display_activation(label, activation, top_n=8, exclude=()):
    print(f"--- {label} ---")
    for rank, (word, weight) in enumerate(top_activations(activation, top_n, exclude), 1):
        print(f"{rank}. {word:<16} : {weight:.4f}")
    print()


def display_curation_ab_test():
    result = curation_ab_result()
    ambiguous = result["ambiguous"]
    river = result["bank_river"]
    financial = result["bank_financial"]

    print("SCENARIO A — one ambiguous concept")
    display_activation(
        "Activation for 'bank'",
        ambiguous["activation"],
        exclude=DISPLAY_STOP_WORDS | {"bank"},
    )
    print(
        "Context weight: "
        f"river={ambiguous['river_context_weight']:.4f}, "
        f"financial={ambiguous['financial_context_weight']:.4f}\n"
    )

    print("SCENARIO B — curated concept identities")
    display_activation(
        "Activation for 'bank_river'",
        river["activation"],
        exclude=DISPLAY_STOP_WORDS | {"bank_river", "bank_financial"},
    )
    print(
        "Context weight: "
        f"own={river['own_context_weight']:.4f}, "
        f"opposite={river['opposite_context_weight']:.4f}\n"
    )
    display_activation(
        "Activation for 'bank_financial'",
        financial["activation"],
        exclude=DISPLAY_STOP_WORDS | {"bank_river", "bank_financial"},
    )
    print(
        "Context weight: "
        f"own={financial['own_context_weight']:.4f}, "
        f"opposite={financial['opposite_context_weight']:.4f}\n"
    )


def main():
    display_curation_ab_test()


if __name__ == "__main__":
    main()
