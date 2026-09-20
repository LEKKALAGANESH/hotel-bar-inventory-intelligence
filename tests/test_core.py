import pandas as pd

from src.data_validation import check_conservation
from src.forecasting import holt_winters_one_step, mae, rmse, wape
from src.inventory_optimization import par_level, reorder_point, safety_stock
from src.simulation import simulate_inventory


def test_forecast_metrics():
    actual = pd.Series([10, 20, 30])
    pred = pd.Series([10, 15, 35])
    assert mae(actual, pred) == 10 / 3
    assert round(wape(actual, pred), 8) == round(10 / 60, 8)
    assert round(rmse(actual, pred), 6) == round((50 / 3) ** 0.5, 6)


def test_holt_winters_one_step_shape_and_fallback():
    weekly = pd.Series([1, 2, 3, 4, 5, 9, 10] * 6, dtype=float)
    assert len(holt_winters_one_step(weekly[:28], weekly)) == len(weekly)
    flat = pd.Series([0.0] * 30)
    assert (holt_winters_one_step(flat[:20], flat) == 0).all()


def test_safety_stock_and_policy():
    ss = safety_stock(2.0, 4.0, 0.95)
    assert ss > 0
    assert reorder_point(10, 4, ss, pending_quantity=5) > 0
    assert par_level(10, 7, 4, ss, pending_quantity=5, moq=20) >= 20


def test_conservation_flags_bad_rows():
    df = pd.DataFrame({"o": [10, 10], "p": [0, 0], "c": [3, 3], "cl": [7, 5]})
    assert check_conservation(df, "o", "p", "c", "cl").tolist() == [False, True]


def test_simulation_orders_up_to_par_without_duplicates():
    r = simulate_inventory([5] * 10, opening_inventory=20, par_level=20, lead_time_days=2)
    assert r.stockout_days == 0 and r.service_level == 1
    assert r.average_inventory <= 20 and r.turnover > 0


def test_simulation_tracks_stockouts():
    r = simulate_inventory([5, 5, 5], opening_inventory=7, par_level=10, lead_time_days=5)
    assert r.stockout_days == 2 and r.lost_units == 8
