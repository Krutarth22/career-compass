---
title: "Exploratory Data Analysis Report on a Messy Real-World Dataset"
track: "data-analyst"
difficulty_tier: "beginner"
estimated_hours: 12
role: "core"
skill_tags: ["data-cleaning", "statistics", "python", "data-visualization"]
skill_prerequisites: ["python", "statistics"]
project_prerequisites: []
prerequisite_learning_hours: 8
---

# Exploratory Data Analysis Report on a Messy Real-World Dataset

## Production Workflow Mirrored
1. Receive a raw, unvetted dataset with no documentation
2. Profile the data (types, missingness, ranges, duplicates, outliers)
3. Clean and standardize (missing values, inconsistent categories, type coercion)
4. Explore distributions and relationships between variables
5. Formulate and test a handful of concrete questions about the data
6. Produce a written report with visuals aimed at a non-technical stakeholder

## What You'll Build
A written exploratory data analysis (EDA) report — code notebook plus a
polished summary document — on a real, messy public dataset (e.g. a city's
311 service requests, a restaurant health inspection dataset, or an airline
on-time performance extract). The report documents your cleaning decisions,
shows the key distributions and relationships you found, and answers 4-5
specific questions a stakeholder would actually ask about the data.

## Student-Scope Notes
- One dataset, one analyst, one sitting — not a recurring pipeline that has
  to handle new data drops every week (that reproducibility problem shows up
  in the SQL and BI projects).
- "Messy" here means realistic messiness you can fix by hand with pandas
  (inconsistent capitalization, mixed date formats, a column that's 30%
  null, a few obvious data-entry typos) — not adversarial or multi-source
  data reconciliation.
- No formal hypothesis testing framework is required here (that's the
  A/B-test template); this is about description and honest exploration, not
  inference.
- The report is static (a notebook + a PDF/Markdown write-up), not an
  interactive dashboard — that's a separate skill covered elsewhere.

## Steps
1. Pick a real, publicly available dataset with at least 5,000 rows and
   visible messiness (a government open-data portal is a good source).
   Avoid a dataset that's already been cleaned for tutorials.
2. Load it and write a profiling pass: row/column counts, dtypes, % missing
   per column, number of duplicate rows, cardinality of categorical columns.
3. Write down, in plain language, every cleaning decision you make and why
   (e.g. "dropped rows missing `zip_code` because it's <1% of rows and not
   imputable"; "standardized `borough` values because the same borough
   appears under 4 different spellings").
4. Handle missing data deliberately per column: drop, impute (mean/median/
   mode, or a flagged "unknown" category), or leave as a signal — never
   silently fill everything with one strategy.
5. Detect and handle outliers: use IQR or z-score to flag them, then decide
   per case whether they're data errors or legitimate extreme values, and
   say which.
6. Compute summary statistics (mean, median, std, quartiles) for key numeric
   columns and frequency tables for key categorical columns.
7. Build 6-10 visualizations: distributions (histograms/boxplots), a
   correlation matrix or pairwise relationships for numeric columns, and at
   least 2 categorical breakdowns (e.g. bar charts by category, over time).
8. Formulate 4-5 specific questions a real stakeholder would ask about this
   dataset (e.g. "which neighborhoods have the slowest response times?")
   and answer each one directly, backed by a chart or table.
9. Write the final report: dataset background, cleaning log, key findings
   (each with a chart), and 2-3 limitations/caveats a reader should know
   before trusting your conclusions.

## Extension Ideas
- Automate the profiling step into a reusable function/report generator you
  can point at any new CSV.
- Add a simple anomaly-flagging rule set and quantify how many rows it
  would catch on a fresh extract of the same dataset.
- Compare two cleaning strategies (e.g. drop vs. impute missing values) and
  show how much your headline findings change.

## Skills Demonstrated
- Data cleaning and preprocessing on real, messy data
- Descriptive statistics and outlier handling
- Exploratory data visualization
- Translating a raw dataset into a stakeholder-readable narrative
