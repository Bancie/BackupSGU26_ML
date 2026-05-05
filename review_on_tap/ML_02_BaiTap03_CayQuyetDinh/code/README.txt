Chạy đối chiếu đáp án:

  cd review_on_tap/ML_02_BaiTap03_CayQuyetDinh/code
  source ../../../.venv/bin/activate   # nếu cần
  python verify_exercises.py

Regenerate các hình cây (PDF), ghi vào ../latex/figures/, nên chạy trước pdflatex:

  python export_tree_figures.py          # đủ 3 hình
  python export_tree_figures.py --season --leaf   # chỉ một phần
