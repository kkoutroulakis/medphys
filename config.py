"""Project-wide paths and settings"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
OUT_DIR = PROJECT_ROOT / "figures"

PLOT_DATA = DATA_DIR / "plots_data.xlsx"

# ---------------------------------------------------------------------------
# Colors
# ---------------------------------------------------------------------------

# General plotting colors
COLORS = {
    "blue": "tab:blue",
    "orange": "tab:orange",
    "green": "tab:green",
    "red": "tab:red",
    "purple": "tab:purple",
    "gray": "tab:grey",
}

# Grouped bar chart colors
BAR_CHART_COLORS = [COLORS["blue"], COLORS["orange"], COLORS["green"]]

# Overlapping-circles diagram colors
OVERLAP_CIRCLE_COLORS = (
    COLORS["blue"],
    COLORS["orange"],
    COLORS["green"],
    "#33a8de",
    "#faa805",
)
