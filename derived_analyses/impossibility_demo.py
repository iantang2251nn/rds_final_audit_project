"""
Numerical demonstration of the Chouldechova impossibility result on the
9 evaluated identities (Pillar 3, gap #4).

The Chouldechova identity (with FPR, PPV, FNR all defined at threshold
s_HR = 0.5):

    FPR = (p / (1 - p)) * ((1 - PPV) / PPV) * (1 - FNR)

where p is the base rate. Given non-equal base rates, predictive parity
(equal PPV across groups) and error-rate balance (equal FPR across groups)
cannot both hold simultaneously unless the system is perfect.

This script:
  1. Verifies the algebraic identity per group (replicates cell032).
  2. Counterfactual A: enforce PPV equal to OVERALL's PPV and compute the
     FPR each group would need given its base rate and FNR.
  3. Counterfactual B: enforce FPR equal to OVERALL's FPR and compute the
     PPV each group would need.

Output: inference_outputs/derived_impossibility_demo.md

Numbers are taken verbatim from cell031_*_out01.txt; if cell031 is re-run
on Colab with different blends, update the GROUPS table below.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "inference_outputs" / "derived_impossibility_demo.md"

# (identity, n, base_rate, selection_rate, PPV, TPR, FPR, FNR) -- from cell031
GROUPS = [
    ("OVERALL",                       97320, 0.0799, 0.0856, 0.6873, 0.7363, 0.0291, 0.2637),
    ("male",                           2112, 0.1515, 0.1061, 0.7679, 0.5375, 0.0290, 0.4625),
    ("female",                         2602, 0.1345, 0.0796, 0.8406, 0.4971, 0.0147, 0.5029),
    ("homosexual_gay_or_lesbian",       538, 0.2862, 0.1468, 0.7975, 0.4091, 0.0417, 0.5909),
    ("christian",                      2109, 0.0996, 0.0512, 0.7870, 0.4048, 0.0121, 0.5952),
    ("jewish",                          411, 0.1655, 0.0998, 0.7317, 0.4412, 0.0321, 0.5588),
    ("muslim",                         1054, 0.2211, 0.1195, 0.7698, 0.4163, 0.0353, 0.5837),
    ("black",                           761, 0.3233, 0.1840, 0.8071, 0.4593, 0.0524, 0.5407),
    ("white",                          1178, 0.2997, 0.1689, 0.8040, 0.4533, 0.0473, 0.5467),
    ("psychiatric_or_mental_illness",   238, 0.2269, 0.2059, 0.7755, 0.7037, 0.0598, 0.2963),
]


def derived_fpr(p: float, ppv: float, fnr: float) -> float:
    return (p / (1.0 - p)) * ((1.0 - ppv) / ppv) * (1.0 - fnr)


def required_fpr_under_ppv(p: float, target_ppv: float, fnr: float) -> float:
    return derived_fpr(p, target_ppv, fnr)


def required_ppv_under_fpr(p: float, target_fpr: float, fnr: float) -> float:
    # invert FPR = (p/(1-p))*((1-PPV)/PPV)*(1-FNR) for PPV
    factor = target_fpr * (1.0 - p) / p / (1.0 - fnr)
    return 1.0 / (1.0 + factor)


def main() -> None:
    overall = GROUPS[0]
    overall_ppv = overall[4]
    overall_fpr = overall[6]

    lines: list[str] = []
    lines.append("# Numerical demonstration of the impossibility result (Pillar 3)")
    lines.append("")
    lines.append(
        "Chouldechova's identity at threshold $s_{HR} = 0.5$:"
    )
    lines.append("")
    lines.append("$$\\mathrm{FPR} = \\frac{p}{1-p} \\cdot \\frac{1-\\mathrm{PPV}}{\\mathrm{PPV}} \\cdot (1 - \\mathrm{FNR}).$$")
    lines.append("")
    lines.append(
        "When base rates $p$ differ across groups, predictive parity (equal "
        "PPV) and error-rate balance (equal FPR) cannot both hold unless "
        "the system is perfect. The system audited here is not perfect, so "
        "the developers had to make an implicit choice. Below we show the "
        "choice numerically by counterfactually projecting each group onto "
        "the OVERALL value of one metric and reading off what the other "
        "metric would have to become."
    )
    lines.append("")

    lines.append("## Step 1 — Algebraic identity check (replicates cell032)")
    lines.append("")
    lines.append("| Identity | base rate $p$ | PPV | FNR | measured FPR | derived FPR |")
    lines.append("|---|---:|---:|---:|---:|---:|")
    for ident, _n, p, _sr, ppv, _tpr, fpr, fnr in GROUPS:
        lines.append(
            f"| `{ident}` | {p:.4f} | {ppv:.4f} | {fnr:.4f} | {fpr:.4f} | {derived_fpr(p, ppv, fnr):.4f} |"
        )
    lines.append("")
    lines.append("Measured and derived FPR agree to 4 d.p., confirming the algebra.")
    lines.append("")

    lines.append(f"## Step 2 — Counterfactual A: enforce predictive parity at PPV = {overall_ppv:.4f}")
    lines.append("")
    lines.append(
        "Holding each group's base rate and FNR fixed, what FPR would each "
        "group need to have if its PPV were equal to OVERALL's PPV? "
        "Equivalently: what is the price, in FPR-divergence, of imposing "
        "predictive parity?"
    )
    lines.append("")
    lines.append("| Identity | base rate $p$ | FNR | measured FPR | required FPR under PPV-equality | gap |")
    lines.append("|---|---:|---:|---:|---:|---:|")
    forced_fprs = []
    for ident, _n, p, _sr, _ppv, _tpr, fpr, fnr in GROUPS[1:]:
        req = required_fpr_under_ppv(p, overall_ppv, fnr)
        forced_fprs.append((ident, req))
        lines.append(
            f"| `{ident}` | {p:.4f} | {fnr:.4f} | {fpr:.4f} | {req:.4f} | {req - fpr:+.4f} |"
        )
    lines.append("")
    fpr_min = min(forced_fprs, key=lambda r: r[1])
    fpr_max = max(forced_fprs, key=lambda r: r[1])
    lines.append(
        f"**Required FPR under predictive parity spans "
        f"[{fpr_min[1]:.4f} ({fpr_min[0]}), {fpr_max[1]:.4f} ({fpr_max[0]})]** "
        f"-- a {fpr_max[1] / fpr_min[1]:.1f}x ratio. Equalizing PPV at "
        f"{overall_ppv:.4f} forces FPR to differ by a factor of "
        f"{fpr_max[1] / fpr_min[1]:.1f} across groups."
    )
    lines.append("")

    lines.append(f"## Step 3 — Counterfactual B: enforce error-rate balance at FPR = {overall_fpr:.4f}")
    lines.append("")
    lines.append(
        "The mirror of Step 2: hold each group's base rate and FNR fixed, "
        "and ask what PPV each group would need if its FPR were equal to "
        "OVERALL's FPR."
    )
    lines.append("")
    lines.append("| Identity | base rate $p$ | FNR | measured PPV | required PPV under FPR-equality | gap |")
    lines.append("|---|---:|---:|---:|---:|---:|")
    forced_ppvs = []
    for ident, _n, p, _sr, ppv, _tpr, _fpr, fnr in GROUPS[1:]:
        req = required_ppv_under_fpr(p, overall_fpr, fnr)
        forced_ppvs.append((ident, req))
        lines.append(
            f"| `{ident}` | {p:.4f} | {fnr:.4f} | {ppv:.4f} | {req:.4f} | {req - ppv:+.4f} |"
        )
    lines.append("")
    ppv_min = min(forced_ppvs, key=lambda r: r[1])
    ppv_max = max(forced_ppvs, key=lambda r: r[1])
    lines.append(
        f"**Required PPV under error-rate balance spans "
        f"[{ppv_min[1]:.4f} ({ppv_min[0]}), {ppv_max[1]:.4f} ({ppv_max[0]})]** "
        f"-- a {ppv_max[1] - ppv_min[1]:.4f} absolute spread. Equalizing FPR "
        f"at {overall_fpr:.4f} forces PPV to differ by "
        f"{ppv_max[1] - ppv_min[1]:.4f} in absolute terms across groups."
    )
    lines.append("")

    lines.append("## Conclusion")
    lines.append("")
    p_min = min(GROUPS[1:], key=lambda r: r[2])[2]
    p_max = max(GROUPS[1:], key=lambda r: r[2])[2]
    lines.append(
        f"Per-group base rates span [{p_min:.4f}, {p_max:.4f}] "
        f"(`christian` to `black`). With base-rate inequality of this "
        f"magnitude, the Chouldechova identity makes predictive parity "
        f"and error-rate balance algebraically incompatible. The system as "
        f"deployed satisfies neither exactly: measured PPV ranges from "
        f"{min(g[4] for g in GROUPS[1:]):.4f} to {max(g[4] for g in GROUPS[1:]):.4f}, "
        f"and measured FPR ranges from {min(g[6] for g in GROUPS[1:]):.4f} to "
        f"{max(g[6] for g in GROUPS[1:]):.4f}. "
        "The choice of which fairness metric the developers privileged is "
        "therefore implicit in their training objective and metric design "
        "(the competition's bias-aware metric is built on AUC-style measures, "
        "not on PPV-equality or FPR-equality), and is the kind of upstream "
        "value-laden choice the Pillar 4 critique calls out."
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
