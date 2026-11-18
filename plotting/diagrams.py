"""Schematic figures that don't plot data."""

from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.legend_handler import HandlerBase
from matplotlib.patches import Circle, Polygon

from config import OVERLAP_CIRCLE_COLORS

from .helpers import _save

# ---------------------------------------------------------------------------
# Overlapping circles diagram
# ---------------------------------------------------------------------------
# Legend styles
# "shape": each region drawn on its own, centered, with its own border
# "context": each region shown in place inside both circle outlines
LEGEND_STYLES = ("shape", "context")

# Horizontal shift that centers each region's shape in the legend icon
# so all "shape" icons line up in one column
_REGION_SHIFT = {
    "left": 0.5,
    "right": -0.5,
    "overlap": 0.0,
    "left_only": 0.75,
    "right_only": -0.75,
}


@dataclass(frozen=True)
class RegionKey:
    """Legend entry for one region of the two-circle diagram."""

    region: str  # "left", "right", "overlap", "left_only", "right_only"
    color: str


def _arc(center, r, start, end, sign, n=100):
    """Points along a circle arc; sign=-1 mirrors it horizontally."""

    t = np.linspace(start, end, n)
    return np.column_stack(
        [center[0] + sign * r * np.cos(t), center[1] + r * np.sin(t)]
    )


def _crescent(own, other, r):
    """Outline of the part of the `own` circle outside the `other` one."""

    sign = 1 if other[0] > own[0] else -1
    alpha = np.arccos(abs(other[0] - own[0]) / (2 * r))
    return np.vstack(
        [
            _arc(own, r, alpha, 2 * np.pi - alpha, sign),
            _arc(other, r, np.pi + alpha, np.pi - alpha, sign),
        ]
    )


def _lens(left, rigth, r):
    """Outline of the overlap between two circles."""

    alpha = np.arccos((rigth[0] - left[0]) / (2 * r))
    return np.vstack(
        [
            _arc(left, r, -alpha, alpha, 1),
            _arc(rigth, r, np.pi - alpha, np.pi + alpha, 1),
        ]
    )


class RegionHandler(HandlerBase):
    """Draws a legend icon for one region, in the given legend style."""

    def __init__(self, style="shape", **kwargs):
        super().__init__(**kwargs)
        self.style = style

    def create_artists(
        self, legend, key, xdescent, ydescent, width, height, fontsize, trans
    ):
        r = height / 2
        shift = _REGION_SHIFT[key.region] if self.style == "shape" else 0
        cx = width / 2 - xdescent + shift * r
        cy = height / 2 - ydescent
        left = (cx - r / 2, cy)
        right = (cx + r / 2, cy)

        # "shape" borders the region itself; "context" borders the circles
        if self.style == "shape":
            edge = {"edgecolor": "black", "linewidth": 1}
        else:
            edge = {"edgecolor": "none"}

        # The region as a single shape
        if key.region == "left":
            region = Circle(left, r, **edge)
        elif key.region == "right":
            region = Circle(right, r, **edge)
        elif key.region == "overlap":
            region = Polygon(_lens(left, right, r), closed=True, **edge)
        elif key.region == "left_only":
            region = Polygon(_crescent(left, right, r), closed=True, **edge)
        else:  # "right_only"
            region = Polygon(_crescent(right, left, r), closed=True, **edge)

        region.set_facecolor(key.color)
        region.set_transform(trans)
        artists = [region]

        # Both circle outlines on top, to show where the region sits
        if self.style == "context":
            for center in (left, right):
                artists.append(
                    Circle(
                        center,
                        r,
                        transform=trans,
                        facecolor="none",
                        edgecolor="black",
                        linewidth=1,
                    )
                )
        return artists


def overlap_circles(
    radius=1.0,
    distance=None,
    colors=OVERLAP_CIRCLE_COLORS,
    labels=None,
    label_fontsize=14,
    legend_labels=None,
    legend_style="shape",
    legend_fontsize=12,
    edgecolor="black",
    linewidth=2,
    ax=None,
    save_path=None,
):
    """
    Draw two equal circles side by side with a colored overlap.

    Parameters
    ----------
    radius: float
        Radius of both circles.
    distance: float
        Distance between circle centers. Defaults to radius.
    colors: tuple
        Colors in the order (left, right, overlap, left_only, right_only).
    labels: tuple, optional
        Text labels for left, right and overlap regions.
    legend_labels: tuple, optional
        Legend labels in the order (left, right, overlap, left_only, right_only).
    legend_style: str
        "shape" (each region on its own, with its own border)
        "context" (each region inside both circle outlines)

    Returns
    -------
    fig, ax
        Matplotlib figure and axes.
    """

    if legend_style not in LEGEND_STYLES:
        raise ValueError(
            f"legend_style must be one of {LEGEND_STYLES}, got {legend_style!r}"
        )

    distance = radius if distance is None else distance
    left = (-distance / 2, 0)
    right = (distance / 2, 0)

    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))
    else:
        fig = ax.figure

    # Filled circles
    ax.add_patch(Circle(left, radius, facecolor=colors[3], edgecolor="none"))
    ax.add_patch(Circle(right, radius, facecolor=colors[4], edgecolor="none"))

    # Overlap: the right circle, clipped to the inside of the left circle
    overlap = Circle(right, radius, facecolor=colors[2], edgecolor="none")
    ax.add_patch(overlap)
    overlap.set_clip_path(Circle(left, radius, transform=ax.transData))

    # Outlines drawn last, so they sit on top of all fills
    for center in (left, right):
        ax.add_patch(
            Circle(
                center,
                radius,
                facecolor="none",
                edgecolor=edgecolor,
                linewidth=linewidth,
            )
        )

    # Optional labels inside the regions
    if labels is not None:
        for x, text in zip((left[0], right[0], 0), labels):
            ax.text(
                x,
                0,
                text,
                ha="center",
                va="center",
                fontsize=label_fontsize,
                fontweight="bold",
            )

    # Optional legend with region icons, placed to the right of the diagram
    if legend_labels is not None:
        keys = [
            RegionKey("left", colors[0]),
            RegionKey("right", colors[1]),
            RegionKey("overlap", colors[2]),
            RegionKey("left_only", colors[3]),
            RegionKey("right_only", colors[4]),
        ]
        ax.legend(
            keys,
            legend_labels,
            handler_map={RegionKey: RegionHandler(style=legend_style)},
            handlelength=3,
            handleheight=2,
            fontsize=legend_fontsize,
            loc="center left",
            bbox_to_anchor=(1.02, 0.5),
            frameon=False,
        )

    # Equal aspect keeps the circles round; hide the axes
    pad = 0.1 * radius
    ax.set_xlim(-distance / 2 - radius - pad, distance / 2 + radius + pad)
    ax.set_ylim(-radius - pad, radius + pad)
    ax.set_aspect("equal")
    ax.axis("off")

    _save(fig, save_path)
    return fig, ax
