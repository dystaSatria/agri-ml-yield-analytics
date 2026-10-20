"""Evaluation metrics and KPI target checks."""
import numpy as np
from sklearn.metrics import r2_score

from src.config import KPI_TARGETS


def mape(y_true, y_pred) -> float:
    """Mean Absolute Percentage Error in percent. Zero true values are excluded."""
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    mask = y_true != 0
    if not mask.any():
        raise ValueError("MAPE is undefined when every true value is zero.")
    return float(np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100)


def check_yield_kpis(y_true, y_pred) -> dict:
    """Compare crop yield predictions against the Week 1 KPI targets."""
    r2 = float(r2_score(y_true, y_pred))
    err = mape(y_true, y_pred)
    return {
        "r2": r2,
        "mape": err,
        "r2_pass": r2 >= KPI_TARGETS["yield_r2_min"],
        "mape_pass": err <= KPI_TARGETS["yield_mape_max"],
    }
