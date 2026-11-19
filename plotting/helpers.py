"""Reusable plotting helpers: load data from Excel, draw plots"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .statistics import bland_altman_stats
from .style import COLORS


# ---------------------------------------------------------------------------
# Load excel
# ---------------------------------------------------------------------------
def load_excel(path, sheet_name=0, skiprows=0, usecols=None, nrows=None):
    """Read table from excel sheet and strip spaces from the heades"""
    data = pd.read_excel(
        path, sheet_name=sheet_name, skiprows=skiprows, usecols=usecols, nrows=nrows
    )
    data.columns = data.columns.astype(str).str.strip()
    return data


# ---------------------------------------------------------------------------
# Bland-Altman
# ---------------------------------------------------------------------------
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

    fig, ax, own_fig = _get_axes(ax)

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
                fontsize=plt.rcParams["ytick.labelsize"],
                clip_on=False,
            )

    _style_axes(ax, title, xlabel, ylabel, xlim, ylim, xticks, yticks)
    _save(fig, save_path, close=own_fig)

    return fig, ax, stats


# ---------------------------------------------------------------------------
# Grouped bar charts
# ---------------------------------------------------------------------------
def grouped_bar_chart(
    df,
    value_cols,
    category_col=None,
    categories=None,
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

    fig, ax, own_fig = _get_axes(ax)

    labels = labels or value_cols

    if categories is not None:
        if len(categories) != len(df):
            raise ValueError(f"Got {len(categories)} categories for {len(df)} rows.")
        tick_labels = categories
    elif category_col is not None:
        tick_labels = df[category_col]
    else:
        tick_labels = range(1, len(df) + 1)

    n_series = len(value_cols)
    x = np.arange(len(df))
    width = bar_width / n_series

    for i, (col, label) in enumerate(zip(value_cols, labels, strict=True)):
        offset = (i - (n_series - 1) / 2) * width
        ax.bar(
            x + offset,
            df[col],
            width,
            label=label,
            color=None if colors is None else colors[i],
        )

    ax.set_xticks(x)
    ax.set_xticklabels(tick_labels)
    ax.set_xlim(-0.6, len(df) - 0.4)
    ax.grid(axis="x", visible=False)
    ax.legend(prop={"weight": "bold"})

    _style_axes(ax, title, xlabel, ylabel, None, ylim, None, yticks)
    _save(fig, save_path, close=own_fig)

    return fig, ax


# ---------------------------------------------------------------------------
# Internal helpers (shared styling and saving)
# ---------------------------------------------------------------------------
def _get_axes(ax):
    """Return (fig, ax, own_fig); own_fig is True when a new figure was made."""

    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))
        return fig, ax, True
    return ax.figure, ax, False


def _style_axes(ax, title, xlabel, ylabel, xlim, ylim, xticks, yticks, xrotation=0):
    """Per-figure text, limits, and ticks; the general look comes from style.py"""

    if title is not None:
        ax.set_title(title)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

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

    plt.setp(
        ax.get_xticklabels() + ax.get_yticklabels(),
        fontweight="bold",
    )


def _save(fig, save_path, close=True, dpi=300, quality=95, bbox_inches="tight"):
    """
    Save the figure if 'save_path is given'.

    The figure is closed afterwards only when 'close' is True
    """
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

    if close:
        plt.close(fig)
