"""Shared test setup: no windows, no writes to the real figures/ folder."""

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest

from plotting import plots
from plotting.structures import BA_STRUCTURES

matplotlib.use("Agg")  # draw without opening windows

# Sheets and columns the bar chart plots and read (see plottings/plots.py)
BAR_SHEETS = {
    "f_plot": ["FSECT", "FVM"],
    "tripple_bar_chart": ["VSECT", "VVM", "Vintersection"],
}


@pytest.fixture(autouse=True)
def _close_figures():
    yield
    plt.close()


@pytest.fixture(autouse=True)
def out_dir(tmp_path, monkeypatch):
    """Send every figure to a temporary folder instead of the real figures/."""

    path = tmp_path / "figures"
    monkeypatch.setattr(plots, "OUT_DIR", path)
    return path


@pytest.fixture
def fake_data(tmp_path, monkeypatch):
    """Small made-up Excel files in the layout the plots expect."""

    rng = np.random.default_rng(0)
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    ba_file = data_dir / "bland_altman_data.xlsx"
    with pd.ExcelWriter(ba_file) as writer:
        for name, entry in BA_STRUCTURES.items():
            col_a, col_b = entry["value_cols"]
            ref = rng.uniform(40, 56, 10)
            df = pd.DataFrame({col_a: ref, col_b: ref - rng.normal(1, 0.5, 10)})
            df.to_excel(writer, sheet_name=name, index=False)

    bar_file = data_dir / "bar_charts_data.xlsx"
    with pd.ExcelWriter(bar_file) as writer:
        for sheet, cols in BAR_SHEETS.items():
            df = pd.DataFrame({col: rng.uniform(5, 50, 6) for col in cols})
            df.to_excel(writer, sheet_name=sheet, index=False)

    monkeypatch.setattr(plots, "BLAND_ALTMAN_DATA", ba_file)
    monkeypatch.setattr(plots, "BAR_CHART_DATA", bar_file)
    return ba_file, bar_file
