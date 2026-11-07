"""Week 2 exploratory data analysis and data quality report.

Run with:  python -m src.eda
Reads from data/sample by default. Point the data_dir argument at data/raw or
data/processed once real datasets are in place.
"""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from src.config import SAMPLE_DIR, REPORTS_DIR
from src.data_pipeline import load_csv
from src.data_quality import (check_date_coverage, check_value_ranges,
                              count_duplicates, profile_dataframe)


def to_md_table(df: pd.DataFrame) -> str:
    """Render a DataFrame as a Markdown table without extra dependencies."""
    cols = list(df.columns)
    lines = ["| " + " | ".join(map(str, cols)) + " |",
             "|" + "|".join(["---"] * len(cols)) + "|"]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(v) for v in row.values) + " |")
    return "\n".join(lines)


def run(data_dir=SAMPLE_DIR, out_dir=REPORTS_DIR) -> str:
    fig_dir = out_dir / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)

    weather = load_csv(data_dir / "weather_daily.csv", date_col="date")
    yields = pd.read_csv(data_dir / "yield_seasonal.csv")
    weather["year"] = weather["date"].dt.year

    sections = ["# Week 2 Data Quality and EDA Report", "",
                f"Source folder: `{data_dir.name}` (synthetic sample data unless stated otherwise).", ""]

    # 1. Profiling
    sections += ["## 1. Weather dataset profile", "", to_md_table(profile_dataframe(weather).round(3)), ""]
    sections += ["## 2. Yield dataset profile", "", to_md_table(profile_dataframe(yields).round(3)), ""]

    # 2. Duplicates and plausibility
    dup_w = count_duplicates(weather, ["date", "region"])
    dup_y = count_duplicates(yields, ["region", "year"])
    rng_w = check_value_ranges(weather, {"temp_c": (15, 40), "rain_mm": (0, 500)})
    rng_y = check_value_ranges(yields, {"yield_t_ha": (0.5, 12)})
    sections += ["## 3. Duplicates and plausibility checks", "",
                 f"- Duplicate weather rows (date, region): {dup_w}",
                 f"- Duplicate yield rows (region, year): {dup_y}",
                 f"- Out-of-range temperature values: {rng_w['temp_c']}",
                 f"- Out-of-range rainfall values: {rng_w['rain_mm']}",
                 f"- Out-of-range yield values: {rng_y['yield_t_ha']}", ""]

    # 3. Date coverage per region
    cov_rows = [{"region": region, **check_date_coverage(g["date"])}
                for region, g in weather.groupby("region")]
    sections += ["## 4. Date coverage by region", "", to_md_table(pd.DataFrame(cov_rows)), ""]

    # 4. Missingness
    miss = weather.groupby(["region", "year"])["temp_c"].apply(lambda s: s.isna().mean() * 100).reset_index()
    fig, ax = plt.subplots(figsize=(8, 4))
    for region, g in miss.groupby("region"):
        ax.plot(g["year"], g["temp_c"], marker="o", label=region)
    ax.set_title("Missing temperature readings per year (%)")
    ax.set_xlabel("Year"); ax.set_ylabel("Missing (%)"); ax.legend(); ax.grid(alpha=0.3)
    fig.tight_layout(); fig.savefig(fig_dir / "missing_temperature_by_year.png", dpi=120); plt.close(fig)
    sections += ["## 5. Missingness", "", "See `figures/missing_temperature_by_year.png`.", ""]

    # 5. Seasonality
    monthly = (weather.assign(month=weather["date"].dt.month)
               .groupby(["region", "month"])["rain_mm"].mean().reset_index())
    fig, ax = plt.subplots(figsize=(8, 4))
    for region, g in monthly.groupby("region"):
        ax.plot(g["month"], g["rain_mm"], marker="o", label=region)
    ax.set_title("Average daily rainfall by month (mm)")
    ax.set_xlabel("Month"); ax.set_ylabel("Rainfall (mm/day)"); ax.legend(); ax.grid(alpha=0.3)
    fig.tight_layout(); fig.savefig(fig_dir / "rainfall_seasonality.png", dpi=120); plt.close(fig)
    sections += ["## 6. Seasonality", "", "See `figures/rainfall_seasonality.png`.", ""]

    # 6. Relationship with yield
    corr_rain = yields["rain_total_mm"].corr(yields["yield_t_ha"])
    corr_temp = yields["temp_mean_c"].corr(yields["yield_t_ha"])
    fig, ax = plt.subplots(figsize=(6, 4))
    for region, g in yields.groupby("region"):
        ax.scatter(g["rain_total_mm"], g["yield_t_ha"], label=region)
    ax.set_title("Annual rainfall vs yield"); ax.set_xlabel("Annual rainfall (mm)")
    ax.set_ylabel("Yield (t/ha)"); ax.legend(); ax.grid(alpha=0.3)
    fig.tight_layout(); fig.savefig(fig_dir / "rainfall_vs_yield.png", dpi=120); plt.close(fig)
    sections += ["## 7. Relationship with yield", "",
                 f"- Pearson correlation, annual rainfall vs yield: {corr_rain:.3f}",
                 f"- Pearson correlation, mean temperature vs yield: {corr_temp:.3f}",
                 "- See `figures/rainfall_vs_yield.png`.", ""]

    report = "\n".join(sections)
    (out_dir / "week2_data_quality.md").write_text(report, encoding="utf-8")
    print(f"Report written to {out_dir / 'week2_data_quality.md'}")
    return report


if __name__ == "__main__":
    run()
