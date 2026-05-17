#!/usr/bin/env python3
"""Câu 4 — scatter điểm + centroid + test; lưu PDF cho LaTeX."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

from datasets import Q4_TEST, Q4_X, Q4_Y
from similarity import nearest_centroid_predict

HERE = Path(__file__).resolve().parent
FIG_DIR = HERE.parent / "latex" / "figures"


def main() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    pred, centroids, _ = nearest_centroid_predict(Q4_X, Q4_Y, Q4_TEST)

    xa, ya, xb, yb = [], [], [], []
    for i, lab in enumerate(Q4_Y):
        if lab == "A":
            xa.append(Q4_X[i, 0])
            ya.append(Q4_X[i, 1])
        else:
            xb.append(Q4_X[i, 0])
            yb.append(Q4_X[i, 1])

    plt.figure(figsize=(6, 4.5))
    plt.scatter(xa, ya, marker="o", s=70, label="lớp A", zorder=2)
    plt.scatter(xb, yb, marker="s", s=70, label="lớp B", zorder=2)
    ca = centroids["A"]
    cb = centroids["B"]
    plt.scatter([ca[0]], [ca[1]], marker="*", s=280, c="darkgreen", edgecolors="black", linewidths=0.6, label="centroid A", zorder=4)
    plt.scatter([cb[0]], [cb[1]], marker="*", s=280, c="darkorange", edgecolors="black", linewidths=0.6, label="centroid B", zorder=4)
    plt.scatter([Q4_TEST[0]], [Q4_TEST[1]], marker="P", s=160, c="crimson", edgecolors="black", linewidths=0.6, label=f"test ({Q4_TEST[0]:g},{Q4_TEST[1]:g}) → {pred}", zorder=3)
    plt.xlabel("$x$")
    plt.ylabel("$y$")
    plt.title("Câu 4 — Nearest centroid")
    plt.legend(loc="upper left", fontsize=8)
    plt.grid(True, alpha=0.3)
    plt.axis("equal")
    out = FIG_DIR / "q4_centroids.pdf"
    plt.tight_layout()
    plt.savefig(out, format="pdf")
    plt.close()
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
