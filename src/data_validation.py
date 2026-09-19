"""Data validation and preprocessing primitives for hotel bar inventory data."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import pandas as pd


@dataclass(frozen=True)
class ValidationResult:
    valid: bool
    errors: tuple[str, ...]
    warnings: tuple[str, ...]


def require_columns(df: pd.DataFrame, columns: Iterable[str]) -> list[str]:
    """Return missing required columns in deterministic order."""
    return [column for column in columns if column not in df.columns]


def validate_frame(df: pd.DataFrame, required_columns: Iterable[str]) -> ValidationResult:
    """Perform structural validation without silently altering source data."""
    errors: list[str] = []
    warnings: list[str] = []
    if df.empty:
        errors.append("Input dataset is empty")
    missing = require_columns(df, required_columns)
    if missing:
        errors.append(f"Missing required columns: {', '.join(missing)}")
    if "date" in df.columns:
        if not pd.api.types.is_datetime64_any_dtype(df["date"]):
            warnings.append("date is not datetime dtype; parse it before modeling")
    numeric_candidates = [c for c in ("consumption", "opening_inventory", "closing_inventory", "purchases") if c in df.columns]
    for column in numeric_candidates:
        if (pd.to_numeric(df[column], errors="coerce") < 0).any():
            warnings.append(f"Negative values detected in {column}")
    return ValidationResult(valid=not errors, errors=tuple(errors), warnings=tuple(warnings))


def derive_consumption(df: pd.DataFrame) -> pd.Series:
    """Derive consumption from opening + purchases - closing when all inputs exist."""
    required = {"opening_inventory", "purchases", "closing_inventory"}
    if not required.issubset(df.columns):
        raise ValueError("Consumption derivation requires opening_inventory, purchases, and closing_inventory")
    return df["opening_inventory"] + df["purchases"] - df["closing_inventory"]


def build_daily_panel(df: pd.DataFrame, group_columns: list[str]) -> pd.DataFrame:
    """Create a dense daily panel so zero-consumption days remain represented."""
    if "date" not in df.columns:
        raise ValueError("date column is required")
    frame = df.copy()
    frame["date"] = pd.to_datetime(frame["date"])
    frame = frame.sort_values("date")
    index_parts = [frame[c].dropna().unique() for c in group_columns]
    if any(len(values) == 0 for values in index_parts):
        return frame
    start, end = frame["date"].min(), frame["date"].max()
    dates = pd.date_range(start, end, freq="D", name="date")
    keys = pd.MultiIndex.from_product([dates, *index_parts], names=["date", *group_columns])
    panel = keys.to_frame(index=False).merge(frame, on=["date", *group_columns], how="left")
    if "consumption" in panel.columns:
        panel["consumption"] = panel["consumption"].fillna(0.0)
    return panel
