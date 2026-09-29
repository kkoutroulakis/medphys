"""Registry that maps a command-line key to a plot function"""

from collections.abc import Callable

PLOTS: dict[str, Callable[[], None]] = {}
DESCRIPTIONS: dict[str, str] = {}


def register(name: str, desc: str = ""):
    """Decorator that makes a function runnable"""

    def decorator(func):
        if name in PLOTS:
            raise ValueError(f"Plot key '{name}' is already registered")

        PLOTS[name] = func
        DESCRIPTIONS[name] = desc
        return func

    return decorator
