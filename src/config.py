"""Validated policy configuration defaults. Replace with assignment/data-backed values before final results."""
from dataclasses import dataclass


@dataclass(frozen=True)
class InventoryPolicy:
    service_level: float = 0.95
    review_period_days: int = 7
    default_lead_time_days: int = 3
    default_moq: float = 0.0
