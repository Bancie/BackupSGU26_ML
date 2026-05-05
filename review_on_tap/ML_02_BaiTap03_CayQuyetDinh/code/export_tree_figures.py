#!/usr/bin/env python3
"""Xuất các hình PDF cây (đúng topology fit) vào ../latex/figures/."""

from __future__ import annotations

import argparse
from pathlib import Path

from categorical_tree import fit
from datasets import (
    LEAF_FEATURES,
    LOAN_FEATURES,
    SEASON_FEATURES,
    leaf_dataset,
    loan_dataset,
    seasonal_training,
)
from tree_draw import render_tree

FIGURES_DIR = Path(__file__).resolve().parent.parent / "latex" / "figures"


def export_season() -> None:
    df = seasonal_training()
    tree = fit(df, list(SEASON_FEATURES), "Mùa", "entropy")
    render_tree(tree, FIGURES_DIR / "tree_muas_entropy.pdf")


def export_leaf() -> None:
    ld = leaf_dataset()
    train = ld[ld["Độc"].notna()].copy()
    tree = fit(train, list(LEAF_FEATURES), "Độc", "gini")
    render_tree(
        tree,
        FIGURES_DIR / "tree_la_gini.pdf",
        dx_leaf=1.95,
    )


def export_loan() -> None:
    ld = loan_dataset()
    train = ld[ld["Quyết định"].notna()].copy()
    tree = fit(train, list(LOAN_FEATURES), "Quyết định", "error")
    render_tree(
        tree,
        FIGURES_DIR / "tree_vay_error.pdf",
        dx_leaf=2.05,
        dy_depth=1.12,
    )


def main() -> None:
    p = argparse.ArgumentParser(description="Xuất hình PDF cây quyết định vào latex/figures/")
    p.add_argument(
        "--all",
        action="store_true",
        help="xuất đủ 3 hình (mặc định)",
    )
    p.add_argument("--season", action="store_true")
    p.add_argument("--leaf", action="store_true")
    p.add_argument("--loan", action="store_true")
    args = p.parse_args()

    do_all = args.all or not (args.season or args.leaf or args.loan)

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    if do_all:
        export_season()
        export_leaf()
        export_loan()
    else:
        if args.season:
            export_season()
        if args.leaf:
            export_leaf()
        if args.loan:
            export_loan()

    print(f"Đã xuất vào: {FIGURES_DIR}")


if __name__ == "__main__":
    main()
