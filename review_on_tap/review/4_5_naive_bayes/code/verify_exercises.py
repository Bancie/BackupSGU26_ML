#!/usr/bin/env python3
"""PER-4810 — đối chiếu đáp án. Chạy: python verify_exercises.py (trong thư mục code)."""

from __future__ import annotations

import math

from bayes import CategoricalNB, GaussianHybridNB, MultinomialNBWords, compute_class_priors_log
from datasets import (
    BANK_FEATURE_CAT,
    BANK_FEATURE_NUM,
    BANK_ROWS,
    BANK_TARGET,
    BANK_TEST,
    EMAIL_LABELS,
    EMAIL_TEST_E4,
    EMAIL_TRAIN,
    Q1_ROWS,
    Q2_ROWS,
    Q2_TEST_B,
    WORD_NAMES,
    q1_split,
)


def _print_bank() -> None:
    print("=" * 70)
    print("CÂU 4.5.1 — Tín dụng (Tuổi, Thu nhập, Số tiền vay: Gaussian; Gia đình: rời rạc), α = 1")
    alpha = 1.0
    norm_rows = []
    for r in BANK_ROWS:
        nr = dict(r)
        nr[BANK_TARGET] = str(nr[BANK_TARGET]).lower()
        norm_rows.append(nr)
    classes = sorted({r[BANK_TARGET] for r in norm_rows})
    priors = compute_class_priors_log(norm_rows, BANK_TARGET, classes, alpha=alpha)

    print("\n--- (a) Prior P(Kết quả) ---")
    for c in classes:
        print(f"  P(Kết quả={c}) = exp({priors[c]:.6f}) = {math.exp(priors[c]):.6f}")

    g = GaussianHybridNB(
        alpha=alpha,
        categorical_features=BANK_FEATURE_CAT,
        numeric_features=BANK_FEATURE_NUM,
    )
    g.fit(BANK_ROWS, BANK_TARGET)

    print("\n--- (a) Gaussian: μ và σ (mẫu, ddof=1) ---")
    for c in g.classes_:
        print(f"  Lớp {c}:")
        for f in g.num_cols:
            print(f"    {f}: μ = {g._mu[c][f]:.6f}, σ = {g._sigma[c][f]:.6f}")

    print("\n--- (a) Likelihood rời rạc P(Gia đình | Kết quả) ---")
    assert g._cat is not None
    for c in g.classes_:
        print(f"\n  Lớp {c}:")
        for v, lv in sorted(g._cat.cond_log_prob[c]["Gia đình"].items(), key=lambda x: str(x[0])):
            print(f"    P(Gia đình={v!r} | {c}) = {math.exp(lv):.6f}")

    x_test = {
        "Gia đình": BANK_TEST["Gia đình"],
        "Tuổi": BANK_TEST["Tuổi"],
        "Thu nhập": BANK_TEST["Thu nhập"],
        "Số tiền vay": BANK_TEST["Số tiền vay"],
    }
    print("\n--- Phân lớp mẫu mới (23, Có, 32, 250) ---")
    sc = g.predict_log_scores(x_test, priors)
    for c in classes:
        print(f"  log score Kết quả={c}: {sc[c]:.6f}")
    pred = g.predict_one(x_test, priors)
    print(f"  → Dự đoán (chữ thường nội bộ): {pred}")


def _print_q1() -> None:
    print("\n" + "=" * 70)
    print("CÂU 4.5.2 — Tennis (thuộc tính rời rạc), Laplace α = 1")
    target = "Play"
    feat_cols = q1_split()
    alpha = 1.0
    model = CategoricalNB(alpha=alpha)
    model.fit(Q1_ROWS, feat_cols, target)

    print("\n--- (a) Prior P(Play) ---")
    for c in model.classes_:
        p = math.exp(model.class_prior_log_[c])
        print(f"  P(Play={c}) = exp({model.class_prior_log_[c]:.6f}) = {p:.6f}")

    print("\n--- (a) Likelihood P(thuộc tính = giá trị | Play) ---")
    for c in model.classes_:
        print(f"\n  Lớp Play = {c}:")
        for f in feat_cols:
            print(f"    {f}:")
            for v, lv in sorted(model.cond_log_prob[c][f].items(), key=lambda x: str(x[0])):
                print(f"      P({f}={v!r} | {c}) = {math.exp(lv):.6f}")

    x_b = {"Outlook": "Sunny", "Temp": "Cool", "Humidity": "High", "Windy": True}
    print("\n--- (b) Mẫu (Sunny, Cool, High, Windy=True) ---")
    scores_b = model.predict_log_proba_dict(x_b)
    for c in model.classes_:
        print(f"  log score Play={c}: {scores_b[c]:.6f}")
    pred_b = model.predict_one(x_b)
    print(f"  → Dự đoán: {pred_b}")

    x_c = {"Outlook": "Sunny", "Temp": "Cool", "Humidity": "High", "Windy": True}
    print("\n--- (c) Outlook thiếu (?, Cool, High, Windy=True) — bỏ hệ số Outlook ---")
    scores_c = model.predict_log_proba_dict(x_c, skip_features={"Outlook"})
    for c in model.classes_:
        print(f"  log score Play={c}: {scores_c[c]:.6f}")
    pred_c = model.predict_one(x_c, skip_features={"Outlook"})
    print(f"  → Dự đoán: {pred_c}")


def _print_q2() -> None:
    print("\n" + "=" * 70)
    print("CÂU 4.5.3 — Tennis (nhiệt độ & độ ẩm số), Gaussian + Laplace rời rạc, α = 1")
    tgt = "Play"
    alpha = 1.0
    norm_rows = []
    for r in Q2_ROWS:
        nr = dict(r)
        nr[tgt] = str(nr[tgt]).lower()
        norm_rows.append(nr)

    classes = sorted({r[tgt] for r in norm_rows})
    priors = compute_class_priors_log(norm_rows, tgt, classes, alpha=alpha)
    print("\n--- (a) Prior P(Play) ---")
    for c in classes:
        print(f"  P(Play={c}) = exp({priors[c]:.6f}) = {math.exp(priors[c]):.6f}")

    g = GaussianHybridNB(alpha=alpha)
    g.fit(Q2_ROWS, tgt)

    print("\n--- (a) Gaussian: μ và σ (mẫu, ddof=1) cho Temperature, Humidity ---")
    for c in g.classes_:
        print(f"  Lớp {c}:")
        for f in g.num_cols:
            print(f"    {f}: μ = {g._mu[c][f]:.6f}, σ = {g._sigma[c][f]:.6f}")

    print("\n--- (a) Likelihood rời rạc P(Outlook), P(Windy) | Play ---")
    cat_nb = g._cat
    assert cat_nb is not None
    for c in g.classes_:
        print(f"\n  Lớp Play = {c}:")
        for f in g.cat_cols:
            for v, lv in sorted(cat_nb.cond_log_prob[c][f].items(), key=lambda x: str(x[0])):
                print(f"    P({f}={v!r} | {c}) = {math.exp(lv):.6f}")

    x_t = dict(Q2_TEST_B)
    print("\n--- (b) Mẫu kiểm tra (sunny, 66, 90, Windy=True) ---")
    sc = g.predict_log_scores(x_t, priors)
    for c in classes:
        print(f"  log score Play={c}: {sc[c]:.6f}")
    pred = g.predict_one(x_t, priors)
    print(f"  → Dự đoán: {pred}")


def _print_q3() -> None:
    print("\n" + "=" * 70)
    print("CÂU 4.5.4 — Email spam, Multinomial NB, V = 7, Laplace α = 1")
    alpha = 1.0
    m = MultinomialNBWords(alpha=alpha)
    m.fit(EMAIL_TRAIN, EMAIL_LABELS, n_classes_prior=2)

    print("\n--- (a) Prior ---")
    for c in m.classes_:
        print(f"  P(class={c}) = exp({m.class_prior_log_[c]:.6f}) = {math.exp(m.class_prior_log_[c]):.6f}")

    print("\n--- (a) P(w_i | class) ---")
    for c in m.classes_:
        print(f"  Lớp {c}:")
        for j, name in enumerate(WORD_NAMES):
            print(f"    P({name}|{c}) = {math.exp(m.word_log_prob[c][j]):.6f}")

    print("\n--- (b) E4 counts:", EMAIL_TEST_E4.tolist(), "---")
    sc = m.predict_log_scores(EMAIL_TEST_E4)
    for c in m.classes_:
        print(f"  log score {c}: {sc[c]:.6f}")
    print(f"  → Dự đoán: {m.predict_one(EMAIL_TEST_E4)}")


def main() -> None:
    _print_bank()
    _print_q1()
    _print_q2()
    _print_q3()
    print("\n" + "=" * 70)
    print("Hoàn thành.")


if __name__ == "__main__":
    main()
