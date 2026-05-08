import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock


@pytest.fixture
def mock_service():
    return Mock()


@pytest.fixture
def trend_df() -> pd.DataFrame:
    return pd.DataFrame({
        "Open": np.arange(200),
        "Close": np.arange(200),
    })


@pytest.fixture
def make_ohlc_df():
    def _create(**overrides) -> pd.DataFrame:
        defaults = {
            "Date": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"],
            "Open": [1, 2, 3, 4, 5],
            "High": [2, 3, 4, 5, 6],
            "Low": [0.5, 1.5, 2.5, 3.5, 4.5],
            "Close": [1.5, 2.5, 3.5, 4.5, 5.5],
        }

        return pd.DataFrame({**defaults, **overrides})

    return _create
