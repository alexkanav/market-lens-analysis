import itertools
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import logging

from core.retry import retry
from settings import settings

logger = logging.getLogger(__name__)


class GoogleSheets:
    def __init__(
            self,
            key_file: str,
            gsheet_id: str,
            read_range: str,
            write_start: str,
    ) -> None:
        self.gsheet_id = gsheet_id
        self.read_range = read_range
        self.write_start = write_start

        try:
            credentials = Credentials.from_service_account_file(key_file, scopes=settings.SCOPES)
            self.service = build('sheets', 'v4', credentials=credentials)
        except Exception:
            logger.exception("Failed to initialize Google Sheets client")
            raise

    def get_tickers(self, retries: int = 3, sheet_range: str | None = None) -> list[list[str]]:
        """Fetch ticker data from Google Sheets."""
        sheet_range = sheet_range or self.read_range

        try:
            values = retry(
                lambda: self.service.spreadsheets().values().get(
                    spreadsheetId=self.gsheet_id,
                    range=sheet_range,
                    majorDimension='ROWS'
                ).execute(),
                retries
            )

            return values.get('values', [])

        except Exception:
            logger.exception(f"Read failed | sheet_id={self.gsheet_id}, range={sheet_range}")
            raise

    def write_values(self, values: list[list[str | float]], retries: int = 3, start_cell: str | None = None) -> None:
        start_cell = start_cell or self.write_start

        if not values:
            logger.warning("No data to write")
            return

        try:
            retry(
                lambda: self.service.spreadsheets().values().batchUpdate(
                    spreadsheetId=self.gsheet_id,
                    body={
                        "valueInputOption": "USER_ENTERED",
                        "data": [
                            {
                                "range": start_cell,
                                "majorDimension": 'ROWS',
                                "values": values
                            }
                        ]
                    }
                ).execute(),
                retries
            )

        except Exception:
            logger.exception(f"Write failed | sheet_id={self.gsheet_id}, range={start_cell}")
            raise

    def save_predictions(self, data: dict[str, list[list[float]]], retries: int = 3) -> None:
        result = [
            [key] + list(itertools.chain.from_iterable(val))
            for key, val in data.items()
        ]

        self.write_values(
            result,
            retries
        )
