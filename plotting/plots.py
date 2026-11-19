"""All registered plots. Each run_* function holds the settings of its figure."""

import numpy as np

from config import BAR_CHART_DATA, BLAND_ALTMAN_DATA, OUT_DIR

from .diagrams import LEGEND_STYLES, overlap_circles
from .helpers import bland_altman_plot, grouped_bar_chart, load_excel
from .registry import register
from .structures import BA_STRUCTURES
from .style import COLORS

# ---------------------------------------------------------------------------
# Bland-Altman
# ---------------------------------------------------------------------------


@register(
    "bland-altman",
    "Bland-Altman plot for method comparison",
    options=tuple(BA_STRUCTURES),
    option_required=True,
)
def run_bland_altman(structure):
    value_cols = ["VMAT_REF", "VMAT_Arc1"]

    plot_data = load_excel(
        BLAND_ALTMAN_DATA,
        sheet_name=structure,
        usecols=value_cols,
    )

    _, _, status = bland_altman_plot(
        plot_data[value_cols[0]],
        plot_data[value_cols[1]],
        save_path=OUT_DIR / "bland_altman" / f"ba-{structure}.jpg",
        **BA_STRUCTURES[structure],
    )
    print(f"structure: {structure.replace('_', ' ').title()}\nstats: {status}")


# ---------------------------------------------------------------------------
# Grouped bar charts
# ---------------------------------------------------------------------------


@register("double-barchart", "Grouped bar chart with two data series")
def run_d_barchart():
    df = load_excel(BAR_CHART_DATA, sheet_name="f_plot")

    grouped_bar_chart(
        df,
        value_cols=["FSECT", "FVM"],
        labels=[
            r"F$_{\mathbf{SECT}}$",
            r"F$_{\mathbf{VM}}$",
        ],
        colors=[COLORS["blue"], COLORS["orange"]],
        title=None,
        xlabel="Patient No",
        ylabel=r"GTV Non-overlap Fraction (%)",
        ylim=(0, 60),
        yticks=np.arange(0, 65, 10),
        save_path=OUT_DIR / "barcharts" / "fsect_fvm.jpg",
    )


@register("triple-barchart", "Grouped bar chart with three data series")
def run_t_barchart():
    df = load_excel(BAR_CHART_DATA, sheet_name="tripple_bar_chart")

    grouped_bar_chart(
        df,
        value_cols=["VSECT", "VVM", "Vintersection"],
        labels=[
            r"V$_{\mathrm{SECT}}$",
            r"V$_{\mathrm{VM}}$",
            r"V$_{\mathrm{intersection}}$",
        ],
        colors=[COLORS["blue"], COLORS["orange"], COLORS["green"]],
        title=None,
        xlabel="Patient No",
        ylabel=r"GTV Volume (cm$^{3}$)",
        ylim=(0, 180),
        yticks=np.arange(0, 181, 20),
        save_path=OUT_DIR / "barcharts" / "tripple_barchart.jpg",
    )


# ---------------------------------------------------------------------------
# Grouped bar charts
# ---------------------------------------------------------------------------


@register("circle-diagram", "Overlapping circles diagram", options=LEGEND_STYLES)
def run_circles_diagram(legend_style="shape"):
    overlap_circles(
        legend_labels=[
            r"V$_{\mathrm{SECT}}$",
            r"V$_{\mathrm{VM}}$",
            r"V$_{\mathrm{INT}}$",
            r"F$_{\mathrm{SECT}}$",
            r"F$_{\mathrm{VM}}$",
        ],
        legend_style=legend_style,
        save_path=OUT_DIR / "diagrams" / f"overlapping_circles_{legend_style}.jpg",
    )
