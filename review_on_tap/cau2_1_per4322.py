"""
PER-4322 — Câu 2.1: tập dữ liệu thuộc tính tuổi (n = 27, đã sắp tăng dần).

Giải tay (thi trên giấy): `README.md` cùng thư mục.
Chạy: python cau2_1_per4322.py — in (a)–(d) và lưu boxplot để đối chiếu.
"""

from __future__ import annotations

import statistics
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Đúng theo đề
AGES = [
    13, 15, 16, 16, 19, 20, 20, 21, 22, 22, 25, 25, 25, 25, 30, 33, 33,
    35, 35, 35, 35, 36, 40, 45, 46, 52, 70,
]

OUT_PNG = Path(__file__).resolve().parent / "boxplot_tuoi_cau2_1.png"


def part_a() -> None:
    x = AGES
    n = len(x)
    mean = sum(x) / n
    median = float(statistics.median(x))
    cnt = Counter(x)
    mcount = max(cnt.values())
    modes = sorted(k for k, v in cnt.items() if v == mcount)
    print("a) Thống kê cơ bản")
    print(f"   n = {n}, tổng = {sum(x)}")
    print(f"   Trung bình: {mean:.6f} (≈ {round(mean, 2)})")
    print(f"   Trung vị: {median}")
    print(
        f"   Mode: {', '.join(str(m) for m in modes)} "
        f"(mỗi giá trị lặp {mcount} lần — tập dữ liệu có hai mode)"
    )


def part_b() -> None:
    """Q1, Q3: n = 27 lẻ; dùng tứ phân vị theo cách bài giải phổ biến (p = (i)/(n+1) hoặc nối tuyến tính)."""
    a = np.array(AGES, dtype=float)
    n = len(a)
    # Nối tuyến tính (gần với hàm quantile/percentile mặc định)
    q1_np = float(np.quantile(a, 0.25, method="linear"))
    q3_np = float(np.quantile(a, 0.75, method="linear"))
    # Vị trí theo công thức 1-based: (n+1)/4, 3(n+1)/4 — lấy yếu tố ở vị trí 7, 21
    p7 = 7
    p21 = 21
    q1_pos = a[p7 - 1]
    q3_pos = a[p21 - 1]
    print("b) Tứ phân vị")
    print(
        f"   Cách nối tuyến tính (xấp xỉ theo bảng tần số: Q1, Q3): Q1 = {q1_np}, Q3 = {q3_np}"
    )
    print(
        f"   Cách theo vị trí 7 & 21 trên tập sắp tăng (1-based): Q1 = {q1_pos}, Q3 = {q3_pos} "
        "(có tài liệu dùng; đề hợp: xấp xỉ if needed — xem cả nối tuyến 20.5, 35)"
    )
    iqr = q3_np - q1_np
    print(f"   IQR = Q3 − Q1 = {iqr} (dùng bộ nối tuyến tính)")


def part_c() -> None:
    print("c) Hộp (boxplot) và nhận xét nhanh")
    print("   Lưu hình: ", OUT_PNG, "(chạy script trong thư mục review_on_tap/)")
    fig, ax = plt.subplots(figsize=(4, 5))
    ax.boxplot(AGES, vert=True, whis=1.5, tick_labels=["Tuổi"])
    ax.set_ylabel("Tuổi")
    ax.set_title("Boxplot – Câu 2.1 (PER-4322)")
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close()
    a = np.array(AGES, dtype=float)
    mean = a.mean()
    med = float(np.median(a))
    print("   Nhận xét: mean ≈", round(mean, 2), "> median =", med, "→ lệch phải;")
    print(
        "   giá trị 70 cao bất thường (lớn hơn Q3 + 1,5*IQR nếu tính IQR theo tứ phân vị tuyến tính), "
        "đuôi dài về phía lớn."
    )


def part_d() -> None:
    s = pd.Series(AGES, name="age")
    mn, mx = s.min(), s.max()
    width = (mx - mn) / 4
    edges = [mn + i * width for i in range(5)]
    s_ew = pd.cut(
        s,
        bins=edges,
        include_lowest=True,
        right=True,
    )
    s_ef = pd.qcut(s, 4, duplicates="drop")
    print("d) Rời rạc hóa với k = 4")
    print(
        f"   Chia đều (equal-width), đoạn: [{edges[0]:.2f}, {edges[1]:.2f}), "
        f"[{edges[1]:.2f}, {edges[2]:.2f}), "
        f"[{edges[2]:.2f}, {edges[3]:.2f}), "
        f"[{edges[3]:.2f}, {edges[4]:.2f}]"
    )
    print("   Số mẫu từng khoảng (equal-width):")
    print(s_ew.value_counts().sort_index().to_string())
    print("   Số mẫu từng lớp (equal-frequency):")
    print(s_ef.value_counts().sort_index().to_string())


if __name__ == "__main__":
    part_a()
    part_b()
    part_c()
    part_d()
