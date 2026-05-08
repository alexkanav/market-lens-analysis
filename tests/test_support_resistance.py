import numpy as np

from analysis.support_resistance import support_resistance_lines


def test_support_resistance_lines__flat_prices__returns_empty_arrays():
    prices = np.array([100, 100, 100, 100])
    levels, ext = support_resistance_lines(prices)

    assert levels.size == 0
    assert ext.size == 0


def test_support_resistance_lines__wave_pattern__returns_detected_extrema():
    prices = np.array([1, 2, 1, 2, 1, 2, 1])
    levels, ext = support_resistance_lines(prices)

    assert ext.size > 0
    assert levels.ndim == 2  # because reshape(-1,1)
    assert levels.shape[1] == 1


def test_support_resistance_lines__valid_prices__returns_numpy_arrays():
    prices = np.array([1, 3, 2, 4, 3, 5, 2])
    levels, ext = support_resistance_lines(prices)

    assert isinstance(levels, np.ndarray)
    assert isinstance(ext, np.ndarray)


def test_support_resistance_lines__valid_levels__stay_within_price_bounds():
    prices = np.array([10, 20, 15, 25, 10])
    levels, _ = support_resistance_lines(prices)

    if levels.size > 0:
        assert levels.min() >= prices.min()
        assert levels.max() <= prices.max()


def test_support_resistance_lines__alternating_peaks__detects_extrema():
    prices = np.array([1, 3, 1, 3, 1])
    _, ext = support_resistance_lines(prices)

    assert len(ext) >= 2  # should detect peaks and troughs


def test_support_resistance_lines__empty_prices__returns_empty_arrays():
    prices = np.array([])

    levels, ext = support_resistance_lines(prices)

    assert levels.size == 0
    assert ext.size == 0
