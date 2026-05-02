# PER-4459 - Đánh giá sơ bộ notebook Pima so với mẫu `ptdl-khaosatbds-faiss`

## Phạm vi đối chiếu
- Notebook được đánh giá: `Nhom01_SGU26_ML/Lab_03/pima_indians_diabetes_lab03.ipynb`
- Chuẩn tham chiếu: tài liệu đã parse trong MCP server `ptdl-khaosatbds-faiss` (corpus `parsing/PTDL_khaosatbds/parsing.md`).
- Lưu ý: Dataset khác nhau (Pima diabetes vs BĐS), nên đánh giá tập trung vào **quy trình**, **mức độ hoàn chỉnh**, và **cách trình bày**.

## Tiêu chí chuẩn rút ra từ `ptdl-khaosatbds-faiss`
Từ các chunk tham chiếu:
- `chunk_id=22`: cấu trúc báo cáo theo mạch 5 chương (tổng quan -> dữ liệu & phương pháp -> thực nghiệm -> kết luận/hạn chế/hướng phát triển).
- `chunk_id=87`: phần chuẩn bị dữ liệu nêu rõ **lý do chọn biến**, **chênh lệch thang đo**, **xử lý outlier**, **chuẩn hóa**.
- `chunk_id=97`: chiến lược chia tập được mô tả rõ mục tiêu tổng quát hóa, tỉ lệ chia, và tính công bằng khi so sánh.
- `chunk_id=100`: đánh giá mô hình có **bảng chỉ số định lượng** + **diễn giải ý nghĩa thực tiễn** (underfitting/rủi ro ứng dụng).
- `chunk_id=113`, `chunk_id=114`: có chương riêng cho **hạn chế nghiên cứu** và **hướng phát triển/kiến nghị**.

## Đánh giá sơ bộ notebook Pima hiện tại

### Điểm đã đạt tốt so với chuẩn
- Đã có mạch chính của Lab: nạp dữ liệu, EDA, làm sạch (zero-as-missing), chia train/val/test, so sánh nhiều chiến lược imputer+scaler+model.
- Có so sánh định lượng nhiều cấu hình (accuracy, f1, precision, recall, roc_auc).
- Có kết luận cấu hình đề xuất dựa trên kết quả thực nghiệm.

### Những gì còn thiếu so với chuẩn `PTDL_khaosatbds`
1. **Thiếu phần mô tả bài toán theo văn phong báo cáo hoàn chỉnh**
   - Mẫu có framing rõ mục tiêu nghiên cứu, câu hỏi nghiên cứu, phạm vi.
   - Notebook Pima mới dừng ở mức mô tả ngắn đầu notebook, chưa có phần "bối cảnh -> mục tiêu -> câu hỏi kiểm chứng".

2. **Thiếu phần giải thích sâu cho quyết định tiền xử lý**
   - Mẫu giải thích kỹ vì sao cần xử lý outlier, vì sao chuẩn hóa là bắt buộc theo cơ chế thuật toán.
   - Notebook Pima có làm các bước nhưng diễn giải còn ngắn, chưa chỉ rõ tác động của từng lựa chọn đến bias/variance hay tính ổn định mô hình.

3. **Thiếu mục "chiến lược đánh giá mô hình" thành một section độc lập**
   - Mẫu tách rõ chiến lược chia dữ liệu và nguyên tắc đánh giá công bằng.
   - Notebook Pima có code chia tập nhưng thiếu đoạn thuyết minh mục tiêu phương pháp luận (vì sao split này, vì sao metric này, rủi ro overfitting).

4. **Thiếu phần phân tích lỗi/diễn giải kết quả mô hình**
   - Mẫu không chỉ đưa số mà còn diễn giải ý nghĩa thực tế của từng mô hình.
   - Notebook Pima mới dừng ở bảng xếp hạng metric và chọn cấu hình tốt nhất, chưa có phân tích các trường hợp sai, chưa có thảo luận trade-off (ví dụ recall vs precision).

5. **Thiếu phần trực quan hóa chất lượng mô hình theo hướng báo cáo**
   - So với chuẩn trình bày mẫu, notebook chưa có các biểu đồ/khối báo cáo kiểu:
     - confusion matrix cho mô hình được chọn,
     - ROC curve cho top cấu hình,
     - calibration hoặc threshold analysis (nếu muốn đi sâu).

6. **Thiếu mục riêng về "hạn chế nghiên cứu"**
   - Mẫu có chương hạn chế rất rõ (dữ liệu, phương pháp, thiên lệch).
   - Notebook Pima chưa có mục liệt kê cụ thể các giới hạn như cỡ mẫu, đặc trưng thiếu, giả định zero-as-missing, và rủi ro external validity.

7. **Thiếu mục "hướng phát triển/kiến nghị"**
   - Mẫu có roadmap cải tiến ngắn hạn/trung hạn.
   - Notebook Pima chưa có kế hoạch mở rộng (feature engineering, CV, tuning, mô hình khác, kiểm định drift, đóng gói pipeline).

8. **Thiếu tính "báo cáo hóa" về cấu trúc trình bày**
   - Mẫu có mục lục/chương mục rõ, danh mục hình, narrative liền mạch.
   - Notebook Pima hiện thiên về notebook kỹ thuật, chưa tối ưu cho nộp báo cáo trình diễn.

## Mức độ hoàn thiện hiện tại (sơ bộ)
- **Quy trình kỹ thuật:** khá tốt cho phạm vi bài Lab.
- **Mức độ trình bày theo chuẩn mẫu PTDL_khaosatbds:** trung bình.
- **Khoảng cách chính:** không nằm ở "thiếu code", mà nằm ở "thiếu chiều sâu diễn giải + cấu trúc báo cáo học thuật".

## Gợi ý ưu tiên bổ sung (ngắn gọn)
1. Thêm 1 section "Chiến lược đánh giá" và giải thích metric/split.
2. Thêm 1 section "Phân tích kết quả mô hình" (confusion matrix + ROC + trade-off).
3. Thêm 2 section cuối: "Hạn chế" và "Hướng phát triển".
4. Chuẩn hóa narrative theo format chương mục gần với mẫu để dễ trình bày/nộp.
