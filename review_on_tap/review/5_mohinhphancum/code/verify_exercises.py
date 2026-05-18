"""PER-4805 — Mô hình phân cụm (K-means + phân cụm phân cấp single linkage).

In kết quả từng bước để đối chiếu với lời giải LaTeX.
"""

from __future__ import annotations

import numpy as np
from scipy.cluster.hierarchy import linkage
from scipy.spatial.distance import pdist, squareform

EPS = 1e-9


def euclidean(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.linalg.norm(a - b))


def kmeans_manual(
    X: np.ndarray,
    names: list[str],
    centroids0: np.ndarray,
    header: str,
) -> tuple[np.ndarray, np.ndarray]:
    """Lloyd: gán theo Euclidean, cập nhật tâm = trung bình. Dừng khi tâm không đổi."""
    print(f"\n{'=' * 72}\n{header}\n{'=' * 72}")
    m, _dim = X.shape
    k = centroids0.shape[0]
    C = centroids0.copy().astype(float)
    it = 0

    while True:
        print(f"\n--- Vòng gán/cập nhật {it}: tâm dùng để gán ---")
        for j in range(k):
            print(f"  C_{j + 1}^({it}) = ({', '.join(f'{c:.6g}' for c in C[j])})")

        dist_mat = np.zeros((m, k))
        for i in range(m):
            for j in range(k):
                dist_mat[i, j] = euclidean(X[i], C[j])
            parts = ", ".join(f"d(_, C_{j + 1})={dist_mat[i, j]:.6g}" for j in range(k))
            print(f"  {names[i]}: {parts} -> cụm {int(dist_mat[i].argmin()) + 1}")

        labels = dist_mat.argmin(axis=1)
        clusters = [np.where(labels == j)[0].tolist() for j in range(k)]
        for j in range(k):
            pts = ", ".join(names[i] for i in clusters[j])
            print(f"  Gán vào cụm {j + 1}: {{{pts}}}")

        C_new = np.stack([X[clusters[j]].mean(axis=0) for j in range(k)])

        print("\n  Cập nhật tâm sau khi gán:")
        for j in range(k):
            xs = ", ".join(f"{v:.6g}" for v in C_new[j])
            print(f"  C_{j + 1}^({it + 1}) = ({xs})")

        if np.linalg.norm(C_new - C) < EPS:
            print("\n=> Tâm không đổi (đến độ chính xác máy) — thuật toán hội tụ.")
            C = C_new
            break

        C = C_new
        it += 1

    clusters_final = [np.where(labels == j)[0].tolist() for j in range(k)]
    print("\n--- Kết quả cuối ---")
    for j in range(k):
        pts = ", ".join(names[i] for i in clusters_final[j])
        print(f"  Cụm {j + 1}: {{{pts}}}")
        print(f"  Tâm cuối C_{j + 1}: ({', '.join(f'{c:.6g}' for c in C[j])})")
    return C, labels


def print_sklearn_check(X: np.ndarray, init: np.ndarray) -> None:
    try:
        from sklearn.cluster import KMeans

        km = KMeans(
            n_clusters=init.shape[0],
            init=init,
            n_init=1,
            max_iter=300,
            tol=1e-10,
            random_state=0,
        )
        km.fit(X)
        print("\n[Đối chiếu sklearn KMeans, n_init=1, init cố định]")
        print("  labels:", km.labels_.tolist())
        print("  cluster_centers_:", km.cluster_centers_)
    except Exception as exc:
        print(f"\n(sklearn không kiểm tra được: {exc})")


def print_single_linkage(X: np.ndarray, labels: list[str], title: str) -> None:
    print(f"\n{'=' * 72}\n{title}\n{'=' * 72}")
    m = X.shape[0]
    dist_condensed = pdist(X, metric="euclidean")
    mat = squareform(dist_condensed)
    print("\nMa trận khoảng cách Euclidean đối xứng:")
    hdr = "      " + "".join(f"{lab:>10}" for lab in labels)
    print(hdr)
    for i in range(m):
        row = f"{labels[i]:>6}"
        for j in range(m):
            row += f"{mat[i, j]:10.6g}"
        print(row)

    Z = linkage(dist_condensed, method="single")
    print("\nBảng linkage (single): mỗi dòng [idx1, idx2, dist, count]")
    print("  idx < n: điểm gốc; idx >= n: cụm đã hợp nhất (cluster idx-n)")
    for row in Z:
        i1, i2, dist, cnt = int(row[0]), int(row[1]), float(row[2]), int(row[3])
        print(f"  Hợp nhất {i1}, {i2} với khoảng cách = {dist:.12g}, |cluster|={cnt}")


def main() -> None:
    # ----- 5.1.1 -----
    X511 = np.array([[1.0, 1.0], [2.0, 1.0], [4.0, 3.0], [5.0, 4.0]], dtype=float)
    names511 = ["P1", "P2", "P3", "P4"]
    c0511 = np.array([[1.0, 1.0], [5.0, 4.0]], dtype=float)
    kmeans_manual(X511, names511, c0511, "Câu 5.1.1 — K-means k=2 (tâm khởi tạo P1, P4)")
    print_sklearn_check(X511, c0511)

    # ----- 5.1.2 -----
    X512 = np.array(
        [[1.0, 2.0], [2.0, 1.0], [4.0, 3.0], [5.0, 4.0], [3.0, 5.0], [6.0, 5.0]],
        dtype=float,
    )
    names512 = ["A", "B", "C", "D", "E", "F"]
    c0512 = np.array([[1.0, 2.0], [5.0, 4.0]], dtype=float)
    kmeans_manual(X512, names512, c0512, "Câu 5.1.2 — K-means k=2 (tâm khởi tạo A, D)")
    print_sklearn_check(X512, c0512)

    # ----- 5.1.3 -----
    X513 = np.array(
        [
            [1.0, 1.0],
            [1.5, 2.0],
            [3.0, 4.0],
            [5.0, 7.0],
            [3.5, 5.0],
            [4.5, 5.0],
            [3.5, 4.5],
        ],
        dtype=float,
    )
    names513 = [f"Đối tượng {i}" for i in range(1, 8)]
    c0513 = np.array([[1.0, 1.0], [5.0, 7.0]], dtype=float)
    kmeans_manual(
        X513,
        names513,
        c0513,
        "Câu 5.1.3 — K-means k=2 (tâm khởi tạo đối tượng 1 và 4)",
    )
    print_sklearn_check(X513, c0513)

    # ----- 5.2.1 hierarchical ABC -----
    X521 = np.array([[1.0, 1.0], [1.5, 1.5], [5.0, 5.0]], dtype=float)
    print_single_linkage(X521, ["A", "B", "C"], "Câu 5.2.1 — Phân cụm phân cấp (single linkage), điểm A, B, C")

    # ----- 5.2.2 hierarchical DEF -----
    X522 = np.array([[3.0, 4.0], [4.0, 4.0], [3.0, 3.5]], dtype=float)
    print_single_linkage(X522, ["D", "E", "F"], "Câu 5.2.2 — Phân cụm phân cấp (single linkage), điểm D, E, F")


if __name__ == "__main__":
    main()
