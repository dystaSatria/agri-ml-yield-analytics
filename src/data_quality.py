"""Data profiling and data quality checks."""
import pandas as pd


def profile_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Summarise each column: type, completeness, cardinality, and range for numeric columns."""
    rows = []
    for col in df.columns:
        s = df[col]
        row = {
            "column": col,
            "dtype": str(s.dtype),
            "non_null": int(s.notna().sum()),
            "missing_pct": round(float(s.isna().mean()) * 100, 2),
            "unique": int(s.nunique(dropna=True)),
        }
        if pd.api.types.is_numeric_dtype(s):
            row.update({"min": s.min(), "max": s.max(), "mean": round(float(s.mean()), 3)})
        rows.append(row)
    return pd.DataFrame(rows)


def check_date_coverage(dates: pd.Series, freq: str = "D") -> dict:
    """Report the observed date range and how many expected dates are missing."""
    d = pd.to_datetime(dates).drop_duplicates().sort_values()
    expected = pd.date_range(d.min(), d.max(), freq=freq)
    return {
        "start": d.min().date(),
        "end": d.max().date(),
        "expected": len(expected),
        "observed": len(d),
        "missing": len(expected.difference(d)),
    }


def count_duplicates(df: pd.DataFrame, subset: list[str]) -> int:
    """Count rows that duplicate an earlier row on the given key columns."""
    return int(df.duplicated(subset=subset).sum())


def check_value_ranges(df: pd.DataFrame, rules: dict[str, tuple[float, float]]) -> dict[str, int]:
    """Count values outside plausible (min, max) bounds for each column."""
    result = {}
    for col, (lo, hi) in rules.items():
        s = df[col].dropna()
        result[col] = int(((s < lo) | (s > hi)).sum())
    return result
