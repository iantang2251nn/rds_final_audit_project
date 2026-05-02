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
| `draft_report_and_slides_Ian_Nick.pdf` | March-12 poster-session draft. Superseded by the current `report.tex` / `report.pdf`. |
| `research paper for reference.pdf` | Borkan et al. — the Jigsaw paper introducing Subgroup / BPSN / BNSP AUCs. |
| `report.tex` | Final report source. §1–§7 prose complete; compiles to a 10-page PDF. |
| `references.bib` | BibTeX entries for the 11 citations used in `report.tex` (Borkan, Chouldechova, Hardt, Kusner, Garg, Bostock, Stoyanovich, Brown, Mitchell, Raji, sakami0000). |
| `report.pdf` | Compiled artifact. Rebuild with `tectonic report.tex`. |
| `COMMENTS.md` | Append-only review log. Dated, signed reviewer entries with verdicts on outstanding edits to `report.tex`. Consult before editing the report. |

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
| `inference_outputs/` | Every output from the audit notebook (figures, tables, stdout) extracted to flat files. Use these to drop into the report without re-running the notebook. Includes `derived_*.md` supplementary tables. |
| `inference_outputs.zip` | Same content, zipped. |
| `extract_outputs.py` | Script that produced the above. Re-run after notebook changes: `python3 extract_outputs.py`. Note: does **not** clear the directory before writing — `rm -rf inference_outputs/*` first to avoid stale artifacts. |
| `derived_analyses/` | Standalone Python scripts (`direction_of_error.py`, `identity_columns.py`, `impossibility_demo.py`) that produce the `inference_outputs/derived_*.md` supplementary tables referenced in `report.tex`. |

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

**Technical (compute) — done.** All Pillar 1–4 numerical artifacts live in `inference_outputs/`. Cross-check table at the end of `next_steps.md`.

**Report prose — done.** `report.tex` covers §1–§7 at exactly 10 pages. All 11 citations resolve via `references.bib`. Pillar 2 must-dos (TikZ anti-causal DAG, causality framing, Kusner / Garg / Bostock cites), Pillar 4 identity inclusion/exclusion enumeration, and Pillar 5 reflection prompts are in.

**Remaining work (in order):**

1. **Apply the `COMMENTS.md` edit set.** Codex's 14 items + 3 course-materials cross-check items + 3 conciseness wins. Net page-count change: −75 to −100 words. See `COMMENTS.md` for verdicts and rationale.
2. **Add Pillar 0 stakeholder table** and **standalone Limitations subsection**. Both fit inside 10 pages once the conciseness wins land.
3. **Recompile** with `tectonic report.tex`. Verify cites resolve, page count holds at 10, no `Empty 'thebibliography'` warning.
4. **Notebook + artifact hygiene** before submission:
   - `jupyter nbconvert --clear-output --inplace 3rd_place_recreation.ipynb` — strips the stale `UsageError` cell.
   - `rm -rf inference_outputs/* && python3 extract_outputs.py` — regenerates flat artifacts; verify the `cellNNN` pointers in `report.tex` still resolve.
5. **Slides + 5-minute video** (deliverables 4 & 5 per `project_instructions.pdf`). PDF slides + MP4 video, both required. Build after the report is locked.
6. **Bright Space submission.** Both partners upload identical PDF + Colab notebook + slides PDF + video.

---

## Local-only (not in the repo)

`bullshit/` (3.6 GB) holds model weights and the original-solution reference code — gitignored. If you need it, ask Ian.
