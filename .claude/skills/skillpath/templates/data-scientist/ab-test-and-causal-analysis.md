---
title: "A/B Test Design and Causal Analysis"
track: "data-scientist"
difficulty_tier: "intermediate"
estimated_hours: 15
role: "core"
skill_tags: ["ab-testing", "causal-inference", "statistics"]
skill_prerequisites: ["statistics", "python"]
project_prerequisites: []
prerequisite_learning_hours: 8
---

# A/B Test Design and Causal Analysis

## Production Workflow Mirrored
1. Frame a business question as a testable hypothesis
2. Design an experiment: unit of randomization, sample size, guardrail
   metrics
3. Simulate/collect experiment data and check for randomization validity
4. Analyze results with correct statistical tests and account for multiple
   comparisons
5. Recognize when a true randomized experiment isn't available or valid
6. Apply a causal-inference technique to estimate an effect from
   observational data
7. Communicate the causal claim honestly, including its assumptions and
   limits

## What You'll Build
Two linked analyses on a single business scenario (e.g. a pricing change,
a new checkout flow, or a product feature rollout): first a properly
designed and analyzed A/B test with power analysis and guardrail metrics,
then a companion causal-inference analysis (difference-in-differences or
propensity score matching) estimating the same kind of effect for a
realistic case where randomization wasn't possible — like a feature that
was rolled out to all users at once, or a policy that changed for one
region but not another.

## Student-Scope Notes
- Experiment data is simulated (with realistic effect sizes and noise) or
  drawn from a public experimentation dataset — you won't be running a live
  test against real users, but the design and analysis techniques are
  identical to production A/B testing.
- The causal-inference half tackles one technique in depth (diff-in-diff or
  propensity matching, your choice) rather than a survey of every causal
  method — depth over breadth.
- No experimentation platform/infrastructure is built here; the focus is
  the statistical design and analysis a data scientist owns, not the
  engineering that routes traffic into variants.

## Steps
1. Define a business question and hypothesis (e.g. "does a simplified
   checkout flow increase conversion rate?").
2. Design the A/B test: define the unit of randomization, primary metric,
   1-2 guardrail metrics (things that shouldn't get worse), and run a power
   analysis to determine required sample size for a chosen minimum
   detectable effect and significance level.
3. Simulate or source experiment data consistent with your design
   (control/treatment assignment, outcome per unit, some realistic noise
   and a modest true effect).
4. Run a sample-ratio mismatch check and basic randomization validity check
   (are control and treatment balanced on pre-experiment covariates?)
   before trusting any result.
5. Analyze the primary metric with the correct test for its type (t-test or
   Mann-Whitney for continuous, chi-square/z-test for proportions);
   analyze guardrail metrics too, and address multiple-comparison risk if
   you're checking several metrics.
6. Report the result: effect size, confidence interval, p-value, and a
   plain-language recommendation (ship, don't ship, or extend the test).
7. Now find or construct an observational scenario where a true experiment
   wasn't run (e.g. a feature launched to 100% of users at once, or a
   policy that changed in one market but not another) and state clearly why
   a naive before/after or treated/untreated comparison would be biased.
8. Apply your chosen causal technique: for diff-in-differences, identify
   treatment and control groups plus pre/post periods and check the
   parallel-trends assumption with a plot; for propensity score matching,
   estimate propensity scores from confounders, match treated to control
   units, and check covariate balance post-matching.
9. Estimate the causal effect and its uncertainty, and explicitly list the
   assumptions your estimate depends on and what would break it.
10. Write a combined report comparing the two analyses: what the RCT gave
    you that the observational method couldn't (or could only approximate),
    and how you'd explain the causal estimate's caveats to a
    non-technical stakeholder deciding on a rollout.

## Extension Ideas
- Add sequential testing / peeking-correction analysis to show why stopping
  an experiment early on a significant result is risky.
- Add a second causal method (e.g. instrumental variables or regression
  discontinuity) to the same scenario and compare estimates.
- Build a small power-analysis calculator others on your team could reuse.
- Add heterogeneous treatment effect analysis (does the effect differ by
  user segment?).

## Skills Demonstrated
- A/B test design: power analysis, guardrail metrics, randomization checks
- Correct statistical hypothesis testing and multiple-comparison awareness
- Causal inference on observational data (diff-in-diff or propensity
  matching)
- Honest communication of causal claims and their assumptions

## Industry Relevance

E-commerce Pricing, Product Growth, Public Policy Evaluation. Companies changing prices or rolling out new features can't always randomize — a policy might change region by region, or a feature might launch to everyone at once — so teams need both proper A/B test design when randomization is available and causal-inference techniques like diff-in-diff or propensity matching when it isn't. This project's pairing of the two builds exactly the judgment a data scientist needs to know which situation they're in and to avoid presenting a biased observational comparison as if it were a clean experimental result.
