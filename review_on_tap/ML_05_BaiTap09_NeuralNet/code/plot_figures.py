#!/usr/bin/env python3
"""Tạo hình cho LaTeX — chạy từ thư mục code/ hoặc gọi trực tiếp."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Thư mục đích: .../ML_05_BaiTap09_NeuralNet/latex/figures
ROOT = Path(__file__).resolve().parent.parent
FIG_DIR = ROOT / "latex" / "figures"


def plot_or_and() -> None:
    fig, axes = plt.subplots(1, 2, figsize=(8, 3.8))

    def draw_points(ax, title: str, or_mode: bool) -> None:
        pts_neg = [(0, 0)] if or_mode else [(0, 0), (1, 0), (0, 1)]
        pts_pos = [(1, 0), (0, 1), (1, 1)] if or_mode else [(1, 1)]
        for x1, x2 in pts_neg:
            ax.scatter([x1], [x2], s=120, c="silver", edgecolors="k", marker="s", zorder=3)
        for x1, x2 in pts_pos:
            ax.scatter([x1], [x2], s=120, c="lightblue", edgecolors="k", marker="o", zorder=3)
        xs = np.linspace(-0.2, 1.2, 50)
        if or_mode:
            ax.plot(xs, 0.5 - xs, "r--", lw=2, label=r"$x_1+x_2=\frac{1}{2}$")
        else:
            ax.plot(xs, 1.5 - xs, "g--", lw=2, label=r"$x_1+x_2=\frac{3}{2}$")
        ax.set_xlim(-0.25, 1.25)
        ax.set_ylim(-0.25, 1.25)
        ax.set_aspect("equal")
        ax.set_xlabel(r"$x_1$")
        ax.set_ylabel(r"$x_2$")
        ax.set_title(title)
        ax.grid(True, alpha=0.3)
        ax.legend(loc="upper right", fontsize=8)

    draw_points(axes[0], "OR (vuông = $-1$, tròn = $+1$)", True)
    draw_points(axes[1], "AND", False)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig_or_and.pdf", bbox_inches="tight")
    plt.close(fig)


def plot_perceptron_gd() -> None:
    fig, ax = plt.subplots(figsize=(5, 5))
    X = [(0, 0), (1, 0), (0, 1), (1, 1)]
    t = [-1, 1, 1, 1]
    for (x1, x2), tv in zip(X, t, strict=True):
        m = "s" if tv < 0 else "o"
        c = "silver" if tv < 0 else "coral"
        ax.scatter([x1], [x2], s=160, c=c, edgecolors="k", marker=m, zorder=3)
    xs = np.linspace(-0.2, 1.15, 80)
    ax.plot(xs, 0.5 * np.ones_like(xs), "b-", lw=2, label=r"Bước 0: $x_2=\frac{1}{2}$")
    ax.plot(xs, 0.1 - 0.4 * xs, "m-", lw=2, label=r"Bước 1: $\frac{2}{5}x_1+x_2=\frac{1}{10}$")
    ax.set_xlim(-0.25, 1.25)
    ax.set_ylim(-0.25, 1.25)
    ax.set_aspect("equal")
    ax.set_xlabel(r"$x_1$")
    ax.set_ylabel(r"$x_2$")
    ax.legend(loc="lower left")
    ax.grid(True, alpha=0.3)
    ax.set_title(r"Perceptron GD batch, $\rho=\frac{2}{5}$")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig_perceptron_gd.pdf", bbox_inches="tight")
    plt.close(fig)


def plot_regression_gd() -> None:
    xs = np.array([0.0, 1.0, 2.0, 3.0])
    ys = np.array([1.0, 3.0, 5.0, 7.0])
    m = len(xs)
    rho = 0.1

    def grads(w: float, b: float) -> tuple[float, float]:
        pred = w * xs + b
        err = ys - pred
        return float(-(err * xs).sum() / m), float(-err.sum() / m)

    states = [(0.0, 1.0, "0")]
    w, b = 0.0, 1.0
    for it in range(1, 4):
        gw, gb = grads(w, b)
        w -= rho * gw
        b -= rho * gb
        states.append((w, b, str(it)))

    fig, ax = plt.subplots(figsize=(5.5, 4))
    ax.scatter(xs, ys, s=90, c="k", zorder=4, label="Dữ liệu")
    xx = np.linspace(-0.2, 3.4, 50)
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]
    for (w, b, lab), col in zip(states, colors, strict=True):
        ax.plot(xx, w * xx + b, lw=2, c=col, label=f"Vòng {lab}: $\\hat y={w:.4g}x+({b:.4g})$")
    ax.set_xlim(-0.35, 3.5)
    ax.set_ylim(-0.5, 8.5)
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")
    ax.legend(loc="upper left", fontsize=8)
    ax.grid(True, alpha=0.3)
    ax.set_title(r"Hồi quy --- các đường $\hat y=wx+b$ ($\rho=\frac{1}{10}$)")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig_regression_gd.pdf", bbox_inches="tight")
    plt.close(fig)


def plot_cnn_diagram() -> None:
    fig, ax = plt.subplots(figsize=(8.5, 2.4))
    ax.axis("off")
    boxes = [
        (0, "Input\n$28\\times28\\times1$"),
        (1.6, "Conv2D 64\n$26\\times26\\times64$"),
        (3.2, "ReLU\n$26\\times26\\times64$"),
        (4.8, "MaxPool\n$13\\times13\\times64$"),
        (6.4, "Flatten\n$10816$"),
        (8.0, "Dense ReLU\n$128$"),
        (9.6, "Dense softm.\n$10$"),
    ]
    w_box = 1.35
    h_box = 1.1
    for x0, txt in boxes:
        ax.add_patch(
            plt.Rectangle(
                (x0, 0.35),
                w_box,
                h_box,
                fill=True,
                facecolor="#e8f4fc",
                edgecolor="navy",
                lw=1.2,
            )
        )
        ax.text(x0 + w_box / 2, 0.35 + h_box / 2, txt, ha="center", va="center", fontsize=8)
    for i in range(len(boxes) - 1):
        x1 = boxes[i][0] + w_box
        x2 = boxes[i + 1][0]
        ax.annotate(
            "",
            xy=(x2, 0.9),
            xytext=(x1, 0.9),
            arrowprops=dict(arrowstyle="->", lw=1.2),
        )
    ax.set_xlim(-0.2, 11.3)
    ax.set_ylim(0, 1.9)
    fig.savefig(FIG_DIR / "fig_cnn_arch.pdf", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    plot_or_and()
    plot_perceptron_gd()
    plot_regression_gd()
    plot_cnn_diagram()
    print(f"Đã ghi hình vào: {FIG_DIR}")


if __name__ == "__main__":
    main()
