"""Project-wide paths and settings"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
OUT_DIR = PROJECT_ROOT / "figures"

PLOT_DATA = DATA_DIR / "plots_data.xlsx"
