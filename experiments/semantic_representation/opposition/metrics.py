"""Information-retrieval measures over the distinct pairs of a relation matrix."""

from __future__ import annotations

import math
from collections import Counter
from dataclasses import dataclass

import numpy as np


def pair_values(values: np.ndarray) -> np.ndarray:
    """Upper-triangle cells: each unordered pair of distinct items once."""
    return values[np.triu_indices(values.shape[0], k=1)]


@dataclass(frozen=True)
class BinaryReport:
    tp: int
    fp: int
    tn: int
    fn: int

    @property
    def sensitivity(self) -> float:
        return self.tp / (self.tp + self.fn) if self.tp + self.fn else math.nan

    @property
    def specificity(self) -> float:
        return self.tn / (self.tn + self.fp) if self.tn + self.fp else math.nan

    @property
    def precision(self) -> float:
        return self.tp / (self.tp + self.fp) if self.tp + self.fp else math.nan


def binary_report(truth: np.ndarray, predicted: np.ndarray) -> BinaryReport:
    truth, predicted = truth.astype(bool), predicted.astype(bool)
    return BinaryReport(
        tp=int(np.sum(truth & predicted)),
        fp=int(np.sum(~truth & predicted)),
        tn=int(np.sum(~truth & ~predicted)),
        fn=int(np.sum(truth & ~predicted)),
    )


def auc(scores: np.ndarray, truth: np.ndarray) -> float:
    """Probability that a random positive outranks a random negative (ties = 1/2)."""
    positives, negatives = scores[truth.astype(bool)], scores[~truth.astype(bool)]
    if not len(positives) or not len(negatives):
        return math.nan
    wins = sum(float(np.sum(p > negatives)) + 0.5 * float(np.sum(p == negatives)) for p in positives)
    return wins / (len(positives) * len(negatives))


def entropy_bits(labels: np.ndarray) -> float:
    """Shannon entropy of the label distribution, in bits."""
    counts = np.array(list(Counter(labels.tolist()).values()), dtype=float)
    p = counts / counts.sum()
    return float(-(p * np.log2(p)).sum())


@dataclass(frozen=True)
class ThreeStateReport:
    accuracy: float
    macro_f1: float
    recall: dict


def three_state_report(truth: np.ndarray, predicted: np.ndarray) -> ThreeStateReport:
    """Accuracy, per-state recall, and macro-F1 for opposite / neutral / alike."""
    names = {-1: "opposite", 0: "neutral", 1: "alike"}
    recall, f1s = {}, []
    for state, name in names.items():
        tp = np.sum((truth == state) & (predicted == state))
        actual, claimed = np.sum(truth == state), np.sum(predicted == state)
        recall[name] = float(tp / actual) if actual else math.nan
        f1s.append(float(2 * tp / (actual + claimed)) if actual + claimed else 0.0)
    return ThreeStateReport(float(np.mean(truth == predicted)), float(np.mean(f1s)), recall)
