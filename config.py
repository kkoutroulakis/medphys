"""Project-wide paths"""

from pathlib import Path

PROJECT_DIR = Path(__file__).parent

DATA_DIR = PROJECT_DIR / "data"
OUT_DIR = PROJECT_DIR / "figures"

BLAND_ALTMAN_DATA = DATA_DIR / "bland_altman_data.xlsx"
BAR_CHART_DATA = DATA_DIR / "bar_charts_data.xlsx"
