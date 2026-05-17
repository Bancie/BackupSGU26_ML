"""PRISM and FOIL helpers for BaiTap06."""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Dict, List, Sequence, Tuple

Row = Dict[str, object]
Literal = Tuple[str, object]


@dataclass(frozen=True)
class Rule:
    antecedents: Tuple[Literal, ...]
    consequent: str

    def as_if_then(self, target_col: str) -> str:
        left = " AND ".join(f"{a}={v}" for a, v in self.antecedents)
        return f"IF {left} THEN {target_col}={self.consequent}"


def _satisfies(row: Row, antecedents: Sequence[Literal]) -> bool:
    return all(row[attr] == val for attr, val in antecedents)


def _count(rows: Sequence[Row], antecedents: Sequence[Literal], target_col: str, target_val: str) -> Tuple[int, int]:
    covered = [r for r in rows if _satisfies(r, antecedents)]
    positive = [r for r in covered if r[target_col] == target_val]
    return len(positive), len(covered)


def _all_literals(rows: Sequence[Row], feature_cols: Sequence[str]) -> List[Literal]:
    lits: List[Literal] = []
    for col in feature_cols:
        values = sorted({r[col] for r in rows})
        for v in values:
            lits.append((col, v))
    return lits


def prism_train(
    rows: Sequence[Row],
    feature_cols: Sequence[str],
    target_col: str,
    target_val: str,
) -> Tuple[List[Rule], List[dict]]:
    """Train PRISM rules for a single target class."""
    remaining = list(rows)
    all_literals = _all_literals(rows, feature_cols)
    rules: List[Rule] = []
    traces: List[dict] = []

    while any(r[target_col] == target_val for r in remaining):
        current_subset = list(remaining)
        antecedents: List[Literal] = []
        used_attrs: set[str] = set()
        step_logs: List[dict] = []

        while True:
            candidates = []
            for attr, val in all_literals:
                if attr in used_attrs:
                    continue
                matched = [r for r in current_subset if r[attr] == val]
                if not matched:
                    continue
                num = sum(1 for r in matched if r[target_col] == target_val)
                den = len(matched)
                acc = num / den
                candidates.append(
                    {
                        "literal": (attr, val),
                        "num": num,
                        "den": den,
                        "acc": acc,
                    }
                )

            if not candidates:
                break

            # Tie-break: highest accuracy, then highest cover (den), then highest numerator.
            candidates.sort(
                key=lambda c: (c["acc"], c["den"], c["num"], str(c["literal"])),
                reverse=True,
            )
            best = candidates[0]
            antecedents.append(best["literal"])
            used_attrs.add(best["literal"][0])
            current_subset = [
                r for r in current_subset if r[best["literal"][0]] == best["literal"][1]
            ]
            step_logs.append(
                {
                    "candidates": candidates,
                    "chosen": best,
                    "subset_size_after": len(current_subset),
                    "positives_after": sum(
                        1 for r in current_subset if r[target_col] == target_val
                    ),
                }
            )

            if current_subset and all(r[target_col] == target_val for r in current_subset):
                break

        rule = Rule(antecedents=tuple(antecedents), consequent=target_val)
        rules.append(rule)

        covered_pos, covered_all = _count(
            remaining, rule.antecedents, target_col=target_col, target_val=target_val
        )
        traces.append(
            {
                "rule": rule,
                "steps": step_logs,
                "covered_pos_in_remaining": covered_pos,
                "covered_all_in_remaining": covered_all,
            }
        )

        remaining = [
            r
            for r in remaining
            if not (_satisfies(r, rule.antecedents) and r[target_col] == target_val)
        ]

    return rules, traces


def rule_quality(
    rows: Sequence[Row],
    rule: Rule,
    target_col: str,
) -> dict:
    covered = [r for r in rows if _satisfies(r, rule.antecedents)]
    hit = [r for r in covered if r[target_col] == rule.consequent]
    total = len(rows)
    return {
        "covered_count": len(covered),
        "hit_count": len(hit),
        "coverage": len(covered) / total if total else 0.0,
        "accuracy": len(hit) / len(covered) if covered else 0.0,
        "covered_ids": [r["S.No"] for r in covered],
    }


def find_conflicts(
    rows: Sequence[Row],
    rules: Sequence[Rule],
    target_col: str,
) -> List[dict]:
    conflicts: List[dict] = []
    for r in rows:
        matched = [rule for rule in rules if _satisfies(r, rule.antecedents)]
        consequents = sorted({rule.consequent for rule in matched})
        if len(consequents) > 1:
            conflicts.append(
                {
                    "id": r["S.No"],
                    "true_label": r[target_col],
                    "matched_rules": matched,
                }
            )
    return conflicts


def foil_gain(p0: int, n0: int, p1: int, n1: int) -> float:
    if p1 == 0:
        return float("-inf")
    before = p0 / (p0 + n0) if (p0 + n0) else 0.0
    after = p1 / (p1 + n1) if (p1 + n1) else 0.0
    if before == 0 or after == 0:
        return float("-inf")
    return p1 * (math.log2(after) - math.log2(before))


def foil_train(
    rows: Sequence[Row],
    feature_cols: Sequence[str],
    target_col: str,
    target_val: str,
) -> Tuple[List[Rule], List[dict]]:
    """Train binary FOIL rule set for target_val."""
    remaining_pos = [r for r in rows if r[target_col] == target_val]
    all_neg = [r for r in rows if r[target_col] != target_val]
    all_literals = _all_literals(rows, feature_cols)
    rules: List[Rule] = []
    traces: List[dict] = []

    while remaining_pos:
        curr_pos = list(remaining_pos)
        curr_neg = list(all_neg)
        antecedents: List[Literal] = []
        used_attrs: set[str] = set()
        step_logs: List[dict] = []

        while curr_neg:
            p0 = len(curr_pos)
            n0 = len(curr_neg)
            candidates = []
            for literal_idx, (attr, val) in enumerate(all_literals):
                if attr in used_attrs:
                    continue
                pos1 = [r for r in curr_pos if r[attr] == val]
                neg1 = [r for r in curr_neg if r[attr] == val]
                p1 = len(pos1)
                n1 = len(neg1)
                gain = foil_gain(p0, n0, p1, n1)
                candidates.append(
                    {
                        "literal": (attr, val),
                        "p0": p0,
                        "n0": n0,
                        "p1": p1,
                        "n1": n1,
                        "gain": gain,
                        "literal_idx": literal_idx,
                    }
                )

            candidates = [c for c in candidates if c["p1"] > 0]
            candidates.sort(
                key=lambda c: (
                    -c["gain"],
                    -(c["p1"] / (c["p1"] + c["n1"]) if (c["p1"] + c["n1"]) else -1.0),
                    -c["p1"],
                    c["n1"],
                    c["literal_idx"],
                ),
            )

            best = candidates[0]
            antecedents.append(best["literal"])
            used_attrs.add(best["literal"][0])
            curr_pos = [r for r in curr_pos if r[best["literal"][0]] == best["literal"][1]]
            curr_neg = [r for r in curr_neg if r[best["literal"][0]] == best["literal"][1]]
            step_logs.append(
                {
                    "candidates": candidates,
                    "chosen": best,
                    "remaining_pos_ids": [r["S.No"] for r in curr_pos],
                    "remaining_neg_ids": [r["S.No"] for r in curr_neg],
                }
            )

        rule = Rule(antecedents=tuple(antecedents), consequent=target_val)
        rules.append(rule)
        traces.append({"rule": rule, "steps": step_logs})
        covered_pos = [r for r in remaining_pos if _satisfies(r, rule.antecedents)]
        covered_ids = {r["S.No"] for r in covered_pos}
        remaining_pos = [r for r in remaining_pos if r["S.No"] not in covered_ids]

    return rules, traces
