# Implementation Plan & Requirement Traceability

This document is an implementation plan, not a claim that the system is complete.

## Core workflow

1. Ingest and validate historical hotel-bar transaction/inventory data.
2. Derive daily item-level consumption and preserve zero-demand days.
3. Engineer calendar, occupancy/event, location, SKU, and lag/rolling features when data supports them.
4. Build a forecasting baseline and candidate models; evaluate on time-aware holdouts.
5. Convert forecast demand into safety stock, reorder point, and dynamic par-level recommendations.
6. Account for lead time, service level, current inventory, pending/on-order quantities, MOQ, and cost parameters when available.
7. Run historical inventory simulation/backtesting.
8. Report stockouts, lost volume, service level, average inventory, excess inventory, turnover, and ordering performance.
9. Produce actionable procurement recommendations with traceable inputs.
10. Document assumptions, decisions, limitations, validation, and reproducibility.

## Capability references gathered from public repositories

- Bar optimization repository: modular preprocessing, forecasting, recommendation, and simulation separation.
- Bar inventory forecasting repository: item/bar-level demand, rolling statistics, par levels, and historical simulation.
- Hotel-bar forecasting repository: consumption derivation, short-horizon forecasting, reorder recommendations, and spreadsheet output.
- Hotel inventory forecasting repository: forecasting + optimization + simulation/dashboard concept.
- Inventory optimization repository: safety stock, EOQ, reorder point, order quantity, turnover, stockout/excess/dead-stock analysis, movement classification, urgency, days-to-stockout, lead-time and on-order analysis.
- Krystal Ball-specific repository: treated only as a project-similarity reference; no third-party implementation is copied.

## Assignment-first rule

The final implementation must be driven by the supplied assignment and its required deliverables. Public repositories are references for understanding possible patterns only, not source code or submission material.

## Validation rule

Do not label a capability complete until code/data/tests or documented analysis demonstrate it. Do not claim runtime validation when execution has not been performed.
