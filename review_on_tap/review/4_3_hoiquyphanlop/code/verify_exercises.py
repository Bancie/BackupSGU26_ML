"""
PER-4808 — Câu 4.3.1: mô hình sign(w^T x + b), hàm chi phí trên tập phân sai, một bước Perceptron.

Định nghĩa sign: +1 nếu z >= 0, -1 nếu z < 0.
Một mẫu phân lớp sai khi ŷ_k != t_k (tương đương t_k(w^T x_k + b) <= 0 với nhãn ±1).
"""

from __future__ import annotations

import numpy as np


def divider(title: str) -> None:
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)


def sign_de(z: float) -> float:
    return 1.0 if z >= 0 else -1.0


def q_4_3_1() -> None:
    X = np.array([[1, 1], [2, 1], [1, 2], [2, 2]], dtype=float)
    t = np.array([1.0, 1.0, -1.0, -1.0])
    w0 = np.array([1.0, 1.0])
    b0 = 0.0
    rho = 1.0

    print("Dữ liệu: (x_k, t_k) với t_k ∈ {-1, +1}")
    for k in range(len(X)):
        print(f"  mẫu {k + 1}: x = {X[k].tolist()}, t = {t[k]:g}")

    print(f"\nKhởi tạo: w^(0) = {w0.tolist()}, b^(0) = {b0:g}, ρ = {rho:g}")
    print("\n--- (a) Dự đoán và tập phân lớp sai ---")

    mis: list[int] = []
    for k in range(len(X)):
        s = float(w0 @ X[k] + b0)
        y_hat = sign_de(s)
        ok = y_hat == t[k]
        print(
            f"  mẫu{k + 1}: w^T x + b = {s:g} → ŷ = {y_hat:g}, t = {t[k]:g} → ",
            end="",
        )
        if ok:
            print("đúng")
        else:
            print("SAI")
            mis.append(k)

    print(f"\nTập chỉ số phân sai (0-based): {mis}")
    print("→ Theo thứ tự mẫu 1…4: tập sai Y = {mẫu 3, mẫu 4}.")

    print("\n--- (b) Đạo hàm của J trên tập sai ---")
    print("J(w,b) = Σ_{k∈Y} (-t_k)(w^T x_k + b)")
    print("∂J/∂w = Σ_{k∈Y} (-t_k) x_k ,  ∂J/∂b = Σ_{k∈Y} (-t_k)")

    g_w = np.zeros(2)
    g_b = 0.0
    for k in mis:
        g_w += (-t[k]) * X[k]
        g_b += -t[k]
    print(f"  ∂J/∂w = {g_w.tolist()}")
    print(f"  ∂J/∂b = {g_b:g}")

    print("\n--- (c) Một bước Perceptron (Rosenblatt), mẫu sai đầu tiên ---")
    print("Cập nhật: w ← w + ρ t_k x_k , b ← b + ρ t_k khi xét mẫu k bị sai.")

    k0 = mis[0]
    w1 = w0 + rho * t[k0] * X[k0]
    b1 = b0 + rho * t[k0]
    print(f"  Mẫu sai đầu tiên: k = {k0 + 1}, x = {X[k0].tolist()}, t = {t[k0]:g}")
    print(f"  w^(1) = {w1.tolist()}, b^(1) = {b1:g}")
    print(f"  Đường ranh giới w^(1)^T x + b^(1) = 0: {w1[0]:g} x₁ + {w1[1]:g} x₂ + ({b1:g}) = 0")

    print("\n--- Tham chiếu: một bước hạ gradient của J với η=1 (khác với PLA một mẫu) ---")
    w_gd = w0 - 1.0 * g_w
    b_gd = b0 - 1.0 * g_b
    print(f"  w ← w - η ∂J/∂w = {w_gd.tolist()}, b ← b - η ∂J/∂b = {b_gd:g}")
    print("  (Biến thể trên chỉ để đối chiếu — phần (c) là một bước Perceptron một mẫu như trên.)")


def main() -> None:
    divider("Câu 4.3.1 — Hồi quy phân lớp (sign), J trên tập sai, Perceptron")
    q_4_3_1()


if __name__ == "__main__":
    main()
