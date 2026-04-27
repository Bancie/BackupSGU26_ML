"""
PER-4375 — Phần 3: Câu 3.1 (PER-4340) … 3.4 (PER-4364).

Chạy: python cau3_phan3_per4375.py
Giải tay: mục «Phần 3» trong `README.md` cùng thư mục.
"""

from __future__ import annotations

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_recall_fscore_support,
)

# --- 3.1: đa lớp A, B, C (PER-4340) ---
Y31_TRUE = list("ABCABCABCA")
Y31_PRED = list("ACCBBAABCC")
LABELS_31 = ["A", "B", "C"]


# --- 3.2: nhị phân P = positive, N = negative (PER-4346) ---
Y32_TRUE = ["P", "N", "P", "P", "N", "N", "P", "N", "P", "N"]
Y32_PRED = ["P", "N", "N", "P", "P", "N", "P", "N", "N", "P"]
POS_32 = "P"


# --- 3.3: quy tắc (PER-4356) ---


def predict_play_33(outlook: str, windy: bool) -> str:
    """
    1) outlook == overcast -> yes
    2) else if windy == True -> no
    3) else if outlook == sunny -> no
    4) else -> yes
    """
    if outlook == "overcast":
        return "yes"
    if windy is True:
        return "no"
    if outlook == "sunny":
        return "no"
    return "yes"


# (outlook, windy, play_thực) — 14 mẫu theo đề
SAMPLES_33: list[tuple[str, bool, str]] = [
    ("sunny", False, "no"),
    ("sunny", True, "no"),
    ("overcast", False, "yes"),
    ("rainy", False, "yes"),
    ("rainy", False, "yes"),
    ("rainy", True, "no"),
    ("overcast", True, "yes"),
    ("sunny", False, "no"),
    ("sunny", False, "yes"),
    ("rainy", False, "yes"),
    ("sunny", True, "yes"),
    ("overcast", True, "yes"),
    ("overcast", False, "yes"),
    ("rainy", True, "no"),
]


def run_3_1() -> None:
    print("=" * 70)
    print("Câu 3.1 (PER-4340) — đa lớp A, B, C  (n=10)")
    print("=" * 70)
    y_t = np.array(Y31_TRUE)
    y_p = np.array(Y31_PRED)
    cm = confusion_matrix(y_t, y_p, labels=LABELS_31)
    print("Nhãn thực: ", "".join(Y31_TRUE))
    print("Nhãn dự:   ", "".join(Y31_PRED))
    print("Ma trận nhầm lẫn (hàng=thực, cột=dự):")
    print("     ", "  ".join(LABELS_31))
    for i, row in zip(LABELS_31, cm):
        print(f"  {i}", row)
    acc = accuracy_score(y_t, y_p)
    print(f"Accuracy: {acc} = {int(acc * 10)}/10")
    print("\nPer-class (macro trung bình cũng in trong bảng sklearn):")
    print(classification_report(y_t, y_p, labels=LABELS_31, digits=4))
    p, r, f, _ = precision_recall_fscore_support(
        y_t, y_p, labels=LABELS_31, average=None, zero_division=0
    )
    for lab, pp, rr, ff in zip(LABELS_31, p, r, f):
        print(f"  {lab}: P={pp:.4f}  R={rr:.4f}  F1={ff:.4f}")
    print()


def run_3_2() -> None:
    print("=" * 70)
    print("Câu 3.2 (PER-4346) — nhị phân (P=positive, N=negative), n=10")
    print("=" * 70)
    y_t = np.array(Y32_TRUE)
    y_p = np.array(Y32_PRED)
    pos, neg = POS_32, "N" if POS_32 == "P" else "P"
    cm = confusion_matrix(y_t, y_p, labels=[pos, neg])
    print("Nhãn thực: ", " ".join(Y32_TRUE))
    print("Nhãn dự:   ", " ".join(Y32_PRED))
    print(f"Ma trận (hàng=thực, cột=dự) — hàng cột: [{pos}, {neg}]")
    print(cm)
    # TP, FP, FN, TN với P positive: sklearn rows first label = P
    # cm[i,j]: actual i, pred j. Row P col P = TP, Row P col N = FN, Row N col P = FP, Row N col N = TN
    tp = cm[0, 0]
    fn = cm[0, 1]
    fp = cm[1, 0]
    tn = cm[1, 1]
    print(f"TP={tp}  FP={fp}  FN={fn}  TN={tn}")
    acc = accuracy_score(y_t, y_p)
    p = tp / (tp + fp) if (tp + fp) else 0.0
    r = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * p * r / (p + r) if (p + r) else 0.0
    print(f"Accuracy:  {acc}")
    print(f"Precision: {p}")
    print(f"Recall:    {r}")
    print(f"F1:        {f1}")
    print()


def run_3_3() -> None:
    print("=" * 70)
    print("Câu 3.3 (PER-4356) — decision list + 14 mẫu, positive = play=yes")
    print("=" * 70)
    y_true: list[str] = []
    y_pred: list[str] = []
    for i, (out, wind, play_act) in enumerate(SAMPLES_33, start=1):
        pred = predict_play_33(out, wind)
        y_true.append(play_act)
        y_pred.append(pred)
        mark = "OK" if pred == play_act else "SAI"
        print(f"  {i:2d}  outlook={out!s:8s}  windy={wind!s:5s}  dự={pred!s:3s}  thực={play_act!s:3s}  {mark}")
    y_t = np.array(y_true)
    y_p = np.array(y_pred)
    # positive class yes
    pos_label = "yes"
    labels = [pos_label, "no"]
    cm = confusion_matrix(y_t, y_p, labels=labels)
    print("\nConfusion (hàng=thực, cột=dự), positive=yes:")
    print("       dự: yes  no")
    for lab, row in zip(labels, cm):
        print(f"  thực {lab:3s}  {row[0]:4d}  {row[1]:4d}")
    # Row order: actual yes first, then no (labels = [yes, no])
    tp, fn = int(cm[0, 0]), int(cm[0, 1])
    fp, tn = int(cm[1, 0]), int(cm[1, 1])
    print(f"TP={tp}  FP={fp}  FN={fn}  TN={tn}")
    acc = accuracy_score(y_t, y_p)
    prec = tp / (tp + fp) if (tp + fp) else 0.0
    rec = tp / (tp + fn) if (tp + fn) else 0.0
    spec = tn / (tn + fp) if (tn + fp) else 0.0
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) else 0.0
    print(f"Accuracy:     {acc}  ({int(acc * 14)}/14)")
    print(f"Precision:    {prec}")
    print(f"Recall=Sens:  {rec}")
    print(f"Specificity:  {spec}")
    print(f"F1:           {f1}")
    print()


def run_3_4() -> None:
    print("=" * 70)
    print("Câu 3.4 (PER-4364) — từ ma trận: TP, FP, TN, FN")
    print("=" * 70)
    tp, fp, tn, fn = 100, 10, 50, 5
    n = tp + fp + tn + fn
    assert n == 165
    acc = (tp + tn) / n
    mis = (fp + fn) / n
    tpr = tp / (tp + fn)  # = recall, sensitivity
    fpr = fp / (fp + tn)
    tnr = tn / (tn + fp)  # = specificity
    prec = tp / (tp + fp)
    rec = tpr
    sens = tpr
    spec = tnr
    prev = (tp + fn) / n
    print(f"N = {n}  (TP+TN+FP+FN)")
    print(
        f"Accuracy:              {acc:.6f}  = (TP+TN)/N = ({tp}+{tn})/{n}"
    )
    print(f"Misclassification rate: {mis:.6f}  = (FP+FN)/N = ({fp}+{fn})/{n}  = 1−accuracy")
    print(f"TPR ( = recall = sens): {tpr:.6f}  = TP/(TP+FN) = {tp}/({tp}+{fn})")
    print(f"FPR:                   {fpr:.6f}  = FP/(FP+TN) = {fp}/({fp}+{tn})")
    print(f"TNR ( = specificity):   {tnr:.6f}  = TN/(TN+FP) = {tn}/({tn}+{fp})")
    print(f"Precision:             {prec:.6f}  = TP/(TP+FP) = {tp}/({tp}+{fp})")
    print(f"Recall:                {rec:.6f}  = TPR")
    print(f"Sensitivity:           {sens:.6f}  = TPR")
    print(f"Specificity:           {spec:.6f}  = TNR")
    print(f"Prevalence:            {prev:.6f}  = (TP+FN)/N = (P thực tế) = ({tp}+{fn})/{n}")
    print()


if __name__ == "__main__":
    run_3_1()
    run_3_2()
    run_3_3()
    run_3_4()
