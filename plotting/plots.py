"""All registered plots"""

from config import OUT_DIR, PLOT_DATA

from .helpers import bland_altman_plot, load_excel
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
        save_path=OUT_DIR / f"{SHEET_NAME}_bland_altman.jpg",
    )
    print(f"structure: {TITLE}\nstats: {status}\n")
