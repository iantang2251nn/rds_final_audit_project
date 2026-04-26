# RDS Final Audit Project — Jigsaw Unintended Bias

**Ian Tang & Nick Chen | DS-UA 202 Spring 2026 | Group 21**

Audit of the 3rd-place solution to the Jigsaw Unintended Bias in Toxicity Classification Kaggle competition. Final deliverable due **2026-05-07**.

---

## Repo guide

### Top-level docs

| File | What it is |
|---|---|
| `next_steps.md` | The work plan. Pillars 0–5, owners, professor's must-do notes, sequencing. **Read this first.** |
| `project_instructions.pdf` | The assignment spec from the course. |
| `draft_report_and_slides_Ian_Nick.pdf` | Our existing draft (sections 1–3 mostly done; sections 4–5 are what we're building toward). |
| `research paper for reference.pdf` | Borkan et al. — the Jigsaw paper introducing Subgroup / BPSN / BNSP AUCs. |
| `report.tex` | Empty LaTeX skeleton — final report goes here. |

### Notebooks

| File | What it is |
|---|---|
| `3rd_place_recreation.ipynb` | Reproduces the 3rd-place ensemble (BERT-large-uncased + LSTM-GRU, Optuna-blended ≈ 99.3% BERT). This is what produced the trained models we audit. |
| `jigsaw_audit_analysis.ipynb` | **The main audit notebook.** All five technical pillars live here — see section map below. |

### Audit notebook section map (`jigsaw_audit_analysis.ipynb`)

| Section | Pillar | What it computes |
|---|---|---|
| 1–10 | setup | env, model loading, blend weights, ensemble inference on the private test set |
| 11 | **Pillar 1** | Per-identity Subgroup / BPSN / BNSP AUCs |
| 12 | **Pillar 3** | Module-1 fairness metrics (PPV, TPR, FPR, FNR, selection rate) at threshold s_HR + impossibility-result demo |
| 13 | **Pillar 3 viz** | Bias-AUC bar chart, score-distribution histograms, Module-1 grouped bars |
| 14 | **Pillar 2** | Counterfactual identity-perturbation experiments + GPT-2 perplexity validity check |
| 15 | **Pillar 4** | Sensitivity to power-mean exponent p and 25/75 weighting |

### Generated artifacts

| File | What it is |
|---|---|
| `inference_outputs/` | Every output from the audit notebook (figures, tables, stdout) extracted to flat files. Use these to drop into the report without re-running the notebook. |
| `inference_outputs.zip` | Same content, zipped. |
| `extract_outputs.py` | Script that produced the above. Re-run it if the notebook changes: `python3 extract_outputs.py`. |

### `inference_outputs/` naming convention

```
cell{NNN}_{first-line-slug}_{kind}.{ext}
```

- `NNN` = cell index in the notebook
- `kind` = `out00` / `out01` / ... for rich outputs, `stdout` / `stderr` for streams, `error` for tracebacks
- `ext` = `.png` (figures), `.html` (DataFrames), `.txt` (plain-text reprs / stdout), `.json` (widget metadata)

To find a specific result, look up the section in the map above, then grep filenames by cell number.

---

## What's done vs. what's left

**Technical (compute) — done.** Every "must-do" the professor flagged has a numerical artifact in `inference_outputs/`. See the cross-check table at the end of `next_steps.md`.

**Remaining work — all prose / LaTeX**, written into `report.tex`:
- Pillar 0 stakeholder map
- Pillar 2 must-dos #1, #2, #4 (TikZ DAG, causality framing, citations to Kusner / Garg / Bostock)
- Pillar 4 enumeration of the 9 evaluated identities vs. excluded columns
- Pillar 5 reflection (4 prompts)
- Limitations section (recreation scope, toxicity-label critique)

---

## Local-only (not in the repo)

`bullshit/` (3.6 GB) holds model weights and the original-solution reference code — gitignored. If you need it, ask Ian.
