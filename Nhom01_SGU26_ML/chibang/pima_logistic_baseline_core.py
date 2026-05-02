"""Logic dùng chung: baseline LR (L2/L1) — Pima Indians Diabetes.

Dùng bởi ``pima_logistic_baseline.py`` (CLI) và ``pima_logistic_baseline_nb.py`` (marimo).
"""

from __future__ import annotations

import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

COLUMN_NAMES = [
    "pregnancies",
    "glucose",
    "blood_pressure",
    "skin_thickness",
    "insulin",
    "bmi",
    "diabetes_pedigree_function",
    "age",
    "outcome",
]
FEATURE_COLUMNS = [c for c in COLUMN_NAMES if c != "outcome"]
ZERO_AS_MISSING_COLUMNS = [
    "glucose",
    "blood_pressure",
    "skin_thickness",
    "insulin",
    "bmi",
]
RANDOM_STATE = 42
TEST_SIZE = 0.2
CV_SPLITS = 5


def apply_sklearn_logistic_warnings_filter() -> None:
    warnings.filterwarnings("ignore", module="sklearn.linear_model._logistic")


def resolve_data_path() -> Path:
    return Path(__file__).resolve().parent / "data" / "pima-indians-diabetes.csv"


def load_xy(data_path: Path) -> tuple[pd.DataFrame, pd.Series]:
    df = pd.read_csv(data_path, header=None, names=COLUMN_NAMES)
    X = df[FEATURE_COLUMNS].copy()
    y = df["outcome"].astype(int)
    return X, y


def mask_invalid_zeros(X: pd.DataFrame) -> pd.DataFrame:
    out = X.copy()
    out[ZERO_AS_MISSING_COLUMNS] = out[ZERO_AS_MISSING_COLUMNS].replace(0, np.nan)
    return out


def make_pipeline(penalty: str) -> Pipeline:
    if penalty == "l2":
        lr = LogisticRegression(
            penalty="l2",
            solver="lbfgs",
            C=1.0,
            max_iter=5000,
            random_state=RANDOM_STATE,
        )
    elif penalty == "l1":
        lr = LogisticRegression(
            penalty="l1",
            solver="saga",
            C=1.0,
            max_iter=10000,
            random_state=RANDOM_STATE,
        )
    else:
        raise ValueError("penalty phải là 'l1' hoặc 'l2'")

    return Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            ("clf", lr),
        ]
    )


def compute_test_metrics(
    pipe: Pipeline,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> dict:
    """Trả metrics + dự đoán để vẽ ROC / confusion."""
    y_prob = pipe.predict_proba(X_test)[:, 1]
    y_pred = pipe.predict(X_test)
    report = classification_report(y_test, y_pred, digits=4, output_dict=True)
    return {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "roc_auc": float(roc_auc_score(y_test, y_prob)),
        "y_prob": y_prob,
        "y_pred": y_pred,
        "report_dict": report,
    }


def build_metrics_comparison_df(
    results: dict[str, dict],
    penalties: tuple[str, ...] = ("l2", "l1"),
) -> pd.DataFrame:
    rows = []
    for p in penalties:
        rows.append({"penalty": p.upper(), "accuracy": results[p]["accuracy"], "roc_auc": results[p]["roc_auc"]})
    return pd.DataFrame(rows)


def get_coefficients(pipe: Pipeline) -> tuple[np.ndarray, list[str]]:
    clf: LogisticRegression = pipe.named_steps["clf"]
    coef = clf.coef_.ravel()
    return coef, FEATURE_COLUMNS


def cross_val_fold_scores(pipe: Pipeline, X: pd.DataFrame, y: pd.Series, n_splits: int = CV_SPLITS) -> np.ndarray:
    cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=RANDOM_STATE)
    out = cross_validate(
        pipe,
        X,
        y,
        cv=cv,
        scoring="roc_auc",
        n_jobs=-1,
        error_score="raise",
    )
    return np.asarray(out["test_score"], dtype=float)


def run_cli() -> None:
    """In kết quả ra stdout (behavior cũ)."""
    apply_sklearn_logistic_warnings_filter()
    data_path = resolve_data_path()
    if not data_path.exists():
        raise FileNotFoundError(f"Không tìm thấy file: {data_path}")

    X_raw, y = load_xy(data_path)
    X = mask_invalid_zeros(X_raw)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        stratify=y,
        random_state=RANDOM_STATE,
    )

    for penalty in ("l2", "l1"):
        pipe = make_pipeline(penalty)
        pipe.fit(X_train, y_train)
        m = compute_test_metrics(pipe, X_test, y_test)
        print(f"\n=== LogisticRegression {penalty.upper()} (test hold-out) ===")
        print(f"Accuracy : {m['accuracy']:.4f}")
        print(f"ROC-AUC   : {m['roc_auc']:.4f}")
        print("Classification report:\n")
        print(classification_report(y_test, m["y_pred"], digits=4))

    print("\n--- Cross-validation ROC-AUC (full train masking, không dùng test) ---")
    for penalty in ("l2", "l1"):
        pipe = make_pipeline(penalty)
        folds = cross_val_fold_scores(pipe, X, y)
        print(f"L{penalty[-1].upper()}  — ROC-AUC 5-fold CV: mean={folds.mean():.4f}, std={folds.std():.4f}")
