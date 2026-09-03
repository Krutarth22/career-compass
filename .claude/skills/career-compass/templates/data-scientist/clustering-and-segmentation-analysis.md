---
title: "Clustering and Customer Segmentation Analysis"
track: "data-scientist"
difficulty_tier: "intermediate"
estimated_hours: 14
role: "core"
skill_tags: ["ml-fundamentals", "feature-engineering", "data-visualization"]
skill_prerequisites: ["python", "statistics", "feature-engineering"]
project_prerequisites: []
prerequisite_learning_hours: 7
---

# Clustering and Customer Segmentation Analysis

## Production Workflow Mirrored
1. Frame a business question that segmentation would answer
2. Select and engineer features that represent behavior, not just raw
   attributes
3. Choose and justify a clustering algorithm and distance/scaling approach
4. Determine the number of segments using multiple validation approaches
5. Profile each segment in business terms
6. Validate segment stability
7. Translate segments into an actionable business recommendation

## What You'll Build
An unsupervised segmentation of users or customers (e.g. retail shoppers,
subscription-service users, or app users) into a small number of
meaningful behavioral segments, complete with feature engineering from raw
transaction/event data, a justified choice of cluster count, rich profiles
of each segment, and a business write-up recommending how each segment
should be treated differently.

## Student-Scope Notes
- One dataset, one clustering pass done well — the goal is depth in
  choosing k, validating clusters, and profiling them meaningfully, not
  surveying every clustering algorithm that exists.
- "Business action" is a recommendation you write and justify, not an
  actual marketing campaign or product change — the analytical rigor
  behind the recommendation is what's being assessed.
- Stability validation uses a straightforward resampling check (e.g.
  bootstrap or train/test cluster agreement), not a full theoretical
  cluster-validity study.

## Steps
1. Choose a dataset of individual-level behavior (e.g. e-commerce
   transaction history, streaming-service usage logs, or telecom usage
   records) with enough signal to support meaningful behavioral
   differences between users.
2. Engineer features that describe behavior rather than raw IDs: recency,
   frequency, monetary value (RFM-style), engagement ratios, category
   preferences, tenure, or usage trend — aim for 8-15 candidate features.
3. Scale/transform features appropriately (e.g. log-transform skewed
   monetary features, standardize before distance-based clustering) and
   check for and handle strongly correlated features that would bias
   distance calculations.
4. Choose a clustering algorithm (e.g. k-means as your primary method,
   optionally compare against hierarchical or DBSCAN) and justify the
   choice given your data's shape (cluster sizes, density, presence of
   outliers).
5. Determine the number of clusters using at least two independent methods
   (e.g. elbow method on inertia, silhouette score, gap statistic) and
   reconcile them if they disagree rather than picking whichever is
   convenient.
6. Fit the final clustering and reduce dimensionality (e.g. PCA or t-SNE)
   to visualize how well-separated the segments actually are.
7. Profile each segment: for every cluster, report the distinguishing
   feature values (mean/median vs. overall population), segment size, and
   a descriptive name (e.g. "high-frequency low-spend browsers").
8. Validate stability: re-run clustering on a bootstrap resample or a
   random subset and check how consistently the same segments emerge (e.g.
   via adjusted Rand index between runs).
9. Write a business report: what each segment represents, how they differ
   in ways that matter for a real decision (e.g. retention risk, upsell
   potential), and a specific recommended action per segment.

## Extension Ideas
- Track segment membership over time and analyze migration between
  segments as a churn/growth signal.
- Compare k-means results against a model-based clustering approach
  (e.g. Gaussian mixture models) and discuss when soft cluster assignment
  matters.
- Build a lightweight scoring function that assigns new/incoming users to
  an existing segment without a full re-cluster.
- Layer in the explainability techniques from the model-explainability
  project to explain what drives assignment to each segment.

## Skills Demonstrated
- Unsupervised machine learning: clustering algorithm selection and tuning
- Feature engineering for behavioral/RFM-style analysis
- Data visualization for dimensionality reduction and segment profiling
- Business-oriented translation of an unsupervised result into
  recommendations

## Industry Relevance

Retail, Streaming Media, Telecommunications. Companies with large user bases in these sectors use behavioral segmentation to decide who gets a retention offer, which content gets recommended, or which usage pattern signals churn risk, and a poorly justified cluster count or unstable segmentation leads directly to misdirected marketing spend. This project's rigor around choosing k with multiple validation methods and checking segment stability mirrors what separates a segmentation a business can act on from one that looks plausible but falls apart on the next data refresh.
