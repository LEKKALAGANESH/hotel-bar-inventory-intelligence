# Hotel Bar Inventory Forecasting & Par Level Recommendation

Forecasts daily demand for each bar and brand from bottle-balance logs, recommends dynamic par levels, and backtests them with an inventory simulation. Built for hotel bar managers who need to avoid both stockouts and overstock.

## Results

The main deliverable is the executed notebook, [`notebooks/inventory_forecasting_solution.ipynb`](notebooks/inventory_forecasting_solution.ipynb), with charts and tables inline. The executive summary is in [`reports/business_report.pdf`](reports/business_report.pdf).

Backtest on the last 74 days (20% of the data), 96 bar-brand series, supplier lead time of 2 days:

| Policy | Stockout days | Lost volume (ml) | Fill rate | Average stock (ml) |
|---|---|---|---|---|
| Static baseline (mean demand x lead time) | 1,086 | 284,594 | 28.1% | 7,791 |
| Dynamic par, 95% service level | 292 | 48,575 | 87.7% | 42,372 |
| Dynamic par, 99% service level | 139 | 23,366 | 94.1% | 55,703 |

Dynamic par levels cut stockout days by 73% to 87%, at the cost of holding 5.4 to 7.1 times more stock on average.

## Table of contents

- [Features](#features)
- [Tech stack](#tech-stack)
- [Getting started](#getting-started)
- [Usage](#usage)
- [Project structure](#project-structure)
- [Testing](#testing)
- [Status and limitations](#status-and-limitations)
- [Contributing](#contributing)

## Features

- Validates the inventory identity `Closing = Opening + Purchase - Consumed` on every row.
- Builds a dense daily panel per bar and brand, keeping zero-demand days.
- Exploratory analysis: ABC velocity classes, weekday pattern, historical stockout audit.
- Four one-step-ahead forecasters compared on a time-based split: 7-day rolling mean, seasonal naive, Holt-Winters, and a pooled RandomForest. Metrics are MAE, RMSE and WAPE.
- Par level = lead-time demand + safety stock, where safety stock = Z x sigma x sqrt(lead time), recomputed daily.
- Order-up-to-par simulation that reports stockout days, lost volume, average stock and turnover.

## Tech stack

Python, pandas, NumPy, statsmodels, scikit-learn, matplotlib, seaborn, Jupyter, pytest.

## Getting started

### Prerequisites

- Python 3.10 or newer (developed on 3.14)
- About 1 GB of free disk space

### Install

```bash
git clone <repository-url>
cd hotel-bar-inventory-intelligence
pip install -r requirements.txt
```

### Configuration

No environment variables are required. Policy defaults (service level, lead time, review period) are in [`src/config.py`](src/config.py).

## Usage

### 1. Run the analysis

```bash
jupyter nbconvert --to notebook --execute --inplace notebooks/inventory_forecasting_solution.ipynb
```

This also writes `data/processed/daily_bar_consumption.csv` and `reports/par_levels.csv`.

### 2. Compute a safety stock

```python
from src.inventory_optimization import safety_stock, par_level

ss = safety_stock(demand_std=170.0, lead_time_days=2, service_level=0.95)
par = par_level(forecast_daily_demand=250.0, review_period_days=0, lead_time_days=2, safety=ss)
```

### 3. Backtest a policy and get an order recommendation

```python
from src.simulation import simulate_inventory
from src.recommendations import recommend_order

result = simulate_inventory([120, 0, 300, 80], opening_inventory=600, par_level=700, lead_time_days=2)
print(result.stockout_days, result.lost_units, result.turnover)

print(recommend_order(current_inventory=200, par_level_value=700, pending_quantity=100))
```

## Project structure

```text
.
├── data/
│   ├── raw/bar_inventory_data.csv           # original transaction logs
│   └── processed/daily_bar_consumption.csv  # dense daily panel per bar and brand
├── docs/                                    # methodology, architecture, validation notes
├── notebooks/
│   └── inventory_forecasting_solution.ipynb # EDA, forecasting, par levels, simulation
├── reports/
│   ├── business_report.pdf                  # executive summary
│   ├── business_report.md                   # source of the PDF
│   └── par_levels.csv                       # latest recommended par levels per series
├── src/                                     # tested helper modules
├── tests/                                   # pytest suite
└── requirements.txt
```

See [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md) and [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for design notes.

## Testing

```bash
python -m pytest -q
```

## Status and limitations

- About 84% of bar-brand-days have no transaction and are treated as zero consumption, so demand is highly intermittent. All forecasters score a WAPE near 1.7, and the 7-day rolling mean is best.
- Lead time is assumed constant at 2 days, and unmet demand is treated as lost, not backordered.
- Safety-stock sigma comes from training-period errors only, so the backtest uses no test-period information.
- Quantities are in ml. No bottle-size conversion is applied.

## Contributing

Open an issue to discuss a change, keep pull requests small, and make sure `python -m pytest -q` passes before submitting.
