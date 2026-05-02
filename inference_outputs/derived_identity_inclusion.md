# Identity column inclusion / exclusion in the metric (Pillar 4)

Source: `test_private_expanded.csv` (n = 97320; mention threshold = 0.5).

The Jigsaw competition's bias-aware metric evaluates **9 of the 24** identity columns collected in Civil Comments. The table below shows all 24 with sample counts at the 0.5 mention-threshold; the rightmost column flags whether the metric evaluates that identity.

## Gender

| Identity | n at threshold | Evaluated by metric |
|---|---:|:---:|
| `male` | 2112 | yes |
| `female` | 2602 | yes |
| `transgender` | 129 | no |
| `other_gender` | 0 | no |

## Sexual orientation

| Identity | n at threshold | Evaluated by metric |
|---|---:|:---:|
| `heterosexual` | 66 | no |
| `homosexual_gay_or_lesbian` | 538 | yes |
| `bisexual` | 21 | no |
| `other_sexual_orientation` | 1 | no |

## Religion

| Identity | n at threshold | Evaluated by metric |
|---|---:|:---:|
| `christian` | 2109 | yes |
| `jewish` | 411 | yes |
| `muslim` | 1054 | yes |
| `hindu` | 28 | no |
| `buddhist` | 27 | no |
| `atheist` | 149 | no |
| `other_religion` | 15 | no |

## Race / ethnicity

| Identity | n at threshold | Evaluated by metric |
|---|---:|:---:|
| `black` | 761 | yes |
| `white` | 1178 | yes |
| `asian` | 217 | no |
| `latino` | 121 | no |
| `other_race_or_ethnicity` | 16 | no |

## Disability

| Identity | n at threshold | Evaluated by metric |
|---|---:|:---:|
| `physical_disability` | 3 | no |
| `intellectual_or_learning_disability` | 14 | no |
| `psychiatric_or_mental_illness` | 238 | yes |
| `other_disability` | 0 | no |

## Summary

- Evaluated subgroups (9): 11003 total mentions at threshold 0.5.
- Excluded subgroups (15): 807 total mentions at threshold 0.5.
- All 9 evaluated subgroups have n >= 238 (smallest: `psychiatric_or_mental_illness`). All 15 excluded subgroups have n <= 217 (largest: `asian`). The selection therefore appears sample-size driven, with a cutoff falling between 217 and 238 mentions in the private test set.

Rendering this list visible matters for the Pillar 4 critique: the metric's identity selection is itself a normative choice. The rule "we evaluate where we have data" compounds the visibility problem of under-represented identities. Subgroups such as `transgender`, `bisexual`, `asian`, `latino`, `hindu`, `buddhist`, `atheist`, and every disability category other than `psychiatric_or_mental_illness` are present in the dataset and annotated, but their performance gaps do not enter the bias-aware score the competition rewarded. Identities most likely to suffer rare-but-severe harms are systematically the ones excluded by a sample-size-driven cutoff.
