"""
Shared look of all figures: colors and matplotlib defaults.

Importing this module applies the rcParams below, so every figure created
afterwards gets the same fonts, tick sizes and spines
"""

import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Colors
# ---------------------------------------------------------------------------

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

# Overlapping-circles diagram colors
OVERLAP_CIRCLE_COLORS = (
    COLORS["blue"],
    COLORS["orange"],
    COLORS["green"],
    COLORS["skyblue"],
    COLORS["dark-orange"],
)

# ---------------------------------------------------------------------------
# Matplotlib defaults
# ---------------------------------------------------------------------------

plt.rcParams.update(
    {
        "font.family": ["Arial", "Times New Roman"],
        # Tiles and axis labels
        "axes.titlesize": 14,
        "axes.titleweight": "bold",
        "axes.labelsize": 14,
        "axes.labelweight": "bold",
        # Axis lines: only bottom and left, thicker
        "axes.linewidth": 2,
        "axes.spines.top": False,
        "axes.spines.right": False,
        # Tick marks and tick labels
        "xtick.major.width": 2,
        "xtick.major.size": 6,
        "xtick.labelsize": 14,
        "ytick.major.width": 2,
        "ytick.major.size": 6,
        "ytick.labelsize": 14,
        # Legends
        "legend.fontsize": 12,
        "legend.frameon": False,
    }
)
