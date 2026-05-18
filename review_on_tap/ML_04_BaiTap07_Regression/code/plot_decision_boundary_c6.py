"""Câu 6: vẽ điểm A–D và đường ranh giới 2x₁ - x₂ + 1 = 0 → x₂ = 2x₁ + 1."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "latex" / "figures" / "cau6_boundary.pdf"


def main() -> None:
    pts = {
        "A": (1, 1),
        "B": (2, 1),
        "C": (1, 3),
        "D": (4, 2),
    }
    fig, ax = plt.subplots(figsize=(5, 4), dpi=120)
    for name, (x1, x2) in pts.items():
        ax.scatter([x1], [x2], s=80, zorder=3)
        ax.annotate(name, (x1, x2), textcoords="offset points", xytext=(5, 5), fontsize=11)

    x1 = np.linspace(-0.2, 4.5, 200)
    x2 = 2 * x1 + 1
    ax.plot(x1, x2, "k-", lw=1.5, label=r"$2x_1 - x_2 + 1 = 0$")

    ax.set_xlabel(r"$x_1$")
    ax.set_ylabel(r"$x_2$")
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(loc="upper left")
    ax.set_title("Câu 6 — Phân lớp tuyến tính")
    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, bbox_inches="tight")
    plt.close(fig)
    print("Đã lưu", OUT)


if __name__ == "__main__":
    main()
