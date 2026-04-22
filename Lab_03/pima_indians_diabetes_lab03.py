"""Marimo EDA notebook for Pima Indians Diabetes dataset."""

import marimo

__generated_with = "0.23.2"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md("""
    # Lab 03 - Exploratory Data Analysis (EDA): Pima Indians Diabetes

    Notebook này thực hiện EDA end-to-end cho dữ liệu:
    - `Lab_03/data/pima-indians-diabetes.csv`
    - `Lab_03/data/pima-indians-diabetes.names`

    Scope:
    - Data loading + schema validation
    - Data quality checks (NaN / duplicates / zero-as-missing)
    - Univariate / bivariate visualization
    - Correlation analysis
    - Insight tổng kết + hướng sang preprocessing/modeling
    - Luồng đối chiếu số liệu bằng MCP (pandas-mcp và mcp-server-ds)
    """)
    return


@app.cell
def _():
    from pathlib import Path

    import ast
    import json
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import seaborn as sns
    import time

    return Path, ast, json, np, pd, plt, sns, time


@app.cell
def _(Path, json, time):
    debug_log_path = Path("/Users/chibangnguyen/ayai/BackupSGU26_ML/.cursor/debug-802d3e.log")

    def agent_debug_log(run_id, hypothesis_id, location, message, data):
        # region agent log
        try:
            payload = {
                "sessionId": "802d3e",
                "runId": run_id,
                "hypothesisId": hypothesis_id,
                "location": location,
                "message": message,
                "data": data,
                "timestamp": int(time.time() * 1000),
            }
            with debug_log_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(payload, ensure_ascii=True) + "\n")
        except Exception:
            pass
        # endregion
    return (agent_debug_log,)


@app.cell
def _(Path, agent_debug_log, ast):
    source_path = Path(__file__).resolve()
    source_text = source_path.read_text(encoding="utf-8")
    tree = ast.parse(source_text)

    assigned_names = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            has_cell_decorator = any(
                isinstance(d, ast.Attribute) and d.attr == "cell" for d in node.decorator_list
            )
            if not has_cell_decorator:
                continue
            for sub in ast.walk(node):
                if isinstance(sub, ast.Assign):
                    for target in sub.targets:
                        if isinstance(target, ast.Name):
                            assigned_names.append(target.id)
                        elif isinstance(target, ast.Tuple):
                            for elt in target.elts:
                                if isinstance(elt, ast.Name):
                                    assigned_names.append(elt.id)

    duplicate_counts = {}
    for name in assigned_names:
        duplicate_counts[name] = duplicate_counts.get(name, 0) + 1
    duplicates = {k: v for k, v in duplicate_counts.items() if v > 1}

    # region agent log
    agent_debug_log(
        run_id="pre-fix",
        hypothesis_id="H1",
        location="pima_indians_diabetes_lab03.py:diagnostic_ast_scan",
        message="Duplicate assigned symbols across marimo cells",
        data={"duplicates": duplicates, "assigned_count": len(assigned_names)},
    )
    # endregion

    # region agent log
    agent_debug_log(
        run_id="pre-fix",
        hypothesis_id="H2",
        location="pima_indians_diabetes_lab03.py:diagnostic_ast_scan",
        message="Marimo source context",
        data={"source_path": str(source_path), "source_len": len(source_text)},
    )
    # endregion

    duplicates
    return


@app.cell
def _():
    column_names = [
        "pregnancies",
        "glucose",
        "blood_pressure",
        "skin_thickness",
        "insulin",
        "bmi",
        "diabetes_pedigree_function",
        "age",
        "outcome",
    ]
    feature_columns = [c for c in column_names if c != "outcome"]
    zero_as_missing_columns = [
        "glucose",
        "blood_pressure",
        "skin_thickness",
        "insulin",
        "bmi",
    ]
    valid_zero_columns = ["pregnancies"]
    random_state = 42
    return column_names, feature_columns, zero_as_missing_columns


@app.cell
def _(Path):
    repo_root = Path(__file__).resolve().parents[1]
    data_path = repo_root / "Lab_03" / "data" / "pima-indians-diabetes.csv"
    names_path = repo_root / "Lab_03" / "data" / "pima-indians-diabetes.names"
    return (data_path,)


@app.cell
def _(column_names, data_path, pd):
    df = pd.read_csv(data_path, header=None, names=column_names)
    return (df,)


@app.cell
def _(df, mo):
    mo.md(f"""
    ## 1) Data Loading & Problem Definition

    - Shape: **{df.shape[0]} rows x {df.shape[1]} columns**
    - Bài toán: **binary classification**
    - Target: `outcome` (0 = negative, 1 = positive diabetes)
    """)
    return


@app.cell
def _(df):
    df.head(10)
    return


@app.cell
def _(df):
    df.dtypes.to_frame(name="dtype")
    return


@app.cell
def _(df, mo):
    class_counts = df["outcome"].value_counts().sort_index().rename("count")
    class_rate = df["outcome"].value_counts(normalize=True).sort_index().rename("rate")
    class_distribution = (
        class_counts.to_frame()
        .join(class_rate.to_frame())
        .assign(rate_pct=lambda x: (100 * x["rate"]).round(2))
    )
    mo.md("## 2) Class Distribution")
    class_distribution
    return (class_distribution,)


@app.cell
def _(agent_debug_log, class_distribution, plt, sns):
    # region agent log
    agent_debug_log(
        run_id="pre-fix",
        hypothesis_id="H3",
        location="pima_indians_diabetes_lab03.py:class_distribution_plot_cell",
        message="Entered class distribution plot cell",
        data={"rows": int(class_distribution["count"].sum())},
    )
    # endregion
    fig_class_dist, ax_class_dist = plt.subplots(figsize=(6, 4))
    sns.barplot(
        x=class_distribution.index.astype(str),
        y=class_distribution["count"].values,
        ax=ax_class_dist,
        palette="viridis",
        hue=class_distribution.index.astype(str),
        legend=False,
    )
    ax_class_dist.set_title("Class distribution of outcome")
    ax_class_dist.set_xlabel("Outcome")
    ax_class_dist.set_ylabel("Count")
    plt.tight_layout()
    fig_class_dist
    return


@app.cell
def _(df, pd, zero_as_missing_columns):
    missing_report = pd.DataFrame(
        {
            "nan_count": df.isna().sum(),
            "nan_rate_pct": (100 * df.isna().mean()).round(2),
            "zero_count": (df == 0).sum(),
            "zero_rate_pct": (100 * (df == 0).mean()).round(2),
        }
    )
    duplicate_count = int(df.duplicated().sum())
    duplicates_preview = df[df.duplicated()].head(10)
    zero_focus_report = (
        missing_report.loc[zero_as_missing_columns + ["pregnancies", "outcome"]]
        .sort_values("zero_rate_pct", ascending=False)
        .copy()
    )
    return (
        duplicate_count,
        duplicates_preview,
        missing_report,
        zero_focus_report,
    )


@app.cell
def _(duplicate_count, mo):
    mo.md(f"""
    ## 3) Data Quality Checks

    - Duplicate rows: **{duplicate_count}**
    - `NaN` trong file gốc thường rất thấp; dữ liệu Pima chủ yếu mã hóa missing bằng giá trị `0` ở một số biến sinh lý.
    """)
    return


@app.cell
def _(missing_report):
    missing_report
    return


@app.cell
def _(duplicates_preview, mo):
    mo.md("### Duplicate rows preview (nếu có)")
    duplicates_preview
    return


@app.cell
def _(zero_focus_report):
    zero_focus_report
    return


@app.cell
def _(df, np, zero_as_missing_columns):
    df_masked = df.copy()
    df_masked[zero_as_missing_columns] = df_masked[zero_as_missing_columns].replace(0, np.nan)
    return (df_masked,)


@app.cell
def _(feature_columns, mo):
    bins_slider = mo.ui.slider(10, 80, value=30, label="Histogram bins")
    feature_selector = mo.ui.dropdown(
        options=feature_columns,
        value="glucose",
        label="Feature to inspect",
    )
    mask_zero_toggle = mo.ui.checkbox(
        value=True,
        label="Treat physiologically-invalid zeros as missing for selected plots",
    )
    mo.hstack([bins_slider, feature_selector, mask_zero_toggle], justify="start")
    return bins_slider, feature_selector, mask_zero_toggle


@app.cell
def _(df, df_masked, feature_selector, mask_zero_toggle):
    selected_feature = feature_selector.value
    plot_df = df_masked if mask_zero_toggle.value else df
    return plot_df, selected_feature


@app.cell
def _(agent_debug_log, bins_slider, plot_df, plt, selected_feature, sns):
    # region agent log
    agent_debug_log(
        run_id="pre-fix",
        hypothesis_id="H4",
        location="pima_indians_diabetes_lab03.py:histplot_cell",
        message="Entered histogram cell",
        data={
            "feature": selected_feature,
            "bins": int(bins_slider.value),
            "plot_rows": int(plot_df.shape[0]),
        },
    )
    # endregion
    fig_hist, ax_hist = plt.subplots(figsize=(7, 4))
    sns.histplot(
        data=plot_df,
        x=selected_feature,
        bins=bins_slider.value,
        kde=True,
        ax=ax_hist,
        color="#4C72B0",
    )
    ax_hist.set_title(f"Distribution of {selected_feature}")
    ax_hist.set_xlabel(selected_feature)
    plt.tight_layout()
    fig_hist
    return


@app.cell
def _(plot_df, plt, selected_feature, sns):
    fig_box, ax_box = plt.subplots(figsize=(6, 4))
    sns.boxplot(
        data=plot_df,
        x="outcome",
        y=selected_feature,
        ax=ax_box,
        palette="Set2",
        hue="outcome",
        legend=False,
    )
    ax_box.set_title(f"{selected_feature} by outcome")
    ax_box.set_xlabel("outcome")
    ax_box.set_ylabel(selected_feature)
    plt.tight_layout()
    fig_box
    return


@app.cell
def _(mo):
    mo.md("""
    ## 4) Descriptive Statistics
    """)
    return


@app.cell
def _(df, feature_columns):
    df[feature_columns].describe().T
    return


@app.cell
def _(df, feature_columns):
    grouped_stats = df.groupby("outcome")[feature_columns].agg(["mean", "median", "std"]).round(3)
    grouped_stats
    return


@app.cell
def _(df, df_masked, mask_zero_toggle):
    corr_source = df_masked if mask_zero_toggle.value else df
    corr_matrix = corr_source.corr(numeric_only=True)
    return corr_matrix, corr_source


@app.cell
def _(corr_matrix, plt, sns):
    fig_corr, ax_corr = plt.subplots(figsize=(9, 7))
    sns.heatmap(
        corr_matrix,
        cmap="coolwarm",
        center=0,
        annot=False,
        linewidths=0.4,
        cbar_kws={"shrink": 0.8},
        ax=ax_corr,
    )
    ax_corr.set_title("Correlation heatmap")
    plt.tight_layout()
    fig_corr
    return


@app.cell
def _(corr_matrix):
    corr_matrix["outcome"].sort_values(ascending=False).to_frame(name="corr_with_outcome")
    return


@app.cell
def _(corr_source, plt, sns):
    fig_scatter, axes_scatter = plt.subplots(1, 2, figsize=(13, 5))

    sns.scatterplot(
        data=corr_source,
        x="glucose",
        y="bmi",
        hue="outcome",
        alpha=0.7,
        ax=axes_scatter[0],
        palette="Set1",
    )
    axes_scatter[0].set_title("Glucose vs BMI by outcome")

    sns.scatterplot(
        data=corr_source,
        x="glucose",
        y="insulin",
        hue="outcome",
        alpha=0.7,
        ax=axes_scatter[1],
        palette="Set1",
        legend=False,
    )
    axes_scatter[1].set_title("Glucose vs Insulin by outcome")

    plt.tight_layout()
    fig_scatter
    return


@app.cell
def _(mo):
    pairplot_toggle = mo.ui.checkbox(
        value=False,
        label="Render pairplot (slow on some machines)",
    )
    mo.hstack([pairplot_toggle], justify="start")
    return (pairplot_toggle,)


@app.cell
def _(df, df_masked, mask_zero_toggle, pairplot_toggle, sns):
    if pairplot_toggle.value:
        pairplot_source = df_masked if mask_zero_toggle.value else df
        pairplot_df = pairplot_source[["glucose", "bmi", "age", "insulin", "outcome"]].dropna()
        grid = sns.pairplot(pairplot_df, hue="outcome", diag_kind="kde", corner=True)
        grid.fig.suptitle("Pairplot for selected features", y=1.02)
        grid.fig
    else:
        "Enable pairplot checkbox to render this chart."
    return


@app.cell
def _(class_distribution, duplicate_count, mo, zero_focus_report):
    top_zero_cols = zero_focus_report.index[:3].tolist()
    mo.md(
        f"""
        ## 5) EDA Insights Summary

        - Dataset có **{int(class_distribution['count'].sum())}** quan sát, target lệch lớp vừa phải
          (class 0 chiếm khoảng **{class_distribution.loc[0, 'rate_pct']:.2f}%**,
          class 1 chiếm **{class_distribution.loc[1, 'rate_pct']:.2f}%**).
        - Số dòng trùng lặp phát hiện: **{duplicate_count}**.
        - Các cột có tỷ lệ `0` cao nhất (gợi ý missing ngầm): **{', '.join(top_zero_cols)}**.
        - Khi chuyển `0 -> NaN` ở các cột sinh lý (`glucose`, `blood_pressure`, `skin_thickness`, `insulin`, `bmi`),
          ma trận tương quan và phân bố thường phản ánh dữ liệu thực tế hơn.
        - Bước tiếp theo: tách train/test có stratify, thử imputation pipeline và baseline model
          (Logistic Regression, RandomForest, XGBoost nếu cần).
        """
    )
    return


@app.cell
def _(data_path, mo):
    mo.md(f"""
    ## 6) MCP-assisted Validation Workflow

    Notebook này chạy EDA chính bằng pandas/seaborn trong marimo.
    Để đối chiếu nhanh kết quả bằng MCP, dùng các tool sau với **absolute path**:
    `{data_path.resolve()}`

    1. `project-0-BackupSGU26_ML-pandas-mcp.read_metadata_tool`
       - Kiểm tra delimiter/encoding/row-count/column stats.
    2. `project-0-BackupSGU26_ML-pandas-mcp.interpret_column_data` với `column_names=[\"outcome\"]`
       - Kiểm tra phân bố lớp 0/1.
    3. `project-0-BackupSGU26_ML-pandas-mcp.run_pandas_code_tool`
       - Đối chiếu `describe`, `value_counts`, correlation/missing patterns.
    4. `project-0-BackupSGU26_ML-mcp-server-ds.load_csv` + `run_script`
       - Chạy script kiểm tra tuyến tính nhiều bước (không tạo chart, không overwrite dataframe cũ).
    """)
    return


if __name__ == "__main__":
    app.run()
