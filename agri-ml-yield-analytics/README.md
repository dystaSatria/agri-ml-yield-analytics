# Agriculture & Agribusiness Machine Learning Data Analytics

Junior Machine Learning Data Analyst internship project (20 Oct 2026 – 17 Nov 2026).

This repository contains the strategic plan, data pipeline, KPI evaluation utilities, and tests for a machine learning project focused on agriculture and agribusiness. The project covers three analytical goals:

1. **Crop yield prediction** from weather data and satellite-derived vegetation indices.
2. **Early plant disease detection** from leaf images (image classification).
3. **Short-term commodity price forecasting** to support sales planning.

## Status

| Week | Task | Status |
|------|------|--------|
| 1 | Strategic Design and Planning | Completed (see `docs/`) |
| 2 | Data Understanding and Source Inventory | Planned |
| 3 | Data Preparation and Integration | Planned |
| 4 | Modelling, Evaluation, and Reporting | Planned |

## Repository structure

```
.
├── README.md
├── LICENSE
├── requirements.txt
├── docs/
│   ├── Week1_Strategic_Plan.md      # Strategy document (English)
│   └── Week1_Strategic_Plan.docx    # Same document in Word format
├── src/
│   ├── config.py                    # Paths, random seed, KPI targets
│   ├── data_pipeline.py             # Loading, cleaning, outlier removal, time split
│   ├── kpi.py                       # MAPE, R², and KPI target checks
│   └── generate_sample_data.py      # Synthetic data for testing the pipeline
├── tests/
│   ├── test_kpi.py
│   └── test_pipeline.py
├── data/
│   ├── README.md                    # Data sources and licensing notes
│   ├── raw/                         # Original data (not versioned)
│   ├── processed/                   # Cleaned data (not versioned)
│   └── sample/                      # Small synthetic dataset (versioned)
├── notebooks/                       # Exploratory analysis (Week 2 onward)
└── reports/                         # Generated figures and results
```

## Getting started

Requirements: Python 3.10 or newer.

```bash
git clone https://github.com/<your-username>/agri-ml-yield-analytics.git
cd agri-ml-yield-analytics
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Generate the synthetic sample data and run the tests:

```bash
python -m src.generate_sample_data
python -m pytest -q
```

## KPI targets

| KPI | Target |
|-----|--------|
| Yield model R² | ≥ 0.70 |
| Yield model MAPE | ≤ 15% |
| Disease classifier accuracy | ≥ 90% |
| Disease classifier macro F1 | ≥ 0.85 |
| 4-week price forecast MAPE | ≤ 10% |

The targets are defined in `src/config.py` and the full rationale is in `docs/Week1_Strategic_Plan.md`.

## Data

Real datasets are not committed to this repository. Sources, licences, and access instructions are listed in `data/README.md`. The files in `data/sample/` are synthetic and exist only to test the pipeline.

## Methodology

The project follows the CRISP-DM framework (business understanding, data understanding, data preparation, modelling, evaluation, deployment). Validation uses time-based splits and region-grouped cross-validation to avoid data leakage and to test generalisation to unseen regions.

## License

MIT. See `LICENSE`.
