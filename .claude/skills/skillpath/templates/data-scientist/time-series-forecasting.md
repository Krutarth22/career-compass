---
title: "Time-Series Forecasting with Backtesting"
track: "data-scientist"
difficulty_tier: "intermediate"
estimated_hours: 16
role: "core"
skill_tags: ["statistics", "model-training", "python"]
skill_prerequisites: ["statistics", "python"]
project_prerequisites: []
prerequisite_learning_hours: 8
---

# Time-Series Forecasting with Backtesting

## Production Workflow Mirrored
1. Frame a business metric as a forecasting problem with a defined horizon
2. Explore the series: trend, seasonality, stationarity, anomalies
3. Build a naive baseline forecast
4. Train one or more forecasting models
5. Backtest using rolling-origin evaluation, not a single train/test split
6. Evaluate with forecasting-appropriate metrics
7. Communicate the forecast with honest uncertainty bounds

## What You'll Build
A forecasting model for a real business-style metric with a clear horizon
(for example, daily retail demand, weekly website traffic, or monthly
subscription revenue), evaluated through proper time-series backtesting
rather than a single held-out split, with a forecast report that includes
uncertainty intervals and a comparison against a naive baseline.

## Student-Scope Notes
- One series (or a small, related family of series, e.g. demand per store
  for a handful of stores) — this is about forecasting method and
  evaluation rigor, not building a forecasting platform for thousands of
  series at once.
- Models used are standard, well-understood approaches (e.g. seasonal
  naive, ETS/Holt-Winters, ARIMA/SARIMA, or a gradient-boosted model with
  lag features) rather than deep-learning forecasting architectures.
- Backtesting uses a manageable number of rolling windows (5-10), not an
  exhaustive walk-forward over every possible origin — enough to show the
  method and get a stable estimate of forecast error.

## Steps
1. Choose a time series with genuine seasonality and trend (daily, weekly,
   or monthly granularity) and a business-relevant forecast horizon (e.g.
   forecast the next 30 days of demand).
2. Explore the series: plot it, decompose into trend/seasonal/residual
   components, run a stationarity test (e.g. ADF), and note any
   structural breaks, holidays, or anomalies that need special handling.
3. Build a naive baseline forecast (seasonal naive: "this week looks like
   last week") and record its error — this is the bar every real model
   must clear.
4. Build at least one classical statistical model (e.g. Holt-Winters or
   SARIMA) with parameters chosen via the series' observed seasonality, and
   at least one ML-style model using engineered lag/rolling/calendar
   features (e.g. gradient boosting on lag features).
5. Set up rolling-origin backtesting: repeatedly move the train/test cutoff
   forward in time, refit or update the model, and forecast the next
   horizon window, for at least 5 separate origins.
6. Evaluate each model with forecasting-appropriate metrics (MAPE or sMAPE,
   MAE, RMSE) averaged across all backtest windows, and compare against the
   naive baseline at every window, not just on average.
7. Generate uncertainty intervals for your best model's forecast (e.g. from
   the statistical model's native intervals, or via residual-based
   quantile estimation for the ML model) and check empirically how often
   the true value actually fell inside the interval during backtesting.
8. Investigate the windows where the model performed worst (e.g. around a
   holiday or demand spike) and note what caused the miss.
9. Produce a final forecast for the true future horizon with plotted
   uncertainty bands, and write up: baseline vs. model performance across
   backtest windows, where the model is reliable vs. shaky, and a
   recommendation on how much to trust the forecast for planning purposes.

## Extension Ideas
- Add exogenous regressors (e.g. promotions, weather, holidays) to the
  feature-based model and measure the accuracy lift.
- Forecast multiple related series at once and compare a per-series
  approach against a pooled/global model.
- Add a simple anomaly-detection pass flagging when actuals diverge sharply
  from the forecast interval, as you'd want for a monitoring alert.
- Compare classical vs. ML-based forecasting formally with a
  statistical significance test on the backtest errors.

## Skills Demonstrated
- Time-series statistics: decomposition, stationarity, seasonality
- Forecasting model training across classical and ML-based approaches
- Rigorous backtesting methodology for time-dependent data
- Python fluency for time-series manipulation and forecasting libraries
- Honest uncertainty communication in a forecast deliverable

## Industry Relevance

Retail Demand Planning, Energy & Utilities, SaaS Revenue Forecasting. Businesses in these sectors make concrete operational commitments — inventory orders, staffing levels, revenue guidance — off a forecast, and a forecast without honest uncertainty bounds or proper backtesting can lead to costly over- or under-provisioning when reality diverges from the point estimate. This project's rolling-origin backtesting against a naive baseline, with uncertainty intervals validated against actual outcomes, mirrors the rigor these industries require before a forecast is trusted enough to drive a purchasing or staffing decision.
