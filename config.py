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
# Typography
# ---------------------------------------------------------------------------

AXIS_STYLES = {
    "fontsize": 14,
    "fontweight": "bold",
    "tick_fontsize": 14,
    "tick_width": 2,
    "tick_length": 6,
    "spine_linewidth": 2,
    "hide_top_spine": True,
    "hide_right_spine": True,
    "legend": 12,
}

# ---------------------------------------------------------------------------
# Colors
# ---------------------------------------------------------------------------

# General plotting colors
COLORS = {
    "blue": "tab:blue",
    "orange": "tab:orange",
    "green": "tab:green",
    "tomato": "tab:red",
    "purple": "tab:purple",
    "gray": "tab:grey",
    "red": "red",
    "black": "black",
    "darkred": "#910000",
    "lightgrey": "#b8b8b8",
    "skyblue": "#33a8de",
    "dark-orange": "#faa805",
}

# Grouped bar chart colors
DOUBLE_BAR_CHART_COLORS = [COLORS["lightgrey"], COLORS["darkred"]]
TRIPLE_BAR_CHART_COLORS = [COLORS["blue"], COLORS["orange"], COLORS["green"]]

# Overlapping-circles diagram colors
OVERLAP_CIRCLE_COLORS = (
    COLORS["blue"],
    COLORS["orange"],
    COLORS["green"],
    COLORS["skyblue"],
    COLORS["dark-orange"],
)
