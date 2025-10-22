from typing import Any

DEBUG = True
ERROR = True

# ANSI color codes:
_RESET = "\033[0m"
_RED = "\033[31m"
_GREEN = "\033[32m"
_YELLOW = "\033[33m"
_BLUE = "\033[34m"
_MAGENTA = "\033[35m"
_CYAN = "\033[36m"
_WHITE = "\033[37m"


def print_debug(message: str) -> None:
    if DEBUG:
        _colourful_print(message, "Debug", _YELLOW)


def print_error(message: str) -> None:
    if ERROR:
        _colourful_print(message, "Error", _RED)


def _colourful_print(message: str, label: str = "", colour_code: str = _WHITE,) -> None:
    """Print a message with a coloured label."""
    prefix = f"{colour_code}{label}:{_RESET}"
    print(f"{prefix} {message}")