"""Impurity và gain (entropy log2; Gini; lỗi phân loại) cho cây rời rạc."""

from __future__ import annotations

import math
from collections import Counter
from typing import Literal

import pandas as pd

ImpurityFn = Literal["entropy", "gini", "error"]


def entropy(labels: list) -> float:
    ctr = Counter(labels)
    n = sum(ctr.values())
    if n == 0:
        return 0.0
    ent = 0.0
    for c in ctr.values():
        p = c / n
        if p > 0:
            ent -= p * math.log2(p)
    return ent


def gini(labels: list) -> float:
    ctr = Counter(labels)
    n = sum(ctr.values())
    if n == 0:
        return 0.0
    return 1.0 - sum((c / n) ** 2 for c in ctr.values())


def classification_error(labels: list) -> float:
    ctr = Counter(labels)
    n = sum(ctr.values())
    if n == 0:
        return 0.0
    return 1.0 - max(ctr.values()) / n


def impurity(labels: list, criterion: ImpurityFn) -> float:
    if criterion == "entropy":
        return entropy(labels)
    if criterion == "gini":
        return gini(labels)
    return classification_error(labels)


def weighted_impurity_after_split(
    subsets: list[list],
    criterion: ImpurityFn,
) -> float:
    total = sum(len(s) for s in subsets)
    if total == 0:
        return 0.0
    acc = 0.0
    for s in subsets:
        acc += len(s) / total * impurity(list(s), criterion)
    return acc


def gain(
    df: pd.DataFrame,
    attr: str,
    target: str,
    criterion: ImpurityFn,
) -> tuple[float, float, float]:
    """Trả về (impurity cha, entropy/Gini/error có trọng số sau tách theo attr, độ giảm / gain)."""
    parent_labels = df[target].tolist()
    ip = impurity(parent_labels, criterion)
    subsets = []
    for v in sorted(df[attr].unique(), key=lambda x: str(x)):
        sub = df[df[attr] == v][target].tolist()
        subsets.append(sub)
    w_child = weighted_impurity_after_split(subsets, criterion)
    return ip, w_child, ip - w_child
