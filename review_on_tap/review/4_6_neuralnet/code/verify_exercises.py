"""
PER-4811 — Bài 4.6 Mô hình Neural Network: đối chiếu số với đề (screenshot Linear).

Phạm vi: Câu 4.6.1–4.6.5 (perceptron, OR batch GD, MLP nhỏ, hồi quy tuyến tính + GD).
"""

from __future__ import annotations

import numpy as np


def divider(title: str) -> None:
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def tau_sign(s: float) -> int:
    return 1 if s >= 0 else -1


def q_4_6_1() -> None:
    """Đường biên: x2 = -1,5 x1 + 3  <=>  1,5 x1 + x2 - 3 = 0."""
    divider("Câu 4.6.1 — Perceptron, đường biên x2 = -1,5 x1 + 3")
    w = np.array([1.5, 1.0])
    b = -3.0
    print("Một bộ tham số (trong khuôn khổ w^T x + b = 0):")
    print(f"  w = ({w[0]:g}, {w[1]:g})^T,  b = {b:g}")
    print("Nhân 2: w = (3, 2)^T, b = -6 — cùng đường thẳng.")
    print("Đầu ra y = τ(w^T x + b) với τ(s)=+1 nếu s≥0, -1 nếu s<0.")


def q_4_6_2() -> None:
    divider("Câu 4.6.2 — Perceptron (trọng số bias -3, x1: 2, x2: 1)")
    b = -3.0
    w = np.array([2.0, 1.0])
    print("(a) Đường biên: 2x1 + x2 - 3 = 0.")

    x1 = np.array([-1.0, 2.0])
    x2 = np.array([0.0, 0.0])
    for i in range(2):
        s = w[0] * x1[i] + w[1] * x2[i] + b
        y = tau_sign(float(s))
        print(f"(b) x^({i + 1})=({x1[i]:g},{x2[i]:g}): s = {s:g}  →  y = {y:+d}")

    print(
        "(c) Đường qua (2,0) và (0,-1): x1 - 2x2 - 2 = 0 "
        "→ hệ số chặn (đầu vào 1) = -2, w1 = 1, w2 = -2."
    )
    w_or = np.array([1.0, 1.0])
    b_or = -0.5
    print("(d) OR: w0=-0,5, w1=1, w2=1 (s = -0,5 + x1 + x2).")
    for x1v, x2v, name in [(0, 0, "(0,0)"), (1, 0, "(1,0)"), (0, 1, "(0,1)"), (1, 1, "(1,1)")]:
        s = b_or + w_or[0] * x1v + w_or[1] * x2v
        print(f"    {name}: s = {s:g}  →  y = {tau_sign(s):+d}")
    w_and = np.array([1.0, 1.0])
    b_and = -1.5
    print("(d) AND: w0=-1,5, w1=1, w2=1 (s = -1,5 + x1 + x2).")
    for x1v, x2v, name in [(0, 0, "(0,0)"), (1, 0, "(1,0)"), (0, 1, "(0,1)"), (1, 1, "(1,1)")]:
        s = b_and + w_and[0] * x1v + w_and[1] * x2v
        print(f"    {name}: s = {s:g}  →  y = {tau_sign(s):+d}")


def q_4_6_3_or_table() -> None:
    divider("Câu 4.6.3 — Bảng OR: (0,0) nhãn -1, còn lại +1")
    X = np.array([(0, 0), (1, 0), (0, 1), (1, 1)], dtype=float)
    t = np.array([-1.0, 1.0, 1.0, 1.0])
    w_or = np.array([1.0, 1.0])
    b_or = -0.5
    for i, (x, tv) in enumerate(zip(X, t, strict=True)):
        s = b_or + w_or @ x
        y = tau_sign(float(s))
        ok = "OK" if y == int(tv) else "XX"
        print(f"  mẫu {i}: x=({int(x[0])},{int(x[1])}), t={int(tv):+d}, s={s:g}, y={y:+d} {ok}")


def perceptron_batch_gd_misclass_loss() -> None:
    divider("Câu 4.6.3 — GD batch OR, J = Σ_{i∈Y} (-t_i)(w^T x_i + b), ρ = 0,4")
    print(
        "(a) Với Y là tập mẫu phân lớp sai: "
        "∂J/∂w = Σ_{i∈Y} (-t_i) x_i,  ∂J/∂b = Σ_{i∈Y} (-t_i)."
    )
    print("    Giảm gradient: w ← w - ρ ∂J/∂w,  b ← b - ρ ∂J/∂b.")
    print(
        "(b) Batch: lặp đến khi không còn mẫu sai — mỗi vòng gom mọi mẫu sai vào Y."
    )
    X = np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
    t = np.array([-1.0, 1.0, 1.0, 1.0])
    rho = 0.4
    w = np.array([0.0, 1.0])
    b = -0.5
    print("(c) Khởi tạo: đường x2 = 0,5  →  w=(0,1)^T, b=-0,5.")

    def classify(xx: np.ndarray, ww: np.ndarray, bb: float) -> int:
        return tau_sign(float(ww @ xx + bb))

    step = 0
    while True:
        preds = np.array([classify(X[i], w, b) for i in range(len(X))])
        mis = np.where(preds != t)[0]
        print(f"\n--- Bước {step}: w=({w[0]:.6g},{w[1]:.6g})^T, b={b:.6g}")
        print("    Dự đoán:", preds.astype(int).tolist(), " nhãn:", t.astype(int).tolist())
        if mis.size == 0:
            print("    Không còn mẫu sai — dừng.")
            break
        Y = mis
        g_w = np.zeros(2)
        g_b = 0.0
        for i in Y:
            g_w += (-t[i]) * X[i]
            g_b += -t[i]
        print(f"    Tập sai Y: {Y.tolist()}  grad_w={g_w.tolist()}  grad_b={g_b:g}")
        w = w - rho * g_w
        b = b - rho * g_b
        step += 1
        if step > 20:
            print("    Giới hạn bước.")
            break

    print(f"\nKết quả cuối: w=({w[0]:.12g},{w[1]:.12g})^T, b={b:.12g}")


def q_4_6_4_mlp() -> None:
    divider("Câu 4.6.4 — MLP, x = (1,1)^T, τ là bước theo dấu")
    x1, x2 = 1.0, 1.0
    s1 = -0.5 + x1 + x2
    s2 = 1.5 - x1 - x2
    h1 = tau_sign(s1)
    h2 = tau_sign(s2)
    s3 = -1.0 + h1 + h2
    y3 = tau_sign(s3)
    print(f"Neuron ①: s₁ = -0,5 + x₁ + x₂ = {s1:g}  →  ra = {h1:+d}")
    print(f"Neuron ②: s₂ = 1,5 - x₁ - x₂ = {s2:g}  →  ra = {h2:+d}")
    print(f"Neuron ③: s₃ = -1 + ra₁ + ra₂ = {s3:g}  →  ra = {y3:+d}")


def q_4_6_5_regression_gd() -> None:
    divider("Câu 4.6.5 — Hồi quy tuyến tính, m = 4, J = (1/2m) Σ(y_i - w x_i - b)²")
    xs = np.array([0.0, 1.0, 2.0, 3.0])
    ys = np.array([1.0, 3.0, 5.0, 7.0])
    m = len(xs)
    print(
        "(a) J(w,b) = (1/2m)Σ (y_i - w x_i - b)²  ⇒  "
        "∂J/∂w = -(1/m)Σ (y_i - w x_i - b) x_i,  "
        "∂J/∂b = -(1/m)Σ (y_i - w x_i - b)."
    )
    print("    Batch GD: w ← w - ρ ∂J/∂w,  b ← b - ρ ∂J/∂b.")

    def j_loss(w: float, bb: float) -> float:
        pred = w * xs + bb
        err = ys - pred
        return float((err**2).sum() / (2 * m))

    def grads(w: float, bb: float) -> tuple[float, float]:
        pred = w * xs + bb
        err = ys - pred
        djw = float(-(err * xs).sum() / m)
        djb = float(-err.sum() / m)
        return djw, djb

    print("Tập: (0,1), (1,3), (2,5), (3,7) — đường thật y = 2x + 1.")
    w, b = 0.0, 1.0
    gw, gb = grads(w, b)
    j0 = j_loss(w, b)
    print(f"(b) Tại w(0)=0, b(0)=1 (ŷ ≡ 1): ∂J/∂w = {gw:g}, ∂J/∂b = {gb:g}, J = {j0:g}")

    rho = 0.1
    print(f"(d) Batch GD, ρ = {rho}, 3 vòng:")
    w, b = 0.0, 1.0
    print(f"    vòng 0: w={w:g}, b={b:g}, J={j_loss(w, b):.12g}")
    for it in range(1, 4):
        gw, gb = grads(w, b)
        w -= rho * gw
        b -= rho * gb
        print(f"    vòng {it}: w={w:.12g}, b={b:.12g}, J={j_loss(w, b):.12g}")


def main() -> None:
    q_4_6_1()
    q_4_6_2()
    q_4_6_3_or_table()
    perceptron_batch_gd_misclass_loss()
    q_4_6_4_mlp()
    q_4_6_5_regression_gd()
    print()


if __name__ == "__main__":
    main()
