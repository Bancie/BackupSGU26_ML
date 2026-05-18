"""KNN §4.4.1 — cho vay tín dụng (PER-4809). Xác minh khoảng cách và đa số láng giềng."""

from __future__ import annotations

from collections import Counter

import numpy as np

EPS = 1e-12

# Mã hoá: Có -> 1, Không -> 0
TRAIN = np.array(
    [
        [25, 1, 20, 120],  # 1
        [22, 0, 15, 200],  # 2
        [24, 1, 18, 180],  # 3
        [30, 0, 17, 130],  # 4
        [31, 1, 22, 250],  # 5
        [35, 1, 22, 150],  # 6
        [22, 0, 23, 210],  # 7
        [28, 1, 19, 280],  # 8
    ],
    dtype=float,
)
LABELS = np.array(["Yes", "No", "Yes", "Yes", "No", "Yes", "No", "No"])

QUERY = np.array([23.0, 1.0, 32.0, 250.0])


def euclidean(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.linalg.norm(a - b))


def minmax_fit_transform(
    train: np.ndarray,
    query: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    tmin = train.min(axis=0)
    tmax = train.max(axis=0)
    denom = np.where((tmax - tmin) < EPS, 1.0, tmax - tmin)

    def tr(x: np.ndarray) -> np.ndarray:
        return (x - tmin) / denom

    return tr(train.copy()), tr(query.copy().reshape(1, -1)).ravel()


def knn_vote(
    dists: list[tuple[int, float, str]],
    k: int,
) -> tuple[str, list[tuple[int, float, str]]]:
    neighbors = dists[:k]
    votes = Counter(lab for _, _, lab in neighbors)
    pred = sorted(votes.items(), key=lambda kv: (-kv[1], str(kv[0])))[0][0]
    return pred, neighbors


def main() -> None:
    rows = [(i + 1, TRAIN[i], LABELS[i]) for i in range(len(TRAIN))]
    dist_sorted: list[tuple[int, float, str]] = []
    for sid, xv, lab in rows:
        d = euclidean(xv, QUERY)
        dist_sorted.append((sid, d, str(lab)))
    dist_sorted.sort(key=lambda t: (t[1], str(t[2])))

    print("=== Dữ liệu huấn luyện (vector: Tuổi, Gia_đình, Thu_nhập, Số_tiền_vay) ===")
    for sid, xv, lab in rows:
        print(f"  ID {sid}: {xv.astype(int).tolist()}  ->  {lab}")
    print("\nTruy vấn:", QUERY.astype(int).tolist(), "(Có -> 1)")

    print("\n=== Euclidean (không chuẩn hoá): bình phương khoảng cách d^2, rồi d ===")
    d2_rows = [(sid, d * d, d, lab) for sid, d, lab in dist_sorted]
    for sid, d2, d, lab in sorted(d2_rows, key=lambda t: (t[1], t[0])):
        print(f"  ID {sid}: d^2={d2:.6g}    d={d:.6g}    {lab}")
    print("(Sắp xếp láng giềng: ưu tiên d nhỏ, hòa theo nhãn từ điển)")

    for k in (3, 5):
        pred, nei = knn_vote(dist_sorted, k)
        print(f"\n--- k={k} --- láng giềng:", [(s, f"d={round(d,4)}", lab) for s, d, lab in nei])
        print(f"Đa số (phá hòa: |phiếu| lớn, rồi nhãn từ điển): {pred}")

    print("\n=== Min–Max chỉ học min/max trên tập huấn luyện, rồi Euclidean ===")
    X_mm, q_mm = minmax_fit_transform(TRAIN, QUERY)
    mm_sorted: list[tuple[int, float, str]] = []
    for i in range(len(TRAIN)):
        d = euclidean(X_mm[i], q_mm)
        mm_sorted.append((i + 1, d, str(LABELS[i])))
    mm_sorted.sort(key=lambda t: (t[1], str(t[2])))
    for sid, d, lab in mm_sorted:
        print(f"  ID {sid}: d={d:.6g}    {lab}")
    for k in (3, 5):
        pred, nei = knn_vote(mm_sorted, k)
        print(f"  k={k} -> {pred}, láng giềng ID: {[s for s, _, _ in nei]}")


if __name__ == "__main__":
    main()
