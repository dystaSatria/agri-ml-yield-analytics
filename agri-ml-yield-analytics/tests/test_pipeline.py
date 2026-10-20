import pandas as pd

from src.data_pipeline import clean_daily_weather, remove_outliers_iqr, time_split


def test_clean_daily_weather_fills_gaps_and_removes_duplicates():
    df = pd.DataFrame({
        "date": ["2024-01-01", "2024-01-02", "2024-01-02", "2024-01-03"],
        "temp_c": [25.0, None, 27.0, 29.0],
    })
    out = clean_daily_weather(df)
    assert len(out) == 3
    assert out["temp_c"].isna().sum() == 0


def test_remove_outliers_iqr_drops_extreme_value():
    df = pd.DataFrame({"x": [1, 2, 3, 2, 1, 2, 3, 1000]})
    out = remove_outliers_iqr(df, ["x"])
    assert 1000 not in out["x"].values


def test_time_split_has_no_overlap():
    df = pd.DataFrame({"date": pd.date_range("2020-01-01", periods=10, freq="D"), "v": range(10)})
    train, test = time_split(df, "date", "2020-01-06")
    assert train["date"].max() < test["date"].min()
    assert len(train) + len(test) == len(df)
