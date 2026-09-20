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
    """Weighted absolute percentage error as a ratio (sum|e| / sum y); NaN when denominator is zero."""
    a = pd.Series(actual, dtype="float64")
    p = pd.Series(predicted, dtype="float64")
    denom = float(a.abs().sum())
    return float(a.subtract(p).abs().sum() / denom) if denom else float("nan")


def rmse(actual: pd.Series, predicted: pd.Series) -> float:
    """Root mean squared error."""
    a = pd.Series(actual, dtype="float64")
    p = pd.Series(predicted, dtype="float64")
    return float(np.sqrt(np.mean((a.to_numpy() - p.to_numpy()) ** 2)))


def holt_winters_one_step(train: pd.Series, full: pd.Series, season_length: int = 7) -> np.ndarray:
    """One-step-ahead additive Holt-Winters predictions for `full`, with parameters and initial state fit on `train` only.

    Falls back to a 7-day shifted rolling mean for short/flat series or fit failure.
    """
    fallback = pd.Series(full, dtype="float64").shift(1).rolling(7, min_periods=1).mean().fillna(0.0).to_numpy()
    tr = pd.Series(train, dtype="float64").to_numpy()
    if len(tr) < 2 * season_length or np.unique(tr).size < 2:
        return fallback
    try:
        from statsmodels.tsa.holtwinters import ExponentialSmoothing

        p = ExponentialSmoothing(tr, seasonal="add", seasonal_periods=season_length).fit().params
        model = ExponentialSmoothing(
            pd.Series(full, dtype="float64").to_numpy(), seasonal="add", seasonal_periods=season_length,
            initialization_method="known", initial_level=p["initial_level"], initial_seasonal=p["initial_seasons"],
        )
        fitted = model.fit(smoothing_level=p["smoothing_level"], smoothing_seasonal=p["smoothing_seasonal"], optimized=False).fittedvalues
        return np.clip(fitted, 0, None)
    except Exception:  # ponytail: any statsmodels convergence failure -> baseline instead of crashing 96 series
        return fallback


def mae(actual: pd.Series, predicted: pd.Series) -> float:
    """Mean absolute error."""
    a = pd.Series(actual, dtype="float64")
    p = pd.Series(predicted, dtype="float64")
    return float(np.abs(a.to_numpy() - p.to_numpy()).mean())
