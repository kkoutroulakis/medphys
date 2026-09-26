"""Reusable plotting helpers: load data from Excel, draw plots"""

from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


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
@dataclass
class BlandAltmanStats:
    bias: float
    sd: float
    lower_loa: float
    upper_loa: float
    n: int

    def __str__(self):
        return (
            f"n = {self.n}\n"
            f"Mean difference (bias): {self.bias:.3f}\n"
            f"SD of MD: {self.sd:.3f}\n"
            f"Limits of agreement: {self.lower_loa:.3f} to {self.upper_loa:.3f}\n"
        )


def bland_altam_stats(a, b):
    """
    Compute bias and 95% limits of agreement for a - b.
    """

    data = pd.DataFrame({"a": a, "b": b}).dropna()
    diff = data["a"] - data["b"]  # x-axis: difference between methods
    bias = diff.mean()
    sd = diff.std(ddof=1)  # standard deviation of the differences

    return BlandAltmanStats(
        bias=bias,
        sd=sd,
        lower_loa=bias - 1.96 * sd,
        upper_loa=bias + 1.96 * sd,
        n=len(diff),
    )


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
    stats = bland_altam_stats(data["a"], data["b"])

    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))
    else:
        fig = ax.figure

    # ax.scatter(mean, diff, alpha=0.7, edgecolor="k")
    ax.scatter(mean, diff, color="red", marker="s")
    ax.axhline(
        stats.bias, color="black", linestyle="-", label=f"Mean diff = {stats.bias:.2f}"
    )
    ax.axhline(
        stats.upper_loa,
        color="black",
        linestyle=":",
        label=f"+1.96 SD = {stats.upper_loa:.2f}",
    )
    ax.axhline(
        stats.lower_loa,
        color="black",
        linestyle=":",
        label=f"-1.96 SD = {stats.lower_loa:.2f}",
    )
    # ax.axhline(0, color="grey", linewidth="0.8")
    # ax.legend()

    _style_axes(ax, title, xlabel, ylabel, xlim, ylim, xticks, yticks)
    _save(fig, save_path)

    return fig, ax, stats


# ---------------------------------------------------------------------------
# Internal helpers (shared styling and saving)
# ---------------------------------------------------------------------------
def _style_axes(ax, title, xlabel, ylabel, xlim, ylim, xticks, yticks):
    if title is not None:
        ax.set_title(title)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    if xlim is not None:
        ax.set_xlim(xlim)
    if ylim is not None:
        ax.set_ylim(ylim)
    if xticks is not None:
        ax.set_xticks(xticks)
    if yticks is not None:
        ax.set_yticks(yticks)
    # ax.grid(alpha=0.3)

    # Show only left and bottom axis lines
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Bold title and axis labels
    ax.title.set_fontweight("bold")
    ax.xaxis.label.set_fontweight("bold")
    ax.yaxis.label.set_fontweight("bold")

    # Bold tick values
    plt.setp(ax.get_xticklabels() + ax.get_yticklabels(), fontweight="bold")

    # Thicker axis lines and tick marks
    ax.spines["left"].set_linewidth(2)
    ax.spines["bottom"].set_linewidth(2)
    ax.tick_params(width=2, length=6)


def _save(fig, save_path):
    if save_path is not None:
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        fig.tight_layout()
        # fig.savefig(save_path, dpi=300) # TODO: for .png
        fig.savefig(save_path, dpi=300, pil_kwargs={"quality": 95})
