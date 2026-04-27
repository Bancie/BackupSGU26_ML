"""
PER-4332 — Câu 2.2: thang đo Stevens & đối chiếu W1..W6 với V.

Sub-issues: PER-4333 … PER-4339 (từng W & thang đo V).
Giải tay: `README_cau2_2.md`
Chạy: python cau2_2_per4332.py
"""

from __future__ import annotations

from dataclasses import dataclass

# Cột A … E — giá trị theo đề (screenshot Câu 2.2)
COLS = ("A", "B", "C", "D", "E")
V = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5}
W1 = {"A": 100, "B": 200, "C": 300, "D": 400, "E": 500}
W2 = {"A": 10, "B": 11, "C": 12, "D": 13, "E": 14}
W3 = {"A": 8, "B": 13, "C": 45, "D": 6, "E": 7}
W4 = {"A": 1, "B": 4, "C": 9, "D": 16, "E": 25}
W5 = {"A": -10, "B": -8, "C": -6, "D": -4, "E": -2}
W6 = {"A": 3, "B": 6, "C": 9, "D": 12, "E": 15}

ALL_W = {"W1": W1, "W2": W2, "W3": W3, "W4": W4, "W5": W5, "W6": W6}


def verify_formulas() -> None:
    """Kiểm tra mối quan hệ đại số V → W (giải tay đã thấy)."""
    for c in COLS:
        v = V[c]
        assert W1[c] == 100 * v
        assert W2[c] == v + 9
        assert W4[c] == v * v
        assert W5[c] == 2 * v - 12
        assert W6[c] == 3 * v
    print("OK: W1=100·V, W2=V+9, W4=V², W5=2V−12, W6=3V (mọi cột).")
    print("W3 không khớp một công thức đơn giản & thứ tự trên dãy W3 ≠ thứ tự V.\n")


def w_order(name: str) -> list[int]:
    return [ALL_W[name][c] for c in COLS]


def is_strictly_monotonic_same_order_as_v(wname: str) -> bool:
    """Cùng thứ tự tăng trên A…E như V hay không."""
    seq = w_order(wname)
    return all(seq[i] < seq[i + 1] for i in range(len(seq) - 1))


def is_affine_positive(vmap: dict[str, int], wmap: dict[str, int]) -> bool:
    """Tồn tại a>0, b: w = a·v + b mọi cột?"""
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


@dataclass(frozen=True)
class IntervalSame:
    """Cùng thang khoảng (interval) với V: ánh xạ afin tăng W = aV+b, a>0."""

    same_interval: bool
    same_ordinal: bool
    same_ratio: bool
    note: str


def analyze(name: str) -> IntervalSame:
    wmap = ALL_W[name]
    aff = is_affine_positive(V, wmap)
    mono = is_strictly_monotonic_same_order_as_v(name)
    # Tỷ lệ (ratio) — phép tương đương thường dạng w = a·v (a>0), qua gốc
    if aff:
        c0 = COLS[0]
        a = (wmap[COLS[1]] - wmap[c0]) / (V[COLS[1]] - V[c0])
        b = wmap[c0] - a * V[c0]
        ratio = abs(b) < 1e-9
    else:
        ratio = False
    n = f"{name}: thứ tự cùng V={mono} | afin tăng W=aV+b={aff} | dạng thuần tỷ lệ aV={ratio}"
    return IntervalSame(
        same_interval=aff,
        same_ordinal=mono,
        same_ratio=ratio,
        note=n,
    )


def part_per_4333() -> None:
    print("=" * 60)
    print("PER-4333 — Thang đo của V(.) (Stevens: định danh / thứ tự / khoảng / tỷ lệ)")
    print("=" * 60)
    print(
        "V lấy 1,2,3,4,5: có thứ tự, khoảng cách từng bước bằng 1, không có 0; "
        "về lý thuyết đo: (1) không chỉ tên, (2) nhiều hơn tên, (3) thường dùng cho "
        "mã cách đều — thang khoảng, (4) tỷ lệ cần gốc 0 tuyệt đối — không mô tả ở đây."
    )
    print("Kết luận đáp án ôn: V theo bảng là thang (3) khoảng (interval) — thang tỷ lệ (4) không phù hợp (không phải số 0 tỷ lệ).")
    print()


def part_comparisons() -> None:
    print("=" * 60)
    print("PER-4334–PER-4339 — Đối chiếu từng W với cùng thang khoảng như V")
    print("=" * 60)
    print("Trên thang khoảng: phép tương đương cho phép là ánh xạ afin tăng f(v)=a·v+b, a>0.\n")
    for name in ("W1", "W2", "W3", "W4", "W5", "W6"):
        a = analyze(name)
        per = f"PER-{4333 + int(name[1])}"
        same = "CÙNG thang khoảng (interval) với V" if a.same_interval else "KHÔNG cùng thang khoảng với V"
        print(f"{per} {name} — {same}")
        print(f"  {a.note}")
        if name == "W1":
            print("  Công thức: W1 = 100·V  (a=100, b=0) → afin, a>0.")
        elif name == "W2":
            print("  Công thức: W2 = V + 9  (a=1, b=9) → afin, a>0.")
        elif name == "W3":
            print("  Dãy W3: 8,13,45,6,7 — thứ tự không tăng dần cùng V; không tồn tại afin W=aV+b.")
        elif name == "W4":
            print("  Công thức: W4 = V² — không afin; không cùng thang khoảng (ví dụ hiệu không bảo 2 lần hiệu trên khoảng V).")
        elif name == "W5":
            print("  Công thức: W5 = 2V − 12  (a=2, b=−12) → afin, a>0.")
        elif name == "W6":
            print("  Công thức: W6 = 3·V  (a=3, b=0) → afin, a>0.")
        print()


def ordinal_note() -> None:
    print("=" * 60)
    print("Ghi chú: nếu thầy dạy V là thang THỨ TỰ (ordinal), phép cho phép = đơn điệu tăng;")
    print("  cùng thứ tự với V: W1, W2, W4, W5, W6 — KHÔNG: W3.")
    print("=" * 60)


if __name__ == "__main__":
    verify_formulas()
    part_per_4333()
    part_comparisons()
    ordinal_note()
