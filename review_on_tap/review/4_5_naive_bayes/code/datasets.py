"""Dữ liệu bài tập PER-4810 — Naive Bayes (ngân hàng + tennis + email)."""

from __future__ import annotations

from typing import Any

import numpy as np

BANK_TARGET = "Kết quả"
BANK_FEATURE_CAT = ["Gia đình"]
BANK_FEATURE_NUM = ["Tuổi", "Thu nhập", "Số tiền vay"]

# --- Câu 4.5.1: tín dụng Lạc Việt (bảng đề) ---
BANK_ROWS: list[dict[str, Any]] = [
    {"Tuổi": 25, "Gia đình": "Có", "Thu nhập": 20, "Số tiền vay": 120, "Kết quả": "Yes"},
    {"Tuổi": 22, "Gia đình": "Không", "Thu nhập": 15, "Số tiền vay": 200, "Kết quả": "No"},
    {"Tuổi": 24, "Gia đình": "Có", "Thu nhập": 18, "Số tiền vay": 180, "Kết quả": "Yes"},
    {"Tuổi": 30, "Gia đình": "Không", "Thu nhập": 17, "Số tiền vay": 130, "Kết quả": "Yes"},
    {"Tuổi": 31, "Gia đình": "Có", "Thu nhập": 22, "Số tiền vay": 250, "Kết quả": "No"},
    {"Tuổi": 35, "Gia đình": "Có", "Thu nhập": 22, "Số tiền vay": 150, "Kết quả": "Yes"},
    {"Tuổi": 22, "Gia đình": "Không", "Thu nhập": 23, "Số tiền vay": 210, "Kết quả": "No"},
    {"Tuổi": 28, "Gia đình": "Có", "Thu nhập": 19, "Số tiền vay": 280, "Kết quả": "No"},
]

BANK_TEST = {"Tuổi": 23, "Gia đình": "Có", "Thu nhập": 32, "Số tiền vay": 250}

# --- Câu 4.5.2: tennis rời rạc ---
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

# --- Câu 4.5.3: tennis số ---
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

Q2_TEST_B = {"Outlook": "sunny", "Temperature": 66, "Humidity": 90, "Windy": True}

# --- Câu 4.5.4: email ---
WORD_NAMES = [f"w{i}" for i in range(1, 8)]

EMAIL_TRAIN = np.array(
    [
        [1, 2, 1, 0, 1, 0, 0],
        [0, 2, 0, 0, 1, 1, 1],
        [1, 0, 1, 1, 0, 2, 0],
    ],
    dtype=np.int64,
)
EMAIL_LABELS = ["N", "N", "S"]
EMAIL_TEST_E4 = np.array([1, 0, 0, 0, 0, 0, 1], dtype=np.int64)


def q1_split() -> list[str]:
    return ["Outlook", "Temp", "Humidity", "Windy"]
