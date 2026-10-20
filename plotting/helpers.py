"""Reusable plotting helpers: load data from Excel, draw plots"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from config import AXIS_STYLES, COLORS

from .statistics import bland_altman_stats

# ---------------------------------------
# Global style for plots
# ---------------------------------------
plt.rcParams["font.family"] = ["Arial", "Times New Roman"]


# ---------------------------------------
# Load excel
# ---------------------------------------
def load_excel(path, sheet_name=0, skiprows=0, usecols=None, nrows=None):
    """Read table from excel sheet and strip spaces from the heades"""
    data = pd.read_excel(
        path, sheet_name=sheet_name, skiprows=skiprows, usecols=usecols, nrows=nrows
    )
    data.columns = data.columns.astype(str).str.strip()
    return data


# ---------------------------------------
# Bland-Altman
# ---------------------------------------
def bland_altman_plot(
    a,
    b,
    title=None,
    xlabel="Mean of the two methods",
    ylabel="Difference of the two methods",
    xlim=None,
    ylim=None,
    xticks=None,
    yticks=None,
    show_loa_labels=True,
    ax=None,
    save_path=None,
):
    """
    Draw a Bland-Altman plot of a - b

    Pass 'ax' to draw into an existing subplot; otherwise a new figure is made.
    Returns (fig, ax, stats)
    """

    data = pd.DataFrame({"a": a, "b": b}).dropna()

    mean = (data["a"] + data["b"]) / 2
    diff = data["a"] - data["b"]

    stats = bland_altman_stats(data["a"], data["b"])

    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))
    else:
        fig = ax.figure

    ax.scatter(mean, diff, color=COLORS["red"], marker="s")

    ax.axhline(stats.bias, color=COLORS["black"], linestyle="-")
    ax.axhline(stats.upper_loa, color=COLORS["black"], linestyle=":")
    ax.axhline(stats.lower_loa, color=COLORS["black"], linestyle=":")

    if show_loa_labels:
        for value, label in [
            (stats.upper_loa, f"+1.96 SD\n{stats.upper_loa:.2f}"),
            (stats.bias, f"Mean\n{stats.bias:.2f}"),
            (stats.lower_loa, f"-1.96 SD\n{stats.lower_loa:.2f}"),
        ]:
            ax.text(
                1.00,
                value,
                label,
                transform=ax.get_yaxis_transform(),
                ha="right",
                va="center_baseline",
                fontsize=AXIS_STYLES["tick_fontsize"],
                clip_on=False,
            )

    _style_axes(ax, title, xlabel, ylabel, xlim, ylim, xticks, yticks)
    _save(fig, save_path)

    return fig, ax, stats


# ---------------------------------------------------------------------------
# Grouped bar charts
# ---------------------------------------------------------------------------
def grouped_bar_chart(
    df,
    value_cols,
    category_col=None,
    labels=None,
    colors=None,
    title=None,
    xlabel="",
    ylabel="Value",
    ylim=None,
    yticks=None,
    bar_width=0.6,
    ax=None,
    save_path=None,
):
    """
    Draw one group of bars per row, with one bar per column in 'value_cols'
    """

    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))
    else:
        fig = ax.figure

    labels = labels or value_cols
    categories = df[category_col] if category_col is not None else range(1, len(df) + 1)
    n_series = len(value_cols)
    x = np.arange(len(df))
    width = bar_width / n_series

    for i, (col, label) in enumerate(zip(value_cols, labels)):
        offset = (i - (n_series - 1) / 2) * width
        ax.bar(
            x + offset,
            df[col],
            width,
            label=label,
            color=None if colors is None else colors[i],
        )

    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.set_xlim(-0.6, len(df) - 0.4)
    ax.grid(axis="x", visible=False)
    ax.legend(fontsize=AXIS_STYLES["legend"])

    _style_axes(ax, title, xlabel, ylabel, None, ylim, None, yticks)
    _save(fig, save_path)

    return fig, ax


# ---------------------------------------------------------------------------
# Internal helpers (shared styling and saving)
# ---------------------------------------------------------------------------
def _style_axes(ax, title, xlabel, ylabel, xlim, ylim, xticks, yticks, xrotation=0):
    # Title
    if title is not None:
        ax.set_title(
            title,
            fontsize=AXIS_STYLES["fontsize"],
            fontweight=AXIS_STYLES["fontweight"],
        )

    # Axis labels
    ax.set_xlabel(
        xlabel, fontsize=AXIS_STYLES["fontsize"], fontweight=AXIS_STYLES["fontweight"]
    )
    ax.set_ylabel(
        ylabel, fontsize=AXIS_STYLES["fontsize"], fontweight=AXIS_STYLES["fontweight"]
    )

    # Axis limits
    if xlim is not None:
        ax.set_xlim(xlim)
    if ylim is not None:
        ax.set_ylim(ylim)

    # Axis ticks
    if xticks is not None:
        ax.set_xticks(xticks)
    if yticks is not None:
        ax.set_yticks(yticks)

    # Rotate x-axis tick label when needed
    ax.tick_params(axis="x", labelrotation=xrotation)

    # Bold tick labels and set their font size
    ax.tick_params(
        axis="both",
        width=AXIS_STYLES["tick_width"],
        length=AXIS_STYLES["tick_length"],
        labelsize=AXIS_STYLES["fontsize"],
    )
    plt.setp(
        ax.get_xticklabels() + ax.get_yticklabels(),
        fontweight=AXIS_STYLES["fontweight"],
    )

    # Show only left and bottom axis lines
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Thicker axis lines and tick marks
    ax.spines["left"].set_linewidth(AXIS_STYLES["spine_linewidth"])
    ax.spines["bottom"].set_linewidth(AXIS_STYLES["spine_linewidth"])

    # Optional grid
    # ax.grid(alpha=0.3)


def _save(fig, save_path, dpi=300, quality=95, bbox_inches="tight"):
    if save_path is None:
        return

    save_path = Path(save_path)
    save_path.parent.mkdir(parents=True, exist_ok=True)

    fig.tight_layout()

    save_kwargs = {"dpi": dpi, "bbox_inches": bbox_inches}

    # JPEG specific options
    if save_path.suffix.lower() in {".jpg", ".jpeg"}:
        save_kwargs["pil_kwargs"] = {"quality": quality}

    fig.savefig(save_path, **save_kwargs)
