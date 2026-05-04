from matplotlib import pyplot as plt
import logging

from settings import settings
from config import ENABLE_VISUALIZATION
from integrations.google_sheets import GoogleSheets
from integrations.yahoo_finance import YahooFinanceClient
from visualization.plotting_pipeline import visualize_ticker
from services.ticker_processor import process_ticker

logging.basicConfig(level=logging.INFO, filename="app.log", filemode="a",
                    format="%(asctime)s %(levelname)s %(message)s")

logger = logging.getLogger(__name__)


def run_pipeline() -> None:
    result = {}

    gsheet = GoogleSheets(
        settings.key_path,
        settings.SHEET_ID,
        settings.SHEET_READ_RANGE,
        settings.WRITE_START_CELL,
    )

    try:
        tickers = gsheet.get_tickers()
    except Exception:
        logger.exception("Failed to fetch tickers")
        raise

    yf_client = YahooFinanceClient()

    for row in tickers:
        if not row:
            continue

        ticker_name = row[0].strip()

        try:
            ticker_data = process_ticker(ticker_name, yf_client)
            if ticker_data is None:
                continue

            result[ticker_name] = ticker_data.y_values

            if ENABLE_VISUALIZATION:
                visualize_ticker(ticker_name, ticker_data)
                plt.show()

        except Exception:
            logger.exception(f"Processing failed for ticker: {ticker_name}")

    if result:
        gsheet.save_predictions(result)
    else:
        logger.warning("No results to write")
        raise RuntimeError("Pipeline produced no results")


def main() -> None:
    try:
        run_pipeline()
    except Exception:
        logger.exception("Pipeline failed")


if __name__ == "__main__":
    main()
