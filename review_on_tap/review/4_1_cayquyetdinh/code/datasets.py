"""Bảng dữ liệu theo đề 4.1.1–4.1.4."""

import pandas as pd

# --- 4.1.1 — Mùa (12 mẫu huấn luyện; X, Y dự báo)

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


# --- 4.1.2 — Lá (1–10 train; 11, 12 kiểm tra)

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


# --- 4.1.3 — Quyết định (1–10 train; A, B kiểm tra)

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


# --- 4.1.4 — Hồ sơ vay (15 mẫu; C4.5 / Information Gain trên thuộc tính rời rạc)

LOAN_C45_COLUMNS = [
    "Mẫu",
    "Age",
    "Has_job",
    "Own_house",
    "Credit_rating",
    "Class",
]


def loan_c45_dataset() -> pd.DataFrame:
    """Đề bài: Has_job, Own_house là boolean; Class là Yes/No."""
    rows = [
        ("1", "young", False, False, "fair", "No"),
        ("2", "young", False, False, "good", "No"),
        ("3", "young", True, False, "good", "Yes"),
        ("4", "young", True, True, "fair", "Yes"),
        ("5", "young", False, False, "fair", "No"),
        ("6", "middle", False, False, "fair", "No"),
        ("7", "middle", False, False, "good", "No"),
        ("8", "middle", True, True, "good", "Yes"),
        ("9", "middle", False, True, "excellent", "Yes"),
        ("10", "middle", False, True, "excellent", "Yes"),
        ("11", "old", False, True, "excellent", "Yes"),
        ("12", "old", False, True, "good", "Yes"),
        ("13", "old", True, False, "good", "Yes"),
        ("14", "old", True, False, "excellent", "Yes"),
        ("15", "old", False, False, "fair", "No"),
    ]
    return pd.DataFrame(rows, columns=LOAN_C45_COLUMNS)


SEASON_FEATURES = ["Thời tiết", "Lá cây", "Nhiệt độ"]
LEAF_FEATURES = LEAF_COLUMNS[1:-1]
LOAN_FEATURES = LOAN_COLUMNS[1:-1]
LOAN_C45_FEATURES = ["Age", "Has_job", "Own_house", "Credit_rating"]
