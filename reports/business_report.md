# Hotel Bar Inventory: Forecasting and Par Levels

Data: 6,575 transactions, 6 bars x 16 brands (96 series), 2023-01-01 to 2024-01-01. Every row satisfies Closing = Opening + Purchase - Consumed. Test window: last 74 days (20%), split by time.

## 1. Core business problem and operational impact
Bars either run out of popular brands or tie up cash and backroom space in slow ones. The data shows 416 closing-balance-zero events (6.3% of records) on items with demand, concentrated in Thomas's (103) and Taylor's (94) bars. Each is a guest who could not order a drink, plus revenue lost. Volume is spread evenly: 69 of 96 series are needed to reach 80% of consumption (Class A), so par levels must be right for most brands, not just a few.

## 2. Assumptions
- Supplier lead time is constant at 2 days (service levels 95% and 99%, Z = 1.645 / 2.326).
- Unmet demand is lost, not backordered.
- A bar-brand-day with no transaction is zero consumption (84% of the daily panel is zero); volumes are in ml with no bottle-size conversion.
- Safety-stock sigma is the training-period error of a 7-day rolling mean, so the backtest uses no test-period information.

## 3. Model selection and trade-offs
Compared: 7-day rolling mean, seasonal naive (t-7), Holt-Winters (weekly season), and one pooled RandomForest (lags 1/7/14, rolling mean/std, weekday, series id).

| Model | WAPE | MAE (ml) | RMSE (ml) |
|---|---|---|---|
| Rolling mean 7d | 1.663 | 92.6 | 153.2 |
| Seasonal naive | 1.751 | 97.5 | 203.6 |
| Holt-Winters | 1.683 | 93.7 | 145.6 |
| RandomForest | 1.724 | 96.1 | 147.1 |

Demand is highly intermittent, so no model beats the rolling mean by more than a few points and weekday seasonality is weak. I use the rolling mean for the level forecast: it is simplest, most interpretable and best on WAPE. Holt-Winters and RandomForest are slightly better on RMSE, which drives safety stock, and are the natural upgrade if richer signals (events, promotions) are added.

## 4. Performance and future improvements
Backtest of an order-up-to policy (lead time 2 days) over the test window, summed over 96 series:

| Policy | Stockout days | Lost volume (ml) | Fill rate | Avg inventory (ml) |
|---|---|---|---|---|
| Static baseline (mean x L) | 1,086 | 284,594 | 28.1% | 7,791 |
| Dynamic par, 95% | 292 | 48,575 | 87.7% | 42,372 |
| Dynamic par, 99% | 139 | 23,366 | 94.1% | 55,703 |

Dynamic par cuts stockout days by 73% (95%) to 87% (99%) and lost volume by 83% to 92%, at the cost of 5.4x to 7.1x higher average stock. The baseline carries little stock because it never protects against variability. Choose the service level by margin per lost ml versus holding cost: 95% for Class B/C, 99% for Class A. Improvements: promotion/event calendar, live POS feed, joint vendor delivery, per-brand lead times, and an actual holding-cost figure to optimise the trade-off instead of picking Z.

## 5. Deployment and production considerations
- A daily job recomputes forecasts and par levels and pushes order recommendations (par minus stock on hand and on order) to bar managers.
- What breaks at scale: lead-time variance (uses a constant), holiday and event shifts, pouring waste and breakage that make recorded consumption differ from real demand, and very sparse series.
- Monitoring: track WAPE and bias per series against actual orders, alert on drift in mean demand or sigma, and track weekly stockout count and fill rate against the 95%/99% targets.
