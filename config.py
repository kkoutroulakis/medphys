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
TRIPLE_BAR_CHART_COLORS = [COLORS["blue"], COLORS["orange"], COLORS["green"]]

# Overlapping-circles diagram colors
OVERLAP_CIRCLE_COLORS = (
    COLORS["blue"],
    COLORS["orange"],
    COLORS["green"],
    COLORS["skyblue"],
    COLORS["dark-orange"],
)

# ---------------------------------------------------------------------------
# Plots
# ---------------------------------------------------------------------------

BLAND_ALTMAN_CONFS = {
    "sheet_name": "brain_stem",
    "value_cols": ["VMAT_REF", "VMAT_Arc1"],
    "title": r"VMAT$_{\mathbf{Ref}}$ - VMAT$_{\mathbf{Arc1}}$",
    "xlabel": r"Μέσος όρος D$_{\mathbf{max}}$ (Gy)",
    "ylabel": r"Εγκεφαλικό στέλεχος: Διαφορά D$_{\mathbf{max}}$ (Gy)",
    "xlim": None,
    "ylim": None,
    "xticks": None,
    "yticks": None,
    "show_loa_labels": True,
}

DOUBLE_BAR_CHART_CONFS = {
    "sheet_name": "f_plot",
    "value_cols": ["FSECT", "FVM"],
    "legends": [
        r"F$_{\mathbf{SECT}}$",
        r"F$_{\mathbf{VM}}$",
    ],
    "colors": [COLORS["blue"], COLORS["orange"]],
    "title": None,
    "xlabel": "Patient No",
    "ylabel": r"GTV Non-overlap Fraction (%)",
    "file_name": "fsect_fvm.jpg",
}
