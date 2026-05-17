#!/usr/bin/env python3
"""Vẽ scatter nhiệt độ--độ ẩm (Câu 2), lưu PDF cho LaTeX."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

from datasets import Q2_ROWS, Q2_TEST_B

HERE = Path(__file__).resolve().parent
FIG_DIR = HERE.parent / "latex" / "figures"


def main() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    xs_yes, ys_yes, xs_no, ys_no = [], [], [], []
    for r in Q2_ROWS:
        if str(r["Play"]).lower() == "yes":
            xs_yes.append(r["Temperature"])
            ys_yes.append(r["Humidity"])
        else:
            xs_no.append(r["Temperature"])
            ys_no.append(r["Humidity"])

    plt.figure(figsize=(6, 4.5))
    plt.scatter(xs_yes, ys_yes, marker="o", s=55, label="play = yes", zorder=2)
    plt.scatter(xs_no, ys_no, marker="s", s=55, label="play = no", zorder=2)
    tx, ty = Q2_TEST_B["Temperature"], Q2_TEST_B["Humidity"]
    plt.scatter([tx], [ty], marker="*", s=220, c="crimson", edgecolors="black", linewidths=0.8, label="mẫu (b)", zorder=3)
    plt.xlabel("Temperature ($^\\circ$F)")
    plt.ylabel("Humidity (\\%)")
    plt.title("Câu 2 --- tennis (số), mẫu kiểm tra đánh dấu sao")
    plt.legend(loc="upper right", fontsize=9)
    plt.grid(True, alpha=0.3)
    out = FIG_DIR / "q2_temp_humidity_scatter.pdf"
    plt.tight_layout()
    plt.savefig(out, format="pdf")
    plt.close()
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
