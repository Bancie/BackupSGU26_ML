#!/usr/bin/env python3
"""Xuất hình PDF cây vào ../latex/figures/."""

from __future__ import annotations

import argparse
from pathlib import Path

from categorical_tree import fit
from datasets import (
    LEAF_FEATURES,
    LOAN_C45_FEATURES,
    LOAN_FEATURES,
    SEASON_FEATURES,
    leaf_dataset,
    loan_c45_dataset,
    loan_dataset,
    seasonal_training,
)
from tree_draw import render_tree

FIGURES_DIR = Path(__file__).resolve().parent.parent / "latex" / "figures"


def export_season() -> None:
    df = seasonal_training()
    tree = fit(df, list(SEASON_FEATURES), "Mùa", "entropy")
    render_tree(tree, FIGURES_DIR / "tree_411_muas_entropy.pdf")


def export_season_gini() -> None:
    df = seasonal_training()
    tree = fit(df, list(SEASON_FEATURES), "Mùa", "gini")
    render_tree(tree, FIGURES_DIR / "tree_411_muas_gini.pdf")


def export_season_error() -> None:
    df = seasonal_training()
    tree = fit(df, list(SEASON_FEATURES), "Mùa", "error")
    render_tree(tree, FIGURES_DIR / "tree_411_muas_error.pdf")


def export_leaf() -> None:
    ld = leaf_dataset()
    train = ld[ld["Độc"].notna()].copy()
    tree = fit(train, list(LEAF_FEATURES), "Độc", "gini")
    render_tree(
        tree,
        FIGURES_DIR / "tree_412_la_gini.pdf",
        dx_leaf=1.95,
    )


def export_loan_vn() -> None:
    ld = loan_dataset()
    train = ld[ld["Quyết định"].notna()].copy()
    tree = fit(train, list(LOAN_FEATURES), "Quyết định", "error")
    render_tree(
        tree,
        FIGURES_DIR / "tree_413_vay_error.pdf",
        dx_leaf=2.05,
        dy_depth=1.12,
    )


def export_loan_c45() -> None:
    cdf = loan_c45_dataset()
    tree = fit(cdf, list(LOAN_C45_FEATURES), "Class", "entropy")
    render_tree(
        tree,
        FIGURES_DIR / "tree_414_loan_ig.pdf",
        dx_leaf=1.85,
        dy_depth=1.1,
        fontsize=8.8,
    )


def main() -> None:
    p = argparse.ArgumentParser(description="Xuất hình PDF cây quyết định vào latex/figures/")
    p.add_argument("--all", action="store_true", help="xuất đủ (mặc định)")
    p.add_argument("--season", action="store_true")
    p.add_argument("--season-extra", action="store_true", help="gini và error cho 4.1.1(c)")
    p.add_argument("--leaf", action="store_true")
    p.add_argument("--loan-vn", action="store_true")
    p.add_argument("--loan-c45", action="store_true")
    args = p.parse_args()

    do_all = args.all or not (
        args.season
        or args.season_extra
        or args.leaf
        or args.loan_vn
        or args.loan_c45
    )

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    if do_all:
        export_season()
        export_season_gini()
        export_season_error()
        export_leaf()
        export_loan_vn()
        export_loan_c45()
    else:
        if args.season:
            export_season()
        if args.season_extra:
            export_season_gini()
            export_season_error()
        if args.leaf:
            export_leaf()
        if args.loan_vn:
            export_loan_vn()
        if args.loan_c45:
            export_loan_c45()

    print(f"Đã xuất vào: {FIGURES_DIR}")


if __name__ == "__main__":
    main()
