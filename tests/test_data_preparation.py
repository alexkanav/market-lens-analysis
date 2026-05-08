import pandas as pd
import pytest

from services.data_preparation import prepare_dataframe


def test_prepare_dataframe__valid_dataframe__returns_clean_sorted_dataframe(make_ohlc_df):
    date_range = ["2025-01-02", "2025-01-01", "2024-12-31", "2024-12-30", "2025-01-03"]
    df = make_ohlc_df(Date=date_range)
    result = prepare_dataframe("AAPL", df)

    # Sorted by Date
    assert list(result["Date"]) == sorted(date_range)

    # Columns preserved
    required = {"Open", "High", "Low", "Close"}
    assert required.issubset(result.columns)


def test_prepare_dataframe__missing_required_columns__raises_value_error(make_ohlc_df):
    df = make_ohlc_df().drop("Close", axis=1)

    with pytest.raises(ValueError, match="Missing required columns"):
        prepare_dataframe("AAPL", df)


def test_prepare_dataframe__invalid_numeric_values__drops_invalid_rows(make_ohlc_df, capsys):
    df = make_ohlc_df(Open=[1, 2, 3, 4, "bad"])
    result = prepare_dataframe("AAPL", df)

    # One row should be dropped
    assert len(result) == 4

    # Check print output
    captured = capsys.readouterr()
    assert "dropped 1 rows" in captured.out


def test_prepare_dataframe__lowercase_columns__capitalizes_column_names():
    df = pd.DataFrame({
        "date": ["2024-01-01"],
        "open": [1],
        "high": [2],
        "low": [0.5],
        "close": [1.5],
    })

    result = prepare_dataframe("AAPL", df)

    assert "Date" in result.columns
    assert "Open" in result.columns


def test_prepare_dataframe__all_invalid_rows__returns_empty_dataframe(make_ohlc_df):
    df = make_ohlc_df(Open=["bad"] * 5)

    result = prepare_dataframe("AAPL", df)

    assert result.empty
