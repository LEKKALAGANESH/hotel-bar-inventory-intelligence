"""Demand forecasting utilities using time-aware, leakage-resistant patterns."""
from __future__ import annotations

import numpy as np
import pandas as pd


def rolling_mean_forecast(history: pd.Series, horizon: int = 7, window: int = 7) -> np.ndarray:
    """Forecast using the mean of the most recent observations."""
    clean = pd.Series(history, dtype="float64").dropna()
    if clean.empty:
        return np.zeros(horizon, dtype=float)
    sample = clean.tail(max(1, window))
    return np.repeat(float(sample.mean()), horizon)


def seasonal_naive_forecast(history: pd.Series, horizon: int = 7, season_length: int = 7) -> np.ndarray:
    """Repeat the most recent complete seasonal pattern when available."""
    clean = pd.Series(history, dtype="float64").dropna().to_numpy()
    if clean.size == 0:
        return np.zeros(horizon, dtype=float)
    pattern = clean[-season_length:] if clean.size >= season_length else clean
    return np.resize(pattern, horizon)


def wape(actual: pd.Series, predicted: pd.Series) -> float:
    """Weighted absolute percentage error; returns NaN when denominator is zero."""
    a = pd.Series(actual, dtype="float64")
    p = pd.Series(predicted, dtype="float64")
    denom = float(a.abs().sum())
    return float((a.subtract(p).abs().sum() / denom) * 100) if denom else float("nan")


def mae(actual: pd.Series, predicted: pd.Series) -> float:
    """Mean absolute error."""
    a = pd.Series(actual, dtype="float64")
    p = pd.Series(predicted, dtype="float64")
    return float(np.abs(a.to_numpy() - p.to_numpy()).mean())
