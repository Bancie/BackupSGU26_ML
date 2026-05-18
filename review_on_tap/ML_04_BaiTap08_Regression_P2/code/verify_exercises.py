"""
PER-4797 — ML_04_BaiTap08_Regression_P2: đối chiếu số theo đề.

Định nghĩa bám đề giảng dạy (trích):

- OLS đơn: a1 = [mean(xy) − x̄ȳ] / [mean(x^2) − x̄^2],  a0 = ȳ − a1·x̄,  mô hình y = a0 + a1 x.

- Phần dư (Câu 2): e_i = y_i − ŷ_i ;  SSE = Σ (y_i − ŷ_i)^2.

- MAE, MSE, RMSE (Câu 3): MAE = (1/n)Σ|y_i − ŷ_i|, MSE = (1/n)Σ(y_i − ŷ_i)^2, RMSE = √MSE.

- RelMSE (Câu 4): RelMSE = Σ(y_i − ŷ_i)^2 / Σ(y_i − ȳ)^2 với y, ŷ ở tập kiểm tra và
  ȳ là trung bình tập huấn luyện.

- CV (Câu 4): CV = RMSE / ȳ (ȳ huấn luyện; RMSE từ tập kiểm tra như trong đề).

- Logistic: p = 1 / (1 + exp(−(...))) ; ngưỡng 0.5.

- Ridge: Loss_Ridge = SSE + λ·a_1^2 (theo đề Câu 12).

- Lasso: LOSS_Lasso = SSE + λ(|a1|+|a2|+|a3|) (đề Câu 13).

- Elastic Net: Loss = SSE + λ1Σ|ai| + λ2Σ ai^2 (đề Câu 14).
"""

from __future__ import annotations

import numpy as np


def divider(title: str) -> None:
    print()
    print("=" * 64)
    print(title)
    print("=" * 64)


def sigmoid(z: float | np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-np.asarray(z)))


def q1() -> None:
    x = np.array([1, 2, 3, 4, 5], dtype=float)
    y = np.array([1.2, 1.8, 2.6, 3.2, 3.8], dtype=float)
    mx = float(x.mean())
    my = float(y.mean())
    mx2 = float((x * x).mean())
    mxy = float((x * y).mean())
    den = mx2 - mx * mx
    a1 = (mxy - mx * my) / den
    a0 = my - a1 * mx
    print(f"(a) x̄ = {mx:g}, ȳ = {my:g}, x²̄ = {mx2:g}, xȳ = {mxy:g}")
    print(f"(b) a1 = {a1:g}")
    print(f"(c) a0 = {a0:g}")
    print(f"(d) Phương trình hồi quy: y = {a0:g} + {a1:g}·x")
    print("(e) Tuần 7: ŷ ≈ {:.4g};  tuần 9: ŷ ≈ {:.4g}".format(a0 + a1 * 7, a0 + a1 * 9))


def q2() -> None:
    x = np.array([1, 2, 3, 4, 5], dtype=float)
    y = np.array([1.2, 1.8, 2.6, 3.2, 3.8], dtype=float)
    y_hat = 0.54 + 0.66 * x
    e = y - y_hat
    sse = float((e**2).sum())
    print("(a) ŷ:", np.round(y_hat, 15).tolist())
    print("(b) e_i = y_i − ŷ_i:", np.round(e, 15).tolist())
    print(f"(c) SSE = Σ e_i² = {sse:g} (= {sse:.12g})")


def q3() -> None:
    y = np.array([80.0, 75, 90, 100])
    y_hat = np.array([75.0, 85, 88, 95])
    n = len(y)
    ae = np.abs(y - y_hat)
    mae = float(ae.mean())
    mse = float(((y - y_hat) ** 2).mean())
    rmse = float(np.sqrt(mse))
    print("(a) |y_i − ŷ_i|:", ae.tolist())
    print(f"(b) MAE = {mae:g} (= {mae})")
    print(f"(c) MSE = {mse:g}")
    print(f"(d) RMSE = √(MSE) = {rmse:.12g}")


def q4() -> None:
    y_train = np.array([80.0, 90, 100, 110, 120])
    yb = float(y_train.mean())
    y_t = np.array([80.0, 75])
    y_hat = np.array([75.0, 85])
    num = float(((y_t - y_hat) ** 2).sum())
    den = float(((y_t - yb) ** 2).sum())
    rel_mse = num / den
    mse = float(((y_t - y_hat) ** 2).mean())
    rmse = float(np.sqrt(mse))
    cv = rmse / yb
    print(f"(a) ȳ (tập huấn luyện) = {yb:g}")
    print(f"(b) RelMSE = {rel_mse:.12g} (= {num}/{den})")
    print(f"(c) RMSE (kiểm tra) = {rmse:.12g}; CV = RMSE/ȳ_huấn_luyện = {cv:.12g}")


def q5() -> None:
    X = np.array([[1.0, 1], [1, 2], [1, 3], [1, 4]])
    Y = np.array([1.0, 3, 4, 8])
    xt_x = X.T @ X
    xt_y = X.T @ Y
    inv_xt_x = np.linalg.inv(xt_x)
    a = inv_xt_x @ xt_y
    print("(a)--(b)")
    print("    X=\n", X)
    print("    Y=", Y.tolist())
    print("(c) X^T X=\n", xt_x)
    print("(d) (X^T X)^{-1}=\n", inv_xt_x)
    print("(e) X^T Y=", xt_y.tolist())
    print("    a = (X^T X)^{-1} X^T Y =", np.round(a, 12).tolist())
    print("(f) y = {:.12g} + {:.12g}·x".format(a[0], a[1]))


def q6() -> None:
    X = np.array([[1.0, 1, 4], [1, 2, 5], [1, 3, 8], [1, 4, 2]])
    Y = np.array([1.0, 6, 8, 12])
    xt_x = X.T @ X
    xt_y = X.T @ Y
    inv_xt_x = np.linalg.inv(xt_x)
    a = inv_xt_x @ xt_y
    print("(a) X=\n", X)
    print("    Y=", Y.tolist())
    print("(c) Phương trình chuẩn: (X^T X)^{-1} X^T Y")
    print("    X^T X=\n", xt_x)
    print("    X^T Y=", xt_y.tolist())
    print("    Đặt a=", np.round(a, 12).tolist())
    print("(e) ŷ ≈ {:.6g} + {:.6g}·x1 + {:.6g}·x2".format(a[0], a[1], a[2]))
    x_new = np.array([1.0, 5, 6])
    print(f"(f) ŷ({5},{6}) ≈ {float(x_new @ a):.12g}")


def q7() -> None:
    x = np.array([1.0, 2, 3, 4])
    y = np.array([1.0, 4, 9, 15])
    x2, x3, x4 = x**2, x**3, x**4
    xy = x * y
    x2y = (x * x) * y
    print("(a)--(b): bảng tính và tổng")
    sums = (
        ("n", len(x)),
        ("Σx", float(x.sum())),
        ("Σy", float(y.sum())),
        ("Σx²", float(x2.sum())),
        ("Σx³", float(x3.sum())),
        ("Σx⁴", float(x4.sum())),
        ("Σ(xy)", float(xy.sum())),
        ("Σ(x²y)", float(x2y.sum())),
    )
    for k, v in sums:
        print(f"    {k} = {v:g}")
    n = len(x)
    sx, sy, sx2, sx3, sx4 = float(x.sum()), float(y.sum()), float(x2.sum()), float(x3.sum()), float(x4.sum())
    sxy, sx2y = float(xy.sum()), float(x2y.sum())
    m = np.array([[n, sx, sx2], [sx, sx2, sx3], [sx2, sx3, sx4]], dtype=float)
    rhs = np.array([sy, sxy, sx2y], dtype=float)
    print("(c) Ma trận hệ Chuẩn (3×3)·[a0,a1,a2]^T = [Σy,Σxy,Σx²y]^T:")
    print("    M × a = RHS với M=\n", m)
    print("    RHS =", rhs.tolist())
    a = np.linalg.solve(m, rhs)
    print("(d)--(f) Hệ số a =", np.round(a, 12).tolist())
    xf = 5.0
    print(f"    Dự báo x={xf:g}: ŷ = {a[0] + a[1] * xf + a[2] * xf ** 2:g}")


def q8() -> None:
    a0, a1 = -4.0, 0.08
    for xv in [40.0, 60, 80]:
        z = a0 + a1 * xv
        p = float(sigmoid(z))
        cls = "Đậu (p≥0,5)" if p >= 0.5 else "Rớt (p<0,5)"
        print(f"  x={xv:g}: z={z:g}, p={p:.12g} → ngưỡng 0,5: {cls}")


def q9() -> None:
    probs = np.array([0.2, 0.5, 0.8])
    lbl = ["A", "B", "C"]
    print("Odds = p/(1−p);  logit = ln(p/(1−p))")
    for i, p in enumerate(probs):
        odds = p / (1 - p)
        logit = float(np.log(odds))
        print(f"  Email {lbl[i]} p={p:g} → odds={odds:g} ; logit={logit:g}")


def q10() -> None:
    rows = [
        ("A", 60.0, 50),
        ("B", 70, 80),
        ("C", 40, 45),
        ("D", 90, 85),
    ]
    hi: list[str] = []
    for name, x1, x2 in rows:
        z = -3.0 + 0.04 * x1 + 0.06 * x2
        p = float(sigmoid(z))
        c05 = "Trúng tuyển (p≥0,5)" if p >= 0.5 else "Không (p<0,5)"
        if p >= 0.8:
            hi.append(name)
        print(f"  {name} ({x1:g},{x2:g}): z={z:g}, p={p:.12g}; (c) ngưỡng 0,5: {c05}")
    print("(d) Ngưỡng 0,8 (p≥0,8 — nhập học):", hi)


def q11() -> None:
    y = np.array([10.0, 15, 20, 25, 30])
    y_hat = np.array([12.0, 14, 19, 27, 28])
    yb = float(y.mean())
    sst = float(((y - yb) ** 2).sum())
    sse = float(((y - y_hat) ** 2).sum())
    r2 = 1 - sse / sst
    print(f"(a) ȳ = {yb:g}")
    print(f"(b) SST = {sst:g}")
    print(f"(c) SSE = {sse:g}")
    print(f"(d) R² = 1 − SSE/SST = {r2:.12g}  (SSE={sse:g}, SST={sst:g})")


def q12() -> None:
    sse = 40.0
    a1 = 3.0
    lam = 2.0
    pen = lam * a1**2
    print(f"(a) Penalty λ·a₁² = {lam}·{a1}^2 = {pen:g}")
    print(f"(b) Loss_Ridge = SSE + penalty = {sse + pen:g}")
    lam2 = 5.0
    pen5 = lam2 * a1**2
    print(f"(c) Với λ=5: penalty = {pen5:g}, tổng loss = {sse + pen5:g}")


def q13() -> None:
    sse = 40.0
    a = np.array([3.0, -2.0, 0.5])
    lam = 2.0
    l1_norm = float(np.abs(a).sum())
    pen = lam * l1_norm
    print(f"(a) |a₁|+|a₂|+|a₃| = {l1_norm:g}")
    print(f"(b) Lasso penalty λ·(...) = {pen:g}")
    print(f"(c) Tổng loss = SSE + penalty = {sse + pen:g}")


def q14() -> None:
    sse = 50.0
    a = np.array([2.0, -1.0, 3.0])
    l1, l2 = 1.0, 0.5
    lace = float(l1 * np.abs(a).sum())
    ridge = float(l2 * (a * a).sum())
    total = sse + lace + ridge
    print(f"(a) λ₁Σ|ai| = {lace:g}")
    print(f"(b) λ₂Σai² = {ridge:g}")
    print(f"(c) Elastic Net loss = {total:g}")


def q15() -> None:
    x = np.array([2.0, 3, 5, 7, 9])
    y = np.array([20.0, 25, 35, 45, 55])
    mx = float(x.mean())
    my = float(y.mean())
    a1 = (float((x * y).mean()) - mx * my) / (float((x * x).mean()) - mx * mx)
    a0 = my - a1 * mx
    y_hat = a0 + a1 * x
    mae = float(np.abs(y - y_hat).mean())
    mse = float(((y - y_hat) ** 2).mean())
    rmse = float(np.sqrt(mse))
    sst = float(((y - my) ** 2).sum())
    sse = float(((y - y_hat) ** 2).sum())
    r2 = 1 - sse / sst
    print("(a)--(b)--(mô hình) OLS:")
    print(f"    y = {a0:.12g} + {a1:.12g}·x ;  ŷ({10:g}) ≈ {a0 + a1 * 10:.12g}")
    print(f"(c) MAE = {mae:.4g}; MSE ≈ {mse:.4g}; RMSE ≈ {rmse:.4g} ≈ 0 (khớp hoàn hảo)")
    print(f"(d) R² = {r2:.12g}")
    print(f"(e) SST={sst:g}, SSE={sse:.3g} (dùng khi giải thích R²)")


def main() -> None:
    divider("Câu 1 — OLS đơn (doanh số theo tuần)")
    q1()
    divider("Câu 2 — Sai số của mô hình ŷ=0,54+0,66x")
    q2()
    divider("Câu 3 — MAE, MSE, RMSE")
    q3()
    divider("Câu 4 — RelMSE, CV")
    q4()
    divider("Câu 5 — Hồi quy ma trận một biến")
    q5()
    divider("Câu 6 — Đa biến OLS")
    q6()
    divider("Câu 7 — Đa thức bậc hai")
    q7()
    divider("Câu 8 — Logistic một biến")
    q8()
    divider("Câu 9 — Odds & logit")
    q9()
    divider("Câu 10 — Logistic hai biến")
    q10()
    divider("Câu 11 — R²")
    q11()
    divider("Câu 12 — Ridge loss")
    q12()
    divider("Câu 13 — Lasso loss")
    q13()
    divider("Câu 14 — Elastic Net")
    q14()
    divider("Câu 15 — Tổng hợp (OLS + chỉ số)")
    q15()


if __name__ == "__main__":
    main()
