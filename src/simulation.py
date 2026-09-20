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
    turnover: float


def simulate_inventory(demand, opening_inventory: float, par_level, lead_time_days: int = 2, reorder_point: float | None = None) -> SimulationResult:
    """Order-up-to-par policy: order (par - on-hand - in-transit) whenever position < reorder_point (default par).

    Lost demand is not backordered. Turnover = units served / average inventory.
    """
    demand = list(demand)
    pars = list(par_level) if hasattr(par_level, "__len__") else [float(par_level)] * len(demand)  # per-day par allows dynamic policies
    lead = max(0, int(lead_time_days))
    inventory = float(opening_inventory)
    in_transit: list[tuple[int, float]] = []
    stockout_days = 0
    lost_units = served_units = total_demand = 0.0
    levels: list[float] = []
    for day, raw in enumerate(demand):
        inventory += sum(qty for due, qty in in_transit if due <= day)
        in_transit = [(due, qty) for due, qty in in_transit if due > day]
        daily = max(0.0, float(raw))
        total_demand += daily
        served = min(inventory, daily)
        inventory -= served
        served_units += served
        lost_units += daily - served
        stockout_days += int(daily > served)
        position = inventory + sum(qty for _, qty in in_transit)
        if position < (pars[day] if reorder_point is None else reorder_point):
            in_transit.append((day + lead, pars[day] - position))
        levels.append(inventory)
    avg = sum(levels) / len(levels) if levels else 0.0
    service = served_units / total_demand if total_demand else 1.0
    return SimulationResult(stockout_days, lost_units, avg, service, inventory, served_units / avg if avg else 0.0)
