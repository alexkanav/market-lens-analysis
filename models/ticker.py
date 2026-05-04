from dataclasses import dataclass
import pandas as pd
import numpy as np


@dataclass
class TickerResult:
    df: pd.DataFrame
    close: np.ndarray
    date_axis: tuple[list[int], list[str]]
    y_values: list[list[float]]
    lines_coords: list[tuple[np.ndarray, np.ndarray]]
    sr_lines: np.ndarray
    extrema_prices: np.ndarray
