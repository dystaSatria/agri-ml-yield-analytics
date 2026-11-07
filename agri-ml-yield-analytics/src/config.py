"""Central configuration: paths, random seed, and KPI targets."""
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
SAMPLE_DIR = DATA_DIR / "sample"
REPORTS_DIR = PROJECT_ROOT / "reports"

RANDOM_SEED = 42

# Target KPIs defined in the Week 1 strategic plan (docs/Week1_Strategic_Plan.md)
KPI_TARGETS = {
    "yield_r2_min": 0.70,          # crop yield model, R^2 at least
    "yield_mape_max": 15.0,        # crop yield model, MAPE in percent at most
    "disease_accuracy_min": 0.90,  # disease classifier, accuracy at least
    "disease_macro_f1_min": 0.85,  # disease classifier, macro F1 at least
    "price_mape_4w_max": 10.0,     # 4-week price forecast, MAPE in percent at most
}
