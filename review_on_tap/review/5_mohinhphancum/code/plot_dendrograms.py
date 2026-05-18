"""Vẽ dendrogram (single linkage) cho Câu 5.2 — lưu PDF vào latex/figures."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import pdist

HERE = Path(__file__).resolve().parent
FIG_DIR = HERE.parent / "latex" / "figures"


def save_dendrogram(X: np.ndarray, labels: list[str], title: str, fname: str) -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    Z = linkage(pdist(X, metric="euclidean"), method="single")
    plt.rcParams.update({"font.size": 11})
    fig, ax = plt.subplots(figsize=(6.2, 3.4))
    dendrogram(Z, labels=labels, ax=ax)
    ax.set_title(title)
    ax.set_ylabel("Khoảng cách (single linkage)")
    fig.tight_layout()
    out = FIG_DIR / fname
    fig.savefig(out, format="pdf", bbox_inches="tight")
    plt.close(fig)
    print(f"Đã lưu {out}")


def main() -> None:
    X_abc = np.array([[1.0, 1.0], [1.5, 1.5], [5.0, 5.0]], dtype=float)
    save_dendrogram(
        X_abc,
        ["A", "B", "C"],
        "Dendrogram — Euclidean, single linkage (A, B, C)",
        "fig_dendrogram_abc.pdf",
    )

    X_def = np.array([[3.0, 4.0], [4.0, 4.0], [3.0, 3.5]], dtype=float)
    save_dendrogram(
        X_def,
        ["D", "E", "F"],
        "Dendrogram — Euclidean, single linkage (D, E, F)",
        "fig_dendrogram_def.pdf",
    )


if __name__ == "__main__":
    main()
