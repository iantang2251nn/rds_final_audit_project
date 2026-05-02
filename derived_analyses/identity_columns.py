"""
Enumerate the identity columns in the Civil Comments private test set,
distinguishing the 9 evaluated by the competition's bias-aware metric
from the 15 that were collected but excluded. Reports per-identity
sample counts at the 0.5 mention-threshold so the inclusion / exclusion
decision is visible numerically.

Output: inference_outputs/derived_identity_inclusion.md
Stdlib-only (no pandas) to keep the local toolchain minimal.
"""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "bullshit" / "original solution for reference" / "input" / "jigsaw-unintended-bias-in-toxicity-classification" / "test_private_expanded.csv"
OUT = ROOT / "inference_outputs" / "derived_identity_inclusion.md"
THRESHOLD = 0.5

EVALUATED = {
    "male", "female",
    "homosexual_gay_or_lesbian",
    "christian", "jewish", "muslim",
    "black", "white",
    "psychiatric_or_mental_illness",
}

GROUPS = {
    "Gender": ["male", "female", "transgender", "other_gender"],
    "Sexual orientation": ["heterosexual", "homosexual_gay_or_lesbian", "bisexual", "other_sexual_orientation"],
    "Religion": ["christian", "jewish", "muslim", "hindu", "buddhist", "atheist", "other_religion"],
    "Race / ethnicity": ["black", "white", "asian", "latino", "other_race_or_ethnicity"],
    "Disability": ["physical_disability", "intellectual_or_learning_disability", "psychiatric_or_mental_illness", "other_disability"],
}


def main() -> None:
    all_cols = [c for cols in GROUPS.values() for c in cols]
    counts = {c: 0 for c in all_cols}
    n = 0
    with CSV_PATH.open(newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            n += 1
            for c in all_cols:
                v = row.get(c, "")
                if v and float(v) >= THRESHOLD:
                    counts[c] += 1

    lines = []
    lines.append("# Identity column inclusion / exclusion in the metric (Pillar 4)")
    lines.append("")
    lines.append(f"Source: `test_private_expanded.csv` (n = {n}; mention threshold = {THRESHOLD}).")
    lines.append("")
    lines.append(
        "The Jigsaw competition's bias-aware metric evaluates **9 of the 24** "
        "identity columns collected in Civil Comments. The table below shows "
        "all 24 with sample counts at the 0.5 mention-threshold; the rightmost "
        "column flags whether the metric evaluates that identity."
    )
    lines.append("")

    for group, cols in GROUPS.items():
        lines.append(f"## {group}")
        lines.append("")
        lines.append("| Identity | n at threshold | Evaluated by metric |")
        lines.append("|---|---:|:---:|")
        for c in cols:
            mark = "yes" if c in EVALUATED else "no"
            lines.append(f"| `{c}` | {counts[c]} | {mark} |")
        lines.append("")

    evaluated_n = sum(counts[c] for c in EVALUATED)
    excluded = [c for c in all_cols if c not in EVALUATED]
    excluded_n = sum(counts[c] for c in excluded)
    smallest_eval = min(EVALUATED, key=lambda c: counts[c])
    largest_excl = max(excluded, key=lambda c: counts[c])

    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Evaluated subgroups (9): {evaluated_n} total mentions at threshold {THRESHOLD}.")
    lines.append(f"- Excluded subgroups (15): {excluded_n} total mentions at threshold {THRESHOLD}.")
    lines.append(
        f"- All 9 evaluated subgroups have n >= {counts[smallest_eval]} "
        f"(smallest: `{smallest_eval}`). All 15 excluded subgroups have "
        f"n <= {counts[largest_excl]} (largest: `{largest_excl}`). "
        "The selection therefore appears sample-size driven, with a cutoff "
        f"falling between {counts[largest_excl]} and {counts[smallest_eval]} "
        "mentions in the private test set."
    )
    lines.append("")
    lines.append(
        "Rendering this list visible matters for the Pillar 4 critique: "
        "the metric's identity selection is itself a normative choice. The "
        "rule \"we evaluate where we have data\" compounds the visibility "
        "problem of under-represented identities. Subgroups such as "
        "`transgender`, `bisexual`, `asian`, `latino`, `hindu`, `buddhist`, "
        "`atheist`, and every disability category other than "
        "`psychiatric_or_mental_illness` are present in the dataset and "
        "annotated, but their performance gaps do not enter the bias-aware "
        "score the competition rewarded. Identities most likely to suffer "
        "rare-but-severe harms are systematically the ones excluded by a "
        "sample-size-driven cutoff."
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
