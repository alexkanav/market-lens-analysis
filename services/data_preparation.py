import pandas as pd


def prepare_dataframe(ticker: str, stock_data: pd.DataFrame) -> pd.DataFrame:
    df = stock_data.copy()

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df = df.reset_index(drop=False)
    df.columns = [col.capitalize() for col in df.columns]

    cols = ['Close', 'High', 'Low', 'Open']
    missing = set(cols) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing} in {ticker}")

    df[cols] = df[cols].apply(pd.to_numeric, errors='coerce')

    before = len(df)
    df = df.dropna(subset=cols)
    after = len(df)

    if before != after:
        print(f"{ticker}: dropped {before - after} rows due to NaNs")

    return df.sort_values("Date")
