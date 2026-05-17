PER-4785 — ML_03 BaiTap06 Rule-based learning

Đối chiếu đáp án:
  python verify_exercises.py

Script in ra:
  - Rule set PRISM cho Câu 1 (Yes/No) và Câu 2 (Pass/Fail).
  - Coverage/Accuracy của từng luật trong rule set cuối.
  - Danh sách conflict theo instance (nếu có) và thứ tự theo accuracy.
  - Bảng FOIL-Gain vòng đầu + quá trình sinh luật FOIL cho Câu 3.

Biên dịch lời giải (từ thư mục ../latex):
  pdflatex main.tex

Phụ thuộc:
  Chỉ dùng Python chuẩn (không cần thư viện ngoài).
PER-4785 — ML_03 Bài 06 Rule-based learning (PRISM + FOIL)

Chạy đối chiếu số:
  python verify_exercises.py

Biên dịch lời giải (từ ../latex):
  pdflatex main.tex

Dữ liệu PRISM: 7 dòng ID 4–10 như trang 2 đề (nếu PDF có thêm mẫu 1–3, bổ sung datasets.py).

Phụ thuộc: pandas (đã có trong requirements.txt gốc repo).
