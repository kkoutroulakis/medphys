import pytest
from numpy import ptp

from plotting.diagrams import _crescent, _lens, _region_shift

# Arcs are drawn with 100 points, so extreme points are only approximate
TOL = 1e-3


@pytest.mark.parametrize("spacing", [0.5, 1.0, 1.5])
def test_lens_is_symmetric_around_midpoint(spacing):
    r = 1.0
    pts = _lens((-spacing / 2, 0), (spacing / 2, 0), r)
    assert pts[:, 0].min() == pytest.approx(-pts[:, 0].max(), abs=TOL)
    # Lens width is 2r - distance
    assert ptp(pts[:, 0]) == pytest.approx(2 * r - spacing, abs=TOL)


@pytest.mark.parametrize("spacing", [0.5, 1.0, 1.5])
def test_shape_shift_centers_crescent(spacing):
    r = 1.0
    left, right = (-spacing / 2, 0), (spacing / 2, 0)
    pts = _crescent(left, right, r)
    middle = (pts[:, 0].min() + pts[:, 0].max()) / 2
    assert middle + _region_shift("left_only", spacing) * r == pytest.approx(0, abs=TOL)


def test_default_spacing_matches_previous_shifts():
    assert _region_shift("left", 1.0) == 0.5
    assert _region_shift("right_only", 1.0) == -0.75
