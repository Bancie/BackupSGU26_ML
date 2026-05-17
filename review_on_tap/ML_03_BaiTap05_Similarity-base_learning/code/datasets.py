"""PER-4784 — dữ liệu bài Similarity-based learning (đúng bảng đề)."""

from __future__ import annotations

import numpy as np

# --- Câu 1: GPA, Assignment, Project -> Pass/Fail ---
Q1_X = np.array(
    [
        [9.0, 88, 9],
        [8.2, 75, 8],
        [6.0, 45, 5],
        [5.5, 40, 4],
        [7.8, 70, 7],
        [6.2, 50, 5],
    ],
    dtype=float,
)
Q1_Y = np.array(["Pass", "Pass", "Fail", "Fail", "Pass", "Fail"], dtype=object)
Q1_TEST = np.array([6.5, 55, 5], dtype=float)

# --- Câu 2: Height, Weight -> A/B; k mặc định = 3 ---
Q2_K = 3
Q2_X = np.array(
    [
        [170, 60],
        [175, 65],
        [160, 90],
        [158, 85],
    ],
    dtype=float,
)
Q2_Y = np.array(["A", "A", "B", "B"], dtype=object)
Q2_TEST = np.array([172, 80], dtype=float)

# --- Câu 3: weighted k-NN 2D (gồm thêm điểm 5,5,A) ---
Q3_X = np.array(
    [
        [2, 3],
        [3, 4],
        [7, 8],
        [8, 9],
        [5, 5],
    ],
    dtype=float,
)
Q3_Y = np.array(["A", "A", "B", "B", "A"], dtype=object)
Q3_TEST = np.array([6, 6], dtype=float)
Q3_K = 3

# --- Câu 4: nearest centroid ---
Q4_X = np.array(
    [
        [2, 1],
        [3, 2],
        [4, 1],
        [7, 6],
        [8, 7],
        [9, 5],
    ],
    dtype=float,
)
Q4_Y = np.array(["A", "A", "A", "B", "B", "B"], dtype=object)
Q4_TEST = np.array([6, 5], dtype=float)

# --- Câu 5: LWR ---
Q5_X1 = np.array([1.0, 2.0, 3.0, 4.0])
Q5_Y = np.array([3.0, 5.0, 7.0, 9.0])
Q5_BETA0, Q5_BETA1 = 1.0, 2.0
Q5_QUERY_X = 2.5
Q5_TAU = 1.0

# --- Câu 6: COVID symptoms (1=Yes, 0=No), 9 đặc trưng ---
COVID_FEATURE_NAMES = [
    "Fever",
    "Dry Cough",
    "Tiredness",
    "Sore Throat",
    "Diarrhea",
    "Headache",
    "Loss of Taste/Smell",
    "Shortness of Breath",
    "Chest Pain",
]
COVID_X = np.array(
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1],  # 1 Positive
        [1, 0, 1, 0, 0, 1, 0, 0, 0],  # 2 Negative
        [0, 0, 0, 0, 0, 0, 0, 0, 0],  # 3 Negative
        [1, 1, 1, 0, 0, 0, 0, 0, 1],  # 4 Negative
        [1, 1, 1, 1, 0, 0, 1, 1, 1],  # 5 Positive
        [1, 1, 1, 0, 0, 1, 0, 0, 0],  # 6 Positive
        [1, 1, 1, 1, 0, 0, 1, 1, 0],  # 7 Positive
        [1, 1, 1, 1, 0, 0, 0, 0, 0],  # 8 Positive
        [1, 1, 1, 1, 0, 0, 0, 0, 0],  # 9 Positive (same pattern as 8)
        [0, 0, 0, 0, 0, 0, 0, 0, 0],  # 10 Negative
    ],
    dtype=int,
)
COVID_Y = np.array(
    [
        "Positive",
        "Negative",
        "Negative",
        "Negative",
        "Positive",
        "Positive",
        "Positive",
        "Positive",
        "Positive",
        "Negative",
    ],
    dtype=object,
)
COVID_TEST = np.array([1, 1, 1, 1, 0, 0, 0, 0, 0], dtype=int)
COVID_KS = [3, 1, 5, 7]
COVID_WEIGHTED_K = 3
