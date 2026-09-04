---
title: "Inventory Policy and Supply Chain Optimization"
track: "industrial-engineer"
difficulty_tier: "intermediate"
estimated_hours: 14
role: "core"
skill_tags: ["supply-chain-inventory", "operations-research", "python", "statistics", "data-visualization"]
skill_prerequisites: ["python", "statistics"]
project_prerequisites: []
prerequisite_learning_hours: 4
---

# Inventory Policy and Supply Chain Optimization

## Production Workflow Mirrored
1. Classifying items and forecasting demand
2. Setting inventory policies with service-level targets
3. Optimizing sourcing or distribution with a mathematical model
4. Simulating the policy against demand uncertainty
5. Reporting cost and service trade-offs to decision makers

## What You'll Build
An inventory and sourcing study on a real or public dataset (a small
business's stock, a club's supplies, or a public retail dataset): an
ABC classification, demand forecasts with error measurement, reorder
point and order quantity policies per class with safety stock for a
target service level, a linear or integer programming model for a
sourcing or distribution decision solved with an open-source solver, a
Monte Carlo simulation of the policies' service and cost, and a
recommendation with a cost-service trade-off curve.

## Student-Scope Notes
- Public datasets are acceptable if you treat them as a real business
  and state assumptions.
- Python with an optimization library and an open-source solver is
  sufficient.
- Report service level and cost together; never one without the other.

## Steps
1. Clean the data and classify items by value and volume; select the
   top items for detailed policy design.
2. Forecast demand with two methods and measure error on a holdout
   period; choose per item.
3. Compute order quantities and reorder points with safety stock from
   forecast error and lead time for a target service level.
4. Formulate the sourcing or distribution problem (supplier
   allocation, warehouse assignment) as an optimization model with
   real constraints, and solve it.
5. Simulate the inventory policies with demand and lead-time
   uncertainty over a year with replications; measure fill rate,
   stockouts, and cost.
6. Build the trade-off curve of cost versus service level across
   policy settings.
7. Run a sensitivity analysis on lead time and forecast error.
8. Write the report with classification, forecasts, policies, the
   optimization model and solution, simulation results, and a
   recommendation.

## Extension Ideas
- Add a multi-echelon model with a central and local stock.
- Add a vendor-managed inventory or consignment comparison.
- Build a dashboard that recomputes policies on new data.
- Model a supply disruption and a mitigation strategy.

## Skills Demonstrated
- Demand classification and forecasting with error measurement
- Inventory policy design for service targets
- Optimization modeling with a solver
- Simulation-based evaluation and trade-off communication

## Industry Relevance

Retail, Consumer Goods, Healthcare Supply, Manufacturing Supply Chains. Inventory and network decisions are where industrial engineers create measurable financial impact in these sectors, and analytical rigor is what hiring managers test for. A study combining forecasting, optimization, and simulation with a trade-off curve is a compelling work sample.
