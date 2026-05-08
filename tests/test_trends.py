import pytest
import pandas as pd
import numpy as np

from analysis.trends import calculate_trend_lines, predictions
from config import TIMEFRAMES_DAYS


def test_calculate_trend_lines__valid_dataframe__returns_numpy_arrays(trend_df):
    (y_min, y_max), preds = calculate_trend_lines(trend_df, timeframe=5, step=2)

    assert isinstance(y_min, np.ndarray)
    assert isinstance(y_max, np.ndarray)
    assert len(preds) == 2


def test_predictions__missing_close_column__raises_key_error():
    df = pd.DataFrame({"Open": np.arange(200)})

    with pytest.raises(KeyError):
        predictions(df, step=5)


def test_calculate_trend_lines__uptrend_dataframe__returns_y_min_below_y_max(trend_df):
    (y_min, y_max), _ = calculate_trend_lines(trend_df, timeframe=10, step=2)

    assert np.all(y_min <= y_max)


def test_predictions__valid_dataframe__returns_expected_output_structure(trend_df):
    y_vals, lines = predictions(trend_df, step=2)

    assert len(y_vals) == len(TIMEFRAMES_DAYS)
    assert len(lines) == len(TIMEFRAMES_DAYS)

    for preds in y_vals:
        assert len(preds) == 2


def test_predictions__valid_dataframe__processes_all_timeframes(trend_df):
    y_vals, lines = predictions(trend_df, step=5)

    assert len(y_vals) == len(TIMEFRAMES_DAYS)
