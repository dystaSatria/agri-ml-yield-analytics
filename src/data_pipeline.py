"""Data loading, cleaning, and time-based splitting utilities."""
import pandas as pd


def load_csv(path, date_col: str | None = None) -> pd.DataFrame:
    """Load a CSV file and optionally parse and sort by a date column."""
    df = pd.read_csv(path)
    if date_col is not None:
        df[date_col] = pd.to_datetime(df[date_col])
        df = df.sort_values(date_col).reset_index(drop=True)
    return df


def clean_daily_weather(df: pd.DataFrame, date_col: str = "date") -> pd.DataFrame:
    """Remove duplicate dates and fill numeric gaps by time-based interpolation.

    Expects a single region per call; group by region before calling if needed.
    """
    out = df.drop_duplicates(subset=date_col).copy()
    out[date_col] = pd.to_datetime(out[date_col])
    out = out.set_index(date_col).sort_index()
    numeric_cols = out.select_dtypes("number").columns
    out[numeric_cols] = out[numeric_cols].interpolate(method="time", limit_direction="both")
    return out.reset_index()


def remove_outliers_iqr(df: pd.DataFrame, cols: list[str], k: float = 1.5) -> pd.DataFrame:
    """Drop rows whose values fall outside the IQR fence for any of the given columns."""
    out = df
    for col in cols:
        q1, q3 = out[col].quantile([0.25, 0.75])
        iqr = q3 - q1
        keep = out[col].between(q1 - k * iqr, q3 + k * iqr) | out[col].isna()
        out = out[keep]
    return out


def time_split(df: pd.DataFrame, date_col: str, cutoff) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split by time to avoid data leakage from the future into training data."""
    cutoff = pd.to_datetime(cutoff)
    train = df[df[date_col] < cutoff]
    test = df[df[date_col] >= cutoff]
    return train, test
