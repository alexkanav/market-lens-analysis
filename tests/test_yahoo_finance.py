import pandas as pd
import pytest

from integrations.yahoo_finance import YahooFinanceClient


@pytest.fixture
def mock_retry(mocker):
    return mocker.patch(
        "integrations.yahoo_finance.retry",
        side_effect=lambda fn, retries: fn()
    )


@pytest.fixture
def mock_download(mocker):
    return mocker.patch("integrations.yahoo_finance.yf.download")


@pytest.fixture
def client():
    return YahooFinanceClient(period="1y", interval="1d")


def test_fetch_ohlc__successful_download__returns_dataframe(
        mock_retry, mock_download, client
):
    df = pd.DataFrame({
        "Open": [1, 2],
        "High": [2, 3],
        "Low": [0.5, 1.5],
        "Close": [1.5, 2.5],
    })

    mock_download.return_value = df

    result = client.fetch_ohlc("AAPL")

    mock_download.assert_called_once_with(
        "AAPL",
        period="1y",
        interval="1d",
        auto_adjust=True,
    )

    assert result.equals(df)


def test_fetch_ohlc__empty_dataframe__raises_value_error(
        mock_retry, mock_download, client
):
    mock_download.return_value = pd.DataFrame()

    with pytest.raises(ValueError, match="No data for ticker"):
        client.fetch_ohlc("AAPL")


def test_fetch_ohlc__download_failure__raises_exception(
        mock_retry, mock_download, client
):
    mock_download.side_effect = Exception("Network error")

    with pytest.raises(Exception):
        client.fetch_ohlc("AAPL")
