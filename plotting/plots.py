"""All registered plots"""

from config import OUT_DIR, PLOT_DATA

from .helpers import bland_altman_plot, grouped_bar_chart, load_excel
from .registry import register


@register("bland-altman", "Bland-Altman plot of SECT vs VNC")
def run_bland_altman():
    SHEET_NAME = "buccal_fat"  # TODO: change file name
    COLUMN_A = "SECT"
    COLUMN_B = "VNC"
    TITLE = SHEET_NAME.replace("_", " ").title()

    plot_data = load_excel(
        PLOT_DATA,
        sheet_name=SHEET_NAME,
        usecols=[COLUMN_A, COLUMN_B],
    )

    _, _, status = bland_altman_plot(
        plot_data[COLUMN_A],
        plot_data[COLUMN_B],
        title=None,
        xlabel="HU Average",
        ylabel=f"{TITLE}: HU Difference",
        save_path=OUT_DIR / "bland_altman" / f"{SHEET_NAME}_bland_altman.jpg",
    )
    print(f"structure: {TITLE}\nstats: {status}")


@register("barchart-f", "Grouped bar chart of F_SECT vs F_VM")
def run_f_barchart():
    # TODO: configs specific about the chart
    SHEET_NAME = "double_bar_chart"
    COLUMN_A = "FSECT"
    COLUMN_B = "FVM"

    df = load_excel(PLOT_DATA, sheet_name=SHEET_NAME)

    grouped_bar_chart(
        df,
        value_cols=[COLUMN_A, COLUMN_B],
        labels=[
            r"V$_{\mathrm{SECT}}$",
            r"V$_{\mathrm{VM}}$",
        ],
        colors=["tab:blue", "tab:orange"],
        title="",
        xlabel="Patient No",
        ylabel="GTV Non-overlap Fraction(%)",
        save_path=OUT_DIR / "barcharts" / "f_barchart.jpg",
    )


@register("barchart-v", "Grouped bar chart of V_SECT, V_VM and V_intersection")
def run_v_barchart():
    # TODO: configs specific about the chart
    SHEET_NAME = "tripple_bar_chart"
    COLUMN_A = "VSECT"
    COLUMN_B = "VVM"
    COLUMN_C = "Vintersection"

    plot_data = load_excel(PLOT_DATA, sheet_name=SHEET_NAME)

    grouped_bar_chart(
        plot_data,
        value_cols=[COLUMN_A, COLUMN_B, COLUMN_C],
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
        yticks=range(0, 181, 20),
        save_path=OUT_DIR / "barcharts" / "v_barchart.jpg",
    )
