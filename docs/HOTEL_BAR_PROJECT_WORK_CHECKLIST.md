# Hotel Bar Inventory Intelligence — Personal Work Checklist

> Personal working checklist for implementation and verification. Keep this file updated as work progresses.
> This is a working tracker, not a substitute for the assignment's required documentation.

## Execution Order
Foundation 1–5 → 6 Forecasting → 7 Walk-Forward Backtesting → 8 Final 7-Day Forecast → 9 Dynamic PAR → 10 Safety Stock → 11 Simulation → 12 Calibration → 13 Recommendations → 15 Testing → 14 Architecture → 16 Documentation → 17 Final Submission

## 1. Data Understanding, Cleaning & Validation
- [x] Inspect raw schema
- [x] Confirm 6,575 transaction rows
- [x] Confirm 2023-01-01 to 2024-01-01 date range
- [x] Confirm 6 bars, 16 brands, 5 alcohol types, 96 series
- [x] Check missing values, duplicates, negatives
- [x] Check inventory conservation
- [x] Check timestamp consistency
- [x] Check Bar + Brand → Alcohol Type consistency
- [x] Check inventory continuity
- [x] Reconcile transaction and daily consumption
- [x] Preserve zero-demand days

## 2. Problem Understanding & Requirements
- [x] Business problem
- [x] Scope
- [x] Assumptions
- [x] Success metrics
- [x] Data/model questions
- [x] Limitations

## 3. EDA / Demand Analysis
- [x] Overall demand
- [x] Bar-level analysis
- [x] Brand-level analysis
- [x] Alcohol-type analysis
- [x] Weekday/hourly/monthly analysis
- [x] Demand sparsity
- [x] Variability
- [x] Dense/sparse series

## 4. Demand Segmentation & ABC
- [x] Annual series consumption
- [x] ABC classification
- [x] ADI
- [x] CV²
- [x] Intermittent-demand classification
- [x] High-volume/sparse series identification

## 5. Daily Demand Dataset / Features
- [x] Full daily panel
- [x] 96 × 366 = 35,136 observations
- [x] Zero-demand days
- [x] Raw/daily reconciliation
- [x] Calendar features
- [x] Lag features
- [x] Leakage-safe rolling features
- [x] Demand-frequency features
- [x] ABC class
- [x] Time-series validation compatibility

## 6. Forecasting Model Development
### Candidate Models
- [ ] Rolling Mean
- [ ] Seasonal Naive
- [ ] ETS / Exponential Smoothing
- [ ] Croston-style intermittent-demand baseline
### Forecast Contract
- [ ] Configurable horizon
- [ ] Exact horizon length
- [ ] Numeric/non-negative forecasts
- [ ] No NaN/inf
- [ ] Empty/short history handling
- [ ] Controlled model fallback
- [ ] Zero-demand preservation
- [ ] No future leakage
### Metrics
- [ ] MAE
- [ ] WAPE
- [ ] sMAPE
- [ ] Zero-denominator behavior documented
### Output
- [ ] Bar
- [ ] Brand
- [ ] Alcohol type
- [ ] Model
- [ ] Forecast date
- [ ] Horizon step
- [ ] Forecast ml
### Gate
- [ ] All 96 series
- [ ] 7-day horizon
- [ ] Sparse series safe
- [ ] Reproducible
- [ ] Existing tests checked
- [ ] Personally reviewed

## 7. Walk-Forward Backtesting — CURRENT
### Validation Design
- [ ] Chronological splits only
- [ ] No random shuffling
- [ ] Explicit forecast horizon
- [ ] Explicit minimum training history
- [ ] Explicit validation origins
- [ ] Same origins for all models
- [ ] Zero-demand days preserved
### Walk-Forward Flow
- [ ] Train only through each origin
- [ ] Forecast next validation horizon
- [ ] Compare with actuals
- [ ] Move origin forward
- [ ] Repeat
### Evaluation
- [ ] MAE per window/model/series
- [ ] WAPE per window/model/series
- [ ] sMAPE per window/model/series
- [ ] Valid-window count
- [ ] Aggregate by model
- [ ] Aggregate by series
### Model Selection
- [ ] Define primary metric before selection
- [ ] Handle zero-demand windows explicitly
- [ ] Deterministic tie-break
- [ ] Select one model per series
- [ ] Retain supporting metrics
- [ ] No claim of universal best model
### Leakage / Edge Cases
- [ ] Training ends before validation
- [ ] No future feature leakage
- [ ] No validation actual leakage
- [ ] Sparse series
- [ ] Zero-demand validation
- [ ] Short history
- [ ] Model failures
- [ ] Missing/NaN values
- [ ] Horizon availability
### Outputs
- [ ] Detailed walk-forward results
- [ ] Per-series metrics
- [ ] Overall model summary
- [ ] Selected model per series
- [ ] Validation configuration
- [ ] No production forecast yet
### Gate
- [ ] All eligible series evaluated
- [ ] Identical validation design across models
- [ ] Leakage check passes
- [ ] Reproducible
- [ ] Deterministic selection
- [ ] Results manually inspected

## 8. Final 7-Day Forecast
- [ ] Use Category 7 selected model
- [ ] Train only on permitted history
- [ ] Exactly 7 future days
- [ ] 96 series
- [ ] Non-negative forecasts
- [ ] Identifiers/date/horizon retained
- [ ] Final forecast dataset
- [ ] Category 7 passed first

## 9. Dynamic PAR Level
- [ ] Lead time
- [ ] Review period
- [ ] Coverage period
- [ ] Demand basis
- [ ] Safety-stock input
- [ ] Current inventory
- [ ] On-order inventory
- [ ] Order-up-to target
- [ ] Rounding rule
- [ ] Traceable recommendation

## 10. Safety Stock / Service Level
- [ ] Service levels
- [ ] z-values
- [ ] Demand variability method
- [ ] Lead-time treatment
- [ ] Scenario comparison
- [ ] Assumptions
- [ ] No unsupported service-level guarantee

## 11. Inventory Simulation
- [ ] Starting inventory
- [ ] Demand consumption
- [ ] Order timing
- [ ] Lead-time receipts
- [ ] On-order tracking
- [ ] Correct inventory position
- [ ] Duplicate-order prevention
- [ ] Stockout/depletion tracking
- [ ] Lost volume
- [ ] Fill/service level
- [ ] Average inventory
- [ ] Ending inventory
- [ ] Orders

## 12. Policy Calibration & Sensitivity
- [ ] Service-level sensitivity
- [ ] Lead-time sensitivity
- [ ] Review-period sensitivity
- [ ] Forecast sensitivity
- [ ] KPI comparison
- [ ] Tradeoffs documented
- [ ] No unsupported optimization claims

## 13. Inventory Recommendations
- [ ] High-volume series
- [ ] High-risk sparse series
- [ ] Stockout/depletion patterns
- [ ] Evidence-linked recommendations
- [ ] Traceable inputs
- [ ] Facts separated from assumptions

## 15. Automated Testing
- [ ] Forecast tests
- [ ] Metric tests
- [ ] Backtesting tests
- [ ] PAR tests
- [ ] Safety-stock tests
- [ ] Simulation tests
- [ ] Edge cases
- [ ] Regression tests
- [ ] Full test suite

## 14. Architecture & Implementation Quality
- [ ] Clear module boundaries
- [ ] No duplicated business logic
- [ ] Centralized configuration
- [ ] Type/shape assumptions documented
- [ ] Error handling
- [ ] Reproducibility
- [ ] Clean imports
- [ ] No dead code
- [ ] No hidden leakage

## 16. Documentation
- [ ] Problem statement
- [ ] Questions before implementation
- [ ] Assumptions
- [ ] Solution approach
- [ ] Architecture
- [ ] Data design
- [ ] Model/service design
- [ ] Forecasting methodology
- [ ] Backtesting methodology
- [ ] PAR methodology
- [ ] Simulation methodology
- [ ] Technical decisions/tradeoffs
- [ ] Challenges
- [ ] Results
- [ ] Limitations
- [ ] Future improvements

## 17. Final Submission
- [ ] Working repository
- [ ] Reproducible pipeline
- [ ] Clean README
- [ ] Final notebook/results
- [ ] Final report
- [ ] Video
- [ ] 10–15 minute explanation
- [ ] Architecture explained
- [ ] Data/database design explained where applicable
- [ ] Model selection explained
- [ ] Module/API flow explained where applicable
- [ ] PAR calculation explained
- [ ] Simulation explained
- [ ] Tradeoffs explained
- [ ] Limitations explained
- [ ] Personally verify every artifact
