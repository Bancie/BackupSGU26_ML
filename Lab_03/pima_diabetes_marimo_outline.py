"""High-level marimo outline for Pima Indians Diabetes (EDA / prep / model placeholder).

Run: marimo edit Lab_03/pima_diabetes_marimo_outline.py
This file intentionally contains structure only (markdown cells), no data logic.
"""

import marimo

__generated_with = "0.23.2"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md(
        """
        # BackupML — Pima Indians Diabetes

        **Marimo outline** (PER-3983): cấu trúc cấp cao cho EDA, tiền xử lý, thử nghiệm ML.
        Chưa triển khai logic; mỗi mục dưới đây tương ứng một nhóm cell khi làm việc thực tế.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## 1. Imports & Configuration

        - Import thư viện dùng chung (dữ liệu, thống kê, visualization, sklearn, …).
        - Cấu hình: seed, style plot, đường dẫn dữ liệu, tên cột / target.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## 2. Data Loading

        - Load dataset **Pima Indians Diabetes** (ví dụ `pima-indians-diabetes.csv`).
        - Preview: head, `shape`, kiểu cột.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## 3. Problem Definition

        - **Input**: các feature (biến số / biến phân loại nếu có).
        - **Output**: nhãn nhị phân (có/không diabetes).
        - **Loại bài toán**: phân loại nhị phân (binary classification).
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## 4. Exploratory Data Analysis (EDA)

        - Thống kê mô tả (`describe`, tần suất theo class).
        - Missing values, duplicates.
        - Phân bố (histogram / density theo feature; theo class nếu cần).
        - Tương quan (heatmap hoặc ma trận tương quan).
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## 5. Data Visualization

        - Biểu đồ đơn biến (theo từng feature hoặc target).
        - Biểu đồ đa biến (scatter pair, boxplot theo class, …).
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## 6. Data Cleaning

        - Xử lý missing values (chiến lược ghi chú tại đây khi triển khai).
        - Xóa trùng lặp.
        - Loại bỏ feature không cần thiết (nếu có, có lý do).
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## 7. Data Transformation

        - Encoding biến phân loại (nếu có thêm sau này).
        - One-hot khi cần tách category thành nhiều cột nhị phân.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## 8. Feature Scaling

        - Lựa chọn và áp dụng **Min-Max** hoặc **Standard** scaling (phù hợp mô hình sau).
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## 9. Data Splitting

        - Chia **train / test** (tỷ lệ và stratify theo target nếu dùng).
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## 10. Model Experimentation (placeholder)

        - Khung thử baseline (ví dụ logistic regression, tree-based, …) — *triển khai sau*.
        - Ghi chú metric: accuracy, precision, recall, ROC-AUC, …
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## 11. Results & Insights (placeholder)

        - Tóm tắt so sánh mô hình / tham số.
        - Insight nghiệp vụ ngắn (rủi ro overfit, giới hạn dữ liệu, bước tiếp theo).
        """
    )
    return


if __name__ == "__main__":
    app.run()
