"""Generate a small SYNTHETIC dataset to test the pipeline end to end.

The output is not real agricultural data. Replace it with data from the
sources listed in data/README.md once they have been collected.

Run with:  python -m src.generate_sample_data
"""
import numpy as np
import pandas as pd

from src.config import RANDOM_SEED, SAMPLE_DIR


def main() -> None:
    rng = np.random.default_rng(RANDOM_SEED)
    SAMPLE_DIR.mkdir(parents=True, exist_ok=True)

    dates = pd.date_range("2016-01-01", "2025-12-31", freq="D")
    regions = ["region_A", "region_B"]

    weather_frames = []
    for region in regions:
        doy = dates.dayofyear.to_numpy()
        temp = 27 + 2 * np.sin(2 * np.pi * doy / 365) + rng.normal(0, 1, len(dates))
        rain = rng.gamma(0.4, 6, len(dates)) * (1 + 0.8 * np.sin(2 * np.pi * (doy - 300) / 365))
        frame = pd.DataFrame({
            "date": dates,
            "region": region,
            "temp_c": temp.round(2),
            "rain_mm": np.clip(rain, 0, None).round(2),
        })
        missing = rng.random(len(frame)) < 0.02  # inject 2% missing temperatures
        frame.loc[missing, "temp_c"] = np.nan
        weather_frames.append(frame)
    weather = pd.concat(weather_frames, ignore_index=True)
    weather.to_csv(SAMPLE_DIR / "weather_daily.csv", index=False)

    yield_rows = []
    for region in regions:
        base = 5.0 + (0.5 if region == "region_B" else 0.0)
        for year in range(2016, 2026):
            w = weather[(weather["region"] == region) & (pd.to_datetime(weather["date"]).dt.year == year)]
            rain_total = w["rain_mm"].sum()
            temp_mean = w["temp_c"].mean()
            yield_t_ha = base + 0.0015 * rain_total - 0.1 * abs(temp_mean - 27) + rng.normal(0, 0.3)
            yield_rows.append({"region": region, "year": year,
                               "rain_total_mm": round(rain_total, 1),
                               "temp_mean_c": round(temp_mean, 2),
                               "yield_t_ha": round(max(yield_t_ha, 0.5), 2)})
    pd.DataFrame(yield_rows).to_csv(SAMPLE_DIR / "yield_seasonal.csv", index=False)
    print(f"Wrote synthetic sample data to {SAMPLE_DIR}")


if __name__ == "__main__":
    main()
