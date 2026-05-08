import pytest
from unittest.mock import Mock, patch

from integrations.google_sheets import GoogleSheets


@pytest.fixture
def sheets(mock_service):
    with patch("integrations.google_sheets.Credentials.from_service_account_file"), \
            patch("integrations.google_sheets.build", return_value=mock_service):
        return GoogleSheets(
            key_file="fake.json",
            gsheet_id="sheet123",
            read_range="A1:A10",
            write_start="B1"
        )


@pytest.mark.parametrize("value, expected", [
    ({"values": [["AAPL"], ["TSLA"]]}, [["AAPL"], ["TSLA"]]),
    ({}, []),
])
def test_get_tickers__valid_response__returns_values(sheets, mock_service, value, expected):
    mock_service.spreadsheets.return_value.values.return_value.get.return_value.execute.return_value = value

    with patch("integrations.google_sheets.retry", side_effect=lambda fn, r: fn()):
        result = sheets.get_tickers()

    assert result == expected


def test_get_tickers__none_response__raises_exception(sheets, mock_service):
    mock_service.spreadsheets.return_value.values.return_value.get.return_value.execute.return_value = None

    with patch("integrations.google_sheets.retry", side_effect=lambda fn, r: fn()):
        with pytest.raises(Exception):
            sheets.get_tickers()


def test_get_tickers__missing_values_key__returns_empty_list(sheets, mock_service):
    values_api = mock_service.spreadsheets.return_value.values.return_value
    values_api.get.return_value.execute.return_value = {"range": "A1:A10"}

    with patch("integrations.google_sheets.retry", side_effect=lambda fn, r: fn()):
        result = sheets.get_tickers()

    assert result == []


def test_write_values__valid_values__executes_batch_update(sheets, mock_service):
    mock_execute = Mock()

    mock_service.spreadsheets.return_value.values.return_value.batchUpdate.return_value.execute = mock_execute

    with patch("integrations.google_sheets.retry", side_effect=lambda fn, r: fn()):
        sheets.write_values([["AAPL", 100]])

    mock_execute.assert_called_once()


def test_write_values__empty_values__does_not_call_retry(sheets):
    with patch("integrations.google_sheets.retry") as mock_retry:
        sheets.write_values([])

    mock_retry.assert_not_called()


def test_write_values__batch_update_failure__raises_exception(sheets, mock_service):
    mock_service.spreadsheets.return_value.values.return_value.batchUpdate.side_effect = Exception("Write error")

    with patch("integrations.google_sheets.retry", side_effect=lambda fn, r: fn()):
        with pytest.raises(Exception):
            sheets.write_values([["AAPL", 100]])


def test_save_predictions__valid_data__formats_and_writes_values(sheets):
    data = {
        "AAPL": [[1.1, 2.2], [3.3]],
        "TSLA": [[4.4]]
    }

    with patch.object(sheets, "write_values") as mock_write:
        sheets.save_predictions(data)

    expected = [
        ["AAPL", 1.1, 2.2, 3.3],
        ["TSLA", 4.4]
    ]

    mock_write.assert_called_once_with(expected, 3)
