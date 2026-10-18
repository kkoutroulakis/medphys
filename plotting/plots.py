"""All registered plots"""

import numpy as np

from config import OUT_DIR, PLOT_DATA

from .diagrams import overlap_circles
from .helpers import bland_altman_plot, grouped_bar_chart, load_excel
from .registry import register


@register("bland-altman", "Bland-Altman plot for method comparison")
def run_bland_altman():
    sheet_name = "tumor"
    value_cols = ["VMAT_REF", "VMAT_SW0.5cm"]
    structure = sheet_name.replace("_", " ").title()

    plot_data = load_excel(
        PLOT_DATA,
        sheet_name=sheet_name,
        usecols=value_cols,
    )

    _, _, status = bland_altman_plot(
        plot_data[value_cols[0]],
        plot_data[value_cols[1]],
        xlabel="HU Average",
        ylabel=f"{structure}: HU Difference",
        save_path=OUT_DIR / "bland_altman" / f"{sheet_name}_bland_altman.jpg",
    )
    print(f"structure: {structure}\nstats: {status}")


@register("double-barchart", "Grouped bar chart with two data series")
def run_d_barchart():
    sheet_name = "double_bar_chart"
    value_cols = ["<10 HU", "<15 HU"]

    df = load_excel(PLOT_DATA, sheet_name=sheet_name)

    grouped_bar_chart(
        df,
        value_cols=value_cols,
        labels=value_cols,
        colors=["tab:blue", "tab:orange"],
        title="",
        xlabel="",
        ylabel="",
        ylim=(-2, 2),
        yticks=np.arange(-2, 2, 0.5),
        save_path=OUT_DIR / "barcharts" / "hu_diff_barchart.jpg",
    )


@register("triple-barchart", "Grouped bar chart with three data series")
def run_t_barchart():
    sheet_name = "tripple_bar_chart"
    value_cols = ["VSECT", "VVM", "Vintersection"]

    df = load_excel(PLOT_DATA, sheet_name=sheet_name)

    grouped_bar_chart(
        df,
        value_cols=value_cols,
        labels=[
            r"V$_{\mathrm{SECT}}$",
            r"V$_{\mathrm{VM}}$",
            r"V$_{\mathrm{intersection}}$",
        ],
        colors=["tab:blue", "tab:orange", "tab:green"],
        title="",
        xlabel="Patient No",
        ylabel=r"GTV Volume (cm$^{3}$)",
        ylim=(0, 180),
        yticks=np.arange(0, 181, 20),
        save_path=OUT_DIR / "barcharts" / "v_barchart.jpg",
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
