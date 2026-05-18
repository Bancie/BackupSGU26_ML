"""Vẽ cây `Internal`/`Leaf` (matplotlib); topology trùng với categorical_tree.fit."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402 — set backend trước

from categorical_tree import DecisionNode, Internal, Leaf


class _Lay:
    __slots__ = ("x_min", "x_max", "x_center", "y", "depth")

    def __init__(
        self,
        x_min: float,
        x_max: float,
        x_center: float,
        y: float,
        depth: int,
    ) -> None:
        self.x_min = x_min
        self.x_max = x_max
        self.x_center = x_center
        self.y = y
        self.depth = depth


def _layoutSubtree(
    node: DecisionNode,
    *,
    y_top: float,
    dx_leaf: float,
    dy_depth: float,
    counter: dict[str, float],
) -> tuple[float, float, dict[int, _Lay]]:
    placement: dict[int, _Lay] = {}

    def recur(n: DecisionNode, depth: int) -> tuple[float, float]:
        cy = y_top - depth * dy_depth

        if isinstance(n, Leaf):
            x = counter["leaf"] * dx_leaf
            counter["leaf"] += 1.0
            placement[id(n)] = _Lay(x, x, x, cy, depth)
            return x, x

        x_lo = float("inf")
        x_hi = float("-inf")
        for _, ch in sorted(n.branches.items(), key=lambda kv: str(kv[0])):
            l, r = recur(ch, depth + 1)
            x_lo = min(x_lo, l)
            x_hi = max(x_hi, r)
        cx = (x_lo + x_hi) / 2.0
        placement[id(n)] = _Lay(x_lo, x_hi, cx, cy, depth)
        return x_lo, x_hi

    x0, x1 = recur(node, 0)
    return x0, x1, placement


def _drawEdges(
    ax: plt.Axes,
    node: DecisionNode,
    placement: dict[int, _Lay],
    *,
    box_half_h: float,
) -> None:
    if isinstance(node, Leaf):
        return
    for lbl, child in sorted(node.branches.items(), key=lambda kv: str(kv[0])):
        p = placement[id(node)]
        c = placement[id(child)]
        y1 = p.y - box_half_h
        y2 = c.y + box_half_h
        xm = (p.x_center + c.x_center) / 2.0
        ym = (y1 + y2) / 2.0
        ax.plot(
            [p.x_center, c.x_center],
            [y1, y2],
            color="#333333",
            linewidth=1.0,
            zorder=1,
        )
        ax.annotate(
            str(lbl),
            xy=(xm, ym),
            fontsize=9,
            ha="center",
            va="center",
            color="#1a1a1a",
            bbox=dict(
                boxstyle="round,pad=0.12",
                facecolor="white",
                edgecolor="none",
                alpha=0.9,
            ),
            zorder=3,
        )
        _drawEdges(ax, child, placement, box_half_h=box_half_h)


def _drawNodes(
    ax: plt.Axes,
    node: DecisionNode,
    placement: dict[int, _Lay],
    *,
    box_half_h: float,
    fontsize: float,
) -> None:
    xy = placement[id(node)]

    if isinstance(node, Leaf):
        text = f"⇒ {node.label}"
        fc = "#e8f4fc"
        ec = "#1f77b4"
    else:
        text = node.attr
        fc = "#fff7e6"
        ec = "#ff7f0e"

    ax.text(
        xy.x_center,
        xy.y,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        zorder=2,
        bbox=dict(
            boxstyle=f"round,pad={max(0.25, fontsize * 0.05)}",
            facecolor=fc,
            edgecolor=ec,
            linewidth=1.2,
        ),
    )

    if isinstance(node, Internal):
        for _, ch in node.branches.items():
            _drawNodes(ax, ch, placement, box_half_h=box_half_h, fontsize=fontsize)


def render_tree(
    node: DecisionNode,
    out_path: Path,
    *,
    title: str | None = None,
    fontsize: float = 9.5,
    figsize_scale: tuple[float, float] = (1.05, 0.82),
    dx_leaf: float = 2.05,
    dy_depth: float = 1.15,
    y_top: float = 0.0,
    dpi: float = 150,
) -> None:
    counter: dict[str, float] = {"leaf": 0.0}
    x0, x1, plac = _layoutSubtree(
        node,
        y_top=y_top,
        dx_leaf=dx_leaf,
        dy_depth=dy_depth,
        counter=counter,
    )

    deepest = max(p.depth for p in plac.values())

    fw = figsize_scale[0] * max(7.8, counter["leaf"] * 2.05)
    fh = figsize_scale[1] * max(6.8, (deepest + 2.35) * 2.05)
    plt.rcParams["font.sans-serif"] = [
        "Arial Unicode MS",
        "DejaVu Sans",
        "Helvetica",
        "sans-serif",
    ]

    fig, ax = plt.subplots(figsize=(fw, fh), dpi=dpi)

    pad_x = dx_leaf * 0.85
    ax.set_xlim(x0 - pad_x, x1 + pad_x)
    ax.set_ylim(
        y_top - (deepest + 1.35) * dy_depth - fontsize * 0.02,
        y_top + 1.05 * dy_depth,
    )

    ax.axis("off")

    box_half_h = fontsize * 0.012 + 0.12

    if title:
        ax.set_title(title, fontsize=fontsize + 1.5, pad=16)

    _drawEdges(ax, node, plac, box_half_h=box_half_h)
    _drawNodes(ax, node, plac, box_half_h=box_half_h, fontsize=fontsize)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        out_path,
        bbox_inches="tight",
        pad_inches=0.08,
        facecolor="white",
    )
    plt.close(fig)
