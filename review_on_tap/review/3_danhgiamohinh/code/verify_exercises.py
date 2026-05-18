"""
Kiểm tra số cho Câu 3.1–3.4 (đánh giá mô hình).
Chạy: python verify_exercises.py
"""

from __future__ import annotations

import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)


def cm_table(cm: pd.DataFrame) -> None:
    print(cm.to_string())
    print()


# --- Câu 3.1: 3 lớp ---
def problem_3_1() -> None:
    labels = ["A", "B", "C"]
    y_true = list("ABCABCABCA")
    y_pred = list("ACCBBAABCC")

    cm = confusion_matrix(y_true, y_pred, labels=labels)
    df = pd.DataFrame(cm, index=[f"Lớp {l}" for l in labels], columns=labels)

    print("=== Câu 3.1 ===")
    print("Ma trận nhầm lẫn (hàng: thực tế, cột: dự đoán):")
    cm_table(df)

    acc = accuracy_score(y_true, y_pred)
    print(f"Độ chính xác tổng thể (accuracy): {acc} (= {accuracy_score(y_true, y_pred) * 10:.0f}/10)")
    prec = precision_score(y_true, y_pred, labels=labels, average=None, zero_division=0)
    rec = recall_score(y_true, y_pred, labels=labels, average=None, zero_division=0)
    f1 = f1_score(y_true, y_pred, labels=labels, average=None, zero_division=0)
    for i, lbl in enumerate(labels):
        print(
            f"  Lớp {lbl}: Precision={prec[i]}, Recall={rec[i]}, F1={f1[i]}"
        )
    print()


# --- Câu 3.2: nhị phân P/N, lớp dương = P ---
def problem_3_2() -> None:
    labels = ["P", "N"]
    y_true = list("PNPPNNPNNP")
    y_pred = list("PNNPPNPNNP")

    cm = confusion_matrix(y_true, y_pred, labels=labels)
    df = pd.DataFrame(cm, index=[f"Thực {l}" for l in labels], columns=[f"Dự đoán {l}" for l in labels])

    print("=== Câu 3.2 ===")
    print("Ma trận nhầm lẫn (hàng: thực tế, cột: dự đoán), lớp dương = P:")
    cm_table(df)

    # Ma trận chuẩn binary với positive = P: [[TN, FP], [FN, TP]] nếu labels [N, P]
    cm_np = confusion_matrix(y_true, y_pred, labels=["N", "P"])
    tn, fp, fn, tp = cm_np.ravel()
    print(f"TP (P so với P) = {tp}, FP (N dự đoán P) = {fp}")
    print(f"FN (P dự đoán N) = {fn}, TN (N so với N) = {tn}")
    print()

    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, pos_label="P", zero_division=0)
    rec = recall_score(y_true, y_pred, pos_label="P", zero_division=0)
    f1 = f1_score(y_true, y_pred, pos_label="P", zero_division=0)
    print(f"Accuracy = {acc}")
    print(f"Precision (P) = {prec}")
    print(f"Recall (P) = {rec}")
    print(f"F1 (P) = {f1}")
    print()


def predict_play_row(outlook: str, windy: bool) -> str:
    """Decision list đề cho: thứ tự cố định."""
    if outlook == "overcast":
        return "yes"
    if windy:
        return "no"
    if outlook == "sunny":
        return "no"
    return "yes"


def problem_3_3() -> None:
    rows = [
        ("sunny", 85.0, 85.0, False, "no"),
        ("sunny", 80.0, 90.0, True, "no"),
        ("overcast", 83.0, 86.0, False, "yes"),
        ("rainy", 70.0, 96.0, False, "yes"),
        ("rainy", 68.0, 80.0, False, "yes"),
        ("rainy", 65.0, 70.0, True, "no"),
        ("overcast", 64.0, 65.0, True, "yes"),
        ("sunny", 72.0, 95.0, False, "no"),
        ("sunny", 69.0, 70.0, False, "yes"),
        ("rainy", 75.0, 80.0, False, "yes"),
        ("sunny", 75.0, 70.0, True, "yes"),
        ("overcast", 72.0, 90.0, True, "yes"),
        ("overcast", 81.0, 75.0, False, "yes"),
        ("rainy", 71.0, 91.0, True, "no"),
    ]

    df = pd.DataFrame(
        rows,
        columns=["outlook", "temperature", "humidity", "windy", "play"],
    )

    preds = []
    for _, r in df.iterrows():
        preds.append(predict_play_row(str(r["outlook"]), bool(r["windy"])))
    df["pred_play"] = preds
    df["ok"] = df["play"] == df["pred_play"]

    print("=== Câu 3.3 ===")
    print("Luật: (1) overcast→yes (2) else windy→no (3) else sunny→no (4) else→yes")
    print()

    print("STT | outlook   | windy | play (thực) | play (dự đoán) | khớp")
    for i in range(len(df)):
        ro = df.iloc[i]
        print(
            f"{i + 1:3d} | {ro['outlook']:<9} | {str(ro['windy']):5} | "
            f"{ro['play']:<11} | {ro['pred_play']:<14} | {ro['ok']}"
        )
    print()

    y_true = df["play"].tolist()
    y_pred = df["pred_play"].tolist()
    labels_yesno = ["no", "yes"]
    cm = confusion_matrix(y_true, y_pred, labels=labels_yesno)
    cm_df = pd.DataFrame(
        cm,
        index=[f"Thực {l}" for l in labels_yesno],
        columns=[f"Dự đoán {l}" for l in labels_yesno],
    )
    print("Ma trận nhầm lẫn (hàng: thực tế, cột: dự đoán), lớp dương = yes:")
    cm_table(cm_df)

    cm_y = confusion_matrix(y_true, y_pred, labels=["yes", "no"])
    tp, fn, fp, tn = cm_y.ravel()
    print(f"TP (yes/yes) = {tp}, FP (no→yes) = {fp}, FN (yes→no) = {fn}, TN (no/no) = {tn}")
    print()

    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, pos_label="yes", zero_division=0)
    rec = recall_score(y_true, y_pred, pos_label="yes", zero_division=0)
    spec = tn / (tn + fp) if (tn + fp) else 0.0
    f1 = f1_score(y_true, y_pred, pos_label="yes", zero_division=0)

    print(f"Accuracy = {acc}")
    print(f"Precision (yes) = {prec}")
    print(f"Recall / Sensitivity (yes) = {rec}")
    print(f"Specificity (yes) = {spec}  (= TN/(TN+FP))")
    print(f"F1 (yes) = {f1}")
    print()


def problem_3_4() -> None:
    tp, tn, fp, fn = 100, 50, 10, 5
    n = tp + tn + fp + fn

    acc = (tp + tn) / n
    mis = 1.0 - acc
    tpr = tp / (tp + fn)
    fpr = fp / (fp + tn)
    tnr = tn / (tn + fp)
    prec = tp / (tp + fp)
    rec = tp / (tp + fn)
    sens = rec
    spec = tn / (tn + fp)
    prev = (tp + fn) / n

    print("=== Câu 3.4 ===")
    print(f"TN={tn}, FP={fp}, FN={fn}, TP={tp}, N={n}")
    print(f"Accuracy = (TP+TN)/N = {acc}")
    print(f"Misclassification rate = 1 - Accuracy = {mis}")
    print(f"TPR = Recall = Sensitivity = TP/(TP+FN) = {tpr}")
    print(f"FPR = FP/(FP+TN) = {fpr}")
    print(f"TNR = Specificity = TN/(TN+FP) = {tnr}")
    print(f"Precision = TP/(TP+FP) = {prec}")
    print(f"Prevalence = (TP+FN)/N = {prev}")
    print()


def main() -> None:
    problem_3_1()
    problem_3_2()
    problem_3_3()
    problem_3_4()


if __name__ == "__main__":
    main()
