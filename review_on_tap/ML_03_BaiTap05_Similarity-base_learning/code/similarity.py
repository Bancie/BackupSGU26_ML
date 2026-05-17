"""Khoảng cách, k-NN, centroid, LWR (WLS) — PER-4784."""

from __future__ import annotations

from collections import Counter
from typing import Any

import numpy as np

EPS = 1e-12


def euclidean(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.linalg.norm(a - b))


def hamming(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.sum(np.abs(a.astype(int) - b.astype(int))))


def minmax_fit_transform(train: np.ndarray, test: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Min–Max theo từng cột chỉ từ train; áp cùng min,max cho train và test."""
    tmin = train.min(axis=0)
    tmax = train.max(axis=0)
    denom = np.where((tmax - tmin) < EPS, 1.0, tmax - tmin)

    def _tr(x: np.ndarray) -> np.ndarray:
        return (x - tmin) / denom

    return _tr(train), _tr(test)


def knn_predict(
    X: np.ndarray,
    y: np.ndarray,
    x_query: np.ndarray,
    k: int,
    dist_fn=euclidean,
) -> tuple[str, list[tuple[int, float, Any]]]:
    """
    Trả về nhãn dự đoán (đa số) và danh sách (index, khoảng cách, nhãn) đã sort.
    Hòa: chọn nhãn nhỏ hơn theo thứ tự lex để ổn định.
    """
    dists = [(i, dist_fn(X[i], x_query), y[i]) for i in range(len(X))]
    dists.sort(key=lambda t: (t[1], str(t[2])))
    neigh = dists[:k]
    votes = Counter(n[2] for n in neigh)
    best = sorted(votes.items(), key=lambda kv: (-kv[1], str(kv[0])))[0][0]
    return best, dists


def weighted_knn_predict(
    X: np.ndarray,
    y: np.ndarray,
    x_query: np.ndarray,
    k: int,
    dist_fn=euclidean,
    inverse_power: int = 1,
) -> tuple[str, list[tuple[int, float, float, Any]]]:
    """
    w_i ∝ 1 / d_i^p (dùng max(d, EPS)); chuẩn hóa; dự đoán lớp có tổng w' lớn nhất.
    Trả về (label, [(idx, d, w_norm, class), ...]) cho k láng giềng gần nhất.
    """
    dists = [(i, dist_fn(X[i], x_query), y[i]) for i in range(len(X))]
    dists.sort(key=lambda t: (t[1], str(t[2])))
    neigh = dists[:k]
    raw = []
    for i, d, lab in neigh:
        de = max(d, EPS)
        raw.append((i, d, (1.0 / de) ** inverse_power, lab))
    s = sum(w for _, _, w, _ in raw) + EPS
    triples = [(i, d, w / s, lab) for i, d, w, lab in raw]
    agg: dict[Any, float] = {}
    for _, _, wn, lab in triples:
        agg[lab] = agg.get(lab, 0.0) + wn
    pred = sorted(agg.items(), key=lambda kv: (-kv[1], str(kv[0])))[0][0]
    return pred, triples


def nearest_centroid_predict(
    X: np.ndarray, y: np.ndarray, x_query: np.ndarray
) -> tuple[str, dict[Any, np.ndarray], dict[Any, float]]:
    labels = sorted(set(y.tolist()), key=str)
    centroids: dict[Any, np.ndarray] = {}
    for c in labels:
        mask = y == c
        centroids[c] = X[mask].mean(axis=0)
    dists = {c: euclidean(centroids[c], x_query) for c in labels}
    pred = sorted(dists.items(), key=lambda kv: (kv[1], str(kv[0])))[0][0]
    return pred, centroids, dists


def lwr_gaussian_weights(x_train: np.ndarray, x_query: float, tau: float) -> np.ndarray:
    """w_i = exp(-(x_i - x)^2 / (2 tau^2))."""
    d = x_train - x_query
    return np.exp(-(d * d) / (2.0 * tau * tau + EPS))


def lwr_linear_predict(x_train: np.ndarray, y_train: np.ndarray, x_query: float, weights: np.ndarray) -> float:
    """
    Hồi quy tuyến tính có trọng số: y ≈ beta0 + beta1 x.
    beta = (X' W X)^{-1} X' W y với X = [1, x]^T.
    """
    Xd = np.column_stack([np.ones(len(x_train)), x_train])
    W = np.diag(weights)
    xtw = Xd.T @ W
    a = xtw @ Xd
    b = xtw @ y_train
    beta = np.linalg.solve(a, b)
    return float(beta[0] + beta[1] * x_query)
