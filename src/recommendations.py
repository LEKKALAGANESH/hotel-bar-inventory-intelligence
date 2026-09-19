"""Procurement recommendation generation."""
from __future__ import annotations


def recommend_order(current_inventory: float, par_level_value: float, pending_quantity: float = 0.0, moq: float = 0.0) -> dict:
    """Return a transparent reorder decision and quantity."""
    position = current_inventory + pending_quantity
    gap = max(0.0, par_level_value - position)
    quantity = max(gap, moq) if gap > 0 else 0.0
    return {
        "inventory_position": position,
        "order_required": quantity > 0,
        "recommended_quantity": quantity,
    }
