"""Marimo: baseline LR (L2/L1) — Pima, trình bày + visualize.

``marimo edit Lab_03/pima_logistic_baseline_nb.py``

CLI: ``python Lab_03/pima_logistic_baseline.py``

Logic: ``Lab_03/pima_logistic_baseline_core.py``.
"""

import marimo

__generated_with = "0.23.3"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import sys
    from pathlib import Path

    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import seaborn as sns

    _lab_dir = Path(__file__).resolve().parent
    if str(_lab_dir) not in sys.path:
        sys.path.insert(0, str(_lab_dir))

    import pima_logistic_baseline_core as plc
    from sklearn.metrics import RocCurveDisplay, classification_report, confusion_matrix
    from sklearn.model_selection import train_test_split

    plc.apply_sklearn_logistic_warnings_filter()

    try:
        plt.style.use("seaborn-v0_8-whitegrid")
    except OSError:
        plt.style.use("ggplot")
    sns.set_theme(style="whitegrid", palette="Set2")
    return (
        RocCurveDisplay,
        classification_report,
        confusion_matrix,
        np,
        pd,
        plc,
        plt,
        sns,
        train_test_split,
    )


@app.cell
def _(mo):
    mo.md("""
    # Lab 03 — Baseline Logistic Regression (Pima Indians Diabetes)

    ## Mục tiêu

    - So sánh hai baseline: Logistic Regression **L2** (`solver=lbfgs`) và **L1** (`solver=saga`), `C=1.0`.
    - Pipeline **SimpleImputer (median) → StandardScaler → LogisticRegression**.
    - Phân loại nhị phân nhãn `outcome`.

    ## Dữ liệu

    - CSV: `Lab_03/data/pima-indians-diabetes.csv` — 768 quan sát và 8 biến số như mô tả UCI.
    """)
    return


@app.cell
def _(plc):
    data_path = plc.resolve_data_path()
    found = bool(data_path.exists())
    X_raw, y_all = plc.load_xy(data_path)
    X_masked = plc.mask_invalid_zeros(X_raw)

    overview = dict(
        path=str(data_path),
        exists=str(found),
        n=len(y_all),
        zero_masked_cols=list(plc.ZERO_AS_MISSING_COLUMNS),
    )
    return X_masked, overview, y_all


@app.cell
def _(mo, overview, plc):
    mo.md(f"""
    ## Tải và mask zero → NaN

    - Đường dẫn: `{overview["path"]}` — có tệp: **{overview["exists"]}**.
    - Kích thước sau mask (ma trận **X** và vector **y**): **{overview["n"]} × {len(plc.FEATURE_COLUMNS)}**.
    - Cột được `0 → NaN` (giá trị 0 không hợp lý sinh học): `{", ".join(overview["zero_masked_cols"])}`.
    """)
    return


@app.cell
def _(mo, plc):
    mo.md(f"""
    ## Stratified split và định tính L1 / L2

    - `test_size={plc.TEST_SIZE}`, `random_state={plc.RANDOM_STATE}`: tái hiện thí nghiệm và **stratify** để giữ tỉ lệ lớp dương gần tổng thể (~35% trong tài liệu gốc).
    - **L2**: có thể co ép mượt, ít ép hệ số về 0.
    - **L1**: thường chọn **một phần hệ số về đúng 0** (biến thưa trong không gian sau chuẩn hóa).
    """)
    return


@app.cell
def _(X_masked, pd, plc, train_test_split, y_all):
    X_train, X_test, y_train, y_test = train_test_split(
        X_masked,
        y_all,
        test_size=plc.TEST_SIZE,
        stratify=y_all,
        random_state=plc.RANDOM_STATE,
    )

    split_stats = pd.DataFrame(
        {
            "subset": ["train", "test"],
            "n": [len(y_train), len(y_test)],
            "rate_positive": [float(y_train.mean()), float(y_test.mean())],
        }
    ).round({"rate_positive": 4})
    split_stats["rate_positive_%"] = (100 * split_stats["rate_positive"]).round(2)
    return X_test, X_train, split_stats, y_test, y_train


@app.cell
def _(split_stats):
    split_stats
    return


@app.cell
def _(X_train, plc, y_train):
    pipes = {}
    for _ptype in ("l2", "l1"):
        p = plc.make_pipeline(_ptype)
        p.fit(X_train, y_train)
        pipes[_ptype] = p
    return (pipes,)


@app.cell
def _(mo):
    mo.md("""
    ## Metrics hold-out và phân loại chi tiết

    - ROC-AUC trên một mảnh chia nhỏ dao động theo seed; kèm CV bên dưới là hữu ích để nhìn ổn định hơn.
    """)
    return


@app.cell
def _(X_test, pipes, plc, y_test):
    results = {_ptype: plc.compute_test_metrics(pi, X_test, y_test) for _ptype, pi in pipes.items()}
    metrics_wide = plc.build_metrics_comparison_df(results)
    return metrics_wide, results


@app.cell
def _(metrics_wide):
    metrics_wide
    return


@app.cell
def _(classification_report, mo, results, y_test):
    blocks = []
    for _ptype in ("l2", "l1"):
        txt = classification_report(y_test, results[_ptype]["y_pred"], digits=4)
        blocks.append(f"### LR {_ptype.upper()}\n```\n{txt}\n```\n")

    mo.md("\n".join(blocks))
    return


@app.cell
def _(RocCurveDisplay, plt, results, sns, y_test):
    fig_roc, ax_roc = plt.subplots(figsize=(7.2, 5.8))

    l2_label = "LR L2 (AUC = %.4f)" % results["l2"]["roc_auc"]
    l1_label = "LR L1 (AUC = %.4f)" % results["l1"]["roc_auc"]

    RocCurveDisplay.from_predictions(
        y_test,
        results["l2"]["y_prob"],
        name=l2_label,
        ax=ax_roc,
    )
    RocCurveDisplay.from_predictions(
        y_test,
        results["l1"]["y_prob"],
        name=l1_label,
        ax=ax_roc,
    )
    ax_roc.plot([0, 1], [0, 1], linestyle="--", color="grey", lw=1, label="Ngẫu nhiên")
    ax_roc.legend(loc="lower right")
    ax_roc.set_title("ROC trên hold-out test")
    sns.despine(fig=fig_roc)
    plt.tight_layout()
    fig_roc
    return


@app.cell
def _(confusion_matrix, np, plt, results, sns, y_test):
    fig_cm, axes_cm = plt.subplots(1, 2, figsize=(11.6, 4.9), sharey=True)

    titles = ("L2 — tỉ lệ theo nhãn thực", "L1 — tỉ lệ theo nhãn thực")

    for _ax_cm, _ptype, title in zip(axes_cm, ("l2", "l1"), titles):
        cm_counts = confusion_matrix(y_test, results[_ptype]["y_pred"]).astype(float)
        denom = cm_counts.sum(axis=1, keepdims=True)
        denom_safe = np.where(denom > 0, denom, 1.0)
        cm_norm = cm_counts / denom_safe

        sns.heatmap(
            cm_norm,
            annot=True,
            fmt=".3f",
            cmap="Blues",
            vmin=0,
            vmax=1,
            ax=_ax_cm,
            cbar=_ax_cm is axes_cm[1],
            xticklabels=["pred 0", "pred 1"],
            yticklabels=["actual 0", "actual 1"],
        )
        _ax_cm.set_title(title)

    plt.tight_layout()
    sns.despine(fig=fig_cm)
    fig_cm
    return


@app.cell
def _(np, pipes, plc, plt, sns):
    fig_coef, axes_coef = plt.subplots(1, 2, figsize=(13.0, 6.0), sharey=True)

    for _ax_coef, _ptype, color in zip(axes_coef, ("l2", "l1"), ("#4c72b0", "#c44e52")):
        coef, feat_names = plc.get_coefficients(pipes[_ptype])
        idx = np.argsort(coef)
        _ax_coef.barh(
            [feat_names[i] for i in idx],
            coef[idx],
            color=color,
            alpha=0.88,
        )
        _ax_coef.axvline(0, color="#333333", linewidth=1)
        _ax_coef.set_title("LR %s — hệ số (đặc trưng đã chuẩn hóa)" % _ptype.upper())
        _ax_coef.set_xlabel("Hệ số")

    plt.tight_layout()
    sns.despine(fig=fig_coef)
    fig_coef
    return


@app.cell
def _(mo):
    mo.md(f"""
    ## Cross-validation (ROC-AUC mỗi fold)

    - Stratified K-fold (**K=5**) trên **toàn bộ** dữ liệu đã mask; mỗi fold fit **pipeline độc lập** (không chia lệch train trong fold).
    - So sánh với chỉ báo ROC-AUC trên hold-out có thể dao động hơn.
    """)
    return


@app.cell
def _(X_masked, np, pd, plc, plt, sns, y_all):
    penalties = ("l2", "l1")
    fold_arrays = []

    cv_rows = []

    for _ptype in penalties:
        pipe = plc.make_pipeline(_ptype)
        folds = plc.cross_val_fold_scores(pipe, X_masked, y_all)
        fold_arrays.append(folds)

        cv_rows.append({"penalty": _ptype.upper(), "mean_auc": folds.mean(), "std_auc": folds.std()})


    cv_tbl = pd.DataFrame(cv_rows)
    fold_df = pd.DataFrame({"roc_auc": np.concatenate(fold_arrays), "penalty": np.repeat(["L2", "L1"], plc.CV_SPLITS)})

    fig_cv, ax_cv = plt.subplots(figsize=(6.4, 4.9))
    sns.boxplot(data=fold_df, x="penalty", y="roc_auc", ax=ax_cv, width=0.45)
    sns.stripplot(
        data=fold_df,
        x="penalty",
        y="roc_auc",
        ax=ax_cv,
        jitter=0.12,
        color="#333333",
        alpha=0.75,
    )
    sns.despine(fig=fig_cv)
    plt.tight_layout()
    ax_cv.set_title(f"Điểm ROC-AUC các fold ({plc.CV_SPLITS}-fold, trên đầy đủ mẫu đã tiền xử lý)")

    fig_cv
    cv_tbl
    return


@app.cell
def _(mo):
    mo.md("""
    ---

    ### Nhận xét và hạn chế

    - ROC-AUC trên test chỉ một lần là **ước lượng thô**; báo độ và CV giúp cảm nhận ổn định hơn.
    - Missing đã mã hoá như zero cần impute — pipeline đặt trong quyết định phân giới trên không gian chuẩn hoá (**không** suy luận định lượng causal trực tiếp từ hệ số).
    - Baseline chỉ **`C = 1.0`**; các bước mở rộng có thể: lưới `C`, `class_weight`, hoặc mô hình phi tuyến (RandomForest,...).
    """)
    return


if __name__ == "__main__":
    app.run()
