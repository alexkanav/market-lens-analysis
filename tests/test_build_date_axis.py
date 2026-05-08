import pandas as pd
import pytest

from visualization.utils import build_date_axis


@pytest.mark.parametrize(
    "interval, expected_x, expected_y",
    [
        (2, [0, 2, 4], ["01-01", "01-03", "01-05"]),
        (0, [0, 1, 2, 3, 4], ["01-01", "01-02", "01-03", "01-04", "01-05"]),
        (-5, [0, 1, 2, 3, 4], ["01-01", "01-02", "01-03", "01-04", "01-05"]),
        (10, [0], ["01-01"]),
    ],
    ids=[
        "interval_2",
        "interval_0_defaults_to_1",
        "negative_interval_defaults_to_1",
        "interval_larger_than_length",
    ]
)
def test_build_date_axis__by_interval__returns_expected_axis(make_ohlc_df, interval, expected_x, expected_y):
    x, y = build_date_axis(make_ohlc_df(), interval=interval)

    assert x == expected_x
    assert y == expected_y


def test_build_date_axis__missing_date_column__raises_value_error():
    df = pd.DataFrame({
        "Close": [1, 2, 3]
    })

    with pytest.raises(ValueError, match="DataFrame must contain 'Date' column"):
        build_date_axis(df, interval=1)


def test_build_date_axis__string_dates__formats_correctly():
    df = pd.DataFrame({
        "Date": ["2024-12-31", "2025-01-01"]
    })

    _, y = build_date_axis(df, interval=1)

    assert y == ["12-31", "01-01"]


def test_build_date_axis__valid_interval__returns_same_length_axes(make_ohlc_df):
    x, y = build_date_axis(make_ohlc_df(), interval=3)

    assert len(x) == len(y)


def test_build_date_axis__invalid_dates__raises_exception():
    df = pd.DataFrame({
        "Date": ["2024-01-01", "invalid-date"]
    })

    with pytest.raises(ValueError, match="Unknown datetime string format|time data"):
        build_date_axis(df, interval=1)
