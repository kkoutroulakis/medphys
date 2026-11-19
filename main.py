"""
Command-line entry point: uv run main.py <plot-key> [option]

In the plot list, <a | b> marks a required option and [a | b] an optional one.
"""

import argparse

from plotting.registry import DESCRIPTIONS, OPTIONS, OPTIONS_REQUIRED, PLOTS


def run(plot_key: str, option: str | None = None) -> None:
    if option is None:
        PLOTS[plot_key]()
    else:
        PLOTS[plot_key](option)


def describe(key: str) -> str:
    text = DESCRIPTIONS[key]
    if OPTIONS[key]:
        choices = " | ".join(OPTIONS[key])
        text += f" <{choices}>" if OPTIONS_REQUIRED[key] else f" [{choices}]"
    return text


def parse_args() -> argparse.Namespace:
    available = "\n".join(f" {k:<18} {describe(k)}" for k in PLOTS)
    parser = argparse.ArgumentParser(
        description="Generate figure images from Excel data.",
        epilog=f"Available plots:\n{available}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("plot", choices=list(PLOTS), help="Which plot to generate")
    parser.add_argument("option", nargs="?", help="Variant of the plot, if it has any")
    args = parser.parse_args()

    valid = OPTIONS[args.plot]
    if args.option is None:
        if OPTIONS_REQUIRED[args.plot]:
            parser.error(
                f"'{args.plot}' needs an option, choose from: {', '.join(valid)}"
            )
    else:
        if not valid:
            parser.error(f"'{args.plot}' has no options")
        if args.option not in valid:
            parser.error(
                f"invalid option '{args.option}' for '{args.plot}', "
                f"choose from: {', '.join(valid)}"
            )
    return args


if __name__ == "__main__":
    args = parse_args()
    run(args.plot, args.option)
