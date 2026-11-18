"""Registry that maps a command-line key to a plot function"""

from collections.abc import Callable

PLOTS: dict[str, Callable[[...], None]] = {}
DESCRIPTIONS: dict[str, str] = {}
OPTIONS: dict[str, tuple[str, ...]] = {}


def register(name: str, description: str = "", options: tuple[str, ...] = ()):
    """
    Decorator that makes a function runnable.

    `options` lists the accepted values for the oprional second argument
    """

    def decorator(func):
        if name in PLOTS:
            raise ValueError(f"Plot key '{name}' is already registered")

        PLOTS[name] = func
        DESCRIPTIONS[name] = description
        OPTIONS[name] = tuple(options)
        return func

    return decorator
