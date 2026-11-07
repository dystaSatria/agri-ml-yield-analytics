# Week 2 Data Quality and EDA Report

Source folder: `sample` (synthetic sample data unless stated otherwise).

## 1. Weather dataset profile

| column | dtype | non_null | missing_pct | unique | min | max | mean |
|---|---|---|---|---|---|---|---|
| date | datetime64[us] | 7306 | 0.0 | 3653 | nan | nan | nan |
| region | str | 7306 | 0.0 | 2 | nan | nan | nan |
| temp_c | float64 | 7153 | 2.09 | 810 | 21.72 | 32.0 | 27.012 |
| rain_mm | float64 | 7306 | 0.0 | 1185 | 0.0 | 54.33 | 2.388 |
| year | int32 | 7306 | 0.0 | 10 | 2016.0 | 2025.0 | 2020.5 |

## 2. Yield dataset profile

| column | dtype | non_null | missing_pct | unique | min | max | mean |
|---|---|---|---|---|---|---|---|
| region | str | 20 | 0.0 | 2 | nan | nan | nan |
| year | int64 | 20 | 0.0 | 10 | 2016.0 | 2025.0 | 2020.5 |
| rain_total_mm | float64 | 20 | 0.0 | 20 | 741.7 | 1035.1 | 872.5 |
| temp_mean_c | float64 | 20 | 0.0 | 15 | 26.84 | 27.11 | 27.012 |
| yield_t_ha | float64 | 20 | 0.0 | 18 | 5.5 | 7.19 | 6.403 |

## 3. Duplicates and plausibility checks

- Duplicate weather rows (date, region): 0
- Duplicate yield rows (region, year): 0
- Out-of-range temperature values: 0
- Out-of-range rainfall values: 0
- Out-of-range yield values: 0

## 4. Date coverage by region

| region | start | end | expected | observed | missing |
|---|---|---|---|---|---|
| region_A | 2016-01-01 | 2025-12-31 | 3653 | 3653 | 0 |
| region_B | 2016-01-01 | 2025-12-31 | 3653 | 3653 | 0 |

## 5. Missingness

See `figures/missing_temperature_by_year.png`.

## 6. Seasonality

See `figures/rainfall_seasonality.png`.

## 7. Relationship with yield

- Pearson correlation, annual rainfall vs yield: 0.290
- Pearson correlation, mean temperature vs yield: 0.233
- See `figures/rainfall_vs_yield.png`.
