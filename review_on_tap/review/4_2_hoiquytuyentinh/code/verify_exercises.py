"""
PER-4807 — Đối chiếu số bài 4.2 (hồi quy tuyến tính, Batch GD).

Đề: J(w,b) = (1/(2m)) Σ_i (y_i - ŷ_i)^2 ,  ŷ_i = w x_i + b
    ∂J/∂w = -(1/m) Σ_i (y_i - ŷ_i) x_i
    ∂J/∂b = -(1/m) Σ_i (y_i - ŷ_i)
    Cập nhật: w ← w - η ∂J/∂w ,  b ← b - η ∂J/∂b
"""

from __future__ import annotations


def divider(title: str) -> None:
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)


def gd_step_half_mse(
    x: list[float],
    y: list[float],
    w: float,
    b: float,
    eta: float,
) -> dict:
    """Một bước batch GD cho J = (1/(2m)) Σ (y_i - wx_i - b)^2."""
    m = len(x)
    y_pred = [w * xi + b for xi in x]
    err = [yi - ypi for yi, ypi in zip(y, y_pred)]
    dj_dw = -(1.0 / m) * sum(e * xi for e, xi in zip(err, x))
    dj_db = -(1.0 / m) * sum(err)
    j = (1.0 / (2 * m)) * sum(e * e for e in err)
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


def q4_bgd() -> None:
    x = [1.0, 2.0, 3.0, 4.0, 5.0]
    y = [2.0, 3.0, 5.0, 4.0, 6.0]
    m = len(x)
    eta = 0.1
    w0, b0 = 0.0, 0.0

    print("Dữ liệu (x,y):", list(zip(x, y)), f", m = {m}")
    print("Khởi tạo w^(0) = b^(0) = 0, η =", eta)
    print()
    print(
        "Biểu thức tổng quát (batch):",
        "J(w,b) = (1/(2m)) Σ_i (y_i - w x_i - b)^2;",
        "∂J/∂w = -(1/m) Σ_i (y_i - ŷ_i) x_i;",
        "∂J/∂b = -(1/m) Σ_i (y_i - ŷ_i).",
    )

    err0 = [yi - (w0 * xi + b0) for yi, xi in zip(y, x)]
    sum_err_x = sum(e * xi for e, xi in zip(err0, x))
    sum_err = sum(err0)
    j0 = (1.0 / (2 * m)) * sum(e * e for e in err0)
    dj_dw = -(1.0 / m) * sum_err_x
    dj_db = -(1.0 / m) * sum_err

    print()
    print("(a) Tại w = b = 0: ŷ_i = 0, y_i - ŷ_i = y_i")
    print(f"    Σ_i (y_i - ŷ_i) x_i = {sum_err_x:g},  Σ_i (y_i - ŷ_i) = {sum_err:g}")
    print(f"    ∂J/∂w = {dj_dw:g} (= -69/5),  ∂J/∂b = {dj_db:g},  J = {j0:g}")

    r = gd_step_half_mse(x, y, w0, b0, eta)
    print()
    print("(b) Một bước Gradient Descent:")
    print(f"    w^(1) = w^(0) - η ∂J/∂w = {r['w_new']:.12g}")
    print(f"    b^(1) = b^(0) - η ∂J/∂b = {r['b_new']:.12g}")

    x_new = 6.0
    pred = r["w_new"] * x_new + r["b_new"]
    print()
    print("(c) Dự đoán sau bước 1, x = 6: ŷ =", f"{pred:.12g}")


def main() -> None:
    divider("Câu 4 — §4.2 Mô hình hồi quy tuyến tính (Batch GD)")
    q4_bgd()


if __name__ == "__main__":
    main()
