"""The figures show the right data."""

import math

import numpy as np
import pandas as pd
import pytest

from plotting.helpers import bland_altman_plot, grouped_bar_chart

# Differences a - b are [1, 2, 3, 4, 5]: mean 3, sample SD sqrt(2.5)
A = [11.0, 12.0, 13.0, 14.0, 15.0]
B = [10.0, 10.0, 10.0, 10.0, 10.0]
SD = math.sqrt(2.5)
BIAS = 3.0
UPPER = BIAS + 1.96 * SD
LOWER = BIAS - 1.96 * SD


def scatter_points(ax):
    return np.asarray(ax.collections[0].get_offsets())


# ---------------------------------------------------------------------------
# x = mean of the two methods, y = first minus second
# ---------------------------------------------------------------------------


def test_points_are_mean_and_a_minus_b():
    _, ax, _ = bland_altman_plot(A, B)
    points = scatter_points(ax)

    np.testing.assert_allclose(points[:, 0], [10.5, 11.0, 11.5, 12.0, 12.5])
    np.testing.assert_allclose(points[:, 1], [1, 2, 3, 4, 5])


def test_swapping_methods_flips_the_sign():
    _, ax, stats = bland_altman_plot(B, A)

    assert stats.bias == pytest.approx(-BIAS)
    np.testing.assert_allclose(scatter_points(ax)[:, 1], [-1, -2, -3, -4, -5])


# ---------------------------------------------------------------------------
# Bias and limit-of-agreement lines and labels match the statistics
# ---------------------------------------------------------------------------


def test_lines_are_at_bias_and_limits():
    _, ax, stats = bland_altman_plot(A, B)
    line_ys = sorted(line.get_ydata()[0] for line in ax.lines)

    assert line_ys == pytest.approx([LOWER, BIAS, UPPER])
    assert (stats.lower_loa, stats.bias, stats.upper_loa) == pytest.approx(
        (LOWER, BIAS, UPPER)
    )


def test_labels_show_values_next_to_their_lines():
    _, ax, _ = bland_altman_plot(A, B)
    labels = {t.get_text(): t.get_position()[1] for t in ax.texts}

    assert labels == {
        f"+1.96 SD\n{UPPER:.2f}": pytest.approx(UPPER),
        f"Mean\n{BIAS:.2f}": pytest.approx(BIAS),
        f"-1.96 SD\n{LOWER:.2f}": pytest.approx(LOWER),
    }


# ---------------------------------------------------------------------------
# Rows with missing value are left out of points and statistics alike
# ---------------------------------------------------------------------------


def test_missing_values_are_left_out_consistently():
    a = [11, 12, math.nan, 14, 15]
    b = [10, 10, 10, math.nan, 10]

    _, ax, stats = bland_altman_plot(a, b)
    points = scatter_points(ax)

    assert len(points) == stats.n == 3
    assert stats.bias == pytest.approx(8 / 3)
    np.testing.assert_allclose(points[:, 1], [1, 2, 5])


# ---------------------------------------------------------------------------
# Bar heights, patient order and labels match the data
# ---------------------------------------------------------------------------


BARS = pd.DataFrame({"x": [5, 1, 3], "y": [2, 8, 4], "z": [7, 6, 9]})


def test_bar_heights_match_each_column():
    _, ax = grouped_bar_chart(BARS, ["x", "y", "z"])

    assert len(ax.containers) == 3
    for container, col in zip(ax.containers, ["x", "y", "z"], strict=True):
        assert [bar.get_height() for bar in container] == BARS[col].tolist()


def test_bars_are_ordered_by_patient_then_column():
    _, ax = grouped_bar_chart(BARS, ["x", "y", "z"])

    # Rows: series (column order), columns: patients
    lefts = np.array([[bar.get_x() for bar in c] for c in ax.containers])
    assert (np.diff(lefts, axis=1) > 0).all(), "patients not left to right"
    assert (np.diff(lefts, axis=0) > 0).all(), "series not in column order"

    # Each patient's group ends before the next one starts
    rights = lefts + np.array([[bar.get_width() for bar in c] for c in ax.containers])
    assert (rights[-1, :-1] <= lefts[0, 1:]).all(), "patients groups overlap"


def test_bar_legend_and_patient_labels():
    _, ax = grouped_bar_chart(
        BARS,
        ["x", "y", "z"],
        labels=["X", "Y", "Z"],
    )

    assert [t.get_text() for t in ax.get_legend().get_texts()] == ["X", "Y", "Z"]
    assert [t.get_text() for t in ax.get_xticklabels()] == ["1", "2", "3"]


def test_bar_chart_rejects_mismatched_labels():
    with pytest.raises(ValueError):
        grouped_bar_chart(BARS, ["x", "y", "z"], labels=["x", "y"])
