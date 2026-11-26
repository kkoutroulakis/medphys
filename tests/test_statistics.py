import math

import numpy as np
import pytest

from plotting.statistics import bland_altman_stats


def test_known_values():
    # Differences a - b are [1, 2, 3, 4, 5]: mean 3, sample SD sqrt(2.5)
    a = [11, 12, 13, 14, 15]
    b = [10, 10, 10, 10, 10]

    stats = bland_altman_stats(a, b)
    sd = math.sqrt(2.5)

    assert stats.n == 5
    assert stats.bias == pytest.approx(3.0)
    assert stats.sd == pytest.approx(sd)
    assert stats.lower_loa == pytest.approx(3.0 - 1.96 * sd)
    assert stats.upper_loa == pytest.approx(3.0 + 1.96 * sd)


def test_direction_is_a_minus_b():
    a = [1, 2, 3]
    b = [2, 3, 4]

    stats = bland_altman_stats(a, b)

    assert stats.bias == pytest.approx(-1.0)
    assert stats.sd == pytest.approx(0.0)


def test_rows_with_missing_values_are_dropped():
    a = [11, 12, np.nan, 14, 15]
    b = [10, 10, 10, np.nan, 10]

    stats = bland_altman_stats(a, b)

    # Only rows 0, 1 and 4 remain: differences [1, 2, 5]
    assert stats.n == 3
    assert stats.bias == pytest.approx(8 / 3)
