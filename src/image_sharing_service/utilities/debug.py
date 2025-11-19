from socket import socket

DEBUG = False
ERROR = True

# ANSI color codes for terminal output
_RESET = "\033[0m"
_RED = "\033[31m"
_GREEN = "\033[32m"
_YELLOW = "\033[33m"
_BLUE = "\033[34m"
_MAGENTA = "\033[35m"
_CYAN = "\033[36m"
_WHITE = "\033[37m"


def print_command_report(
    sock: socket,
    command: str,
    success: bool,
    filename: str | None = None,
    error_message: str | None = None,
) -> None:
    """Print a formatted report of the outcome of a client command."""
    _SUCCESS_VAL = "SUCCESS"
    _FAILURE_VAL = "FAILURE"

    status = _SUCCESS_VAL if success else _FAILURE_VAL
    host = sock.getpeername()
    parts = [str(host), command]
    if filename:
        parts.append(filename)
    parts.append(status)

    report = "\t".join(parts)
    if not success and error_message:
        report += f": {error_message}."
    print(report)


def print_debug(message: str) -> None:
    """Print a debug message if DEBUG is enabled."""
    if DEBUG:
        _colourful_print(message, "Debug", _YELLOW)


def print_error(message: str) -> None:
    """Print an error message if ERROR is enabled."""
    if ERROR:
        _colourful_print(message, "Error", _RED)


def _colourful_print(message: str, label: str = "", colour_code: str = _WHITE) -> None:
    """Print a message with a coloured label."""
    prefix = f"{colour_code}{label}:{_RESET}"
    print(f"{prefix} {message}")
