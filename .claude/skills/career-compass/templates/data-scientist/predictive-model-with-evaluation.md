---
title: "Predictive Model with Rigorous Evaluation Harness"
track: "data-scientist"
difficulty_tier: "intermediate"
estimated_hours: 18
role: "core"
skill_tags: ["ml-fundamentals", "model-training", "model-evaluation", "python"]
skill_prerequisites: ["python", "statistics", "feature-engineering"]
project_prerequisites: []
prerequisite_learning_hours: 8
---

# Predictive Model with Rigorous Evaluation Harness

## Production Workflow Mirrored
1. Frame the prediction problem and choose a success metric tied to a
   real decision
2. Split data correctly (train/validation/test, respecting leakage and
   time where relevant)
3. Establish a naive baseline before touching a real model
4. Train multiple candidate models
5. Tune and cross-validate
6. Evaluate on held-out test data with multiple metrics, not one
7. Analyze errors and failure modes, not just aggregate scores
8. Document the model's limits so a downstream consumer knows when to
   trust it

## What You'll Build
A supervised classification or regression model (your choice of domain —
e.g. predicting loan default, house price, or customer churn) trained
through a disciplined evaluation harness: a documented baseline, k-fold
cross-validation, multiple candidate algorithms compared on multiple
metrics, and a held-out test-set report that includes error analysis, not
just a single accuracy number.

## Student-Scope Notes
- One dataset, one well-scoped prediction target — this is about depth of
  evaluation rigor, not breadth of modeling problems.
- Hyperparameter tuning uses a standard grid/random search over a bounded
  space, not a full AutoML sweep or distributed tuning job.
- No production serving here — the deliverable is a trained model artifact
  and a defensible evaluation report; serving it behind an API is a
  separate concern outside this track.

## Steps
1. Choose a supervised learning problem with a real, defensible target
   (classification: e.g. churn/fraud/default; regression: e.g. price/demand)
   and a dataset with at least a few thousand rows.
2. Pick a primary metric justified by the real-world cost of errors (e.g.
   recall over accuracy for fraud detection because false negatives are
   expensive) and write one paragraph justifying the choice before modeling.
3. Split the data into train/validation/test. If there's any time
   dimension, use a time-based split and explain why a random split would
   leak information.
4. Build a naive baseline (majority class, mean predictor, or a simple
   rule) and record its score on the chosen metric — every later model must
   beat this to be worth using.
5. Train at least 3 candidate models spanning different families (e.g.
   logistic/linear regression, a tree ensemble like random forest or
   gradient boosting, and one other) using consistent preprocessing.
6. Run k-fold cross-validation on the training set for each candidate;
   report mean and variance of the metric across folds, not just a single
   number.
7. Tune hyperparameters for your best 1-2 candidates via grid or random
   search, using cross-validation to select, never the test set.
8. Evaluate the final chosen model once on the held-out test set, reporting
   at least 3 metrics (e.g. for classification: precision, recall, F1,
   ROC-AUC; for regression: RMSE, MAE, R²).
9. Do error analysis: identify the segments or examples where the model is
   most wrong, check for systematic bias (does it underperform on a
   particular subgroup or value range?), and inspect a handful of the worst
   misses by hand.
10. Write an evaluation report: baseline vs. final model, metric results
    with cross-validation variance, error analysis findings, and an
    explicit statement of when/why this model should NOT be trusted.

## Extension Ideas
- Add calibration analysis (are predicted probabilities trustworthy?) for
  classification problems.
- Add a fairness/subgroup performance breakdown across a sensitive or
  business-relevant attribute.
- Compare cross-validation strategy choices (k-fold vs. stratified vs.
  time-series split) and show how the reported metric changes.
- Package the final model with a versioned artifact and a short model card.

## Skills Demonstrated
- End-to-end supervised model training across multiple algorithm families
- Rigorous evaluation methodology: baselines, cross-validation, multi-metric
  reporting
- Applied statistics for interpreting variance and significance in model
  comparisons
- Error analysis and honest reporting of model limitations
- Python fluency across a full scikit-learn-style modeling workflow

## Industry Relevance

Consumer Lending, Fraud Detection, Real Estate. A model predicting default, fraud, or price in these sectors is only as trustworthy as the evaluation behind it, and a team that skips a proper baseline, cross-validation, or subgroup error analysis risks shipping a model that looks strong on a single held-out number but fails badly for a specific customer segment or edge case. This project's rigorous baseline-to-final-model evaluation harness and honest documentation of the model's limits is the exact bar these industries hold a model to before it's allowed to influence a real financial or business decision.
