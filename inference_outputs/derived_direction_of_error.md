# Direction of error per identity (Pillar 1)

Using the bias-AUC trio from cell029, each evaluated identity is classified as **over-flag** (BPSN < BNSP, model over-attributes toxicity to benign identity mentions), **under-flag** (BNSP < BPSN, model under-attributes toxicity to comments targeting the identity), or **balanced** (|BPSN - BNSP| <= 0.005).

| Identity | n | Subgroup AUC | BPSN AUC | BNSP AUC | BPSN - BNSP | Direction |
|---|---:|---:|---:|---:|---:|:---|
| `male` | 2112 | 0.9367 | 0.9621 | 0.9592 | +0.0029 | balanced |
| `female` | 2602 | 0.9418 | 0.9722 | 0.9515 | +0.0207 | under-flag |
| `homosexual_gay_or_lesbian` | 538 | 0.8541 | 0.9298 | 0.9504 | -0.0206 | over-flag |
| `christian` | 2109 | 0.9475 | 0.9761 | 0.9471 | +0.0290 | under-flag |
| `jewish` | 411 | 0.9098 | 0.9541 | 0.9518 | +0.0023 | balanced |
| `muslim` | 1054 | 0.8723 | 0.9424 | 0.9489 | -0.0065 | over-flag |
| `black` | 761 | 0.8670 | 0.9258 | 0.9573 | -0.0315 | over-flag |
| `white` | 1178 | 0.8738 | 0.9243 | 0.9593 | -0.0350 | over-flag |
| `psychiatric_or_mental_illness` | 238 | 0.9560 | 0.9514 | 0.9753 | -0.0239 | over-flag |

## Summary

- Over-flag (5): `white`, `black`, `psychiatric_or_mental_illness`, `homosexual_gay_or_lesbian`, `muslim`
- Under-flag (2): `christian`, `female`
- Balanced (2): `male`, `jewish`

The strongest over-flagging is on race mentions (`white`, `black`) and on `psychiatric_or_mental_illness`, with substantial over-flagging also on `homosexual_gay_or_lesbian` and `muslim`: the model treats these identity tokens as toxicity-adjacent regardless of context. The strongest under-flagging is on `christian` and `female`, where the model under-detects toxicity targeting the group. This split is the asymmetry the Pillar 0 stakeholder analysis must address: false positives (silencing of identity mentions) and false negatives (toleration of targeted toxicity) fall on disjoint identity groups, so a single fairness metric cannot remediate both directions simultaneously.
