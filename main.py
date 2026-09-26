"""command-line entry point: uv run main.py <plot-key>"""

import argparse

from plotting.registry import DESCRIPTIONS, PLOTS


def run(key: str) -> None:
    p = PLOTS.get(key)
    p()


def parse_args() -> argparse.Namespace:
    available = "\n".join(f" {k:<15} {v}" for k, v in DESCRIPTIONS.items())
    parser = argparse.ArgumentParser(
        description="Generate plots from excel data.",
        epilog=f"Available plots:\n{available}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("plot", choices=[*PLOTS], help="Which plot to geneate")
    return parser.parse_args()


if __name__ == "__main__":
    run(parse_args().plot)
