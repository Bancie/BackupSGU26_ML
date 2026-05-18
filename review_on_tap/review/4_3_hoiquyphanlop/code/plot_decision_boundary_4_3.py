"""Câu 4.3.1: điểm dữ liệu và đường ranh giới w^T x + b = 0 (trước và sau một bước Perceptron)."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "latex" / "figures" / "cau4_3_boundary.pdf"


def main() -> None:
    X = np.array([[1, 1], [2, 1], [1, 2], [2, 2]], dtype=float)
    t = np.array([1.0, 1.0, -1.0, -1.0])

    fig, ax = plt.subplots(figsize=(5.2, 4.2), dpi=120)
    pos = t > 0
    ax.scatter(X[pos, 0], X[pos, 1], s=90, zorder=3, label=r"$t=+1$", marker="o")
    ax.scatter(X[~pos, 0], X[~pos, 1], s=90, zorder=3, label=r"$t=-1$", marker="s")
    for k in range(len(X)):
        ax.annotate(str(k + 1), (X[k, 0], X[k, 1]), textcoords="offset points", xytext=(6, 4), fontsize=10)

    x1 = np.linspace(-0.3, 2.7, 200)
    # w=(1,1), b=0  →  x2 = -x1
    ax.plot(x1, -x1, "k--", lw=1.4, label=r"$w^{(0)\top}x+b^{(0)}=0$ ($x_1+x_2=0$)")

    # w=(0,-1), b=-1  →  -x2 - 1 = 0  →  x2 = -1
    ax.axhline(-1.0, color="C0", lw=1.5, label=r"$w^{(1)\top}x+b^{(1)}=0$ ($x_2=-1$)")

    ax.set_xlabel(r"$x_1$")
    ax.set_ylabel(r"$x_2$")
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(loc="upper left", fontsize=8)
    ax.set_title("Câu 4.3.1 — Ranh giới trước và sau một bước Perceptron")
    ax.set_xlim(-0.35, 2.6)
    ax.set_ylim(-1.55, 2.6)
    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, bbox_inches="tight")
    plt.close(fig)
    print("Đã lưu", OUT)


if __name__ == "__main__":
    main()
