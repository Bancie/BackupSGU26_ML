"""Bảng dữ liệu trích theo đề bài."""

import pandas as pd

# --- Phần 1: Mùa (mẫu 1–12 huấn luyện; X, Y dự báo)

SEASON_COLUMNS = ["Mẫu", "Thời tiết", "Lá cây", "Nhiệt độ", "Mùa"]


def seasonal_training() -> pd.DataFrame:
    rows = [
        ("1", "Nắng", "Vàng", "Trung bình", "Thu"),
        ("2", "Tuyết", "Xanh", "Thấp", "Đông"),
        ("3", "Tuyết", "Vàng", "Thấp", "Đông"),
        ("4", "Mưa", "Vàng", "Trung bình", "Thu"),
        ("5", "Mưa", "Rụng", "Thấp", "Đông"),
        ("6", "Tuyết", "Rụng", "Thấp", "Đông"),
        ("7", "Nắng", "Rụng", "Thấp", "Đông"),
        ("8", "Nắng", "Xanh", "Trung bình", "Xuân"),
        ("9", "Nắng", "Xanh", "Cao", "Hè"),
        ("10", "Mưa", "Rụng", "Trung bình", "Thu"),
        ("11", "Mưa", "Xanh", "Cao", "Hè"),
        ("12", "Mưa", "Xanh", "Trung bình", "Xuân"),
    ]
    return pd.DataFrame(rows, columns=SEASON_COLUMNS)


def seasonal_test_XY() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("X", "Mưa", "Vàng", "Thấp"),
            ("Y", "Tuyết", "Rụng", "Trung bình"),
        ],
        columns=["Mẫu"] + SEASON_COLUMNS[1:-1],
    )


# --- Phần 2 (đề lá cây, trang 3 trên—mẫu 1–10 train; 11, 12 kiểm tra)

LEAF_COLUMNS = ["Mẫu", "Hình dạng", "Dạng", "Màu", "Kích thước", "Độc"]


def leaf_dataset() -> pd.DataFrame:
    rows = [
        ("1", "Tròn", "Đơn", "Đỏ", "Nhỏ", "Không"),
        ("2", "Tròn", "Kép", "Đỏ", "Nhỏ", "Có"),
        ("3", "Tròn", "Đơn", "Xanh", "To", "Không"),
        ("4", "Dài", "Đơn", "Xanh", "Nhỏ", "Không"),
        ("5", "Dài", "Kép", "Vàng", "Nhỏ", "Có"),
        ("6", "Dài", "Đơn", "Xanh", "Vừa", "Có"),
        ("7", "Tròn", "Kép", "Vàng", "To", "Không"),
        ("8", "Tròn", "Kép", "Vàng", "Vừa", "Có"),
        ("9", "Tròn", "Đơn", "Đỏ", "Vừa", "Có"),
        ("10", "Dài", "Đơn", "Đỏ", "Vừa", "Có"),
        ("11", "Dài", "Kép", "Đỏ", "Vừa", None),
        ("12", "Tròn", "Đơn", "Xanh", "Nhỏ", None),
    ]
    return pd.DataFrame(rows, columns=LEAF_COLUMNS)


# --- Phần 3 «Bài 3» — tín dụng (train 1–10; A, B kiểm tra)

LOAN_COLUMNS = ["Mẫu", "Phái", "Công việc", "Học vấn", "Độ tuổi", "Quyết định"]


def loan_dataset() -> pd.DataFrame:
    rows = [
        ("1", "Nam", "LĐ Chân tay", "Cao đẳng", "Trung niên", "Không"),
        ("2", "Nữ", "LĐ Trí óc", "Đại học", "Trung niên", "Có"),
        ("3", "Nữ", "LĐ Chân tay", "Phổ thông", "Già", "Có"),
        ("4", "Nam", "LĐ Trí óc", "Cao đẳng", "Trung niên", "Có"),
        ("5", "Nam", "LĐ Chân tay", "Phổ thông", "Thanh niên", "Không"),
        ("6", "Nam", "LĐ Trí óc", "Đại học", "Già", "Có"),
        ("7", "Nam", "LĐ Chân tay", "Cao đẳng", "Già", "Có"),
        ("8", "Nữ", "LĐ Chân tay", "Phổ thông", "Trung niên", "Không"),
        ("9", "Nam", "LĐ Trí óc", "Đại học", "Thanh niên", "Không"),
        ("10", "Nữ", "LĐ Chân tay", "Cao đẳng", "Già", "Có"),
        ("A", "Nữ", "LĐ Trí óc", "Cao đẳng", "Già", None),
        ("B", "Nam", "LĐ Chân tay", "Phổ thông", "Trung niên", None),
    ]
    return pd.DataFrame(rows, columns=LOAN_COLUMNS)


SEASON_FEATURES = ["Thời tiết", "Lá cây", "Nhiệt độ"]
LEAF_FEATURES = LEAF_COLUMNS[1:-1]
LOAN_FEATURES = LOAN_COLUMNS[1:-1]
