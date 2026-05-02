# Numerical demonstration of the impossibility result (Pillar 3)

Chouldechova's identity at threshold $s_{HR} = 0.5$:

$$\mathrm{FPR} = \frac{p}{1-p} \cdot \frac{1-\mathrm{PPV}}{\mathrm{PPV}} \cdot (1 - \mathrm{FNR}).$$

When base rates $p$ differ across groups, predictive parity (equal PPV) and error-rate balance (equal FPR) cannot both hold unless the system is perfect. The system audited here is not perfect, so the developers had to make an implicit choice. Below we show the choice numerically by counterfactually projecting each group onto the OVERALL value of one metric and reading off what the other metric would have to become.

## Step 1 — Algebraic identity check (replicates cell032)

| Identity | base rate $p$ | PPV | FNR | measured FPR | derived FPR |
|---|---:|---:|---:|---:|---:|
| `OVERALL` | 0.0799 | 0.6873 | 0.2637 | 0.0291 | 0.0291 |
| `male` | 0.1515 | 0.7679 | 0.4625 | 0.0290 | 0.0290 |
| `female` | 0.1345 | 0.8406 | 0.5029 | 0.0147 | 0.0146 |
| `homosexual_gay_or_lesbian` | 0.2862 | 0.7975 | 0.5909 | 0.0417 | 0.0417 |
| `christian` | 0.0996 | 0.7870 | 0.5952 | 0.0121 | 0.0121 |
| `jewish` | 0.1655 | 0.7317 | 0.5588 | 0.0321 | 0.0321 |
| `muslim` | 0.2211 | 0.7698 | 0.5837 | 0.0353 | 0.0353 |
| `black` | 0.3233 | 0.8071 | 0.5407 | 0.0524 | 0.0524 |
| `white` | 0.2997 | 0.8040 | 0.5467 | 0.0473 | 0.0473 |
| `psychiatric_or_mental_illness` | 0.2269 | 0.7755 | 0.2963 | 0.0598 | 0.0598 |

Measured and derived FPR agree to 4 d.p., confirming the algebra.

## Step 2 — Counterfactual A: enforce predictive parity at PPV = 0.6873

Holding each group's base rate and FNR fixed, what FPR would each group need to have if its PPV were equal to OVERALL's PPV? Equivalently: what is the price, in FPR-divergence, of imposing predictive parity?

| Identity | base rate $p$ | FNR | measured FPR | required FPR under PPV-equality | gap |
|---|---:|---:|---:|---:|---:|
| `male` | 0.1515 | 0.4625 | 0.0290 | 0.0437 | +0.0147 |
| `female` | 0.1345 | 0.5029 | 0.0147 | 0.0351 | +0.0204 |
| `homosexual_gay_or_lesbian` | 0.2862 | 0.5909 | 0.0417 | 0.0746 | +0.0329 |
| `christian` | 0.0996 | 0.5952 | 0.0121 | 0.0204 | +0.0083 |
| `jewish` | 0.1655 | 0.5588 | 0.0321 | 0.0398 | +0.0077 |
| `muslim` | 0.2211 | 0.5837 | 0.0353 | 0.0538 | +0.0185 |
| `black` | 0.3233 | 0.5407 | 0.0524 | 0.0998 | +0.0474 |
| `white` | 0.2997 | 0.5467 | 0.0473 | 0.0883 | +0.0410 |
| `psychiatric_or_mental_illness` | 0.2269 | 0.2963 | 0.0598 | 0.0940 | +0.0342 |

**Required FPR under predictive parity spans [0.0204 (christian), 0.0998 (black)]** -- a 4.9x ratio. Equalizing PPV at 0.6873 forces FPR to differ by a factor of 4.9 across groups.

## Step 3 — Counterfactual B: enforce error-rate balance at FPR = 0.0291

The mirror of Step 2: hold each group's base rate and FNR fixed, and ask what PPV each group would need if its FPR were equal to OVERALL's FPR.

| Identity | base rate $p$ | FNR | measured PPV | required PPV under FPR-equality | gap |
|---|---:|---:|---:|---:|---:|
| `male` | 0.1515 | 0.4625 | 0.7679 | 0.7673 | -0.0006 |
| `female` | 0.1345 | 0.5029 | 0.8406 | 0.7264 | -0.1142 |
| `homosexual_gay_or_lesbian` | 0.2862 | 0.5909 | 0.7975 | 0.8493 | +0.0518 |
| `christian` | 0.0996 | 0.5952 | 0.7870 | 0.6061 | -0.1809 |
| `jewish` | 0.1655 | 0.5588 | 0.7317 | 0.7504 | +0.0187 |
| `muslim` | 0.2211 | 0.5837 | 0.7698 | 0.8024 | +0.0326 |
| `black` | 0.3233 | 0.5407 | 0.8071 | 0.8829 | +0.0758 |
| `white` | 0.2997 | 0.5467 | 0.8040 | 0.8696 | +0.0656 |
| `psychiatric_or_mental_illness` | 0.2269 | 0.2963 | 0.7755 | 0.8765 | +0.1010 |

**Required PPV under error-rate balance spans [0.6061 (christian), 0.8829 (black)]** -- a 0.2768 absolute spread. Equalizing FPR at 0.0291 forces PPV to differ by 0.2768 in absolute terms across groups.

## Conclusion

Per-group base rates span [0.0996, 0.3233] (`christian` to `black`). With base-rate inequality of this magnitude, the Chouldechova identity makes predictive parity and error-rate balance algebraically incompatible. The system as deployed satisfies neither exactly: measured PPV ranges from 0.7317 to 0.8406, and measured FPR ranges from 0.0121 to 0.0598. The choice of which fairness metric the developers privileged is therefore implicit in their training objective and metric design (the competition's bias-aware metric is built on AUC-style measures, not on PPV-equality or FPR-equality), and is the kind of upstream value-laden choice the Pillar 4 critique calls out.
