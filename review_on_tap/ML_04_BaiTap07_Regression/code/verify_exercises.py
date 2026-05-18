"""
PER-4796 — Đối chiếu số bài ML_04 BT07.

Công thức JD (đề cho Câu 3, Câu 5):
  J(w,b) = (1/(2m)) * Σ_i (y_i - ŷ_i)² ,  ŷ_i = w x_i + b
  ∂J/∂w = -(1/m) Σ_i (y_i - ŷ_i) x_i
  ∂J/∂b = -(1/m) Σ_i (y_i - ŷ_i)
  Cập nhật GD: w ← w - η ∂J/∂w , b ← b - η ∂J/∂b

Cross-entropy (Câu 8):
  Loss mẫu i: - [ y_i ln z_i + (1-y_i) ln(1-z_i) ] (z_i là xác suất dự đoán đề cho)
"""

from __future__ import annotations

import numpy as np


def divider(title: str) -> None:
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)


def sign_clf(z: float) -> float:
    return 1.0 if z >= 0 else -1.0


def q1() -> None:
    x = np.array([1, 2, 3, 4, 5], dtype=float)
    y = np.array([3, 5, 7, 9, 11], dtype=float)
    n = len(x)
    x_mean = float(x.mean())
    y_mean = float(y.mean())
    ss_xy = float(((x - x_mean) * (y - y_mean)).sum())
    ss_x = float(((x - x_mean) ** 2).sum())
    beta1 = ss_xy / ss_x
    beta0 = y_mean - beta1 * x_mean
    x_new = 6.0
    y_hat = beta0 + beta1 * x_new
    print("(a) x̄ =", x_mean, ", ȳ =", y_mean)
    print("(b) SS_xy =", ss_xy, ", SS_x =", ss_x)
    print("(c) β̂₁ =", beta1)
    print("(d) β̂₀ =", beta0)
    print("(e) ŷ =", f"{beta0:g} + {beta1:g} x")
    print("(f) Dự báo tại x = 6: ŷ =", y_hat)


def q2() -> None:
    x = np.array([1, 2, 3, 4], dtype=float)
    y = np.array([4, 6, 8, 11], dtype=float)
    y_hat = 2 * x + 1
    e = y_hat - y
    mse = float((e**2).mean())
    print("(a) ŷ:", y_hat.tolist())
    print("(b) e_i = ŷ_i - y_i:", e.tolist())
    print("(c) MSE = (1/n) Σ e_i² =", mse, f"= {mse * 4}/4 (= 7/4)")
    print("(d) MSE ~ 1,75 — mô hình lệch vì sai số không đều (|e_4| = 2).")


def gd_step_half_mse(x: np.ndarray, y: np.ndarray, w: float, b: float, eta: float) -> dict:
    """Một bước batch GD cho J = (1/(2m)) Σ (y_i - wx_i - b)^2."""
    m = len(x)
    y_pred = w * x + b
    err = y - y_pred
    dj_dw = -(1.0 / m) * float((err * x).sum())
    dj_db = -(1.0 / m) * float(err.sum())
    j = (1.0 / (2 * m)) * float((err**2).sum())
    w_new = w - eta * dj_dw
    b_new = b - eta * dj_db
    return {
        "J": j,
        "dj_dw": dj_dw,
        "dj_db": dj_db,
        "w_new": w_new,
        "b_new": b_new,
        "y_pred": y_pred,
    }


def q3() -> None:
    x = np.array([1, 2, 4], dtype=float)
    y = np.array([3, 5, 9], dtype=float)
    eta = 0.1
    r = gd_step_half_mse(x, y, 0.0, 0.0, eta)
    print("Khởi tạo w = 0, b = 0, η = 0.1, m = 3")
    print("(a) ŷ ban đầu (toàn bộ 0):", r["y_pred"].tolist())
    print("(b) ∂J/∂w =", r["dj_dw"], ", ∂J/∂b =", r["dj_db"])
    print("(c) w_mới =", r["w_new"], ", b_mới =", r["b_new"])
    print("(d) Phương trình sau 1 bước: ŷ = {:.6g} x + {:.6g}".format(r["w_new"], r["b_new"]))


def q4() -> None:
    X = np.array([[1, 1, 2], [1, 2, 1], [1, 3, 2], [1, 4, 3]], dtype=float)
    Y = np.array([5, 6, 9, 12], dtype=float)
    xt_x = X.T @ X
    xt_y = X.T @ Y
    beta = np.linalg.solve(xt_x, xt_y)
    print("(a) X (thêm cột 1 cho β₀):\n", X)
    print("    Y:", Y.tolist())
    print("(c) X^T X:\n", xt_x)
    print("(d) X^T Y:", xt_y.tolist())
    print("(e) β̂ = (X^T X)^{-1} X^T Y =", beta.tolist())
    x_new = np.array([1, 5, 2], dtype=float)
    y_hat = float(x_new @ beta)
    print("(f) Dự báo (x₁,x₂) = (5,2): x = [1,5,2], ŷ =", y_hat)


def q5() -> None:
    x = np.array([1, 2, 3, 4, 5], dtype=float)
    y = np.array([2, 3, 5, 4, 6], dtype=float)
    m = len(x)
    eta = 0.1
    w, b = 0.0, 0.0
    err = y - (w * x + b)
    dj_dw = -(1.0 / m) * float((err * x).sum())
    dj_db = -(1.0 / m) * float(err.sum())
    j0 = (1.0 / (2 * m)) * float((err**2).sum())
    print("m = 5, η = 0.1, J = (1/(2m)) Σ(y_i - wx_i - b)²")
    print("(a) ∂J/∂w = -(1/m) Σ (y_i - ŷ_i) x_i ; ∂J/∂b = -(1/m) Σ (y_i - ŷ_i)")
    print(f"    Tại w=b=0: J = {j0}; ∂J/∂w = {dj_dw}; ∂J/∂b = {dj_db}")
    r = gd_step_half_mse(x, y, 0.0, 0.0, eta)
    print("(b) Sau 1 GD: w =", r["w_new"], ", b =", r["b_new"])
    x6 = 6.0
    pred = r["w_new"] * x6 + r["b_new"]
    print("(c) Dự báo x = 6: ŷ =", pred)


def q6_values() -> None:
    w = np.array([2.0, -1.0])
    b = 1.0
    pts = np.array([(1, 1, "A"), (2, 1, "B"), (1, 3, "C"), (4, 2, "D")])
    names = pts[:, 2]
    xs = np.array([[float(pts[i, 0]), float(pts[i, 1])] for i in range(len(pts))])
    print("Quy tắc: wᵀx + b ≥ 0 → lớp 1 ; < 0 → lớp 0")
    print("(a)-(b)")
    for i, nm in enumerate(names):
        s = float(w @ xs[i] + b)
        cls = 1 if s >= 0 else 0
        print(f"   Điểm {nm} ({xs[i][0]:g},{xs[i][1]:g}): wᵀx+b = {s:.3g} → lớp {cls}")
    print("(c) Đường ranh giới: 2x₁ - x₂ + 1 = 0  ⟺  x₂ = 2x₁ + 1")
    print("(d) Hình: chạy plot_decision_boundary_c6.py")


def sigmoid(z: float) -> float:
    return float(1.0 / (1.0 + np.exp(-z)))


def q7() -> None:
    w1, w2, b = 0.5, -1.0, 0.2
    x1, x2 = 2.0, 1.0
    z = w1 * x1 + w2 * x2 + b
    p = sigmoid(z)
    print("(a) z =", z)
    print("(b) P(y=1|x) = σ(z) =", p)
    print("(c) Ngưỡng 0,5 → lớp 1" if p >= 0.5 else "(c) Ngưỡng 0,5 → lớp 0")
    print("(d) Ngưỡng 0,8 → lớp 1" if p >= 0.8 else "(d) Ngưỡng 0,8 → lớp 0")


def q8() -> None:
    y = np.array([1.0, 0.0, 1.0])
    z = np.array([0.9, 0.2, 0.7])
    per = -(y * np.log(z) + (1 - y) * np.log(1 - z))
    total = float(per.sum())
    avg = total / len(y)
    print("Loss mẫu i: -[y_i ln z_i + (1-y_i) ln(1-z_i)]")
    for i in range(3):
        print(f"   Mẫu {i+1}: {per[i]:.8f}")
    print("(b) Tổng loss =", total)
    print("(c) Loss trung bình =", avg)
    print("(d) Loss hữu hạn, thấp hơn nhiều so với bộ mẫu rất sai; mẫu 1 gần nhất với nhãn 1.")


def perceptron_epoch(
    X: np.ndarray,
    t: np.ndarray,
    w: np.ndarray,
    b: float,
    rho: float,
) -> tuple[np.ndarray, float, list[str]]:
    """Một epoch: lần lượt từng mẫu; đúng khi t_k (wᵀx_k+b) > 0; ngược lại cập nhật PLA."""
    w = w.copy()
    log: list[str] = []
    for k in range(len(X)):
        xk = X[k]
        tk = t[k]
        score = float(w @ xk + b)
        margin = tk * score
        ok = margin > 0
        log.append(
            f"  mẫu{k+1} x={xk.tolist()} t={tk:g} score={score:.4g} t·score={margin:.4g} → "
            + ("đúng" if ok else "SAI")
        )
        if not ok:
            w = w + rho * tk * xk
            b = b + rho * tk
            log.append(f"    cập nhật: w={w.tolist()}, b={b:g}")
    return w, b, log


def q9() -> None:
    X = np.array([[1, 1], [2, 1], [1, 3]], dtype=float)
    t = np.array([1.0, 1.0, -1.0])
    rho = 1.0
    w0 = np.array([0.0, 0.0])
    b0 = 0.0
    print("Khởi tạo w=(0,0), b=0, ρ=1. Đúng khi t_k (wᵀx_k+b) > 0 (nghiêm).")
    w, b = w0.copy(), b0
    log0: list[str] = []
    for k in range(len(X)):
        score = float(w @ X[k] + b)
        m = t[k] * score
        log0.append(
            f"  mẫu{k+1}: t·(wᵀx+b) = {m:g} → "
            + ("đúng" if m > 0 else "sai phân lớp (cần cập nhật nếu đi qua PLA)")
        )
    print("(a) Với tham số ban đầu:")
    for line in log0:
        print(line)
    print("    → Cả 3 mẫu có điểm trên mặt phẳng wᵀx+b = 0 nên t·(wᵀx+b) = 0 ≤ 0: đều chưa phân lớp đúng theo tiêu chí nghiêm.")
    print("(b)–(c) Một epoch (duyệt lần lượt 3 mẫu, cập nhật khi sai):")
    w, b, log = perceptron_epoch(X, t, w0, b0, rho)
    for line in log:
        print(line)
    print("Sau 1 epoch: w =", w.tolist(), ", b =", b)
    print("(d) Đường ranh giới wᵀx + b = 0:")
    print(f"    {w[0]:g} x₁ + {w[1]:g} x₂ + ({b:g}) = 0")


def q10() -> None:
    X = np.array([[1, 1], [2, 1], [1, 2], [2, 2]], dtype=float)
    t = np.array([1.0, 1.0, -1.0, -1.0])
    w0 = np.array([1.0, 1.0])
    b0 = 0.0
    print("w⁽⁰⁾=(1,1), b⁽⁰⁾=0. Sai nếu t_k (wᵀx_k+b) ≤ 0.")
    mis = []
    for k in range(len(X)):
        s = float(w0 @ X[k] + b0)
        pred = sign_clf(s)
        ok = pred == t[k]
        print(
            f"  mẫu{k+1} x={X[k].tolist()} t={t[k]:g} wᵀx+b={s:.4g} sign={pred:g} → "
            + ("đúng" if ok else "SAI")
        )
        if not ok:
            mis.append(k)
    print("(a) Tập phân lớp sai Y = {mẫu có t_k (wᵀx_k+b) ≤ 0} → mẫu 3 và 4.")
    print(
        "(b) J = Σ_{k∈Y} (-t_k)(wᵀx_k+b)  ⟹  "
        "∂J/∂w = Σ_{k∈Y} (-t_k) x_k ,  ∂J/∂b = Σ_{k∈Y} (-t_k)"
    )
    g_w = np.zeros(2)
    g_b = 0.0
    for k in mis:
        g_w += (-t[k]) * X[k]
        g_b += -t[k]
    print(f"    Số học (tại w⁽⁰⁾, b⁽⁰⁾): ∂J/∂w = {g_w.tolist()} , ∂J/∂b = {g_b:g}")
    print(
        "(c) Một bước Perceptron (Rosenblatt) trên mẫu sai đầu tiên (1,2), t=-1, ρ=1:"
    )
    k0 = mis[0]
    w1 = w0 + 1.0 * t[k0] * X[k0]
    b1 = b0 + 1.0 * t[k0]
    print(f"    w⁽¹⁾ = w⁽⁰⁾ + t_k x_k = {w1.tolist()} , b⁽¹⁾ = {b1:g}")


def main() -> None:
    divider("Câu 1 — Hồi quy tuyến tính đơn")
    q1()
    divider("Câu 2 — MSE")
    q2()
    divider("Câu 3 — Một bước GD (m=3)")
    q3()
    divider("Câu 4 — Hồi quy đa biến (phương trình chuẩn)")
    q4()
    divider("Câu 5 — Batch GD (m=5)")
    q5()
    divider("Câu 6 — Phân lớp đường ranh giới tuyến tính")
    q6_values()
    divider("Câu 7 — Logistic")
    q7()
    divider("Câu 8 — Cross-entropy")
    q8()
    divider("Câu 9 — Perceptron (3 mẫu)")
    q9()
    divider("Câu 10 — Perceptron + hàm mất mát trên tập sai")
    q10()


if __name__ == "__main__":
    main()
