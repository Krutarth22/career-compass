---
title: "End-to-End A/B Test Analysis and Recommendation"
track: "data-analyst"
difficulty_tier: "intermediate"
estimated_hours: 12
role: "core"
skill_tags: ["ab-testing", "statistics", "data-visualization"]
skill_prerequisites: ["statistics", "python"]
project_prerequisites: []
prerequisite_learning_hours: 10
---

# End-to-End A/B Test Analysis and Recommendation

## Production Workflow Mirrored
1. Define the hypothesis and success metric before looking at results
2. Check experiment health (sample ratio mismatch, randomization validity)
3. Run the appropriate significance test on the primary metric
4. Check guardrail metrics for unintended negative effects
5. Quantify the practical (not just statistical) significance of the result
6. Deliver a clear ship/no-ship recommendation with caveats

## What You'll Build
A complete analysis of an A/B test (using a public experiment dataset, e.g.
a website conversion test, an email subject-line test, or a simulated
pricing test you generate yourself with a known effect size) that goes from
raw event-level data to a written ship/no-ship recommendation, including
significance testing, confidence intervals, and guardrail-metric checks.

## Student-Scope Notes
- One experiment, one primary metric, a handful of guardrails — not a full
  experimentation platform with sequential testing or automatic stopping
  rules.
- If a public dataset with a real experiment isn't available, simulating
  data with a known true effect (and then checking whether your analysis
  recovers it) is an accepted and encouraged substitute — it's a legitimate
  way to sanity-check your own statistical pipeline.
- Frequentist hypothesis testing (t-test / z-test / chi-square as
  appropriate) is the required core; Bayesian A/B testing is optional and
  covered only as an extension.
- No experimental design/power-analysis tooling integration is required
  beyond a manual power calculation for the write-up.

## Steps
1. State the hypothesis explicitly before touching results data: what
   changed (the treatment), what metric it should move (primary metric),
   and in what direction, plus 1-2 guardrail metrics that should NOT get
   worse.
2. Do a power calculation: given a baseline conversion rate and minimum
   detectable effect, compute the required sample size, and compare it to
   what the dataset actually has.
3. Load the experiment data and check assignment health: are control/
   treatment group sizes close to the expected split (sample ratio
   mismatch check), and is there any sign of non-random assignment (e.g. by
   day of week or channel)?
4. Compute the primary metric for each arm (e.g. conversion rate, average
   order value) and run the appropriate test: two-proportion z-test/
   chi-square for a rate metric, or a t-test (checking variance/normality
   assumptions) for a continuous metric.
5. Report the result properly: p-value, effect size, and a confidence
   interval on the effect — not just "significant" or "not significant."
6. Check the guardrail metrics the same way, and flag any that moved in an
   unintended direction even if the primary metric looks good.
7. Segment the primary result by 1-2 relevant dimensions (e.g. new vs.
   returning users, device type) and check whether the effect is consistent
   or concentrated in one segment (Simpson's-paradox awareness).
8. Translate statistical significance into practical significance: given the
   effect size, what's the estimated business impact (e.g. revenue) if you
   ship this, with the confidence interval carried through.
9. Write the final recommendation memo: hypothesis, result, guardrail check,
   segment findings, and a clear ship/hold/kill call with the reasoning and
   caveats a skeptical stakeholder would want to see.

## Extension Ideas
- Add a Bayesian analysis alongside the frequentist one and compare how the
  recommendation would differ.
- Simulate a peeking/early-stopping scenario and show how it inflates false
  positive rate versus a fixed-horizon test.
- Add a novelty-effect check by looking at the treatment effect over the
  first days of the test versus later days.
- Build a small reusable script that takes any two-arm metric dataset and
  outputs the significance test + confidence interval automatically.

## Skills Demonstrated
- A/B test design and analysis, including experiment health checks
- Statistical hypothesis testing and confidence interval interpretation
- Guardrail-metric and segment-level thinking to avoid misleading headline
  results
- Data visualization of experiment results
- Turning a statistical result into a business recommendation
