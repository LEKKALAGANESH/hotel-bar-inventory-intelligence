"""Inventory policy calculations with explicit business parameters."""
from __future__ import annotations

from math import sqrt
from statistics import NormalDist


def safety_stock(demand_std: float, lead_time_days: float, service_level: float = 0.95) -> float:
    """Safety stock using z * sigma * sqrt(L), with validated service level."""
    if not 0 < service_level < 1:
        raise ValueError("service_level must be between 0 and 1")
    if demand_std < 0 or lead_time_days < 0:
        raise ValueError("demand_std and lead_time_days must be non-negative")
    z = NormalDist().inv_cdf(service_level)
    return max(0.0, z * demand_std * sqrt(lead_time_days))


def reorder_point(avg_daily_demand: float, lead_time_days: float, safety: float, pending_quantity: float = 0.0) -> float:
    """Reorder point accounting for demand during lead time and pending supply."""
    if min(avg_daily_demand, lead_time_days, safety, pending_quantity) < 0:
        raise ValueError("inventory quantities and demand parameters must be non-negative")
    return max(0.0, avg_daily_demand * lead_time_days + safety - pending_quantity)


def par_level(forecast_daily_demand: float, review_period_days: float, lead_time_days: float, safety: float, pending_quantity: float = 0.0, moq: float = 0.0) -> float:
    """Dynamic target inventory covering lead time + review period plus safety stock."""
    if min(forecast_daily_demand, review_period_days, lead_time_days, safety, pending_quantity, moq) < 0:
        raise ValueError("inventory and policy parameters must be non-negative")
    target = forecast_daily_demand * (lead_time_days + review_period_days) + safety - pending_quantity
    target = max(0.0, target)
    if moq > 0 and target > 0:
        target = max(target, moq)
    return target


def eoq(annual_demand: float, ordering_cost: float, annual_holding_cost_per_unit: float) -> float:
    """Economic order quantity when cost assumptions are available."""
    if min(annual_demand, ordering_cost, annual_holding_cost_per_unit) < 0:
        raise ValueError("EOQ inputs must be non-negative")
    if annual_holding_cost_per_unit == 0:
        return 0.0
    return sqrt((2.0 * annual_demand * ordering_cost) / annual_holding_cost_per_unit)
