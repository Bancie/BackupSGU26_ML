"""Datasets for ML_03 BaiTap06 (Rule-based learning)."""

from __future__ import annotations

PRISM_Q1_ROWS = [
    {
        "S.No": 1,
        "CGPA": ">9",
        "Interactiveness": "Yes",
        "Practical Knowledge": "Very good",
        "Communication Skills": "Good",
        "Job Offer": "Yes",
    },
    {
        "S.No": 2,
        "CGPA": ">8",
        "Interactiveness": "No",
        "Practical Knowledge": "Good",
        "Communication Skills": "Moderate",
        "Job Offer": "Yes",
    },
    {
        "S.No": 3,
        "CGPA": ">9",
        "Interactiveness": "No",
        "Practical Knowledge": "Average",
        "Communication Skills": "Poor",
        "Job Offer": "No",
    },
    {
        "S.No": 4,
        "CGPA": "<8",
        "Interactiveness": "No",
        "Practical Knowledge": "Average",
        "Communication Skills": "Good",
        "Job Offer": "No",
    },
    {
        "S.No": 5,
        "CGPA": ">8",
        "Interactiveness": "Yes",
        "Practical Knowledge": "Good",
        "Communication Skills": "Moderate",
        "Job Offer": "Yes",
    },
    {
        "S.No": 6,
        "CGPA": ">9",
        "Interactiveness": "Yes",
        "Practical Knowledge": "Good",
        "Communication Skills": "Moderate",
        "Job Offer": "Yes",
    },
    {
        "S.No": 7,
        "CGPA": "<8",
        "Interactiveness": "Yes",
        "Practical Knowledge": "Good",
        "Communication Skills": "Poor",
        "Job Offer": "No",
    },
    {
        "S.No": 8,
        "CGPA": ">9",
        "Interactiveness": "No",
        "Practical Knowledge": "Very good",
        "Communication Skills": "Good",
        "Job Offer": "Yes",
    },
    {
        "S.No": 9,
        "CGPA": ">8",
        "Interactiveness": "Yes",
        "Practical Knowledge": "Good",
        "Communication Skills": "Good",
        "Job Offer": "Yes",
    },
    {
        "S.No": 10,
        "CGPA": ">8",
        "Interactiveness": "Yes",
        "Practical Knowledge": "Average",
        "Communication Skills": "Good",
        "Job Offer": "Yes",
    },
]

PRISM_Q1_FEATURES = [
    "CGPA",
    "Interactiveness",
    "Practical Knowledge",
    "Communication Skills",
]
PRISM_Q1_TARGET = "Job Offer"


PRISM_Q2_ROWS = [
    {
        "S.No": 1,
        "Attendance": "Good",
        "Assignment": "Yes",
        "Project Submitted": "Yes",
        "Communication Skill": "Good",
        "Result": "Pass",
    },
    {
        "S.No": 2,
        "Attendance": "Average",
        "Assignment": "Yes",
        "Project Submitted": "No",
        "Communication Skill": "Poor",
        "Result": "Fail",
    },
    {
        "S.No": 3,
        "Attendance": "Good",
        "Assignment": "No",
        "Project Submitted": "Yes",
        "Communication Skill": "Good",
        "Result": "Pass",
    },
    {
        "S.No": 4,
        "Attendance": "Poor",
        "Assignment": "No",
        "Project Submitted": "No",
        "Communication Skill": "Poor",
        "Result": "Fail",
    },
    {
        "S.No": 5,
        "Attendance": "Good",
        "Assignment": "Yes",
        "Project Submitted": "Yes",
        "Communication Skill": "Good",
        "Result": "Pass",
    },
    {
        "S.No": 6,
        "Attendance": "Average",
        "Assignment": "No",
        "Project Submitted": "Yes",
        "Communication Skill": "Good",
        "Result": "Pass",
    },
    {
        "S.No": 7,
        "Attendance": "Good",
        "Assignment": "No",
        "Project Submitted": "No",
        "Communication Skill": "Fair",
        "Result": "Pass",
    },
    {
        "S.No": 8,
        "Attendance": "Poor",
        "Assignment": "Yes",
        "Project Submitted": "Yes",
        "Communication Skill": "Good",
        "Result": "Fail",
    },
    {
        "S.No": 9,
        "Attendance": "Average",
        "Assignment": "No",
        "Project Submitted": "No",
        "Communication Skill": "Poor",
        "Result": "Fail",
    },
    {
        "S.No": 10,
        "Attendance": "Good",
        "Assignment": "Yes",
        "Project Submitted": "Yes",
        "Communication Skill": "Fair",
        "Result": "Pass",
    },
]

PRISM_Q2_FEATURES = [
    "Attendance",
    "Assignment",
    "Project Submitted",
    "Communication Skill",
]
PRISM_Q2_TARGET = "Result"


FOIL_Q3_ROWS = [
    {
        "S.No": 1,
        "CGPA": ">9",
        "Interactiveness": "Yes",
        "Practical Knowledge": "Good",
        "Job Offer": "Yes",
    },
    {
        "S.No": 2,
        "CGPA": "<8",
        "Interactiveness": "Yes",
        "Practical Knowledge": "Good",
        "Job Offer": "Yes",
    },
    {
        "S.No": 3,
        "CGPA": ">9",
        "Interactiveness": "Yes",
        "Practical Knowledge": "Average",
        "Job Offer": "No",
    },
    {
        "S.No": 4,
        "CGPA": "<8",
        "Interactiveness": "No",
        "Practical Knowledge": "Good",
        "Job Offer": "No",
    },
    {
        "S.No": 5,
        "CGPA": ">8",
        "Interactiveness": "Yes",
        "Practical Knowledge": "Good",
        "Job Offer": "No",
    },
]

FOIL_Q3_FEATURES = ["CGPA", "Interactiveness", "Practical Knowledge"]
FOIL_Q3_TARGET = "Job Offer"
