---
title: "Web Performance Audit and Optimization"
track: "frontend-engineer"
difficulty_tier: "intermediate"
estimated_hours: 12
role: "core"
skill_tags: ["web-performance", "build-tooling", "browser-apis", "performance-profiling"]
skill_prerequisites: ["javascript", "frontend-frameworks"]
project_prerequisites: ["data-driven-dashboard-ui.md"]
prerequisite_learning_hours: 3
---

# Web Performance Audit and Optimization

## Production Workflow Mirrored
1. Measuring Core Web Vitals and bundle composition on a real build
2. Finding the largest contributors: oversized bundles, render-blocking
   assets, layout shifts, slow main-thread work
3. Applying targeted fixes: code splitting, lazy loading, image
   optimization, caching headers
4. Guarding against regression with a performance budget in CI
5. Reporting results in numbers a product manager can read

## What You'll Build
A performance audit and optimization pass on the dashboard from
`data-driven-dashboard-ui.md`, producing a before/after report of
Lighthouse scores, Core Web Vitals (LCP, INP, CLS), and bundle size, with
at least five concrete optimizations applied and a CI check that fails
the build if the bundle exceeds a budget.

## Student-Scope Notes
- Measure on a production build served over a local static server with
  throttling enabled in DevTools, not on the dev server.
- Optimizations are chosen from evidence in the bundle analyzer and the
  performance panel, not from a checklist.
- A CDN and real-user monitoring are out of scope; document what you
  would add.

## Steps
1. Produce a production build and record baseline Lighthouse scores,
   LCP/INP/CLS, total JS bytes, and a bundle analyzer treemap.
2. Identify the top three bundle contributors and the largest layout
   shift. Write down the hypothesis for each before changing anything.
3. Apply route-level and component-level code splitting so the initial
   bundle drops measurably. Re-measure.
4. Optimize images and fonts: modern formats, explicit dimensions to kill
   layout shift, font-display strategy, preloading the LCP asset.
5. Move any heavy synchronous work off the main thread (a web worker or
   deferred scheduling) and confirm INP improves.
6. Set cache headers on static assets with content hashing and verify
   repeat visits are served from cache.
7. Add a bundle-size budget check to CI that fails when the initial
   bundle grows past your threshold.
8. Write the report: a before/after table for every metric, one
   paragraph per optimization explaining the evidence and the effect, and
   what you would tackle next.

## Extension Ideas
- Add server-side rendering or static generation for the first paint and
  compare LCP.
- Add a service worker for offline shell caching.
- Add real-user monitoring with the web-vitals library reporting to a
  tiny endpoint.

## Skills Demonstrated
- Core Web Vitals measurement and interpretation
- Bundle analysis, code splitting, and asset optimization
- Main-thread performance profiling
- Performance budgets enforced in CI

## Industry Relevance

E-commerce, Media Publishing, Travel Booking. Conversion and search ranking in these sectors move measurably with load time, so frontend teams there treat performance as a product feature and ask candidates to walk through a real optimization with numbers. A before/after audit with evidence is the strongest possible answer.
