"""Project-wide paths and settings"""

from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

PROJECT_DIR = Path(__file__).parent

DATA_DIR = PROJECT_DIR / "data"
OUT_DIR = PROJECT_DIR / "figures"

BLAND_ALTMAN_DATA = DATA_DIR / "bland_altman_data.xlsx"
BAR_CHART_DATA = DATA_DIR / "bar_charts_data.xlsx"


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
