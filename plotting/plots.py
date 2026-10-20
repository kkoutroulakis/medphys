"""All registered plots"""

import numpy as np

from config import (
    BAR_CHART_DATA,
    BLAND_ALTMAN_CONFS,
    BLAND_ALTMAN_DATA,
    DOUBLE_BAR_CHART_COLORS,
    OUT_DIR,
    TRIPLE_BAR_CHART_COLORS,
)

from .diagrams import overlap_circles
from .helpers import bland_altman_plot, grouped_bar_chart, load_excel
from .registry import register


@register("bland-altman", "Bland-Altman plot for method comparison")
def run_bland_altman():
    sheet_name = BLAND_ALTMAN_CONFS["sheet_name"]
    value_cols = BLAND_ALTMAN_CONFS["value_cols"]
    structure = sheet_name.replace("_", " ").title()

    plot_data = load_excel(
        BLAND_ALTMAN_DATA,
        sheet_name=sheet_name,
        usecols=value_cols,
    )

    _, _, status = bland_altman_plot(
        plot_data[value_cols[0]],
        plot_data[value_cols[1]],
        title=BLAND_ALTMAN_CONFS["title"],
        xlabel=BLAND_ALTMAN_CONFS["xlabel"],
        ylabel=BLAND_ALTMAN_CONFS["ylabel"],
        xlim=(38, 58),
        xticks=np.arange(38, 59, 4),
        ylim=(-4, 6),
        yticks=np.arange(-4, 6.5, 2),
        save_path=OUT_DIR / "bland_altman" / f"{sheet_name}.jpg",
    )
    print(f"structure: {structure}\nstats: {status}")


@register("double-barchart", "Grouped bar chart with two data series")
def run_d_barchart():
    sheet_name = "double_bar_tumor"
    value_cols = ["SECT", "VM"]

    df = load_excel(BAR_CHART_DATA, sheet_name=sheet_name)

    grouped_bar_chart(
        df,
        value_cols=value_cols,
        labels=value_cols,
        colors=DOUBLE_BAR_CHART_COLORS,
        title="",
        xlabel="Αριθμός ασθενών",
        ylabel="Όγκος GTV (cm$^{3}$)",
        # ylim=(-2, 2),
        # yticks=np.arange(-2, 2, 0.5),
        save_path=OUT_DIR / "barcharts" / "tumor.jpg",
    )


@register("triple-barchart", "Grouped bar chart with three data series")
def run_t_barchart():
    sheet_name = "tripple_bar_chart"
    value_cols = ["VSECT", "VVM", "Vintersection"]

    df = load_excel(BAR_CHART_DATA, sheet_name=sheet_name)

    grouped_bar_chart(
        df,
        value_cols=value_cols,
        labels=[
            r"V$_{\mathrm{SECT}}$",
            r"V$_{\mathrm{VM}}$",
            r"V$_{\mathrm{intersection}}$",
        ],
        colors=TRIPLE_BAR_CHART_COLORS[: len(value_cols)],
        title="",
        xlabel="Patient No",
        ylabel=r"GTV Volume (cm$^{3}$)",
        ylim=(0, 180),
        yticks=np.arange(0, 181, 20),
        save_path=OUT_DIR / "barcharts" / "tripple_barchart.jpg",
    )


@register("circle-diagram", "Overlapping circles: V_SECT, V_VM and their intersection")
def run_circles_diagram():
    overlap_circles(
        legend_labels=[
            r"V$_{\mathrm{SECT}}$",
            r"V$_{\mathrm{VM}}$",
            r"V$_{\mathrm{intersection}}$",
            r"F$_{\mathrm{SECT}}$",
            r"F$_{\mathrm{VM}}$",
        ],
        save_path=OUT_DIR / "diagrams" / "overlapping_circles.jpg",
    )
