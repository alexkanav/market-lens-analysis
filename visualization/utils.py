import pandas as pd


def build_date_axis(df: pd.DataFrame, interval: int) -> tuple[list[int], list[str]]:
    if 'Date' not in df.columns:
        raise ValueError("DataFrame must contain 'Date' column")

    date_series = pd.to_datetime(df['Date'])
    date_list = date_series.dt.strftime('%m-%d').tolist()
    interval = max(1, interval)
    x = list(range(0, len(date_list), interval))
    y = date_list[::interval]

    return x, y
