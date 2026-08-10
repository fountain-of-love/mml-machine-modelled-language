"""Compile semantic transition models and query them for contextual activation.

Ground the known. Focus the intended. Activate the related.

Vocabulary: ``docs/activate-grounded-focus-vocabulary.md``.

This module is the technical expression of "words carry weight":

- words are addressable semantic identities in a ``TransitionModel``;
- weight is explicit transition capacity in the compiled operator;
- carry is the activation strategy propagating activation between identities; and
- weight is expressed contextually in the resulting activation distribution.

The first activation strategy uses Personalized PageRank. Other strategies can
activate the same model, and future compilers can produce models from richer semantic
relations than the co-occurrence observations used by ``compile_transition_model``.
"""

# Ground the known. Focus the intended. Activate the related.

from dataclasses import dataclass
from typing import Protocol, runtime_checkable

import numpy as np


@dataclass(frozen=True)
class TransitionModel:
    """Addressable semantic identities and their transition operator."""

    identities: tuple
    identity_to_index: dict
    transition: np.ndarray


@dataclass(frozen=True)
class SemanticGrounding:
    """Ground one corpus occurrence in a governed semantic identity."""

    sentence_index: int
    surface_identity: str
    grounded_identity: str


@dataclass(frozen=True)
class SemanticFocus:
    """Represent narrowing from an ambiguous identity to a focused identity."""

    source_identity: str
    focused_identity: str


@dataclass(frozen=True)
class Activation:
    """Query-relative activation assigned to each semantic identity."""

    model: TransitionModel
    weights: np.ndarray
    converged: object = None
    iterations: int = 0
    residual: object = None

    def by_identity(self):
        return {
            identity: float(self.weights[index])
            for index, identity in enumerate(self.model.identities)
        }

    def weight_for(self, identity):
        index = self.model.identity_to_index.get(identity)
        if index is None:
            return 0.0
        return float(self.weights[index])


@runtime_checkable
class ActivationStrategy(Protocol):
    """Interchangeable algorithm for activating a transition model."""

    def activate(self, model, semantic_identity):
        """Return the activation produced for one semantic identity."""


@dataclass(frozen=True)
class PersonalizedPageRankActivationStrategy:
    """Activate through converged Personalized PageRank with query restart."""

    damping: float = 0.85
    max_iterations: int = 100
    tolerance: float = 1e-6

    def activate(self, model, semantic_identity):
        if semantic_identity not in model.identity_to_index:
            raise ValueError(f"'{semantic_identity}' not in model")

        anchor = np.zeros(len(model.identities))
        anchor[model.identity_to_index[semantic_identity]] = 1.0
        activation = anchor.copy()

        residual = None
        for iteration in range(1, self.max_iterations + 1):
            next_activation = (
                self.damping * (activation @ model.transition)
                + (1 - self.damping) * anchor
            )
            residual = float(np.linalg.norm(next_activation - activation, ord=1))
            if residual < self.tolerance:
                return Activation(
                    model,
                    next_activation,
                    converged=True,
                    iterations=iteration,
                    residual=residual,
                )
            activation = next_activation

        return Activation(
            model,
            activation,
            converged=False,
            iterations=self.max_iterations,
            residual=residual,
        )


def compile_transition_model(sentences, window_size=2):
    """Compile local token co-occurrence into a row-stochastic transition model."""
    tokenized = [sentence.lower().split() for sentence in sentences]
    identities = tuple(sorted({token for tokens in tokenized for token in tokens}))
    if not identities:
        raise ValueError("at least one semantic identity is required")

    identity_to_index = {
        identity: index for index, identity in enumerate(identities)
    }
    co_occurrence = np.zeros((len(identities), len(identities)))

    for tokens in tokenized:
        for index, token in enumerate(tokens):
            start = max(0, index - window_size)
            end = min(len(tokens), index + window_size + 1)
            for neighbor_position in range(start, end):
                if index != neighbor_position:
                    neighbor = tokens[neighbor_position]
                    co_occurrence[
                        identity_to_index[token], identity_to_index[neighbor]
                    ] += 1.0

    row_sums = co_occurrence.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1.0
    transition = co_occurrence / row_sums
    return TransitionModel(identities, identity_to_index, transition)


def ground(sentences, semantic_groundings):
    """Apply declared semantic groundings to corpus occurrences."""
    grounded = [sentence.split() for sentence in sentences]
    touched_sentences = set()

    for semantic_grounding in semantic_groundings:
        sentence_index = semantic_grounding.sentence_index
        surface_identity = semantic_grounding.surface_identity
        grounded_identity = semantic_grounding.grounded_identity
        if sentence_index in touched_sentences:
            raise ValueError("each sentence can have only one grounding in this experiment")
        if not 0 <= sentence_index < len(grounded):
            raise ValueError("grounding sentence_index is outside the corpus")
        if grounded[sentence_index].count(surface_identity) != 1:
            raise ValueError("grounded surface must occur exactly once in its sentence")
        if grounded_identity == surface_identity:
            raise ValueError("semantic grounding must identify a different identity")
        grounded[sentence_index] = [
            grounded_identity if token == surface_identity else token
            for token in grounded[sentence_index]
        ]
        touched_sentences.add(sentence_index)

    return tuple(" ".join(tokens) for tokens in grounded)


def focus(source_identity, semantic_focus):
    """Apply one declared semantic focus before activation."""
    if semantic_focus.source_identity != source_identity:
        raise ValueError("semantic focus does not apply to the source identity")
    if semantic_focus.focused_identity == source_identity:
        raise ValueError("semantic focus must narrow to a different identity")
    return semantic_focus.focused_identity


def activate(model, semantic_identity, strategy):
    """Activate a transition model through the selected strategy."""
    return strategy.activate(model, semantic_identity)
