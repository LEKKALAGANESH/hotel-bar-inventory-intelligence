"""Inventory analytics helpers independent of any UI layer."""
from __future__ import annotations

import pandas as pd


def classify_movement(turnover: pd.Series, fast_threshold: float, slow_threshold: float) -> pd.Series:
    """Classify inventory movement using explicit thresholds."""
    if slow_threshold > fast_threshold:
        raise ValueError("slow_threshold must not exceed fast_threshold")
    return pd.Series(turnover).map(lambda x: "fast" if x >= fast_threshold else ("slow" if x <= slow_threshold else "medium"))


def days_to_stockout(current_inventory: pd.Series, daily_demand: pd.Series) -> pd.Series:
    """Estimate days until stockout; infinity for zero-demand items."""
    inv = pd.to_numeric(current_inventory, errors="coerce")
    demand = pd.to_numeric(daily_demand, errors="coerce")
    return inv.div(demand.replace(0, pd.NA)).fillna(float("inf"))
