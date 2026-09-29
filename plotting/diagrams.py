"""Schemantic figures that don't plot data."""

from dataclasses import dataclass

import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerBase
from matplotlib.patches import Circle

from .helpers import _save


# ---------------------------------------------------------------------------
# Overlapping circles diagram
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class RegionKey:
    """Legend entry for one region of the two-circle diagram."""

    region: str  # "left", "right", "overlap", "left_only", "right_only"
    color: str


class RegionHandler(HandlerBase):
    """Draws a small two-circle icon with only the entry's region filled"""

    def create_artists(
        self, legend, key, xdescent, ydescent, width, height, fontsize, trans
    ):
        r = height / 2
        cx = width / 2 - xdescent
        cy = height / 2 - ydescent
        left = (cx - r / 2, cy)
        right = (cx + r / 2, cy)
        artists = []

        def circle(center, **kwargs):
            patch = Circle(center, r, transform=trans, **kwargs)
            artists.append(patch)
            return patch

        def clip_to(center):
            return Circle(center, r, transform=trans)

        # Fill the region this entry represents
        if key.region in ("left", "left_only"):
            circle(left, facecolor=key.color, edgecolor="none")
        if key.region in ("right", "right_only"):
            circle(right, facecolor=key.color, edgecolor="none")
        if key.region == "overlap":
            circle(right, facecolor=key.color, edgecolor="none").set_clip_path(
                clip_to(left)
            )

        # For the "only" regions, blank out the overlap again
        if key.region == "left_only":
            circle(right, facecolor="white", edgecolor="none").set_clip_path(
                clip_to(left)
            )
        if key.region == "right_only":
            circle(left, facecolor="white", edgecolor="none").set_clip_path(
                clip_to(right)
            )

        # Outlines of both circles on top
        circle(left, facecolor="none", edgecolor="black", linewidth=1)
        circle(right, facecolor="none", edgecolor="black", linewidth=1)
        return artists


def overlap_circles(
    radius=1.0,
    distance=None,
    # colors=("tab:blue", "tab:orange", "tab:green", "#aec7e8", "#ffbb78"),
    colors=("tab:blue", "tab:orange", "tab:green", "#33a8de", "#faa805"),
    labels=None,
    label_fontsize=14,
    legend_labels=None,
    legend_fontsize=12,
    edgecolor="black",
    linewidth=2,
    ax=None,
    save_path=None,
):
    """
    Draw two equal circles side by side with a colored overlap.

    `distance` is the distance between the centers (defaults to `radius`).
    `colors` are (left, right, overlap).
    `labels` are optional text inside the regions: (left, right, overlap).
    `legend_labels` are optional legend entries, in this order:
        (left circle, right circle, overlap, left part only, right part only).
    Returns (fig, ax).
    """
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
        for x, text in zip((-radius, radius, 0), labels):
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
            handler_map={RegionKey: RegionHandler()},
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
