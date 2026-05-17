"""Dữ liệu bài tập PER-4783 — phân lớp Bayes (Play Tennis + email)."""

from __future__ import annotations

from typing import Any

import numpy as np

# --- Câu 1: categorical tennis (như đề, chữ hoa đầu cụm) ---
Q1_COLUMNS = ["Outlook", "Temp", "Humidity", "Windy", "Play"]

Q1_ROWS: list[dict[str, Any]] = [
    {"Outlook": "Sunny", "Temp": "Hot", "Humidity": "High", "Windy": False, "Play": "No"},
    {"Outlook": "Sunny", "Temp": "Hot", "Humidity": "High", "Windy": True, "Play": "No"},
    {"Outlook": "Overcast", "Temp": "Hot", "Humidity": "High", "Windy": False, "Play": "Yes"},
    {"Outlook": "Rainy", "Temp": "Mild", "Humidity": "High", "Windy": False, "Play": "Yes"},
    {"Outlook": "Rainy", "Temp": "Cool", "Humidity": "Normal", "Windy": False, "Play": "Yes"},
    {"Outlook": "Rainy", "Temp": "Cool", "Humidity": "Normal", "Windy": True, "Play": "No"},
    {"Outlook": "Overcast", "Temp": "Cool", "Humidity": "Normal", "Windy": True, "Play": "Yes"},
    {"Outlook": "Sunny", "Temp": "Mild", "Humidity": "High", "Windy": False, "Play": "No"},
    {"Outlook": "Sunny", "Temp": "Cool", "Humidity": "Normal", "Windy": False, "Play": "Yes"},
    {"Outlook": "Rainy", "Temp": "Mild", "Humidity": "Normal", "Windy": False, "Play": "Yes"},
    {"Outlook": "Sunny", "Temp": "Mild", "Humidity": "Normal", "Windy": True, "Play": "Yes"},
    {"Outlook": "Overcast", "Temp": "Mild", "Humidity": "High", "Windy": True, "Play": "Yes"},
    {"Outlook": "Overcast", "Temp": "Hot", "Humidity": "Normal", "Windy": False, "Play": "Yes"},
    {"Outlook": "Rainy", "Temp": "Mild", "Humidity": "High", "Windy": True, "Play": "No"},
]

# --- Câu 2: numeric tennis (đúng bảng đề, chữ thường outlook / rain) ---
Q2_COLUMNS = ["Outlook", "Temperature", "Humidity", "Windy", "Play"]

Q2_ROWS: list[dict[str, Any]] = [
    {"Outlook": "sunny", "Temperature": 85, "Humidity": 85, "Windy": False, "Play": "no"},
    {"Outlook": "sunny", "Temperature": 80, "Humidity": 90, "Windy": True, "Play": "no"},
    {"Outlook": "overcast", "Temperature": 83, "Humidity": 78, "Windy": False, "Play": "yes"},
    {"Outlook": "rain", "Temperature": 70, "Humidity": 96, "Windy": False, "Play": "yes"},
    {"Outlook": "rain", "Temperature": 68, "Humidity": 80, "Windy": False, "Play": "yes"},
    {"Outlook": "rain", "Temperature": 65, "Humidity": 70, "Windy": True, "Play": "no"},
    {"Outlook": "overcast", "Temperature": 64, "Humidity": 65, "Windy": True, "Play": "yes"},
    {"Outlook": "sunny", "Temperature": 72, "Humidity": 95, "Windy": False, "Play": "no"},
    {"Outlook": "sunny", "Temperature": 69, "Humidity": 70, "Windy": False, "Play": "yes"},
    {"Outlook": "rain", "Temperature": 75, "Humidity": 80, "Windy": False, "Play": "yes"},
    {"Outlook": "sunny", "Temperature": 75, "Humidity": 70, "Windy": True, "Play": "yes"},
    {"Outlook": "overcast", "Temperature": 72, "Humidity": 90, "Windy": True, "Play": "yes"},
    {"Outlook": "overcast", "Temperature": 81, "Humidity": 75, "Windy": False, "Play": "yes"},
    {"Outlook": "rain", "Temperature": 71, "Humidity": 80, "Windy": True, "Play": "no"},
]

# Mẫu (b) Câu 2 — snippet phía trên tài liệu; đối chiếu PDF nếu khác
Q2_TEST_B = {"Outlook": "sunny", "Temperature": 66, "Humidity": 90, "Windy": True}

# --- Câu 3: email, đếm từ w1..w7 ---
WORD_NAMES = [f"w{i}" for i in range(1, 8)]

EMAIL_TRAIN = np.array(
    [
        [1, 2, 1, 0, 1, 0, 0],  # E1 N
        [0, 2, 0, 0, 1, 1, 1],  # E2 N
        [1, 0, 1, 1, 0, 2, 0],  # E3 S
    ],
    dtype=np.int64,
)
EMAIL_LABELS = ["N", "N", "S"]
EMAIL_TEST_E4 = np.array([1, 0, 0, 0, 0, 0, 1], dtype=np.int64)


def q1_split() -> list[str]:
    return ["Outlook", "Temp", "Humidity", "Windy"]
