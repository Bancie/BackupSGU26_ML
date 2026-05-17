#!/usr/bin/env python3
"""PER-4784 — đối chiếu đáp án. Chạy: python verify_exercises.py (trong thư mục code)."""

from __future__ import annotations

import numpy as np

from datasets import (
    COVID_FEATURE_NAMES,
    COVID_KS,
    COVID_WEIGHTED_K,
    COVID_X,
    COVID_Y,
    COVID_TEST,
    Q1_TEST,
    Q1_X,
    Q1_Y,
    Q2_K,
    Q2_TEST,
    Q2_X,
    Q2_Y,
    Q3_K,
    Q3_TEST,
    Q3_X,
    Q3_Y,
    Q4_TEST,
    Q4_X,
    Q4_Y,
    Q5_BETA0,
    Q5_BETA1,
    Q5_QUERY_X,
    Q5_TAU,
    Q5_X1,
    Q5_Y,
)
from similarity import (
    euclidean,
    hamming,
    knn_predict,
    lwr_gaussian_weights,
    lwr_linear_predict,
    minmax_fit_transform,
    nearest_centroid_predict,
    weighted_knn_predict,
)


def _print_q1() -> None:
    print("=" * 72)
    print("CÂU 1 — k-NN cơ bản (Euclidean), test (6.5, 55, 5)")
    _, sorted_all = knn_predict(Q1_X, Q1_Y, Q1_TEST, k=len(Q1_X), dist_fn=euclidean)
    print("\nKhoảng cách tới từng mẫu (đã sort tăng dần):")
    for idx, d, lab in sorted_all:
        print(f"  mẫu {idx + 1}: d = {d:.6f}  nhãn = {lab}")
    for k in (3, 1, 5):
        pred, neigh = knn_predict(Q1_X, Q1_Y, Q1_TEST, k=k)
        print(f"\n  k = {k}: 3 (hoặc k) láng giềng gần nhất:")
        for rank, (idx, d, lab) in enumerate(neigh[:k], 1):
            print(f"    #{rank} mẫu {idx + 1}: d={d:.6f} -> {lab}")
        print(f"  → Dự đoán đa số: {pred}")


def _print_q2() -> None:
    print("\n" + "=" * 72)
    print(f"CÂU 2 — k = {Q2_K}; test (172, 80)")
    pred_raw, sort_raw = knn_predict(Q2_X, Q2_Y, Q2_TEST, k=Q2_K)
    print("\n(1) Không chuẩn hóa — khoảng cách sort:")
    for idx, d, lab in sort_raw:
        print(f"  mẫu {idx + 1}: d = {d:.6f}  {lab}")
    print(f"  → Dự đoán: {pred_raw}")

    tr, te = minmax_fit_transform(Q2_X, Q2_TEST.reshape(1, -1))
    te = te.ravel()
    print("\n(2) Min–Max trên tập huấn luyện; train transformed:")
    print(" ", tr)
    print("  test transformed:", te)
    pred_mm, sort_mm = knn_predict(tr, Q2_Y, te, k=Q2_K)
    print("\n(3) Sau chuẩn hóa — khoảng cách sort:")
    for idx, d, lab in sort_mm:
        print(f"  mẫu {idx + 1}: d = {d:.6f}  {lab}")
    print(f"  → Dự đoán: {pred_mm}")
    print("\n(4) So sánh: trước SCALE =", pred_raw, "| sau SCALE =", pred_mm)


def _print_q3() -> None:
    print("\n" + "=" * 72)
    print("CÂU 3 — Weighted k-NN, k=3, test (6,6)")
    pred_std, sort_all = knn_predict(Q3_X, Q3_Y, Q3_TEST, k=Q3_K)
    print("\nk-NN thường (đa số), 3 láng giềng:")
    for rank, (idx, d, lab) in enumerate(sort_all[: Q3_K], 1):
        print(f"  #{rank} điểm ({Q3_X[idx][0]:g},{Q3_X[idx][1]:g}) d={d:.6f} -> {lab}")
    print(f"  → Dự đoán: {pred_std}")

    pred_w, triples = weighted_knn_predict(Q3_X, Q3_Y, Q3_TEST, Q3_K, dist_fn=euclidean, inverse_power=1)
    print("\nWeighted k-NN: w_i = (1/d_i) / sum(1/d_j) trên 3 láng giềng:")
    agg = {}
    for idx, d, wn, lab in triples:
        print(f"  mẫu {idx + 1}: d={d:.6f}  w'={wn:.6f} -> {lab}")
        agg[lab] = agg.get(lab, 0.0) + wn
    print("  Tổng w' theo lớp:", dict(sorted(agg.items(), key=str)))
    print(f"  → Dự đoán (weighted): {pred_w}")


def _print_q4() -> None:
    print("\n" + "=" * 72)
    print("CÂU 4 — Nearest centroid, test (6,5)")
    pred, centroids, cdist = nearest_centroid_predict(Q4_X, Q4_Y, Q4_TEST)
    for c in sorted(centroids, key=str):
        cx, cy = centroids[c]
        print(f"  Centroid lớp {c}: ({cx:.6f}, {cy:.6f})  | d(test)={cdist[c]:.6f}")
    print(f"  → Dự đoán: {pred}")


def _print_q5() -> None:
    print("\n" + "=" * 72)
    print("CÂU 5 — LWR / kernel Gaussian, x_query = 2.5, tau = 1")
    h0 = Q5_BETA0 + Q5_BETA1 * Q5_QUERY_X
    print(f"\n(1) h(x) = {Q5_BETA0} + {Q5_BETA1} x  =>  h({Q5_QUERY_X}) = {h0:.6f}")
    print("\n(2) |x_i - x_query|:")
    for i, xi in enumerate(Q5_X1):
        print(f"  i={i + 1}: x_i={xi:g}  |d|={abs(xi - Q5_QUERY_X):.6f}")
    w = lwr_gaussian_weights(Q5_X1, Q5_QUERY_X, Q5_TAU)
    print(f"\n(3) w_i = exp(-(x_i - x)^2 / (2 tau^2)), tau={Q5_TAU}:")
    for i, wi in enumerate(w):
        print(f"  i={i + 1}: w_i = {wi:.6f}")
    y_hat = lwr_linear_predict(Q5_X1, Q5_Y, Q5_QUERY_X, w)
    print(f"\n(4 bổ sung đề) Hồi quy tuyến tính có trọng số (LWR) tại x={Q5_QUERY_X}: y_hat = {y_hat:.6f}")


def _print_q6() -> None:
    print("\n" + "=" * 72)
    print("CÂU 6 — COVID symptoms, Hamming, test binary 111100000")
    print("Mã hóa Yes=1 No=0 (mẫu test đã cho).")
    dist_rows = []
    for i in range(len(COVID_X)):
        d = hamming(COVID_X[i], COVID_TEST)
        dist_rows.append((i, d, COVID_Y[i]))
    dist_rows.sort(key=lambda t: (t[1], str(t[2])))
    print("\nHamming distance (sort):")
    for idx, d, lab in dist_rows:
        print(f"  ID {idx + 1}: d={d:g}  -> {lab}")

    for k in COVID_KS:
        pred, neigh = knn_predict(COVID_X, COVID_Y, COVID_TEST, k=k, dist_fn=hamming)
        labs = [n[2] for n in neigh[:k]]
        print(f"\n  k = {k}: láng giềng {labs}  → đa số: {pred}")

    print(f"\nWeighted k-NN (k={COVID_WEIGHTED_K}, w=1/d, chuẩn hóa):")
    pred_w, triples = weighted_knn_predict(
        COVID_X, COVID_Y, COVID_TEST, COVID_WEIGHTED_K, dist_fn=hamming, inverse_power=1
    )
    agg = {}
    for idx, d, wn, lab in triples:
        print(f"  ID {idx + 1}: d={d:g}  w'={wn:.6f} -> {lab}")
        agg[lab] = agg.get(lab, 0.0) + wn
    print("  Tổng w' theo lớp:", dict(sorted(agg.items(), key=str)))
    print(f"  → Dự đoán: {pred_w}")


def _symptom_stats() -> None:
    print("\n" + "=" * 72)
    print("PHÂN TÍCH (đề) — tần suất triệu chứng = 1 trong tập huấn luyện")
    pos_mask = COVID_Y == "Positive"
    neg_mask = COVID_Y == "Negative"
    xp = COVID_X[pos_mask].sum(axis=0)
    xn = COVID_X[neg_mask].sum(axis=0)
    np_ = pos_mask.sum()
    nn = neg_mask.sum()
    print(f"  Số mẫu Positive: {np_}, Negative: {nn}")
    print("\n  Tổng 'Yes' (1) theo triệu chứng:")
    for j, name in enumerate(COVID_FEATURE_NAMES):
        print(f"    {name}: Positive_sum={int(xp[j])}/{np_}  Negative_sum={int(xn[j])}/{nn}")


def main() -> None:
    _print_q1()
    _print_q2()
    _print_q3()
    _print_q4()
    _print_q5()
    _print_q6()
    _symptom_stats()
    print("\n" + "=" * 72)
    print("Hoàn thành.")


if __name__ == "__main__":
    main()
