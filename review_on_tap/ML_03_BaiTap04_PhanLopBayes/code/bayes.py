"""Naive Bayes: categorical + Gaussian (hybrid) + multinomial — PER-4783."""

from __future__ import annotations

import math
from collections import defaultdict
from typing import Any

import numpy as np

EPS = 1e-9


def _log_gaussian_pdf(x: float, mu: float, sigma: float) -> float:
    s = max(sigma, EPS)
    return -0.5 * math.log(2 * math.pi * s * s) - ((x - mu) ** 2) / (2 * s * s)


class CategoricalNB:
    """Laplace alpha cho prior và likelihood; mỗi thuộc tính rời rạc."""

    def __init__(self, alpha: float = 1.0) -> None:
        self.alpha = float(alpha)
        self.classes_: list[Any] = []
        self.class_prior_log_: dict[Any, float] = {}
        # cond_log_prob[c][feat][value] = log P(value|c)
        self.cond_log_prob: dict[Any, dict[str, dict[Any, float]]] = {}
        self.feature_names: list[str] = []

    def fit(self, rows: list[dict[str, Any]], feature_cols: list[str], target: str) -> None:
        self.feature_names = list(feature_cols)
        y_all = [r[target] for r in rows]
        self.classes_ = sorted(set(y_all), key=lambda x: str(x))
        n_classes = len(self.classes_)

        counts_y = defaultdict(int)
        for y in y_all:
            counts_y[y] += 1

        denom_p = len(rows) + self.alpha * n_classes
        self.class_prior_log_ = {
            c: math.log((counts_y[c] + self.alpha) / denom_p) for c in self.classes_
        }

        self.cond_log_prob = {c: {} for c in self.classes_}
        for f in feature_cols:
            domain = sorted({r[f] for r in rows}, key=lambda x: str(x))
            V = len(domain)

            for c in self.classes_:
                sub = [r[f] for r in rows if r[target] == c]
                cnt = defaultdict(int)
                for v in sub:
                    cnt[v] += 1
                denom = len(sub) + self.alpha * V
                self.cond_log_prob[c][f] = {
                    v: math.log((cnt[v] + self.alpha) / denom) for v in domain
                }

    def predict_log_proba_dict(self, x: dict[str, Any], skip_features: set[str] | None = None) -> dict[Any, float]:
        skip = skip_features or set()
        scores: dict[Any, float] = {}
        for c in self.classes_:
            lp = self.class_prior_log_[c]
            for f in self.feature_names:
                if f in skip:
                    continue
                v = x[f]
                lp += self.cond_log_prob[c][f][v]
            scores[c] = lp
        return scores

    def predict_one(self, x: dict[str, Any], skip_features: set[str] | None = None) -> Any:
        scores = self.predict_log_proba_dict(x, skip_features)
        return max(scores, key=scores.get)


class GaussianHybridNB:
    """
    Outlook, Windy: categorical Laplace.
    Temperature, Humidity: Gaussian với mean và độ lệch chuẩn mẫu (ddof=1).
    """

    def __init__(self, alpha: float = 1.0) -> None:
        self.alpha = float(alpha)
        self.classes_: list[str] = []
        self.cat_cols: list[str] = ["Outlook", "Windy"]
        self.num_cols: list[str] = ["Temperature", "Humidity"]
        self._cat: CategoricalNB | None = None
        self._mu: dict[str, dict[str, float]] = {}
        self._sigma: dict[str, dict[str, float]] = {}

    def fit(self, rows: list[dict[str, Any]], target: str) -> None:
        # Chuẩn hóa nhãn yes/no
        norm_rows = []
        for r in rows:
            nr = dict(r)
            nr[target] = str(nr[target]).lower()
            norm_rows.append(nr)

        self.classes_ = sorted({str(r[target]).lower() for r in norm_rows})

        self._cat = CategoricalNB(alpha=self.alpha)
        self._cat.fit(norm_rows, self.cat_cols, target)

        for c in self.classes_:
            sub = [r for r in norm_rows if r[target] == c]
            self._mu[c] = {}
            self._sigma[c] = {}
            for f in self.num_cols:
                arr = np.array([r[f] for r in sub], dtype=float)
                if len(arr) == 0:
                    self._mu[c][f] = 0.0
                    self._sigma[c][f] = EPS
                elif len(arr) == 1:
                    self._mu[c][f] = float(arr[0])
                    self._sigma[c][f] = EPS
                else:
                    self._mu[c][f] = float(arr.mean())
                    self._sigma[c][f] = float(arr.std(ddof=1))

    def predict_log_scores(self, x: dict[str, Any], class_priors_log: dict[str, float]) -> dict[str, float]:
        assert self._cat is not None
        scores: dict[str, float] = {}
        xn = dict(x)
        for c in self.classes_:
            lp = class_priors_log[c]
            for f in self.cat_cols:
                lp += self._cat.cond_log_prob[c][f][xn[f]]
            for f in self.num_cols:
                lp += _log_gaussian_pdf(float(xn[f]), self._mu[c][f], self._sigma[c][f])
            scores[c] = lp
        return scores

    def predict_one(self, x: dict[str, Any], class_priors_log: dict[str, float]) -> str:
        s = self.predict_log_scores(x, class_priors_log)
        return max(s, key=s.get)


def compute_class_priors_log(rows: list[dict[str, Any]], target: str, classes: list[str], alpha: float = 1.0) -> dict[str, float]:
    n = len(rows)
    k = len(classes)
    counts = defaultdict(int)
    for r in rows:
        counts[str(r[target]).lower()] += 1
    denom = n + alpha * k
    return {c: math.log((counts[c] + alpha) / denom) for c in classes}


class MultinomialNBWords:
    """Multinomial với Laplace trên V từ vựng."""

    def __init__(self, alpha: float = 1.0) -> None:
        self.alpha = float(alpha)
        self.V = 0
        self.classes_: list[str] = []
        self.class_prior_log_: dict[str, float] = {}
        self.word_log_prob: dict[str, np.ndarray] = {}

    def fit(self, X: np.ndarray, y: list[str], n_classes_prior: int | None = None) -> None:
        # X: (n_docs, V) counts
        self.V = X.shape[1]
        self.classes_ = sorted(set(y))
        alpha_c = self.alpha
        counts_class = defaultdict(int)
        for lab in y:
            counts_class[lab] += 1
        n_c = len(self.classes_)
        denom_prior = len(y) + alpha_c * (n_classes_prior if n_classes_prior is not None else n_c)
        self.class_prior_log_ = {c: math.log((counts_class[c] + alpha_c) / denom_prior) for c in self.classes_}

        self.word_log_prob = {}
        for c in self.classes_:
            idx = [i for i, lab in enumerate(y) if lab == c]
            sub = X[idx].sum(axis=0).astype(float)
            tot = float(sub.sum())
            denom = tot + alpha_c * self.V
            probs = (sub + alpha_c) / denom
            self.word_log_prob[c] = np.log(probs)

    def predict_log_scores(self, counts: np.ndarray) -> dict[str, float]:
        return {
            c: self.class_prior_log_[c] + float(np.dot(counts.astype(float), self.word_log_prob[c]))
            for c in self.classes_
        }

    def predict_one(self, counts: np.ndarray) -> str:
        s = self.predict_log_scores(counts)
        return max(s, key=s.get)
