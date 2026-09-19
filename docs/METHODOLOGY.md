# Methodology

## Forecasting

Start with interpretable baselines (recent rolling mean and seasonal-naive weekly pattern). Candidate models may be added only when the available data and evaluation design justify them. Evaluation must use chronological holdouts to avoid future leakage.

## Inventory policy

Core policy layers are:
- Safety stock from demand variability, lead time, and service level.
- Reorder point from expected lead-time demand plus safety stock, adjusted for pending supply where available.
- Dynamic par level from expected demand over lead time plus the review period, plus safety stock and applicable constraints.
- EOQ/MOQ/cost-aware ordering only when the assignment/data supports the required cost inputs.

## Simulation

Replay historical demand and inventory decisions under a defined policy. Track stockout days, lost units, average inventory, service level, and ending inventory. Additional KPIs can be added when the underlying data supports them.

## Transparency

Every recommendation should retain the forecast, policy parameters, current inventory position, pending quantity, and resulting order calculation so a reviewer can reproduce it.
