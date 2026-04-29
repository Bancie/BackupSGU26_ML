# Yêu cầu lab 03

## Mô tả yêu cầu

- Task 1 - Exploratory Data Analysis (EDA) pima_indians_diabetes dataset: Mục tiêu là Exploratory Data Analysis (EDA) dữ liệu diabetes trong đó data được cấp gồm file `Lab_03/data/pima-indians-diabetes.csv` và `Lab_03/data/pima-indians-diabetes.names`, yêu cầu thực hiện EDA cho tập dữ liệu trên và đưa ra insight + hướng tiếp cận xử lý các missing value tồn tại trong tập dữ liệu.
- Task 2 - Gõ các lại các ví dụ trong paper thầy giao gồm: `Lab_03/paper1.pdf`, `Lab_03/paper2.pdf`, `Lab_03/paper3.pdf`: Mục tiêu là gõ lại các ví dụ có trong các file paper thầy giao vào notebook và chạy thử để xem kết quả.

## Nhật ký thực hiện

> **Trạng thái:** **Lab 03: Đã hoàn thành** (29/04/2026)

### Đã thực hiện

- **Task 1 — EDA (Pima Indians Diabetes)**  
  - Notebook Marimo `[pima_indians_diabetes_lab03.py](./pima_indians_diabetes_lab03.py)`: tải dữ liệu `pima-indians-diabetes.csv` / `.names`, kiểm tra chất lượng (duplicate, NaN, zero coi như missing ở một số cột sinh lý), mô tả thống kê theo nhãn `outcome`, correlation heatmap, scatter/pairplot, tóm tắt insight và hướng tiền xử lý.
- **Mô hình baseline (ngoài wording Task 1, phục vụ báo cáo / lab)**  
  - Module chia sẻ `[pima_logistic_baseline_core.py](./pima_logistic_baseline_core.py)`: mask `0→NaN`, pipeline `SimpleImputer (median) → StandardScaler → LogisticRegression` (L2 `lbfgs` / L1 `saga`, `C=1`), chia train/test stratified `random_state=42`, ROC-AUC test, cross-validation Stratified K-fold ROC-AUC.  
  - Script CLI `[pima_logistic_baseline.py](./pima_logistic_baseline.py)` gọi `run_cli()`.  
  - Notebook Marimo `[pima_logistic_baseline_nb.py](./pima_logistic_baseline_nb.py)`: markdown giải thích, bảng metrics hold-out + `classification_report`, biểu đồ ROC, confusion matrix (chuẩn hóa theo hàng), hệ số theo đặc trưng đã scale, box/strip ROC-AUC từng fold; phụ thuộc `pandas` / `matplotlib` / `seaborn` trong `[requirements.txt](../requirements.txt)`.
- **Công cụ & repo**  
  - Cập nhật `.gitignore`: loại trừ `.cursor/` (gồm `mcp.json`), thư mục clone MCP `tools/mcp/` (không đẩy lên Git).  
  - Clone cục bộ hai MCP vào `tools/mcp/` (pandas-mcp-server, mcp-server-data-exploration), ghim Python **3.12** trong từng project (tránh lỗi build trên 3.14), chạy `uv sync` để có thể dùng theo `.cursor/mcp.json`.
- **Task 2 — Minh họa nội dung paper (paper1, paper2, paper3)**  
  - Notebook Jupyter `[lab03_task2_papers_examples.ipynb](./lab03_task2_papers_examples.ipynb)`: gõ và chạy các ví dụ có thể mã hóa từ ba PDF — (1) WHO 1999: quy đổi và phân vùng FPG / IFG; (2) Smith et al. 1988: bảng ca mẫu (theo Table 2), một bước cập nhật trọng số kiểu ADAP rút gọn, ROC minh họa bằng `sklearn`; (3) NDDG 1979: hàm kiểm tra nhánh OGTT (FPG dưới 140 mg/dl nhưng 2h và mốc giữa kỳ ≥ 200 mg/dl). Đã chạy thử toàn bộ cell trên môi trường Python 3.

### Chưa thực hiện / cần làm tiếp

- Không còn hạng mục bắt buộc theo `yeucau.md` cho Lab 03.