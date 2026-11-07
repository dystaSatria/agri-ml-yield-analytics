---
title: "Week 2 – Data Understanding and Source Inventory"
subtitle: "Machine Learning Data Analysis Project for Agriculture and Agribusiness"
---

**Intern:** ____________________ **Programme:** Junior Machine Learning Data Analyst – Agriculture & Agribusiness
**Week:** 2 of 4 **Repository:** https://github.com/<your-username>/agri-ml-yield-analytics

# 1. Purpose of Week 2

Week 1 defined what the project should answer. Week 2 checks whether the data needed to answer it exists, can be accessed, and is good enough to use. The main outputs are:

1. A **source inventory** listing every candidate dataset, its provider, licence, coverage, and access status.
2. A **data dictionary** describing the variables we expect to use in the yield, disease, and price models.
3. An **initial data quality assessment** covering completeness, consistency, duplicates, value plausibility, and temporal coverage.
4. **Exploratory data analysis (EDA)** to find early patterns, seasonality, and relationships that inform feature design in Week 3.
5. A list of **data risks and open questions** that feed back into the Week 1 risk register.

# 2. Approach

The work followed the data understanding phase of CRISP-DM (Shearer, 2000). Each dataset was reviewed against four questions: Is it relevant to an objective in Week 1? Can we legally and practically obtain it? What does it contain and how reliable is it? What must be fixed before modelling?

The repository contains a reproducible EDA pipeline (`src/eda.py`) and data quality functions (`src/data_quality.py`). Because real datasets must be downloaded and checked for licence terms first, the quality checks in this report were run on the **synthetic sample dataset** (`data/sample/`). The same script runs unchanged on real data once it is placed in `data/raw/`, so the results below demonstrate the method and will be replaced with real findings in Week 3.

# 3. Source Inventory

The inventory is maintained in `data/catalogue.csv`. A summary is below.

| ID | Dataset | Provider | Licence (summary) | Coverage | Access status | Role |
|----|---------|----------|-------------------|----------|---------------|------|
| DS01 | Sentinel-2 L2A imagery | Copernicus (ESA) | Free and open | 2015 onward, 10–60 m, ~5-day revisit | Account and API access to confirm | NDVI, EVI for yield model |
| DS02 | Daily meteorological data | NASA POWER | Open, cite source | 1981 onward, 0.5° grid, daily | Public API, no registration | Rainfall, temperature features |
| DS03 | Crop production statistics | BPS Indonesia | Open data, cite source | Annual, district level | Manual download; check target crop tables | Yield labels |
| DS04 | Crop production statistics (global) | FAOSTAT | Open data | Annual, country level | Public bulk download | Cross-check of yield labels |
| DS05 | PlantVillage leaf images | PlantVillage / Hughes & Salathé (2015) | Open access; verify repository licence | Lab-captured images | Public download | Disease classification |
| DS06 | Commodity price panels | Government food price portals | To be confirmed | To be confirmed | Source selection pending | Price forecasting |

## 3.1 Assessment

- **Yield labels (DS03, DS04)** are the most critical dependency. District-level BPS data is the most relevant for our pilot regions, but tables must be checked for the target commodity, unit consistency (dry versus wet grain, hectares versus area harvested), and revisions between editions.
- **Weather (DS02)** is the most accessible source and can be integrated first. Its 0.5° resolution is coarse, so regional averages must be computed carefully and the limitation stated in the final report.
- **Satellite imagery (DS01)** requires cloud masking and significant storage. Its access process must be confirmed early because it is a dependency for the yield model.
- **Disease images (DS05)** are lab-captured and may not represent field photos. This confirms risk R6 from Week 1.
- **Price data (DS06)** has no source selected yet. Finding a reliable, machine-readable price series is an open action for Week 3 and a new risk (R11, below).

# 4. Data Dictionary (Planned Variables)

The following variables are expected in the integrated dataset. Units and valid ranges are proposed for validation purposes and will be confirmed against source documentation.

| Variable | Description | Unit | Source | Expected range |
|----------|-------------|------|--------|----------------|
| `date` | Observation date | YYYY-MM-DD | DS02 | 1981 onward |
| `region` | Pilot region identifier | Text | All | Fixed list |
| `temp_c` | Daily mean temperature | °C | DS02 | 15–40 |
| `rain_mm` | Daily precipitation | mm/day | DS02 | 0–500 |
| `ndvi` | Normalised difference vegetation index | Index | DS01 | −1 to 1 |
| `rain_total_mm` | Seasonal rainfall total | mm | Derived | 0–3000 |
| `temp_mean_c` | Seasonal mean temperature | °C | Derived | 15–40 |
| `yield_t_ha` | Harvested yield | t/ha | DS03 / DS04 | 0.5–12 |
| `disease_label` | Leaf condition class | Category | DS05 | Defined class list |
| `price_idr_kg` | Commodity price | IDR/kg | DS06 | To be confirmed |

# 5. Data Quality Assessment

The assessment below was run on the synthetic sample dataset to validate the method. Full output is in `reports/week2_data_quality.md`.

## 5.1 Completeness

- **Weather data:** 7,306 records across two regions and ten years. Temperature has 2.09% missing values; rainfall has none. Missing values are spread across all years rather than concentrated in one period.
- **Yield data:** 20 region-season records with no missing values.

## 5.2 Consistency and Uniqueness

- No duplicate records were found for the date–region key in the weather data, or for the region–year key in the yield data.
- Date coverage is complete for both regions: 3,653 expected days, 3,653 observed days, with no gaps.

## 5.3 Plausibility

- All temperature values fall between 15 °C and 40 °C (observed range 21.7–32.0 °C).
- All rainfall values are non-negative (observed range 0–54.3 mm/day).
- All yield values fall between 0.5 and 12 t/ha (observed range 5.5–7.2 t/ha).

## 5.4 Interpretation

The sample dataset passes all checks, which is expected for synthetic data. Real datasets are likely to contain problems that the synthetic data does not, such as district boundary changes, missing years for some districts, revised statistics, and sensor gaps in weather records. Week 3 must test for these explicitly.

# 6. Exploratory Data Analysis

## 6.1 Missing Temperature Readings

Missingness is spread across years and regions (see `reports/figures/missing_temperature_by_year.png`). This pattern is consistent with random gaps, which can be handled with time-based interpolation. Systematic gaps in real data would need separate treatment.

## 6.2 Rainfall Seasonality

Average daily rainfall follows a clear annual cycle in both regions (see `reports/figures/rainfall_seasonality.png`). This confirms that seasonal aggregation, and features aligned with the growing season, are important for the yield model.

## 6.3 Relationship with Yield

- Correlation between annual rainfall and yield: **0.29**.
- Correlation between mean temperature and yield: **0.23**.

Both correlations are weak. In the synthetic data, yield was generated from rainfall and temperature with random noise, so a weak correlation is expected when noise is large relative to the signal. For real data, weak linear correlation does not mean weak predictability: non-linear effects, timing within the season, and satellite-derived vegetation indices are likely to explain more variation. The correlations will be re-estimated with real data in Week 3, and this section will be updated.

# 7. Data Risks and Open Questions

| ID | Risk or question | Impact | Action | Owner | Due |
|----|------------------|--------|--------|-------|-----|
| R1 (updated) | BPS yield tables may have inconsistent units or missing districts | High | Download all editions; document units; build a district mapping table | Intern | Week 3 |
| R12 | Sentinel-2 API access may require account approval | High | Register early; prepare a fallback using a pre-processed NDVI product | Intern | Week 2 |
| R11 | No price series identified yet (DS06) | Medium | List three candidate sources and test machine-readability | Intern | Week 3 |
| R13 | NASA POWER grid resolution may not match district boundaries | Medium | Map district centroids to the nearest grid point; test sensitivity | Intern | Week 3 |
| Q1 | Which commodity is the pilot focus (for example rice or maize)? | High | Confirm with mentor; this determines DS03 table selection | Mentor | Week 2 |
| Q2 | Are the pilot regions fixed? | High | Propose two regions with complete yield records | Intern and mentor | Week 2 |

# 8. Next Steps (Week 3)

1. Confirm the commodity and pilot regions (Q1, Q2).
2. Register for Sentinel-2 access and download NASA POWER data for the pilot regions.
3. Download BPS yield tables and build a cleaned yield dataset with a units check.
4. Run `src/eda.py` on the real processed data and update this report.
5. Select a price data source (DS06).

# 9. Conclusion

Week 2 confirmed that the project's main data needs can be met mostly with open sources. Weather data is readily available. Yield labels are available but need careful cleaning. Satellite imagery and price data require access steps that must start early. The EDA pipeline is ready and tested, and it will be applied to real data in Week 3. The primary risks are yield label quality and the availability of a price series.

# References

Copernicus Programme, European Space Agency. *Sentinel-2 mission documentation*. https://sentinels.copernicus.org

Hughes, D. P., & Salathé, M. (2015). An open access repository of images on plant health to enable the development of mobile disease diagnostics. *arXiv preprint arXiv:1511.08060*.

NASA Prediction Of Worldwide Energy Resources (POWER) Project. https://power.larc.nasa.gov

Shearer, C. (2000). The CRISP-DM model: The new blueprint for data mining. *Journal of Data Warehousing, 5*(4), 13–22.
