"""
Classify each evaluated identity by the direction of its bias error,
using the Subgroup / BPSN / BNSP AUCs already computed in cell029.

Interpretation:
  BPSN AUC = Background-Positive, Subgroup-Negative.
    Low BPSN means the model wrongly assigns high toxicity to non-toxic
    mentions of the identity, i.e. OVER-FLAGGING the identity.
  BNSP AUC = Background-Negative, Subgroup-Positive.
    Low BNSP means the model wrongly assigns low toxicity to toxic
    mentions of the identity, i.e. UNDER-FLAGGING toxicity targeting
    the identity.

Direction per identity:
  BPSN < BNSP - 0.005  -> over-flagging
  BNSP < BPSN - 0.005  -> under-flagging
  otherwise            -> balanced

Output: inference_outputs/derived_direction_of_error.md
Numbers are taken verbatim from cell029_*_out01.txt; if that cell is
re-run on Colab with different blends, update the AUCS table below.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "inference_outputs" / "derived_direction_of_error.md"
TOL = 0.005

# (identity, n, subgroup_auc, bpsn_auc, bnsp_auc) -- from cell029
AUCS = [
    ("male",                          2112, 0.9367, 0.9621, 0.9592),
    ("female",                        2602, 0.9418, 0.9722, 0.9515),
    ("homosexual_gay_or_lesbian",      538, 0.8541, 0.9298, 0.9504),
    ("christian",                     2109, 0.9475, 0.9761, 0.9471),
    ("jewish",                         411, 0.9098, 0.9541, 0.9518),
    ("muslim",                        1054, 0.8723, 0.9424, 0.9489),
    ("black",                          761, 0.8670, 0.9258, 0.9573),
    ("white",                         1178, 0.8738, 0.9243, 0.9593),
    ("psychiatric_or_mental_illness",  238, 0.9560, 0.9514, 0.9753),
]


def classify(bpsn: float, bnsp: float) -> str:
    if bpsn < bnsp - TOL:
        return "over-flag"
    if bnsp < bpsn - TOL:
        return "under-flag"
    return "balanced"


def main() -> None:
    rows = []
    for ident, n, sub, bpsn, bnsp in AUCS:
        gap = bpsn - bnsp
        rows.append((ident, n, sub, bpsn, bnsp, gap, classify(bpsn, bnsp)))

    over = [r for r in rows if r[6] == "over-flag"]
    under = [r for r in rows if r[6] == "under-flag"]
    balanced = [r for r in rows if r[6] == "balanced"]

    lines = []
    lines.append("# Direction of error per identity (Pillar 1)")
    lines.append("")
    lines.append(
        "Using the bias-AUC trio from cell029, each evaluated identity is "
        "classified as **over-flag** (BPSN < BNSP, model over-attributes "
        "toxicity to benign identity mentions), **under-flag** (BNSP < BPSN, "
        "model under-attributes toxicity to comments targeting the identity), "
        f"or **balanced** (|BPSN - BNSP| <= {TOL})."
    )
    lines.append("")
    lines.append("| Identity | n | Subgroup AUC | BPSN AUC | BNSP AUC | BPSN - BNSP | Direction |")
    lines.append("|---|---:|---:|---:|---:|---:|:---|")
    for ident, n, sub, bpsn, bnsp, gap, direction in rows:
        lines.append(
            f"| `{ident}` | {n} | {sub:.4f} | {bpsn:.4f} | {bnsp:.4f} | {gap:+.4f} | {direction} |"
        )
    lines.append("")

    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Over-flag ({len(over)}): " + ", ".join(f"`{r[0]}`" for r in sorted(over, key=lambda r: r[5])))
    lines.append(f"- Under-flag ({len(under)}): " + ", ".join(f"`{r[0]}`" for r in sorted(under, key=lambda r: -r[5])))
    if balanced:
        lines.append(f"- Balanced ({len(balanced)}): " + ", ".join(f"`{r[0]}`" for r in balanced))
    lines.append("")
    lines.append(
        "The strongest over-flagging is on race mentions (`white`, `black`) "
        "and on `psychiatric_or_mental_illness`, with substantial over-"
        "flagging also on `homosexual_gay_or_lesbian` and `muslim`: the "
        "model treats these identity tokens as toxicity-adjacent regardless "
        "of context. The strongest under-flagging is on `christian` and "
        "`female`, where the model under-detects toxicity targeting the "
        "group. This split is the asymmetry the Pillar 0 stakeholder "
        "analysis must address: false positives (silencing of identity "
        "mentions) and false negatives (toleration of targeted toxicity) "
        "fall on disjoint identity groups, so a single fairness metric "
        "cannot remediate both directions simultaneously."
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
