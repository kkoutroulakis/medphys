"""Every entry in structures.py is complete and usable"""

import inspect

import pytest

from plotting.helpers import bland_altman_plot
from plotting.structures import BA_STRUCTURES

# Parameters an entry may may set; a, b and save_path are set by run_bland_altman
PLOT_SETTINGS = set(inspect.signature(bland_altman_plot).parameters) - {
    "a",
    "b",
    "ax",
    "save_path",
}
STRUCTURES = list(BA_STRUCTURES)


def test_at_least_one_structure():
    assert BA_STRUCTURES


# ---------------------------------------------------------------------------
# Required settings
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("name", STRUCTURES)
def test_value_cols_are_two_different_columns(name):
    cols = BA_STRUCTURES[name].get("value_cols")

    assert isinstance(cols, list | tuple), f"{name}: value_cols missing"
    assert len(cols) == 2, f"{name}: value_cols needs exactly two columns"
    assert all(isinstance(c, str) and c.strip() for c in cols)
    assert cols[0] != cols[1], f"{name}: value_cols compares a column with itself"


@pytest.mark.parametrize("name", STRUCTURES)
@pytest.mark.parametrize("key", ["xlabel", "ylabel"])
def test_axis_labels_are_present(name, key):
    """Required: without them the plot falls back to English default labels."""

    value = BA_STRUCTURES[name].get(key)

    assert isinstance(value, str) and value.strip(), f"{name}: {key} missing"


@pytest.mark.parametrize("name", STRUCTURES)
def test_title_is_optional_but_not_empty(name):
    """A title may be left out or set to be None; if it is text, it must not be blank."""

    title = BA_STRUCTURES[name].get("title")

    assert title is None or (isinstance(title, str) and title.strip()), (
        f"{name}: title is set but empty; use None for no title"
    )


# ---------------------------------------------------------------------------
# No unknown keys (typos like ylable)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("name", STRUCTURES)
def test_keys_are_plot_settings(name):
    unknown = set(BA_STRUCTURES[name]) - {"value_cols"} - PLOT_SETTINGS

    assert not unknown, (
        f"{name}: unknown settings {sorted(unknown)}; ",
        f"allowed: value_cols, {', '.join(sorted(PLOT_SETTINGS))}",
    )


# ---------------------------------------------------------------------------
# Limits are in order and ticks fall inside them
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("name", STRUCTURES)
@pytest.mark.parametrize("axis", ["x", "y"])
def test_ticks_inside_limits(name, axis):
    entry = BA_STRUCTURES[name]
    lim = entry.get(f"{axis}lim")
    ticks = entry.get(f"{axis}ticks")

    if lim is None:
        return  # autoscaled: nothing to check
    low, high = lim

    assert low < high, f"{name}: {axis}lim must go from low to high"

    if ticks is not None:
        outside = [t for t in ticks if not low <= t <= high]

        assert not outside, f"{name}: {axis}ticks {outside} outside {axis}lim {lim}"
