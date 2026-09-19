import math
import pandas as pd

from src.forecasting import mae, wape, rolling_mean_forecast
from src.inventory_optimization import safety_stock, reorder_point, par_level
from src.simulation import simulate_inventory


def test_forecast_metrics():
    actual = pd.Series([10, 20, 30])
    pred = pd.Series([10, 15, 35])
    assert mae(actual, pred) == 10 / 3
    assert round(wape(actual, pred), 8) == round((10 / 60) * 100, 8)


def test_safety_stock_and_policy():
    ss = safety_stock(2.0, 4.0, 0.95)
    assert ss > 0
    rp = reorder_point(10, 4, ss, pending_quantity=5)
    assert rp > 0
    par = par_level(10, 7, 4, ss, pending_quantity=5, moq=20)
    assert par >= 20


def test_simulation_tracks_stockouts():
    result = simulate_inventory([5, 5, 5], opening_inventory=7, reorder_quantity=10, reorder_point=3, lead_time_days=1)
    assert result.stockout_days >= 0
    assert result.lost_units >= 0
    assert 0 <= result.service_level <= 1
