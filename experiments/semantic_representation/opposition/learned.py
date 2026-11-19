"""A toy 'learned' relation: distributional similarity from a tiny corpus.

This stands in for weights a model acquires from text. It is not an LLM. Each
animal becomes a vector of the words it co-occurs with in a sentence; the
learned signed relation is the cosine of mean-centred vectors, in [-1, 1].
The point is the validation procedure applied to it, not the model itself.
"""

from __future__ import annotations

import re

import numpy as np

from src.semantic_representation.relation_encoding import SignedRelationMatrix


def context_vectors(animals: tuple[str, ...], sentences: list[str], stopwords: set[str]) -> tuple[np.ndarray, tuple[str, ...]]:
    """Count, per animal, the other content words in each sentence it occurs in."""
    tokenized = [[w for w in re.findall(r"[a-z]+", s.lower()) if w not in stopwords] for s in sentences]
    vocabulary = tuple(sorted({w for words in tokenized for w in words}))
    column = {word: j for j, word in enumerate(vocabulary)}
    counts = np.zeros((len(animals), len(vocabulary)))
    for words in tokenized:
        for i, animal in enumerate(animals):
            if animal in words:
                for word in words:
                    if word != animal:
                        counts[i, column[word]] += 1
    return counts, vocabulary


def learned_relation(fixture: dict) -> SignedRelationMatrix:
    """Mean-centred cosine similarity between animal context vectors."""
    animals = tuple(fixture["animals"])
    corpus = fixture["toy_corpus"]
    counts, _ = context_vectors(animals, corpus["sentences"], set(corpus["stopwords"]))
    centred = counts - counts.mean(axis=0)
    norms = np.linalg.norm(centred, axis=1, keepdims=True)
    unit = centred / np.where(norms == 0, 1.0, norms)
    similarity = np.clip(unit @ unit.T, -1.0, 1.0)
    np.fill_diagonal(similarity, 1.0)
    similarity.setflags(write=False)
    return SignedRelationMatrix(animals, similarity)
