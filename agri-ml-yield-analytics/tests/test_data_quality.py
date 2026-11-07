import pandas as pd

from src.data_quality import profile_dataframe, check_date_coverage, count_duplicates, check_value_ranges


def test_profile_reports_missing_pct():
    df = pd.DataFrame({"a": [1.0, None, 3.0, 4.0]})
    prof = profile_dataframe(df).set_index("column")
    assert prof.loc["a", "missing_pct"] == 25.0


def test_check_date_coverage_detects_gap():
    dates = pd.Series(["2024-01-01", "2024-01-02", "2024-01-04"])
    cov = check_date_coverage(dates)
    assert cov["expected"] == 4 and cov["observed"] == 3 and cov["missing"] == 1


def test_count_duplicates():
    df = pd.DataFrame({"k": [1, 1, 2], "v": [5, 6, 7]})
    assert count_duplicates(df, ["k"]) == 1


def test_check_value_ranges():
    df = pd.DataFrame({"t": [20, 50, 30, -5]})
    assert check_value_ranges(df, {"t": (0, 40)}) == {"t": 2}
