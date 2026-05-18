#!/usr/bin/env python3
"""Đối chiếu số cho PER-4806 — chạy: python verify_exercises.py (trong thư mục code)."""

from __future__ import annotations

from datasets import (
    LEAF_FEATURES,
    LOAN_C45_FEATURES,
    LOAN_FEATURES,
    SEASON_FEATURES,
    leaf_dataset,
    loan_c45_dataset,
    loan_dataset,
    seasonal_test_XY,
    seasonal_training,
)
from categorical_tree import fit, predict_one, print_tree
from metrics import entropy, gain


def summarize_root_entropy(df, target: str, features: list[str], banner: str) -> None:
    print(f"\n--- {banner} ---")
    print(f"H(tập) entropy (log₂) = {entropy(df[target].tolist()):.6f}")
    for name in sorted(features, key=lambda x: str(x)):
        _ip, weighted, gn = gain(df, name, target, "entropy")
        print(f"  {name}: entropy có trọng số = {weighted:.6f}; gain = {gn:.6f}")


def summarize_branch_all_criteria(df, target: str, features: list[str], banner: str) -> None:
    print(f"\n--- {banner} ---")
    for crit in ("entropy", "gini", "error"):
        print(f"* {crit.upper()}")
        for name in sorted(features, key=lambda x: str(x)):
            _ip, weighted, gn = gain(df, name, target, crit)  # type: ignore[arg-type]
            if crit == "entropy":
                lbl = ("entropy có trọng số", "gain")
            elif crit == "gini":
                lbl = ("Gini có trọng số", "Δ(Gini_impurity)")
            else:
                lbl = ("lỗi có trọng số", "Δ(lỗi)")
            print(f"    {name}: {lbl[0]} = {weighted:.6f}; {lbl[1]} = {gn:.6f}")


def main() -> None:
    print("=" * 62)
    print("4.1.1 — Dự báo mùa (12 mẫu huấn luyện)")

    df = seasonal_training()
    summarize_root_entropy(df, "Mùa", list(SEASON_FEATURES), "Lần 1 — toàn mẫu")

    tb = df[df["Nhiệt độ"] == "Trung bình"]
    summarize_branch_all_criteria(
        tb,
        "Mùa",
        ["Thời tiết", "Lá cây"],
        "Lần 2 — nhánh «Nhiệt độ = Trung bình»",
    )

    feat_season = list(SEASON_FEATURES)
    entr = fit(df, feat_season, "Mùa", "entropy")
    print("\nCấu trúc cây ID3 (Information Gain / entropy):")
    print_tree(entr)

    print("\n(b) — Dự báo X và Y:")
    tst = seasonal_test_XY()
    for _, r in tst.iterrows():
        feats = tuple((f, r[f]) for f in feat_season)
        pred = predict_one(entr, r)
        print(f"  Mẫu {r['Mẫu']}: {feats}  -> {pred}")

    print("\n(c) — So khớp dự báo X, Y giữa entropy / gini / error:")
    pred_x_e = predict_one(entr, tst.iloc[0])
    pred_y_e = predict_one(entr, tst.iloc[1])
    for crit in ("gini", "error"):
        tr = fit(df, feat_season, "Mùa", crit)
        px = predict_one(tr, tst.iloc[0])
        py = predict_one(tr, tst.iloc[1])
        print(
            f"  {crit}: X={px}, Y={py}; giống entropy? "
            f"{px == pred_x_e and py == pred_y_e}"
        )

    print("\n" + "=" * 62)
    print("4.1.2 — Độc / không độc (10 mẫu học)")
    ldf = leaf_dataset()
    tr_leaves = ldf[ldf["Độc"].notna()].copy()
    feats_leaf = list(LEAF_FEATURES)
    summarize_branch_all_criteria(tr_leaves, "Độc", feats_leaf, "gốc (trước khi chia)")

    for crit in ("gini", "entropy", "error"):
        tr = fit(tr_leaves, feats_leaf, "Độc", crit)
        lab = {"gini": "Gini", "entropy": "Entropy", "error": "lỗi phân loại"}[crit]
        print(f"\n--- Cây theo {lab} ---")
        print_tree(tr)
        for sid in ("11", "12"):
            row = ldf[ldf["Mẫu"] == sid].iloc[0]
            print(f"  Dự báo mẫu {sid}: {predict_one(tr, row)}")

    print("\n" + "=" * 62)
    print("4.1.3 — Quyết định cho vay (10 mẫu học)")
    mdf = loan_dataset()
    train_m = mdf[mdf["Quyết định"].notna()].copy()
    feats_m = list(LOAN_FEATURES)

    summarize_branch_all_criteria(
        train_m, "Quyết định", feats_m, "gốc (trước khi chia)"
    )

    for crit in ("error", "gini", "entropy"):
        tr = fit(train_m, feats_m, "Quyết định", crit)
        lbl = {"error": "lỗi phân loại", "gini": "Gini", "entropy": "Entropy"}[crit]
        print(f"\n--- Cây theo «{lbl}» ---")
        print_tree(tr)
        for sid in ("A", "B"):
            row = mdf[mdf["Mẫu"] == sid].iloc[0]
            print(f"  Mẫu {sid}: {predict_one(tr, row)}")

    print("\n" + "=" * 62)
    print("4.1.4 — Hồ sơ vay (15 mẫu; Information Gain = entropy gain / ID3-style)")
    cdf = loan_c45_dataset()
    feats_c = list(LOAN_C45_FEATURES)

    summarize_branch_all_criteria(cdf, "Class", feats_c, "gốc — Information Gain")

    tree_c45 = fit(cdf, feats_c, "Class", "entropy")
    print("\nCây (entropy / Information Gain):")
    print_tree(tree_c45)

    print("\n" + "=" * 62)


if __name__ == "__main__":
    main()
