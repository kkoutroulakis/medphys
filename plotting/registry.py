"""Registry that maps a command-line key to a plot function"""

from collections.abc import Callable

PLOTS: dict[str, Callable[..., None]] = {}
DESCRIPTIONS: dict[str, str] = {}
OPTIONS: dict[str, tuple[str, ...]] = {}
OPTIONS_REQUIRED: dict[str, bool] = {}


def register(
    name: str,
    description: str = "",
    options: tuple[str, ...] = (),
    option_required: bool = False,
):
    """
    Decorator that makes a function runnable.

    `options` lists the accepted values for the optional second argument
    `option_required` makes the user pass one option
    """

    def decorator(func):
        if name in PLOTS:
            raise ValueError(f"Plot key '{name}' is already registered")
        if option_required and not options:
            raise ValueError(f"Plot '{name}' requires an option but lists none")

        PLOTS[name] = func
        DESCRIPTIONS[name] = description
        OPTIONS[name] = tuple(options)
        OPTIONS_REQUIRED[name] = option_required
        return func

    return decorator
