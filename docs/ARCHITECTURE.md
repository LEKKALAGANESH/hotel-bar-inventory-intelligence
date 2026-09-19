# Architecture

The system is intentionally layered:

1. **Data ingestion & validation** — schema checks, type normalization, reconciliation rules, missingness and anomaly flags.
2. **Demand dataset construction** — daily item/location panel with zero-demand days retained.
3. **Forecasting** — baseline and candidate demand models evaluated using time-aware validation.
4. **Inventory optimization** — safety stock, reorder point, dynamic par level, and optional EOQ/MOQ/cost constraints.
5. **Simulation** — replay historical demand under candidate inventory policies.
6. **Analytics** — stockout risk, excess inventory, movement classification, days-to-stockout, turnover, and order urgency when source data supports them.
7. **Recommendations** — transparent recommended order quantity, priority, and rationale.
8. **Reporting** — reproducible tables, charts, methodology, assumptions, validation results, and limitations.

A production UI is not assumed unless the assignment explicitly requires one; analytical outputs remain usable without coupling the core logic to a web framework.
