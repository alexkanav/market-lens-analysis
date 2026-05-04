import logging

from integrations.yahoo_finance import YahooFinanceClient
from services.data_preparation import prepare_dataframe
from visualization.utils import build_date_axis
from analysis.support_resistance import support_resistance_lines
from analysis.trends import predictions
from config import STEP, CHART_DATE_LABEL_INTERVAL, MIN_ROWS
from models.ticker import TickerResult

logger = logging.getLogger(__name__)


def process_ticker(ticker: str, client: YahooFinanceClient) -> TickerResult | None:
    stock_data = client.fetch_ohlc(ticker)
    if len(stock_data) < MIN_ROWS:
        logger.warning(f"Insufficient raw data | ticker={ticker}, rows={len(stock_data)}")
        return None

    df = prepare_dataframe(ticker, stock_data)
    if len(df) < MIN_ROWS:
        logger.warning(f"Insufficient cleaned data | ticker={ticker}, rows={len(df)}")
        return None

    close_prices = df['Close'].to_numpy(dtype=float)

    date_axis = build_date_axis(df, CHART_DATE_LABEL_INTERVAL)

    sr_lines, extrema_prices = support_resistance_lines(close_prices)

    y_values, lines_coords = predictions(df, STEP)

    return TickerResult(
        df=df,
        close=close_prices,
        date_axis=date_axis,
        y_values=y_values,
        lines_coords=lines_coords,
        sr_lines=sr_lines,
        extrema_prices=extrema_prices,
    )
