import numpy as np
import pytest

from src.kpi import mape, check_yield_kpis


def test_mape_known_value():
    # errors are 10% and 10%, so the mean is 10%
    assert mape([100, 200], [110, 180]) == pytest.approx(10.0)


def test_mape_ignores_zero_true_values():
    assert mape([0, 100], [5, 90]) == pytest.approx(10.0)


def test_mape_all_zero_raises():
    with pytest.raises(ValueError):
        mape([0, 0], [1, 2])


def test_check_yield_kpis_perfect_prediction_passes():
    y = np.array([4.0, 5.0, 6.0, 7.0])
    result = check_yield_kpis(y, y)
    assert result["r2"] == pytest.approx(1.0)
    assert result["r2_pass"] and result["mape_pass"]
