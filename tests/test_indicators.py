import pandas as pd
import pytest

from stock import rsi


def test_rsi_all_gains():
    series = pd.Series([1, 2, 3, 4])
    result = rsi(series)
    assert result == pytest.approx(100)


def test_rsi_all_losses():
    series = pd.Series([-1, -2, -3, -4])
    result = rsi(series)
    assert result == pytest.approx(0)


def test_rsi_all_zeros():
    series = pd.Series([0, 0, 0, 0])
    result = rsi(series)
    assert result == 0
    assert not pd.isna(result)

