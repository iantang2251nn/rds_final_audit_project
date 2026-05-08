# 5-Minute Presentation Script

**Auditing the 3rd-Place Solution to the Jigsaw Unintended Bias in Toxicity Classification Competition**

*Ian Tang & Nick Chen — DS-UA 202, Spring 2026, Group 21*

Pace target: ~120–130 wpm conversational delivery. Each `## [time]` heading marks a slide-transition point. Total ~660 words.

---

## [0:00] Opening — the stakes

A toxicity classifier is a decision-support system. When it gets a comment wrong, the cost lands on a real person — a wrongful flag silences someone's voice in a public conversation; a missed slur leaves a targeted reader exposed to the harm the platform was meant to absorb. The question this audit asks is whose voice and whose dignity the deployed model treats equivalently across identity lines.

## [0:25] Audit framing

The competition ran on the Civil Comments corpus — about 1.8 million comments from a third-party news-site comment platform that shut down in 2017, released by Jigsaw with crowd-rated toxicity scores and identity annotations across twenty-four identity columns. Participants were asked to maximize toxicity-prediction quality while minimizing unintended bias against identity subgroups whose mention correlates with toxic content in the training data. This audit covers two objects: the third-place 2019 solution, and the metric that solution was trained against. The metric — the Subgroup/BPSN/BNSP power-mean — is itself a designed artifact. Jigsaw introduced it specifically to correct the identity–toxicity correlations the 2018 plain-AUC competition rewarded. The metric carries normative commitments of its own, and a model that passes it might still be passing the wrong test. So we audit both the model and the metric: this intersection is the crux of our project.

## [1:25] First arc — the asymmetry

Per-identity bias AUCs reveal something striking. Five identities are over-flagged: white, black, Muslim, queer, mental-health mentions. Two are under-flagged: Christian, female. The over-flagged set and the under-flagged set are disjoint.

That disjointness is the first major finding. False-positive harm — silencing commenters who mention their own identity — falls on one set of people. False-negative harm — letting toxicity targeting Christian and female communities stand — falls on a different set. You cannot optimize for both. A choice has to be made.

## [2:05] Second arc — the choice

Chouldechova's impossibility result, applied to our data: with unequal base rates, the system cannot simultaneously achieve predictive parity and error-rate balance. The confusion matrix at threshold 0.5 shows the consequence — FPR varies by a factor of five across the nine identities the metric evaluates.

The developers made a choice when they trained on the bias-aware metric. They simply did so implicitly, because the metric's defaults made the choice for them. Our audit privileges the commenter as the stakeholder of greatest concern: a wrongful flag silences with no in-platform recourse. Under that anchor, the implementation is unfair.

## [2:45] Counterfactual corroboration

To rule out a test-set artifact, we asked: if you take a comment and edit only the speaker's identity — say, "I am a lesbian" becomes "I am straight" — should the toxicity score change? When it does, the platform's enforcement is being driven by who is speaking, with the speech itself held constant. The biggest counterfactual gaps fall on the same identities the bias-AUC analysis flagged. Both methods point at the same identities.

## [3:20] Third arc — the metric itself

The competition metric rests on three constants. The power-mean exponent encodes a difference-principle-style commitment to the worst-off subgroup. The 25/75 fairness-utility weighting is heavily binding — sweeping it from zero to one moves the score by 0.04, substantially more than our recreation-vs-original gap. And the metric averages over 9 of the 24 identity columns the dataset annotates. The other 15 — transgender, bisexual, Asian, Latino, every disability category except mental-health — never enter the competition's score.

The groups most likely to suffer rare-but-severe harms are precisely the ones the metric cannot see. Operationally usable; normatively under-specified.

## [4:15] The verdict

Public-sector deployment: no. A government-deployed classifier that systematically removes more speech from commenters who mention their own race, sexual orientation, religion, or mental-health status would face speech-governance and disparate-impact challenges that the audit's evidence cannot defeat.

Industry deployment: only with guardrails — a public model card documenting the value choices, multi-threshold reporting, rater-pool auditing, and monitoring across all twenty-four identity columns the dataset annotates.

The bottom line: the system passes the metric the competition rewarded. The metric was always carrying normative commitments of its own, and the system's behavior under stakeholder-grounded fairness conditions favors one community at the expense of another. That trade-off lay hidden inside the metric's defaults. Our contribution is to surface it, so any participant choosing to deploy this approach has to choose deliberately, with each metric default surfaced and owned.
