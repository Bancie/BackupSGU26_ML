"""Cây quyết định đa nhánh cho thuộc tính phân loại (ID3‑style gain)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd

from metrics import ImpurityFn, gain


@dataclass
class Leaf:
    label: Any

    def __str__(self) -> str:  # noqa: D401
        return f"Leaf({self.label})"


@dataclass
class Internal:
    attr: str
    branches: dict[Any, DecisionNode]

    def __str__(self) -> str:
        inner = ", ".join(f"{k}: {v}" for k, v in self.branches.items())
        return f"Split({self.attr}| {inner})"


DecisionNode = Internal | Leaf


def _majority_label(series: pd.Series):
    vc = series.value_counts()
    if len(vc) == 0:
        raise ValueError("empty node")
    mx = vc.max()
    # hòa chọn nhãn từ điển âm học nhỏ nhất để ổn định
    candidates = [k for k, v in vc.items() if v == mx]
    return sorted(candidates, key=lambda x: str(x))[0]


def fit(
    df: pd.DataFrame,
    features: list[str],
    target: str,
    criterion: ImpurityFn,
) -> DecisionNode:
    labels = df[target].tolist()
    if df.empty:
        raise ValueError("empty dataframe")

    pure = len(set(labels)) <= 1
    if pure:
        return Leaf(labels[0])

    feats = [f for f in features if f in df.columns]
    if not feats:
        return Leaf(_majority_label(df[target]))

    candidates: list[tuple[float, float, float, str]] = []
    for f in feats:
        ip_parent, weighted, gn = gain(df, f, target, criterion)
        candidates.append((gn, weighted, ip_parent, f))

    # Gain lớn nhất; nếu hòa: entropy có trọng số nhỏ hơn; rồi tên thuộc tính âm học
    candidates.sort(key=lambda row: (-row[0], row[1], str(row[-1])))
    best_attr = candidates[0][-1]

    branches: dict[Any, DecisionNode] = {}
    feats_left = [x for x in feats if x != best_attr]
    vals = sorted(df[best_attr].unique(), key=lambda x: str(x))
    for v in vals:
        sub = df[df[best_attr] == v]
        if len(sub) == 0:
            continue
        branches[v] = fit(sub.copy(), feats_left, target, criterion)

    if not branches:
        return Leaf(_majority_label(df[target]))

    return Internal(best_attr, branches)


def predict_one(node: DecisionNode, row: pd.Series) -> Any:
    if isinstance(node, Leaf):
        return node.label
    val = row[node.attr]
    if val not in node.branches:
        raise KeyError(f"Không có nhánh '{val}' tại nút '{node.attr}'")
    return predict_one(node.branches[val], row)


def print_tree(node: DecisionNode, indent: int = 0) -> None:
    pad = "  " * indent
    if isinstance(node, Leaf):
        print(f"{pad}Leaf -> {node.label}")
    else:
        print(f"{pad}if {node.attr}:")
        for k, child in sorted(node.branches.items(), key=lambda x: str(x[0])):
            print(f"{pad}  = {k}:")
            print_tree(child, indent + 2)
