"""
Kiểm tra số cho Câu 2.1 & 2.2 (tiền xử lý dữ liệu).
Chạy từ bất kỳ đâu: python path/to/verify_exercises.py
"""

from __future__ import annotations

import statistics
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Thư mục chứa hình cho LaTeX
_ROOT = Path(__file__).resolve().parent.parent
FIG_DIR = _ROOT / "latex" / "figures"
BOX_PNG = FIG_DIR / "boxplot_tuoi.png"

AGES = [
    13, 15, 16, 16, 19, 20, 20, 21, 22, 22, 25, 25, 25, 25, 30, 33, 33,
    35, 35, 35, 35, 36, 40, 45, 46, 52, 70,
]

COLS = ("A", "B", "C", "D", "E")
V = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5}
W1 = {"A": 100, "B": 200, "C": 300, "D": 400, "E": 500}
W2 = {"A": 10, "B": 11, "C": 12, "D": 13, "E": 14}
W3 = {"A": 8, "B": 13, "C": 45, "D": 6, "E": 7}
W4 = {"A": 1, "B": 4, "C": 9, "D": 16, "E": 25}
W5 = {"A": -10, "B": -8, "C": -6, "D": -4, "E": -2}
W6 = {"A": 3, "B": 6, "C": 9, "D": 12, "E": 15}
ALL_W = {"W1": W1, "W2": W2, "W3": W3, "W4": W4, "W5": W5, "W6": W6}


def part_2_1a() -> None:
    x = AGES
    n = len(x)
    mean = sum(x) / n
    med = float(statistics.median(x))
    cnt = Counter(x)
    mcount = max(cnt.values())
    modes = sorted(k for k, v in cnt.items() if v == mcount)
    print("=== Câu 2.1 (a) ===")
    print(f"n = {n}, tổng = {sum(x)}")
    print(f"Trung bình: {mean} (≈ {round(mean, 2)})")
    print(f"Trung vị: {med}")
    print(f"Mốt (tần số {mcount}): {modes}")
    print()


def part_2_1b() -> None:
    a = np.array(AGES, dtype=float)
    n = len(a)
    q1_lin = float(np.quantile(a, 0.25, method="linear"))
    q3_lin = float(np.quantile(a, 0.75, method="linear"))
    p1 = (n + 1) / 4
    p3 = 3 * (n + 1) / 4
    q1_idx = int(p1)
    q3_idx = int(p3)
    q1_pos = float(a[q1_idx - 1])
    q3_pos = float(a[q3_idx - 1])
    print("=== Câu 2.1 (b) ===")
    print(f"Vị trí (n+1)/4 = {p1}, 3(n+1)/4 = {p3} (1-based)")
    print(f"Q1, Q3 theo vị trí nguyên (lấy phần tử thứ 7 và 21): Q1 = {q1_pos}, Q3 = {q3_pos}, IQR = {q3_pos - q1_pos}")
    print(f"Q1, Q3 nội suy tuyến tính (numpy linear): Q1 = {q1_lin}, Q3 = {q3_lin}, IQR = {q3_lin - q1_lin}")
    print()


def part_2_1c() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(4.5, 5))
    ax.boxplot(AGES, vert=True, whis=1.5, tick_labels=["Tuổi"])
    ax.set_ylabel("Tuổi")
    ax.set_title("Boxplot — tuổi (Câu 2.1)")
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(BOX_PNG, dpi=150)
    plt.close(fig)
    a = np.array(AGES, dtype=float)
    print("=== Câu 2.1 (c) ===")
    print(f"Đã lưu hình: {BOX_PNG}")
    print(
        f"min={a.min()}, max={a.max()}, mean={a.mean():.6f}, median={np.median(a)}"
    )
    print()


def _equal_frequency_index_bins(k: int = 4) -> list[tuple[int, int]]:
    """Chia dãy đã sắp thành k nhóm: n=27 → 7+7+7+6."""
    n = len(AGES)
    base = n // k
    rem = n % k
    cuts: list[tuple[int, int]] = []
    start = 0
    for i in range(k):
        sz = base + (1 if i < rem else 0)
        cuts.append((start, start + sz))
        start += sz
    return cuts


def part_2_1d() -> None:
    mn, mx = min(AGES), max(AGES)
    width = (mx - mn) / 4
    edges = [mn + i * width for i in range(5)]
    s = pd.Series(AGES, name="age")
    s_ew = pd.cut(s, bins=edges, include_lowest=True, right=True)
    s_ef = pd.qcut(s, 4, duplicates="drop")
    print("=== Câu 2.1 (d) ===")
    print(f"Chia độ rộng đều: bước w = {(mx - mn) / 4}, cận {[round(e, 2) for e in edges]}")
    print(s_ew.value_counts().sort_index())
    print("pd.qcut (equal-frequency quantiles):")
    print(s_ef.value_counts().sort_index())
    print("Chia tần số đều theo chỉ số trên dãy đã sắp (7+7+7+6):")
    for j, (lo, hi) in enumerate(_equal_frequency_index_bins(4)):
        chunk = AGES[lo:hi]
        print(f"  Nhóm {j + 1} [{lo}:{hi}]: {chunk} — n={len(chunk)}")
    print()


def _is_affine_positive(vmap: dict[str, int], wmap: dict[str, int]) -> bool:
    c0, c1 = COLS[0], COLS[1]
    v0, w0 = vmap[c0], wmap[c0]
    v1, w1_ = vmap[c1], wmap[c1]
    if v0 == v1:
        return False
    a = (w1_ - w0) / (v1 - v0)
    if a <= 0:
        return False
    b = w0 - a * v0
    return all(abs(wmap[c] - (a * vmap[c] + b)) < 1e-9 for c in COLS)


def part_2_2() -> None:
    print("=== Câu 2.2 ===")
    for c in COLS:
        assert W1[c] == 100 * V[c]
        assert W2[c] == V[c] + 9
        assert W4[c] == V[c] ** 2
        assert W5[c] == 2 * V[c] - 12
        assert W6[c] == 3 * V[c]
    print("Đối chiếu công thức V→W (W3 không affine): OK")
    interval_same = []
    for name, wmap in ALL_W.items():
        ok = _is_affine_positive(V, wmap)
        print(f"{name}: cùng thang khoảng với V (tồn tại W=aV+b, a>0)? {ok}")
        if ok:
            interval_same.append(name)
    print(f"Cùng thang khoảng: {', '.join(interval_same)}")
    print()


def main() -> None:
    part_2_1a()
    part_2_1b()
    part_2_1c()
    part_2_1d()
    part_2_2()


if __name__ == "__main__":
    main()
