# Final Audit — Next Steps

**Ian Tang & Nick Chen | Group No. 21 | DS-UA 202 Spring 2026**
**Final report + Colab + slides + 5-min video due 2026-05-07 (no late days)**

---

## 0. Central Framing (orient everything around this)

> **Normative understanding of fairness → criticism of technical implementation and ADS audit.**

Algorithmic fairness and justice is the **normative framework** under which the audit operates. Every technical result (subgroup AUCs, counterfactual gaps, metric critique) must be tied back to a normative claim about who is harmed, what kind of justice is being approximated, and where the implementation falls short of that ideal. Read the audit as: *Civil Comments + sakami0000's 3rd-place ensemble implicitly enacts a particular theory of fairness; we name that theory, test how well the system actually realizes it, and surface the value choices the developers left implicit.*

This framing is the spine of the report — Sections 4 (Outcomes) and 5 (Summary) should each open by re-anchoring to it.

---

## 1. Limitations to Surface Explicitly in the Report

These are not afterthoughts; the professor flagged them and they should appear in their own subsection of the report (not buried).

- **Recreation scope.** We re-implemented BERT-large-uncased + LSTM-GRU (Optuna-blended, ~99.3% BERT) instead of the full F.H.S.D.Y. ensemble. Logistic constraints (compute, time, GPT-2 fine-tuning cost) prevented a full reproduction. → Discuss the **fairness implication**: a single dominant model can encode a single bias profile; ensembles with structural diversity may attenuate or amplify specific biases. We can only speculate about what the missing models would have changed.
- **Toxicity-score definition itself.** The Civil Comments label is the *fraction of human raters who labeled the comment toxic.* This is a measurement choice — it conflates rater subjectivity, rater demographics, and an implicit majoritarian threshold. → Flag whether this definition is itself an upstream fairness problem (whose toxicity? rated by whom?) and how it propagates to every downstream metric we compute.

---

## 2. Work Plan (analytical pillars)

Each pillar lists: owner, deliverable, professor's must-do notes (where given), and the course concept it connects to. Treat the professor's notes as non-negotiable execution requirements.

### Pillar 0 — Stakeholder Analysis *(owner: TBD)*

**Deliverable:** A short table/diagram in the report identifying:
- Who are the stakeholders of the ADS? (commenters, moderators, platform operators, identity-group members)
- Who wants to see what outcome? (false-positive vs. false-negative cost varies by stakeholder)
- Who gets hurt by errors, and which errors?
- Who benefits from the system being deployed?

**Why it matters:** The fairness metric you choose is a stakeholder choice. Predictive parity favors one stakeholder, error-rate balance favors another. The stakeholder map is the bridge between the normative framing (§0) and the metric critique (Pillar 4).

---

### Pillar 1 — Subgroup Fairness Analysis *(owner: Ian)*

**Deliverable:** Per-identity disaggregation of model performance across the 9 evaluated identity subgroups, using the duo-model predictions we already have.

- Per-identity **Subgroup AUC**, **BPSN AUC** (Background Positive, Subgroup Negative), and **BNSP AUC** (Background Negative, Subgroup Positive)
- Identify which subgroups experience the largest performance gaps and characterize the gap direction (over- vs. under-flagging)
- Tie the gaps back to data-side imbalances surfaced in §2 of the draft (input profiling)

**Connects to:** Standard subgroup-AUC framework introduced by Borkan et al. (Jigsaw paper), Mitchell et al. model-card style of per-subgroup reporting.

---

### Pillar 2 — Counterfactual Testing *(owner: Ian)*

**Deliverable:** Execute the design in `kaggle_jigsaw/counterfactual_framework_outline.md` — template sentences with swapped identity tokens, run through all 7 multi-task heads (toxicity + 6 subtype heads). Produce: template×identity heatmaps, identity marginal effects, pairwise identity gap matrix, BERT vs. LSTM vs. blend comparison.

**Professor's must-do notes — execute all four:**

1. **Build the DAG explicitly**, including the **anti-causal structure**. In toxicity classification the text causes the label (text → human-rater toxicity judgment), so the standard "features cause outcome" causal direction is reversed. Identity mention is a *node in the text*, not a separate confounder, which complicates the "intervene on $A$" step. State this clearly in the report.
2. **Conceptualize causality** for this domain. What does it mean to "intervene" on identity in a sentence? We are implicitly assuming the template-substitution operation is a valid do-intervention on the identity attribute — surface that assumption.
3. **Test the causality assumption.** Empirically check whether template substitution preserves sentence meaning (e.g., "I am a Muslim" vs. "I am a Christian" — does grammar/coherence hold? Are there identity terms where the substitution breaks fluency and confounds the score difference?). Report substitutions where the assumption fails.
4. **Reference text counterfactual fairness literature.** The Kusner et al. (2017) framework in Appendix A is the foundation; also cite text-specific counterfactual fairness work (e.g., Garg et al. on counterfactual token fairness) so the methodology is grounded, not improvised.

**Connects to:** Counterfactual demographic parity (Appendix A), Bostock v. Clayton County "but-for" causation framing, Lecture 8.

---

### Pillar 3 — Visualization of Bias Patterns *(owner: Nick)*

**Deliverable:**
- Grouped bar chart of the three bias AUCs (Subgroup / BPSN / BNSP) per identity
- Score-distribution histograms per subgroup (overlay positive vs. negative class within each subgroup)
- Highlight systematic differences in model behavior across subgroups
- Most plotting code already written — focus on labeling, legends, and embedding-ready figures (PDF export for LaTeX)

**Professor's must-do note (mandatory, "this is a must"):**

> **Utilize and analyze the Module 1 fairness metrics** (Appendix B) in the report.

Concretely: choose at least one operating threshold $s_{HR}$ on the toxicity score (justify the choice — e.g., the threshold a deployed moderator might use), then compute per-subgroup confusion matrices and report at minimum:

- **Calibration / Predictive parity** — PPV across subgroups
- **Error rate balance** — FPR and FNR across subgroups
- **Statistical parity** — selection rate across subgroups
- **Equalized odds / Equal opportunity** — TPR (and FPR jointly) across subgroups

Then explicitly invoke the **impossibility result** (Chouldechova): with differing base rates across identity subgroups in Civil Comments, the system *cannot* simultaneously satisfy predictive parity and error-rate balance unless it is perfect. Use this to argue that the developers made an implicit choice about *which* fairness metric to optimize.

**Connects to:** Module 1, Lectures 2–3, Chouldechova reading.

---

### Pillar 4 — Critique of the Kaggle Competition Metric *(owner: Ian)*

**Deliverable:** A standalone subsection that interrogates the design of the competition's bias-aware metric — the implicit normative claims it makes.

- **Power mean with $p = -5$.** Heavy emphasis on the *worst-performing* subgroup. Argue this is an implicit **Rawlsian "worst-off welfare" principle**: the metric maximizes the minimum subgroup performance. Note that this normative choice was made by the Jigsaw competition designers but **not stated as such** — the metric design itself encodes a theory of justice that participants inherited unexamined.
- **25/75 weighting** between Overall AUC and the bias metrics. Why this split? What does it signal about the competition's relative weighting of utility vs. fairness?
- **Identity column inclusion/exclusion decisions.** Which 9 identities were chosen for evaluation, and which were collected but excluded? Whose harm is rendered visible vs. invisible?
- **Meta-point:** *Metric design itself can be looked at carefully — what metric design produces what kind of outcome that impacts fairness?* The choice of fairness metric is an upstream act of value-laden design, not a neutral technical step.

**Connects to:** Course readings on metric design (Brown et al. "The algorithm audit," Stoyanovich & Howe "Nutritional labels for data and models"), Rawls' difference principle.

---

### Pillar 5 — Reflection & Synthesis *(owner: both)*

**Deliverable:** Section 5 of the report, addressing the four required reflection prompts from the assignment spec, but threading the §0 framing throughout:

a. **Was the data appropriate?** Tie back to the toxicity-score definition critique (§1) and stakeholder analysis (Pillar 0).
b. **Is the implementation robust, accurate, and fair?** Synthesize Pillars 1–3. Be explicit about which fairness metric you privilege and why, and which stakeholder that choice serves.
c. **Would you deploy this in public sector / industry?** Distinguish — the answer may differ. Invoke the metric critique (Pillar 4) to argue what additional governance would be needed.
d. **Recommendations** for data collection, processing, methodology. Concrete, not vague.

---

## 3. Suggested Sequencing (with ~12 days to deadline)

Rough cadence to keep both partners unblocked:

1. **Days 1–3:** Pillars 1 + 3 in parallel (Ian computes per-identity AUCs; Nick builds plots from existing predictions). Stakeholder analysis (Pillar 0) drafted in parallel — short, can be done alongside.
2. **Days 4–7:** Pillar 2 counterfactual experiments (most novel, most time-uncertain — protect this budget). Pillar 3 Module-1 metrics computed once Pillar 1 confusion matrices exist.
3. **Days 7–9:** Pillar 4 metric critique written (mostly prose + math, no new compute). Limitations section drafted.
4. **Days 9–11:** Pillar 5 synthesis. Final report assembly in LaTeX.
5. **Days 11–12:** Slides + 5-min video. Buffer for the no-late-day rule.

---

## Appendix A — Counterfactual Fairness Framework

**Core question** (Lecture 8): *"What would have happened if your <race, ethnicity, gender, disability, …> had been different?"* This is framed as the "dominant paradigm for fairness + recourse analysis."

### Formal definition (counterfactual demographic parity)

From Causality_ML_chapter (Kusner et al. 2017, introduced as *counterfactual fairness*):

Setup: features $X$, sensitive attribute $A$, outcome $Y$, predictor $\hat{Y}$.

> "For every possible demographic described by the event $E := \{X := x, A := a\}$ and every possible setting $a'$ of $A$ we ask that the counterfactual $\hat{Y}_{A:=a}(E)$ and the counterfactual $\hat{Y}_{A:=a'}(E)$ follow the same distribution."

The textbook calls this *counterfactual demographic parity* because it is the causal analog of conditional demographic parity ($\hat{Y} \perp A \mid X$).

### How counterfactuals are computed

Counterfactuals are defined inside a structural causal model (SCM) via a three-step procedure (Causality_ML_chapter, Definition 2):

1. **Abduction** — condition the joint distribution of exogenous noise $U$ on the observed event $E$ to get a biased $U'$.
2. **Action** — perform the do-intervention $X := x$ in $M$, yielding $M' = M[X:=x]$.
3. **Prediction** — compute the target $Y_{X:=x}(E)$ using $U'$ as the random seed in $M'$.

Note: "Answers to counterfactual questions strongly depend on the specifics of the structural causal model" — two SCMs with identical graphs and identical interventional behavior can give different counterfactual answers.

### Easiest way to satisfy it

Causality_ML_chapter: *"The easiest way to satisfy counterfactual demographic parity is for the predictor $\hat{Y}$ to only use non-descendants of $A$ in the causal graph."* This is the causal analog of using only features statistically independent of $A$.

### Legal grounding (Lecture 8)

The framework aligns with the "but-for causation" standard articulated in *Bostock v. Clayton County* (2020):

> "what would have happened if the plaintiff had been White? This focus fits naturally with the ordinary rule that a plaintiff must prove but-for causation."

> "a but-for test directs us to change one thing at a time and see if the outcome changes."

### Bank loan illustration (Lecture 8)

Predictor $\hat{Y} = A \lor (X > \tau)$: eligible if in group $A=1$ OR if qualification $X$ exceeds threshold $\tau$.

- **Traditional counterfactual fairness perspective:** a person in $A=0$ with $X > \tau$ gets the same prediction in the counterfactual where $A^* = 1$ → judged **fair for this individual**.
- **Backtracking counterfactual perspective:** the person in $A=0$ had to clear $X > \tau$, which group $A=1$ did not need to clear → judged **unfair**.

This contrast shows the traditional framework can miss differential opportunity/effort that the backtracking variant catches.

### Important caveat

Causality_ML_chapter:

> "Just because a causal variant of a criterion might get around some statistical issues of non-causal correlations does not mean that the causal criterion resolves normative concerns or questions with its observational cousin."

Causal fairness exposes and quantifies the questions but does not eliminate the normative judgments (e.g., which paths from $A$ to $\hat{Y}$ count as discrimination).

---

## Appendix B — Module 1 Fairness Metrics

From Module 1 (Chouldechova reading + Lectures 2–3), all stated as constraints on the **confusion matrix** (TN, FP, FN, TP).

### 1. Calibration (Definition 1)

A score $S$ is well-calibrated if, for each score value $s$:

$$P(Y = 1 \mid S = s, R = b) = P(Y = 1 \mid S = s, R = w)$$

Lecture 2/3: *"A risk assessment tool is calibrated if the predicted risks match actual observed outcomes."*

### 2. Predictive parity (Definition 2)

Equal **positive predictive value (PPV = TP/(TP+FP))** across groups, at threshold $s_{HR}$:

$$P(Y = 1 \mid S > s_{HR}, R = b) = P(Y = 1 \mid S > s_{HR}, R = w)$$

Lecture 3: *"A risk assessment tool exhibits predictive parity if, for a given risk score, the probability of the positive outcome is independent of group membership."* Also called group calibration.

### 3. Error rate balance (Definition 3)

Equal **FPR** and **FNR** across groups at threshold $s_{HR}$:

$$P(S > s_{HR} \mid Y = 0, R = b) = P(S > s_{HR} \mid Y = 0, R = w) \quad (\text{FPR})$$
$$P(S \leq s_{HR} \mid Y = 1, R = b) = P(S \leq s_{HR} \mid Y = 1, R = w) \quad (\text{FNR})$$

where $\text{FPR} = FP/(FP+TN)$ and $\text{FNR} = FN/(FN+TP)$.

Chouldechova: *"Error rate balance is also closely connected to the notions of equalized odds and equal opportunity as introduced in the recent work of Hardt et al."*

### 4. Statistical parity (Definition 4)

Equal **selection rate** (= (TP+FP)/N) across groups:

$$P(S > s_{HR} \mid R = b) = P(S > s_{HR} \mid R = w)$$

*"Also goes by the name of equal acceptance rates or group fairness."* Also called demographic parity. The reading notes it is "difficult to motivate in the recidivism prediction setting."

### 5. Balance for the positive / negative class (Kleinberg et al.)

Mentioned in Section 2.2: *"the average score assigned to non-recidivists (the negative class) should be the same for both groups, and that the same should hold among recidivists (the positive class)."* (Score-based, but tied to the same TN/FP and FN/TP partitions.)

### Key relationship from the confusion matrix

$$\text{FPR} = \frac{p}{1-p}\cdot\frac{1-\text{PPV}}{\text{PPV}}\,(1 - \text{FNR})$$

where $p$ is prevalence, leading to the **impossibility result** (Lecture 2/3):

> "If a risk assessment tool satisfies predictive parity ... and the base rates ... differ between groups, then the tool cannot achieve both equal false positive rates across groups, and equal false negative rates across groups, unless the tool has perfect accuracy."

### Summary table (confusion-matrix link)

| Metric | Confusion-matrix quantity equalized across groups |
|---|---|
| Calibration / Predictive parity | PPV = TP/(TP+FP) |
| Error rate balance — FPR | FP/(FP+TN) |
| Error rate balance — FNR | FN/(FN+TP) |
| Statistical parity | (TP+FP)/N |
| Equalized odds (Hardt et al.) | FPR and TPR jointly |
| Equal opportunity (Hardt et al.) | TPR = TP/(TP+FN) only |

Note: The lecture/reading frames calibration in terms of the score $S$ rather than the binarized confusion matrix; only after thresholding at $s_{HR}$ do calibration's implications collapse onto PPV (predictive parity).
