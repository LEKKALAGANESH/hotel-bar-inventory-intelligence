"""Deterministic inventory policy simulation/backtesting primitives."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SimulationResult:
    stockout_days: int
    lost_units: float
    average_inventory: float
    service_level: float
    ending_inventory: float


def simulate_inventory(demand, opening_inventory: float, reorder_quantity: float, reorder_point: float, lead_time_days: int = 0) -> SimulationResult:
    """Simulate a simple replenishment policy against an ordered demand sequence."""
    inventory = float(opening_inventory)
    in_transit: list[tuple[int, float]] = []
    stockout_days = 0
    lost_units = 0.0
    inventory_levels: list[float] = []
    served_units = 0.0
    total_demand = 0.0
    for day, raw_demand in enumerate(demand):
        arrivals = sum(qty for arrival_day, qty in in_transit if arrival_day <= day)
        in_transit = [(arrival_day, qty) for arrival_day, qty in in_transit if arrival_day > day]
        inventory += arrivals
        daily = max(0.0, float(raw_demand))
        total_demand += daily
        served = min(inventory, daily)
        inventory -= served
        served_units += served
        lost = daily - served
        lost_units += lost
        stockout_days += int(lost > 0)
        if inventory <= reorder_point and reorder_quantity > 0:
            in_transit.append((day + max(0, int(lead_time_days)), reorder_quantity))
        inventory_levels.append(inventory)
    avg = sum(inventory_levels) / len(inventory_levels) if inventory_levels else 0.0
    service = served_units / total_demand if total_demand else 1.0
    return SimulationResult(stockout_days, lost_units, avg, service, inventory)
