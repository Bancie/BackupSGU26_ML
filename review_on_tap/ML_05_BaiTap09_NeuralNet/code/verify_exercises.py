"""
PER-4798 — ML_05_BaiTap09_NeuralNet: đối chiếu số theo đề Bài tập Neural Networks.
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


def q1() -> None:
    """Đường biên: x2 = -1.5*x1 + 3  <=>  1.5*x1 + x2 - 3 = 0."""
    divider("Câu 1 — Perceptron cho đường biên x2 = -1,5 x1 + 3")
    w = np.array([1.5, 1.0])
    b = -3.0
    print("Một bộ tham số (trong không gian w^T x + b = 0):")
    print(f"  w = ({w[0]:g}, {w[1]:g})^T,  b = {b:g}")
    print("Nhân 2 để tránh thập phân: w = (3, 2)^T, b = -6 — cùng đường thẳng.")
    print("Output y = τ(w^T x + b) với τ(s)=+1 nếu s≥0, -1 nếu s<0.")


def q2() -> None:
    divider("Câu 2 — Perceptron bias -3, trọng số x1: 2, x2: 1")
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
        "→ bias (hệ số 1) = -2, w1 = 1, w2 = -2."
    )
    w_or = np.array([1.0, 1.0])
    b_or = -0.5
    print("(d) OR (thử nghiệm): w0=-0,5, w1=1, w2=1 (ký hiệu s = -0,5 + x1 + x2).")
    for x1v, x2v, name in [(0, 0, "(0,0)"), (1, 0, "(1,0)"), (0, 1, "(0,1)"), (1, 1, "(1,1)")]:
        s = b_or + w_or[0] * x1v + w_or[1] * x2v
        print(f"    {name}: s = {s:g}  →  y = {tau_sign(s):+d}")
    w_and = np.array([1.0, 1.0])
    b_and = -1.5
    print("(d) AND: w0=-1,5, w1=1, w2=1 (s = -1,5 + x1 + x2).")
    for x1v, x2v, name in [(0, 0, "(0,0)"), (1, 0, "(1,0)"), (0, 1, "(0,1)"), (1, 1, "(1,1)")]:
        s = b_and + w_and[0] * x1v + w_and[1] * x2v
        print(f"    {name}: s = {s:g}  →  y = {tau_sign(s):+d}")


def q3_or_table() -> None:
    divider("Câu 3 — Bảng OR (x1,x2) ∈ {0,1}^2, a=(0,0) nhãn -1, còn lại +1")
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
    divider("Perceptron — GD batch, J = Σ_{i∈Y} (-t_i)(w^T x_i + b), ρ = 0,4")
    print(
        "(a) Với Y là tập mẫu bị phân lớp sai: "
        "∂J/∂w = Σ_{i∈Y} (-t_i) x_i,  ∂J/∂b = Σ_{i∈Y} (-t_i)."
    )
    print("    Gradient descent (tối thiểu hóa J): w ← w - ρ ∂J/∂w,  b ← b - ρ ∂J/∂b.")
    print(
        "(b) Thuật toán batch: lặp cho đến khi không còn mẫu sai — "
        "mỗi vòng gom mọi mẫu sai vào Y, "
        "nếu Y rỗng thì dừng, nếu không thì cập nhật w,b một lần từ toàn bộ Y."
    )
    X = np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
    t = np.array([-1.0, 1.0, 1.0, 1.0])
    rho = 0.4
    w = np.array([0.0, 1.0])
    b = -0.5
    print("Khởi tạo: đường x2 = 0,5  →  w=(0,1)^T, b=-0,5.")

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
        print(f"    Tập sai Y indices: {Y.tolist()}  grad_w={g_w.tolist()}  grad_b={g_b:g}")
        w = w - rho * g_w
        b = b - rho * g_b
        step += 1
        if step > 20:
            print("    Giới hạn bước — kiểm tra lại.")
            break

    print(f"\nKết quả cuối: w=({w[0]:.12g},{w[1]:.12g})^T, b={b:.12g}")


def q4_mlp() -> None:
    divider("Câu 4 — MLP forward, x = (1,1)^T, τ là dấu")
    x1, x2 = 1.0, 1.0
    s1 = -0.5 + x1 + x2
    s2 = 1.5 - x1 - x2
    h1 = tau_sign(s1)
    h2 = tau_sign(s2)
    s3 = -1.0 + h1 + h2
    y3 = tau_sign(s3)
    print(f"Neuron ①: s₁ = -0,5 + x₁ + x₂ = {s1:g}  →  out = {h1:+d}")
    print(f"Neuron ②: s₂ = 1,5 - x₁ - x₂ = {s2:g}  →  out = {h2:+d}")
    print(f"Neuron ③: s₃ = -1 + out₁ + out₂ = {s3:g}  →  out = {y3:+d}")


def q5_regression_gd() -> None:
    divider("Câu 5 — Hồi quy tuyến tính, m = 4, J = (1/2m) Σ(y_i - wx_i - b)²")
    xs = np.array([0.0, 1.0, 2.0, 3.0])
    ys = np.array([1.0, 3.0, 5.0, 7.0])
    m = len(xs)
    print(
        "(a) J(w,b) = (1/2m)Σ (y_i - w x_i - b)²  ⇒  "
        "∂J/∂w = -(1/m)Σ (y_i - w x_i - b) x_i,  "
        "∂J/∂b = -(1/m)Σ (y_i - w x_i - b)."
    )
    print("    Cập nhật batch GD: w ← w - ρ ∂J/∂w,  b ← b - ρ ∂J/∂b.")

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
    print(f"(b) Tại w(0)=0, b(0)=1 (đường ŷ ≡ 1): ∂J/∂w = {gw:g}, ∂J/∂b = {gb:g}, J = {j0:g}")

    rho = 0.1
    print(f"(d) Gradient descent batch, ρ = {rho}, 3 vòng lặp:")
    w, b = 0.0, 1.0
    print(f"    vòng 0: w={w:g}, b={b:g}, J={j_loss(w, b):.12g}")
    for it in range(1, 4):
        gw, gb = grads(w, b)
        w -= rho * gw
        b -= rho * gb
        print(f"    vòng {it}: w={w:.12g}, b={b:.12g}, J={j_loss(w, b):.12g}")


def q5a_cnn_dims() -> None:
    divider("Câu 5a — Conv output (128,128,3), 32 filter 3×3, stride 2, pad 1")
    hin, win, cin = 128, 128, 3
    k, p, s_ = 3, 1, 2
    hout = (hin + 2 * p - k) // s_ + 1
    wout = (win + 2 * p - k) // s_ + 1
    cout = 32
    print(f"Kích thước đầu ra (b, c, a trong hình):  cao = chiều cao c = {hout}, "
          f"rong = chiều rộng b = {wout},  sâu a = {cout}.")
    print(f"  (tensor: {hout}×{wout}×{cout})")


def conv2d_valid(x: np.ndarray, k: np.ndarray) -> np.ndarray:
    xh, xw = x.shape
    kh, kw = k.shape
    oh, ow = xh - kh + 1, xw - kw + 1
    out = np.zeros((oh, ow))
    for i in range(oh):
        for j in range(ow):
            out[i, j] = np.sum(x[i : i + kh, j : j + kw] * k)
    return out


def q5b_conv_pool() -> None:
    divider("Câu 5b — Convolution valid rồi max pooling 2×2")
    X = np.array(
        [[4, 6, 3, 4], [1, 7, 3, 4], [5, 8, 4, 4], [2, 7, 4, 4]],
        dtype=float,
    )
    K = np.array([[0, -0.25, 0], [-0.25, 1, -0.25], [0, -0.25, 0]], dtype=float)
    c_map = conv2d_valid(X, K)
    print("Bản đồ sau conv (2×2):")
    print(c_map)
    pooled = float(np.max(c_map))
    print(f"Sau max-pooling 2×2 (một cửa sổ phủ cả 2×2): giá trị = {pooled:g}")


def q6_mlp_digits() -> None:
    divider("Câu 6 — MLP chữ số 0–9, ảnh 10×10")
    n_pix = 100
    k = "k"
    print("(a) y = softmax(z) (đề ghi softmax(x) — hiểu nhầm, vector y kích thước 10).")
    print(f"(b) flatten n ∈ R^{n_pix}; lớp ẩn k nút:")
    print(f"    W^(1) ∈ R^{{{k}×{n_pix}}} (theo quy ước cột = n → mỗi cột một input), "
          f"thường viết Z = W^(1) n + b^(1) với W^(1) kích thước ({k}, {n_pix}).")
    print(f"    W^(2) ∈ R^(10×{k}) (ánh xạ {k} → 10).")
    print("    (Nếu dùng ký hiệu hàng×cột như NumPy: W1 shape (k, 100), W2 shape (10, k).)")


def q7_cnn_keras() -> None:
    divider("Câu 7 — CNN Keras (28,28,1)")
    h0, w0, c0 = 28, 28, 1
    # valid conv 3x3
    h1, w1 = h0 - 2, w0 - 2
    c1 = 64
    h2, w2 = h1 // 2, w1 // 2
    flat = h2 * w2 * c1
    d1, d2 = 128, 10
    conv_w = (3 * 3 * c0 + 1) * c1
    dense1_w = flat * d1 + d1
    dense2_w = d1 * d2 + d2
    print(f"Input:     {h0}×{w0}×{c0}")
    print(f"Conv+ReLU: {h1}×{w1}×{c1}  (valid)")
    print(f"MaxPool:   {h2}×{w2}×{c1}")
    print(f"Flatten:   vector độ dài {flat}")
    print(f"Dense-1:   128 nút; Dense-2: 10 nút (softmax)")
    print("Tham số:")
    print(f"  Conv2D:  (3·3·{c0}+1)·{c1} = {conv_w}")
    print(f"  Dense-1: {flat}·128 + 128 = {dense1_w}")
    print(f"  Dense-2: 128·10 + 10 = {dense2_w}")
    print(f"  Tổng (ước): {conv_w + dense1_w + dense2_w}")


def q8_rnn() -> None:
    divider("Câu 8 — RNN: tanh trạng thái, softmax đầu ra")
    print("Với ma trận U, W, V và bias (theo hình unrolled):")
    print("  s_t = tanh(U x_t + W s_{t-1} + b)")
    print("  o_t = softmax(V s_t + c)")


def q9_lstm() -> None:
    divider("Câu 9 — LSTM: công thức chuẩn theo sơ đồ [h_{t-1}, x_t]")
    print("Ký hiệu [h_{t-1}, x_t] là nối vector; σ là sigmoid; ⊙ là nhân từng phần tử.")
    print("  f_t = σ(W_f [h_{t-1}, x_t] + b_f)")
    print("  i_t = σ(W_i [h_{t-1}, x_t] + b_i)")
    print("  C̃_t = tanh(W_C [h_{t-1}, x_t] + b_C)")
    print("  C_t = f_t ⊙ C_{t-1} + i_t ⊙ C̃_t")
    print("  o_t = σ(W_o [h_{t-1}, x_t] + b_o)")
    print("  h_t = o_t ⊙ tanh(C_t)")


def main() -> None:
    q1()
    q2()
    q3_or_table()
    perceptron_batch_gd_misclass_loss()
    q4_mlp()
    q5_regression_gd()
    q5a_cnn_dims()
    q5b_conv_pool()
    q6_mlp_digits()
    q7_cnn_keras()
    q8_rnn()
    q9_lstm()
    print()


if __name__ == "__main__":
    main()
