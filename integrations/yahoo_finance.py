import yfinance as yf
import pandas as pd
import logging

from core.retry import retry
from settings import settings

logger = logging.getLogger(__name__)


class YahooFinanceClient:
    def __init__(self, period: str = settings.YF_PERIOD, interval: str = settings.YF_INTERVAL):
        self.period = period
        self.interval = interval

    def fetch_ohlc(self, ticker: str, retries: int = 2) -> pd.DataFrame:
        try:
            df = retry(
                lambda: yf.download(
                    ticker,
                    period=self.period,
                    interval=self.interval,
                    auto_adjust=True,
                ),
                retries,
            )

            if df.empty:
                raise ValueError(f"No data for ticker: {ticker}")

            return df

        except Exception:
            logger.exception(f"Download failed | ticker={ticker}, period={self.period}, interval={self.interval}")
            raise
