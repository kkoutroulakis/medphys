"""Statistical calculations used by the plotting package."""

from dataclasses import dataclass

import pandas as pd


@dataclass
class BlandAltmanStats:
    """Summary statistics for a Bland-Altman analysis."""

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


def bland_altman_stats(a, b):
    """Compute bias and 95% limits of agreement for a - b."""

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
