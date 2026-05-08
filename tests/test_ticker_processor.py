import pytest
import pandas as pd
import numpy as np

from services.ticker_processor import process_ticker


def test_process_ticker__insufficient_raw_data__returns_none(mocker):
    client = mocker.Mock()
    client.fetch_ohlc.return_value = pd.DataFrame({"Close": [1] * 10})

    result = process_ticker("AAPL", client)

    assert result is None


def test_process_ticker__insufficient_cleaned_data__returns_none(mocker):
    client = mocker.Mock()
    raw_df = pd.DataFrame({"Close": [1] * 200, "Open": [1] * 200})
    client.fetch_ohlc.return_value = raw_df

    mocker.patch("services.ticker_processor.prepare_dataframe", return_value=raw_df.iloc[:10])

    result = process_ticker("AAPL", client)

    assert result is None


def test_process_ticker__valid_data__returns_ticker_result(mocker, mock_service, trend_df):
    mock_service.fetch_ohlc.return_value = trend_df

    mocker.patch("services.ticker_processor.prepare_dataframe", return_value=trend_df)
    mocker.patch("services.ticker_processor.build_date_axis", return_value=([0, 1], ["01-01", "01-02"]))
    mocker.patch("services.ticker_processor.support_resistance_lines",
                 return_value=(np.array([1, 2]), np.array([1, 2])))
    mocker.patch("services.ticker_processor.predictions", return_value=([[1, 2]], [(np.array([1]), np.array([2]))]))

    result = process_ticker("AAPL", mock_service)

    assert result is not None
    assert isinstance(result.close, np.ndarray)
    assert np.array_equal(result.close, trend_df["Close"].to_numpy())


def test_process_ticker__valid_data__calls_processing_dependencies(mocker, mock_service, trend_df):
    mock_service.fetch_ohlc.return_value = trend_df

    prepare_mock = mocker.patch("services.ticker_processor.prepare_dataframe", return_value=trend_df)
    build_axis_mock = mocker.patch("services.ticker_processor.build_date_axis", return_value=([], []))
    sr_mock = mocker.patch("services.ticker_processor.support_resistance_lines", return_value=([], []))
    pred_mock = mocker.patch("services.ticker_processor.predictions", return_value=([], []))

    process_ticker("AAPL", mock_service)

    prepare_mock.assert_called_once_with("AAPL", trend_df)
    build_axis_mock.assert_called_once()
    sr_mock.assert_called_once()
    pred_mock.assert_called_once()


def test_process_ticker__fetch_failure__raises_exception(mocker):
    client = mocker.Mock()
    client.fetch_ohlc.side_effect = RuntimeError("API failed")

    with pytest.raises(RuntimeError):
        process_ticker("AAPL", client)
