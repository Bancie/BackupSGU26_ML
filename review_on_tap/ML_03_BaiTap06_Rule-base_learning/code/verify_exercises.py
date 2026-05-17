#!/usr/bin/env python3
"""PER-4785 — verify answers for BaiTap06 Rule-based learning."""

from __future__ import annotations

from collections import defaultdict

from datasets import (
    FOIL_Q3_FEATURES,
    FOIL_Q3_ROWS,
    FOIL_Q3_TARGET,
    PRISM_Q1_FEATURES,
    PRISM_Q1_ROWS,
    PRISM_Q1_TARGET,
    PRISM_Q2_FEATURES,
    PRISM_Q2_ROWS,
    PRISM_Q2_TARGET,
)
from rule_learning import Rule, find_conflicts, foil_train, prism_train, rule_quality


def _fmt_rule(rule: Rule, target_col: str) -> str:
    return rule.as_if_then(target_col)


def _print_prism_case(name: str, rows, features, target_col, pos_label, neg_label) -> None:
    print("=" * 88)
    print(name)
    print("-" * 88)
    print(f"Target positive: {target_col}={pos_label}")

    pos_rules, pos_traces = prism_train(rows, features, target_col, pos_label)
    neg_rules, neg_traces = prism_train(rows, features, target_col, neg_label)

    print("\n[a] PRISM for positive class")
    for i, t in enumerate(pos_traces, start=1):
        print(f"Rule {i}: {_fmt_rule(t['rule'], target_col)}")
        for step_i, step in enumerate(t["steps"], start=1):
            chosen = step["chosen"]
            lit = chosen["literal"]
            print(
                f"  Step {step_i}: choose {lit[0]}={lit[1]} "
                f"(num={chosen['num']}, den={chosen['den']}, acc={chosen['acc']:.4f})"
            )

    print("\n[b] PRISM for negative class")
    for i, t in enumerate(neg_traces, start=1):
        print(f"Rule {i}: {_fmt_rule(t['rule'], target_col)}")
        for step_i, step in enumerate(t["steps"], start=1):
            chosen = step["chosen"]
            lit = chosen["literal"]
            print(
                f"  Step {step_i}: choose {lit[0]}={lit[1]} "
                f"(num={chosen['num']}, den={chosen['den']}, acc={chosen['acc']:.4f})"
            )

    final_rules = pos_rules + neg_rules
    print("\n[c] Final rule set (ordering = learned order)")
    for i, r in enumerate(final_rules, start=1):
        q = rule_quality(rows, r, target_col)
        print(
            f"R{i}: {_fmt_rule(r, target_col)} | "
            f"coverage={q['coverage']:.4f} ({q['covered_count']}/{len(rows)}), "
            f"accuracy={q['accuracy']:.4f} ({q['hit_count']}/{q['covered_count']})"
        )

    conflicts = find_conflicts(rows, final_rules, target_col)
    print("\n[d] Conflicts")
    if not conflicts:
        print("No instance-level conflict (no row matched rules with different consequents).")
    else:
        for c in conflicts:
            print(f"Row {c['id']} true={c['true_label']}")
            for r in c["matched_rules"]:
                print(f"  - {_fmt_rule(r, target_col)}")

    # Accuracy ordering list for conflict resolution reference.
    acc_buckets = defaultdict(list)
    for r in final_rules:
        q = rule_quality(rows, r, target_col)
        acc_buckets[round(q["accuracy"], 10)].append((_fmt_rule(r, target_col), q))
    print("\n[e] Accuracy ordering (desc)")
    for acc in sorted(acc_buckets.keys(), reverse=True):
        for rule_text, q in acc_buckets[acc]:
            print(
                f"  acc={acc:.4f} | cov={q['coverage']:.4f} "
                f"| {rule_text}"
            )


def _print_foil_case() -> None:
    print("=" * 88)
    print("Câu 3 — FOIL gain")
    print("-" * 88)
    rules, traces = foil_train(
        rows=FOIL_Q3_ROWS,
        feature_cols=FOIL_Q3_FEATURES,
        target_col=FOIL_Q3_TARGET,
        target_val="Yes",
    )

    first_step = traces[0]["steps"][0]
    print("[a] FOIL gain at first iteration (p0, n0, p1, n1, gain)")
    for cand in first_step["candidates"]:
        lit = cand["literal"]
        print(
            f"  {lit[0]}={lit[1]:<8} | p0={cand['p0']} n0={cand['n0']} "
            f"p1={cand['p1']} n1={cand['n1']} gain={cand['gain']:.6f}"
        )
    best = first_step["chosen"]
    print(f"Best first literal: {best['literal'][0]}={best['literal'][1]}")

    print("\n[b] Rule growing details")
    for i, tr in enumerate(traces, start=1):
        print(f"Rule {i}: {_fmt_rule(tr['rule'], FOIL_Q3_TARGET)}")
        for step_i, step in enumerate(tr["steps"], start=1):
            chosen = step["chosen"]
            print(
                f"  Step {step_i}: {chosen['literal'][0]}={chosen['literal'][1]} "
                f"(gain={chosen['gain']:.6f}, p1={chosen['p1']}, n1={chosen['n1']})"
            )
            print(
                f"    Remaining positives: {step['remaining_pos_ids']}, "
                f"negatives: {step['remaining_neg_ids']}"
            )

    print("\n[c] Final IF-THEN rules (FOIL)")
    for i, r in enumerate(rules, start=1):
        q = rule_quality(FOIL_Q3_ROWS, r, FOIL_Q3_TARGET)
        print(
            f"R{i}: {_fmt_rule(r, FOIL_Q3_TARGET)} | "
            f"coverage={q['coverage']:.4f}, accuracy={q['accuracy']:.4f}"
        )


def main() -> None:
    _print_prism_case(
        "Câu 1 — PRISM Algorithm",
        PRISM_Q1_ROWS,
        PRISM_Q1_FEATURES,
        PRISM_Q1_TARGET,
        pos_label="Yes",
        neg_label="No",
    )
    _print_prism_case(
        "Câu 2 — Xây dựng luật phân lớp bằng PRISM",
        PRISM_Q2_ROWS,
        PRISM_Q2_FEATURES,
        PRISM_Q2_TARGET,
        pos_label="Pass",
        neg_label="Fail",
    )
    _print_foil_case()
    print("=" * 88)
    print("Done.")


if __name__ == "__main__":
    main()
