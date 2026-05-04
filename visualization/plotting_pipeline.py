import logging

from visualization.chart import draw_turning_points, draw_candle_chart, draw_line_chart
from models.ticker import TickerResult
from config import LINE_STYLES, UP_COLOR, DOWN_COLOR

logger = logging.getLogger(__name__)


def visualize_ticker(
        ticker_name: str,
        ticker_data: TickerResult,
        show_turning=True,
        show_candles=True,
        show_trends=True,
) -> None:
    if show_turning:
        try:
            draw_turning_points(
                ticker_name,
                ticker_data.close,
                ticker_data.extrema_prices
            )
        except Exception:
            logger.exception(f"Turning points failed | ticker={ticker_name}")

    if show_candles:
        try:
            draw_candle_chart(
                ticker_name,
                ticker_data.df,
                ticker_data.sr_lines,
                UP_COLOR,
                DOWN_COLOR,
                ticker_data.date_axis
            )
        except Exception:
            logger.exception(f"Candle chart failed | ticker={ticker_name}")

    if show_trends:
        try:
            draw_line_chart(
                ticker_name,
                ticker_data.df,
                ticker_data.close,
                ticker_data.lines_coords,
                ticker_data.date_axis,
                LINE_STYLES
            )
        except Exception:
            logger.exception(f"Line chart failed | ticker={ticker_name}")
