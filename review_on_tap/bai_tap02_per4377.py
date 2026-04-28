"""
PER-4377 — Bài tập 02 (EDA & tiền xử lý). Chạy: python bai_tap02_per4377.py

Giải tay: README_baitap02_per4377.md
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

HERE = Path(__file__).resolve().parent

# Theo đề — ? => NaN | Lương có -2000 tại ID 5
RAW_ROWS = [
    [1, 25, 8000.0, 7.5, "Nam", "Yes"],
    [2, 30, np.nan, 8.0, "Nữ", "No"],
    [3, 22, 5000.0, 6.5, "Nam", "Yes"],
    [4, 40, 15000.0, 9.0, "Nữ", "Yes"],
    [5, 35, -2000.0, 7.0, "Nam", "No"],
    [6, np.nan, 7000.0, 6.0, "Nữ", "Yes"],
    [7, 29, 8500.0, 8.5, "Nam", "Yes"],
    [8, 50, 30000.0, 9.5, "Nữ", "Yes"],
    [9, 27, 8200.0, np.nan, "Nam", "No"],
    [10, 31, 7800.0, 7.8, "Nữ", "Yes"],
]
COLS = ["ID", "Tuổi", "Lương", "Điểm", "Giới tính", "Mua hàng"]

NUMERIC = ["Tuổi", "Lương", "Điểm"]
CAT = ["Giới tính", "Mua hàng"]


def df_raw() -> pd.DataFrame:
    return pd.DataFrame(RAW_ROWS, columns=COLS)


def hdr(s: str) -> None:
    print("\n" + "=" * 72)
    print(s)
    print("=" * 72)


def q1_basic(df: pd.DataFrame) -> None:
    hdr("Câu 1 — Số quan trắc, số thuộc tính, định tính / định lượng")
    n_samples, n_features = df.shape[0], df.shape[1] - 1  # không tính ID làm đặc trưng
    print(f"Số quan trắc (hàng): {n_samples}")
    print(f"Số đặc trưng ôn có thể dùng (không đến ID làm predictor): {n_features}")
    print("Kiểu từng cột:")
    print(df.dtypes.replace({"object": "object (chuỗi / danh mục)"}))
    desc = []
    for c in NUMERIC:
        desc.append((c, "định lượng"))
    desc.extend([("Giới tính", "định tính (danh mục)"), ("Mua hàng", "định tính (nhị phân) / label")])
    for c, t in desc:
        print(f"  {c}: {t}")
    display_rows = NUMERIC + CAT + ["ID"]
    print("\nĐầu file:")
    print(df[display_rows].head(11).to_string())


def q2_stats(df: pd.DataFrame) -> None:
    hdr("Câu 2 — Mean / Median / Mode (pandas bỏ qua NaN khi.mean/.median)")
    sub = df[NUMERIC].copy()
    for c in NUMERIC:
        s = sub[c].dropna()
        mean = float(s.mean())
        median = float(s.median())
        mode_series = sub[c].dropna().mode()
        mode_v = (
            mode_series.iloc[0] if len(mode_series) > 0 else float("nan")
        )
        print(f"\n{c}:")
        print(f"  mean={mean:.6g}  median={median:.6g}  mode={mode_v}")
        print(f"  (số các giá trị không phụ thuộc: {sub[c].count()})")


def q3_plots(df: pd.DataFrame) -> None:
    hdr("Câu 3 — Histogram Tuổi, boxplot Lương (+ nhận xét ngắn)")
    tuoi = df["Tuổi"].dropna()

    _, ax = plt.subplots(1, 2, figsize=(10, 4))
    ax[0].hist(tuoi, bins="auto", edgecolor="black")
    ax[0].set_title("Tuổi — histogram")
    ax[0].set_xlabel("Tuổi")

    ax[1].boxplot(df["Lương"].dropna(), tick_labels=["Lương"])
    ax[1].set_title("Lương — boxplot")
    ax[1].set_ylabel("Lương")

    plt.tight_layout()
    fp = HERE / "hist_tuoi_boxplot_luong_baitap02.png"
    plt.savefig(fp, dpi=150)
    plt.close()
    print(f"Đã lưu: {fp}")
    age_skew = float(tuoi.skew())
    print(f"Lệch của Tuổi (skew mẫu): {age_skew:.4f}")
    print(
        "Nhận xét nhanh: tuổi không quá lệch; boxplot lương có đuôi và có điểm −2000 (không thực tế)."
    )


def q4_scatter(df: pd.DataFrame) -> None:
    hdr("Câu 4 — Scatter Tuổi vs Lương")
    d = df[["Tuổi", "Lương"]].dropna(subset=["Tuổi", "Lương"])
    _, ax = plt.subplots(figsize=(5, 4))
    ax.scatter(d["Tuổi"], d["Lương"])
    ax.set_xlabel("Tuổi")
    ax.set_ylabel("Lương")
    ax.axhline(y=0, color="gray", linestyle="--", alpha=0.5)
    ax.set_title("Tuổi–Lương")
    fp = HERE / "scatter_age_luong_baitap02.png"
    plt.tight_layout()
    plt.savefig(fp, dpi=150)
    plt.close()
    print(f"Đã lưu {fp}")
    if len(d) >= 2:
        r = np.corrcoef(d["Tuổi"], d["Lương"])[0, 1]
        print(f"Hệ số tương quan mẫu (Pearson, trên các cặp đồng đủ): r ≈ {r:.4f}")
    print(
        "Gợi ý tiền xử lý: điền thiếu lương/tuổi; cố định hoặc loại −2000; có thể log(lương) sau làm hợp lệ."
    )


def q5_missing(df: pd.DataFrame) -> pd.Series:
    hdr("Câu 5 — Missing: vị trí, số ô, phần trăm")
    miss = df[NUMERIC].isna()
    pct = df[NUMERIC].isna().sum() / len(df) * 100
    for c in NUMERIC:
        idx = df.index[miss[c]].tolist()
        print(f"{c}: thiếu {miss[c].sum()} ô (~{pct[c]:.1f} %) tại chỉ mẫu (ID): {df.loc[idx, 'ID'].tolist()}")
        print(df.loc[miss[c], ["ID", c]])
    return pct


def q6_imputation(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    hdr("Câu 6 — Điền thiếu: mean vs median trên các số sau khi biến lương âm thành NaN (để không kéo trung bình bởi −2000)")
    X = df[NUMERIC].copy()
    X.loc[X["Lương"] < 0, "Lương"] = np.nan

    imp_mean = SimpleImputer(strategy="mean")
    imp_med = SimpleImputer(strategy="median")

    dm = df[["ID"]].copy()
    dm[NUMERIC] = imp_mean.fit_transform(X.to_numpy())

    dk = df[["ID"]].copy()
    dk[NUMERIC] = imp_med.fit_transform(X.to_numpy())

    print("--- Mean imputation ---")
    print(dm.to_string(index=False))
    print("--- Median imputation ---")
    print(dk.to_string(index=False))
    diff = np.abs(dm[NUMERIC].values - dk[NUMERIC].values).max(axis=0)
    print(f"Max |chênh lệch cột| Tuổi, Lương, Điểm = {diff}")
    print(
        "Thông thường lấy median khi có outlier/skew (xem README).",
    )
    return dm, dk


def q7_quality(df: pd.DataFrame) -> None:
    hdr("Câu 7 — Giá trị không hợp lệ (lương âm)")
    mask = df["Lương"] < 0
    print(df.loc[mask, ["ID", "Tuổi", "Lương"]])
    print(
        "Xử lý: thay median/mean sau khi bỏ lỗi, hoặc NA rồi điền; hoặc loại khỏi mẫu nếu thầy đồng ý flag lỗi."
    )


def q8_outliers_salary(df: pd.DataFrame) -> None:
    hdr("Câu 8 — Ngoại lai trên Lương — IQR (1.5) và Z-score (|z|>3)")
    s_full = df["Lương"].dropna()
    # IQR
    q1, q3 = s_full.quantile(0.25), s_full.quantile(0.75)
    iqr = q3 - q1
    low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    out_iqr = df.loc[(df["Lương"].notna()) & ((df["Lương"] < low) | (df["Lương"] > high)), ["ID", "Lương"]]
    print(f"Q1={q1:g} Q3={q3:g} IQR={iqr:g}  khoảng IQR [{low:g}; {high:g}]")
    print("Ngoài khoảng (IQR):")
    print(out_iqr.to_string(index=False) if len(out_iqr) else "(none)")

    # Z-score toàn bộ không thiếu
    vals = df["Lương"].dropna()
    mu, sig = vals.mean(), vals.std(ddof=0)
    z = (vals - mu) / (sig if sig > 1e-12 else 1)
    zs = pd.DataFrame({"ID": df.loc[vals.index, "ID"], "Lương": vals, "z": z.values})
    out_z = zs[np.abs(zs["z"]) > 3]
    print(f"μ={mu:.4g} σ={sig:.4g} (quan sát không thiếu lương)")
    print("Ngưỡng thường |z|>3:")
    print(out_z.to_string(index=False) if len(out_z) else "(none với ±3)")
    print(zs.to_string())


def cleaned_for_later(df: pd.DataFrame, imputed_median_df: pd.DataFrame) -> pd.DataFrame:
    """Điền Tuổi/Điểm/Lương bằng median (từ Câu 6); −2000 → median lương > 0; ghép lại Giới tính / Mua."""
    dc = imputed_median_df.copy()
    dc["Giới tính"] = df["Giới tính"].values
    dc["Mua hàng"] = df["Mua hàng"].values
    med_pos = df.loc[(df["Lương"].notna()) & (df["Lương"] > 0), "Lương"].median()
    dc.loc[df["Lương"].notna() & (df["Lương"] < 0), "Lương"] = med_pos
    return dc


def q9_zscore(df_clean: pd.DataFrame) -> None:
    hdr("Câu 9 — Z-score chỉnh Lương (chuẩn hóa)")
    vals = df_clean[["Lương"]].values
    scaler = StandardScaler(with_mean=True, with_std=True)
    zvals = scaler.fit_transform(vals).ravel()
    out = df_clean[["ID", "Tuổi", "Lương"]].copy()
    out["Lương_z"] = np.round(zvals, 6)
    print(out.to_string(index=False))
    print(
        f"Σ z / n = {zvals.mean():.10f} (chuẩn sklearn ≈ 0 sau StandardScaler có ddof cho σ). "
        f"Độ lệch chỉ là sai số số học nhỏ."
    )


def q10_encoding(df_clean: pd.DataFrame) -> None:
    hdr("Câu 10 — One-hot Giới tính; Purchase Yes/No → 1/0")
    dummies = pd.get_dummies(df_clean["Giới tính"], prefix="Sex", dtype=int)
    y = df_clean["Mua hàng"].map({"Yes": 1, "No": 0})
    merged = pd.concat(
        [
            df_clean[["ID"]],
            df_clean[NUMERIC],
            dummies,
            y.rename("Mua_binary"),
        ],
        axis=1,
    )
    print(merged.to_string(index=False))


def q11_12_placeholder() -> None:
    hdr("Câu 11–12 — Chiến lược đặt tên (xem README bài tay)")
    print(
        "Đọc README_baitap02_per4377.md: đề xuất giữ/thả thuộc tính; PCA vs đơn giản là bớt cột/ID không cho model."
    )


def main() -> None:
    df = df_raw()
    q1_basic(df)
    q2_stats(df)
    q3_plots(df)
    q4_scatter(df)
    q5_missing(df)

    dm, dk = q6_imputation(df)
    q7_quality(df)
    q8_outliers_salary(df)

    cleaned = cleaned_for_later(df, dk)

    q9_zscore(cleaned)
    q10_encoding(cleaned)
    q11_12_placeholder()


if __name__ == "__main__":
    main()
